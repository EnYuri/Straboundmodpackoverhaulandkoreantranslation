# Build TSV for description group: 224 memory hits (normalized EN) + 1 new translation.
import csv, pickle, re, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

vals = pickle.load(open('scratch/_vals_description_67da.pkl', 'rb'))
if isinstance(vals, dict):
    vals = list(vals.keys())

mem = {}
for r in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    mem[r['english']] = r['korean']
normmap = {re.sub(r'\r\n?', '\n', k): v for k, v in mem.items()}

# New translation for the one uncovered string (index noted from _desc_nohit).
new_ko = {
    re.sub(r'\r\n?', '\n',
        "''It's easy for the child to throw a keystone into a mountain and cause a landslide, but it's another story if she's the one having to dig her blade into the guts of someone. Despite her dismissive tone on the incident, it was clear to the tengu around her that behind the girl's bravado, was someone who's shaken from the incident.''\r\n"
        "^#5054be;Evasive Leap: Peforming a Special Melee Attack grants 2 ^#C8FAFA;HIT-SHIELDS^reset;^#5054be; for 20s. | 60s Cooldown\r\n"
        "+10% DODGE Chance | DEF: +10% PSYCHIC & THERMAL^reset;"):
    "''아이가 산에 돌 하나 던져 산사태를 일으키는 건 쉽다. 하지만 자기 검을 직접 누군가의 배에 꽂아 넣어야 하는 거라면 이야기는 달라진다. 그 일을 대수롭지 않다는 듯 말했지만, 주변 텐구들에겐 명백했다. 저 소녀의 허세 뒤에는 그 사건으로 동요한 사람이 있었다는 게.''\n"
    "^#5054be;회피 도약: 특수 근접 공격 시전 시 20초간 ^#C8FAFA;피격 방패^reset;^#5054be; 2개 획득. | 60초 재사용 대기시간\n"
    "회피 확률 +10% | 방어력: 정신 +10% & 열^reset;",
}

rows = []
used = set()
for v in vals:
    nv = re.sub(r'\r\n?', '\n', v)
    if nv in normmap:
        ko = normmap[nv]
        rows.append((nv, ko))
        used.add(nv)
    elif nv in new_ko:
        rows.append((nv, new_ko[nv]))
        used.add(nv)
    else:
        print('SKIP:', repr(v[:60]))

print('rows:', len(rows))
with open('data/_uncov_ko_desc_mem.tsv', 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['en', 'ko'])
    w.writerows(rows)
