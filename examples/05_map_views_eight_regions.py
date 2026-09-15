"""八個交界帶的平面圖，一次畫完，同一套設定方便對照：
地形底圖、USGS 地震三段深度、比例尺、右上角地球儀標出位置。

輸出：map_views_eight_regions.png
資料：USGS 地震目錄 API、GMT 全球地形 2 角分。
需要：pygmt 0.17（含 pandas、numpy）。執行約 3–5 分鐘，需連網。
"""
import math
import urllib.request

import pandas as pd
import pygmt

# ==== 改這裡：名稱與範圍（西、東、南、北） ====
REGIONS = [
    ("Japan-Kuril", [138, 155, 33, 48]),
    ("Tonga-Kermadec", [175, 190, -38, -15]),    # 跨換日線，經度直接用到 190
    ("Peru-Chile", [-80, -65, -35, -15]),
    ("Cascadia", [-130, -118, 40, 52]),
    ("East African Rift", [28, 42, -12, 12]),
    ("East Pacific Rise", [-115, -95, -20, 5]),
    ("San Andreas", [-125, -114, 32, 40]),
    ("Himalaya", [75, 95, 22, 38]),
]
START = "2010-01-01"
OUT = "map_views_eight_regions.png"
# ==========================================
MAX_W, MAX_H = 8.0, 7.5   # 每格最大寬高（cm）
base = "https://earthquake.usgs.gov/fdsnws/event/1/"


def fetch(region):
    """從 M >= 4.5 開始，超過 20,000 筆就提高規模"""
    for minmag in (4.5, 5.0, 5.5, 6.0):
        q = (f"starttime={START}&minmagnitude={minmag}"
             f"&minlongitude={region[0]}&maxlongitude={region[1]}&minlatitude={region[2]}&maxlatitude={region[3]}")
        if int(urllib.request.urlopen(base + "count?" + q).read()) <= 20000:
            df = pd.read_csv(base + "query?format=csv&" + q).dropna(subset=["longitude", "latitude", "depth", "mag"])
            return df, minmag
    raise RuntimeError("too many events")


def mag_size(m):
    return 0.06 * 2 ** (m - 4.5)


def panel_size(region):
    """依麥卡托投影的長寬比決定格子大小"""
    y0 = math.log(math.tan(math.pi / 4 + math.radians(region[2]) / 2))
    y1 = math.log(math.tan(math.pi / 4 + math.radians(region[3]) / 2))
    ratio = (y1 - y0) / math.radians(region[1] - region[0])
    w = MAX_W
    h = w * ratio
    if h > MAX_H:
        h, w = MAX_H, MAX_H / ratio
    return w, h


fig = pygmt.Figure()
pygmt.config(FONT_ANNOT_PRIMARY="7p", FONT_TITLE="10p", MAP_FRAME_TYPE="plain")
cols = 4
for i, (name, region) in enumerate(REGIONS):
    quakes, minmag = fetch(region)
    quakes = quakes.sort_values("depth", ascending=False)  # 深的先畫
    grid = pygmt.datasets.load_earth_relief(resolution="02m", region=region)
    w, h = panel_size(region)
    col, row = i % cols, i // cols
    fig.shift_origin(xshift=f"f{1 + col * (MAX_W + 1.5)}c", yshift=f"f{1 + (1 - row) * (MAX_H + 2.5)}c")

    fig.grdimage(grid=grid, region=region, projection=f"M{w}c", cmap="geo", shading="+a-45+nt0.5",
                 frame=[f"WSne+t{name}", "a5f1"])
    fig.coast(shorelines="0.3p,gray20", resolution="i")
    pygmt.makecpt(cmap="#d7191c,#fdae61,#2c7bb6", series="0,70,300,700")
    fig.plot(x=quakes.longitude, y=quakes.latitude, size=quakes.mag.apply(mag_size),
             fill=quakes.depth, cmap=True, style="c", pen="0.15p,black", transparency=30)
    fig.basemap(map_scale=f"jBL+c{(region[2] + region[3]) / 2}+w500k+o0.3c/0.3c+f+lkm")
    fig.text(text=f"USGS M>={minmag} since {START[:4]}: {len(quakes)} events", position="TL",
             offset="0.15c/-0.15c", font="6p", fill="white@30")
    with fig.inset(position="jTR+w2c+o0.1c"):
        lon_c, lat_c = (region[0] + region[1]) / 2, (region[2] + region[3]) / 2
        fig.coast(region="g", projection=f"G{lon_c}/{lat_c}/2c", land="gray70", water="white", frame="g")
        fig.plot(x=[region[0], region[1], region[1], region[0]], y=[region[2], region[2], region[3], region[3]],
                 close=True, pen="1p,red")
    print(name, "M>=", minmag, len(quakes))

fig.shift_origin(xshift="f1c", yshift="f0.2c")
fig.colorbar(cmap=True, position="x0c/0c+w6c/0.3c+h", frame=["a0", "+lDepth class (km): 0-70 / 70-300 / 300-700"])
fig.savefig(OUT, dpi=150)
print("saved", OUT)
