"""A-B sections for Japan and Himalaya with a tomography background:
TX2019slab (Lu et al. 2019, EarthScope EMC) P-wave perturbation (dvp, %)
sliced along the same line, USGS earthquakes on top. Map above each section."""
import numpy as np
import pandas as pd
import pygmt
import requests
import xarray as xr

MODEL = "TX2019slab.nc"      # EarthScope EMC, 1x1 deg, 22 depth levels 50-2770 km
VAR = "dvp"                  # or "dvs"
CASES = [
    dict(name="Japan", region=[128, 150, 30, 46], A=(130, 38.5), B=(148, 38.5), half_km=100),
    dict(name="Himalaya", region=[74, 96, 20, 38], A=(84, 22), B=(84, 36), half_km=150),
]
START = "1990-01-01"
MINMAG = 5.0
Z_MAX = 700
DEPTH_EDGES = "0,70,300,700"
DEPTH_COLORS = "#d7191c,#fdae61,#2c7bb6"


def fetch(region):
    base = "https://earthquake.usgs.gov/fdsnws/event/1/"
    q = (f"starttime={START}&minmagnitude={MINMAG}"
         f"&minlongitude={region[0]}&maxlongitude={region[1]}"
         f"&minlatitude={region[2]}&maxlatitude={region[3]}")
    n = int(requests.get(base + "count?" + q, timeout=60).text)
    assert n <= 20000, n
    return pd.read_csv(base + "query?format=csv&" + q).dropna(subset=["longitude", "latitude", "depth", "mag"])


def mag_size(m):
    return min(0.05 * 2 ** (m - 5), 0.35)


def tomo_slice(model, track, z_step=10):
    """Return DataArray (depth x distance) of VAR along track (lon, lat, distance)."""
    da = model[VAR]
    pts = da.interp(longitude=("track", track.lon.values), latitude=("track", track.lat.values))
    z_new = np.arange(0, Z_MAX + z_step, z_step)
    vals = np.full((len(z_new), len(track)), np.nan)
    z_old = pts.depth.values
    for j in range(len(track)):
        col = pts.values[:, j]
        ok = np.isfinite(col)
        vals[:, j] = np.interp(z_new, z_old[ok], col[ok], left=np.nan, right=np.nan)
    return xr.DataArray(vals, coords={"y": z_new, "x": track.distance.values}, dims=("y", "x"))


model = xr.open_dataset(MODEL)
fig = pygmt.Figure()
pygmt.config(FONT_ANNOT_PRIMARY="8p", FONT_LABEL="9p", FONT_TITLE="11p", MAP_FRAME_TYPE="plain")

