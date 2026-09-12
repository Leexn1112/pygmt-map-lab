"""Synchronize the version-controlled setup cell into the three notebooks."""
import json
from pathlib import Path

root = Path(__file__).resolve().parents[1]
source = (root / 'packaging/colab/setup_first.py').read_text().splitlines(keepends=True)[1:]
for path in sorted(root.glob('0[123]_*.ipynb')):
    notebook = json.loads(path.read_text())
    cell = next(c for c in notebook['cells'] if c['id'] == 'workshop-02')
    cell['source'] = source
    cell['execution_count'] = None
    cell['outputs'] = []
    path.write_text(json.dumps(notebook, ensure_ascii=False, indent=1)+'\n')
