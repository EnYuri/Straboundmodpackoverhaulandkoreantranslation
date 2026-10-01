import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
by=collections.Counter();ex=collections.defaultdict(list)
for r in csv.DictReader(open('data/qa_mt_style_report.tsv',encoding='utf-8-sig'),delimiter='\t'):
    if r['kind']!='PHRASE:dangsin':continue
    a=r['asset']
    cat='dialog' if '/dialog' in a or 'npctype' in a or 'radiomessage' in a else \
        'codex' if 'codex' in a else 'quest' if 'quest' in a else 'item' if 'item' in a or 'activeitem' in a or 'object' in a or 'consumable' in a or 'augment' in a else 'other'
    by[cat]+=1
    if len(ex[cat])<8:ex[cat].append((a,r['pointer'],r['korean']))
for c,n in by.most_common():
    print('===',c,n)
    for a,p,k in ex[c]:print('   ',a[-38:],'|',k[:100].replace('\n','|'))
