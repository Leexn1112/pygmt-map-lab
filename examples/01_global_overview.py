"""全球總覽：地形底圖 + USGS 地震（三段深度）+ 全新世火山 + 熱點。

輸出：global_overview.png
資料：USGS 地震目錄 API、NOAA NCEI 火山位置 API（源自 Smithsonian GVP）、
      GMT 範例檔 @hotspots.txt（Müller, Royer & Lawver 1993）、GMT 全球地形 10 角分。
需要：pygmt 0.17（含 pandas、numpy）。執行約 1 分鐘，需連網。
"""
import json
import urllib.request

import pandas as pd
import pygmt

# ==== 可以改的參數 ====
START = "2000-01-01"          # 地震起始日
MINMAG = 5.5                  # 最低規模；全球 M >= 5.5 自 2000 年約 13,000 筆
OUT = "global_overview.png"
# ======================

# 1. 地震：先查筆數，超過 USGS 單次上限 20,000 就提高規模
base = "https://earthquake.usgs.gov/fdsnws/event/1/"
minmag = MINMAG
while True:
    query = f"starttime={START}&minmagnitude={minmag}"
    count = int(urllib.request.urlopen(base + "count?" + query).read())
    if count <= 20000:
        break
    minmag += 0.5
quakes = pd.read_csv(base + "query?format=csv&" + query).dropna(subset=["longitude", "latitude", "depth", "mag"])
quakes = quakes.sort_values("depth", ascending=False)  # 深的先畫，淺的疊在上面
print(f"USGS {START} 起 M >= {minmag}：{len(quakes)} 筆")

# 2. 火山：NCEI 全新世火山清單，每頁 200 筆
rows, page = [], 1
while True:
    url = f"https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/volcanolocs?itemsPerPage=200&page={page}"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    rows += data["items"]
    if page >= data["totalPages"]:
        break
    page += 1
volcanoes = pd.DataFrame(rows).dropna(subset=["latitude", "longitude"])
print(f"火山：{len(volcanoes)} 座")

# 3. 熱點：GMT 範例檔，第 1、2 欄是經度、緯度
hotspots = pd.read_csv(pygmt.which("@hotspots.txt", download="c"), sep=r"\s+",
                       comment="#", header=None, usecols=[0, 1], names=["lon", "lat"])
print(f"熱點：{len(hotspots)} 個")

# 4. 畫圖
fig = pygmt.Figure()
fig.grdimage(grid="@earth_relief_10m", region="d", projection="N150/22c", cmap="geo", shading="+a-45+nt0.4",
             frame=[f"+tGlobal seismicity (USGS M>={minmag} since {START[:4]}), volcanoes, hotspots", "g30"])
fig.coast(shorelines="0.15p,gray30")
pygmt.makecpt(cmap="#d7191c,#fdae61,#2c7bb6", series="0,70,300,700")  # 淺、中、深三段
fig.plot(x=quakes.longitude, y=quakes.latitude, style="c0.05c", fill=quakes.depth, cmap=True, transparency=40)
fig.plot(x=volcanoes.longitude, y=volcanoes.latitude, style="t0.1c", fill="white", pen="0.15p,black")
fig.plot(x=hotspots.lon, y=hotspots.lat, style="a0.3c", fill="yellow", pen="0.4p,black")
fig.colorbar(position="JBC+w8c/0.3c+h+o0c/0.8c", frame=["a0", "+lEarthquake depth (km): 0-70 / 70-300 / 300-700"])
fig.savefig(OUT, dpi=150)
print("saved", OUT, "| 白三角＝全新世火山；黃星＝熱點")
