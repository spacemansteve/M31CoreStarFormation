#!/usr/bin/env python3
"""Recompute candidate counts from saved metadata; these are not accepted science frames."""
import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/evidence'


def main():
    with (EVIDENCE / 'koa_osiris_expanded.csv').open() as handle:
        rows = list(csv.DictReader(handle))
    counts = {}
    for date in ('20081021', '20100815', '20100828', '20100829'):
        candidates = [r for r in rows if r['koaid'].startswith(f'OS.{date}.')
                      and r['targname'] in ('M31-nuc', 'tt000', 'tt001')
                      and r['sfilter'] == 'Kbb'
                      and float(r['elaptime'] or 0) == 900
                      and float(r['sscale'] or 0) == 0.05]
        counts[date] = len({r['koaid'] for r in candidates})
    print('OSIRIS candidates from broad query:', counts)
    print('Paper counts: 13, 18, 22, 23. 2008 discrepancy and narrow-query inconsistencies remain unresolved.')
    print('Retained-night candidates:', sum(n for date, n in counts.items() if date != '20100828'))
    observations = json.loads((EVIDENCE / 'mast_10571.json').read_text())
    if observations['status'] != 'COMPLETE' or observations['paging']['pagesFiltered'] != 1:
        raise ValueError('Incomplete MAST observation response')
    totals = {}
    # Use only the five named associations, not their duplicate combined products.
    ids = {'j9am01010', 'j9am01020', 'j9am01030', 'j9am01050', 'j9am01070'}
    for row in observations['data']:
        if row['obs_id'] in ids:
            if row['dataRights'] != 'PUBLIC':
                raise ValueError('Observation is not public')
            totals[row['filters']] = totals.get(row['filters'], 0) + row['t_exptime']
    print('ACS association exposure totals (seconds):', totals)
    products = json.loads((EVIDENCE / 'mast_10571_products.json').read_text())
    if products['status'] != 'COMPLETE' or products['paging']['pagesFiltered'] != 1:
        raise ValueError('Incomplete MAST product response')
    selected = {r['dataURI']: r['size'] for r in products['data']
                if r['productFilename'] in {name + '_drz.fits' for name in ids}}
    print('Five unique association drizzles:', len(selected), 'total advertised bytes:', sum(selected.values()))
    print('These Stage 0 counts use metadata only. See docs/hst_product.json for the later F435W payload verification.')


if __name__ == '__main__':
    main()
