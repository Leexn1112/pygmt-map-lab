# PyGMT Colab 範例程式重點

## 來源

- Notebook：[plot_plate_boundary_pygmt](https://github.com/oceanicdayi/plot_plate_boundary_pygmt/blob/main/pygmt_plot_plate_boundary.ipynb)
- 可直接透過 Notebook 上方的 **Open in Colab** 按鈕開啟

## 範例內容概覽

這份 Notebook 目前涵蓋：

1. 在 Google Colab 安裝 Conda 環境與 PyGMT
2. 顯示 PyGMT、GMT 與相關套件版本
3. 繪製全球地形與熱點分布
4. 繪製台灣海岸線地圖
5. 繪製台灣彩色地形圖

## Colab 環境設定

- 先安裝 `condacolab`，再安裝指定的 Miniforge
- 安裝過程會自動重新啟動 Colab kernel
- kernel 重啟後，以 `mamba install pygmt` 安裝 PyGMT
- 使用 `pygmt.show_versions()` 確認 PyGMT、GMT 與相依套件是否安裝成功
- Notebook 另有安裝 ObsPy，但目前繪圖程式沒有使用到；本課程可先移除這一步

> Notebook 記錄的是 PyGMT 0.17 與當時的 Colab 安裝方式。Colab 環境可能改變，正式上課前需要重新測試整份 Notebook。

## 主要 PyGMT 指令

- `pygmt.Figure()`：建立圖件
- `fig.basemap()`：設定繪圖範圍、投影與座標框
- `fig.coast()`：繪製海岸線、陸地與海洋
- `load_earth_relief()`：下載指定範圍與解析度的全球地形資料
- `fig.grdimage()`：將網格地形資料畫成彩色影像
- `fig.plot()`：加入點位資料；範例用來繪製 GMT 內建的火山熱點資料
- `fig.colorbar()`：加入色階
- `fig.show()`：顯示圖件

## 範例中的重要參數

- 全球範圍：`region="g"`
- 台灣範圍：`region="119/123/21/26"`
- 台灣區域投影：`projection="M15c"`
- 全球方位投影：`projection="G330/-30/12c"`
- 全球地形解析度：`resolution="01d"`
- 台灣地形解析度：`resolution="05m"`
- 地形色階：`cmap="geo"`
- 地形陰影：`shading=True`

## 與課程教案的連結

這份 Notebook 可以作為學生一開始拿到的 Colab 基底，適合支援以下內容：

- 基本地圖與海岸線
- 從全球範圍切換至台灣範圍
- 彩色 topography 地形圖
- 認識圖層疊加：底圖、地形、海岸線、點位與色階

學生可先照著台灣範例操作，再修改 `region`、`projection` 與地形解析度，延伸成世界或自選區域的作品。

## 尚未涵蓋的內容

- 雖然 repository 名稱提到 plate boundary，目前 Notebook 並沒有實際繪製板塊邊界
- 沒有取得或繪製地震目錄資料
- 沒有 3D 地形圖或旋轉動畫
- 沒有 GitHub 作業繳交流程

以上內容需要在正式課程用的 Colab Notebook 中另外補上。
