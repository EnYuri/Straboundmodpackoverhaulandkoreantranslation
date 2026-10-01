import sys,io,csv,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if 'bo_multi_caliber' in r['asset']:
        print('PTR',r['pointer'])
        print('KO',repr(r['korean']))
        print()
    if 'fuoutpostcivilian' in r['asset'] and 'fumantizi' in r['pointer'] and r['pointer'].endswith('/35'):
        print('CIV35 test:',repr(r['english']))
