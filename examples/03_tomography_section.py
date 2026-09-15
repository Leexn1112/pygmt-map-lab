"""速度剖面：同一條 A–B 底下鋪 TX2019slab（Lu et al. 2019）的 P 波速度異常，地震疊在上面。
藍色快，通常是冷的板片；紅色慢，通常是熱的地函。模型 1°×1°、22 層，50 km 以下才有值。

輸出：tomography_section.png
資料：EarthScope EMC TX2019slab（6.7 MB，首次執行下載）、USGS 地震目錄 API。
需要：pygmt 0.17（含 pandas、numpy、xarray）。三維模型由 GMT 自己讀，不需要 netCDF4 或 SciPy。
"""
import os
import re
import urllib.request

import numpy as np
import pandas as pd
import pygmt
import xarray as xr
from pygmt.clib import Session

# ==== 改這裡（和 02_region_map_section.py 用同一組參數，兩張圖才對得上）====
REGION = [128, 150, 30, 46]
START, MINMAG = "1990-01-01", 5.0
A, B = (130, 38.5), (148, 38.5)
HALF_WIDTH_KM = 100
DEPTH_MAX = 700
VAR = "dvp"                        # 或 "dvs"
MODEL = "TX2019slab.nc"
MODEL_URL = "https://data.earthscope.org/archive/seismology/products/emc/netcdf/TX2019slab_percent.r0.0-n4c.nc"
OUT = "tomography_section.png"
# ==========================================================================

# 1. 地震與 A–B 走廊（與 02 相同）
base = "https://earthquake.usgs.gov/fdsnws/event/1/"
query = (f"starttime={START}&minmagnitude={MINMAG}"
         f"&minlongitude={REGION[0]}&maxlongitude={REGION[1]}&minlatitude={REGION[2]}&maxlatitude={REGION[3]}")
assert int(urllib.request.urlopen(base + "count?" + query).read()) <= 20000, "超過 USGS 上限，請提高 MINMAG"
quakes = pd.read_csv(base + "query?format=csv&" + query).dropna(subset=["longitude", "latitude", "depth", "mag"])
selected = pygmt.project(data=quakes[["longitude", "latitude", "depth", "mag"]],
                         center=list(A), endpoint=list(B), unit=True, length="w",
                         width=[-HALF_WIDTH_KM, HALF_WIDTH_KM], convention="xypqz")
selected.columns = ["longitude", "latitude", "distance", "offset", "depth", "mag"]
track = pygmt.project(center=list(A), endpoint=list(B), generate=10, unit=True)
track.columns = ["lon", "lat", "distance"]
length_km = float(track.distance.iloc[-1])
print(f"USGS {START} 起 M >= {MINMAG}：{len(quakes)} 筆，走廊內 {len(selected)} 筆")


def mag_size(m):
    return min(0.05 * 2 ** (m - 5), 0.4)


# 2. 下載模型（只下載一次）
if not os.path.exists(MODEL):
    print("下載 TX2019slab ...")
    urllib.request.urlretrieve(MODEL_URL, MODEL)

# 3. 用 GMT 讀三維模型：grdinterpolate -T 抽出一層，再用 grdtrack 沿 A–B 取樣，逐層做完就是剖面
info = pygmt.grdinfo(f"{MODEL}?{VAR}")
levels = [float(v) for v in re.search(r"z_levels: (.*)", info).group(1).split(",")]
levels = [level for level in levels if level <= DEPTH_MAX]


def sample_level(level):
    with Session() as lib:
        with lib.virtualfile_out(kind="grid") as vout:
            lib.call_module("grdinterpolate", [f"{MODEL}?{VAR}", f"-T{level}", f"-G{vout}"])
            layer = lib.virtualfile_to_raster(vfname=vout, kind="grid")
    return pygmt.grdtrack(points=track[["lon", "lat"]], grid=layer, newcolname="value").value.to_numpy()


matrix = np.array([sample_level(level) for level in levels])  # 深度層 x 點
levels = np.array(levels)

# 4. 深度再內插成每 10 km；模型最淺一層 50 km，以上留白
depths = np.arange(0, DEPTH_MAX + 10, 10)
slice_values = np.full((len(depths), matrix.shape[1]), np.nan)
for j in range(matrix.shape[1]):
    slice_values[:, j] = np.interp(depths, levels, matrix[:, j], left=np.nan, right=np.nan)
tomo = xr.DataArray(slice_values, coords={"y": depths, "x": track.distance.values}, dims=("y", "x"))

# 5. 速度剖面 + 地震
fig = pygmt.Figure()
pygmt.makecpt(cmap="roma", series=[-2, 2, 0.1])  # 紅慢、藍快
fig.grdimage(grid=tomo, region=[0, length_km, 0, DEPTH_MAX], projection="X14c/-8c", cmap=True, nan_transparent=True,
             frame=[f"WSne+t{VAR} TX2019slab (Lu et al. 2019)", "xa200f100+lDistance from A (km)", "ya100f50+lDepth (km)"])
fig.colorbar(position="JBC+w8c/0.3c+h+o0c/1c", frame=["a1", f"+l{VAR} (%): red slow, blue fast"])
pygmt.makecpt(cmap="#d7191c,#fdae61,#2c7bb6", series="0,70,300,700")
fig.plot(x=selected.distance, y=selected.depth, size=selected.mag.apply(mag_size),
         fill=selected.depth, cmap=True, style="c", pen="0.3p,black")
fig.text(text="A", position="TL", offset="0.15c/-0.1c", font="10p,Helvetica-Bold")
fig.text(text="B", position="TR", offset="-0.15c/-0.1c", font="10p,Helvetica-Bold")
fig.text(text=f"corridor +/-{HALF_WIDTH_KM} km, {len(selected)} events; model 1x1 deg, no data above 50 km",
         position="BL", offset="0.15c/0.15c", font="8p", fill="white@30")
fig.savefig(OUT, dpi=150)
print("saved", OUT, "| 讀圖：藍色帶是否傾斜？地震是否貼著它？")
