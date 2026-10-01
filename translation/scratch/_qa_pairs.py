import sys,io,os,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0,'tools')
import pak,sbjson
pk=pak.Pak(r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak')
tag=re.compile(r'\^[a-zA-Z#][^;^]*;')
ph=re.compile(r'<[^>]+>')
glyph=re.compile(r'[\ue000-\ue0ff]')
BS=chr(92)
issues=collections.Counter();samples=collections.defaultdict(list)
np_=0
for fn in pk.index:
    if not fn.endswith('.patch'):continue
    try:d=sbjson.parse_sb(pk.read(fn).decode('utf-8-sig'))
    except:continue
    tests={};reps={}
    def walk(o):
        if isinstance(o,list):
            for x in o:walk(x)
        elif isinstance(o,dict):
            if o.get('op')=='test':tests[o.get('path')]=o.get('value')
            elif o.get('op')=='replace':reps[o.get('path')]=o.get('value')
            for v in o.values():
                if isinstance(v,(list,dict)):walk(v)
    walk(d)
    for p,rv in reps.items():
        if p not in tests or not isinstance(rv,str) or not isinstance(tests[p],str):continue
        en,kv=tests[p],rv;np_+=1
        em,km=collections.Counter(tag.findall(en)),collections.Counter(tag.findall(kv))
        if em!=km:
            if em-km:issues['tag_missing']+=1;samples['tag_missing'].append((fn,p,en,kv))
            if km-em:issues['tag_added']+=1;samples['tag_added'].append((fn,p,en,kv))
        if ph.findall(en)!=ph.findall(kv):issues['ph']+=1;samples['ph'].append((fn,p,en,kv))
        if glyph.findall(en)!=glyph.findall(kv):issues['glyph']+=1;samples['glyph'].append((fn,p,en,kv))
        if en.count('\n')!=kv.count('\n'):issues['nl']+=1;samples['nl'].append((fn,p,en,kv))
        if kv.count(BS+'n')!=en.count(BS+'n') and kv.count(BS+'n')>en.count(BS+'n'):issues['litnl']+=1;samples['litnl'].append((fn,p,en,kv))
print('pairs:',np_,'issues:',dict(issues))
with open('data/_qa_pairs_issues.tsv','w',encoding='utf-8',newline='') as f:
    w=csv.writer(f,delimiter='\t')
    w.writerow(['kind','asset','pointer','en','ko'])
    for k,ss in samples.items():
        for s in ss:w.writerow([k,*s])
