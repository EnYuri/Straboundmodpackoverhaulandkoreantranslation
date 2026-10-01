import csv, glob, re, sys, collections
sys.stdout.reconfigure(encoding='utf-8')
wl = {r['id']: r for r in csv.DictReader(open('translations/customrace_unique.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}
ko = {}; src = {}
for bf in sorted(glob.glob('translations/customrace_batch_*.tsv')):
    for r in csv.reader(open(bf, encoding='utf-8-sig', newline=''), delimiter='\t'):
        if r and r[0].isdigit():
            ko[r[0]] = r[1] if len(r) > 1 else ''
            src[r[0]] = bf
TAG = re.compile(r'\^[^;^\s]{1,20};')
PH = re.compile(r'%s|%\d+|\{[^}]{1,20}\}|<[A-Za-z_][A-Za-z0-9_]*>|\$\{[^}]+\}')
PUA = re.compile(r'[-]')
INPUT = re.compile(r'\[(?:FIRE|ALT-FIRE|Alt-Fire|ALT|CRIT|SHIFT|UP|Down|DOWN|Jump|LEFT-MOUSE|RIGHT-MOUSE|A|D)\]')
rows = []
missing_ids = []
for k in sorted(ko, key=int):
    e = wl.get(k, {}).get('english')
    t = ko[k]
    if e is None:
        missing_ids.append(k)
        continue
    iss = []
    if not t.strip():
        iss.append('empty')
    if e.count('\n') != t.count('\n'):
        iss.append('lines')
    if collections.Counter(TAG.findall(e)) != collections.Counter(TAG.findall(t)):
        iss.append('tags')
    if collections.Counter(PH.findall(e)) != collections.Counter(PH.findall(t)):
        iss.append('placeholders')
    if collections.Counter(PUA.findall(e)) != collections.Counter(PUA.findall(t)):
        iss.append('glyphs')
    if collections.Counter(INPUT.findall(e)) != collections.Counter(INPUT.findall(t)):
        iss.append('inputtoken')
    if re.search(r'[A-Za-z]{4,}', t) and not re.search(r'^[A-Z][A-Za-z0-9 .\'\-]*$', e):
        # long latin run survived translation on a non-proper-noun-only source; flag for eyeball review
        iss.append('possible-untranslated')
    if iss:
        rows.append((k, src[k], ','.join(iss)))

open('data/qa_customrace_all.tsv', 'w', encoding='utf-8-sig', newline='').write(
    'id\tfile\tissues\n' + ''.join(f'{a}\t{b}\t{c}\n' for a, b, c in rows))
print('translated total:', len(ko))
print('unknown ids (not in customrace_unique.tsv):', len(missing_ids), missing_ids[:20])
print('affected rows:', len(rows))
print(collections.Counter(r[2] for r in rows).most_common())
