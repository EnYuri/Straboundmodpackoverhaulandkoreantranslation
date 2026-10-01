import csv,glob,sys
sys.stdout.reconfigure(encoding='utf-8')
wl={r['id']:r for r in csv.DictReader(open('data/rest_worklist.tsv',encoding='utf-8-sig',newline=''),delimiter='\t')}
ko={}
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    for r in csv.reader(open(bf,encoding='utf-8-sig',newline=''),delimiter='\t'):
        if r and r[0].isdigit(): ko[r[0]]=r[1]
ids=sys.argv[1:]
for k in ids:
    print(f"===== {k}  [{wl[k]['count']}x {wl[k]['keyHints'][:50]}] {wl[k]['mods'][:50]}")
    print("--EN--"); print(wl[k]['englishText'])
    print("--KO--"); print(ko[k])
