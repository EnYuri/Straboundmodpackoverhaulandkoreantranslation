import csv, json, re, sys, subprocess
# Merge a JSON {id: korean} map into a new-translation batch file, then run qa_structure.
# usage: python add_batch.py translations/rest_26001_26350.tsv new.json [more.json ...]
# Private-use glyphs may be written as ⟦E024⟧ (the form dump_batch.py prints); they are restored here.
sys.stdout.reconfigure(encoding='utf-8')
bf = sys.argv[1]
def dump_cell(t):
    return '"'+t.replace('"','""')+'"' if ('\n' in t or '"' in t or '\t' in t or t!=t.strip()) else t
rows = {}
try:
    for r in csv.reader(open(bf, encoding='utf-8-sig', newline=''), delimiter='\t'):
        if r and r[0].isdigit():
            rows[r[0]] = r[1]
except FileNotFoundError:
    pass
en = {r['id']: r['englishText'] for r in csv.DictReader(open('rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')}
added = 0
for jf in sys.argv[2:]:
    for k, v in json.load(open(jf, encoding='utf-8')).items():
        if k not in en:
            print('unknown id', k); continue
        v = re.sub(r'⟦([0-9A-F]{4})⟧', lambda m: chr(int(m.group(1), 16)), v)
        if en[k].count('\n') != v.count('\n'):
            print('line-count mismatch', k, en[k].count('\n'), v.count('\n'))
        rows[k] = v; added += 1
open(bf, 'w', encoding='utf-8-sig', newline='').write(''.join(k+'\t'+dump_cell(rows[k])+'\n' for k in sorted(rows, key=int)))
print('merged', added, 'rows; file now', len(rows))
subprocess.run([sys.executable, 'qa_structure.py'])
