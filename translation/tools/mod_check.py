# -*- coding: utf-8 -*-
# Per-mod QA: inconsistent translations of identical source, untranslated leftovers, summary
import csv, glob, sys, re, collections

target = sys.argv[1]  # pak filename substring
ko = {}
for fn in glob.glob('translations/rest_*.tsv'):
    with open(fn, encoding='utf-8-sig', newline='') as f:
        for r in csv.reader(f, delimiter='\t'):
            if r and r[0].isdigit(): ko[r[0]] = r[1]

rows = []
with open('data/rest_worklist.tsv', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        if target in r['mods']:
            rows.append(r)

print(f'rows: {len(rows)}')
done = [r for r in rows if r['id'] in ko]
print(f'translated: {len(done)}')

# untranslated leftovers
unt = [r for r in rows if r['id'] not in ko]
desc_keys = re.compile(r'description|longDescription|inspect', re.I)
nondesc_unt = [r for r in unt if not desc_keys.search(r['keyHints'])]
print(f'untranslated: {len(unt)} (non-desc keys: {len(nondesc_unt)})')
for r in nondesc_unt[:15]:
    print(f'  UNT [{r["id"]}] {r["keyHints"][:40]}: {r["englishText"][:80]}')

# same source -> different Korean
bymap = collections.defaultdict(set)
for r in done:
    e = r['englishText'].strip()
    if len(e) >= 8:
        bymap[e].add(ko[r['id']])
diff = {e: k for e, k in bymap.items() if len(k) > 1}
print(f'inconsistent same-source translations: {len(diff)}')
for e, ks in list(diff.items())[:25]:
    print(f'  EN: {e[:90]}')
    for k in ks:
        print(f'    -> {k[:90]}')
