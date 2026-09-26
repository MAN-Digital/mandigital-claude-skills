#!/usr/bin/env bash
# Local QA gates 1-4 for a HubSpot theme dir. Gate 5 (staging) is manual per runbook.
# Usage: validate-theme.sh <theme-dir> --inventory <inventory.json>
# Env: HS_BIN (default: hs)
set -euo pipefail

HS_BIN="${HS_BIN:-hs}"
[[ $# -eq 3 && "$2" == "--inventory" ]] || { echo "usage: validate-theme.sh <theme-dir> --inventory <inventory.json>" >&2; exit 2; }
theme_dir=$(cd "$1" && pwd)
inventory=$(cd "$(dirname "$3")" && pwd)/$(basename "$3")
[[ -f "$inventory" ]] || { echo "FAIL: g0: inventory not found: $3" >&2; exit 1; }

fail() { echo "FAIL: g$1: $2" >&2; exit 1; }

# ---- Gate 1: completeness ----
[[ -f "$theme_dir/theme.json" ]] || fail 1 "missing theme.json"
[[ -f "$theme_dir/fields.json" ]] || fail 1 "missing root fields.json"
[[ -f "$theme_dir/deploy.json" ]] || fail 1 "missing deploy.json"
[[ -f "$theme_dir/assets.json" ]] || fail 1 "missing assets.json"
for c in fonts variables common custom; do
  [[ -f "$theme_dir/css/$c.css" ]] || fail 1 "missing css/$c.css"
done
[[ -d "$theme_dir/modules/header.module" ]] || fail 1 "missing header.module"
[[ -d "$theme_dir/modules/footer.module" ]] || fail 1 "missing footer.module"
[[ -d "$theme_dir/modules/blog_listing.module" ]] || fail 1 "missing blog_listing.module"
[[ -d "$theme_dir/modules/blog_post.module" ]] || fail 1 "missing blog_post.module"
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
deploy = json.loads((theme / "deploy.json").read_text(encoding="utf-8"))
entries = {p["templatePath"]: p for p in deploy["pages"]}
homes = [p for p in deploy["pages"] if p.get("isHomepage")]
if len(homes) != 1:
    print(f"want exactly one homepage, found {len(homes)}"); sys.exit(1)
slugs = [p["slug"] for p in deploy["pages"]]
if len(set(slugs)) != len(slugs):
    print("duplicate slugs in deploy.json"); sys.exit(1)
for tpl in sorted((theme / "templates").glob("*.html")):
    rel = f"templates/{tpl.name}"
    head = tpl.read_text(encoding="utf-8")[:600]
    m = re.search(r"templateType:\s*(\w+)", head)
    ttype = m.group(1) if m else ""
    if ttype in ("blog_listing", "blog_post"):
        continue  # assigned via blog provisioning, not deploy.json
    if rel not in entries:
        print(f"page template without deploy.json entry: {rel}"); sys.exit(1)
    if not (theme / entries[rel]["templatePath"]).is_file():
        print(f"deploy.json points at missing file: {rel}"); sys.exit(1)
for tpl in sorted((theme / "templates").glob("*.html")):
    text = tpl.read_text(encoding="utf-8")
    for ref in re.findall(r'path="(../modules/[^"]+)"', text):
        if not (tpl.parent / ref).is_dir():
            print(f"{tpl.name} references missing module: {ref}"); sys.exit(1)
PYEOF
) || fail 1 "$out"

# ---- Gate 2: field wiring ----
out=$(python3 - "$theme_dir" "$inventory" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme, inv = Path(sys.argv[1]), json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
verbatim = set(inv.get("verbatim", []))
for mod in sorted((theme / "modules").glob("*.module")):
    fields = json.loads((mod / "fields.json").read_text(encoding="utf-8"))
    html = (mod / "module.html").read_text(encoding="utf-8")
    names = [(f["name"], None) for f in fields]
    for f in fields:
        for child in f.get("children", []) or []:
            names.append((child["name"], f["name"]))
    for name, parent in names:
        if parent is None:
            if f"module.{name}" not in html:
                print(f"orphan field {mod.name}/{name}"); sys.exit(1)
        else:
            if f".{name}" not in html:
                print(f"orphan child field {mod.name}/{parent}.{name}"); sys.exit(1)
    stripped = re.sub(r"\{#.*?#\}", "", html, flags=re.S)
    stripped = re.sub(r"\{\{.*?\}\}", "", stripped, flags=re.S)
    stripped = re.sub(r"\{%.*?%\}", "", stripped, flags=re.S)
    stripped = re.sub(r"<[^>]+>", " ", stripped)
    for chunk in (c.strip() for c in stripped.split()):
        if chunk and chunk not in verbatim:
            print(f"hardcoded copy in {mod.name}/module.html: {chunk[:60]!r}"); sys.exit(1)
PYEOF
) || fail 2 "$out"

# ---- Gate 3: validity ----
find "$theme_dir" -name '*.json' -print0 | python3 -c "
import json, sys
for raw in sys.stdin.buffer.read().split(b'\0'):
    if raw:
        json.load(open(raw.decode(), encoding='utf-8'))
" || fail 3 "invalid JSON present"
"$HS_BIN" cms lint "$theme_dir" || fail 3 "hs cms lint failed"
"$HS_BIN" cms theme marketplace-validate --src="$theme_dir" || fail 3 "marketplace-validate failed"
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import re, sys
from pathlib import Path
for tpl in sorted((Path(sys.argv[1]) / "templates").glob("*.html")):
    text = tpl.read_text(encoding="utf-8")
    head = text[:600]
    m = re.search(r"templateType:\s*(\w+)", head)
    ttype = m.group(1) if m else ""
    areas = len(re.findall(r"{%\s*dnd_area\b", text))
    if ttype == "blog_post":
        if areas != 0 or "{% module" not in text:
            print(f"{tpl.name}: blog_post must use static modules, no dnd_area"); sys.exit(1)
    elif areas != 1:
        print(f"{tpl.name}: want exactly one dnd_area, found {areas}"); sys.exit(1)
PYEOF
) || fail 3 "$out"

