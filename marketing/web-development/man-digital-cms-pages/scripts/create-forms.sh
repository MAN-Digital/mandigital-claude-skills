#!/usr/bin/env bash
# Provision HubSpot forms from a form-spec JSON via Forms API v3.
# Idempotent by form name: look up first, skip existing (or --update to replace).
# Usage: create-forms.sh [--spec SPEC.json] --portal ID --config portals.yaml [--token T]
#                        [--prefix P] [--update] [--dry-run] [--out MAP.json]
# Env: CURL_BIN (default curl), HS_TOKEN (token fallback),
# plus the per-portal var named by the entry's tokenEnv key (runbook §1)
# Exit codes: 0 ok, 1 API/network failure, 2 usage/config/spec error.
# Spec format + design-field mapping: references/deploy-runbook.md §"Form provisioning".
# API shapes mirror the verified OpenAPI on the create/update-form doc pages
# (see references/api-playbook.md §1); --dry-run never touches the network.
set -euo pipefail
exec python3 - "$@" <<'PYEOF'
import getpass, json, os, subprocess, sys, tempfile
from datetime import datetime, timezone

CURL_BIN = os.environ.get("CURL_BIN", "curl")
API = "https://api.hubapi.com"
FORMS = f"{API}/marketing/v3/forms"

FIELD_TYPES = {
    "text": "single_line_text",
    "email": "email",
    "phone": "phone",
    "textarea": "multi_line_text",
    "select": "dropdown",
    "checkbox": "single_checkbox",
    "consent": None,  # collected into legalConsentOptions, not a form field
}
CONSENT_MODES = {"none", "implicit", "explicit"}

def die(msg, code=1):
    print(f"create-forms.sh: {msg}", file=sys.stderr); sys.exit(code)

def parse(argv):
    opts = {"spec": None, "portal": None, "config": None,
            "token": os.environ.get("HS_TOKEN"), "token_flag": False,
            "prefix": None, "update": False, "dry_run": False, "out": None}
    valued = {"--spec": "spec", "--portal": "portal", "--config": "config",
              "--token": "token", "--prefix": "prefix", "--out": "out"}
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
        elif a == "--update": opts["update"] = True; i += 1
        elif a == "--dry-run": opts["dry_run"] = True; i += 1
        else: die(f"unknown flag: {a}", 2)
    if not opts["portal"] or not opts["config"]:
        die("usage: create-forms.sh [--spec SPEC.json] --portal ID --config portals.yaml "
            "[--token T] [--prefix P] [--update] [--dry-run] [--out MAP.json]", 2)
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

def forms_provision(portal):
    """Validate the optional formsProvision block; {} when absent (back-compat)."""
    raw = portal.get("formsProvision")
    if raw is None:
        return {}
    if not isinstance(raw, dict):
        die("config formsProvision must be a mapping (enabled/spec/prefix)", 2)
    for key in ("enabled", "spec", "prefix"):
        if key not in raw:
            continue
        want = bool if key == "enabled" else str
        if not isinstance(raw[key], want) or (want is str and not raw[key].strip()):
            die(f"config formsProvision.{key} must be a non-empty {want.__name__}", 2)
    unknown = sorted(set(raw) - {"enabled", "spec", "prefix"})
    if unknown:
        die(f"config formsProvision has unknown key(s): {', '.join(unknown)}", 2)
    return raw

