# Fix corrupt fields: deployed pak fields whose KO came from misaligned rest_* rows.
# The correct KO for each EN comes from realign_fix_map.tsv (pak/sbkor) + _realign_map.MANUAL.
import csv,sys,io,os,json,glob,collections,re,time
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0,r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0,'tools')
import pak,sbjson,pak_writer
from _realign_map import MANUAL
MODS=r'E:/My Games/steamapps/common/Starbound/mods'
TR=os.path.join(MODS,'zz_translation_female.pak')
DRY='--apply' not in sys.argv

wl={r['id']:r['englishText'] for r in csv.DictReader(open('data/rest_worklist.tsv',encoding='utf-8-sig',newline=''),delimiter='\t')}
en2ko={}
for bf in sorted(glob.glob('translations/rest_*.tsv')):
    for r in csv.reader(open(bf,encoding='utf-8-sig',newline=''),delimiter='\t'):
        if len(r)>=2 and r[0].isdigit() and r[0] in wl:
            en2ko[wl[r[0]]]=r[1]
fix={r['en']:r['ko'] for r in csv.DictReader(open('data/realign_fix_map.tsv',encoding='utf-8-sig',newline=''),delimiter='\t')}
fix.update(MANUAL)
pk=pak.Pak(TR)
# collect patch files that contain a replace op whose value == en2ko[EN] for its test EN
changed=collections.Counter();missing=[];touched={}
def walk(o,fn):
    if isinstance(o,list):
        # scan group: test+replace pairs
        for i in range(len(o)):
            a=o[i]
            if isinstance(a,dict) and a.get('op')=='replace' and isinstance(a.get('value'),str):
                # find preceding test in same list
                te=None
                for j in range(i-1,-1,-1):
                    b=o[j]
                    if isinstance(b,dict) and b.get('op')=='test' and b.get('path')==a.get('path'):
                        te=b.get('value');break
                    if isinstance(b,dict) and b.get('op')=='replace' and b.get('path')==a.get('path'):
                        break
                if isinstance(te,str):
                    e=te.strip();k=a['value'].strip()
                    if e in en2ko and en2ko[e].strip()==k and e in fix:
                        a['value']=fix[e];changed[fn]+=1;touched[fn]=o if False else None
                    elif e in en2ko and en2ko[e].strip()==k and e not in fix:
                        missing.append((fn,a.get('path'),e[:50]))
        for x in o:walk(x,fn)
    elif isinstance(o,dict):
        for v in o.values():
            if isinstance(v,(list,dict)):walk(v,fn)
for fn in pk.index:
    if not fn.endswith('.patch'):continue
    try:d=sbjson.parse_sb(pk.read(fn).decode('utf-8'))
    except:continue
    walk(d,fn)
    if changed[fn]:
        pass
print('ops to fix:',sum(changed.values()),'files:',len(changed))
print('unfixed (no map entry):',len(missing))
for m in missing[:10]:print('  MISS',m)
if DRY:
    import collections as C
    print('--- dry run ---');sys.exit()
# apply: re-read each touched file, redo replacement, collect overrides
ov={}
def apply(o):
    n=0
    if isinstance(o,list):
        for i in range(len(o)):
            a=o[i]
            if isinstance(a,dict) and a.get('op')=='replace' and isinstance(a.get('value'),str):
                te=None
                for j in range(i-1,-1,-1):
                    b=o[j]
                    if isinstance(b,dict) and b.get('op')=='test' and b.get('path')==a.get('path'):
                        te=b.get('value');break
                    if isinstance(b,dict) and b.get('op')=='replace' and b.get('path')==a.get('path'):
                        break
                if isinstance(te,str):
                    e=te.strip()
                    if e in en2ko and en2ko[e].strip()==a['value'].strip() and e in fix:
                        a['value']=fix[e];n+=1
        for x in o:n+=apply(x)
    elif isinstance(o,dict):
        for v in o.values():
            if isinstance(v,(list,dict)):n+=apply(v)
    return n
for fn in changed:
    d=sbjson.parse_sb(pk.read(fn).decode('utf-8'))
    n=apply(d)
    ov[fn]=json.dumps(d,ensure_ascii=False,separators=(',',':')).encode('utf-8')
del pk
print('overrides:',len(ov))
staged=TR+'.staged'
pak_writer.write_pak(staged,TR,ov)
print('staged written')
for i in range(90):
    try:os.replace(staged,TR);print('replaced');break
    except PermissionError:time.sleep(5)
else:print('LOCKED - staged at',staged)
