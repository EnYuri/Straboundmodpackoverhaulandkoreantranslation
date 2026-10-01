# -*- coding: utf-8 -*-
# Reattach multiline-cell tails: pair owner rows (id order) with EOF fragment groups (file order).
import csv, io, re, collections, sys

TAG = re.compile(r'\^[^;^\s]{1,20};')
FILES = ['rest_priority_0102','rest_priority_0134','rest_priority_0142','rest_priority_0154','rest_priority_0779']

wl = {r['id']: r for r in csv.DictReader(open('data/rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}

# flagged rows from qa
flagged = collections.defaultdict(set)
for r in csv.reader(open('data/qa_struct_all.tsv', encoding='utf-8-sig', newline=''), delimiter='\t'):
    if r and r[0].isdigit():
        flagged[r[1]].add(r[0])

def split_groups(nonid):
    groups = []; cur = []
    for r in nonid:
        cur.append(r[0])
        if r[0].rstrip().endswith('"'):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    return groups

for fn in FILES:
    path = 'translations/' + fn + '.tsv'
    rows = [r for r in csv.reader(open(path, encoding='utf-8-sig', newline=''), delimiter='\t') if r]
    idrows = [r for r in rows if r[0].isdigit()]
    nonid = [r for r in rows if not r[0].isdigit()]
    groups = split_groups(nonid)

    # owners: flagged rows in this file + cells containing embedded id\t segs
    owners = []
    for r in idrows:
        i = r[0]
        has_junk = len(r) > 1 and re.search(r'\n\d+\t', r[1])
        if i in flagged[fn + '.tsv'] or has_junk:
            owners.append(r)

    print('=' * 10, fn, 'owners:', len(owners), 'groups:', len(groups))
    # restore: drop embedded id\t segs from every cell
    extra_rows = []
    for r in idrows:
        if len(r) > 1 and re.search(r'\n\d+\t', r[1]):
            segs = r[1].split('\n')
            r[1] = segs[0] + ('\n' + '\n'.join(s for s in segs[1:] if not re.match(r'\d+\t', s)) if any(not re.match(r'\d+\t', s) for s in segs[1:]) else '')

    # pair in order; allow skipping extra flagged rows if counts differ
    for r, g in zip(owners, groups):
        tail = '\n'.join(g)
        tail = tail[:-1] if tail.endswith('"') else tail
        tail = tail.replace('""', '"')
        r[1] = r[1] + '\n' + tail
        # verify
        e = wl[r[0]]['englishText'] if r[0] in wl else None
        if e:
            ln_ok = e.count('\n') == r[1].count('\n')
            tg_ok = collections.Counter(TAG.findall(e)) == collections.Counter(TAG.findall(r[1]))
            print(f'  {r[0]}: lines {e.count(chr(10))}->{r[1].count(chr(10))} {"OK" if ln_ok else "MISMATCH"} | tags {"OK" if tg_ok else "MISMATCH"}')
            if not ln_ok or not tg_ok:
                print('    EN:', repr(e[:150]))
                print('    KO:', repr(r[1][:200]))

    if len(owners) != len(groups):
        print('  !! count mismatch — manual review needed')
        continue

    # write repaired file: id rows sorted + no nonid
    idrows.sort(key=lambda r: int(r[0]))
    def dump_cell(t):
        return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip()) else t
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        for r in idrows:
            f.write('\t'.join(dump_cell(c) for c in r) + '\n')
    print('  written')
