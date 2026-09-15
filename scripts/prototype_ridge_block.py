"""Test: 3D seafloor block of a Mid-Atlantic Ridge segment with a vertical cut
face showing USGS earthquakes, plus map view and a plain 2D cross-section."""
import numpy as np
import pandas as pd
import pygmt

# ---- parameters -----------------------------------------------------------
REGION = [-50, -36, 22, 34]          # full box (W, E, S, N)
CUT_LAT = 28.0                       # latitude of the vertical cut face
HALF_WIDTH_DEG = 0.5                 # corridor half-width (~55 km)
Z_MIN_KM = -20                       # bottom of the block (km, negative = down)
ZSIZE_CM = 5
WIDTH_CM = 15
PERSPECTIVE = [165, 30]              # azimuth, elevation
OUT = "mar_block.png"

# ---- data -----------------------------------------------------------------
url = (
    "https://earthquake.usgs.gov/fdsnws/event/1/query?format=csv"
    "&starttime=2000-01-01&minmagnitude=4"
    f"&minlongitude={REGION[0]}&maxlongitude={REGION[1]}"
    f"&minlatitude={REGION[2]}&maxlatitude={REGION[3]}"
)
quakes = pd.read_csv(url).dropna(subset=["longitude", "latitude", "depth", "mag"])
print("quakes:", len(quakes), "| depth fixed at 10 km:", (quakes.depth == 10).mean().round(2))

grid = pygmt.datasets.load_earth_relief(resolution="02m", region=REGION) / 1000.0  # km
corridor = quakes[(quakes.latitude - CUT_LAT).abs() <= HALF_WIDTH_DEG].copy()
print("corridor quakes:", len(corridor))

def mag_size(m):
    return 0.12 * 2 ** (m - 4)       # cm; M4 -> 0.12, M5 -> 0.24, M6 -> 0.48

km_per_deg_lon = 111.32 * np.cos(np.radians(CUT_LAT))
width_km = (REGION[1] - REGION[0]) * km_per_deg_lon
ve_3d = (ZSIZE_CM / abs(Z_MIN_KM)) / (WIDTH_CM / width_km)

# ---- figure ---------------------------------------------------------------
fig = pygmt.Figure()

# (a) 3D block. Only the half north of the cut is drawn, so the block's
#     southern edge IS the cut face; `plane` paints that facade grey.
north = [REGION[0], REGION[1], CUT_LAT, REGION[3]]
pygmt.makecpt(cmap="abyss", series=[-6, -1])
fig.grdview(
    grid=grid,
    region=north + [Z_MIN_KM, 0],
    projection=f"M{WIDTH_CM}c",
    zsize=f"{ZSIZE_CM}c",
    perspective=PERSPECTIVE,
    surftype="i",
    cmap=True,
    shading="+a-45+nt0.8",
    plane=f"{Z_MIN_KM}+ggray85",
    frame=["WSnEZ+tMid-Atlantic Ridge block, cut at 28N", "xa4f2", "ya2f1", "za5f1+lz (km)"],
)
pygmt.makecpt(cmap="batlow", series=[0, 20, 1], background=True)
fig.plot3d(
    x=corridor.longitude, y=[CUT_LAT] * len(corridor), z=-corridor.depth,
    size=corridor.mag.apply(mag_size), fill=corridor.depth, cmap=True,
    style="c", pen="0.3p,black", transparency=20,
    perspective=PERSPECTIVE, region=north + [Z_MIN_KM, 0],
    projection=f"M{WIDTH_CM}c", zsize=f"{ZSIZE_CM}c",
)

# (b0) world map with the study box
fig.shift_origin(yshift="-8c")
fig.coast(region="d", projection=f"N{(REGION[0]+REGION[1])/2}/12c", land="gray80", water="white",
          shorelines="0.2p,gray50", frame=["+tWhere is this box?", "g30"])
fig.plot(x=[REGION[0], REGION[1], REGION[1], REGION[0]], y=[REGION[2], REGION[2], REGION[3], REGION[3]],
         close=True, pen="1.5p,red")
fig.plot(x=[REGION[0], REGION[1]], y=[CUT_LAT, CUT_LAT], pen="1p,red,--")
fig.text(x=REGION[1] + 2, y=(REGION[2]+REGION[3])/2, text="Mid-Atlantic Ridge box",
         justify="ML", font="9p,Helvetica-Bold,red")

# (b) map view with the cut line and corridor
fig.shift_origin(yshift="-9.5c")
pygmt.makecpt(cmap="abyss", series=[-6, -1])
fig.grdimage(grid=grid, region=REGION, projection="M7c", cmap=True,
             shading="+a-45+nt0.8", frame=["WSne+tMap view", "xa4f2", "ya2f1"])
fig.plot(x=[REGION[0], REGION[1], REGION[1], REGION[0]],
         y=[CUT_LAT - HALF_WIDTH_DEG, CUT_LAT - HALF_WIDTH_DEG, CUT_LAT + HALF_WIDTH_DEG, CUT_LAT + HALF_WIDTH_DEG],
         close=True, pen="0.8p,white,--")
fig.plot(x=[REGION[0], REGION[1]], y=[CUT_LAT, CUT_LAT], pen="1.2p,white")
pygmt.makecpt(cmap="batlow", series=[0, 20, 1], background=True)
fig.plot(x=quakes.longitude, y=quakes.latitude, size=quakes.mag.apply(mag_size) * 0.5,
         fill=quakes.depth, cmap=True, style="c", pen="0.2p,black")
fig.basemap(map_scale=f"jBL+c{CUT_LAT}+w200k+o0.4c/0.4c+f+lkm")
fig.colorbar(frame="a5+lDepth (km)", position="JBC+o0c/1.2c+w6c/0.3c+h")

# (c) 2D section along the cut: topography axis exaggerated separately
fig.shift_origin(xshift="8.5c")
track = pygmt.grdtrack(
    points=pd.DataFrame({"lon": np.arange(REGION[0], REGION[1] + 1e-9, 0.05), "lat": CUT_LAT}),
    grid=grid, newcolname="z",
)
sec_w, sec_h = 12, 6
ve_2d = (sec_h / abs(Z_MIN_KM)) / (sec_w / width_km)
fig.basemap(region=[REGION[0], REGION[1], Z_MIN_KM, 0], projection=f"X{sec_w}c/{sec_h}c",
            frame=[f"WSne+tSection along {CUT_LAT:.0f}N, corridor +/-{HALF_WIDTH_DEG} deg (VE ~{ve_2d:.0f}x)",
                   "xa4f2+lLongitude (deg)", "ya5f1+lz (km)"])
fig.plot(x=track.lon, y=track.z, pen="1p,black")
fig.plot(x=corridor.longitude, y=-corridor.depth, size=corridor.mag.apply(mag_size),
         fill=corridor.depth, cmap=True, style="c", pen="0.3p,black", transparency=20)
fig.text(text="USGS M>=4, 2000-now. Most ridge depths are fixed at 10 km by USGS, not measured.",
         position="BL", offset="0.2c/0.2c", font="8p")

fig.savefig(OUT, dpi=150)
print("saved", OUT, "| VE 3D:", round(ve_3d), "VE 2D:", round(ve_2d))
