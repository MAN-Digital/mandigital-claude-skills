#!/usr/bin/env bash
# Blog template verifier: proves the theme's blog_listing + blog_post templates
# exist, carry the right templateType annotations, are uploaded, and (when the
# portal entry has a blogId) reports which templates the blog has assigned.
# READ-ONLY: local file checks plus `hs cms list` / `hs api` GET probes.
# The blog-settings API is read-only (PUT/PATCH return 405), so assignment
# itself is a manual UI step — the script always prints the exact UI path.
# Usage: verify-blog.sh <theme-dir> [--portal <id> --config portals.yaml]
#          [--blog NAME] [--require-assigned] [--token T]
# Env: HS_BIN (default hs). Assignment state reads via `hs api` first, then the
# private-app token (--token > portal tokenEnv > HS_TOKEN), because hs CLI keys
# often lack the `content` scope blog-settings needs. When both fail the state
# is reported as unknown (NOTE) rather than failing the run.
# Exit codes: 0 all checks pass (unknown assignment state is a NOTE, not a
# failure), 1 check failure, 2 usage/config error.
set -euo pipefail
exec python3 - "$@" <<'PYEOF'
import json, os, re, subprocess, sys
from pathlib import Path

HS_BIN = os.environ.get("HS_BIN", "hs")
EXPECTED = {"blog_listing.html": "blog_listing", "blog_post.html": "blog_post"}

def die(msg, code=1):
    print(f"verify-blog.sh: {msg}", file=sys.stderr); sys.exit(code)

def parse(argv):
    opts = {"theme": None, "portal": None, "config": None, "token": None,
            "blog": None, "require_assigned": False}
    i = 0
    if argv and not argv[0].startswith("--"):
        opts["theme"] = argv[0]; i = 1
    valued = {"--portal": "portal", "--config": "config", "--token": "token",
              "--blog": "blog"}
    while i < len(argv):
        a = argv[i]
        if a == "--require-assigned":
            opts["require_assigned"] = True; i += 1
        elif a in valued:
            if i + 1 >= len(argv):
                die(f"missing value for {a}", 2)
            opts[valued[a]] = argv[i + 1]; i += 2
        else:
            die(f"unknown flag: {a}", 2)
    if not opts["theme"]:
        die("usage: verify-blog.sh <theme-dir> [--portal <id> --config portals.yaml] "
            "[--blog NAME] [--require-assigned] [--token T]", 2)
    if bool(opts["portal"]) != bool(opts["config"]):
        die("--portal and --config must be given together", 2)
    return opts

def load_portal(path, wanted):
    try:
        import yaml
    except ImportError:
        die("PyYAML missing: run: pip3 install --user pyyaml (add --break-system-packages if refused)")
    try:
        with open(path, encoding="utf-8") as handle:
            portals = {p["id"]: p for p in yaml.safe_load(handle).get("portals", [])}
    except OSError as exc:
        die(f"cannot read config {path}: {exc.strerror or exc}", 2)
    except (yaml.YAMLError, AttributeError, KeyError, TypeError) as exc:
        die(f"invalid config: {type(exc).__name__}", 2)
    if wanted not in portals:
        die(f"unknown portal: {wanted} (have: {', '.join(sorted(portals))})", 2)
    portal = portals[wanted]
    for key in ("theme", "hsAccount"):
        if not portal.get(key):
            die(f"invalid config: portal {wanted} lacks required key {key!r}", 2)
    return portal

def header_fields(path):
    """Template annotation block: {key: value} from the leading <!-- -->."""
    fields = {}
    try:
        head = path.read_text(encoding="utf-8").split("-->", 1)[0]
    except OSError:
        return fields
    for line in head.splitlines():
        if ":" in line:
            key, _, val = line.partition(":")
            fields[key.strip()] = val.strip()
    return fields

def parse_settings(raw):
    """First-{ to last-} JSON parse; (settings, error)."""
    try:
        return json.loads(raw[raw.index("{"):raw.rindex("}") + 1]), None
    except (ValueError, json.JSONDecodeError) as exc:
        return None, f"unparseable blog-settings response: {raw.strip()[:100]} ({exc})"