def resolve_token(opts, portal):
    """Token precedence: --token flag > portal tokenEnv var > HS_TOKEN > prompt.

    tokenEnv names the env var holding THIS portal's private-app token, so each
    portal entry points at its own secret when working across portals. Fail
    closed: a configured-but-unset tokenEnv dies instead of silently falling
    back to another portal's HS_TOKEN. Mirrors the same-named helper in
    deploy.sh (no shared lib by repo convention — keep in sync).
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

def spec_error(where, msg):
    die(f"spec error ({where}): {msg}", 2)

def load_spec(path):
    try:
        with open(path, encoding="utf-8") as handle:
            data = json.load(handle)
    except (OSError, ValueError) as exc:
        die(f"cannot read spec {path}: {exc}", 2)
    if not isinstance(data, dict) or not isinstance(data.get("forms"), list) or not data["forms"]:
        spec_error(path, 'top level must be {"forms": [non-empty list]}')
    seen = set()
    for idx, form in enumerate(data["forms"]):
        where = f"forms[{idx}]"
        if not isinstance(form, dict):
            spec_error(where, "must be an object")
        for key in ("module", "name"):
            if not isinstance(form.get(key), str) or not form[key].strip():
                spec_error(where, f'"{key}" must be a non-empty string')
        if form["module"] in seen:
            spec_error(where, f'duplicate module "{form["module"]}"')
        seen.add(form["module"])
        fields = form.get("fields")
        if not isinstance(fields, list) or not fields:
            spec_error(where, '"fields" must be a non-empty list')
        for fidx, field in enumerate(fields):
            validate_field(f"{where}.fields[{fidx}]", field)
        validate_consent(f"{where}.consent", form.get("consent"), fields)
        for key, want in (("submitText", str), ("redirectUrl", str),
                          ("thankYouText", str), ("language", str)):
            if key in form and (not isinstance(form[key], want) or not form[key].strip()):
                spec_error(where, f'"{key}" must be a non-empty string')
        if "redirectUrl" in form and "thankYouText" in form:
            spec_error(where, 'only one of "redirectUrl" / "thankYouText"')
        if "recaptcha" in form and not isinstance(form["recaptcha"], bool):
            spec_error(where, '"recaptcha" must be boolean')
        if "notifyRecipients" in form and (
                not isinstance(form["notifyRecipients"], list)
                or not all(isinstance(v, str) and v.strip() for v in form["notifyRecipients"])):
            spec_error(where, '"notifyRecipients" must be a list of user-id strings')
    return data["forms"]

def validate_field(where, field):
    if not isinstance(field, dict):
        spec_error(where, "must be an object")
    for key in ("name", "label", "type"):
        if not isinstance(field.get(key), str) or not field[key].strip():
            spec_error(where, f'"{key}" must be a non-empty string')
    ftype = field["type"]
    if ftype not in FIELD_TYPES:
        spec_error(where, f'unknown type "{ftype}" (want one of: {", ".join(sorted(FIELD_TYPES))})')
    if "required" in field and not isinstance(field["required"], bool):
        spec_error(where, '"required" must be boolean')
    if ftype == "select":
        options = field.get("options")
        if (not isinstance(options, list) or not options
                or not all(isinstance(o, dict) and isinstance(o.get("label"), str)
                           and isinstance(o.get("value"), str) and o["label"].strip()
                           and o["value"].strip() for o in options)):
            spec_error(where, '"options" must be a non-empty [{label, value}] list for select')
    elif "options" in field:
        spec_error(where, f'"options" is only valid for select (not {ftype})')
    if ftype == "consent":
        if not isinstance(field.get("subscriptionTypeId"), int):
            spec_error(where, '"subscriptionTypeId" (int) is required for consent')
    elif "subscriptionTypeId" in field:
        spec_error(where, f'"subscriptionTypeId" is only valid for consent (not {ftype})')
    if "blockFreeEmail" in field:
        if ftype != "email" or not isinstance(field["blockFreeEmail"], bool):
            spec_error(where, '"blockFreeEmail" is a boolean valid only for email')
    if "useCountryCodeSelect" in field:
        if ftype != "phone" or not isinstance(field["useCountryCodeSelect"], bool):
            spec_error(where, '"useCountryCodeSelect" is a boolean valid only for phone')
    for key in ("placeholder", "description"):
        if key in field and (not isinstance(field[key], str) or ftype == "consent"):
            spec_error(where, f'"{key}" must be a string (and is meaningless on consent)')

def validate_consent(where, consent, fields):
    has_consent_fields = any(isinstance(f, dict) and f.get("type") == "consent" for f in fields)
    if consent is None:
        if has_consent_fields:
            spec_error(where, 'a consent object with "privacyText" is required '
                               'when consent-type fields are present')
        return
    if not isinstance(consent, dict):
        spec_error(where, "must be an object")
    mode = consent.get("mode", "implicit" if has_consent_fields else "none")
    if mode not in CONSENT_MODES:
        spec_error(where, f'unknown mode "{mode}" (want one of: none/implicit/explicit)')
    if mode == "none" and has_consent_fields:
        spec_error(where, 'mode "none" contradicts consent-type fields (drop them or pick implicit/explicit)')
    if mode != "none" and not has_consent_fields:
        spec_error(where, f'mode "{mode}" needs at least one consent-type field')
    for key in ("privacyText", "communicationConsentText", "consentToProcessText",
                "consentToProcessCheckboxLabel", "consentToProcessFooterText"):
        if key in consent and (not isinstance(consent[key], str) or not consent[key].strip()):
            spec_error(where, f'"{key}" must be a non-empty string')
    if mode != "none" and not isinstance(consent.get("privacyText"), str):
        spec_error(where, f'mode "{mode}" requires "privacyText" (API-required)')

def build_field(field):
    ftype = field["type"]
    out = {
        "dependentFields": [],
        "fieldType": FIELD_TYPES[ftype],
        "hidden": False,
        "label": field["label"],
        "name": field["name"],
        "objectTypeId": "0-1",  # CONTACT per the create-form OpenAPI
        "required": bool(field.get("required", False)),
    }
    if ftype in ("text", "email", "phone", "textarea", "select"):
        if field.get("placeholder"):
            out["placeholder"] = field["placeholder"]
    if ftype in ("text", "email", "phone", "textarea", "select", "checkbox"):
        if field.get("description"):
            out["description"] = field["description"]
    if ftype == "email":
        out["validation"] = {"blockedEmailDomains": [],
                             "useDefaultBlockList": bool(field.get("blockFreeEmail", False))}
    elif ftype == "phone":
        out["useCountryCodeSelect"] = bool(field.get("useCountryCodeSelect", False))
        out["validation"] = {"minAllowedDigits": 7, "maxAllowedDigits": 20}
    elif ftype == "select":
        # displayOrder is required on v3 options (verified live 2026-09-27).
        out["options"] = [{"label": o["label"], "value": o["value"], "displayOrder": n}
                          for n, o in enumerate(field["options"])]
        out["defaultValues"] = []
    return out

def build_consent(form, consent_fields):
    consent = form.get("consent") or {}
    mode = consent.get("mode") or ("implicit" if consent_fields else "none")
    if mode == "none":
        return {"type": "none"}
    boxes = [{"label": f["label"], "required": bool(f.get("required", False)),
              "subscriptionTypeId": f["subscriptionTypeId"]} for f in consent_fields]
    out = {"communicationsCheckboxes": boxes,
           "privacyText": consent["privacyText"],
           "type": "explicit_consent_to_process" if mode == "explicit"
                   else "implicit_consent_to_process"}
    for key in ("communicationConsentText", "consentToProcessText",
                "consentToProcessCheckboxLabel", "consentToProcessFooterText"):
        if consent.get(key):
            out[key] = consent[key]
    return out

def build_payload(form, full_name):
    now = datetime.now(timezone.utc).isoformat()
    api_fields = [build_field(f) for f in form["fields"] if f["type"] != "consent"]
    consent_fields = [f for f in form["fields"] if f["type"] == "consent"]
    if "redirectUrl" in form:
        post = {"type": "redirect_url", "value": form["redirectUrl"]}
    else:
        post = {"type": "thank_you", "value": form.get("thankYouText", "Thank you.")}
    return {
        "archived": False,
        "configuration": {
            "allowLinkToResetKnownValues": False,
            "archivable": True,
            "cloneable": True,
            "createNewContactForNewEmail": True,
            "editable": True,
            "language": form.get("language", "en"),
            "lifecycleStages": [],
            "notifyContactOwner": False,
            "notifyRecipients": list(form.get("notifyRecipients", [])),
            "postSubmitAction": post,
            "prePopulateKnownValues": True,
            "recaptchaEnabled": bool(form.get("recaptcha", False)),
        },
        "createdAt": now,
        "displayOptions": {
            "renderRawHtml": False,
            "style": {
                "backgroundWidth": "100%",
                "fontFamily": "arial, helvetica, sans-serif",
                "helpTextColor": "#33475b",
                "helpTextSize": "11px",
                "labelTextColor": "#33475b",
                "labelTextSize": "13px",
                "legalConsentTextColor": "#33475b",
                "legalConsentTextSize": "12px",
                "submitAlignment": "left",
                "submitColor": "#ff7a59",
                "submitFontColor": "#ffffff",
                "submitSize": "15px",
            },
            "submitButtonText": form.get("submitText", "Submit"),
            "theme": "default_style",  # v3 enum: default is rejected (verified live 2026-09-27)
        },
        # v3 caps a group at 3 fields (verified live 2026-09-27); chunk it.
        # Shape mirrors a live GET: no richText key on the group.
        "fieldGroups": [{"fields": api_fields[i:i + 3],
                         "groupType": "default_group",
                         "richTextType": "text"}
                        for i in range(0, max(len(api_fields), 1), 3)],
        "formType": "hubspot",
        "legalConsentOptions": build_consent(form, consent_fields),
        "name": full_name,
        "updatedAt": now,
    }

def main():
    opts = parse(sys.argv[1:])
    portal = load_portal(opts["config"], opts["portal"])
    provision = forms_provision(portal)
    spec_path = opts["spec"] or provision.get("spec")
    if not spec_path:
        die("no spec: pass --spec SPEC.json or set formsProvision.spec in the portal entry", 2)
    if not os.path.isabs(spec_path):
        spec_path = os.path.join(os.path.dirname(os.path.abspath(opts["config"])), spec_path)
    prefix = opts["prefix"] if opts["prefix"] is not None else provision.get("prefix", "")
    forms = load_spec(spec_path)  # full validation BEFORE any network or token use
    full_names = {f["module"]: prefix + f["name"] for f in forms}
    if opts["dry_run"]:
        print(f"create-forms: portal {opts['portal']}: {len(forms)} form(s) from {spec_path}")
        for f in forms:
            kinds = ",".join(sorted({fld["type"] for fld in f["fields"]}))
            print(f"[DRY-RUN] {f['module']}: \"{full_names[f['module']]}\" "
                  f"({len(f['fields'])} field(s): {kinds})")
        return
    token = resolve_token(opts, portal)

    hdr_fd, hdr_path = tempfile.mkstemp(prefix="cms-forms-hdr-")  # 0600: token off ps argv
    try:
        with os.fdopen(hdr_fd, "w") as handle:
            handle.write(f'header = "Authorization: Bearer {token}"\n')

        def curl(args, step, data=None):
            argv = [CURL_BIN, "-sS", "-f", "-K", hdr_path,
                   "-H", "Content-Type: application/json", *args]
            tmp = None
            if data is not None:
                tmp_fd, tmp = tempfile.mkstemp(prefix="cms-forms-body-")
                with os.fdopen(tmp_fd, "w") as handle:
                    handle.write(data)
                argv += ["--data", f"@{tmp}"]
            try:
                proc = subprocess.run(argv, capture_output=True, text=True)
            finally:
                if tmp:
                    try: os.unlink(tmp)
                    except OSError: pass
            if proc.returncode != 0:
                body = (proc.stderr or proc.stdout or "").strip().replace(token, "[REDACTED]")[:500]
                die(f"{step} failed (exit {proc.returncode}): {body or 'no detail'}\n"
                    f"manual fallback: create the form by hand in HubSpot (Marketing > Forms), "
                    f"then add its module: guid line under portals.yaml forms: and re-run.")
            try:
                return json.loads(proc.stdout) if proc.stdout.strip() else {}
            except ValueError:
                die(f"{step} returned non-JSON: {proc.stdout.strip()[:200]}")

        existing = {}  # form name -> id
        after = None
        for _page in range(10):
            url = f"{FORMS}?limit=100" + (f"&after={after}" if after else "")
            page = curl([url], "form lookup")
            results = page.get("results", page) if isinstance(page, dict) else []
            if isinstance(results, dict):
                results = [results]
            for item in results or []:
                if isinstance(item, dict) and "name" in item and "id" in item:
                    existing.setdefault(item["name"], item["id"])
            after = (page.get("paging", {}).get("next", {}) or {}).get("after")
            if not after:
                break

        guids = {}
        for form in forms:
            module, full_name = form["module"], full_names[form["module"]]
            payload = json.dumps(build_payload(form, full_name))
            if full_name in existing:
                guid = existing[full_name]
                if opts["update"]:
                    curl(["-X", "PUT", f"{FORMS}/{guid}"], f"update form \"{full_name}\"", payload)
                    print(f"UPDATED {module} \"{full_name}\" {guid}")
                else:
                    print(f"SKIP {module} \"{full_name}\" {guid} (exists; use --update to replace)")
                guids[module] = guid
            else:
                created = curl(["-X", "POST", FORMS], f"create form \"{full_name}\"", payload)
                guid = created.get("id")
                if not guid:
                    die(f"create form \"{full_name}\" returned no id: "
                        f"{json.dumps(created)[:200]}")
                print(f"CREATED {module} \"{full_name}\" {guid}")
                guids[module] = guid
                existing[full_name] = guid
            print(f"FORM_GUID {module}={guids[module]}")
        if opts["out"]:
            with open(opts["out"], "w", encoding="utf-8") as handle:
                json.dump(guids, handle, indent=2, sort_keys=True)
                handle.write("\n")
        print(f"create-forms: done: {len(guids)} form(s) for portal {opts['portal']}")
    finally:
        try: os.unlink(hdr_path)
        except OSError: pass

main()
PYEOF
