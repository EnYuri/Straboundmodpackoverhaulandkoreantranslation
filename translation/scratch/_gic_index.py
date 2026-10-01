import re, json, io, sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
txt = open(r'scratch/_gic_uniq.txt', encoding='utf-8').read()
parts = re.split(r'^### (\d+) x(\d+)\s*\n', txt, flags=re.M)
# parts[0] header, then triples idx,cnt,body
out = {}
for i in range(1, len(parts), 3):
    idx = int(parts[i]); body = parts[i+2]
    out[idx] = body.rstrip('\n')
json.dump(out, open(r'data/gic_uniq.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(out), 'entries; max idx', max(out))