def read_blog_settings(account, portal, blog_id, cli_token):
    """(settings dict|None, error). Tries `hs api` first (PAK auth), then the
    private-app token (--token > portal tokenEnv > HS_TOKEN), since hs keys
    often lack the `content` scope blog-settings needs."""
    got = subprocess.run(
        [HS_BIN, "api", f"/cms/v3/blog-settings/settings/{blog_id}",
         f"--account={account}", "--json"],
        text=True, capture_output=True)
    if got.returncode == 0:
        settings, err = parse_settings(got.stdout)
        if settings is not None:
            return settings, None
        hs_err = err
    else:
        hs_err = (got.stderr or got.stdout).strip().splitlines()
        hs_err = hs_err[0][:100] if hs_err else f"exit {got.returncode}"
    # Token precedence mirrors resolve_token in create-forms.sh/deploy.sh
    # (no shared lib by repo convention — keep in sync): --token flag >
    # portal tokenEnv var > HS_TOKEN. Fail closed: a configured-but-unset
    # tokenEnv dies instead of silently reading another portal's settings.
    # An empty/whitespace --token is treated as unset (falls through).
    token = cli_token.strip() if cli_token and cli_token.strip() else None
    tenv = portal.get("tokenEnv")
    if not token and tenv is not None:
        if not isinstance(tenv, str) or not tenv.strip():
            die("config tokenEnv must be a non-empty string", 2)
        val = os.environ.get(tenv.strip())
        if val and val.strip():
            token = val
        else:
            die(f"token for portal missing: env var {tenv.strip()} (tokenEnv) is unset or empty", 2)
    if not token:
        token = os.environ.get("HS_TOKEN") or None
    if not token:
        return None, f"hs api failed ({hs_err}); no token (--token / tokenEnv / HS_TOKEN)"
    import urllib.request, urllib.error
    req = urllib.request.Request(
        f"https://api.hubapi.com/cms/v3/blog-settings/settings/{blog_id}",
        headers={"Authorization": f"Bearer {token}"})
    try:
        body = urllib.request.urlopen(req, timeout=30).read().decode()
    except urllib.error.HTTPError as exc:
        return None, f"hs api failed ({hs_err}); token GET: HTTP {exc.code}"
    except Exception as exc:
        return None, f"hs api failed ({hs_err}); token GET: {exc}"
    settings, err = parse_settings(body)
    if settings is None:
        return None, f"hs api failed ({hs_err}); token GET: {err}"
    return settings, None

def ui_steps(blog_label, theme):
    return (
        "ASSIGN IN UI (blog-settings API is read-only: PUT/PATCH return 405):\n"
        f"  Marketing > Website > Blog > {blog_label} > Settings > Templates\n"
        f"  - \"Blog listing pages\" -> {theme}/templates/blog_listing.html\n"
        f"  - \"Blog posts\"         -> {theme}/templates/blog_post.html"
    )

def main():
    opts = parse(sys.argv[1:])
    theme_dir = Path(opts["theme"])
    failures = []
    for name, want_type in EXPECTED.items():
        path = theme_dir / "templates" / name
        if not path.is_file():
            failures.append(f"missing local template: templates/{name}")
            continue
        fields = header_fields(path)
        if fields.get("templateType") != want_type:
            failures.append(f"templates/{name}: templateType is "
                            f"{fields.get('templateType')!r}, want {want_type!r}")
        elif fields.get("isAvailableForNewContent") != "true":
            failures.append(f"templates/{name}: isAvailableForNewContent is not true "
                            "(template invisible to the blog's template picker)")
        else:
            print(f"OK templates/{name} ({want_type}, available for new content)")
    if failures:
        for item in failures:
            print(f"verify-blog.sh: {item}", file=sys.stderr)
        sys.exit(1)

    if not opts["portal"]:
        print(ui_steps(opts["blog"] or "your blog", "<theme>"))
        return

    portal = load_portal(opts["config"], opts["portal"])
    theme, account = portal["theme"], portal["hsAccount"]
    blog_label = opts["blog"] or (f"blog {portal.get('blogId')}"
                                  if portal.get("blogId") else "your blog")

    listed = subprocess.run(
        [HS_BIN, "cms", "list", f"{theme}/templates", f"--account={account}"],
        text=True, capture_output=True)
    if listed.returncode != 0:
        die(f"hs cms list failed: {(listed.stderr or listed.stdout).strip()}")
    # Strip ANSI: `hs cms list` colorizes through chalk, which honors
    # FORCE_COLOR even when piped — escape codes would break exact matching.
    ansi = re.compile(r"\x1b\[[0-9;]*m")
    remote = {ansi.sub("", line).strip() for line in listed.stdout.splitlines()
              if ansi.sub("", line).strip()}
    for name in EXPECTED:
        if name in remote:
            print(f"OK remote {theme}/templates/{name}")
        else:
            die(f"template not uploaded: {theme}/templates/{name} "
                f"(run: hs cms upload <theme-dir> {theme} --account={account})")

    if portal.get("blogId"):
        settings, state_err = read_blog_settings(
            account, portal, portal["blogId"], opts["token"])
        if settings is None:
            print(f"NOTE could not read blog assignment ({state_err}); the templates "
                  f"above are uploaded and ready to assign.")
            if opts["require_assigned"]:
                die("cannot prove assignment: blog-settings unreadable")
        if settings is not None:
            want = {n: f"{theme}/templates/{n}" for n in EXPECTED}
            have = {"blog_listing.html": settings.get("listingPageTemplatePath"),
                    "blog_post.html": settings.get("postTemplatePath")}
            unassigned = False
            for name in EXPECTED:
                if have[name] == want[name]:
                    print(f"ASSIGNED {name} -> {have[name]}")
                elif not have[name]:
                    unassigned = True
                    print(f"UNASSIGNED {name} (want {want[name]})")
                else:
                    unassigned = True
                    print(f"MISMATCH {name}: blog uses {have[name]}, want {want[name]}")
            if unassigned and opts["require_assigned"]:
                print("verify-blog.sh: blog templates not assigned (see UNASSIGNED/MISMATCH above)",
                      file=sys.stderr)
                sys.exit(1)
    else:
        print("NOTE portal blogId is null: provision the blog by hand, then rerun "
              "with --portal to check its assignment.")
    print(ui_steps(blog_label, theme))

main()
PYEOF
