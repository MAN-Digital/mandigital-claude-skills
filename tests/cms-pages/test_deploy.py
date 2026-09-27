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
        (mod / "module.html").write_text(
            '<section id="{{ module.section_id }}">{{ module.hs_form }}</section>\n',
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

    def _config_with_forms(self, forms: dict) -> Path:
        cfg = self.tmp / "portals-forms.yaml"
        lines = ["portals:", "  - id: staging", "    portalId: 11111111",
                 "    hsAccount: test-staging", "    theme: mini-staging",
                 "    staging: true", "    blogId: null", "    domain: null"]
        if forms:
            lines.append("    forms:")
            for key, guid in forms.items():
                lines.append(f'      {key}: "{guid}"')
        else:
            lines.append("    forms: {}")
        cfg.write_text("\n".join(lines) + "\n", encoding="utf-8")
        return cfg

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


if __name__ == "__main__":
    unittest.main()
