"""Insert concise teaching introductions and self-contained gallery attachments."""
import base64
from pathlib import Path
import nbformat
import requests

ROOT = Path(__file__).resolve().parent

ASSETS = ROOT / 'assets' / 'intro'
ASSETS.mkdir(parents=True, exist_ok=True)
asset_urls = {
    'gmt-logo.png': 'https://www.generic-mapping-tools.org/_static/gmt-logo.png',
    'pygmt-logo.png': 'https://raw.githubusercontent.com/GenericMappingTools/pygmt/main/doc/_static/pygmtlogo.png',
    'surface.png': 'https://www.pygmt.org/v0.17.0/_images/sphx_glr_grdview_surface_001.png',
    'meca.png': 'https://www.pygmt.org/v0.17.0/_images/sphx_glr_meca_001.png',
    'choropleth.png': 'https://www.pygmt.org/v0.17.0/_images/sphx_glr_choropleth_map_001.png',
}
for name, url in asset_urls.items():
    if not (ASSETS / name).exists():
        response = requests.get(url, timeout=60)
        response.raise_for_status()
        assert response.content.startswith(b'\x89PNG'), url
        (ASSETS / name).write_bytes(response.content)

def attach_png(cell, name):
    cell.setdefault('attachments', {})[name] = {
        'image/png': base64.b64encode((ASSETS / name).read_bytes()).decode('ascii')
    }

def markdown(cell_id, text):
    cell = nbformat.v4.new_markdown_cell(text)
    cell.id = cell_id
    return cell

def introductions():
    gmt = markdown('intro-gmt', '''## 先認識 GMT：用程式畫地圖

**GMT（Generic Mapping Tools）** 是一套地理資料處理與科學繪圖工具，可以畫海岸線、地形、地震分布、剖面與 3D 地形。

畫圖時，我們把幾個決定交給工具：**畫哪裡、用什麼資料、選什麼投影，以及如何用顏色與符號表達。** 保留程式後，就能換資料、改範圍、重新產生地圖。

今天的目標：從範例改出自己的地圖，知道各設定的意思，再用 AI 加快修改與延伸。

[GMT 官方網站](https://www.generic-mapping-tools.org/)''')
    gallery = markdown('intro-gallery', '''## Gallery：一張地圖可以變成什麼？

先看本教材實際產出的成果，不需要先安裝或執行程式。

上排：台灣海岸線、地震分布、彩色地形。下排：3D 地形與全球地形。

![本教材五種地圖成果](attachment:preview.png)

同一份地形資料，連續改變觀看角度，就能製作旋轉動畫。圖中垂直尺度有誇大。

![台灣地形旋轉動畫](attachment:taiwan_rotation.gif)

**想一想：你想畫哪個地方？希望讀者看到什麼？**

圖片由本教材 PyGMT 程式產生，動畫另用 Python 合成；後面會逐步拆解。也可探索 [PyGMT 官方 Gallery](https://www.pygmt.org/v0.17.0/gallery/index.html)。''')
    gallery.attachments = {
        name: {mime: base64.b64encode((ROOT / 'outputs' / name).read_bytes()).decode('ascii')}
        for name, mime in [('preview.png', 'image/png'), ('taiwan_rotation.gif', 'image/gif')]
    }
    pygmt = markdown('intro-pygmt', '''## PyGMT：把 GMT 接進 Python 流程

PyGMT 讓我們用 **Python 呼叫 GMT**，將資料讀取、整理、分析和繪圖放在同一份 Notebook 裡，也方便使用變數與迴圈。

- **GMT**：提供地圖與科學繪圖能力。
- **PyGMT**：用 Python 操作 GMT，串接資料分析流程。
- **AI**：協助寫程式、修改與除錯；我們仍要檢查資料、範圍和圖例。

傳統 GMT 搭配 shell 也能寫變數與迴圈；PyGMT 的便利在於能接上 Python 生態系。

接下來先自己跑圖、改幾個參數，熟悉後再請 AI 延伸作品。

[PyGMT 官方文件](https://www.pygmt.org/v0.17.0/)''')
    gmt.source = gmt.source.replace('## 先認識 GMT：用程式畫地圖',
        '## 先認識 GMT：用程式畫地圖\n\n![GMT 官方 logo](attachment:gmt-logo.png)')
    attach_png(gmt, 'gmt-logo.png')
    pygmt.source = pygmt.source.replace('## PyGMT：把 GMT 接進 Python 流程',
        '## PyGMT：把 GMT 接進 Python 流程\n\n![PyGMT 官方 logo](attachment:pygmt-logo.png)')
    attach_png(pygmt, 'pygmt-logo.png')
    official = markdown('intro-official-gallery', '''## 官方 Gallery：還可以畫什麼？

以下為 PyGMT 官方範例，點來源連結可查看完整程式。

### 3D 曲面：把網格數值立體呈現

![官方 3D 曲面範例](attachment:surface.png)

這張使用數學函數產生的示範曲面，不是真實地形；同類繪圖方法也能呈現高程網格。

[來源：Plotting a surface](https://www.pygmt.org/v0.17.0/gallery/3d_plots/grdview_surface.html)

### 地震震源機制：用符號表達地震資訊

![官方震源機制範例](attachment:meca.png)

這些「沙灘球」符號用來表達震源機制，這堂課先欣賞，不需要學會解讀所有細節。

[來源：Focal mechanisms](https://www.pygmt.org/v0.17.0/gallery/seismology/meca.html)

### 分區設色：把統計資料放到地圖上

![官方分區設色範例](attachment:choropleth.png)

地圖也能呈現不同地區的統計數值，不只地形和地震。

[來源：Choropleth map](https://www.pygmt.org/v0.17.0/gallery/maps/choropleth_map.html)

圖像來源：PyGMT 官方 Gallery（Generic Mapping Tools 專案）；原始資料與製圖程式詳見各範例頁。''')
    for name in ['surface.png', 'meca.png', 'choropleth.png']:
        attach_png(official, name)
    return [gmt, official, gallery, pygmt]

