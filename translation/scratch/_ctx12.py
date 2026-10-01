import sys,io,csv,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
KINDS={'PHRASE:can-become','PHRASE:musimushi','PHRASE:rosseo'}
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if r['kind'] in KINDS:
        print(f"[{r['kind']}] {r['asset'][-46:]} | {r['pointer'][-25:]}")
        print('  KO:',r['korean'][:140].replace('\n','|'))
