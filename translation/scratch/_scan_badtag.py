import sys,io,csv,re,collections
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
COLORS={'red','green','blue','yellow','cyan','orange','white','reset','magenta','pink','gray','grey','black','violet','brown','shadow','gold','dark'}
hits=collections.defaultdict(list)
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    ko=r['korean']
    for m in re.finditer(r'\^([#a-zA-Z][a-zA-Z0-9#]*)',ko):
        tok=m.group(1)
        nxt=ko[m.end()] if m.end()<len(ko) else ''
        if nxt==';':continue  # well-formed
        if tok.lower() in COLORS or re.fullmatch(r'#[0-9a-fA-F]{6}',tok) or tok.lower()=='':
            hits['caret-nosemi'].append((r['asset'],r['pointer'],ko[max(0,m.start()-30):m.end()+30]))
        elif tok.lower() in {'white','yellow'}:
            hits['caret-nosemi'].append((r['asset'],r['pointer'],ko[max(0,m.start()-30):m.end()+30]))
    for m in re.finditer(r'(?<![\^#a-zA-Z0-9])([a-z]+);',ko):
        if m.group(1).lower() in COLORS:
            hits['bare-colorname'].append((r['asset'],r['pointer'],ko[max(0,m.start()-30):m.end()+30]))
for k,v in hits.items():
    print('===',k,len(v))
    for a,p,c in v[:30]:print('  ',a[-48:],'|',p[-25:],'|',repr(c))
