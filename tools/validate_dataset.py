"""Validate the frozen input snapshot without a solver or external packages."""
import csv, hashlib, json
from collections import Counter
from pathlib import Path
root = Path(__file__).resolve().parents[1]
with (root/'instances_index.csv').open(encoding='utf-8', newline='') as f:
    rows = list(csv.DictReader(f))
assert len(rows) == 900 and len({r['file'] for r in rows}) == 900
assert {p.relative_to(root).as_posix() for p in (root/'instances').rglob('*.json')} == {r['file'] for r in rows}
groups, layouts = Counter(), Counter()
for r in rows:
    payload = (root/r['file']).read_bytes()
    assert hashlib.sha256(payload).hexdigest() == r['sha256'], r['file']
    obj = json.loads(payload); p = obj['params']
    assert len(obj['orders']) == int(r['n_orders']) == p['n_orders']
    assert all(o['tw_early'] == 0 for o in obj['orders'])
    groups[obj['scale']] += 1; layouts[p['layout']] += 1
assert groups == {'small':180, 'benchmark':180, 'large':540}
assert layouts == {'C':450, 'R':450}
print('PASS: 900 unchanged JSON inputs; groups and SHA-256 checksums verified.')
