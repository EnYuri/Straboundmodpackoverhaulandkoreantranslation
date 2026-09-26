#!/usr/bin/env python3
"""Flag batch rows written in the compressed 'telegraphic' style so they can be
rewritten as natural Korean.

Primary signal: Hangul characters per English word. Human-reviewed natural prose
sits at a median of ~2.0 with a 5th percentile of 1.38 (8-19 source words) and
1.59 (20+ words); telegraphic rows fall between 1.0 and 1.5. Rows with at least 8
source words and a density below 1.45 (short) or 1.62 (20+ words) are flagged.

Secondary signal: '·' used to glue Korean words together where the source has no
such compound.

Writes style_worklist.tsv (id, file, density, flags, status).
"""
import csv, glob, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
# density thresholds by source length (natural prose 5th percentile is ~1.38-1.59)
SHORT_THR, LONG_THR, MINW = 1.45, 1.62, 8
TAG = re.compile(r'\^[^;^\s]{1,20};')
HAN = re.compile(r'[\uac00-\ud7a3]')
MIDDOT = re.compile(r'[\uac00-\ud7a3]·[\uac00-\ud7a3]')
wl = {r['id']: r for r in csv.DictReader(open('rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}
ko, src = {}, {}
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    for r in csv.reader(open(bf, encoding='utf-8-sig', newline=''), delimiter='\t'):
        if r:
            ko[r[0]] = r[1]; src[r[0]] = bf[13:]
rows = []
for k, t in ko.items():
    e = TAG.sub('', wl.get(k, {}).get('englishText', ''))
    kt = TAG.sub('', t)
    ew = len(re.findall(r"[A-Za-z][A-Za-z'\-]*", e))
    han = len(HAN.findall(kt))
    if not han:
        continue
    dens = han / ew if ew else 99
    flags = []
    thr = SHORT_THR if ew < 20 else LONG_THR
    if ew >= MINW and dens < thr:
        flags.append('dense%.2f' % dens)
    if MIDDOT.search(kt) and not MIDDOT.search(e.replace('&', '·')):
        flags.append('middot')
    if flags:
        rows.append((k, src[k], '%.2f' % dens, ';'.join(flags)))
prev = {}
try:
    for r in csv.DictReader(open('style_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t'):
        if r['status'] != 'TODO':
            prev[r['id']] = r['status']
except FileNotFoundError:
    pass
with open('style_worklist.tsv', 'w', encoding='utf-8-sig', newline='') as f:
    f.write('id\tfile\tdensity\tflags\tstatus\n')
    for r in sorted(rows, key=lambda x: int(x[0])):
        f.write('\t'.join(r) + '\t' + prev.get(r[0], 'TODO') + '\n')
print('flagged rows:', len(rows), collections.Counter(r[3].split(';')[0][:5] for r in rows))
print('carried-over statuses kept:', len(prev))
print('reviewed-range (25551+) hits:', sum(1 for r in rows if int(r[0]) >= 25551))