sources = '''## 地震資料從哪裡來？

PyGMT 負責繪圖，地震資料需要從資料服務取得。本次使用的是**地震目錄**：一列代表一筆事件，不是連續的地震波形。

| 資料來源 | 這堂課怎麼使用？ |
| --- | --- |
| **USGS（美國地質調查所）** | 本次主要地震資料來源；查詢全球事件並下載 CSV，方便從台灣延伸到其他地區。 |
| **台灣 GDMS（中央氣象署臺灣地震與地球物理資料管理系統）** | 補充介紹的台灣資料管道，包含地震目錄、波形與測站等資料；本次不操作下載。 |

先認識五個欄位：**經度、緯度、發生時間、規模、深度**。查詢時選定範圍、期間與最低規模，畫圖時再決定如何呈現。

不同目錄可能有不同的收錄條件與規模類型，筆數不一定相同；使用前要看欄位說明、單位與時間標準。

[USGS 查詢與 CSV 說明](https://earthquake.usgs.gov/fdsnws/event/1/) · [台灣 GDMS](https://gdms.cwa.gov.tw/) · [GDMS 使用說明](https://gdms.cwa.gov.tw/help.php)'''

for filename in ['pygmt_workshop.ipynb', 'pygmt_workshop_executed.ipynb']:
    path = ROOT / filename
    notebook = nbformat.read(path, as_version=4)
    original_codes = [c.source for c in notebook.cells if c.cell_type == 'code']
    notebook.cells = [c for c in notebook.cells if c.id not in {
        'intro-gmt', 'intro-gallery', 'intro-pygmt', 'intro-earthquake-sources', 'intro-official-gallery'
    }]
    notebook.cells[1:1] = introductions()
    index = next(i for i, c in enumerate(notebook.cells)
                 if c.cell_type == 'markdown' and c.source.startswith('## 2. 地震在哪裡'))
    notebook.cells.insert(index, markdown('intro-earthquake-sources', sources))
    assert original_codes == [c.source for c in notebook.cells if c.cell_type == 'code']
    nbformat.validate(notebook)
    nbformat.write(notebook, path)
    print(f'{filename}: {len(notebook.cells)} cells; code and existing outputs preserved')
