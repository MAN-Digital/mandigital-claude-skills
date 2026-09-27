#!/usr/bin/env bash
# Guided config-driven HubSpot deploy. ZIP-first, evidence-checked, explicit auth.
# Usage: deploy.sh [--portal ID] --zip FILE --config portals.yaml [--token T] [--dry-run] [--yes]
# Env: HS_BIN (default hs), CURL_BIN (default curl), HS_TOKEN (token fallback)
# Exit codes: 0 ok, 1 failed check, 2 usage/unknown portal, 3 authorization required.
# Step 4 note: live `hubspot` CLI has no cms/api subcommands (CRM-only CLI,
# per references/api-playbook.md §1), so content probes use verified REST paths
# via curl (see CONTENT_PROBES).
set -euo pipefail
exec python3 - "$@" <<'PYEOF'
import getpass, json, os, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone

HS_BIN = os.environ.get("HS_BIN", "hs")
CURL_BIN = os.environ.get("CURL_BIN", "curl")
CONTENT_PROBES = [  # verified REST paths per references/api-playbook.md §1
    ("pages", "/cms/v3/pages/site-pages"),
    ("blog_posts", "/cms/v3/blogs/posts"),
    ("forms", "/marketing/v3/forms"),
]

def die(msg, code=1):
    print(f"deploy.sh: {msg}", file=sys.stderr); sys.exit(code)

def parse(argv):
    opts = {"portal": None, "zip": None, "config": None, "token": os.environ.get("HS_TOKEN"),
            "dry_run": False, "yes": False}
    valued = {"--portal": "portal", "--zip": "zip", "--config": "config", "--token": "token"}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in valued:
            if i + 1 >= len(argv):
                die(f"missing value for {a}", 2)
            opts[valued[a]] = argv[i + 1]; i += 2
        elif a == "--dry-run": opts["dry_run"] = True; i += 1
        elif a == "--yes": opts["yes"] = True; i += 1
        else: die(f"unknown flag: {a}", 2)
    if not opts["zip"] or not opts["config"]:
        die("usage: deploy.sh [--portal ID] --zip FILE --config portals.yaml [--token T] [--dry-run] [--yes]", 2)
    return opts

def load_config(path):
    try:
        import yaml
    except ImportError:
        die("PyYAML missing: run: pip3 install --user pyyaml (add --break-system-packages if refused)")
    try:
        with open(path, encoding="utf-8") as handle:
            data = yaml.safe_load(handle)
        portals = {p["id"]: p for p in data.get("portals", [])}
    except (yaml.YAMLError, AttributeError, KeyError, TypeError) as exc:
        die(f"invalid config: {type(exc).__name__}")
    if sum(1 for p in portals.values() if p.get("staging")) != 1:
        die("config must flag exactly one staging portal")
    return portals

def pick_portal(portals, wanted):
    if wanted:
        if wanted not in portals:
            die(f"unknown portal: {wanted} (have: {', '.join(sorted(portals))})", 2)
        return wanted, portals[wanted]
    names = sorted(portals)
    print("Available portals:")
    for n in names:
        print(f"  - {n} (portal {portals[n]['portalId']}, theme {portals[n]['theme']})")
    try:
        choice = input("Portal id: ").strip()
    except EOFError:
        die("no portal selected", 2)
    if choice not in portals:
        die(f"unknown portal: {choice}", 2)
    return choice, portals[choice]

