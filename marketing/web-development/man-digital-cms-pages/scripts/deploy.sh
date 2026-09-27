#!/usr/bin/env bash
# Guided config-driven HubSpot deploy. ZIP-first, evidence-checked, explicit auth.
# Usage: deploy.sh [--portal ID] --zip FILE --config portals.yaml [--token T] [--dry-run] [--yes]
# Env: HS_BIN (default hs), CURL_BIN (default curl), HS_TOKEN (token fallback),
# CREATE_FORMS_BIN (default: create-forms.sh next to this script),
# plus the per-portal var named by the entry's tokenEnv key (runbook §1)
# Exit codes: 0 ok, 1 failed check, 2 usage/unknown portal, 3 authorization required.
# Step 4 note: live `hubspot` CLI has no cms/api subcommands (CRM-only CLI,
# per references/api-playbook.md §1), so content probes use verified REST paths
# via curl (see CONTENT_PROBES).
set -euo pipefail
export CMS_SCRIPTS_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
exec python3 - "$@" <<'PYEOF'
import getpass, json, os, shutil, subprocess, sys, tempfile
from datetime import datetime, timezone

HS_BIN = os.environ.get("HS_BIN", "hs")
CURL_BIN = os.environ.get("CURL_BIN", "curl")
def _default_create_forms():
    here = os.environ.get("CMS_SCRIPTS_DIR")
    if here:
        return os.path.join(here, "create-forms.sh")
    return "create-forms.sh"  # last resort: PATH lookup

CREATE_FORMS_BIN = os.environ.get("CREATE_FORMS_BIN") or _default_create_forms()
CONTENT_PROBES = [  # verified REST paths per references/api-playbook.md §1
    ("pages", "/cms/v3/pages/site-pages"),
    ("blog_posts", "/cms/v3/blogs/posts"),
    ("forms", "/marketing/v3/forms"),
]

def die(msg, code=1):
    print(f"deploy.sh: {msg}", file=sys.stderr); sys.exit(code)

def parse(argv):
    opts = {"portal": None, "zip": None, "config": None, "token": os.environ.get("HS_TOKEN"),
            "token_flag": False, "dry_run": False, "yes": False}
    valued = {"--portal": "portal", "--zip": "zip", "--config": "config", "--token": "token"}
    i = 0
    while i < len(argv):
        a = argv[i]
        if a in valued:
            if i + 1 >= len(argv):
                die(f"missing value for {a}", 2)
            opts[valued[a]] = argv[i + 1]
            if a == "--token":
                opts["token_flag"] = True
            i += 2
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

def resolve_token(opts, portal):
    """Token precedence: --token flag > portal tokenEnv var > HS_TOKEN > prompt.

    tokenEnv names the env var holding THIS portal's private-app token, so each
    portal entry points at its own secret when working across portals. Fail
    closed: a configured-but-unset tokenEnv dies instead of silently falling
    back to another portal's HS_TOKEN. Dry-run never needs a token, so the
    fail-closed check is skipped there. Mirrors the same-named helper in
    create-forms.sh (no shared lib by repo convention — keep in sync).
    """
    if opts["token_flag"]:
        return opts["token"]
    tenv = portal.get("tokenEnv")
    if tenv is not None:
        if not isinstance(tenv, str) or not tenv.strip():
            die("config tokenEnv must be a non-empty string")
        val = os.environ.get(tenv.strip())
        if val:
            return val
        if not opts["dry_run"]:
            die(f"token for portal missing: env var {tenv.strip()} (tokenEnv) is unset or empty")
    if opts["token"]:
        return opts["token"]
    if opts["dry_run"]:
        return "DRY-RUN-TOKEN"
    try:
        token = getpass.getpass("Private-app token (hidden, never stored): ").strip()
    except EOFError:
        die("no token supplied", 2)
    if not token:
        die("no token supplied", 2)
    return token

def forms_provision(portal, config_dir):
    """Validate the optional formsProvision block; {} when absent (back-compat).

    Shape: {enabled: bool (default false), spec: path (required when enabled,
    resolved relative to the config file), prefix: str}. Mirrors the same-named
    helper in create-forms.sh (no shared lib by repo convention — keep in sync).
    """
    raw = portal.get("formsProvision")
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        die("config formsProvision must be a mapping (enabled/spec/prefix)")
    unknown = sorted(set(raw) - {"enabled", "spec", "prefix"})
    if unknown:
        die(f"config formsProvision has unknown key(s): {', '.join(unknown)}")
    if "enabled" in raw and not isinstance(raw["enabled"], bool):
        die("config formsProvision.enabled must be boolean")
    out = {"enabled": bool(raw.get("enabled", False)),
           "prefix": raw.get("prefix", "")}
    if "prefix" in raw and (not isinstance(raw["prefix"], str) or not raw["prefix"].strip()):
        die("config formsProvision.prefix must be a non-empty string")
    if out["enabled"]:
        spec = raw.get("spec")
        if not isinstance(spec, str) or not spec.strip():
            die("config formsProvision.spec is required when enabled")
        out["spec"] = spec if os.path.isabs(spec) else os.path.join(config_dir, spec)
    elif "spec" in raw:
        out["spec"] = raw["spec"]
    return out

