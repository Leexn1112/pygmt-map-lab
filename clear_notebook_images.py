"""Remove embedded images from notebooks without changing executable code."""
from pathlib import Path
import re
import nbformat

ROOT = Path(__file__).resolve().parent

def clear_images(notebook):
    for cell in notebook.cells:
        cell.pop('attachments', None)
        if cell.cell_type == 'markdown':
            cell.source = re.sub(r'!\[[^\]]*\]\([^\n]*?\)', '', cell.source)
            cell.source = re.sub(r'<img\b[^>]*>', '', cell.source, flags=re.I)
            cell.source = re.sub(r'\n{3,}', '\n\n', cell.source)
            cell.source = cell.source.replace(
                '先看本教材實際產出的成果，不需要先安裝或執行程式。',
                '執行後面的繪圖程式，即可查看本教材的成果。')
            cell.source = cell.source.replace(
                '上排：台灣海岸線、地震分布、彩色地形。下排：3D 地形與全球地形。',
                '包含台灣海岸線、地震分布、彩色地形、3D 地形與全球地形。')
            cell.source = cell.source.replace(
                '以下為 PyGMT 官方範例，點來源連結可查看完整程式。',
                '以下為 PyGMT 官方範例，點來源連結可查看圖片與完整程式。')
        elif cell.cell_type == 'code':
            cell.outputs = [o for o in cell.get('outputs', []) if not any(
                key.startswith('image/') or key in ('application/pdf', 'video/mp4')
                or (key == 'text/html' and re.search(r'<(?:img|video)\b', str(value), re.I))
                for key, value in o.get('data', {}).items()
            )]
    return notebook

if __name__ == '__main__':
    for path in ROOT.glob('*.ipynb'):
        notebook = nbformat.read(path, as_version=4)
        code_before = [c.source for c in notebook.cells if c.cell_type == 'code']
        clear_images(notebook)
        assert code_before == [c.source for c in notebook.cells if c.cell_type == 'code']
        nbformat.validate(notebook)
        nbformat.write(notebook, path)
        print(f'Cleared images: {path.name}')
