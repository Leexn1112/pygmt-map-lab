"""A-B cross-sections for two boxes (Japan, Himalaya): map with the line and
corridor, then distance-depth section with topography on top. Same depth
axis (0-700 km) for both so they can be compared."""
import numpy as np
import pandas as pd
import pygmt
import requests

CASES = [
    dict(name="Japan", region=[128, 150, 30, 46], A=(130, 38.5), B=(148, 38.5), half_km=100),
    dict(name="Himalaya", region=[74, 96, 20, 38], A=(84, 22), B=(84, 36), half_km=150),
]
START = "2010-01-01"
Z_MAX = 700
DEPTH_EDGES = "0,70,300,700"
DEPTH_COLORS = "#d7191c,#fdae61,#2c7bb6"


def fetch(region):
    base = "https://earthquake.usgs.gov/fdsnws/event/1/"
    for minmag in (4.5, 5.0, 5.5):
        q = (f"starttime={START}&minmagnitude={minmag}"
             f"&minlongitude={region[0]}&maxlongitude={region[1]}"
             f"&minlatitude={region[2]}&maxlatitude={region[3]}")
        if int(requests.get(base + "count?" + q, timeout=60).text) <= 20000:
            return pd.read_csv(base + "query?format=csv&" + q).dropna(
                subset=["longitude", "latitude", "depth", "mag"]), minmag


def mag_size(m):
    return 0.06 * 2 ** (m - 4.5)


fig = pygmt.Figure()
pygmt.config(FONT_ANNOT_PRIMARY="8p", FONT_LABEL="9p", FONT_TITLE="11p", MAP_FRAME_TYPE="plain")

for i, c in enumerate(CASES):
    region, A, B, hw = c["region"], c["A"], c["B"], c["half_km"]
    quakes, minmag = fetch(region)
    grid = pygmt.datasets.load_earth_relief(resolution="02m", region=region)

    sel = pygmt.project(data=quakes[["longitude", "latitude", "depth", "mag"]],
                        center=list(A), endpoint=list(B), unit=True, length="w",
                        width=[-hw, hw], convention="xypqz")
    sel.columns = ["longitude", "latitude", "distance", "offset", "depth", "mag"]
    sel = sel.sort_values("depth", ascending=False)
    length_km = float(pygmt.project(center=list(A), endpoint=list(B), generate=1, unit=True).iloc[-1, 2])
    track = pygmt.project(center=list(A), endpoint=list(B), generate=2, unit=True)
    track.columns = ["lon", "lat", "distance"]
    topo = pygmt.grdtrack(points=track[["lon", "lat"]], grid=grid, newcolname="z")
    topo["distance"] = track["distance"].values
    corridor = pygmt.project(center=list(A), endpoint=list(B), generate=1, unit=True)
    print(c["name"], "M>=", minmag, len(quakes), "in corridor:", len(sel), "length km:", round(length_km))

    # ---- map -------------------------------------------------------------
    fig.shift_origin(xshift=f"f{1 + i * 15}c", yshift="f10c")
    pygmt.makecpt(cmap="geo", series=[-8000, 6000])
    fig.grdimage(grid=grid, region=region, projection="M10c", cmap=True, shading="+a-45+nt0.5",
                 frame=[f"WSne+t{c['name']}: USGS M>={minmag} since 2010", "a5f1"])
    fig.coast(shorelines="0.3p,gray20", resolution="i")
    pygmt.makecpt(cmap=DEPTH_COLORS, series=DEPTH_EDGES)
    fig.plot(x=quakes.longitude, y=quakes.latitude, size=quakes.mag.apply(mag_size) * 0.7,
             fill=quakes.depth, cmap=True, style="c", pen="0.1p,black", transparency=40)
    # corridor outline: shift the track left/right by hw km (approx via project)
    left = pygmt.project(center=list(A), endpoint=list(B), generate=5, unit=True)
    fig.plot(x=[A[0], B[0]], y=[A[1], B[1]], pen="1.5p,black")
    az = float(np.degrees(np.arctan2(B[0] - A[0], B[1] - A[1])))  # rough azimuth
    # corridor as a polygon by offsetting endpoints perpendicular (approximate)
    dlat = hw / 111.32
    dlon = hw / (111.32 * np.cos(np.radians((A[1] + B[1]) / 2)))
    if abs(B[1] - A[1]) < abs(B[0] - A[0]):   # E-W line: offset in latitude
        poly_x = [A[0], B[0], B[0], A[0]]; poly_y = [A[1] - dlat, B[1] - dlat, B[1] + dlat, A[1] + dlat]
    else:                                     # N-S line: offset in longitude
        poly_x = [A[0] - dlon, B[0] - dlon, B[0] + dlon, A[0] + dlon]; poly_y = [A[1], B[1], B[1], A[1]]
    fig.plot(x=poly_x, y=poly_y, close=True, pen="0.8p,black,--")
    fig.text(x=[A[0], B[0]], y=[A[1], B[1]], text=["A", "B"], font="10p,Helvetica-Bold",
             fill="white", pen="0.5p,black", offset="0c/0.3c")
    fig.basemap(map_scale=f"jBL+c{(region[2]+region[3])/2}+w500k+o0.3c/0.3c+f+lkm")

    # ---- section ---------------------------------------------------------
    fig.shift_origin(yshift="f6.5c")
    # topography strip (own axis, km, exaggerated)
    fig.basemap(region=[0, length_km, -10, 10], projection="X10c/1.5c",
                frame=["Wsne", "ya10f5+lTopo (km)"])
    fig.plot(x=topo.distance, y=topo.z / 1000, pen="0.8p,black")
    fig.plot(x=[0, length_km], y=[0, 0], pen="0.3p,gray50,--")
    # earthquakes
    fig.shift_origin(yshift="-5.5c")
    fig.basemap(region=[0, length_km, 0, Z_MAX], projection="X10c/-5.5c",
                frame=["WSne", f"xa200f100+lDistance from A (km)", "ya100f50+lDepth (km)"])
    fig.plot(x=sel.distance, y=sel.depth, size=sel.mag.apply(mag_size), fill=sel.depth, cmap=True,
             style="c", pen="0.15p,black", transparency=30)
    ve = (5.5 / Z_MAX) / (10 / length_km)
    fig.text(text="A", position="TL", offset="0.15c/-0.1c", font="10p,Helvetica-Bold")
    fig.text(text="B", position="TR", offset="-0.15c/-0.1c", font="10p,Helvetica-Bold")
    fig.text(text=f"corridor +/-{hw} km, {len(sel)} events, VE = {ve:.1f}x (topo strip separate)",
             position="BR", offset="-0.15c/0.15c", font="7p")

fig.shift_origin(xshift="f1c", yshift="f0c")
fig.colorbar(cmap=True, position="jBL+w6c/0.3c+h+o0c/-1.5c", frame=["a0", "+lDepth class (km)"])
fig.savefig("sections.png", dpi=150)
print("saved")
