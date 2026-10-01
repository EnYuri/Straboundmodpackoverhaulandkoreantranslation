import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
by=collections.Counter();ex=[]
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if r['kind']!='TONE_MIX':continue
    a=r['asset']
    cat='dialog' if '/dialog' in a or 'npctype' in a or 'radiomessage' in a else \
        'codex' if 'codex' in a else 'quest' if 'quest' in a or 'cinematic' in a else \
        'itemdesc' if re.search(r'\.(item|activeitem|object|consumable|augment|matitem|legs|chest|head|back|monsterpart)',a) else 'other'
    by[cat]+=1
    if cat in ('itemdesc','codex','other') and len(ex)<30:ex.append(r)
for c,n in by.most_common():print(c,n)
print('---- itemdesc/codex/other samples ----')
for r in ex:
    print(r['asset'][-48:],'|',r['pointer'][-22:],'|',r['detail'])
    print('   KO:',r['korean'][:110].replace('\n','|'))
