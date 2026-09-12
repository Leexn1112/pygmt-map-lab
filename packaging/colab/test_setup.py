"""Offline branch tests; these do not install packages or restart a kernel."""
import contextlib
import hashlib
import io
from pathlib import Path
import subprocess
import sys
import tempfile
import types
import unittest
from unittest.mock import patch
from urllib.error import URLError

SOURCE = Path(__file__).with_name('setup_first.py').read_text()

class SetupTests(unittest.TestCase):
    def run_case(self, ready=False, available=False, force_original=False, conda_ready=False, bad_hash=False):
        calls = []
        fake = types.ModuleType('condacolab')
        def check():
            if not conda_ready:
                raise AssertionError('not installed')
        fake.check = check
        fake.install = lambda: calls.append('original')
        fake.install_from_url = lambda *a, **k: calls.append('prebuilt')
        payload = b'test installer, never executed'
        digest = hashlib.sha256(payload).hexdigest()
        source = SOURCE.replace('PREBUILT_URL = ""', 'PREBUILT_URL = "https://example.invalid/test.sh"')
        source = source.replace('PREBUILT_SHA256 = ""', f'PREBUILT_SHA256 = "{"0"*64 if bad_hash else digest}"')
        if force_original:
            source = source.replace('USE_PREBUILT = True', 'USE_PREBUILT = False')
        with tempfile.TemporaryDirectory() as folder, contextlib.ExitStack() as stack:
            stack.enter_context(patch.dict(sys.modules, {'condacolab': fake}))
            stack.enter_context(patch('sys.version_info', (3,13,0)))
            stack.enter_context(patch('importlib.util.find_spec', return_value=object()))
            stack.enter_context(patch('subprocess.run', return_value=subprocess.CompletedProcess([], 0 if ready else 1)))
            stack.enter_context(patch('subprocess.check_call', side_effect=lambda *a, **k: calls.append('pip')))
            stack.enter_context(patch('tempfile.mkdtemp', return_value=folder))
            stack.enter_context(patch('urllib.request.urlopen', side_effect=(lambda *a, **k: io.BytesIO(payload)) if available else URLError('404')))
            stack.enter_context(contextlib.redirect_stdout(io.StringIO()))
            exec(compile(source, 'setup_first.py', 'exec'), {})
        return calls

    def test_ready_skips_all_installs(self):
        self.assertEqual(self.run_case(ready=True), [])
    def test_download_failure_falls_back(self):
        self.assertEqual(self.run_case(), ['pip','original'])
    def test_verified_package_installs(self):
        self.assertEqual(self.run_case(available=True), ['pip','prebuilt'])
    def test_manual_original(self):
        self.assertEqual(self.run_case(available=True, force_original=True), ['pip','original'])
    def test_existing_conda_not_overwritten(self):
        self.assertEqual(self.run_case(conda_ready=True), ['pip'])
    def test_checksum_failure_stops(self):
        with self.assertRaises(RuntimeError):
            self.run_case(available=True, bad_hash=True)

if __name__ == '__main__':
    unittest.main()
