#!/usr/bin/env python3
"""Render a slate .md to a .pdf twin (same basename) for one-click preview.

Chain (per the house export contract, man-digital-youtube-scripts §7.3):
markdown module -> styled HTML -> Chromium-family headless --print-to-pdf.
pandoc is skipped deliberately: the styled-HTML path is what carries the
candidate-card layout, which is the point of the PDF.

Layout contract the CSS expects (see SKILL.md output contract):
  h2  section        (## Candidates / ## Near-misses / ...)
  h3  candidate      (### S1 · "label")      -> wrapped in a bordered card
  h4  block label    (#### Score / Blueprint / Spans / Build notes / Risks)
  h5  blueprint beat (##### HOOK · 0:00-0:04) -> accent chip
Verdict tokens (STRONG/PARTIAL/WEAK), GATING and the ⚑ flag are badged.
Accent color is picked from the filename: youtube / linkedin / neutral.

Usage: python3 render_pdf.py FILE.md [FILE2.md ...] [--keep-html]
Exit non-zero if any render fails — the caller ships the .md and flags the
missing PDF rather than blocking delivery.
"""
import pathlib
import re
import subprocess
import sys

BROWSERS = [
    "/Applications/Brave Browser.app/Contents/MacOS/Brave Browser",
    "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
    "/Applications/Chromium.app/Contents/MacOS/Chromium",
    "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge",
]

ACCENTS = {"youtube": "#c4302b", "linkedin": "#0a66c2"}
NEUTRAL = "#33415c"

CSS = """
@page { margin: 12mm 11mm; }
* { box-sizing: border-box; }
body { font-family: -apple-system, 'Helvetica Neue', Arial, sans-serif;
       font-size: 11.5px; line-height: 1.42; color: #1b1b1b; margin: 0; }

h1 { font-size: 19px; margin: 0 0 4px; color: __ACCENT__; }
h1 + p { margin-top: 0; }
h2 { font-size: 13px; text-transform: uppercase; letter-spacing: .10em;
     margin: 26px 0 10px; padding: 5px 8px; background: #1b1b1b; color: #fff;
     border-radius: 2px; break-after: avoid; }
p  { margin: 4px 0; }
hr { border: none; border-top: 1px solid #d5d5d5; margin: 18px 0; }

/* ---- header metadata block ---- */
.meta { background: #f4f6f8; border: 1px solid #e0e4e8;
        border-left: 3px solid __ACCENT__; border-radius: 3px;
        padding: 9px 12px; margin: 8px 0 0; font-size: 10.5px; }
.meta p { margin: 5px 0; }
.meta hr { display: none; }

/* ---- candidate card ---- */
section.cand { border: 1px solid #ccc; border-left: 4px solid __ACCENT__;
               border-radius: 3px; padding: 11px 14px 13px; margin: 0 0 16px;
               background: #fcfcfc; }
section.cand h3 { font-size: 14.5px; margin: 0 0 7px; padding: 0 0 6px;
                  border-bottom: 2px solid __ACCENT__; break-after: avoid; }
section.cand > p { margin: 3px 0; }

/* ---- block label inside a candidate ---- */
h4 { font-size: 10px; text-transform: uppercase; letter-spacing: .11em;
     color: __ACCENT__; font-weight: 700; margin: 15px 0 5px;
     padding-bottom: 3px; border-bottom: 1px solid #dedede;
     break-after: avoid; }

/* ---- blueprint beat chip ---- */
h5 { display: inline-block; font-size: 9.5px; letter-spacing: .08em;
     text-transform: uppercase; background: __ACCENT__; color: #fff;
     padding: 2px 9px; border-radius: 3px; margin: 11px 0 4px;
     font-weight: 700; break-after: avoid; }
h5 + ul { margin-top: 3px; }

ul, ol { margin: 4px 0 4px 0; padding-left: 17px; }
li { margin: 2.5px 0; }

table { border-collapse: collapse; font-size: 10px; margin: 5px 0 3px;
        width: 100%; }
th, td { border: 1px solid #c8c8c8; padding: 3px 6px; text-align: left;
         vertical-align: top; }
th { background: #ececec; text-transform: uppercase; font-size: 9px;
     letter-spacing: .05em; }
tbody tr:nth-child(even) td { background: #f6f6f6; }

code { background: #eef1f4; padding: 1px 4px; border-radius: 2px;
       font-family: Menlo, monospace; font-size: 9.5px; color: #24303f; }

/* ---- badges ---- */
.v { display: inline-block; padding: 0 6px; border-radius: 8px; color: #fff;
     font-size: 8.5px; font-weight: 700; letter-spacing: .05em; }
.v-strong  { background: #0b7a3b; }
.v-partial { background: #b26a00; }
.v-weak    { background: #7a7a7a; }
.flag { background: #ffe8e8; color: #a11; border: 1px solid #f0b6b6;
        padding: 0 4px; border-radius: 2px; font-weight: 700; }
.rec { background: #0b7a3b; color: #fff; padding: 1px 7px; border-radius: 8px;
       font-size: 9px; letter-spacing: .05em; }
"""


