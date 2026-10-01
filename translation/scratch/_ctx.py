import csv, sys, io, re
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PATTERNS = {
    'PHRASE:musimushi': r'하는 중입니다|하는 중이다',
    'PHRASE:many-things': r'많은 것들|몇몇 것들',
    'PHRASE:can-become': r'할 수 있게 되|할 수 있게 됩니|할 수 있게 됐',
    'PHRASE:geunom': r'그 녀석|그녀석|저 녀석|저녀석',
    'PHRASE:passive': r'에 의해|에 의해서|에 의한',
    'PHRASE:have-gajigo': r'[을를] 가지고 있',
    'PHRASE:geot-boin': r'것으로 보입니다|것으로 보인다|것 같습니다',
    'PHRASE:jashin': r'자신의|자신을|자신이',
    'PHRASE:through': r'[을를] 통해',
    'PHRASE:this-is': r'(?:그것은|이것은|저것은)',
    'PHRASE:plural-they': r'그들은|그녀들은|우리들은|너희들은',
    'PHRASE:doeeo-is': r'되어 있|되어져|되어진|되어지',
    'PHRASE:geot-imnida': r'것입니다|것이다',
}

WANT = sys.argv[1] if len(sys.argv) > 1 else 'PHRASE:many-things'
LIMIT = int(sys.argv[2]) if len(sys.argv) > 2 else 1000

rx = re.compile(PATTERNS[WANT])
n = 0
for row in csv.DictReader(open('data/qa_mt_style_report.tsv', encoding='utf-8'), delimiter='\t'):
    if row['kind'] != WANT:
        continue
    ko = row['korean']
    m = rx.search(ko)
    i = m.start() if m else 0
    ctxv = ko[max(0, i - 70):i + 90].replace('\n', '\\n')
    print(row['asset'].split('/')[-1] + row['pointer'], '|', ctxv)
    n += 1
    if n >= LIMIT:
        break
print('total shown:', n)
