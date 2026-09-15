"""3D 海底方塊 + 切面地震：以中大西洋洋脊為例。
只畫切線以北的半塊地形，方塊南緣就是切面，`plane` 把切面塗灰，走廊內地震投到切面上；
下面配一張世界地圖標出研究區、一張平面圖、一張 2D 剖面。

輸出：ridge_block_3d.png
資料：USGS 地震目錄 API、GMT 全球地形 2 角分。
需要：pygmt 0.17（含 pandas、numpy）。需連網。
注意：這個框內 97% 的地震深度是 USGS 固定的 10 km，不是量到的；洋脊區只能說「淺」。
"""
import numpy as np
import pandas as pd
import pygmt

# ==== 改這裡 ====
REGION = [-50, -36, 22, 34]          # 西、東、南、北
CUT_LAT = 28.0                       # 切面緯度
HALF_WIDTH_DEG = 0.5                 # 走廊半寬（度，約 55 km）
START, MINMAG = "2000-01-01", 4.0
Z_MIN_KM = -20                       # 方塊底部（km，負值向下）
ZSIZE_CM, WIDTH_CM = 5, 15
PERSPECTIVE = [165, 30]              # 方位角、仰角
OUT = "ridge_block_3d.png"
# ================

url = ("https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
       f"&starttime={START}&minmagnitude={MINMAG}"
       f"&minlongitude={REGION[0]}&maxlongitude={REGION[1]}&minlatitude={REGION[2]}&maxlatitude={REGION[3]}")
quakes = pd.read_csv(url).dropna(subset=["longitude", "latitude", "depth", "mag"])
print("quakes:", len(quakes), "| 深度為預設 10 km 的比例:", (quakes.depth == 10).mean().round(2))

grid = pygmt.datasets.load_earth_relief(resolution="02m", region=REGION) / 1000.0  # 換成 km，和地震深度同單位
corridor = quakes[(quakes.latitude - CUT_LAT).abs() <= HALF_WIDTH_DEG].copy()
print("corridor quakes:", len(corridor))


def mag_size(m):
    return 0.12 * 2 ** (m - 4)


km_per_deg_lon = 111.32 * np.cos(np.radians(CUT_LAT))
width_km = (REGION[1] - REGION[0]) * km_per_deg_lon
ve_3d = (ZSIZE_CM / abs(Z_MIN_KM)) / (WIDTH_CM / width_km)

fig = pygmt.Figure()

# (a) 3D 方塊：只畫切線以北，南緣就是切面
north = [REGION[0], REGION[1], CUT_LAT, REGION[3]]
pygmt.makecpt(cmap="abyss", series=[-6, -1])
fig.grdview(grid=grid, region=north + [Z_MIN_KM, 0], projection=f"M{WIDTH_CM}c", zsize=f"{ZSIZE_CM}c",
            perspective=PERSPECTIVE, surftype="i", cmap=True, shading="+a-45+nt0.8",
            plane=f"{Z_MIN_KM}+ggray85",
            frame=[f"WSnEZ+tMid-Atlantic Ridge block, cut at {CUT_LAT:.0f}N (VE ~{ve_3d:.0f}x)",
                   "xa4f2", "ya2f1", "za5f1+lz (km)"])
pygmt.makecpt(cmap="batlow", series=[0, 20, 1], background=True)
fig.plot3d(x=corridor.longitude, y=[CUT_LAT] * len(corridor), z=-corridor.depth,
           size=corridor.mag.apply(mag_size), fill=corridor.depth, cmap=True,
           style="c", pen="0.3p,black", transparency=20,
           perspective=PERSPECTIVE, region=north + [Z_MIN_KM, 0], projection=f"M{WIDTH_CM}c", zsize=f"{ZSIZE_CM}c")

# (b) 世界地圖：紅框是研究區，虛線是切線
fig.shift_origin(yshift="-8c")
fig.coast(region="d", projection=f"N{(REGION[0] + REGION[1]) / 2}/12c", land="gray80", water="white",
          shorelines="0.2p,gray50", frame=["+tWhere is this box?", "g30"])
fig.plot(x=[REGION[0], REGION[1], REGION[1], REGION[0]], y=[REGION[2], REGION[2], REGION[3], REGION[3]],
         close=True, pen="1.5p,red")
fig.plot(x=[REGION[0], REGION[1]], y=[CUT_LAT, CUT_LAT], pen="1p,red,--")

# (c) 平面圖：切線與走廊
fig.shift_origin(yshift="-9.5c")
pygmt.makecpt(cmap="abyss", series=[-6, -1])
fig.grdimage(grid=grid, region=REGION, projection="M7c", cmap=True, shading="+a-45+nt0.8",
             frame=["WSne+tMap view", "xa4f2", "ya2f1"])
fig.plot(x=[REGION[0], REGION[1], REGION[1], REGION[0]],
         y=[CUT_LAT - HALF_WIDTH_DEG, CUT_LAT - HALF_WIDTH_DEG, CUT_LAT + HALF_WIDTH_DEG, CUT_LAT + HALF_WIDTH_DEG],
         close=True, pen="0.8p,white,--")
fig.plot(x=[REGION[0], REGION[1]], y=[CUT_LAT, CUT_LAT], pen="1.2p,white")
pygmt.makecpt(cmap="batlow", series=[0, 20, 1], background=True)
fig.plot(x=quakes.longitude, y=quakes.latitude, size=quakes.mag.apply(mag_size) * 0.5,
         fill=quakes.depth, cmap=True, style="c", pen="0.2p,black")
fig.basemap(map_scale=f"jBL+c{CUT_LAT}+w200k+o0.4c/0.4c+f+lkm")
fig.colorbar(frame="a5+lDepth (km)", position="JBC+o0c/1.2c+w6c/0.3c+h")

# (d) 2D 剖面
fig.shift_origin(xshift="8.5c")
track = pygmt.grdtrack(points=pd.DataFrame({"lon": np.arange(REGION[0], REGION[1] + 1e-9, 0.05), "lat": CUT_LAT}),
                       grid=grid, newcolname="z")
sec_w, sec_h = 12, 6
ve_2d = (sec_h / abs(Z_MIN_KM)) / (sec_w / width_km)
fig.basemap(region=[REGION[0], REGION[1], Z_MIN_KM, 0], projection=f"X{sec_w}c/{sec_h}c",
            frame=[f"WSne+tSection along {CUT_LAT:.0f}N, corridor +/-{HALF_WIDTH_DEG} deg (VE ~{ve_2d:.0f}x)",
                   "xa4f2+lLongitude (deg)", "ya5f1+lz (km)"])
fig.plot(x=track.lon, y=track.z, pen="1p,black")
fig.plot(x=corridor.longitude, y=-corridor.depth, size=corridor.mag.apply(mag_size),
         fill=corridor.depth, cmap=True, style="c", pen="0.3p,black", transparency=20)
fig.text(text=f"USGS M>={MINMAG}, {START[:4]}-now. Most ridge depths are fixed at 10 km by USGS, not measured.",
         position="BL", offset="0.2c/0.2c", font="8p")
fig.savefig(OUT, dpi=150)
print("saved", OUT, "| VE 3D:", round(ve_3d), "VE 2D:", round(ve_2d))
