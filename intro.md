# 課程介紹｜從 GMT 到自己的地圖

[回課程首頁](README.md) · [開始 Colab 實作](https://colab.research.google.com/github/jimmy60504/pygmt-map-lab/blob/main/pygmt_workshop.ipynb)

先認識工具、看看作品，再打開 Notebook 動手畫圖。這份介紹可直接在 GitHub 閱讀。

## 先認識 GMT：用程式畫地圖

<img src="https://www.generic-mapping-tools.org/_static/gmt-logo.png" alt="GMT logo" width="360">

**GMT（Generic Mapping Tools）** 是一套地理資料處理與科學繪圖工具，可以畫海岸線、地形、地震分布、剖面與 3D 地形。

畫圖時，我們把幾個決定交給工具：**畫哪裡、用什麼資料、選什麼投影，以及如何用顏色與符號表達。** 保留程式後，就能換資料、改範圍、重新產生地圖。

今天的目標：從範例改出自己的地圖，知道各設定的意思，再用 AI 加快修改與延伸。

[GMT 官方網站](https://www.generic-mapping-tools.org/)

## 官方 Gallery：還可以畫什麼？

以下為 PyGMT 官方範例，點來源連結可查看圖片與完整程式。

### 3D 曲面：把網格數值立體呈現

<img src="https://www.pygmt.org/v0.17.0/_images/sphx_glr_grdview_surface_001.png" alt="grdview_surface" width="520">

這張使用數學函數產生的示範曲面，不是真實地形；同類繪圖方法也能呈現高程網格。

[來源：Plotting a surface](https://www.pygmt.org/v0.17.0/gallery/3d_plots/grdview_surface.html)

### 地震震源機制：用符號表達地震資訊

<img src="https://www.pygmt.org/v0.17.0/_images/sphx_glr_meca_001.png" alt="meca" width="520">

這些「沙灘球」符號用來表達震源機制，這堂課先欣賞，不需要學會解讀所有細節。

[來源：Focal mechanisms](https://www.pygmt.org/v0.17.0/gallery/seismology/meca.html)

### 分區設色：把統計資料放到地圖上

<img src="https://www.pygmt.org/v0.17.0/_images/sphx_glr_choropleth_map_001.png" alt="choropleth_map" width="520">

地圖也能呈現不同地區的統計數值，不只地形和地震。

[來源：Choropleth map](https://www.pygmt.org/v0.17.0/gallery/maps/choropleth_map.html)

圖像來源：PyGMT 官方 Gallery（Generic Mapping Tools 專案）；原始資料與製圖程式詳見各範例頁。

## 今天會做出的地圖

從台灣海岸線開始，加入地震點、彩色地形，再換成 3D 視角。同一份地形連續改變觀看角度，還能合成旋轉動畫。

**想一想：你想畫哪個地方？希望讀者看到什麼？**

後面的 Notebook 會一步步拆解，最後用 AI 協助延伸到世界其他區域。

## PyGMT：把 GMT 接進 Python 流程

<img src="https://raw.githubusercontent.com/GenericMappingTools/pygmt/main/doc/_static/pygmtlogo.png" alt="PyGMT logo" width="360">

PyGMT 讓我們用 **Python 呼叫 GMT**，將資料讀取、整理、分析和繪圖放在同一份 Notebook 裡，也方便使用變數與迴圈。

- **GMT**：提供地圖與科學繪圖能力。
- **PyGMT**：用 Python 操作 GMT，串接資料分析流程。
- **AI**：協助寫程式、修改與除錯；我們仍要檢查資料、範圍和圖例。

傳統 GMT 搭配 shell 也能寫變數與迴圈；PyGMT 的便利在於能接上 Python 生態系。

接下來先自己跑圖、改幾個參數，熟悉後再請 AI 延伸作品。

[PyGMT 官方文件](https://www.pygmt.org/v0.17.0/)

## 地震資料從哪裡來？

PyGMT 負責繪圖，地震資料需要從資料服務取得。本次使用的是**地震目錄**：一列代表一筆事件，不是連續的地震波形。

| 資料來源 | 這堂課怎麼使用？ |
| --- | --- |
| **USGS（美國地質調查所）** | 本次主要地震資料來源；查詢全球事件並下載 CSV，方便從台灣延伸到其他地區。 |
| **台灣 GDMS（中央氣象署臺灣地震與地球物理資料管理系統）** | 補充介紹的台灣資料管道，包含地震目錄、波形與測站等資料；本次不操作下載。 |

先認識五個欄位：**經度、緯度、發生時間、規模、深度**。查詢時選定範圍、期間與最低規模，畫圖時再決定如何呈現。

不同目錄可能有不同的收錄條件與規模類型，筆數不一定相同；使用前要看欄位說明、單位與時間標準。

[USGS 查詢與 CSV 說明](https://earthquake.usgs.gov/fdsnws/event/1/) · [台灣 GDMS](https://gdms.cwa.gov.tw/) · [GDMS 使用說明](https://gdms.cwa.gov.tw/help.php)

## 接著動手做

[開啟課程 Notebook](https://colab.research.google.com/github/jimmy60504/pygmt-map-lab/blob/main/pygmt_workshop.ipynb)，另存自己的副本，從「準備環境」開始。先親手改參數，再進入 AI 延伸練習。
