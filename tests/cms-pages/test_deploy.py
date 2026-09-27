from __future__ import annotations

import json
import os
import shutil
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
FIX = REPO_ROOT / "tests" / "cms-pages" / "fixtures"
SKILL_SCRIPTS = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts"


def validated_zip(tmp: Path) -> Path:
    theme = tmp / "mini-theme"
    if theme.exists():
        shutil.rmtree(theme)
    shutil.copytree(FIX / "mini-theme", theme)
    out = tmp / "dist"
    out.mkdir(exist_ok=True)
    env = dict(os.environ)
    env["HS_BIN"] = str(FIX / "fake-hs")
    subprocess.run(
        [str(SKILL_SCRIPTS / "validate-theme.sh"), str(theme), "--inventory", str(FIX / "mini-inventory.json")],
        text=True, capture_output=True, env=env, check=True,
    )
    packaged = subprocess.run(
        [str(SKILL_SCRIPTS / "package-zip.sh"), str(theme), str(out), "--date", "20260926"],
        text=True, capture_output=True, check=True,
    )
    return Path(packaged.stdout.strip().removeprefix("PACKAGED: ").strip())


class DeployTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.zip = validated_zip(self.tmp)
        self.config = FIX / "portals.yaml"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def run_deploy(self, *args: str, env_extra: dict | None = None) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        env["CURL_BIN"] = str(FIX / "fake-curl")
        if env_extra:
            env.update(env_extra)
        return subprocess.run(
            [str(SKILL_SCRIPTS / "deploy.sh"), *args],
            text=True, capture_output=True, env=env, input="",
        )

    def test_no_yes_stops_after_plan(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run")
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertIn("AUTHORIZATION REQUIRED", result.stdout)
        self.assertIn("DRY-RUN", result.stdout)

    def test_dry_run_with_yes_lists_all_steps(self) -> None:
        result = self.run_deploy("--portal", "prod", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        for step in ("verify evidence", "upload images", "upload theme", "pages", "menus", "blog", "forms"):
            self.assertIn(step, result.stdout)

    def test_refuses_unvalidated_zip(self) -> None:
        bad = self.tmp / "bad.zip"
        shutil.copy(self.zip, bad)
        subprocess.run(["zip", "-d", str(bad), "mini-theme/QA-EVIDENCE.json"],
                       text=True, capture_output=True, check=True)
        result = self.run_deploy("--portal", "staging", "--zip", str(bad), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("QA-EVIDENCE", result.stderr + result.stdout)

    def test_unknown_portal_is_usage_error(self) -> None:
        result = self.run_deploy("--portal", "nope", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 2)

    def test_live_with_fakes_succeeds(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NOT automated", result.stdout)

    def test_live_curl_failure_redacts_token(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--yes",
                                env_extra={"FAKE_CURL_FAIL": "1"})
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertNotIn("pat-test-1234", result.stdout + result.stderr)
        self.assertIn("failed (exit 22)", result.stderr)

    def test_parse_missing_value_usage(self) -> None:
        result = self.run_deploy("--portal")
        self.assertEqual(result.returncode, 2, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_malformed_config_clean_error(self) -> None:
        bad = self.tmp / "bad-portals.yaml"
        bad.write_text("{{{\nnot: [valid\n", encoding="utf-8")
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip), "--config", str(bad),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def _zip_with_form_module(self, name: str = "contact_form") -> Path:
        # Inject a form module per the SB-7 marker rule (fields.json entry with
        # "type": "form"), then validate + package exactly like validated_zip().
        theme = self.tmp / "form-theme"
        if theme.exists():
            shutil.rmtree(theme)
        shutil.copytree(FIX / "mini-theme", theme)
        mod = theme / "modules" / f"{name}.module"
        mod.mkdir()
        shutil.copy(theme / "modules" / "header.module" / "meta.json", mod / "meta.json")
        (mod / "fields.json").write_text(json.dumps([
            {"type": "text", "name": "section_id", "label": "Section id",
             "default": f"{name}_instance"},
            {"type": "form", "name": "hs_form", "label": "HubSpot form",
             "default": {"form_id": ""}},
        ]), encoding="utf-8")
        # S4: form modules must render via a native {% form %} tag.
        (mod / "module.html").write_text(
            f'<section id="{{{{ module.section_id }}}}">{{% form "{name}_instance" '
            'form_to_use="{{ module.hs_form.form_id }}" %}</section>\n',
            encoding="utf-8")
        (mod / "module.css").write_text("/* form module */\n", encoding="utf-8")
        out = self.tmp / "dist-form"
        out.mkdir(exist_ok=True)
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        subprocess.run(
            [str(SKILL_SCRIPTS / "validate-theme.sh"), str(theme), "--inventory", str(FIX / "mini-inventory.json")],
            text=True, capture_output=True, env=env, check=True,
        )
        packaged = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(theme), str(out), "--date", "20260926"],
            text=True, capture_output=True, check=True,
        )
        return Path(packaged.stdout.strip().removeprefix("PACKAGED: ").strip())

    def _config_with_forms(self, forms: dict, provision: dict | None = None,
                             extra: dict | None = None) -> Path:
        cfg = self.tmp / "portals-forms.yaml"
        lines = ["portals:", "  - id: staging", "    portalId: 11111111",
                 "    hsAccount: test-staging", "    theme: mini-staging",
                 "    staging: true", "    blogId: null", "    domain: null"]
        for key, value in (extra or {}).items():
            lines.append(f"    {key}: {value}")
        if forms:
            lines.append("    forms:")
            for key, guid in forms.items():
                lines.append(f'      {key}: "{guid}"')
        else:
            lines.append("    forms: {}")
        if provision is not None:
            lines.append("    formsProvision:")
            for key, value in provision.items():
                rendered = "true" if value is True else "false" if value is False else f'"{value}"'
                lines.append(f"      {key}: {rendered}")
        cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return cfg

    def _write_spec(self, modules: list[str]) -> Path:
        spec = self.tmp / "forms-spec.json"
        spec.write_text(json.dumps({"forms": [
            {"module": module, "name": module.replace("_", " ").title(),
             "fields": [{"name": "email", "label": "Email", "type": "email",
                         "required": True}]}
            for module in modules
        ]}), encoding="utf-8")
        return spec

    def test_unmapped_form_module_refuses_dry_run(self) -> None:
        zip_path = self._zip_with_form_module()
        result = self.run_deploy("--portal", "staging", "--zip", str(zip_path),
                                "--config", str(self._config_with_forms({})),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("contact_form", result.stderr)

    def test_mapped_form_module_dry_run_ok(self) -> None:
        zip_path = self._zip_with_form_module()
        result = self.run_deploy("--portal", "staging", "--zip", str(zip_path),
                                "--config", str(self._config_with_forms(
                                    {"contact_form": "00000000-0000-0000-0000-000000000000"})),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("DRY-RUN", result.stdout)

    def test_provisioned_form_module_dry_run_ok(self) -> None:
        zip_path = self._zip_with_form_module()
        spec = self._write_spec(["contact_form"])
        result = self.run_deploy("--portal", "staging", "--zip", str(zip_path),
                                "--config", str(self._config_with_forms(
                                    {}, {"enabled": True, "spec": str(spec)})),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("2b. provision forms: 1 form(s)", result.stdout)
        self.assertIn("1 provisioned form(s)", result.stdout)

    def test_provision_live_surfaces_guids(self) -> None:
        zip_path = self._zip_with_form_module()
        spec = self._write_spec(["contact_form"])
        result = self.run_deploy("--portal", "staging", "--zip", str(zip_path),
                                "--config", str(self._config_with_forms(
                                    {}, {"enabled": True, "spec": str(spec)})),
                                "--token", "pat-test-1234", "--yes")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("FORM_GUID contact_form=11111111-1111-1111-1111-111111111111", result.stdout)
        self.assertIn("1 form(s) provisioned", result.stdout)

    def test_provision_disabled_keeps_fail_closed(self) -> None:
        zip_path = self._zip_with_form_module()
        spec = self._write_spec(["contact_form"])
        result = self.run_deploy("--portal", "staging", "--zip", str(zip_path),
                                "--config", str(self._config_with_forms(
                                    {}, {"enabled": False, "spec": str(spec)})),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 1, result.stdout + result.stderr)
        self.assertIn("contact_form", result.stderr)
        self.assertNotIn("2b. provision forms", result.stdout)

    def test_provision_malformed_is_clean_error(self) -> None:
        cfg = self.tmp / "bad-provision.yaml"
        cfg.write_text("portals:\n  - id: staging\n    portalId: 11111111\n"
                       "    hsAccount: test-staging\n    theme: mini-staging\n"
                       "    staging: true\n    blogId: null\n    domain: null\n"
                       "    forms: {}\n    formsProvision: [not, a, mapping]\n",
                       encoding="utf-8")
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip),
                                "--config", str(cfg),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("formsProvision must be a mapping", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_provision_missing_spec_is_clean_error(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip),
                                "--config", str(self._config_with_forms(
                                    {}, {"enabled": True,
                                         "spec": str(self.tmp / "no-such-spec.json")})),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("cannot read formsProvision.spec", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_traversal_refused(self) -> None:
        theme = self.tmp / "evil-theme"
        shutil.copytree(FIX / "mini-theme", theme)
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        subprocess.run(
            [str(SKILL_SCRIPTS / "validate-theme.sh"), str(theme), "--inventory", str(FIX / "mini-inventory.json")],
            text=True, capture_output=True, env=env, check=True,
        )
        # Mutate AFTER validate: validator gate 4 rejects missing/unreferenced
        # manifest locals, so the bad entry must be introduced post-validation.
        assets_path = theme / "assets.json"
        manifest = json.loads(assets_path.read_text(encoding="utf-8"))
        manifest["files"].append({"local": "../../evil.txt", "dest": "/evil.txt"})
        assets_path.write_text(json.dumps(manifest), encoding="utf-8")
        # Backdate so the evidence-freshness check passes and the run reaches
        # the traversal guard (zip/unzip preserve mtimes).
        old = time.time() - 3600
        os.utime(assets_path, (old, old))
        out = self.tmp / "dist-evil"
        out.mkdir(exist_ok=True)
        packaged = subprocess.run(
            [str(SKILL_SCRIPTS / "package-zip.sh"), str(theme), str(out), "--date", "20260926"],
            text=True, capture_output=True, check=True,
        )
        evil_zip = Path(packaged.stdout.strip().removeprefix("PACKAGED: ").strip())
        result = self.run_deploy("--portal", "staging", "--zip", str(evil_zip), "--config", str(self.config),
                                "--token", "pat-test-1234", "--dry-run", "--yes")
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("escapes theme dir", result.stderr)

    def test_token_env_resolves_named_var_live(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip),
                                "--config", str(self._config_with_forms(
                                    {}, extra={"tokenEnv": "HS_TOKEN_MINI_TEST"})),
                                "--yes",
                                env_extra={"HS_TOKEN_MINI_TEST": "pat-test-1234"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[LIVE] done", result.stdout)

    def test_token_env_unset_fails_closed_live(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip),
                                "--config", str(self._config_with_forms(
                                    {}, extra={"tokenEnv": "HS_TOKEN_MINI_TEST"})),
                                "--yes",
                                env_extra={"HS_TOKEN_MINI_TEST": ""})
        self.assertEqual(result.returncode, 1, result.stderr)
        self.assertIn("HS_TOKEN_MINI_TEST", result.stderr)
        self.assertIn("unset or empty", result.stderr)

    def test_token_flag_overrides_token_env(self) -> None:
        result = self.run_deploy("--portal", "staging", "--zip", str(self.zip),
                                "--config", str(self._config_with_forms(
                                    {}, extra={"tokenEnv": "HS_TOKEN_MINI_TEST"})),
                                "--token", "pat-test-1234", "--yes",
                                env_extra={"HS_TOKEN_MINI_TEST": ""})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("[LIVE] done", result.stdout)


if __name__ == "__main__":
    unittest.main()
