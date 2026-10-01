import sys,io,pickle,csv,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
st=pickle.load(open('data/_upstream_state.pkl','rb'));final=st['final']
for k,v in final.items():
    if 'fuoutpostcivilian' in k:
        for p,val in v.items():
            if 'fumantizi' in p and p.rstrip('0123456789').endswith('/'):
                pass
    if 'bo_multi_caliber' in k:
        for p,val in v.items():
            print('MULTI',p,'->',repr(str(val))[:300])
# civilian 35: find pointer ending /35
for k,v in final.items():
    if 'fuoutpostcivilian' in k:
        for p,val in v.items():
            if p.endswith('/35') and 'fumantizi' in p:
                print('CIV35 upstream:',p,'->',repr(str(val))[:200])
csv.field_size_limit(10**7)
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if 'bo_multi_caliber' in r['asset'] and r['pointer']=='/description':
        print('MULTI KO:',repr(r['korean']))
