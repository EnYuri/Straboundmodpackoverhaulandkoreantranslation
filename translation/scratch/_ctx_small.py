import sys,io,csv,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
want={
 '_FUversioning':'우 !',
 'ffguide3':'!.',
 'bo_multi':'..',
 'pf_poisonprotection':'..',
 'fuoutpostcivilian':'되죠',
 'outfitfitter_saturn':'\x01',
 'vierahistory2':'숲를',
 'vieralore23':'숲가',
 'vieralore33':'숲와',
 'networkguide':'묶음를',
 'pharitu1':'PAREN',
 'pharitu7':'PAREN',
 'fu_warped1':'???',
}
seen=set()
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8'),delimiter='\t'):
    for pat,key in want.items():
        if pat in r['asset'] and (pat,r['pointer']) not in seen:
            seen.add((pat,r['pointer']))
            ko=r['korean']
            print(f"--- {r['asset'][-48:]} | {r['pointer'][-28:]} [{r['kind']}:{r['detail']}]")
            if key=='PAREN':
                print('  KO:',ko[:400].replace('\n','|'))
            else:
                m=re.search(re.escape(key),ko)
                if m:
                    s=max(0,m.start()-70)
                    print('  ...',repr(ko[s:m.end()+70]))
                else:
                    print('  key not found; head:',repr(ko[:120]))
            break
