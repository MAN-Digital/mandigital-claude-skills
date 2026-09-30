import importlib.util
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('cms_token', Path(__file__).parents[1] / 'cms-token.py')
cms = importlib.util.module_from_spec(spec)
spec.loader.exec_module(cms)


class CredentialTests(unittest.TestCase):
    def test_wrong_portal_and_missing_scope_rejected(self):
        for metadata in [{'hubId': 2, 'scopes': ['content']}, {'hubId': 1, 'scopes': []}]:
            with patch.object(cms, 'request', return_value=metadata):
                with self.assertRaises(cms.SafeError):
                    cms.verify('fake-token', 1)

    def test_valid_portal_and_scope(self):
        with patch.object(cms, 'request', return_value={'hubId': 1, 'scopes': ['content']}):
            self.assertEqual(cms.verify('fake-token', 1)['hubId'], 1)

    def test_private_storage_and_roundtrip(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(cms.Path, 'home', return_value=Path(directory)):
            target = cms.save_token('fake-token', 1)
            self.assertEqual(target.stat().st_mode & 0o777, 0o600)
            self.assertEqual(target.parent.stat().st_mode & 0o777, 0o700)
            self.assertEqual(cms.load_token(1), 'fake-token')
            target.chmod(0o644)
            with self.assertRaises(cms.SafeError):
                cms.load_token(1)

    def test_symlink_file_rejected(self):
        with tempfile.TemporaryDirectory() as directory, patch.object(cms.Path, 'home', return_value=Path(directory)):
            target = cms.save_token('fake-token', 1)
            target.unlink()
            target.symlink_to(Path(directory) / 'other')
            with self.assertRaises(cms.SafeError):
                cms.save_token('replacement', 1)

    def test_invalid_portal_rejected(self):
        with self.assertRaises(cms.SafeError):
            cms.credential_path(-1)

    def test_redirect_never_forwards_secret(self):
        with self.assertRaises(cms.SafeError):
            cms.NoRedirect().redirect_request(None, None, 302, '', {}, 'https://example.com')

    def test_noninteractive_setup_rejected(self):
        with patch.object(cms.sys, 'argv', ['cms-token.py', 'setup', '--portal-id', '1']), patch.object(cms.sys.stdin, 'isatty', return_value=False), patch.object(cms, 'save_token') as save:
            with self.assertRaises(cms.SafeError):
                cms.main()
            save.assert_not_called()


if __name__ == '__main__':
    unittest.main()
