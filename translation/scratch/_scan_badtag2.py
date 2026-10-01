import sys,io,csv,re
sys.stdout=io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')
csv.field_size_limit(10**7)
COLORS={'red','green','blue','yellow','cyan','orange','white','reset','magenta','pink','gray','grey','black','violet','brown'}
out=open('data/_badtags.tsv','w',encoding='utf-8',newline='')
for r in csv.DictReader(open('data/pak_pairs.tsv',encoding='utf-8-sig'),delimiter='\t'):
    ko=r['korean']
    for m in re.finditer(r'\^([#a-zA-Z][a-zA-Z0-9#]*)',ko):
        tok=m.group(1);nxt=ko[m.end()] if m.end()<len(ko) else ''
        if nxt==';':continue
        # skip compound tags (contain comma list) - tok won't contain comma anyway; check if NEXT part forms compound: ^a,b; - tok='a'? actually regex stops at comma
        # check: is this a compound like ^white,shadow; -> tok='white', nxt=',' -> legit compound, skip
        if nxt==',':continue
        if tok.lower() in COLORS or re.fullmatch(r'#[0-9a-fA-F]{6}',tok):
            out.write(f"NOSEMI\t{r['asset']}\t{r['pointer']}\t{ko[max(0,m.start()-40):m.end()+40]}\n")
    for m in re.finditer(r'(?<![\^#a-zA-Z0-9,])([a-z]+);',ko):
        if m.group(1).lower() in COLORS:
            out.write(f"BARE\t{r['asset']}\t{r['pointer']}\t{ko[max(0,m.start()-40):m.end()+40]}\n")
out.close()
print(open('data/_badtags.tsv',encoding='utf-8').read())
