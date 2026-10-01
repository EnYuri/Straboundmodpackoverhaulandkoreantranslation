import sys,io,csv
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
pats=['naked.npctype','NNCSU','lawenforcementheadquarters01c','mfgstation','ffs_radiomessages_hc','gic_scope_charm','neb-damagetypekills','gic_sawdustbread','plebiancap','10industrialcentrifuge','shoggoth_wagner']
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    for p in pats:
        if p in r['asset']:
            print('===',r['asset'][-45:],'|',r['pointer'][-40:])
            print('  EN:',repr(r['english'])[:260])
            print('  KO:',repr(r['korean'])[:260])
            break