def style_tokens(html):
    """Badge verdict/flag tokens. Operates on text nodes only — a token that
    ends an element (`<td>STRONG</td>`) must still match, so tag-awareness
    comes from splitting on tags, never from lookarounds."""
    subs = [("STRONG", 'v v-strong'), ("PARTIAL", 'v v-partial'),
            ("WEAK", 'v v-weak'), ("GATING", 'flag'), ("RECOMMENDED", 'rec')]
    parts = re.split(r"(<[^>]+>)", html)
    for i, seg in enumerate(parts):
        if seg.startswith("<"):
            continue
        for tok, cls in subs:
            seg = re.sub(rf"\b{tok}\b", f'<span class="{cls}">{tok}</span>', seg)
        seg = seg.replace("⚑", '<span class="flag">⚑</span>')
        parts[i] = seg
    return "".join(parts)


def wrap_header(html):
    """Box the metadata paragraphs between the title and the first section."""
    end_h1 = re.search(r"</h1>", html)
    first_h2 = re.search(r"<h2", html)
    if not (end_h1 and first_h2 and first_h2.start() > end_h1.end()):
        return html
    return (html[:end_h1.end()] + '<div class="meta">'
            + html[end_h1.end():first_h2.start()] + "</div>"
            + html[first_h2.start():])


def wrap_candidates(html):
    """Wrap each <h3>…(until next h3/h2) in a bordered card section."""
    parts = re.split(r"(?=<h3)", html)
    out = []
    for part in parts:
        if not part.startswith("<h3"):
            out.append(part)
            continue
        nxt = re.search(r"<h2", part)
        if nxt:
            out.append(f'<section class="cand">{part[:nxt.start()]}</section>'
                       + part[nxt.start():])
        else:
            out.append(f'<section class="cand">{part}</section>')
    return "".join(out)


def build_html(md_path):
    import markdown
    accent = NEUTRAL
    for key, color in ACCENTS.items():
        if key in md_path.name.lower():
            accent = color
            break
    body = markdown.markdown(md_path.read_text(),
                             extensions=["tables", "fenced_code", "sane_lists"])
    body = wrap_candidates(wrap_header(style_tokens(body)))
    return (f"<!doctype html><html><head><meta charset='utf-8'>"
            f"<title>{md_path.stem}</title>"
            f"<style>{CSS.replace('__ACCENT__', accent)}</style></head>"
            f"<body>{body}</body></html>")


def render(md_path, keep_html=False):
    md_path = pathlib.Path(md_path).resolve()
    pdf_path = md_path.with_suffix(".pdf")
    html_path = md_path.with_suffix(".render-tmp.html")
    html_path.write_text(build_html(md_path))
    try:
        browser = next((b for b in BROWSERS if pathlib.Path(b).exists()), None)
        if not browser:
            raise RuntimeError("no Chromium-family browser found")
        r = subprocess.run(
            [browser, "--headless", "--disable-gpu",
             f"--print-to-pdf={pdf_path}", "--no-pdf-header-footer",
             html_path.as_uri()],
            capture_output=True, text=True, timeout=180)
        if not pdf_path.exists() or pdf_path.stat().st_size == 0:
            raise RuntimeError(f"browser render failed: {r.stderr.strip()[-400:]}")
    finally:
        if not keep_html:
            html_path.unlink(missing_ok=True)
    return pdf_path


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    keep = "--keep-html" in sys.argv
    if not args:
        sys.exit(__doc__)
    failures = 0
    for arg in args:
        try:
            out = render(arg, keep_html=keep)
            print(f"OK  {out}  ({out.stat().st_size} bytes)")
        except Exception as e:
            failures += 1
            print(f"FAIL  {arg}  — {e}", file=sys.stderr)
    sys.exit(1 if failures else 0)


if __name__ == "__main__":
    main()
