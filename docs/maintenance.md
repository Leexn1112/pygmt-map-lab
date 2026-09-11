# 教材維護說明

本頁供授課者維護與測試教材使用，學生請從 [課程入口](../README.md) 開始。

## 實跑結果

2026-09-09 在本機 macOS ARM64 的獨立 Conda 環境執行，Python 3.12、PyGMT 0.17.0、GMT 6.5.0、Ghostscript 10.04.0。完整 Notebook（含動畫）執行成功，沒有錯誤輸出。

- 真實地震資料：USGS，UTC 2024-04-01 至 2024-05-01，119–123°E、21–26°N、M ≥ 4，共 302 筆有效事件。目錄後續修訂可能造成筆數變化。
- 台灣地形：GMT earth relief，2 角分，151 × 121 網格；使用較粗資料以加快課堂操作。
- 全球地形：1 度網格。
- 3D：固定視角圖，以及每 30 度一格、共 12 格的旋轉 GIF；垂直尺度有誇大。

已檢查主要成果的海岸線、點位、圖例、色階與座標標籤。**Colab 雲端安裝尚未實測**；本機成功不代表所有 Colab 帳號與環境均可直接安裝，正式上課前需再驗證。

## 本機重跑

```sh
conda env create -f environment.yml
conda activate pygmt-workshop
python scripts/run_notebook.py
```

執行器以全新 kernel 跑操作版，開啟選做動畫，輸出至 `pygmt_workshop_executed.ipynb`。會更新同名圖片與下載資料，不修改操作版。此次本機環境位於 `.conda-env/`，已由 `.gitignore` 排除。

其他維護工具（在專案根目錄執行）：

- `python scripts/clear_notebook_images.py`：清除兩份 Notebook 的嵌入圖片與圖片輸出；重跑教材後、上傳 Colab 前可使用。

課前介紹與 Gallery 在根目錄 `intro.md` 維護；Notebook 保留實作說明與程式。

資料與工具來源：[USGS 地震目錄](https://earthquake.usgs.gov/fdsnws/event/1/)、[GMT 地形](https://docs.generic-mapping-tools.org/latest/datasets/remote-data.html)、[PyGMT 安裝](https://www.pygmt.org/v0.17.0/install.html)、[CondaColab](https://github.com/conda-incubator/condacolab/tree/0.1.x)。

## 檔案與產物

- `intro.md`：GitHub 上的課前介紹與 Gallery，圖片引用官方網址。
- `pygmt_workshop.ipynb`：課程實作主檔，維護操作說明與程式。
- `pygmt_workshop_executed.ipynb`：本機執行紀錄；已移除圖片輸出。
- `scripts/`：執行與清除圖片的維護工具。
- 根目錄的 `01_`–`05_` 成果 PNG、`outputs/`（選做動畫）、`data/`：執行時產生，不納入 Git。

GitHub 為教材主版本；更新後需從課程連結重新開啟，已另存的學生副本不會自動更新。
