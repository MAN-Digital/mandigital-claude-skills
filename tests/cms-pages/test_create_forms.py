from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SCRIPT = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts" / "create-forms.sh"


def run_forms(*args: str, env_extra: dict[str, str] | None = None,
              env_drop: list[str] | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["CURL_BIN"] = str(FIX / "fake-curl")
    if env_extra:
        env.update(env_extra)
    for key in env_drop or []:
        env.pop(key, None)
    return subprocess.run(
        [str(SCRIPT), *args],
        text=True, capture_output=True, env=env, input="",
    )


def write_spec(tmp: Path, forms: list) -> Path:
    spec = tmp / "forms-spec.json"
    spec.write_text(json.dumps({"forms": forms}), encoding="utf-8")
    return spec


def write_config(tmp: Path, provision: dict | None, extra: dict | None = None) -> Path:
    cfg = tmp / "portals-forms.yaml"
    lines = ["portals:", "  - id: staging", "    portalId: 11111111",
             "    hsAccount: test-staging", "    theme: mini-staging",
             "    staging: true", "    blogId: null", "    domain: null",
             "    forms: {}"]
    for key, value in (extra or {}).items():
        lines.append(f"    {key}: {value}")
    if provision is not None:
        lines.append("    formsProvision:")
        for key, value in provision.items():
            rendered = "true" if value is True else "false" if value is False else f'"{value}"'
            lines.append(f"      {key}: {rendered}")
    cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return cfg


CONTACT_FORM = {
    "module": "contact_form",
    "name": "Contact",
    "fields": [
        {"name": "firstname", "label": "First name", "type": "text", "required": True},
        {"name": "email", "label": "Business email", "type": "email", "required": True,
         "blockFreeEmail": True},
    ],
    "submitText": "Send",
}


class CreateFormsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.config = FIX / "portals.yaml"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_unknown_type_is_spec_error_without_network(self) -> None:
        bad = dict(CONTACT_FORM, fields=[
            {"name": "x", "label": "X", "type": "wizard", "required": False},
        ])
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [bad])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('unknown type "wizard"', result.stderr)
        self.assertFalse(log.exists(), "spec errors must precede any network call")

    def test_select_without_options_is_spec_error(self) -> None:
        bad = dict(CONTACT_FORM, fields=[
            {"name": "size", "label": "Size", "type": "select", "required": False},
        ])
        result = run_forms("--spec", str(write_spec(self.tmp, [bad])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('"options" must be a non-empty [{label, value}] list', result.stderr)

    def test_consent_without_subscription_is_spec_error(self) -> None:
        bad = dict(CONTACT_FORM, fields=[
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "consent", "label": "Consent", "type": "consent", "required": True},
        ], consent={"mode": "implicit", "privacyText": "We process data."})
        result = run_forms("--spec", str(write_spec(self.tmp, [bad])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('"subscriptionTypeId"', result.stderr)

    def test_consent_fields_without_consent_object_is_spec_error(self) -> None:
        bad = dict(CONTACT_FORM, fields=[
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "consent", "label": "Consent", "type": "consent", "required": True,
             "subscriptionTypeId": 12345},
        ])
        result = run_forms("--spec", str(write_spec(self.tmp, [bad])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("privacyText", result.stderr)

    def test_create_path_posts_and_emits_guid(self) -> None:
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('CREATED contact_form "Contact"', result.stdout)
        self.assertIn("FORM_GUID contact_form=11111111-1111-1111-1111-111111111111", result.stdout)
        calls = log.read_text(encoding="utf-8")
        self.assertIn("GET https://api.hubapi.com/marketing/v3/forms?limit=100", calls)
        self.assertIn("POST https://api.hubapi.com/marketing/v3/forms", calls)
        # Payload mirrors the verified v3 shape: fieldType mapping + contact object id.
        self.assertIn('"fieldType": "single_line_text"', calls)
        self.assertIn('"fieldType": "email"', calls)
        self.assertIn('"useDefaultBlockList": true', calls)
        self.assertIn('"objectTypeId": "0-1"', calls)
        self.assertIn('"type": "none"', calls)  # no consent fields -> legalConsent none
        self.assertNotIn("pat-test-1234", calls + result.stdout + result.stderr)

    def test_consent_maps_to_legal_consent_options(self) -> None:
        form = dict(CONTACT_FORM, fields=[
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "consent", "label": "Email me news", "type": "consent", "required": False,
             "subscriptionTypeId": 12345},
        ], consent={"mode": "explicit", "privacyText": "We process data.",
                    "consentToProcessText": "Process my data."})
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [form])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = log.read_text(encoding="utf-8")
        self.assertIn('"type": "explicit_consent_to_process"', calls)
        self.assertIn('"subscriptionTypeId": 12345', calls)
        self.assertIn('"privacyText": "We process data."', calls)

    def test_existing_name_skips_without_post(self) -> None:
        log = self.tmp / "curl.log"
        existing = {"results": [{"id": "aaaaaaaa-0000-0000-0000-000000000000",
                                 "name": "Contact"}]}
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_LOG": str(log),
                                      "FAKE_CURL_GET_RESP": json.dumps(existing)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('SKIP contact_form "Contact"', result.stdout)
        self.assertIn("FORM_GUID contact_form=aaaaaaaa-0000-0000-0000-000000000000", result.stdout)
        calls = log.read_text(encoding="utf-8")
        self.assertIn("GET https://api.hubapi.com/marketing/v3/forms", calls)
        self.assertNotIn("POST ", calls)
        self.assertNotIn("PUT ", calls)

    def test_update_flag_puts_existing_form(self) -> None:
        log = self.tmp / "curl.log"
        existing = {"results": [{"id": "aaaaaaaa-0000-0000-0000-000000000000",
                                 "name": "Contact"}]}
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234", "--update",
                           env_extra={"FAKE_CURL_LOG": str(log),
                                      "FAKE_CURL_GET_RESP": json.dumps(existing)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('UPDATED contact_form "Contact"', result.stdout)
        calls = log.read_text(encoding="utf-8")
        self.assertIn("PUT https://api.hubapi.com/marketing/v3/forms/aaaaaaaa-0000-0000-0000-000000000000",
                      calls)
        self.assertNotIn("POST ", calls)

    def test_out_writes_guid_map(self) -> None:
        out = self.tmp / "guids.json"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234", "--out", str(out))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(out.read_text(encoding="utf-8")),
                         {"contact_form": "11111111-1111-1111-1111-111111111111"})

    def test_dry_run_validates_without_network(self) -> None:
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--dry-run",
                           env_extra={"FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('[DRY-RUN] contact_form: "Contact"', result.stdout)
        self.assertFalse(log.exists(), "dry-run must not touch the network")

    def test_prefix_applies_to_lookup_name(self) -> None:
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234", "--prefix", "[stg] ",
                           env_extra={"FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('CREATED contact_form "[stg] Contact"', result.stdout)
        self.assertIn('"name": "[stg] Contact"', log.read_text(encoding="utf-8"))

    def test_spec_and_prefix_default_from_portal_config(self) -> None:
        spec = write_spec(self.tmp, [CONTACT_FORM])
        cfg = write_config(self.tmp, {"enabled": True, "spec": str(spec), "prefix": "[cfg] "})
        log = self.tmp / "curl.log"
        result = run_forms("--portal", "staging", "--config", str(cfg),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn('CREATED contact_form "[cfg] Contact"', result.stdout)

    def test_bad_provision_shape_is_usage_error(self) -> None:
        cfg = self.tmp / "bad-provision.yaml"
        cfg.write_text("portals:\n  - id: staging\n    portalId: 11111111\n"
                       "    hsAccount: x\n    theme: y\n    staging: true\n"
                       "    blogId: null\n    domain: null\n    forms: {}\n"
                       "    formsProvision: definitely-not-a-mapping\n", encoding="utf-8")
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(cfg),
                           "--token", "pat-test-1234")
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("formsProvision must be a mapping", result.stderr)

    def test_api_failure_names_manual_fallback(self) -> None:
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_FAIL": "1"})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("manual fallback", result.stderr)
        self.assertNotIn("pat-test-1234", result.stdout + result.stderr)

    def test_payload_matches_live_v3_shape(self) -> None:
        # theme default_style (not "default"), groups chunked <=3 fields,
        # displayOrder on select options — all verified live 2026-09-27.
        form = dict(CONTACT_FORM, fields=[
            {"name": "firstname", "label": "First", "type": "text", "required": True},
            {"name": "email", "label": "Email", "type": "email", "required": True},
            {"name": "phone", "label": "Phone", "type": "phone", "required": False},
            {"name": "course", "label": "Course", "type": "select", "required": True,
             "options": [{"label": "A", "value": "a"}, {"label": "B", "value": "b"}]},
        ])
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [form])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 0, result.stderr)
        calls = log.read_text(encoding="utf-8")
        self.assertIn('"theme": "default_style"', calls)
        self.assertEqual(calls.count('"groupType": "default_group"'), 2)
        self.assertIn('"displayOrder": 0', calls)
        self.assertIn('"displayOrder": 1', calls)
        posts = [line.split(" ", 2)[2] for line in calls.splitlines()
                 if line.startswith("POST ")]
        self.assertEqual(len(posts), 1)
        payload = json.loads(posts[0])
        # No "richText" KEY anywhere (richTextType is legitimate and stays).
        self.assertNotIn('"richText":', json.dumps(payload))
        groups = payload["fieldGroups"]
        self.assertEqual(len(groups), 2)
        for group in groups:
            self.assertLessEqual(len(group["fields"]), 3)
        self.assertEqual(sum(len(g["fields"]) for g in groups), 4)

    def test_token_env_resolves_named_var(self) -> None:
        cfg = write_config(self.tmp, None, extra={"tokenEnv": "HS_TOKEN_MINI_TEST"})
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(cfg),
                           env_extra={"HS_TOKEN_MINI_TEST": "pat-test-1234"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FORM_GUID contact_form=", result.stdout)

    def test_token_env_unset_fails_closed(self) -> None:
        cfg = write_config(self.tmp, None, extra={"tokenEnv": "HS_TOKEN_MINI_TEST"})
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(cfg),
                           env_extra={"HS_TOKEN_MINI_TEST": "",
                                      "FAKE_CURL_LOG": str(log)})
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("HS_TOKEN_MINI_TEST", result.stderr)
        self.assertIn("unset or empty", result.stderr)
        self.assertFalse(log.exists(), "token failure must precede any network call")

    def test_non_json_response_redacts_token(self) -> None:
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_LOG": str(log),
                                      "FAKE_CURL_GET_RESP": "boom pat-test-1234"})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("[REDACTED]", result.stderr)
        self.assertNotIn("pat-test-1234", result.stdout + result.stderr)

    def test_missing_id_redacts_token(self) -> None:
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "pat-test-1234",
                           env_extra={"FAKE_CURL_POST_RESP": '{"error": "pat-test-1234"}'})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("[REDACTED]", result.stderr)
        self.assertNotIn("pat-test-1234", result.stdout + result.stderr)

    def test_empty_token_flag_falls_through_to_env(self) -> None:
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "",
                           env_extra={"HS_TOKEN": "pat-test-1234",
                                      "FAKE_CURL_LOG": str(log),
                                      "FAKE_CURL_ECHO_AUTH": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        auths = [line for line in log.read_text(encoding="utf-8").splitlines()
                 if line.startswith("AUTH ")]
        self.assertTrue(auths, "expected AUTH lines in curl log")
        for line in auths:
            self.assertEqual(line, "AUTH pat-test-1234")

    def test_empty_token_flag_with_nothing_dies_before_network(self) -> None:
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "",
                           env_extra={"FAKE_CURL_LOG": str(log)},
                           env_drop=["HS_TOKEN"])
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn("no token supplied", result.stderr)
        self.assertFalse(log.exists(), "token failure must precede any network call")

    def test_whitespace_token_flag_falls_through_to_env(self) -> None:
        log = self.tmp / "curl.log"
        result = run_forms("--spec", str(write_spec(self.tmp, [CONTACT_FORM])),
                           "--portal", "staging", "--config", str(self.config),
                           "--token", "   ",
                           env_extra={"HS_TOKEN": "pat-test-1234",
                                      "FAKE_CURL_LOG": str(log),
                                      "FAKE_CURL_ECHO_AUTH": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        auths = [line for line in log.read_text(encoding="utf-8").splitlines()
                 if line.startswith("AUTH ")]
        self.assertTrue(auths, "expected AUTH lines in curl log")
        for line in auths:
            self.assertEqual(line, "AUTH pat-test-1234")


if __name__ == "__main__":
    unittest.main()
