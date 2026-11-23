#!/usr/bin/env python3
"""Verify saved audit inputs without network access or executing third-party code."""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def verify():
    manifest = json.loads((ROOT / 'docs/acquisition_manifest.json').read_text())
    failures = []
    for item in manifest['files']:
        path = ROOT / item['path']
        if not path.is_file():
            failures.append(f"Missing: {item['path']}")
            continue
        payload = path.read_bytes()
        if len(payload) != item['size_bytes'] or hashlib.sha256(payload).hexdigest() != item['sha256']:
            failures.append(f"Changed: {item['path']}")
    tree_path = ROOT / 'docs/evidence/jlu_tree.json'
    if tree_path.exists():
        tree = json.loads(tree_path.read_text())
        if tree.get('truncated'):
            failures.append('GitHub tree was truncated')
        blobs = {x['path']: x['sha'] for x in tree['tree']}
        for name in ('model_fit.py', 'ppxf_m31.py', 'paper_2017.py'):
            p = ROOT / 'docs/evidence' / name
            if p.exists():
                data = p.read_bytes()
                sha = hashlib.sha1(b'blob ' + str(len(data)).encode() + b'\0' + data).hexdigest()
                if sha != blobs.get('jlu/m31/' + name):
                    failures.append(f'Source does not match pinned Git tree: {name}')
    for failure in failures:
        print(failure)
    if failures:
        raise SystemExit(1)
    print(f"Verified {len(manifest['files'])} audit files; public source blobs match pinned tree.")


if __name__ == '__main__':
    verify()