for i, c in enumerate(CASES):
    region, A, B, hw = c["region"], c["A"], c["B"], c["half_km"]
    quakes = fetch(region)
    grid = pygmt.datasets.load_earth_relief(resolution="02m", region=region)

    sel = pygmt.project(data=quakes[["longitude", "latitude", "depth", "mag"]],
                        center=list(A), endpoint=list(B), unit=True, length="w",
                        width=[-hw, hw], convention="xypqz")
    sel.columns = ["longitude", "latitude", "distance", "offset", "depth", "mag"]
    sel = sel.sort_values("mag")
    track = pygmt.project(center=list(A), endpoint=list(B), generate=10, unit=True)
    track.columns = ["lon", "lat", "distance"]
    length_km = float(track.distance.iloc[-1])
    topo = pygmt.grdtrack(points=track[["lon", "lat"]], grid=grid, newcolname="z")
    slab = tomo_slice(model, track)
    print(c["name"], "quakes:", len(quakes), "corridor:", len(sel), "dvp range:",
          np.nanmin(slab.values).round(1), np.nanmax(slab.values).round(1))

    # ---- map -------------------------------------------------------------
    fig.shift_origin(xshift=f"f{1 + i * 15}c", yshift="f10c")
    pygmt.makecpt(cmap="geo", series=[-8000, 6000])
    fig.grdimage(grid=grid, region=region, projection="M10c", cmap=True, shading="+a-45+nt0.5",
                 frame=[f"WSne+t{c['name']}: USGS M>={MINMAG} since {START[:4]}", "a5f1"])
    fig.coast(shorelines="0.3p,gray20", resolution="i")
    pygmt.makecpt(cmap=DEPTH_COLORS, series=DEPTH_EDGES)
    fig.plot(x=quakes.longitude, y=quakes.latitude, size=quakes.mag.apply(mag_size) * 0.7,
             fill=quakes.depth, cmap=True, style="c", pen="0.1p,black", transparency=40)
    dlat, dlon = hw / 111.32, hw / (111.32 * np.cos(np.radians((A[1] + B[1]) / 2)))
    if abs(B[1] - A[1]) < abs(B[0] - A[0]):
        px, py = [A[0], B[0], B[0], A[0]], [A[1] - dlat, B[1] - dlat, B[1] + dlat, A[1] + dlat]
    else:
        px, py = [A[0] - dlon, B[0] - dlon, B[0] + dlon, A[0] + dlon], [A[1], B[1], B[1], A[1]]
    fig.plot(x=px, y=py, close=True, pen="0.8p,black,--")
    fig.plot(x=[A[0], B[0]], y=[A[1], B[1]], pen="1.5p,black")
    fig.text(x=[A[0], B[0]], y=[A[1], B[1]], text=["A", "B"], font="10p,Helvetica-Bold",
             fill="white", pen="0.5p,black", offset="0c/0.3c")
    fig.basemap(map_scale=f"jBL+c{(region[2]+region[3])/2}+w500k+o0.3c/0.3c+f+lkm")

    # ---- section: topo strip ----------------------------------------------
    fig.shift_origin(yshift="f7.2c")
    fig.basemap(region=[0, length_km, -10, 10], projection="X10c/1.2c", frame=["Wsne", "ya10f5+lTopo (km)"])
    fig.plot(x=topo.distance if "distance" in topo else track.distance, y=topo.z / 1000, pen="0.8p,black")
    fig.plot(x=[0, length_km], y=[0, 0], pen="0.3p,gray50,--")

    # ---- section: tomography + earthquakes ---------------------------------
    fig.shift_origin(yshift="-6c")
    pygmt.makecpt(cmap="roma", series=[-2, 2, 0.1], reverse=False)  # roma: red=slow(-), blue=fast(+)
    fig.grdimage(grid=slab, region=[0, length_km, 0, Z_MAX], projection="X10c/-6c", cmap=True,
                 frame=["WSne", "xa200f100+lDistance from A (km)", "ya100f50+lDepth (km)"], nan_transparent=True)
    pygmt.makecpt(cmap=DEPTH_COLORS, series=DEPTH_EDGES)
    fig.plot(x=sel.distance, y=sel.depth, size=sel.mag.apply(mag_size), fill=sel.depth, cmap=True,
             style="c", pen="0.3p,black")
    fig.text(text="A", position="TL", offset="0.15c/-0.1c", font="10p,Helvetica-Bold")
    fig.text(text="B", position="TR", offset="-0.15c/-0.1c", font="10p,Helvetica-Bold")
    fig.text(text=f"corridor +/-{hw} km, {len(sel)} events; model TX2019slab {VAR} (Lu et al. 2019), 1x1 deg, no data above 50 km",
             position="BL", offset="0.15c/0.15c", font="6p", fill="white@30")

pygmt.makecpt(cmap="roma", series=[-2, 2, 0.1])
fig.shift_origin(xshift="f1c", yshift="f0.2c")
fig.colorbar(cmap=True, position="x0c/0c+w6c/0.3c+h", frame=["a1", "+ldVp (%): red slow, blue fast"])
pygmt.makecpt(cmap=DEPTH_COLORS, series=DEPTH_EDGES)
fig.colorbar(cmap=True, position="x8c/0c+w6c/0.3c+h", frame=["a0", "+lEarthquake depth class (km): 0-70 / 70-300 / 300-700"])
fig.savefig("tomo_sections.png", dpi=150)
print("saved")
