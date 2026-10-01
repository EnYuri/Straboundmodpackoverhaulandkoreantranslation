import sys,io,pickle
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
st=pickle.load(open('data/_upstream_state.pkl','rb'));final,seen=st['final'],st['seen']
for k,v in final.items():
    if 'fuoutpostcivilian' in k:
        for p,val in v.items():
            if 'mantizi' in p or 'mantiz' in p:
                print('F',p,'->',repr(str(val))[:130])
print('---- seen ----')
for k,v in seen.items():
    if 'fuoutpostcivilian' in k:
        for p,vals in v.items():
            if 'mantizi' in p:
                for val in vals:print('S',p,'->',repr(str(val))[:130])
