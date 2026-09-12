"""Source for the first installation cell in all course notebooks."""
import importlib.util
import subprocess
import sys
import hashlib
from pathlib import Path
import tempfile
import shutil
from urllib.error import URLError
from urllib.request import urlopen

# 改成 False 就使用原本的 Conda／mamba 安裝方式。
USE_PREBUILT = True
PREBUILT_URL = ""  # 建置通過後填入固定版本下載網址
PREBUILT_SHA256 = ""

# 在子程序檢查，避免安裝前先載入 kernel 的動態函式庫。
check_code = """
import pygmt, pandas, PIL, ipywidgets, ipyleaflet, pyproj, shutil
from pygmt.clib import Session
assert pygmt.__version__.lstrip('v').startswith('0.17.')
assert shutil.which('gs')
with Session() as session:
    assert session.info['version'].startswith('6.5.')
"""
try:
    ENV_READY = subprocess.run(
        [sys.executable, "-c", check_code], capture_output=True, timeout=30
    ).returncode == 0
except subprocess.TimeoutExpired:
    ENV_READY = False

IN_COLAB = importlib.util.find_spec("google.colab") is not None if importlib.util.find_spec("google") else False
if ENV_READY:
    print("環境已可用，跳過安裝。")
elif IN_COLAB:
    subprocess.check_call([sys.executable, "-m", "pip", "install", "-q", "condacolab==0.1.13"])
    import condacolab
    try:
        condacolab.check()
        CONDA_READY = True
    except AssertionError:
        CONDA_READY = False

    if CONDA_READY:
        print("Conda 已安裝，請執行下一格補齊套件。")
    else:
        installer = None
        if USE_PREBUILT and PREBUILT_URL and sys.version_info[:2] == (3, 13):
            installer = Path(tempfile.mkdtemp(prefix="pygmt-installer-")) / "installer.sh"
            print("下載預打包環境……")
            try:
                with urlopen(PREBUILT_URL, timeout=60) as response, installer.open("wb") as stream:
                    shutil.copyfileobj(response, stream)
            except (URLError, OSError) as error:
                print(f"預打包版無法下載，改用原本安裝方式：{type(error).__name__}")
                installer = None
            if installer is not None:
                with installer.open("rb") as stream:
                    digest = hashlib.file_digest(stream, "sha256").hexdigest()
                if not PREBUILT_SHA256 or digest != PREBUILT_SHA256:
                    raise RuntimeError("安裝包校驗失敗，已停止。請重新下載或手動設 USE_PREBUILT=False。")
        elif USE_PREBUILT:
            print("預打包版未提供或 Python 版本不符，改用原本安裝方式。")

        if installer is not None:
            # 安裝錯誤不自動重裝：避免在部分安裝的環境上繼續覆寫。
            condacolab.install_from_url(installer.as_uri(), sha256=PREBUILT_SHA256)
        else:
            # 備案：先安裝 Conda，重啟後在下一格用 mamba 安裝套件。
            condacolab.install()
else:
    print("本機模式：使用目前 Python 環境。")
