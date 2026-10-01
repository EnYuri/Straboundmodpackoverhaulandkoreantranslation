import csv, sys, glob, io
start, end = int(sys.argv[1]), int(sys.argv[2])
wl = {}
for r in csv.DictReader(open('data/rest_worklist.tsv', encoding='utf-8-sig', newline=''), delimiter='\t'):
    wl[r['id']] = r
ko = {}
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    for r in csv.reader(open(bf, encoding='utf-8-sig', newline=''), delimiter='\t'):
        if r and r[0].isdigit() and len(r) >= 2:
            ko[r[0]] = r[1]
sys.stdout.reconfigure(encoding='utf-8')
for i in range(start, end+1):
    k = str(i)
    if k not in wl: continue
    r = wl[k]
    print(f"--- {k}  [{r['count']}x {r['keyHints'][:80]}]  mods={r['mods'][:60]}")
    print("EN: " + r['englishText'].replace('\n','\n'))
    print("KO: " + ko.get(k, '<<MISSING>>').replace('\n','\n'))
