#!/usr/bin/env python3
"""Upload MAN Digital blog graphics and replace HubSpot placeholders in a draft.

This helper is intentionally conservative:
- dry-run by default;
- uploads only when --upload is passed;
- patches only the draft postBody when --patch-draft is passed;
- refuses placeholder/image count mismatches unless --allow-partial is explicit.
"""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import shutil
import sys
import time
from dataclasses import dataclass, replace
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

try:
    import requests
    from bs4 import BeautifulSoup
except ImportError as exc:  # pragma: no cover - environment guidance
    raise SystemExit(
        "Missing dependency. Run with the OpenClaw blog-pipeline venv, e.g. "
        "`cd /Users/romeoman/Documents/Dev/OpenClaw/openclaw-infra/blog-pipeline && "
        "PYTHONPATH=src .venv/bin/python /Users/romeoman/.codex/skills/"
        "man-digital-blog-graphics/scripts/hubspot_placeholder_publish.py ...`, "
        "or install requests and beautifulsoup4."
    ) from exc


CMS_2026_BASE = "https://api.hubapi.com/cms/blogs/2026-03/posts"
CMS_V3_BASE = "https://api.hubapi.com/cms/v3/blogs/posts"
FILES_UPLOAD_URL = "https://api.hubapi.com/files/v3/files"
PLACEHOLDER_CLASS = "man-graphic-placeholder"
TOKEN_KEYS = ("HUBSPOT_ACCESS_TOKEN", "HUBSPOT_API_KEY")


@dataclass(frozen=True)
class Asset:
    index: int
    display_number: int
    image_path: Path | None
    source_pen_path: Path | None
    url: str
    alt: str
    width: int | None
    height: int | None
    title: str


def safe_slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "graphic"


