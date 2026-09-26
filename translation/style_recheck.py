#!/usr/bin/env python3
import csv, glob, io, re, sys

sys.stdout.reconfigure(encoding='utf-8')
path = 'style_worklist.tsv'
rows = list(csv.reader(open(path, encoding='utf-8-sig', newline=''), delimiter='\t'))
head, body = rows[0], rows[1:]

if len(sys.argv) > 1 and sys.argv[1] == 'start':
    if any(r[-1] == 'RECHECK' for r in body):
        raise SystemExit('RECHECK campaign is already in progress')
    changed = 0
    for r in body:
        if r[-1] == 'OK':
            r[-1] = 'RECHECK'
            changed += 1
    out = io.StringIO()
    writer = csv.writer(out, delimiter='\t', lineterminator='\n')
    writer.writerow(head)
    writer.writerows(body)
    open(path, 'w', encoding='utf-8-sig', newline='').write(out.getvalue())
    print(f'marked for recheck: {changed}')
    raise SystemExit

n = int(sys.argv[1]) if len(sys.argv) > 1 else 20
mode = sys.argv[2] if len(sys.argv) > 2 else 'long'
tag_re = re.compile(r'\^[^;^\s]{1,20};')
worklist = {
    r['id']: r
    for r in csv.DictReader(open('rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t')
}
korean = {}
for batch in glob.glob('translations/rest_*.tsv'):
    for row in csv.reader(open(batch, encoding='utf-8-sig', newline=''), delimiter='\t'):
        if row:
            korean[row[0]] = row[1]

def word_count(row):
    source = tag_re.sub('', worklist[row[0]]['englishText'])
    return len(re.findall(r"[A-Za-z][A-Za-z'\-]*", source))

def is_inspection(row):
    hints = [x.strip().lower() for x in worklist[row[0]]['keyHints'].split('|') if x.strip()]
    generic = {'description', 'longdescription', 'shortdescription'}
    return bool(hints) and all(x.endswith('description') and x not in generic for x in hints)

pending = [r for r in body if r[-1] == 'RECHECK']
if mode == 'worst':
    pending.sort(key=lambda r: float(r[2]))
elif mode == 'long':
    pending.sort(key=lambda r: (is_inspection(r), -word_count(r)))
elif mode == 'inspect':
    pending = [r for r in pending if is_inspection(r)]
    pending.sort(key=lambda r: -word_count(r))
elif mode != 'id':
    raise SystemExit(f'unknown order: {mode}')

print(f'# RECHECK remaining: {len(pending)}  (order: {mode})')
for row in pending[:n]:
    item_id = row[0]
    source = worklist[item_id]
    print(f"===== {item_id} [{source['keyHints'][:40]}] {source['mods'][:40]} ({row[3]})")
    print('--EN--')
    print(source['englishText'])
    print('--KO--')
    print(korean[item_id])
