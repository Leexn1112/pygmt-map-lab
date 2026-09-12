"""Experimental loader: upload the installer and SHA256SUMS to /content first.

Run as a cell with %run /content/install_colab.py before importing PyGMT.
Requires Python 3.13 Colab; does not replace the normal notebook installer.
"""
import hashlib
import importlib.util
from pathlib import Path
import subprocess
import sys

if importlib.util.find_spec('google.colab') is None:
    raise RuntimeError('此安裝器只供 Google Colab 使用。')
if sys.version_info[:2] != (3, 13):
    raise RuntimeError('此試用包只支援 Python 3.13；請使用教材原本的安裝方式。')

probe = 'import pygmt, pandas, PIL, ipywidgets, ipyleaflet, pyproj, shutil; from pygmt.clib import Session;\nwith Session() as s: assert s.info["version"].startswith("6.5.");\nassert pygmt.__version__.lstrip("v").startswith("0.17."); assert shutil.which("gs")'
if subprocess.run([sys.executable, '-c', probe], capture_output=True, timeout=30).returncode == 0:
    print('環境已可用，跳過安裝。')
else:
    checksum_file = Path('/content/SHA256SUMS')
    expected, filename = checksum_file.read_text().strip().split(maxsplit=1)
    installer = Path('/content') / Path(filename.lstrip('*')).name
    with installer.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    if digest != expected:
        raise RuntimeError('安裝包 SHA256 不符，請重新下載。')
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-q', 'condacolab==0.1.13'])
    import condacolab
    try:
        condacolab.check()
    except AssertionError:
        condacolab.install_from_url(installer.as_uri(), sha256=expected)
    else:
        raise RuntimeError('已安裝其他 Conda 環境；請換全新 runtime 再試預打包版，避免覆寫目前環境。')
