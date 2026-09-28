#!/usr/bin/env bash
# File Manager existence verifier (S2): every assets.json dest must already
# exist in the portal's File Manager. READ-ONLY: probes via `hs filemanager
# fetch` into a temp dir, uploads nothing.
# Usage: verify-fm.sh <theme-dir> --portal <id> --config portals.yaml [--token T]
# Env: HS_BIN (default hs). --token is accepted for deploy.sh CLI symmetry but
# unused: hs CLI authenticates via the portal's configured account, not a token.
# Exit codes: 0 all dests exist, 1 one or more missing, 2 usage/unknown portal.
set -euo pipefail
exec python3 - "$@" <<'PYEOF'
import os, shutil, subprocess, sys, tempfile

HS_BIN = os.environ.get("HS_BIN", "hs")

def die(msg, code=1):
    print(f"verify-fm.sh: {msg}", file=sys.stderr); sys.exit(code)

def parse(argv):
    opts = {"theme": None, "portal": None, "config": None, "token": None}
    i = 0
    if argv and not argv[0].startswith("--"):
        opts["theme"] = argv[0]; i = 1
    valued = {"--portal": "portal", "--config": "config", "--token": "token"}
    while i < len(argv):
        a = argv[i]
        if a in valued:
            if i + 1 >= len(argv):
                die(f"missing value for {a}", 2)
            opts[valued[a]] = argv[i + 1]; i += 2
        else:
            die(f"unknown flag: {a}", 2)
    if not opts["theme"] or not opts["portal"] or not opts["config"]:
        die("usage: verify-fm.sh <theme-dir> --portal <id> --config portals.yaml [--token T]", 2)
    return opts

def load_portal(path, wanted):
    try:
        import yaml
    except ImportError:
        die("PyYAML missing: run: pip3 install --user pyyaml (add --break-system-packages if refused)")
    try:
        with open(path, encoding="utf-8") as handle:
            portals = {p["id"]: p for p in yaml.safe_load(handle).get("portals", [])}
    except (yaml.YAMLError, AttributeError, KeyError, TypeError) as exc:
        die(f"invalid config: {type(exc).__name__}")
    if wanted not in portals:
        die(f"unknown portal: {wanted} (have: {', '.join(sorted(portals))})", 2)
    return portals[wanted]

def main():
    opts = parse(sys.argv[1:])
    portal = load_portal(opts["config"], opts["portal"])
    try:
        with open(os.path.join(opts["theme"], "assets.json"), encoding="utf-8") as handle:
            import json
            dests = [f["dest"] for f in json.load(handle)["files"]]
    except (OSError, ValueError, KeyError) as exc:
        die(f"cannot read assets.json: {exc}")
    print(f"verify-fm: portal {opts['portal']} (account {portal['hsAccount']}): {len(dests)} file(s)")
    work = tempfile.mkdtemp(prefix="cms-verify-fm-")
    try:
        missing = []
        for dest in dests:
            target = os.path.join(work, "probe")
            proc = subprocess.run(
                [HS_BIN, "filemanager", "fetch", dest, target,
                 f"--account={portal['hsAccount']}"],
                capture_output=True, text=True)
            if proc.returncode == 0:
                print(f"OK {dest}")
            else:
                print(f"MISSING {dest}")
                missing.append(dest)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if missing:
        print(f"verify-fm: {len(missing)} of {len(dests)} file(s) missing from File Manager: "
              + ", ".join(missing), file=sys.stderr)
        sys.exit(1)
    print(f"verify-fm: all {len(dests)} file(s) present in File Manager")

main()
PYEOF
