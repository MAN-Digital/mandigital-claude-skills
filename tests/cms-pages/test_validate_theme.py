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

    def test_clean_lint_output_passes_gate3(self) -> None:
        # SB-2 guard: a clean "0 issues found." lint summary must NOT trip the
        # gate-3 NZ-issues detector — the lead-digit class must stay [1-9], so
        # a future simplification to [0-9]+ fails loudly here, not in prod.
        result = run_validator(self.theme, self.inventory, {"FAKE_HS_CLEAN": "1"})
        self.assertEqual(result.returncode, 0, result.stderr)
        evidence = json.loads((self.theme / "QA-EVIDENCE.json").read_text(encoding="utf-8"))
        self.assertEqual(evidence["gates"], {"g1": "pass", "g2": "pass", "g3": "pass", "g4": "pass"})

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

    # S1: HubSpot-emitted "src" : "..." (space before colon) must match.
    def test_spaced_src_with_manifest_passes(self) -> None:
        fields = self.theme / "modules" / "header.module" / "fields.json"
        text = fields.read_text(encoding="utf-8").replace('"src": "/brand/x.jpg"', '"src" : "/brand/x.jpg"')
        self.assertIn('"src" : ', text)
        fields.write_text(text, encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_spaced_src_without_manifest_fails_gate4(self) -> None:
        fields = self.theme / "modules" / "header.module" / "fields.json"
        text = fields.read_text(encoding="utf-8").replace('"src": "/brand/x.jpg"', '"src" : "/brand/none.jpg"')
        fields.write_text(text, encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g4", result.stderr)
        self.assertIn("unmanifested image src /brand/none.jpg", result.stderr)

    # S4 (gate-2): form-type field requires a native {% form %} tag.
    def _add_form_module(self, name: str, html: str) -> None:
        mod = self.theme / "modules" / f"{name}.module"
        mod.mkdir()
        (mod / "fields.json").write_text(
            json.dumps([{"type": "form", "name": "hs_form", "label": "Form",
                         "default": {"form_id": "abc"}}]), encoding="utf-8")
        (mod / "meta.json").write_text(
            json.dumps({"host_template_types": ["PAGE"], "content_types": ["ANY"]}),
            encoding="utf-8")
        (mod / "module.html").write_text(html, encoding="utf-8")

    def test_form_field_with_native_tag_passes(self) -> None:
        self._add_form_module(
            "enquiry_form",
            '{% form "enquiry_form_instance" form_to_use="{{ module.hs_form.form_id }}" %}\n')
        result = run_validator(self.theme, self.inventory)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_form_field_without_tag_fails_gate2(self) -> None:
        self._add_form_module("enquiry_form", "<div>{{ module.hs_form }}</div>\n")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)
        self.assertIn("enquiry_form.module", result.stderr)
        self.assertIn("form field without {% form %} tag", result.stderr)

    def test_form_field_custom_submit_warns_not_fails(self) -> None:
        self._add_form_module(
            "enquiry_form",
            '<form data-hsforms-ignore="true">{{ module.hs_form }}</form>\n')
        result = run_validator(self.theme, self.inventory)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("WARN: enquiry_form.module uses custom form submit", result.stderr)

    # S6 (gate-4): [...] placeholders in defaults fail; clean defaults pass.
    def _add_footer_text_field(self, name: str, default: object) -> None:
        fields = self.theme / "modules" / "footer.module" / "fields.json"
        data = json.loads(fields.read_text(encoding="utf-8"))
        data.append({"type": "text", "name": name, "label": name, "default": default})
        fields.write_text(json.dumps(data), encoding="utf-8")
        footer = self.theme / "modules" / "footer.module" / "module.html"
        footer.write_text(footer.read_text(encoding="utf-8") + "{{ module." + name + " }}\n",
                          encoding="utf-8")

    def test_bracket_placeholder_default_fails_gate4(self) -> None:
        self._add_footer_text_field("brochure", "PDF, [size]")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g4", result.stderr)
        self.assertIn("footer.module/fields.json", result.stderr)
        self.assertIn("PDF, [size]", result.stderr)

    def test_long_bracket_placeholder_default_fails_gate4(self) -> None:
        long_token = ("[Plassholder – før opp kjente avvik, for eksempel PDF-dokumenter "
                      "som ennå ikke er fullt tilgjengelige.]")
        self.assertGreater(len(long_token), 60)
        self._add_footer_text_field("note", "<p>" + long_token + "</p>")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g4", result.stderr)
        self.assertIn("footer.module/fields.json", result.stderr)

    def test_clean_default_passes_gate4(self) -> None:
        self._add_footer_text_field("brochure", "PDF, 2 MB")
        result = run_validator(self.theme, self.inventory)
        self.assertEqual(result.returncode, 0, result.stderr)

    # S8 (gate-2): <img> with {{ }} src needs an {% if %} guard.
    def test_guarded_img_passes_gate2(self) -> None:
        header = self.theme / "modules" / "header.module" / "module.html"
        header.write_text(
            '<a href="/kontakt">{{ module.cta_text }}</a>\n'
            "{% if module.logo.src %}\n"
            '<img src="{{ module.logo.src }}" alt="{{ module.logo.alt }}">\n'
            "{% endif %}\n", encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertEqual(result.returncode, 0, result.stderr)

    def test_unguarded_img_fails_gate2(self) -> None:
        header = self.theme / "modules" / "header.module" / "module.html"
        header.write_text(
            '<a href="/kontakt">{{ module.cta_text }}</a><img src="{{ module.logo.src }}" alt="">\n',
            encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)
        self.assertIn("header.module/module.html:1", result.stderr)

    # S9 (gate-2): HubSpot-reserved field names fail before upload.
    def test_reserved_field_name_fails_gate2(self) -> None:
        self._add_footer_text_field("body", "hello")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)
        self.assertIn("reserved field name footer.module/body", result.stderr)

    def test_reserved_child_name_fails_gate2(self) -> None:
        fields = self.theme / "modules" / "footer.module" / "fields.json"
        data = json.loads(fields.read_text(encoding="utf-8"))
        data.append({"type": "group", "name": "columns", "label": "columns",
                     "children": [{"type": "text", "name": "label", "label": "label"}]})
        fields.write_text(json.dumps(data), encoding="utf-8")
        footer = self.theme / "modules" / "footer.module" / "module.html"
        footer.write_text(footer.read_text(encoding="utf-8")
                          + "{{ module.columns }}{{ x.label }}\n",
                          encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)
        self.assertIn("reserved field name footer.module/label", result.stderr)

    # S10 (gate-2): group default row keys must match child names.
    def test_stale_default_row_key_fails_gate2(self) -> None:
        fields = self.theme / "modules" / "footer.module" / "fields.json"
        data = json.loads(fields.read_text(encoding="utf-8"))
        data.append({"type": "group", "name": "columns", "label": "columns",
                     "children": [{"type": "text", "name": "heading", "label": "heading"}],
                     "default": [{"headline": "hi"}]})
        fields.write_text(json.dumps(data), encoding="utf-8")
        footer = self.theme / "modules" / "footer.module" / "module.html"
        footer.write_text(footer.read_text(encoding="utf-8")
                          + "{{ module.columns }}{{ x.heading }}\n",
                          encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)
        self.assertIn("default row key 'headline' matches no child of 'columns'",
                      result.stderr)

    # S11 (gate-2): unknown field types fail before upload.
    def test_textarea_type_fails_gate2(self) -> None:
        fields = self.theme / "modules" / "footer.module" / "fields.json"
        data = json.loads(fields.read_text(encoding="utf-8"))
        data.append({"type": "textarea", "name": "blurb", "label": "blurb",
                     "default": "hi"})
        fields.write_text(json.dumps(data), encoding="utf-8")
        footer = self.theme / "modules" / "footer.module" / "module.html"
        footer.write_text(footer.read_text(encoding="utf-8") + "{{ module.blurb }}\n",
                          encoding="utf-8")
        result = run_validator(self.theme, self.inventory)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("FAIL: g2", result.stderr)
        self.assertIn("invalid field type 'textarea' on 'blurb'", result.stderr)


if __name__ == "__main__":
    unittest.main()
