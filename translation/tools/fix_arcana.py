# -*- coding: utf-8 -*-
# Arcana consistency fixes: Exousia spelling, Arcanium spelling, slash skills, workstation
import csv, glob, re

ko_files = glob.glob('translations/rest_*.tsv')

SUBS = [
    ('엑소시아', '엑수시아'),
    ('아르카늄', '아르카니움'),
    ('현대식 작업대', '현대 작업대'),
    ('엑수시아 워크스테이션 미니', '엑수시아 작업대 미니'),
]

EXACT = {
    '122232': '^#1276e5;< ^reset;빙결 베기^#1276e5; >^reset;',
    '76010':  '빙결 베기',
    '101334': '휩쓸 베기',
}

ADD = {
    '51065':  '기본 모루',
    '58082':  '대시 베기',
    '123289': '^#b9b5b2;혁신 작업대',
}

def dump_cell(t):
    return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip()) else t

# read all files once
file_rows = {}
file_ids = {}
for fn in ko_files:
    with open(fn, encoding='utf-8-sig', newline='') as f:
        rows = [r for r in csv.reader(f, delimiter='\t') if r]
        file_rows[fn] = rows
        file_ids[fn] = {r[0] for r in rows if r and r[0].isdigit()}

n = 0
# subs + exact
for fn, rows in file_rows.items():
    for r in rows:
        if not (r and r[0].isdigit() and len(r) > 1):
            continue
        if r[0] in EXACT:
            r[1] = EXACT[r[0]]; n += 1
        else:
            k2 = r[1]
            for a, b in SUBS:
                k2 = k2.replace(a, b)
            if k2 != r[1]:
                r[1] = k2; n += 1

# pick a target file per ADD id: file containing the largest id < target
for i, txt in ADD.items():
    ti = int(i)
    best = None; best_floor = -1
    for fn, ids in file_ids.items():
        lowers = [int(x) for x in ids if int(x) < ti]
        if not lowers:
            continue
        fl = max(lowers)
        if fl > best_floor:
            best_floor = fl; best = fn
    if best is None:
        best = 'translations/rest_31601_31950.tsv'
    file_rows[best].append([i, txt])
    file_ids.setdefault(best, set()).add(i)
    n += 1
    print('add', i, '->', best)

# write all dirty files (rewrite everything; cheap enough)
for fn, rows in file_rows.items():
    rows.sort(key=lambda r: int(r[0]) if r and r[0].isdigit() else 0)
    with open(fn, 'w', encoding='utf-8-sig', newline='') as f:
        for r in rows:
            f.write('\t'.join(dump_cell(c) for c in r) + '\n')
print(n, 'fixed/added')
