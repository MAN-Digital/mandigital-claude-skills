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
SCRIPT = REPO_ROOT / "marketing" / "web-development" / "man-digital-cms-pages" / "scripts" / "verify-blog.sh"


def run_verify(theme: Path, *args: str, env_extra: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = dict(os.environ)
    env["HS_BIN"] = str(FIX / "fake-hs")
    if env_extra:
        env.update(env_extra)
    return subprocess.run(
        [str(SCRIPT), str(theme), *args],
        text=True, capture_output=True, env=env,
    )


class VerifyBlogTests(unittest.TestCase):
    def setUp(self) -> None:
        self.tmp = Path(tempfile.mkdtemp())
        self.theme = self.tmp / "mini-theme"
        shutil.copytree(FIX / "mini-theme", self.theme)
        self.config = FIX / "portals.yaml"

    def tearDown(self) -> None:
        shutil.rmtree(self.tmp, ignore_errors=True)

    def test_local_good_theme_exits_zero(self) -> None:
        result = run_verify(self.theme)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK templates/blog_listing.html", result.stdout)
        self.assertIn("OK templates/blog_post.html", result.stdout)
        self.assertIn("ASSIGN IN UI", result.stdout)

    def test_missing_listing_template_exits_one(self) -> None:
        (self.theme / "templates" / "blog_listing.html").unlink()
        result = run_verify(self.theme)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("missing local template: templates/blog_listing.html", result.stderr)

    def test_wrong_template_type_exits_one(self) -> None:
        listing = self.theme / "templates" / "blog_listing.html"
        listing.write_text(listing.read_text(encoding="utf-8").replace(
            "templateType: blog_listing", "templateType: page"), encoding="utf-8")
        result = run_verify(self.theme)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("templateType is 'page', want 'blog_listing'", result.stderr)

    def test_remote_staging_without_blog_id(self) -> None:
        result = run_verify(self.theme, "--portal", "staging", "--config", str(self.config))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("OK remote mini-staging/templates/blog_listing.html", result.stdout)
        self.assertIn("OK remote mini-staging/templates/blog_post.html", result.stdout)
        self.assertIn("blogId is null", result.stdout)

    def test_remote_prod_unassigned_is_informational(self) -> None:
        result = run_verify(self.theme, "--portal", "prod", "--config", str(self.config))
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("UNASSIGNED blog_listing.html (want mini/templates/blog_listing.html)",
                      result.stdout)
        self.assertIn('"Blog posts"         -> mini/templates/blog_post.html', result.stdout)

    def test_remote_prod_assigned(self) -> None:
        settings = json.dumps({
            "listingPageTemplatePath": "mini/templates/blog_listing.html",
            "postTemplatePath": "mini/templates/blog_post.html",
        })
        result = run_verify(self.theme, "--portal", "prod", "--config", str(self.config),
                            env_extra={"FAKE_BLOG_SETTINGS": settings})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("ASSIGNED blog_listing.html -> mini/templates/blog_listing.html", result.stdout)
        self.assertIn("ASSIGNED blog_post.html -> mini/templates/blog_post.html", result.stdout)

    def test_require_assigned_fails_when_unassigned(self) -> None:
        result = run_verify(self.theme, "--portal", "prod", "--config", str(self.config),
                            "--require-assigned")
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("blog templates not assigned", result.stderr)

    def test_remote_missing_template_exits_one(self) -> None:
        result = run_verify(self.theme, "--portal", "staging", "--config", str(self.config),
                            env_extra={"FAKE_CMS_MISSING": "blog_listing.html"})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("template not uploaded: mini-staging/templates/blog_listing.html",
                      result.stderr)

    def test_unreadable_assignment_is_note_not_failure(self) -> None:
        # hs key without content scope + no token: state unknown, templates OK.
        result = run_verify(self.theme, "--portal", "prod", "--config", str(self.config),
                            env_extra={"FAKE_API_FAIL": "1", "HS_TOKEN": ""})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("NOTE could not read blog assignment", result.stdout)
        self.assertIn("ASSIGN IN UI", result.stdout)

    def test_require_assigned_fails_when_unreadable(self) -> None:
        result = run_verify(self.theme, "--portal", "prod", "--config", str(self.config),
                            "--require-assigned",
                            env_extra={"FAKE_API_FAIL": "1", "HS_TOKEN": ""})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("cannot prove assignment", result.stderr)

    def test_unknown_portal_is_usage_error(self) -> None:
        result = run_verify(self.theme, "--portal", "nope", "--config", str(self.config))
        self.assertEqual(result.returncode, 2)
        self.assertIn("unknown portal", result.stderr)

    def test_portal_without_config_is_usage_error(self) -> None:
        result = run_verify(self.theme, "--portal", "staging")
        self.assertEqual(result.returncode, 2)
        self.assertIn("--portal and --config must be given together", result.stderr)

    def test_config_without_portal_is_usage_error(self) -> None:
        result = run_verify(self.theme, "--config", str(self.config))
        self.assertEqual(result.returncode, 2)
        self.assertIn("--portal and --config must be given together", result.stderr)

    def test_missing_config_is_clean_error_not_traceback(self) -> None:
        result = run_verify(self.theme, "--portal", "staging",
                            "--config", str(self.tmp / "nope.yaml"))
        self.assertEqual(result.returncode, 2)
        self.assertIn("cannot read config", result.stderr)
        self.assertNotIn("Traceback", result.stderr)

    def test_invalid_config_exits_two(self) -> None:
        bad = self.tmp / "bad.yaml"
        bad.write_text("[unclosed", encoding="utf-8")
        result = run_verify(self.theme, "--portal", "staging", "--config", str(bad))
        self.assertEqual(result.returncode, 2)
        self.assertIn("invalid config", result.stderr)

    def test_portal_missing_keys_exits_two(self) -> None:
        cfg = self.tmp / "nokeys.yaml"
        cfg.write_text("portals:\n  - id: thin\n    portalId: 1\n", encoding="utf-8")
        result = run_verify(self.theme, "--portal", "thin", "--config", str(cfg))
        self.assertEqual(result.returncode, 2)
        self.assertIn("lacks required key", result.stderr)

    def test_cms_list_failure_exits_one(self) -> None:
        result = run_verify(self.theme, "--portal", "staging", "--config", str(self.config),
                            env_extra={"FAKE_HS_FAIL": "1"})
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("hs cms list failed", result.stderr)

    def test_mismatch_reported(self) -> None:
        settings = json.dumps({
            "listingPageTemplatePath": "other-theme/templates/blog_listing.html",
            "postTemplatePath": "mini/templates/blog_post.html",
        })
        result = run_verify(self.theme, "--portal", "prod", "--config", str(self.config),
                            env_extra={"FAKE_BLOG_SETTINGS": settings})
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("MISMATCH blog_listing.html: blog uses other-theme/templates/blog_listing.html",
                      result.stdout)
        self.assertIn("ASSIGNED blog_post.html", result.stdout)

    def test_unavailable_for_new_content_fails(self) -> None:
        listing = self.theme / "templates" / "blog_listing.html"
        listing.write_text(listing.read_text(encoding="utf-8").replace(
            "isAvailableForNewContent: true", "isAvailableForNewContent: false"),
            encoding="utf-8")
        result = run_verify(self.theme)
        self.assertEqual(result.returncode, 1, result.stdout)
        self.assertIn("isAvailableForNewContent is not true", result.stderr)

    def test_tokenenv_unset_fails_closed(self) -> None:
        # Mirrors resolve_token in create-forms.sh: a configured-but-unset
        # tokenEnv dies instead of falling back to HS_TOKEN. Whitespace
        # --token falls through (does not rescue the run).
        cfg = self.tmp / "tenv.yaml"
        cfg.write_text(
            "portals:\n  - id: walled\n    portalId: 1\n    hsAccount: test-walled\n"
            "    theme: mini\n    staging: false\n    blogId: 123\n"
            "    tokenEnv: VERIFY_BLOG_TEST_UNSET_XYZ\n", encoding="utf-8")
        result = run_verify(self.theme, "--portal", "walled", "--config", str(cfg),
                            "--token", "   ",
                            env_extra={"FAKE_API_FAIL": "1", "HS_TOKEN": "wrong-portal-token"})
        self.assertEqual(result.returncode, 2, result.stdout)
        self.assertIn("VERIFY_BLOG_TEST_UNSET_XYZ (tokenEnv) is unset or empty", result.stderr)


if __name__ == "__main__":
    unittest.main()
