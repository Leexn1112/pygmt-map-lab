"""Execute the workshop in a fresh kernel, including the initial slider view."""
from pathlib import Path
import argparse
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('notebooks', nargs='*', help='Notebook filenames; default: all three parts')
args = parser.parse_args()
paths = [root / p for p in args.notebooks] if args.notebooks else sorted(root.glob('0[123]_*.ipynb'))
for path in paths:
    nb = nbformat.read(path, as_version=4)
    client = NotebookClient(nb, timeout=300, kernel_name='python3', resources={'metadata': {'path': str(root)}})
    client.on_cell_start = lambda cell, cell_index, **kwargs: print(f'Cell {cell_index}: {cell.source[:75]}', flush=True)
    client.execute()
    print(f'{path.name}: executed successfully (outputs kept in memory only).')
