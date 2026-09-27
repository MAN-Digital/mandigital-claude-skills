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
SCRIPT = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts" / "validate-theme.sh"


def run_validator(theme: Path, inventory: Path, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["HS_BIN"] = str(FIX / "fake-hs")
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [str(SCRIPT), str(theme), "--inventory", str(inventory)],
        text=True, capture_output=True, env=env,
    )


class ValidateThemeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.theme = self.tmp / "mini-theme"
        shutil.copytree(FIX / "mini-theme", self.theme)
        self.inventory = FIX / "mini-inventory.json"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_valid_theme_passes(self) -> None:
        result = run_validator(self.theme, self.inventory)
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads((self.theme / "QA-EVIDENCE.json").read_text(encoding="utf-8"))
        self.assertEqual(evidence["gates"], {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"})
        self.assertEqual(evidence["theme"], "mini")

    def test_orphan_field_fails_gate2(self) -> None:
        fields = self.theme / "modules" / "footer.module" / "fields.json"
        data = json.loads(fields.read_text(encoding="utf-8"))
        data.append({"type": "text", "name": "orphan", "label": "Orphan", "default": "x"})
        fields.write_text(json.dumps(data), encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)

    def test_unmanifested_image_fails_gate4(self) -> None:
        fields = self.theme / "modules" / "header.module" / "fields.json"
        text = fields.read_text(encoding="utf-8").replace("/brand/x.jpg", "/brand/missing.jpg")
        fields.write_text(text, encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g4", result.stderr)

    def test_hs_failure_fails_gate3(self) -> None:
        result = run_validator(self.theme, self.inventory, {"FAKE_HS_FAIL": "1"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g3", result.stderr)

    def test_dangling_deploy_entry_fails_gate1(self) -> None:
        deploy = self.theme / "deploy.json"
        data = json.loads(deploy.read_text(encoding="utf-8"))
        data["pages"].append({"slug": "ghost", "title": "Ghost", "templatePath": "templates/ghost.html", "menuOrder": 20})
        deploy.write_text(json.dumps(data), encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g1", result.stderr)

    def test_deleted_template_fails_gate1(self) -> None:
        (self.theme / "templates" / "home.html").unlink()
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g1", result.stderr)

    def test_missing_blog_template_fails_gate1(self) -> None:
        (self.theme / "templates" / "blog_post.html").unlink()
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g1", result.stderr)

    def test_unbalanced_dnd_tags_fails_gate3(self) -> None:
        home = self.theme / "templates" / "home.html"
        text = home.read_text(encoding="utf-8").replace("{% end_dnd_section %}", "", 1)
        home.write_text(text, encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g3", result.stderr)

    def test_verbatim_phrase_passes_gate2(self) -> None:
        footer = self.theme / "modules" / "footer.module" / "module.html"
        footer.write_text(footer.read_text(encoding="utf-8") + "<p>Buy now</p>\n", encoding="utf-8")
        inv = json.loads(self.inventory.read_text(encoding="utf-8"))
        inv["verbatim"] = ["Buy now"]
        tmp_inv = self.tmp / "inventory.json"
        tmp_inv.write_text(json.dumps(inv), encoding="utf-8")
        result = run_validator(self.theme, tmp_inv)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_invalid_json_clean_message(self) -> None:
        (self.theme / "deploy.json").write_text("{not valid json", encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g1", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_missing_preview_path_fails_gate1(self) -> None:
        theme_json = self.theme / "theme.json"
        data = json.loads(theme_json.read_text(encoding="utf-8"))
        del data["preview_path"]
        theme_json.write_text(json.dumps(data), encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g1", result.stderr)

    def test_meta_missing_content_types_fails_gate1(self) -> None:
        meta = self.theme / "modules" / "header.module" / "meta.json"
        data = json.loads(meta.read_text(encoding="utf-8"))
        del data["content_types"]
        meta.write_text(json.dumps(data), encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g1", result.stderr)

    def _inject_richtext_link(self, url: str) -> None:
        # SB-1: an https link inside a JSON field default is stored with \"
        # escapes, so the raw-text URL regex used to swallow a trailing "\\".
        fields = self.theme / "modules" / "footer.module" / "fields.json"
        data = json.loads(fields.read_text(encoding="utf-8"))
        data.append({"type": "richtext", "name": "body_copy", "label": "Body",
                     "default": f'<a href="{url}">y</a>'})
        fields.write_text(json.dumps(data), encoding="utf-8")
        footer = self.theme / "modules" / "footer.module" / "module.html"
        footer.write_text(footer.read_text(encoding="utf-8") + "{{ module.body_copy }}\n",
                          encoding="utf-8")

    def test_json_escaped_allowlisted_url_passes_gate4(self) -> None:
        # NOTE: host must avoid the gate-4 BANNED list ("example.com" is banned),
        # so .net stands in for the dry-run's real-world .no URL.
        url = "https://allowed.example.net/x"
        self._inject_richtext_link(url)
        inv = json.loads(self.inventory.read_text(encoding="utf-8"))
        inv["external_urls"] = [url]
        tmp_inv = self.tmp / "inventory.json"
        tmp_inv.write_text(json.dumps(inv), encoding="utf-8")
        result = run_validator(self.theme, tmp_inv)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue((self.theme / "QA-EVIDENCE.json").is_file())

    def test_json_escaped_url_control_names_clean_url(self) -> None:
        url = "https://allowed.example.net/x"
        self._inject_richtext_link(url)
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g4", result.stderr)
        self.assertIn(f"unallowlisted external URL {url} in", result.stderr)
        self.assertNotIn(url + "\\", result.stderr)

    def test_lint_output_errors_fail_gate3_despite_exit_zero(self) -> None:
        result = run_validator(self.theme, self.inventory, {"FAKE_HS_ERRORS": "1"})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g3", result.stderr)

    def test_hs_account_passthrough_passes_clean(self) -> None:
        result = run_validator(self.theme, self.inventory, {"HS_ACCOUNT": "foo"})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--account=foo", result.stdout)
        self.assertTrue((self.theme / "QA-EVIDENCE.json").is_file())

    def test_missing_inventory_flag_is_usage_error(self) -> None:
        env = dict(os.environ)
        env["HS_BIN"] = str(FIX / "fake-hs")
        result = subprocess.run([str(SCRIPT), str(self.theme)], text=True, capture_output=True, env=env)
        self.assertEqual(result.returncode, 2)


if __name__ == "__main__":
    unittest.main()
