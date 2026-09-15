"""火山與熱點：全球圖，加上日本（火山弧對地震深度）與夏威夷（熱點，不是交界）兩個局部圖。

輸出：volcanoes_hotspots.png
資料：NOAA NCEI 火山位置 API（全新世清單，源自 Smithsonian GVP）、GMT 範例檔 @hotspots.txt、
      USGS 地震目錄 API、GMT 全球地形。
需要：pygmt 0.17（含 pandas）。需連網。
"""
import json
import urllib.request

import pandas as pd
import pygmt

OUT = "volcanoes_hotspots.png"

# 1. 火山：NCEI，每頁 200 筆
rows, page = [], 1
while True:
    url = f"https://www.ngdc.noaa.gov/hazel/hazard-service/api/v1/volcanolocs?itemsPerPage=200&page={page}"
    with urllib.request.urlopen(url) as response:
        data = json.load(response)
    rows += data["items"]
    if page >= data["totalPages"]:
        break
    page += 1
volc = pd.DataFrame(rows).dropna(subset=["latitude", "longitude"])

# 2. 熱點：GMT 範例檔
hot = pd.read_csv(pygmt.which("@hotspots.txt", download="c"), sep=r"\s+", comment="#", header=None,
                  usecols=[0, 1], names=["lon", "lat"])
print("volcanoes:", len(volc), "hotspots:", len(hot))

DEPTH_EDGES, DEPTH_COLORS = "0,70,300,700", "#d7191c,#fdae61,#2c7bb6"


def quakes(region, start, minmag):
    q = (f"format=csv&starttime={start}&minmagnitude={minmag}&minlongitude={region[0]}"
         f"&maxlongitude={region[1]}&minlatitude={region[2]}&maxlatitude={region[3]}")
    return pd.read_csv("https://earthquake.usgs.gov/fdsnws/event/1/query?" + q).dropna(
        subset=["longitude", "latitude", "depth", "mag"])


fig = pygmt.Figure()
pygmt.config(FONT_ANNOT_PRIMARY="8p", FONT_LABEL="9p", FONT_TITLE="11p", MAP_FRAME_TYPE="plain")

# (a) 全球：地形 + 火山 + 熱點
fig.grdimage(grid="@earth_relief_10m", region="d", projection="N150/22c", cmap="geo", shading="+a-45+nt0.4",
             frame=["+tHolocene volcanoes (NCEI/GVP) and hotspots (Mueller et al. 1993)", "g30"])
fig.coast(shorelines="0.15p,gray30")
fig.plot(x=volc.longitude, y=volc.latitude, style="t0.12c", fill="red", pen="0.1p,black")
fig.plot(x=hot.lon, y=hot.lat, style="a0.35c", fill="yellow", pen="0.4p,black")
fig.plot(x=[-175], y=[-75], style="t0.25c", fill="red", pen="0.1p,black")
fig.text(x=-170, y=-75, text="Holocene volcano", justify="ML", font="8p")
fig.plot(x=[-175], y=[-82], style="a0.4c", fill="yellow", pen="0.4p,black")
fig.text(x=-170, y=-82, text="Hotspot", justify="ML", font="8p")

# (b) 日本：火山弧落在橘色中源震正上方
fig.shift_origin(yshift="-9.5c")
reg = [128, 150, 30, 46]
q = quakes(reg, "2010-01-01", 4.5).sort_values("depth", ascending=False)
fig.grdimage(grid=pygmt.datasets.load_earth_relief("02m", region=reg), region=reg, projection="M9c",
             cmap="geo", shading="+a-45+nt0.5", frame=["WSne+tJapan: volcanic arc vs earthquake depth", "a5f1"])
fig.coast(shorelines="0.3p,gray20", resolution="i")
pygmt.makecpt(cmap=DEPTH_COLORS, series=DEPTH_EDGES)
fig.plot(x=q.longitude, y=q.latitude, style="c0.06c", fill=q.depth, cmap=True, transparency=50)
v = volc[(volc.longitude.between(*reg[:2])) & (volc.latitude.between(*reg[2:]))]
fig.plot(x=v.longitude, y=v.latitude, style="t0.22c", fill="white", pen="0.6p,black")
fig.basemap(map_scale="jBL+c38+w500k+o0.3c/0.3c+f+lkm")
fig.text(text=f"{len(v)} volcanoes; quakes USGS M>=4.5 since 2010, red<70 / orange 70-300 / blue>300 km",
         position="TL", offset="0.15c/-0.15c", font="6p", fill="white@30")

# (c) 夏威夷：熱點鏈，只有淺震、只在年輕端
fig.shift_origin(xshift="11c")
reg = [-162, -152, 17, 24]
q = quakes(reg, "2010-01-01", 4.0).sort_values("depth", ascending=False)
fig.grdimage(grid=pygmt.datasets.load_earth_relief("01m", region=reg), region=reg, projection="M9c",
             cmap="geo", shading="+a-45+nt0.5", frame=["WSne+tHawaii: hotspot, no boundary", "a2f1"])
fig.coast(shorelines="0.3p,gray20", resolution="h")
pygmt.makecpt(cmap=DEPTH_COLORS, series=DEPTH_EDGES)
fig.plot(x=q.longitude, y=q.latitude, style="c0.08c", fill=q.depth, cmap=True, transparency=40)
v = volc[(volc.longitude.between(*reg[:2])) & (volc.latitude.between(*reg[2:]))]
fig.plot(x=v.longitude, y=v.latitude, style="t0.25c", fill="white", pen="0.6p,black")
h = hot[(hot.lon.between(*reg[:2])) & (hot.lat.between(*reg[2:]))]
fig.plot(x=h.lon, y=h.lat, style="a0.6c", fill="yellow", pen="0.6p,black")
fig.basemap(map_scale="jBL+c20+w200k+o0.3c/0.3c+f+lkm")
fig.text(text=f"{len(v)} volcanoes, {len(h)} hotspot; quakes USGS M>=4 since 2010, all shallow, only at the young end",
         position="TL", offset="0.15c/-0.15c", font="6p", fill="white@30")

fig.savefig(OUT, dpi=150)
print("saved", OUT)