def main():
    opts = parse(sys.argv[1:])
    portals = load_config(opts["config"])
    pid, portal = pick_portal(portals, opts["portal"])
    token = opts["token"]
    if not token and not opts["dry_run"]:
        try:
            token = getpass.getpass("Private-app token (hidden, never stored): ").strip()
        except EOFError:
            die("no token supplied", 2)
    if not token:
        token = "DRY-RUN-TOKEN"
    work = tempfile.mkdtemp(prefix="cms-deploy-")
    try:
        try:
            subprocess.run(["unzip", "-q", "-o", opts["zip"], "-d", work], check=True, capture_output=True, text=True)
        except FileNotFoundError:
            die("cannot unpack ZIP: 'unzip' command not found")
        except subprocess.CalledProcessError as exc:
            die(f"cannot unpack ZIP: {exc.stderr.strip() or exc}")
        roots = [d for d in os.listdir(work) if os.path.isfile(os.path.join(work, d, "QA-EVIDENCE.json"))]
        if len(roots) != 1:
            die(f"ZIP must contain exactly one theme root with QA-EVIDENCE.json (found {len(roots)})")
        # Canonicalize: mkdtemp may sit under a symlink (e.g. macOS /var -> /private/var);
        # the traversal guard compares realpath'd entries against this, so it must be real too.
        theme_dir = os.path.realpath(os.path.join(work, roots[0]))
        with open(os.path.join(theme_dir, "QA-EVIDENCE.json"), encoding="utf-8") as handle:
            evidence = json.load(handle)
        gates = evidence.get("gates", {})
        if [gates.get(g) for g in ("g1", "g2", "g3", "g4")] != ["pass"] * 4:
            die("QA-EVIDENCE gates are not all pass — re-run validate-theme.sh")
        cutoff = datetime.fromisoformat(evidence["at"])
        for base, _dirs, files in os.walk(theme_dir):
            for name in files:
                if name == "QA-EVIDENCE.json":
                    continue
                mtime = datetime.fromtimestamp(os.path.getmtime(os.path.join(base, name)), tz=timezone.utc)
                if mtime > cutoff:
                    die(f"theme changed after validation: {os.path.relpath(os.path.join(base, name), theme_dir)}")
        with open(os.path.join(theme_dir, "assets.json"), encoding="utf-8") as handle:
            images = json.load(handle)["files"]
        # Fail fast on the shared path too: dry-run never reaches LIVE execution,
        # so traversal entries must be refused here as well (mirrors LIVE guard).
        for item in images:
            requested = os.path.realpath(os.path.join(theme_dir, item["local"]))
            if os.path.commonpath([requested, theme_dir]) != theme_dir:
                die(f"assets.json escapes theme dir: {item['local']}")
        with open(os.path.join(theme_dir, "deploy.json"), encoding="utf-8") as handle:
            pages = json.load(handle)["pages"]
        # Fail closed on unmapped form modules (runbook §3 step 7; SB-7). Marker rule:
        # a module is a form module iff any entry in its fields.json has "type": "form"
        # (HubSpot form picker; default carries form_id). Map keys are module dir names
        # minus the ".module" suffix. Enforced on dry-run too — refusal is the point.
        form_modules = set()
        modules_dir = os.path.join(theme_dir, "modules")
        if os.path.isdir(modules_dir):
            for entry in sorted(os.listdir(modules_dir)):
                if not entry.endswith(".module"):
                    continue
                try:
                    with open(os.path.join(modules_dir, entry, "fields.json"), encoding="utf-8") as handle:
                        fields = json.load(handle)
                except (OSError, ValueError):
                    continue
                if any(isinstance(f, dict) and f.get("type") == "form" for f in fields):
                    form_modules.add(entry[:-len(".module")])
        unmapped = sorted(form_modules - set((portal.get("forms") or {}).keys()))
        if unmapped:
            die(f"unmapped form module(s) without portals.yaml forms entry: {', '.join(unmapped)}")
        mode = "DRY-RUN" if opts["dry_run"] else "LIVE"
        plan = [
            f"[{mode}] portal {pid} (portalId {portal['portalId']}, theme {portal['theme']})",
            f"[{mode}] 1. verify evidence: {evidence['theme']} @ {evidence['commit']} — OK",
            f"[{mode}] 2. upload images: {len(images)} file(s) to File Manager",
            f"[{mode}] 3. upload theme: {HS_BIN} cms upload {theme_dir} {portal['theme']} --account={portal['hsAccount']}",
            f"[{mode}] 4. pages: {len(pages)} page(s) per deploy.json (manual in v1)",
            f"[{mode}] 5. menus: create/update per menu order (manual in v1)",
            f"[{mode}] 6. blog: {'use blog ' + str(portal['blogId']) if portal.get('blogId') else 'provision blog'} + assign templates (manual in v1)",
            f"[{mode}] 7. forms: {len(portal.get('forms') or {})} mapped form(s) (manual in v1)",
        ]
        print("\n".join(plan))
        if not opts["yes"]:
            print("AUTHORIZATION REQUIRED: re-run with --yes to execute.", file=sys.stdout)
            sys.exit(3)
        if opts["dry_run"]:
            print(f"[{mode}] content probes: " + ", ".join(f"{name} GET {path}" for name, path in CONTENT_PROBES))
            return
        # LIVE execution (runbook §3 order: images step 2, theme step 3, then probes)
        env = dict(os.environ, HS_TOKEN=token)

        def run_live(argv, step):
            try:
                return subprocess.run(argv, check=True, env=env, capture_output=True, text=True)
            except subprocess.CalledProcessError as exc:
                body = (exc.stderr or exc.stdout or "").strip().replace(token, "[REDACTED]")[:500]
                die(f"{step} failed (exit {exc.returncode}): {body or 'no detail'}")

        def curl_with_auth(args, step):
            import tempfile as _tf
            fd, path = _tf.mkstemp(prefix="cms-hdr-")  # mkstemp is 0600: token off ps argv and world-unreadable
            try:
                with os.fdopen(fd, "w") as handle:
                    handle.write(f'header = "Authorization: Bearer {token}"\n')
                return run_live([CURL_BIN, "-sS", "-f", "-K", path, *args], step)
            finally:
                try: os.unlink(path)
                except OSError: pass

        for item in images:
            requested = os.path.realpath(os.path.join(theme_dir, item["local"]))
            if os.path.commonpath([requested, theme_dir]) != theme_dir:
                die(f"assets.json escapes theme dir: {item['local']}")
            local = requested
            folder = "/" + item["dest"].strip("/").rsplit("/", 1)[0] if "/" in item["dest"].strip("/") else "/"
            curl_with_auth(["-X", "POST", "https://api.hubapi.com/files/v3/files",
                            "-F", f"file=@{local}", "-F", f"fileName={os.path.basename(item['dest'])}",
                            "-F", f"folderPath={folder}", "-F", 'options={"access":"PUBLIC_INDEXABLE","overwrite":true}'],
                           f"image upload {item['dest']}")
        run_live([HS_BIN, "cms", "upload", theme_dir, portal["theme"], f"--account={portal['hsAccount']}"], "theme upload")
        for name, probe_path in CONTENT_PROBES:
            curl_with_auth([f"https://api.hubapi.com{probe_path}?limit=1"], f"probe {name}")
        print(f"[LIVE] done: theme + {len(images)} image(s) pushed; content probes OK; pages/menus/blog/forms NOT automated in v1 — follow runbook §3 steps 4-7 manually.")
    finally:
        shutil.rmtree(work, ignore_errors=True)

main()
PYEOF