def spec_modules(spec_path):
    """Module keys covered by a form-spec file (for the fail-closed pre-check).

    Full spec validation happens inside create-forms.sh at execution time; here
    only the module list is needed, and an unreadable spec fails the deploy.
    """
    try:
        with open(spec_path, encoding="utf-8") as handle:
            data = json.load(handle)
        modules = {f["module"] for f in data["forms"]}
    except (OSError, ValueError, KeyError, TypeError) as exc:
        die(f"cannot read formsProvision.spec {spec_path}: {type(exc).__name__}")
    if not modules or not all(isinstance(m, str) for m in modules):
        die(f"formsProvision.spec {spec_path} has no usable form modules")
    return modules

def main():
    opts = parse(sys.argv[1:])
    portals = load_config(opts["config"])
    pid, portal = pick_portal(portals, opts["portal"])
    token = resolve_token(opts, portal)
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
        provision = forms_provision(portal, config_dir=os.path.dirname(os.path.abspath(opts["config"])))
        provisioned_modules = set()
        if provision.get("enabled"):
            provisioned_modules = spec_modules(provision["spec"])
        unmapped = sorted(form_modules - set((portal.get("forms") or {}).keys()) - provisioned_modules)
        if unmapped:
            die(f"unmapped form module(s) without portals.yaml forms entry: {', '.join(unmapped)}")
        mode = "DRY-RUN" if opts["dry_run"] else "LIVE"
        plan = [
            f"[{mode}] portal {pid} (portalId {portal['portalId']}, theme {portal['theme']})",
            f"[{mode}] 1. verify evidence: {evidence['theme']} @ {evidence['commit']} — OK",
            f"[{mode}] 2. upload images: {len(images)} file(s) to File Manager",
        ]
        if provision.get("enabled"):
            plan.append(
                f"[{mode}] 2b. provision forms: {len(provisioned_modules)} form(s) from "
                f"{provision['spec']} via create-forms.sh"
                + (f" (prefix \"{provision['prefix']}\")" if provision.get("prefix") else ""))
        if provision.get("enabled"):
            step7 = (f"[{mode}] 7. forms: {len(portal.get('forms') or {})} mapped + "
                     f"{len(provisioned_modules)} provisioned form(s); "
                     f"record FORM_GUIDs in portals.yaml")
        else:
            step7 = f"[{mode}] 7. forms: {len(portal.get('forms') or {})} mapped form(s) (manual in v1)"
        plan.extend([
            f"[{mode}] 3. upload theme: {HS_BIN} cms upload {theme_dir} {portal['theme']} --account={portal['hsAccount']}",
            f"[{mode}] 4. pages: {len(pages)} page(s) per deploy.json (manual in v1)",
            f"[{mode}] 5. menus: create/update per menu order (manual in v1)",
            f"[{mode}] 6. blog: {'use blog ' + str(portal['blogId']) if portal.get('blogId') else 'provision blog'} + assign templates (manual in v1)",
            step7,
        ])
        print("\n".join(plan))
        if not opts["yes"]:
            print("AUTHORIZATION REQUIRED: re-run with --yes to execute.", file=sys.stdout)
            sys.exit(3)
        if opts["dry_run"]:
            print(f"[{mode}] content probes: " + ", ".join(f"{name} GET {path}" for name, path in CONTENT_PROBES))
            return
        # LIVE execution (runbook §3 order: images 2, forms 2b when enabled, theme 3, then probes)
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
        if provision.get("enabled"):
            try:
                forms_proc = run_live(
                    [CREATE_FORMS_BIN, "--portal", pid, "--config", opts["config"]],
                    "form provisioning")
            except FileNotFoundError:
                die(f"form provisioning failed: {CREATE_FORMS_BIN} not found "
                    f"(override with CREATE_FORMS_BIN)")
            for line in (forms_proc.stdout or "").splitlines():
                if line.startswith("FORM_GUID "):
                    print(f"[LIVE] {line}")
        run_live([HS_BIN, "cms", "upload", theme_dir, portal["theme"], f"--account={portal['hsAccount']}"], "theme upload")
        for name, probe_path in CONTENT_PROBES:
            curl_with_auth([f"https://api.hubapi.com{probe_path}?limit=1"], f"probe {name}")
        if provision.get("enabled"):
            print(f"[LIVE] done: theme + {len(images)} image(s) pushed; "
                  f"{len(provisioned_modules)} form(s) provisioned; content probes OK; "
                  f"pages/menus/blog NOT automated in v1 — follow runbook §3 steps 4-6 manually; "
                  f"record the FORM_GUID lines above in portals.yaml forms:.")
        else:
            print(f"[LIVE] done: theme + {len(images)} image(s) pushed; content probes OK; pages/menus/blog/forms NOT automated in v1 — follow runbook §3 steps 4-7 manually.")
    finally:
        shutil.rmtree(work, ignore_errors=True)

main()
PYEOF
