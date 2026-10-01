import io, sys, json, re
sys.stdout.reconfigure(encoding='utf-8')
uniq = {int(k): v for k, v in json.load(open('data/gic_uniq.json', encoding='utf-8')).items()}
ko = {}
for l in open('data/gic_ko_05.tsv', encoding='utf-8'):
    if l.strip():
        i, t = l.rstrip('\n').split('\t', 1); ko[int(i)] = t
tagre = re.compile(r'\^[#A-Za-z0-9]+;')
out = open('scratch/_gic_05_review.txt', 'w', encoding='utf-8')
for i in range(1101, 1401):
    en, k = uniq[i], ko[i]
    flag = ''
    if sorted(tagre.findall(en)) != sorted(tagre.findall(k)):
        flag += ' [TAGDIFF]'
    if en.count('\n') != k.count('\\n'):
        flag += ' [NLDIFF]'
    cls = 'NAME' if len(en) < 60 else 'DESC'
    out.write(f'{i} [{cls}]{flag}\n  EN: {en[:100]!r}\n  KO: {k[:100]!r}\n')
out.close()
print('done')