# ---- Gate 4: links + assets ----
out=$(python3 - "$theme_dir" "$inventory" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
inv = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
manifest = {f["dest"]: f["local"] for f in json.loads((theme / "assets.json").read_text(encoding="utf-8"))["files"]}
for f in manifest.values():
    if not (theme / f).is_file():
        print(f"manifest local file missing: {f}"); sys.exit(1)
used = set()
for fields_file in sorted((theme / "modules").glob("*.module/fields.json")):
    text = fields_file.read_text(encoding="utf-8")
    for src in re.findall(r'"src":\s*"(/[^"]+)"', text):
        used.add(src)
        if src not in manifest:
            print(f"unmanifested image src {src} in {fields_file.parent.name}"); sys.exit(1)
for dest in manifest:
    if dest not in used:
        print(f"dead manifest entry (unreferenced): {dest}"); sys.exit(1)
BANNED = ("localhost", "127.0.0.1", "placehold.", "lorempixel", "example.com")
allowed = set(inv.get("external_urls", []))
for path in sorted(theme.rglob("*")):
    if not path.is_file() or path.suffix in (".jpg", ".jpeg", ".png", ".gif", ".webp", ".svg", ".ico"):
        continue
    try:
        text = path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    for bad in BANNED:
        if bad in text:
            print(f"banned string {bad!r} in {path.relative_to(theme)}"); sys.exit(1)
    for url in set(re.findall(r"https?://[^\s\"'<>]+", text)):
        if url not in allowed:
            print(f"unallowlisted external URL {url} in {path.relative_to(theme)}"); sys.exit(1)
PYEOF
) || fail 4 "$out"

# ---- Evidence ----
python3 - "$theme_dir" "$inventory" <<'PYEOF'
import datetime, json, sys
from pathlib import Path
theme = Path(sys.argv[1])
inv = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
label = json.loads((theme / "theme.json").read_text(encoding="utf-8"))["label"]
evidence = {"theme": label, "commit": inv.get("commit", "n/a"),
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "gates": {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"},
            "staging": {"url": None, "at": None}}
(theme / "QA-EVIDENCE.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
PYEOF
echo "PASS: all local gates (g1-g4) for $theme_dir"
