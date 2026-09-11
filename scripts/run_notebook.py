"""Execute the workshop in a fresh kernel, including the initial slider view."""
from pathlib import Path
import nbformat
from nbclient import NotebookClient

root = Path(__file__).resolve().parents[1]
nb = nbformat.read(root / 'pygmt_workshop.ipynb', as_version=4)
for i, cell in enumerate(nb.cells):
    cell['id'] = f'workshop-{i:02d}'
client = NotebookClient(nb, timeout=300, kernel_name='python3', resources={'metadata': {'path': str(root)}})
client.on_cell_start = lambda cell, cell_index, **kwargs: print(f'Cell {cell_index}: {cell.source[:75]}', flush=True)
try:
    client.execute()
finally:
    nbformat.write(nb, root / 'pygmt_workshop_executed.ipynb')
print('Notebook executed successfully.')
