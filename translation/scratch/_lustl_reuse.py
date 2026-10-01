# Quantify reuse potential for Lustlings' uncovered modifyed items by matching
# EN text against every available KO source: zz_translation_female pairs and
# the sbkor translation pak's own patch values.
import sys, io, json, re, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
SBKOR = r"E:\My Games\steamapps\common\Starbound\mods\-9998_trans_sbkor_0.98_structfix.pak"
LK = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"
PAIRS = r"data\pak_pairs.tsv"

FIELDS = ('shortdescription', 'description')


def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out = []
    ins = False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        out.append('\\r' if ins and c == '\r' else '\\n' if ins and c == '\n' else c)
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))


def flat_ops(raw):
    ops = json.loads(raw)
    return [o for x in ops for o in (x if isinstance(x, list) else [x])]


def norm(s):
    s = re.sub(r'\^[a-zA-Z#0-9;]*;', '', s)
    s = re.sub(r'\s+', ' ', s).strip().lower()
    return s


# build EN->KO maps
csv.field_size_limit(10 ** 8)
en2ko = {}
with open(PAIRS, encoding='utf-8-sig') as f:
    for r in csv.reader(f, delimiter='\t'):
        if len(r) >= 4:
            en2ko.setdefault(r[2], r[3])
print('pairs EN map:', len(en2ko))

# sbkor: derive EN->KO from test+replace pairs
sb = Pak(SBKOR)
sb_pairs = 0
for p in sb.index:
    if not p.endswith('.patch'):
        continue
    try:
        flat = flat_ops(sb.read(p).decode('utf-8'))
    except Exception:
        continue
    for i in range(len(flat) - 1):
        a, b = flat[i], flat[i + 1]
        if a.get('op') == 'test' and b.get('op') == 'replace' \
                and a.get('path') == b.get('path') \
                and isinstance(a.get('value'), str) and isinstance(b.get('value'), str) \
                and re.search(r'[가-힣]', b['value']):
            en2ko.setdefault(a['value'], b['value'])
            sb_pairs += 1
print('after sbkor:', len(en2ko), '(+', sb_pairs, ')')

nmap = {norm(k): v for k, v in en2ko.items()}

tr = Pak(TR)
ti = set(tr.index)
lk = Pak(LK)
total = full = part = none = 0
full_items = []
none_items = []
for p in lk.index:
    ext = p.rsplit('.', 1)[-1] if '.' in p else ''
    if ext in ('patch', 'png', 'frames', 'ogg', 'wav', 'lua', 'json'):
        continue
    if 'lustl' not in p.lower():
        continue
    if p + '.patch' in ti or p in ti:
        continue
    try:
        doc = parse_sb(lk.read(p))
    except Exception:
        continue
    hits = []
    for f in FIELDS:
        v = doc.get(f)
        if isinstance(v, str) and re.search(r'[a-zA-Z]{4,}', v):
            hits.append((f, v))
    if not hits:
        continue
    total += 1
    got = [en2ko.get(v) or nmap.get(norm(v)) for _, v in hits]
    if all(got):
        full += 1
        full_items.append(p)
    elif any(got):
        part += 1
    else:
        none += 1
        none_items.append((p, hits))
print(f'text assets={total} full-reuse={full} partial={part} none={none}')
for p, h in none_items[:40]:
    print('  NONE', p, '|', h[0][1][:60])
