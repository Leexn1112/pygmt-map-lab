# PyGMT Map Lab｜地圖實作教室

從一張台灣地圖開始，探索地震、山脈與海底地形，再把視角轉向世界。

這堂課使用 PyGMT，帶你從現成範例修改出自己的地圖。先認識繪圖的基本設定，再嘗試用 AI 協助修改與除錯，將想法做成作品。

## 開始上課

**[先看課程介紹與 Gallery →](intro.md)**

三份 Notebook 各自包含環境設置，可獨立開始：

- [01｜基本地圖與地震](https://colab.research.google.com/github/jimmy60504/pygmt-map-lab/blob/main/01_maps_earthquakes.ipynb)
- [02｜地形與 3D](https://colab.research.google.com/github/jimmy60504/pygmt-map-lab/blob/main/02_terrain_3d.ipynb)
- [03｜AI 探索與作業](https://colab.research.google.com/github/jimmy60504/pygmt-map-lab/blob/main/03_ai_exploration.ipynb)

先在 GitHub 閱讀 GMT、PyGMT 與資料來源介紹，再到 Colab 跟著範例程式與練習操作。

1. 登入 Google 帳號，開啟上方連結。
2. 將 Notebook 另存副本，作為自己的練習檔。
3. 依照「準備環境」的說明執行安裝，再開始畫圖。

教材庫已公開，可由上方連結開啟 Colab。執行與另存副本仍需登入 Google 帳號。

## 這堂課會做什麼？

- **認識 GMT 與 PyGMT**：看看科學地圖能有哪些表現方式。
- **畫出台灣海岸線**：修改範圍、投影與顏色，了解設定如何影響地圖。
- **把地震放上地圖**：取得 USGS 地震資料，以點位、大小和顏色呈現事件。
- **呈現彩色地形**：用高程資料看見山脈與海底起伏。
- **換個角度看 3D 地形**：先認識靜態視角，再於 AI 展示用拉桿旋轉地形。
- **用 AI 互動探索**：先用拉桿旋轉地形，再點選 A、B，使用 PyGMT 畫出地下地震剖面。

先親手修改幾個參數，再使用前一堂課準備的 Codex；Colab Gemini 作為備案。重點是能說明自己畫了什麼、用了哪些資料，以及修改帶來的變化。

## 資料從哪裡來？

地震實作主要使用 [USGS 地震目錄](https://earthquake.usgs.gov/fdsnws/event/1/)，並介紹 [台灣 GDMS](https://gdms.cwa.gov.tw/) 這個在地資料管道。地形則透過 PyGMT 取得 [GMT 全球地形資料](https://docs.generic-mapping-tools.org/latest/datasets/remote-data.html)。

Notebook 會在執行時下載資料並產生圖片，請保持網路連線。

## 隔週繳交作品

這次作業就用 AI 做！想想你想呈現什麼，讓 AI 幫你把點子做出來。還沒靈感的話，可以先逛逛 [PyGMT Gallery](https://www.pygmt.org/v0.17.0/gallery/index.html)，找喜歡的範例，再試著改造或組合。

作品請把**圖＋一小段圖說**放在一起：說明你想看什麼、如何呈現，以及實際觀察到什麼。不必創新或複雜，也不必得到符合原先猜想的結果；重點是讓人一眼抓到你想表達的事。可以搭配其他工具，不必只用 PyGMT。

作業只需滿足兩個條件：

1. **作品與 PyGMT 有關。**
2. **將作品上傳 GitHub，繳交 repository 連結**，並確認教師能開啟。

題材、區域、呈現形式與圖的張數都可自由發揮，不限定沿用課堂範例；隔週繳交即可。


### 先逛逛論文的圖，找找靈感

不用一開始就讀懂整篇 paper。先到 [Google Scholar](https://scholar.google.com/) 搜尋 `seismic`、`earthquake` 或 `seismicity`，也可以加上 `Taiwan`、`subduction`、`cross section`、`waveform` 等地區或圖像關鍵字。或先用 Google 圖片搜尋，看到有興趣的圖，再回到原論文看圖說。

也可以直接逛這些期刊，挑一篇題目有興趣的文章，先翻圖片：

| 期刊入口 | 主要範圍 | 逛圖時可以找什麼 |
| --- | --- | --- |
| [SRL — Seismological Research Letters](https://pubs.geoscienceworld.org/srl) | 地震學及相關觀測、方法與應用 | 地震事件、測站、波形與資料展示。 |
| [BSSA — Bulletin of the Seismological Society of America](https://pubs.geoscienceworld.org/bssa) | 地震學與相關研究 | 地震分布、震源、地動與分析結果。 |
| [GJI — Geophysical Journal International](https://academic.oup.com/gji) | 固體地球物理，不限地震 | 地下構造、剖面、波形與模型比較。 |
| [GRL — Geophysical Research Letters](https://agupubs.onlinelibrary.wiley.com/journal/19448007) | 地球與太空科學，不限地震 | 搜尋地震相關文章，看作者怎麼用少量圖呈現重點。 |
| [Seismica](https://seismica.library.mcgill.ca/) | 地震學與地震科學，開放取用 | 地震研究、資料與方法的各種呈現方式。 |

挑一張喜歡的圖就好，想想：**它想表達什麼？資料怎麼篩選或排列？我可以借用哪種畫法來表達自己的問題？** 重點是學呈現方式，不是照抄結論，也不必做出同樣複雜的研究。遇到付費文章，可找開放版本或換一篇。

把原論文連結與圖號留給自己，也可以給 AI 當討論參考。圖片搜尋只是入口，仍要回原文確認圖說；若要把原圖放進公開 GitHub，需確認授權並標明來源。

### 資料也可以換，找找新的靈感

地震資料不只有 USGS；先想清楚要的是「地震發生在哪裡」的目錄，還是「測站記錄到怎麼搖」的波形。

| 想找什麼 | 資料入口 | 可以做什麼 |
| --- | --- | --- |
| 台灣更細的地震資料 | [氣象署 GDMS](https://gdms.cwa.gov.tw/) | 查找台灣地震目錄與波形；想研究小地震或局部構造，可以從這裡找起，下載方式與權限依網站說明。 |
| 全球地震目錄 | [USGS](https://earthquake.usgs.gov/fdsnws/event/1/)／[ISC Bulletin](https://www.isc.ac.uk/iscbulletin/search/) | 取得時間、位置、深度與規模，畫分布圖或剖面；各目錄的收錄範圍與更新速度不同。 |
| 全球測站的地震波形 | [EarthScope（原 IRIS 服務）](https://service.earthscope.org/fdsnws/dataselect/1/) | 按測站、通道與時間下載波形，試做「震央與測站地圖＋波形」；不是每個測站都有所有時段的資料。 |

波形不是地震目錄，不能直接套進本課的地震點位程式。可以請 AI 協助讀取、處理，再用 PyGMT 呈現；例如畫出同一場地震在不同測站的記錄。以上只是靈感，不是額外作業要求。

### 不只地震：把不同資料放在一起看

也可以加入地形、雨量、人口或土地覆蓋，探索一個簡單的小問題。以下是資料入口與發想，不是指定題目：

| 範圍 | 資料入口 | 可以想想的問題 |
| --- | --- | --- |
| 台灣 | [20 公尺數值地形模型](https://data.gov.tw/dataset/35430) | 換成較細的地形，能看出哪些山谷、盆地或地形邊界？ |
| 台灣 | [氣象署開放資料](https://opendata.cwa.gov.tw/index)：雨量與氣象觀測 | 同一場降雨，山區和平地的分布有何不同？ |
| 全球 | [GEBCO 海陸地形](https://www.gebco.net/data-products/gridded-bathymetry-data) | 海溝的位置與不同深度的地震如何對應？ |
| 全球 | [Global CMT 震源機制目錄](https://www.globalcmt.org/CMTfiles.html) | 不同區域的地震，斷層運動型態是否不同？ |
| 全球 | [WorldPop 人口網格](https://www.worldpop.org/) | 地震周邊的人口集中在哪裡？空間分布不等於災害風險。 |
| 全球 | [Copernicus 土地覆蓋](https://land.copernicus.eu/en/products/global-dynamic-land-cover/land-cover-2020-raster-10-m-global-annual) | 山地與平原的森林、農地、建成區分布有何差異？ |
| 全球 | [Natural Earth 基礎圖資](https://www.naturalearthdata.com/downloads/) | 加上國界、城市與河流，能否讓研究區域更容易理解？適合區域或全球圖，不是精細街道圖。 |

可以從「地震＋海底地形」、「地震＋震源機制」或「地形＋雨量」選一個方向。先選小區域、少量資料，把一個問題講清楚即可；不必把所有資料都放上圖。

下載前請 AI 一起檢查年份、座標系統、解析度、單位與授權；部分服務可能需要註冊或 API 金鑰。公開資料不代表格式能直接混用，資料疊在一起也不代表已證明因果關係。作品仍需用到 PyGMT，但可以搭配其他工具處理與呈現。

## 想再多探索？

- [PyGMT Gallery](https://www.pygmt.org/v0.17.0/gallery/index.html)：從範例找靈感。
- [PyGMT 文件](https://www.pygmt.org/v0.17.0/)：查閱函式與參數。
- [GMT 官方網站](https://www.generic-mapping-tools.org/)：認識背後的繪圖工具。

授課者使用的環境設定與測試紀錄，另見 [教材維護說明](docs/maintenance.md)。
