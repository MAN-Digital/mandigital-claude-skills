#!/usr/bin/env bash
# Local QA gates 1-4 for a HubSpot theme dir. Gate 5 (staging) is manual per runbook.
# Usage: validate-theme.sh <theme-dir> --inventory <inventory.json>
# Env: HS_BIN (default: hs), HS_ACCOUNT (optional: passed as --account to hs cms lint)
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
[[ -d "$theme_dir/js" ]] || fail 1 "missing js/"
[[ -d "$theme_dir/images" ]] || fail 1 "missing images/"
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import json, sys
from pathlib import Path
theme = Path(sys.argv[1])
try:
    theme_json = json.loads((theme / "theme.json").read_text(encoding="utf-8"))
except json.JSONDecodeError:
    print("theme.json is not valid JSON"); sys.exit(1)
if "preview_path" not in theme_json:
    print("theme.json missing preview_path"); sys.exit(1)
for mod in sorted((theme / "modules").glob("*.module")):
    meta = mod / "meta.json"
    if not meta.is_file():
        print(f"{mod.name} missing meta.json"); sys.exit(1)
    try:
        data = json.loads(meta.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"{mod.name}/meta.json is not valid JSON"); sys.exit(1)
    for key in ("host_template_types", "content_types"):
        if key not in data:
            print(f"{mod.name}/meta.json missing {key}"); sys.exit(1)
PYEOF
) || fail 1 "$out"
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
try:
    deploy = json.loads((theme / "deploy.json").read_text(encoding="utf-8"))
except json.JSONDecodeError:
    print("deploy.json is not valid JSON"); sys.exit(1)
entries = {p["templatePath"]: p for p in deploy["pages"]}
counts = {}
for p in deploy["pages"]:
    counts[p["templatePath"]] = counts.get(p["templatePath"], 0) + 1
homes = [p for p in deploy["pages"] if p.get("isHomepage")]
if len(homes) != 1:
    print(f"want exactly one homepage, found {len(homes)}"); sys.exit(1)
slugs = [p["slug"] for p in deploy["pages"]]
if len(set(slugs)) != len(slugs):
    print("duplicate slugs in deploy.json"); sys.exit(1)
for p in deploy["pages"]:
    if not (theme / p["templatePath"]).is_file():
        print(f"deploy.json points at missing file: {p['templatePath']}"); sys.exit(1)
for b in ("templates/blog_listing.html", "templates/blog_post.html"):
    if not (theme / b).is_file():
        print(f"missing blog template: {b}"); sys.exit(1)
for tpl in sorted((theme / "templates").glob("*.html")):
    rel = f"templates/{tpl.name}"
    head = tpl.read_text(encoding="utf-8")[:600]
    m = re.search(r"templateType:\s*(\w+)", head)
    ttype = m.group(1) if m else ""
    if ttype in ("blog_listing", "blog_post"):
        continue  # assigned via blog provisioning, not deploy.json
    if rel not in entries:
        print(f"page template without deploy.json entry: {rel}"); sys.exit(1)
    if counts[rel] > 1:
        print(f"duplicate deploy.json entry: {rel}"); sys.exit(1)
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
theme = Path(sys.argv[1])
try:
    inv = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
except json.JSONDecodeError:
    print(f"{Path(sys.argv[2]).name} is not valid JSON"); sys.exit(1)
verbatim = set(inv.get("verbatim", []))
for mod in sorted((theme / "modules").glob("*.module")):
    try:
        fields = json.loads((mod / "fields.json").read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        print(f"{mod.name}/fields.json is not valid JSON"); sys.exit(1)
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
    for phrase in verbatim:
        stripped = stripped.replace(phrase, " ")
    for chunk in (c.strip() for c in stripped.split()):
        if chunk and chunk not in verbatim:
            print(f"hardcoded copy in {mod.name}/module.html: {chunk[:60]!r}"); sys.exit(1)
PYEOF
) || fail 2 "$out"