def seo_file_stem(index: int, title: str) -> str:
    return f"graphic-{index:02d}-{safe_slug(title)}"


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: Any) -> None:
    path.write_text(json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def read_openclaw_env_vars(path: Path) -> dict[str, str]:
    try:
        data = read_json(path)
    except (OSError, json.JSONDecodeError):
        return {}
    if not isinstance(data, dict):
        return {}
    env_section = data.get("env")
    if not isinstance(env_section, dict):
        return {}
    vars_section = env_section.get("vars")
    if not isinstance(vars_section, dict):
        return {}
    return {str(key): str(value) for key, value in vars_section.items() if value}


def candidate_config_paths(
    *,
    explicit_config: str | None = None,
    env: Mapping[str, str] | None = None,
    cwd: Path | None = None,
) -> list[Path]:
    env = env or os.environ
    cwd = (cwd or Path.cwd()).resolve()
    seen: set[Path] = set()
    candidates: list[Path] = []

    def add(path: str | Path | None) -> None:
        if not path:
            return
        expanded = Path(path).expanduser()
        try:
            key = expanded.resolve()
        except OSError:
            key = expanded
        if key in seen:
            return
        seen.add(key)
        candidates.append(expanded)

    if explicit_config:
        add(explicit_config)
    else:
        add(env.get("OPENCLAW_CONFIG") or env.get("OPENCLAW_CONFIG_PATH"))
        if env.get("OPENCLAW_HOME"):
            add(Path(env["OPENCLAW_HOME"]).expanduser() / "openclaw.json")

    for parent in (cwd, *cwd.parents):
        candidate = parent / "data" / "openclaw" / "openclaw.json"
        if candidate.exists():
            add(candidate)
            break

    home = env.get("HOME") or os.path.expanduser("~")
    if home and home != "~":
        add(Path(home) / ".openclaw" / "openclaw.json")

    return candidates


def resolve_hubspot_token(config: str | None = None) -> tuple[str, dict[str, Any]]:
    checked: list[str] = []
    for path in candidate_config_paths(explicit_config=config):
        checked.append(str(path))
        if not path.exists():
            continue
        env_vars = read_openclaw_env_vars(path)
        for key in TOKEN_KEYS:
            token = env_vars.get(key, "").strip()
            if token:
                return token, {"source": str(path), "key": key, "checked": checked}

    for key in TOKEN_KEYS:
        token = os.environ.get(key, "").strip()
        if token:
            return token, {"source": "environment", "key": key, "checked": checked}

    return "", {"source": "", "key": "", "checked": checked}


def response_json(resp: requests.Response) -> dict[str, Any]:
    try:
        data = resp.json()
    except ValueError:
        return {"raw": (resp.text or "")[:2000]}
    return data if isinstance(data, dict) else {"value": data}


def request_json(
    method: str,
    url: str,
    token: str,
    *,
    timeout: float = 45,
    max_retries: int = 2,
    **kwargs: Any,
) -> dict[str, Any]:
    headers = dict(kwargs.pop("headers", {}) or {})
    headers["Authorization"] = f"Bearer {token}"
    last_error = ""
    for attempt in range(max_retries + 1):
        resp = requests.request(method, url, headers=headers, timeout=timeout, **kwargs)
        payload = response_json(resp)
        if resp.ok:
            return payload
        last_error = f"{method} {url} -> {resp.status_code}: {json.dumps(payload)[:1000]}"
        if resp.status_code == 429 and attempt < max_retries:
            retry_after = resp.headers.get("Retry-After", "2")
            try:
                wait_seconds = max(float(retry_after), 0.0)
            except ValueError:
                wait_seconds = 2.0
            time.sleep(wait_seconds)
            continue
        break
    raise RuntimeError(last_error)


def draft_endpoint(post_id: str, api_mode: str, token: str) -> tuple[str, dict[str, Any]]:
    candidates: list[str]
    if api_mode == "2026-03":
        candidates = [f"{CMS_2026_BASE}/{post_id}/draft"]
    elif api_mode == "v3":
        candidates = [f"{CMS_V3_BASE}/{post_id}/draft"]
    else:
        candidates = [f"{CMS_2026_BASE}/{post_id}/draft", f"{CMS_V3_BASE}/{post_id}/draft"]

    errors: list[str] = []
    for url in candidates:
        try:
            return url, request_json("GET", url, token)
        except RuntimeError as exc:
            errors.append(str(exc))
    raise RuntimeError("Could not fetch draft post. " + " | ".join(errors))


def extract_post_body(post_payload: dict[str, Any]) -> str:
    for key in ("postBody", "post_body", "body", "content", "html", "rssBody"):
        value = post_payload.get(key)
        if isinstance(value, str) and value.strip():
            return value
    raise RuntimeError("Fetched post did not include a recognizable postBody field.")


def load_manifest(path: Path | None) -> dict[str, Any]:
    if not path:
        return {}
    data = read_json(path)
    if not isinstance(data, dict):
        raise ValueError(f"Manifest must be an object: {path}")
    return data


def normalize_asset(raw: Mapping[str, Any], manifest_by_index: dict[int, dict[str, Any]]) -> Asset:
    raw_index = raw.get("index", raw.get("graphic_number", raw.get("number")))
    if raw_index is None:
        raise ValueError(f"Asset is missing index/graphic_number: {raw}")
    index = int(raw_index)
    manifest_entry = manifest_by_index.get(index, {})
    display_number = int(raw.get("display_number") or raw.get("original_index") or raw.get("graphic_number") or index)
    title = str(raw.get("title") or manifest_entry.get("title") or f"Graphic {index}")
    alt = str(raw.get("alt") or raw.get("alt_text") or title)
    url = str(raw.get("url") or raw.get("hubspot_url") or "").strip()
    image_value = raw.get("image_path") or raw.get("path") or raw.get("file")
    image_path = Path(str(image_value)).expanduser() if image_value else None
    source_pen_value = raw.get("source_pen_path") or raw.get("pen_path") or raw.get("pencil_file")
    source_pen_path = Path(str(source_pen_value)).expanduser() if source_pen_value else None
    width = int(raw["width"]) if raw.get("width") not in (None, "") else None
    height = int(raw["height"]) if raw.get("height") not in (None, "") else None
    if not url and image_path is None:
        raise ValueError(f"Asset {index} needs image_path/path/file or url.")
    return Asset(
        index=index,
        display_number=display_number,
        image_path=image_path,
        source_pen_path=source_pen_path,
        url=url,
        alt=alt,
        width=width,
        height=height,
        title=title,
    )


def load_assets(path: Path, manifest: dict[str, Any]) -> dict[int, Asset]:
    payload = read_json(path)
    if isinstance(payload, dict) and isinstance(payload.get("graphics"), list):
        raw_assets = payload["graphics"]
    elif isinstance(payload, list):
        raw_assets = payload
    elif isinstance(payload, dict):
        raw_assets = []
        for key, value in payload.items():
            if isinstance(value, dict):
                raw = dict(value)
                raw.setdefault("index", key)
                raw_assets.append(raw)
    else:
        raise ValueError("Assets JSON must be a list, a {graphics: []} object, or an index map.")

    manifest_by_index = {
        int(item["index"]): item
        for item in manifest.get("graphics", [])
        if isinstance(item, dict) and item.get("index") is not None
    }
    assets = [normalize_asset(item, manifest_by_index) for item in raw_assets if isinstance(item, dict)]
    by_index = {asset.index: asset for asset in assets}
    if len(by_index) != len(assets):
        raise ValueError("Assets JSON contains duplicate graphic indexes.")
    return by_index


def validate_asset_set(
    *,
    assets: dict[int, Asset],
    placeholder_count: int,
    manifest: dict[str, Any],
    allow_partial: bool,
    require_pen_source: bool,
    figure_numbers: set[int] | None = None,
) -> None:
    figure_numbers = figure_numbers or set()
    if not placeholder_count:
        # No man-graphic-placeholder blocks remain (already-patched / re-publish case).
        # Allow replacing existing man-blog-graphic figures by data-man-graphic-number.
        missing = sorted(a.display_number for a in assets.values() if a.display_number not in figure_numbers)
        if not figure_numbers or missing:
            raise ValueError(
                "No man-graphic-placeholder blocks found, and assets do not all match existing "
                f"man-blog-graphic figures by data-man-graphic-number (missing: {missing})."
            )
    else:
        expected = set(range(1, placeholder_count + 1))
        actual = set(assets)
        if not allow_partial and actual != expected:
            raise ValueError(
                f"Asset indexes must match placeholders exactly. expected={sorted(expected)} actual={sorted(actual)}"
            )
        if allow_partial and not actual <= expected:
            # Tolerate assets whose index exceeds the placeholder range when they target
            # an existing figure by display_number (mixed placeholder + figure re-publish).
            outside = sorted(i for i in (actual - expected) if assets[i].display_number not in figure_numbers)
            if outside:
                raise ValueError(f"Asset indexes outside placeholder range: {outside}")

    manifest_count = int(manifest.get("placeholder_count") or 0)
    if manifest_count and placeholder_count and manifest_count != placeholder_count:
        raise ValueError(
            f"Fetched postBody placeholder count {placeholder_count} differs from manifest count {manifest_count}."
        )

    for asset in assets.values():
        if asset.image_path and not asset.image_path.exists():
            raise FileNotFoundError(str(asset.image_path))

    if require_pen_source:
        seen_pen_paths: dict[Path, int] = {}
        for asset in assets.values():
            if asset.source_pen_path is None:
                raise ValueError(
                    f"Graphic {asset.display_number} is missing source_pen_path. "
                    "HubSpot placement requires one traceable editable .pen file per graphic."
                )
            if asset.source_pen_path.suffix.lower() != ".pen":
                raise ValueError(f"Graphic {asset.display_number} source_pen_path is not a .pen file: {asset.source_pen_path}")
            if not asset.source_pen_path.exists():
                raise FileNotFoundError(str(asset.source_pen_path))
            if asset.source_pen_path.name.lower() == "playground.pen":
                raise ValueError("Do not publish from Playground.pen. Each graphic needs its own prompt-specific .pen file.")
            resolved = asset.source_pen_path.resolve()
            if resolved in seen_pen_paths:
                other = seen_pen_paths[resolved]
                raise ValueError(
                    f"Graphics {other} and {asset.display_number} use the same .pen file. "
                    "Each graphic must have its own separate editable source."
                )
            seen_pen_paths[resolved] = asset.display_number
            display_patterns = [
                rf"\bgraphic\s*0?{asset.display_number}\b",
                rf"\bgraphic-0?{asset.display_number}\b",
            ]
            if not any(re.search(pattern, asset.source_pen_path.stem, flags=re.IGNORECASE) for pattern in display_patterns):
                raise ValueError(
                    f"Graphic {asset.display_number} source_pen_path does not include its placement number: {asset.source_pen_path.name}"
                )


def upload_asset(
    asset: Asset,
    *,
    token: str,
    folder_path: str,
    folder_id: str,
    access: str,
) -> dict[str, Any]:
    if not asset.image_path:
        raise ValueError(f"Asset {asset.index} has no local image_path to upload.")
    mime_type = mimetypes.guess_type(str(asset.image_path))[0] or "application/octet-stream"
    options = json.dumps({"access": access})
    data = {
        "fileName": asset.image_path.name,
        "options": options,
    }
    if folder_id:
        data["folderId"] = folder_id
    else:
        data["folderPath"] = folder_path
    with asset.image_path.open("rb") as handle:
        files = {"file": (asset.image_path.name, handle, mime_type)}
        headers = {"Authorization": f"Bearer {token}"}
        resp = requests.post(FILES_UPLOAD_URL, headers=headers, data=data, files=files, timeout=90)
    payload = response_json(resp)
    if not resp.ok:
        raise RuntimeError(f"Upload failed for Graphic {asset.index}: {resp.status_code} {json.dumps(payload)[:1000]}")
    return payload


def prepare_webp_asset(
    asset: Asset,
    *,
    output_dir: Path,
    quality: int,
    lossless: bool,
) -> Asset:
    if asset.image_path is None:
        return asset
    output_dir.mkdir(parents=True, exist_ok=True)
    target = output_dir / f"{seo_file_stem(asset.display_number, asset.title)}.webp"
    if asset.image_path.suffix.lower() == ".webp":
        if asset.image_path.resolve() != target.resolve():
            shutil.copy2(asset.image_path, target)
        return replace(asset, image_path=target)

    try:
        from PIL import Image
    except ImportError as exc:  # pragma: no cover - environment guidance
        raise RuntimeError(
            "Pillow is required to prepare WebP uploads from non-WebP exports. "
            "Run this script with the OpenClaw blog-pipeline .venv."
        ) from exc

    with Image.open(asset.image_path) as image:
        image.save(
            target,
            format="WEBP",
            lossless=lossless,
            quality=quality,
            method=6,
        )
    return replace(asset, image_path=target)


def build_replacement_tag(
    soup: BeautifulSoup,
    *,
    index: int,
    asset: Asset,
    url: str,
    file_id: str,
) -> Any:
    figure = soup.new_tag("figure")
    figure["class"] = "man-blog-graphic"
    figure["data-man-graphic-number"] = str(asset.display_number)
    if file_id:
        figure["data-hubspot-file-id"] = file_id
    figure["data-man-graphic-title"] = asset.title

    img = soup.new_tag("img")
    img["src"] = url
    img["alt"] = asset.alt
    img["title"] = asset.title
    img["loading"] = "lazy"
    img["decoding"] = "async"
    if asset.width:
        img["width"] = str(asset.width)
    if asset.height:
        img["height"] = str(asset.height)
    figure.append(img)
    return figure


def replace_placeholders(
    post_body: str,
    *,
    assets: dict[int, Asset],
    uploaded: dict[int, dict[str, Any]],
    allow_partial: bool,
) -> tuple[str, int, list[dict[str, Any]]]:
    soup = BeautifulSoup(post_body, "html.parser")
    placeholders = soup.find_all("div", class_=lambda value: value and PLACEHOLDER_CLASS in str(value).split())
    replacements: list[dict[str, Any]] = []
    used_display: set[int] = set()
    for index, placeholder in enumerate(placeholders, start=1):
        asset = assets.get(index)
        if asset is None:
            if allow_partial:
                continue
            raise ValueError(f"Missing asset for placeholder Graphic {index}.")

        upload_payload = uploaded.get(index, {})
        url = asset.url or str(upload_payload.get("url") or upload_payload.get("defaultHostingUrl") or "")
        file_id = str(upload_payload.get("id") or "")
        if not url:
            raise ValueError(f"Graphic {index} has no URL after upload.")
        replacement = build_replacement_tag(soup, index=index, asset=asset, url=url, file_id=file_id)
        placeholder.replace_with(replacement)
        used_display.add(asset.display_number)
        replacements.append(
            {
                "index": index,
                "display_number": asset.display_number,
                "url": url,
                "file_id": file_id,
                "alt": asset.alt,
                "title": asset.title,
                "target": "placeholder",
            }
        )

    # Re-publish / correction case: replace already-published man-blog-graphic figures
    # by data-man-graphic-number for any asset not placed via a placeholder above.
    figures = soup.find_all("figure", class_=lambda value: value and "man-blog-graphic" in str(value).split())
    fig_by_num: dict[int, Any] = {}
    for fg in figures:
        try:
            fig_by_num[int(fg.get("data-man-graphic-number"))] = fg
        except (TypeError, ValueError):
            continue
    figures_replaced = 0
    for index in sorted(assets):
        asset = assets[index]
        if asset.display_number in used_display:
            continue
        fg = fig_by_num.get(asset.display_number)
        if fg is None:
            continue
        upload_payload = uploaded.get(index, {})
        url = asset.url or str(upload_payload.get("url") or upload_payload.get("defaultHostingUrl") or "")
        file_id = str(upload_payload.get("id") or "")
        if not url:
            raise ValueError(f"Graphic {asset.display_number} has no URL after upload.")
        new_fig = build_replacement_tag(soup, index=index, asset=asset, url=url, file_id=file_id)
        fg.replace_with(new_fig)
        used_display.add(asset.display_number)
        figures_replaced += 1
        replacements.append(
            {
                "index": index,
                "display_number": asset.display_number,
                "url": url,
                "file_id": file_id,
                "alt": asset.alt,
                "title": asset.title,
                "target": "figure",
            }
        )
    return str(soup), len(placeholders) + figures_replaced, replacements


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--post-id", required=True, help="HubSpot blog post ID to update.")
    parser.add_argument("--assets-json", required=True, type=Path, help="JSON mapping placeholder indexes to image files or URLs.")
    parser.add_argument("--manifest", type=Path, help="Fetched *.graphic-placeholders.json manifest for validation.")
    parser.add_argument("--folder-path", default="", help="HubSpot Files folder path for uploads.")
    parser.add_argument("--folder-id", default="", help="HubSpot Files folder ID for uploads.")
    parser.add_argument("--access", default="PUBLIC_NOT_INDEXABLE", help="HubSpot file access, e.g. PUBLIC_NOT_INDEXABLE.")
    parser.add_argument("--prepare-webp", action=argparse.BooleanOptionalAction, default=True, help="Prepare SEO-named WebP upload files before upload/patch.")
    parser.add_argument("--webp-quality", type=int, default=100, help="WebP quality. Use 100 for best-looking lossless exports.")
    parser.add_argument("--webp-lossless", action=argparse.BooleanOptionalAction, default=True, help="Use lossless WebP when preparing upload assets.")
    parser.add_argument("--config", help="Optional openclaw.json path.")
    parser.add_argument("--api-mode", choices=("auto", "2026-03", "v3"), default="auto")
    parser.add_argument("--output-dir", type=Path, default=Path("output/hubspot-placeholder-publish"))
    parser.add_argument("--upload", action="store_true", help="Upload local image files to HubSpot Files.")
    parser.add_argument("--patch-draft", action="store_true", help="PATCH the HubSpot draft postBody. Requires explicit use.")
    parser.add_argument("--allow-partial", action="store_true", help="Allow replacing only provided placeholder indexes.")
    parser.add_argument(
        "--allow-missing-pen-source",
        action="store_true",
        help=(
            "Emergency override: allow upload/patch without one editable source .pen per graphic. "
            "Use only with explicit user approval and document the limitation."
        ),
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if not 1 <= int(args.webp_quality) <= 100:
        raise SystemExit("--webp-quality must be between 1 and 100.")
    if args.upload and not (args.folder_path or args.folder_id):
        raise SystemExit("--upload requires --folder-path or --folder-id.")

    token, token_meta = resolve_hubspot_token(args.config)
    if not token:
        raise SystemExit("HUBSPOT_ACCESS_TOKEN not found in openclaw.json or environment.")

    endpoint, post_payload = draft_endpoint(args.post_id, args.api_mode, token)
    post_body = extract_post_body(post_payload)
    manifest = load_manifest(args.manifest)
    assets = load_assets(args.assets_json, manifest)

    soup = BeautifulSoup(post_body, "html.parser")
    placeholder_count = len(soup.find_all("div", class_=lambda value: value and PLACEHOLDER_CLASS in str(value).split()))
    figure_numbers: set[int] = set()
    for fg in soup.find_all("figure", class_=lambda value: value and "man-blog-graphic" in str(value).split()):
        try:
            figure_numbers.add(int(fg.get("data-man-graphic-number")))
        except (TypeError, ValueError):
            continue
    validate_asset_set(
        assets=assets,
        placeholder_count=placeholder_count,
        manifest=manifest,
        allow_partial=args.allow_partial,
        require_pen_source=(args.upload or args.patch_draft) and not args.allow_missing_pen_source,
        figure_numbers=figure_numbers,
    )

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    out_dir = args.output_dir / f"post-{args.post_id}-{timestamp}"
    out_dir.mkdir(parents=True, exist_ok=True)
    original_path = out_dir / "postBody.original.html"
    patched_path = out_dir / "postBody.patched.html"
    upload_manifest_path = out_dir / "upload-manifest.json"
    original_path.write_text(post_body, encoding="utf-8")

    prepared_assets_dir = out_dir / "webp-assets"
    if args.prepare_webp:
        assets = {
            index: prepare_webp_asset(
                asset,
                output_dir=prepared_assets_dir,
                quality=args.webp_quality,
                lossless=args.webp_lossless,
            )
            for index, asset in assets.items()
        }

    uploaded: dict[int, dict[str, Any]] = {}
    if args.upload:
        for index in sorted(assets):
            asset = assets[index]
            if asset.url:
                uploaded[index] = {"url": asset.url, "id": ""}
            else:
                uploaded[index] = upload_asset(
                    asset,
                    token=token,
                    folder_path=args.folder_path,
                    folder_id=args.folder_id,
                    access=args.access,
                )
    else:
        for index, asset in assets.items():
            suffix = asset.image_path.suffix.lower() if asset.image_path else ".webp"
            uploaded[index] = {"url": asset.url or f"https://example.invalid/dry-run/{seo_file_stem(index, asset.title)}{suffix}", "id": ""}

    patched_body, found_count, replacements = replace_placeholders(
        post_body,
        assets=assets,
        uploaded=uploaded,
        allow_partial=args.allow_partial,
    )
    patched_path.write_text(patched_body, encoding="utf-8")
    write_json(
        upload_manifest_path,
        {
            "post_id": args.post_id,
            "draft_endpoint": endpoint,
            "token_source": token_meta.get("source", ""),
            "folder_path": args.folder_path,
            "folder_id": args.folder_id,
            "asset_format": "webp" if args.prepare_webp else "source",
            "webp_quality": args.webp_quality if args.prepare_webp else None,
            "webp_lossless": args.webp_lossless if args.prepare_webp else None,
            "prepared_assets_dir": str(prepared_assets_dir) if args.prepare_webp else "",
            "prepared_assets": {
                str(index): str(asset.image_path) if asset.image_path else ""
                for index, asset in assets.items()
            },
            "source_pen_paths": {
                str(index): str(asset.source_pen_path) if asset.source_pen_path else ""
                for index, asset in assets.items()
            },
            "missing_pen_source_override": bool(args.allow_missing_pen_source),
            "uploaded": uploaded,
            "replacements": replacements,
            "placeholder_count": found_count,
            "patched_draft": False,
        },
    )

    if args.patch_draft:
        dry_urls = [item for item in replacements if str(item["url"]).startswith("https://example.invalid/")]
        if dry_urls:
            raise SystemExit("--patch-draft requires real image URLs. Use --upload or provide url entries in assets JSON.")
        request_json(
            "PATCH",
            endpoint,
            token,
            headers={"Content-Type": "application/json"},
            json={"postBody": patched_body},
        )
        manifest_payload = read_json(upload_manifest_path)
        manifest_payload["patched_draft"] = True
        write_json(upload_manifest_path, manifest_payload)

    print(f"Post ID: {args.post_id}")
    print(f"Draft endpoint: {endpoint}")
    print(f"Placeholders found: {found_count}")
    print(f"Placeholders replaced: {len(replacements)}")
    print(f"Uploaded files: {len([item for item in uploaded.values() if item.get('id')])}")
    print(f"Patched draft: {'yes' if args.patch_draft else 'no'}")
    print(f"Original backup: {original_path}")
    print(f"Patched HTML: {patched_path}")
    print(f"Upload manifest: {upload_manifest_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
