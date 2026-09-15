"""Map views of several plate-boundary boxes: relief + USGS earthquakes in
three depth classes, scale bar, and a globe inset showing where the box is."""
import math
import numpy as np
import pandas as pd
import pygmt
import requests

REGIONS = [
    ("Japan-Kuril", [138, 155, 33, 48]),
    ("Tonga-Kermadec", [175, 190, -38, -15]),
    ("Peru-Chile", [-80, -65, -35, -15]),
    ("Cascadia", [-130, -118, 40, 52]),
    ("East African Rift", [28, 42, -12, 12]),
    ("East Pacific Rise", [-115, -95, -20, 5]),
    ("San Andreas", [-125, -114, 32, 40]),
    ("Himalaya", [75, 95, 22, 38]),
]
START = "2010-01-01"
DEPTH_EDGES = "0,70,300,700"
DEPTH_COLORS = "#d7191c,#fdae61,#2c7bb6"
MAX_W, MAX_H = 8.0, 7.5   # cm per panel


def usgs(region, minmag):
    base = "https://earthquake.usgs.gov/fdsnws/event/1/"
    q = (f"starttime={START}&minmagnitude={minmag}"
         f"&minlongitude={region[0]}&maxlongitude={region[1]}"
         f"&minlatitude={region[2]}&maxlatitude={region[3]}")
    n = int(requests.get(base + "count?" + q, timeout=60).text)
    return n, base + "query?format=csv&" + q


def fetch(region):
    for minmag in (4.5, 5.0, 5.5, 6.0):
        n, url = usgs(region, minmag)
        if n <= 20000:
            df = pd.read_csv(url).dropna(subset=["longitude", "latitude", "depth", "mag"])
            return df, minmag
    raise RuntimeError("too many events")


def mag_size(m):
    return 0.06 * 2 ** (m - 4.5)


def panel_size(region):
    lon_span = region[1] - region[0]
    lat_mid = math.radians((region[2] + region[3]) / 2)
    # Mercator height/width ratio, approximate
    y0 = math.log(math.tan(math.pi / 4 + math.radians(region[2]) / 2))
    y1 = math.log(math.tan(math.pi / 4 + math.radians(region[3]) / 2))
    ratio = (y1 - y0) / math.radians(lon_span)
    w = MAX_W
    h = w * ratio
    if h > MAX_H:
        h = MAX_H
        w = h / ratio
    return w, h


fig = pygmt.Figure()
pygmt.config(FONT_ANNOT_PRIMARY="7p", FONT_TITLE="10p", MAP_FRAME_TYPE="plain")
cols = 4
for i, (name, region) in enumerate(REGIONS):
    quakes, minmag = fetch(region)
    quakes = quakes.sort_values("depth", ascending=False)  # deep first, shallow on top
    grid = pygmt.datasets.load_earth_relief(resolution="02m", region=region)
    w, h = panel_size(region)
    col, row = i % cols, i // cols
    fig.shift_origin(xshift="f" + f"{1 + col * (MAX_W + 1.5)}c", yshift="f" + f"{1 + (1 - row) * (MAX_H + 2.5)}c")

    pygmt.makecpt(cmap="geo", series=[-8000, 6000])
    fig.grdimage(grid=grid, region=region, projection=f"M{w}c", cmap=True, shading="+a-45+nt0.5",
                 frame=[f"WSne+t{name}", "a5f1"])
    fig.coast(shorelines="0.3p,gray20", resolution="i")
    pygmt.makecpt(cmap=DEPTH_COLORS, series=DEPTH_EDGES)
    fig.plot(x=quakes.longitude, y=quakes.latitude, size=quakes.mag.apply(mag_size),
             fill=quakes.depth, cmap=True, style="c", pen="0.15p,black", transparency=30)
    lat_ref = (region[2] + region[3]) / 2
    fig.basemap(map_scale=f"jBL+c{lat_ref}+w500k+o0.3c/0.3c+f+lkm")
    fig.text(text=f"USGS M>={minmag} since {START[:4]}: {len(quakes)} events", position="TL",
             offset="0.15c/-0.15c", font="6p", fill="white@30")
    with fig.inset(position="jTR+w2c+o0.1c"):
        lon_c, lat_c = (region[0] + region[1]) / 2, (region[2] + region[3]) / 2
        fig.coast(region="g", projection=f"G{lon_c}/{lat_c}/2c", land="gray70", water="white", frame="g")
        fig.plot(x=[region[0], region[1], region[1], region[0]], y=[region[2], region[2], region[3], region[3]],
                 close=True, pen="1p,red")
    print(name, "M>=", minmag, len(quakes))

# shared legend
fig.shift_origin(xshift="f1c", yshift="f0.2c")
fig.colorbar(cmap=True, position="jBL+w6c/0.3c+h", frame=["a0", "+lDepth class (km): 0-70 / 70-300 / 300-700"])
fig.savefig("map_views.png", dpi=150)
print("saved")
