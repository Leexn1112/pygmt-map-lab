# PyGMT Map Lab｜地圖實作教室

從台灣海岸線、地震分布到 3D 地形，使用 PyGMT 與 AI 探索科學繪圖。

[在 Colab 開啟操作版](https://colab.research.google.com/github/jimmy60504/pygmt-map-lab/blob/main/pygmt_workshop.ipynb)

GitHub 為主版本；更新後從上方連結重新開啟。私人 repository 需在 Colab 授權有權限的 GitHub 帳號，並非公開教材連結。

- `pygmt_workshop.ipynb`：學生操作版，簡短中文說明、可執行程式與修改練習。
- `pygmt_workshop_executed.ipynb`：實際執行版，保留文字結果與資料預覽；為避免 Colab 顯示問題，已清除嵌入圖片與動畫。
- `outputs/`：5 張主要成果圖、12 個旋轉影格及 GIF。
- `data/`：USGS 原始 CSV 與對應查詢條件。
- `scripts/`：教材維護工具，學生上課不需要執行。

## 使用方式

從上方連結開啟操作版，或在 Google Colab 選擇「上傳 Notebook」。先執行第一個安裝儲存格，等待 kernel 重啟，再執行第二個安裝儲存格及後續內容。首次下載地形需要網路。若要使用地震備份，把提供的 `data/` 資料夾上傳至 Colab 工作目錄。兩份 Notebook 均不嵌入圖片；執行程式時會重新產生圖。

依序完成：台灣海岸線 → 地震分布 → 彩色地形 → 3D 視角 → AI 與全球練習 → 隔週 GitHub 繳交。旋轉 GIF 是選做，操作版預設不執行；執行版已開啟並測試。

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
- `python scripts/make_preview.py`：將 `outputs/` 的五張成果圖整理成預覽圖。

介紹文字直接在 Notebook 維護。

資料與工具來源：[USGS 地震目錄](https://earthquake.usgs.gov/fdsnws/event/1/)、[GMT 地形](https://docs.generic-mapping-tools.org/latest/datasets/remote-data.html)、[PyGMT 安裝](https://www.pygmt.org/v0.17.0/install.html)、[CondaColab](https://github.com/conda-incubator/condacolab/tree/0.1.x)。
