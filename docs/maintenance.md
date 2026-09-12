# 教材維護說明

本頁供授課者維護與測試教材使用，學生請從 [課程入口](../README.md) 開始。

## 三份教材拆分檢查（2026-09-12）

- 三份均通過 Notebook 格式、Python 語法與獨立環境設置檢查，教材不保留輸出圖片。
- 地形篇在全新 kernel 實跑 GMT 地形下載、陰影、等高線、靜態 3D 與拉桿初始畫面。
- 基本地圖篇與 AI 篇各自以全新 kernel、測試地震目錄跑通，AI 篇另模擬 A–B 座標產生地圖與剖面。這次未重新驗證 USGS 即時下載或 Colab 滑鼠互動。

## 早期版本實跑紀錄（不代表目前三份已完整重跑）

2026-09-09 在本機 macOS ARM64 的獨立 Conda 環境執行，Python 3.12、PyGMT 0.17.0、GMT 6.5.0、Ghostscript 10.04.0。完整 Notebook（含動畫）執行成功，沒有錯誤輸出。

- 真實地震資料：USGS，UTC 2024-04-01 至 2024-05-01，119–123°E、21–26°N、M ≥ 4，共 302 筆有效事件。目錄後續修訂可能造成筆數變化。
- 台灣地形：GMT earth relief，2 角分，151 × 121 網格；使用較粗資料以加快課堂操作。
- 全球地形：1 度網格。
- 3D：固定視角圖，以及每 30 度一格、共 12 格的旋轉 GIF；垂直尺度有誇大。

已檢查主要成果的海岸線、點位、圖例、色階與座標標籤。授課者已確認 Colab 可以運作。

## 本機重跑

Colab 使用 Conda／mamba 安裝。三份環境格會先檢查，套件已可用時跳過安裝。

各份只明列自己的套件；相依套件由 mamba 自動安裝：

- 基本地圖與地震：PyGMT、GMT、Ghostscript、Pandas。
- 地形與 3D：PyGMT、GMT、Ghostscript、ipywidgets。
- AI 探索：PyGMT、GMT、Ghostscript、Pandas、NumPy、ipywidgets、ipyleaflet、pyproj。

環境可用性檢查也依各份需求執行，不會因其他篇章的套件未安裝而重跑安裝。此調整未在 Colab 重新計時；PyGMT／GMT 自身的相依套件仍會下載。

```sh
conda env create -f environment.yml
conda activate pygmt-workshop
python scripts/run_notebook.py
```

執行器依序以各自全新的 kernel 跑三份 Notebook，結果只保留在記憶體，不修改教材、不新增執行版。也可指定單份，例如 `python scripts/run_notebook.py 02_terrain_3d.ipynb`。旋轉拉桿僅執行初始畫面；A–B 點選需另外互動測試。本機環境 `.conda-env/` 已由 `.gitignore` 排除。

其他維護工具（在專案根目錄執行）：

- `python scripts/clear_notebook_images.py`：清除三份 Notebook 的嵌入圖片與圖片輸出；重跑教材後、上傳 Colab 前可使用。

課前介紹與 Gallery 在根目錄 `intro.md` 維護；Notebook 保留實作說明與程式。

資料與工具來源：[USGS 地震目錄](https://earthquake.usgs.gov/fdsnws/event/1/)、[GMT 地形](https://docs.generic-mapping-tools.org/latest/datasets/remote-data.html)、[PyGMT 安裝](https://www.pygmt.org/v0.17.0/install.html)、[CondaColab](https://github.com/conda-incubator/condacolab/tree/0.1.x)。

## 檔案與產物

- `intro.md`：GitHub 上的課前介紹與 Gallery，圖片引用官方網址。
- `01_maps_earthquakes.ipynb`：基本地圖與地震。
- `02_terrain_3d.ipynb`：地形、陰影、等高線、3D 與 AI 拉桿前導。
- `03_ai_exploration.ipynb`：AI 引導、資料靈感、A–B 剖面與作業。
- 三份都包含環境設置與快捷鍵；不共用執行狀態。舊整份與 executed 副本已移除，可由 Git 歷史還原。
- `scripts/`：執行與清除圖片的維護工具。
- 圖片直接顯示在 Notebook，不另存 PNG；旋轉地形使用拉桿，不再產生 GIF。地震資料直接由 USGS 查詢網址讀取，不再建立本機快取或查詢 JSON。

GitHub 為教材主版本；更新後需從課程連結重新開啟，已另存的學生副本不會自動更新。
