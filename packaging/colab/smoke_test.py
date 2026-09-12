"""Smoke-test the prebuilt environment without downloading external datasets."""
import tempfile
from pathlib import Path
import numpy as np
import xarray as xr
import pandas
import PIL
import ipywidgets
import ipyleaflet
import pyproj
import pygmt

pygmt.show_versions()
x = np.linspace(119, 123, 61)
y = np.linspace(21, 26, 76)
grid = xr.DataArray(2000 * np.sin(x[None, :] * 4) * np.cos(y[:, None] * 3),
                    coords={'lat': y, 'lon': x}, dims=['lat', 'lon'])
with tempfile.TemporaryDirectory() as directory:
    fig = pygmt.Figure()
    fig.grdimage(grid=grid, projection='M10c', cmap='geo', shading='+a-45+nt1', frame=True)
    fig.grdcontour(grid=grid, interval=500, annotation=1000)
    path = Path(directory) / 'smoke.png'
    fig.savefig(path)
    with PIL.Image.open(path) as image:
        assert image.width > 100 and image.height > 100
        image.verify()
    selected = pygmt.project(data=[[121, 23, 10, 4]], center=[120, 22], endpoint=[122, 25],
                             unit=True, convention='xypqz')
    assert selected.shape == (1, 6)
print('PASS: imports, GMT, Ghostscript, shaded terrain, contours and project')