# S4 (gate-2: module wiring): a module whose fields.json contains a form-type
# field MUST render it with a native {% form %} tag. Escape hatch: modules
# that submit via custom JS declare it with data-hsforms-ignore — that passes
# with a WARN (stderr) instead of failing. (2> >(cat >&2) lets the WARN bypass
# the $() capture so it stays visible on passing runs; FAIL detail is captured.)
out=$(python3 - "$theme_dir" 2> >(cat >&2) <<'PYEOF'
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
FORM_TAG = re.compile(r"\{%\s*form\b")
for mod in sorted((theme / "modules").glob("*.module")):
    try:
        fields = json.loads((mod / "fields.json").read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        continue  # malformed JSON is reported by the main gate-2/3 checks
    if not any(isinstance(f, dict) and f.get("type") == "form" for f in fields):
        continue
    html = (mod / "module.html").read_text(encoding="utf-8")
    if FORM_TAG.search(html):
        continue
    if "data-hsforms-ignore" in html:
        print(f"WARN: {mod.name} uses custom form submit (not native {{% form %}})",
              file=sys.stderr)
        continue
    print(f"{mod.name}: form field without {{% form %}} tag"); sys.exit(1)
PYEOF
) || fail 2 "$out"

# S8 (gate-2: module wiring): LINE-BASED HEURISTIC, not a parse. Every <img>
# tag whose src attribute carries a {{ }} expression must sit inside an
# {% if %} guard, else an empty src renders as <img src="">. Window = the 5
# preceding lines plus the current line up to the <img (same-line
# "{% if x %}<img ...>" counts — the dominant minified-module style).
# Misreads multi-line <img> tags and guards further than 5 lines up; keep
# guards adjacent to the img.
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import re, sys
from pathlib import Path
theme = Path(sys.argv[1])
IF_TAG = re.compile(r"\{%\s*if\b")
DYN_SRC = re.compile(r"src\s*=\s*[\"'][^\"']*\{\{")
for mod in sorted((theme / "modules").glob("*.module")):
    lines = (mod / "module.html").read_text(encoding="utf-8").splitlines()
    for i, line in enumerate(lines):
        for m in re.finditer(r"<img\b", line):
            tag = line[m.start():].split(">", 1)[0]
            if not DYN_SRC.search(tag):
                continue
            window = "\n".join(lines[max(0, i - 5):i]) + "\n" + line[:m.start()]
            if not IF_TAG.search(window):
                print(f"unguarded img with dynamic src in {mod.name}/module.html:{i + 1}")
                sys.exit(1)
PYEOF
) || fail 2 "$out"

# ---- Gate 3: validity ----
find "$theme_dir" -name '*.json' -print0 | python3 -c "
import json, sys
for raw in sys.stdin.buffer.read().split(b'\0'):
    if raw:
        json.load(open(raw.decode(), encoding='utf-8'))
" || fail 3 "invalid JSON present"
lint_args=("$theme_dir")
[[ -n "${HS_ACCOUNT:-}" ]] && lint_args+=("--account=$HS_ACCOUNT")
lint_out=""
lint_rc=0
lint_out=$("$HS_BIN" cms lint "${lint_args[@]}" 2>&1) || lint_rc=$?
printf '%s\n' "$lint_out"
[[ "$lint_rc" -ne 0 ]] && fail 3 "hs cms lint failed"
# hs exits 0 even with errors (SB-2): fail on any nonzero issue count or
# error marker. "0 issues found" must keep passing, hence [1-9] lead digit.
echo "$lint_out" | grep -Eq '([1-9][0-9]* issues? found|✖|ERROR)' && fail 3 "hs cms lint reported issues"
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
    else:
        for open_pat, close_pat in ((r"\{%\s*dnd_section\b", r"\{%\s*end_dnd_section\b"),
                                     (r"\{%\s*dnd_module\b", r"\{%\s*end_dnd_module\b")):
            if len(re.findall(open_pat, text)) != len(re.findall(close_pat, text)):
                print(f"{tpl.name}: unbalanced dnd tags"); sys.exit(1)
