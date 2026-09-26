import csv, glob, io, json, re, sys
sys.stdout.reconfigure(encoding='utf-8')
NEW=json.load(open(sys.argv[1], encoding='utf-8'))
def dump_cell(t):
    return '"'+t.replace('"','""')+'"' if ('\n' in t or '"' in t or '\t' in t or t!=t.strip()) else t
done=set()
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    rows=[r for r in csv.reader(open(bf,encoding='utf-8-sig',newline=''),delimiter='\t') if r]
    ch=False
    for r in rows:
        if r[0] in NEW:
            if r[1]!=NEW[r[0]]: r[1]=NEW[r[0]]; ch=True
            done.add(r[0])
    if ch:
        open(bf,'w',encoding='utf-8-sig',newline='').write(''.join(r[0]+'\t'+dump_cell(r[1])+'\n' for r in rows))
        print('updated',bf)
print('set',len(done),'missing ids:',[k for k in NEW if k not in done])
