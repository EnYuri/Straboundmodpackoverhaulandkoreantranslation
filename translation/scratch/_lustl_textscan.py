# Extract text fields from Lustlings' uncovered "modifyed" item files and match
# them against known EN->KO pairs so existing translations can be reused.
import sys, io, json, re, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
LK = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"
PAIRS = r"data\pak_pairs.tsv"

FIELDS = ('shortdescription', 'description', 'title', 'label', 'subtitle',
          'caption', 'text', 'name', 'floranDescription', 'novakidDescription',
          'avianDescription', 'apexDescription', 'glitchDescription',
          'humanDescription', 'hylotlDescription')


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


def walk(d, path, hits):
    if isinstance(d, dict):
        for k, v in d.items():
            if isinstance(v, str) and re.search(r'[a-zA-Z]{4,}', v):
                hits.append((path + '/' + k, v))
            else:
                walk(v, path + '/' + k, hits)
    elif isinstance(d, list):
        for i, v in enumerate(d):
            walk(v, path + '/' + str(i), hits)


tr = Pak(TR)
ti = set(tr.index)
lk = Pak(LK)

# EN->KO map from pak_pairs for reuse
csv.field_size_limit(10 ** 8)
en2ko = {}
with open(PAIRS, encoding='utf-8-sig') as f:
    for r in csv.reader(f, delimiter='\t'):
        if len(r) >= 4:
            en2ko.setdefault(r[2], r[3])

uncov = []
for p in lk.index:
    ext = p.rsplit('.', 1)[-1] if '.' in p else ''
    if ext in ('patch', 'png', 'frames', 'ogg', 'wav', 'lua', 'json'):
        continue
    if 'lustl' not in p.lower():
        continue
    if p + '.patch' in ti or p in ti:
        continue
    uncov.append(p)

have_text = 0
reuse_full = 0
reuse_part = 0
new = []
field_counts = {}
for p in uncov:
    try:
        doc = parse_sb(lk.read(p))
    except Exception:
        continue
    hits = []
    walk(doc, '', hits)
    hits = [(pp, v) for pp, v in hits
            if any(pp.endswith('/' + f) or '/' + f + '/' in pp or pp.endswith(f) for f in FIELDS)]
    if not hits:
        continue
    have_text += 1
    matched = sum(1 for _, v in hits if v in en2ko)
    for pp, _ in hits:
        f = pp.rsplit('/', 1)[-1]
        field_counts[f] = field_counts.get(f, 0) + 1
    if matched == len(hits):
        reuse_full += 1
    elif matched:
        reuse_part += 1
        new.append((p, hits))
    else:
        new.append((p, hits))

print(f'uncovered assets={len(uncov)} with-text={have_text} all-fields-known={reuse_full} partial={reuse_part} none={have_text - reuse_full - reuse_part}')
print('field dist:', field_counts)
print('\n-- assets needing new translation (sample):')
for p, hits in new[:30]:
    print(' ', p)
    for pp, v in hits[:4]:
        print('    ', pp, repr(v[:90]))
print('total needing new translation:', len(new))
