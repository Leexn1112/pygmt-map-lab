"""Experimental loader: upload the installer and SHA256SUMS to /content first.

Run as a cell with %run /content/install_colab.py before importing PyGMT.
Requires Python 3.13 Colab; does not replace the normal notebook installer.
"""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys
import time

if importlib.util.find_spec('google.colab') is None:
    raise RuntimeError('此安裝器只供 Google Colab 使用。')
if sys.version_info[:2] != (3, 13):
    raise RuntimeError('此試用包只支援 Python 3.13；請使用教材原本的安裝方式。')

probe = 'import pygmt, pandas, PIL, ipywidgets, ipyleaflet, pyproj; from pygmt.clib import Session;\nwith Session() as s: assert s.info["version"].startswith("6.5.");\nassert pygmt.__version__.startswith("v0.17.")'
if subprocess.run([sys.executable, '-c', probe], capture_output=True).returncode == 0:
    print('環境已可用，跳過安裝。')
else:
    checksum_file = Path('/content/SHA256SUMS')
    expected, filename = checksum_file.read_text().strip().split(maxsplit=1)
    installer = Path('/content') / Path(filename.lstrip('*')).name
    digest = hashlib.file_digest(installer.open('rb'), 'sha256').hexdigest()
    if digest != expected:
        raise RuntimeError('安裝包 SHA256 不符，請重新下載。')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'condacolab==0.1.13'])
    import condacolab
    start = time.monotonic()
    # A prior standard Conda installation must not silently skip this package.
    condacolab.install_from_url(installer.as_uri(), sha256=expected, run_checks=False)
