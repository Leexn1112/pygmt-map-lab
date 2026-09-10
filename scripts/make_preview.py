"""Create a contact sheet of the five scientific plots, without changing them."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw

root = Path(__file__).resolve().parents[1] / 'outputs'
files = sorted(root.glob('0[1-5]_*.png'))
canvas = Image.new('RGB', (1500, 1200), '#eeeeee')
for index, path in enumerate(files):
    with Image.open(path) as original:
        thumbnail = ImageOps.contain(original.convert('RGB'), (480, 550))
    x, y = (index % 3) * 500, (index // 3) * 600
    canvas.paste(thumbnail, (x + (500-thumbnail.width)//2, y + 20))
    ImageDraw.Draw(canvas).text((x+20, y+575), path.stem, fill='black')
canvas.save(root / 'preview.png')
