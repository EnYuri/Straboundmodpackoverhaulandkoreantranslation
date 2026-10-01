import sys,io,csv,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
rows={}
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    a=r['asset']
    if 'fuoutpostcivilian' in a and '/35' in r['pointer'] and 'fumantizi' in r['pointer']:
        print('CIV35 EN:',r['english'][:150]);print('CIV35 KO:',r['korean'][:150])
    if 'outfitfitter_saturn' in a and '/description'==r['pointer']:
        print('SATURN EN:',repr(r['english'])[:200]);print('SATURN KO:',repr(r['korean'])[:200])
    if 'bo_multi_caliber' in a:
        ko=r['korean']
        m=re.search(r'\.\.',ko)
        if m:print('MULTI ...:',repr(ko[max(0,m.start()-70):m.end()+70]))
        print('MULTI EN tail:',repr(r['english'][-120:]))
    if '_FUversioning' in a and r['pointer']=='/welcome':
        print('FW EN:',repr(r['english'][:400]))
