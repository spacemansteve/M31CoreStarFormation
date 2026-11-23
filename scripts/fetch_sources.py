#!/usr/bin/env python3
"""Restore manifest-listed evidence, never raw astronomy datasets or existing files."""
import argparse
import hashlib
import json
from pathlib import Path
import urllib.parse
import urllib.request

ROOT = Path(__file__).resolve().parents[1]
MAX_BYTES = 32 * 1024 * 1024


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--fetch-missing', action='store_true', help='Actually fetch missing files; otherwise list them.')
    args = parser.parse_args()
    manifest = json.loads((ROOT / 'docs/acquisition_manifest.json').read_text())
    failures = []
    for item in manifest['files']:
        path = ROOT / item['path']
        if path.exists():
            if hashlib.sha256(path.read_bytes()).hexdigest() != item['sha256']:
                failures.append(f"Existing file differs; not overwritten: {item['path']}")
            continue
        print(f"Missing: {item['path']}")
        if not args.fetch_missing:
            continue
        request = item['request']
        url = request['url']
        params = request.get('params', {})
        encoded = urllib.parse.urlencode(params).encode()
        method = request.get('method', 'GET')
        if method == 'GET' and params:
            url += ('&' if '?' in url else '?') + encoded.decode()
        req = urllib.request.Request(url, data=encoded if method == 'POST' else None,
                                     headers={'User-Agent': 'M31-reproduction-resource-audit/0.1'}, method=method)
        try:
            with urllib.request.urlopen(req, timeout=45) as response:
                data = response.read(MAX_BYTES + 1)
            if len(data) > MAX_BYTES:
                raise ValueError('Response exceeds 32 MiB audit limit')
            if hashlib.sha256(data).hexdigest() != item['sha256']:
                raise ValueError('Response differs from recorded snapshot; start a new documented audit instead')
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open('xb') as handle:
                handle.write(data)
            print(f"Restored and verified: {item['path']}")
        except Exception as error:
            failures.append(f"{item['path']}: {error}")
    for failure in failures:
        print(failure)
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
