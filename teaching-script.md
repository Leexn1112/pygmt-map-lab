# 北市大 PyGMT 教案草稿

先整理要講的主題與練習，三節課的時間分配之後再安排。

## 課程設定

- 電腦教室上課，學生一開始拿到準備好的 Colab Notebook。
- 第一階段不使用 AI，先認識基本指令；第二階段再用 AI 協助繪圖。
- 前一堂課會安裝 Codex，Colab Gemini 作為備案。
- 教師先以台灣示範，學生再延伸至世界或自選區域。
- 作業隔週繳交，提交 GitHub repository 網址。

## 1. 開場與 Colab 操作

先展示海岸線與地震分布、彩色地形、3D 地形三種成果，說明今天會從現成程式開始，逐步修改成自己的地圖。

- 開啟 Notebook、另存副本，認識儲存格與執行順序。
- 執行環境準備與第一張台灣地圖。
- 簡單說明：重新啟動執行環境後，可能需要重跑前面的準備步驟。

## 2. 海岸線與基本地圖

從台灣地圖認識範圍、投影與圖層，了解程式中的設定如何影響畫面。

- 主要指令：`Figure()`、`basemap()`、`coast()`、`show()`。
- 重點參數：`region` 決定經緯度範圍，`projection` 決定投影與圖件尺寸。
- 練習：改陸海顏色、調整範圍，觀察結果。

## 3. 在地圖上顯示地震

先看地震資料表，再把事件位置畫成點。資料取得與讀表使用一般 Python 工具，繪圖使用 PyGMT，暫不使用 ObsPy。

- 認識經度、緯度、時間、規模與深度。
- 示範如何取得資料；暫以 USGS CSV 為候選來源。
- 用 `plot()` 加入地震點，再以大小表示規模、顏色表示深度，搭配圖例與色階。
- 練習：調整時間或規模條件，觀察分布變化。

## 4. 彩色地形圖

介紹地形網格，用顏色表達高低，再加上陰影與海岸線。

- 使用 `load_earth_relief()` 取得資料、`grdimage()` 繪圖。
- 說明解析度、色階與陰影的用途；全球圖先用較粗資料，區域圖再細化。
- 練習：更換色階或切換陰影，辨認台灣山脈與海底地形。

## 5. 3D 地形與旋轉視角

使用同一份地形資料，改成從斜角觀看，理解視角與垂直尺度如何影響地形外觀。

- 用 `grdview()` 畫 3D 地形，調整方位角與仰角。
- 練習：比較兩個不同視角，找出較容易辨認地形的方向。
- 旋轉動畫列為延伸：連續改變角度並輸出影格，是否實作再決定。

## 6. AI 輔助與世界地圖練習

以 Codex 為主、Colab Gemini 為備案，示範如何提供現有程式、提出修改需求，再執行並檢查結果。

- 示範需求：加標題、修改地震符號、更換區域或協助除錯。
- 學生選擇世界其他區域或全球範圍，延伸自己的作品；同步調整投影與資料解析度。
- 檢查資料來源、地圖範圍、單位和圖例，並能說明 AI 改了什麼。

## 7. 作業與繳交

這次作業就用 AI 做！想想你想呈現什麼，讓 AI 幫你把點子做出來。還沒靈感的話，先逛逛 [PyGMT Gallery](https://www.pygmt.org/v0.17.0/gallery/index.html)，找喜歡的範例，再試著改造或組合。

作業隔週繳交，只要滿足兩個條件：作品與 PyGMT 有關，以及將作品上傳 GitHub、繳交教師可開啟的 repository 連結。

其餘自由發揮，題材、區域、形式與圖的張數不限。


### 資料也可以換，找找新的靈感

地震資料不只有 USGS；先想清楚要的是「地震發生在哪裡」的目錄，還是「測站記錄到怎麼搖」的波形。

| 想找什麼 | 資料入口 | 可以做什麼 |
| --- | --- | --- |
| 台灣更細的地震資料 | [氣象署 GDMS](https://gdms.cwa.gov.tw/) | 查找台灣地震目錄與波形；想研究小地震或局部構造，可以從這裡找起，下載方式與權限依網站說明。 |
| 全球地震目錄 | [USGS](https://earthquake.usgs.gov/fdsnws/event/1/)／[ISC Bulletin](https://www.isc.ac.uk/iscbulletin/search/) | 取得時間、位置、深度與規模，畫分布圖或剖面；各目錄的收錄範圍與更新速度不同。 |
| 全球測站的地震波形 | [EarthScope（原 IRIS 服務）](https://service.earthscope.org/fdsnws/dataselect/1/) | 按測站、通道與時間下載波形，試做「震央與測站地圖＋波形」；不是每個測站都有所有時段的資料。 |

波形不是地震目錄，不能直接套進本課的地震點位程式。可以請 AI 協助讀取、處理，再用 PyGMT 呈現；例如畫出同一場地震在不同測站的記錄。以上只是靈感，不是額外作業要求。

## 課前待準備

- 測試完整 Colab 與 AI 使用流程。
- 補上原範例尚缺的地震資料、3D 地形與 GitHub 繳交示範。
- 確認地震資料期間、準備備份檔，決定旋轉動畫的教學深度。

## 參考資料

- [原始 Notebook](https://github.com/oceanicdayi/plot_plate_boundary_pygmt/blob/main/pygmt_plot_plate_boundary.ipynb)
- [範例重點筆記](kb/pygmt-colab-example.md)
- [USGS 地震目錄](https://earthquake.usgs.gov/fdsnws/event/1/)
- [PyGMT 地形資料](https://www.pygmt.org/latest/api/generated/pygmt.datasets.load_earth_relief.html)
- [PyGMT 3D 地形](https://www.pygmt.org/latest/api/generated/pygmt.Figure.grdview.html)
