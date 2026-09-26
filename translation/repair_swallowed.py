# -*- coding: utf-8 -*-
# Repair files where line-based edits merged quoted multiline cells with following rows.
# A corrupted cell reads as: "ko_part1\n<id>\t<ko>\n<id>\t<ko>\n...\nko_lastpart"
# seg0+lastseg = original cell; middle "id\tko" segments = swallowed real rows.
# Only treat as swallowed when that id has NO own row in the file (proves it was consumed).
import csv, glob, re

ID_ROW = re.compile(r'^(\d+)\t(.*)$', re.S)
repaired_cells = 0
restored = 0

for fn in glob.glob('translations/rest_*.tsv'):
    with open(fn, encoding='utf-8-sig', newline='') as f:
        rows = [r for r in csv.reader(f, delimiter='\t') if r]
    ids = {r[0] for r in rows if r and r[0].isdigit()}
    changed = False
    extra = []
    for r in rows:
        if not (r and r[0].isdigit() and len(r) > 1):
            continue
        cell = r[1]
        if '\n' not in cell and '\r' not in cell:
            continue
        segs = re.split(r'\r?\n', cell)
        if len(segs) < 3:
            continue
        own = int(r[0])
        swallowed = []
        keep = []
        ok = True
        for s in segs[1:]:
            m = ID_ROW.match(s)
            if m and m.group(1) not in ids and int(m.group(1)) != own:
                swallowed.append(s)
            else:
                keep.append(s)
        if not swallowed:
            continue
        # cell = seg0 + kept tail segments (excluding swallowed)
        r[1] = '\n'.join([segs[0]] + keep)
        for s in swallowed:
            m = ID_ROW.match(s)
            extra.append([m.group(1), m.group(2)])
            restored += 1
        repaired_cells += 1
        changed = True
    if changed:
        rows.extend(extra)
        rows.sort(key=lambda r: int(r[0]) if r[0].isdigit() else 0)
        def dump_cell(t):
            return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip()) else t
        with open(fn, 'w', encoding='utf-8-sig', newline='') as f:
            for r in rows:
                f.write('\t'.join(dump_cell(c) for c in r) + '\n')
        print('repaired', fn, '+', len(extra), 'rows')
print('cells repaired:', repaired_cells, 'rows restored:', restored)
