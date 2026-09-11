# PyGMT Map Lab｜地圖實作教室

從一張台灣地圖開始，探索地震、山脈與海底地形，再把視角轉向世界。

這堂課使用 PyGMT，帶你從現成範例修改出自己的地圖。先認識繪圖的基本設定，再嘗試用 AI 協助修改與除錯，將想法做成作品。

## 開始上課

**[先看課程介紹與 Gallery →](intro.md)**

**[開啟 Colab 課程 Notebook →](https://colab.research.google.com/github/jimmy60504/pygmt-map-lab/blob/main/pygmt_workshop.ipynb)**

先在 GitHub 閱讀 GMT、PyGMT 與資料來源介紹，再到 Colab 跟著範例程式與練習操作。

1. 登入 Google 帳號，開啟上方連結。
2. 將 Notebook 另存副本，作為自己的練習檔。
3. 依照「準備環境」的說明執行安裝，再開始畫圖。

目前教材庫為私人，透過 Colab 開啟時需授權有存取權限的 GitHub 帳號；若無法開啟，請向授課者取得教材或存取權限。

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

作業只需滿足兩個條件：

1. **作品與 PyGMT 有關。**
2. **將作品上傳 GitHub，繳交 repository 連結**，並確認教師能開啟。

題材、區域、呈現形式與圖的張數都可自由發揮，也可以使用 AI 完成。不限定沿用課堂範例；隔週繳交即可。

## 想再多探索？

- [PyGMT Gallery](https://www.pygmt.org/v0.17.0/gallery/index.html)：從範例找靈感。
- [PyGMT 文件](https://www.pygmt.org/v0.17.0/)：查閱函式與參數。
- [GMT 官方網站](https://www.generic-mapping-tools.org/)：認識背後的繪圖工具。

授課者使用的環境設定與測試紀錄，另見 [教材維護說明](docs/maintenance.md)。
