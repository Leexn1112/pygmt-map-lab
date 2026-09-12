# Colab 預打包環境（試用）

用途：預先解決套件版本與下載套件，學生只需取得一個 Linux 安裝包並解壓安裝。仍需下載與重啟 kernel；不保證比一般安裝快，必須在 Colab 比較。

## 規格

- Linux x86_64、Python 3.13，對應 CondaColab 0.1.13。
- PyGMT 0.17、GMT 6.5、Ghostscript 10.04，包含三份教材使用的 Python 套件。
- 不含地形或地震資料，第一次作圖仍需下載。
- `construct.yaml` 定義需求；每次建置附上完整 `environment-linux-64.lock.txt` 與安裝包 SHA256。需求不是全部依賴的固定鎖版，重建時應重新驗證。

## 建置與測試

手動執行 GitHub Actions 的 **Build Colab environment** 工作流程。流程使用 Linux runner 建立 constructor 安裝包，安裝到隔離目錄，測試套件載入、GMT、Ghostscript、陰影、等高線與剖面投影，再上傳 artifact（保留 14 天）。

教材 repo 已經授課者授權改成公開。通過測試的安裝包會放在固定版本 GitHub Release；Notebook 使用該版本 URL 與 SHA256，不追蹤不固定的 latest 下載。

## Notebook 預設安裝與備案

第一格先用子程序檢查套件、GMT 版本與 Ghostscript 是否可用；已備妥就跳過。否则優先下載預打包版，校驗 SHA256 後透過 CondaColab 安裝並重啟。

- URL 無法下載時，自動改回原本的 `condacolab.install()`，重啟後由第二格執行 `mamba install`。
- 想直接比較原版，先將第一格的 `USE_PREBUILT = False`，再從全新的 runtime 執行。
- 校驗失敗或安裝失敗會停止，不會在可能損壞的環境裡自動覆寫重裝。
- 已有 Conda 但套件不齊全時，不再重裝 Conda；下一格補齊套件。
- 不同 Colab Python 版本不使用此預打包包；原版 CondaColab 也有 Python 相容性限制，若提示不支援，需更換相容 runtime 或更新安裝工具，不能保證所有版本皆可直接回退。

`setup_first.py` 是第一格來源；修改 URL／SHA256 後，執行 `python scripts/sync_colab_setup.py` 同步三份教材。`python packaging/colab/test_setup.py` 可離線檢查跳過、下載失敗回退、手動原版、已裝 Conda 與 SHA256 失敗等分支，不會真的安裝。

## 手動上傳試用（備用）

1. 從成功的 Actions run 下載並解壓 artifact。
2. 開啟 **全新 Python 3.13 runtime**，先不要執行教材原本的安裝 cell。
3. 用 Colab 左側「檔案」上傳安裝包 `.sh`、`SHA256SUMS`，以及本目錄最新的 `install_colab.py`，放在 `/content/`。
4. 執行 `%run /content/install_colab.py`。驗證 SHA256 後會安裝，並重啟 kernel。
5. 重新連線後執行教材的環境檢查；正常時兩格都應顯示「環境已可用，跳過安裝」。再測試出圖。

若已跑過原本 Conda 安裝，請用新的 runtime 試用，不要覆寫目前環境。不要把 API 金鑰或 GitHub token 寫進共用 Notebook。

比較速度時要把「上傳／下載安裝包＋安裝＋重啟」一起計時，不能只比較解壓時間。Linux 出圖測試不等於 Colab 重啟與互動相容性測試；正式課堂使用前仍需在 Colab 完整跑一次。

參考：[CondaColab 自訂安裝包](https://github.com/conda-incubator/condacolab/tree/0.1.x#how-can-i-cache-my-installation-i-dont-want-to-wait-every-time-i-start-colab)。