PYEOF
) || fail 3 "$out"

# ---- Gate 4: links + assets ----
out=$(python3 - "$theme_dir" "$inventory" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
try:
    inv = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
except json.JSONDecodeError:
    print(f"{Path(sys.argv[2]).name} is not valid JSON"); sys.exit(1)
try:
    manifest = {f["dest"]: f["local"] for f in json.loads((theme / "assets.json").read_text(encoding="utf-8"))["files"]}
except json.JSONDecodeError:
    print("assets.json is not valid JSON"); sys.exit(1)
for f in manifest.values():
    if not (theme / f).is_file():
        print(f"manifest local file missing: {f}"); sys.exit(1)
used = set()
for fields_file in sorted((theme / "modules").glob("*.module/fields.json")):
    text = fields_file.read_text(encoding="utf-8")
    # S1: HubSpot-emitted JSON has a space before the colon ("src" : "...");
    # the strict '"src":' pattern missed those srcs entirely (false-pass on
    # unmanifested srcs + false "dead manifest entry"). Tolerate the space.
    for src in re.findall(r'"src"\s*:\s*"(/[^"]+)"', text):
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
    for raw in set(re.findall(r"https?://[^\s\"'<>]+", text)):
        # JSON \" escapes leak a trailing backslash into the raw-text match (SB-1).
        url = raw.rstrip("\\")
        if url not in allowed:
            print(f"unallowlisted external URL {url} in {path.relative_to(theme)}"); sys.exit(1)
PYEOF
) || fail 4 "$out"

# S6 (gate-4: links + assets): no [...] placeholder text in fields.json
# DEFAULT string values (they render to visitors). Parsed-JSON walk, not raw
# text: structural brackets (arrays) never match — only string VALUES held in
# a "default" key (top-level or group-children) are tested.
out=$(python3 - "$theme_dir" <<'PYEOF' 2>&1
import json, re, sys
from pathlib import Path
theme = Path(sys.argv[1])
PLACEHOLDER = re.compile(r"\[[^\[\]]{1,60}\]")
def default_strings(node):
    if isinstance(node, dict):
        if "default" in node:
            yield from value_strings(node["default"])
        for key, val in node.items():
            if key != "default":
                yield from default_strings(val)
    elif isinstance(node, list):
        for val in node:
            yield from default_strings(val)
def value_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for val in value.values():
            yield from value_strings(val)
    elif isinstance(value, list):
        for val in value:
            yield from value_strings(val)
for fields_file in sorted((theme / "modules").glob("*.module/fields.json")):
    try:
        fields = json.loads(fields_file.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        continue  # malformed JSON is reported by the gate-3 check
    for s in default_strings(fields):
        if PLACEHOLDER.search(s):
            print(f"placeholder '[...]' in default {s[:80]!r} ({fields_file.parent.name}/fields.json)")
            sys.exit(1)
PYEOF
) || fail 4 "$out"

# ---- Evidence ----
out=$(python3 - "$theme_dir" "$inventory" <<'PYEOF' 2>&1
import datetime, json, sys
from pathlib import Path
theme = Path(sys.argv[1])
try:
    inv = json.loads(Path(sys.argv[2]).read_text(encoding="utf-8"))
    label = json.loads((theme / "theme.json").read_text(encoding="utf-8"))["label"]
except (json.JSONDecodeError, KeyError) as e:
    print(f"cannot build evidence: {e}", file=sys.stderr); sys.exit(1)
evidence = {"theme": label, "commit": inv.get("commit", "n/a"),
            "at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "gates": {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"},
            "staging": {"url": None, "at": None}}
(theme / "QA-EVIDENCE.json").write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")
PYEOF
) || { echo "FAIL: evidence: $out" >&2; exit 1; }
echo "PASS: all local gates (g1-g4) for $theme_dir"
