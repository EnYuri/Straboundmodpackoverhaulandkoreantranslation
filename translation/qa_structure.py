import csv,glob,re,sys,collections
sys.stdout.reconfigure(encoding='utf-8')
wl={r['id']:r for r in csv.DictReader(open('rest_worklist.tsv',encoding='utf-8-sig',newline=''),delimiter='\t')}
ko={}; src={}
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    for r in csv.reader(open(bf,encoding='utf-8-sig',newline=''),delimiter='\t'):
        if r and r[0].isdigit(): ko[r[0]]=r[1]; src[r[0]]=bf
TAG=re.compile(r'\^[^;^\s]{1,20};')
PH=re.compile(r'%s|%\d+|\{[^}]{1,20}\}|<[A-Za-z_][A-Za-z0-9_]*>|\$\{[^}]+\}')
PUA=re.compile(r'[\ue000-\uf8ff]')
INPUT=re.compile(r'\[(?:FIRE|ALT-FIRE|Alt-Fire|ALT|CRIT|SHIFT|UP|Down|DOWN|Jump|LEFT-MOUSE|RIGHT-MOUSE|A|D)\]')
# 의도적 예외: 25930은 영문 원문의 깨진 ^reset. 대신 올바른 ^reset;를 넣어 색 번짐을 막는다
KNOWN_OK={'25930'}
rows=[]
for k in sorted(ko,key=int):
    e=wl.get(k,{}).get('englishText'); t=ko[k]
    if e is None: continue
    iss=[]
    if e.count('\n')!=t.count('\n'): iss.append('lines')
    if collections.Counter(TAG.findall(e))!=collections.Counter(TAG.findall(t)): iss.append('tags')
    if collections.Counter(PH.findall(e))!=collections.Counter(PH.findall(t)): iss.append('placeholders')
    if collections.Counter(PUA.findall(e))!=collections.Counter(PUA.findall(t)): iss.append('glyphs')
    if collections.Counter(INPUT.findall(e))!=collections.Counter(INPUT.findall(t)): iss.append('inputtoken')
    if iss and k not in KNOWN_OK: rows.append((k,src[k][13:],','.join(iss)))
open('qa_struct_all.tsv','w',encoding='utf-8-sig',newline='').write('id\tfile\tissues\n'+''.join(f'{a}\t{b}\t{c}\n' for a,b,c in rows))
print('affected rows:',len(rows))
print(collections.Counter(r[2] for r in rows).most_common())
print(collections.Counter(r[1] for r in rows).most_common(10))
