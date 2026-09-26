# -*- coding: utf-8 -*-
# Definitive repair: restore corrupted multiline cells.
# 0102/0779 -> authoritative JSON originals. 0134/0142/0154 -> verified fragment reassembly.
import csv, io, re, json, collections, os

TAG = re.compile(r'\^[^;^\s]{1,20};')
wl = {r['id']: r for r in csv.DictReader(open('rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}

def readrows(fn):
    return [r for r in csv.reader(open('translations/' + fn + '.tsv', encoding='utf-8-sig', newline=''), delimiter='\t') if r]

def writefile(fn, idrows):
    idrows.sort(key=lambda r: int(r[0]))
    def dc(t):
        return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip() or not t) else t
    with open('translations/' + fn + '.tsv', 'w', encoding='utf-8-sig', newline='') as f:
        for r in idrows:
            f.write('\t'.join(dc(c) for c in r) + '\n')

def nonid_groups(nonid):
    groups = []; cur = []
    for r in nonid:
        cur.append(r[0].rstrip('\r'))
        if r[0].rstrip().endswith('"'):
            groups.append(cur); cur = []
    if cur: groups.append(cur)
    return groups

def strip_tail(g):
    t = '\n'.join(g)
    if t.endswith('"'): t = t[:-1]
    return t.replace('""', '"')

def segs(cell): return cell.split('\n')

report = []

# ---------- 0102: restore verbatim from priority_0102.json ----------
fn = 'rest_priority_0102'
d = json.load(open('priority_0102.json', encoding='utf-8-sig'))
fix = {i: d[i] for i in ['51263','51270','51272','51276','51288','51329','51330','51331','51335','51336','51340','51385','51407','51411']}
rows = readrows(fn); idrows = [r for r in rows if r[0].isdigit()]
have = {r[0] for r in idrows}
for r in idrows:
    if r[0] in fix: r[1] = fix[r[0]]
if '51330' not in have: idrows.append(['51330', fix['51330']])
writefile(fn, idrows); report.append((fn, sorted(fix)))

# ---------- 0779: restore verbatim ----------
fn = 'rest_priority_0779'
d = json.load(open('priority_0779.json', encoding='utf-8-sig'))
fix = {i: d[i] for i in ['63271','63272']}
rows = readrows(fn); idrows = [r for r in rows if r[0].isdigit()]
have = {r[0] for r in idrows}
for r in idrows:
    if r[0] in fix: r[1] = fix[r[0]]
if '63272' not in have: idrows.append(['63272', fix['63272']])
writefile(fn, idrows); report.append((fn, sorted(fix)))

# ---------- 0134: fragment reassembly ----------
fn = 'rest_priority_0134'
rows = readrows(fn); idrows = [r for r in rows if r[0].isdigit()]
nonid = [r for r in rows if not r[0].isdigit()]
G = nonid_groups(nonid)
cm = {r[0]: r for r in idrows}
seg_58159 = segs(cm['58158'][1])[1].split('\t', 1)[1]      # '치명적인 칼날에는...'
seg_58168 = segs(cm['58167'][1])[1].split('\t', 1)[1]      # '리샨의 신도 여러분...'
seg_plasma = segs(cm['58357'][1])[1]                       # ^cyan;세트 보너스...플라즈마...
fix = {
 '58158': segs(cm['58158'][1])[0] + '\n' + strip_tail([seg_plasma]),
 '58159': seg_58159 + '\n' + strip_tail(G[0]),
 '58160': segs(cm['58160'][1])[0] + '\n' + strip_tail(G[1]),
 '58166': segs(cm['58166'][1])[0] + '\n\n' + strip_tail(G[2]),
 '58167': segs(cm['58167'][1])[0] + '\n\n' + strip_tail([G[3][0]]) + '\n\n' + strip_tail([G[3][1]]),
 '58168': seg_58168 + '\n\n' + strip_tail([G[4][0]]) + '\n\n' + strip_tail([G[4][1]]),
 '58169': segs(cm['58169'][1])[0] + '\n' + strip_tail([G[5][0]]) + '\n\n' + strip_tail([G[5][1]]),
 '58180': segs(cm['58180'][1])[0] + '\n\n\n' + strip_tail(G[6]),
 '58189': segs(cm['58189'][1])[0] + '\n\n' + strip_tail(G[7]),
 '58211': segs(cm['58211'][1])[0] + '\n' + strip_tail(G[8]),
 '58283': segs(cm['58283'][1])[0] + '\n' + strip_tail(G[9]),
 '58355': segs(cm['58355'][1])[0] + '\n' + strip_tail(G[10]),
 '58357': segs(cm['58357'][1])[0] + '\n\n' + strip_tail([G[11][0]]) + '\n\n' + '\n'.join(strip_tail([x]) for x in G[11][1:5]) + '\n\n' + '\n'.join(strip_tail([x]) for x in G[11][5:7]) + '\n\n' + '\n'.join(strip_tail([x]) for x in G[11][7:13]) + '\n\n' + '\n'.join(strip_tail([x]) for x in G[11][13:]),
}
have = {r[0] for r in idrows}
for i, v in fix.items():
    if i in have: cm[i][1] = v
    else: idrows.append([i, v])
writefile(fn, idrows); report.append((fn, sorted(fix)))

# ---------- 0142 ----------
fn = 'rest_priority_0142'
rows = readrows(fn); idrows = [r for r in rows if r[0].isdigit()]
nonid = [r for r in rows if not r[0].isdigit()]
G = nonid_groups(nonid)
cm = {r[0]: r for r in idrows}
fix = {
 '60035': segs(cm['60035'][1])[0] + '\n' + strip_tail(G[0]),
 '60079': segs(cm['60079'][1])[0] + '\n\n' + strip_tail([G[1][0]]) + '\n\n' + strip_tail([G[1][1]]),
 '60080': segs(cm['60080'][1])[0] + '\n\n' + strip_tail([G[2][0]]) + '\n\n' + strip_tail([G[2][1]]),
 '60139': segs(cm['60139'][1])[0] + '\n' + strip_tail(G[3]),
 '60144': segs(cm['60144'][1])[0] + '\n\n' + strip_tail(G[4]),
 '60177': segs(cm['60177'][1])[0] + '\n' + strip_tail(G[5]),
}
for i, v in fix.items(): cm[i][1] = v
writefile(fn, idrows); report.append((fn, sorted(fix)))

# ---------- 0154 ----------
fn = 'rest_priority_0154'
rows = readrows(fn); idrows = [r for r in rows if r[0].isdigit()]
nonid = [r for r in rows if not r[0].isdigit()]
G = nonid_groups(nonid)
cm = {r[0]: r for r in idrows}
seg_62675_tail = segs(cm['62870'][1])[3]                  # '여왕의 음부를...'
seg_62818 = segs(cm['62797'][1])[1].split('\t', 1)[1]     # original wording
seg_62824 = segs(cm['62797'][1])[2].split('\t', 1)[1]
seg_62877 = segs(cm['62870'][1])[1].split('\t', 1)[1]
seg_62881 = segs(cm['62870'][1])[2].split('\t', 1)[1]
fix = {
 '62675': segs(cm['62675'][1])[0] + '\n\n' + seg_62675_tail,
 '62681': segs(cm['62681'][1])[0] + '\n' + strip_tail(G[0]),
 '62685': segs(cm['62685'][1])[0] + '\n\n' + strip_tail([G[1][0]]) + '\n' + strip_tail([G[1][1]]),
 '62736': segs(cm['62736'][1])[0] + '\n' + strip_tail(G[2]),
 '62747': segs(cm['62747'][1])[0] + '\n' + strip_tail(G[3]),
 '62749': segs(cm['62749'][1])[0] + '\n' + strip_tail(G[4]),
 '62797': segs(cm['62797'][1])[0] + '\n' + strip_tail(G[5]),
 '62848': segs(cm['62848'][1])[0] + '\n' + strip_tail([G[6][0]]) + '\n' + strip_tail([G[6][1]]),
 '62870': segs(cm['62870'][1])[0] + '\n' + strip_tail(G[7]),
 '62818': seg_62818, '62824': seg_62824, '62877': seg_62877, '62881': seg_62881,
}
for i, v in fix.items(): cm[i][1] = v
writefile(fn, idrows); report.append((fn, sorted(fix)))

# ---------- verify ----------
print('=== VERIFY ===')
bad = 0
for fn, ids in report:
    rows = readrows(fn)
    idrows = [r for r in rows if r[0].isdigit()]
    nonid = [r for r in rows if not r[0].isdigit()]
    if nonid: print(fn, 'LEFTOVER NONID:', len(nonid)); bad += 1
    seen = set()
    for r in idrows:
        if r[0] in seen: print(fn, 'DUP', r[0]); bad += 1
        seen.add(r[0])
        if len(r) > 1 and re.search(r'\n\d+\t', r[1]): print(fn, 'EMBEDDED', r[0]); bad += 1
        e = wl.get(r[0])
        if e and len(r) > 1:
            if e['englishText'].count('\n') != r[1].count('\n'):
                print(fn, r[0], 'LINES', e['englishText'].count('\n'), '->', r[1].count('\n')); bad += 1
            if collections.Counter(TAG.findall(e['englishText'])) != collections.Counter(TAG.findall(r[1])):
                print(fn, r[0], 'TAGS'); bad += 1
print('bad:', bad)
for fn, ids in report: print(fn, 'fixed', len(ids), 'rows:', ids)
