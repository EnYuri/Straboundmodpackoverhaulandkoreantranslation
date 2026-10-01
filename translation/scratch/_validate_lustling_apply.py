# Validate whether the translation pak's patch test-ops still match the current
# Lustlings 1.2.9 asset bases. Also inspect the mod's own patch files for
# text-bearing ops uncovered by the translation pak.
import sys, io, json, re
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
LK = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"


def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out = []
    ins = False
    i = 0
    while i < len(s):
        c = s[i]
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        if ins and c == '\r':
            out.append('\\r')
        elif ins and c == '\n':
            out.append('\\n')
        else:
            out.append(c)
        i += 1
    s = ''.join(out)
    s = re.sub(r',(\s*[}\]])', r'\1', s)
    return json.loads(s)


def getsegs(p):
    return [x.replace('~1', '/').replace('~0', '~') for x in p.split('/') if x]


def resolve(d, segs):
    cur = d
    for s in segs:
        cur = cur[int(s)] if isinstance(cur, list) else cur[s]
    return cur


def deq(a, b):
    if isinstance(b, dict) and isinstance(a, dict):
        return all(k in a and deq(a[k], v) for k, v in b.items())
    if isinstance(b, list) and isinstance(a, list):
        return len(a) >= len(b) and all(deq(a[i], b[i]) for i in range(len(b)))
    return a == b


tr = Pak(TR)
ti = set(tr.index)
lk = Pak(LK)

fail = []
ok = 0
badbase = []
for pp in ti:
    if not pp.endswith('.patch'):
        continue
    tgt = pp[:-6]
    if tgt not in lk.index:
        continue
    try:
        base = parse_sb(lk.read(tgt))
    except Exception as e:
        badbase.append((tgt, str(e)[:90]))
        continue
    try:
        ops = json.loads(tr.read(pp).decode('utf-8'))
    except Exception:
        continue
    flat = [o for x in ops for o in (x if isinstance(x, list) else [x])]
    bad = []
    for op in flat:
        if op.get('op') == 'test':
            try:
                if not deq(resolve(base, getsegs(op['path'])), op.get('value')):
                    bad.append(op['path'])
            except Exception:
                bad.append('MISS ' + op['path'])
    if bad:
        fail.append((pp, len(bad), bad[:3]))
    else:
        ok += 1

print('translation patches on lustling assets: ok', ok, '| test-fail', len(fail), '| unparseable base', len(badbase))
for p, n, b in fail:
    print(' FAIL', p, n, b)
for p, e in badbase:
    print(' UNPARSEABLE', p, e)

# mod's own .patch files not mirrored in translation: do they carry text ops?
TEXT_FIELDS = ('description', 'shortdescription', 'title', 'label', 'value',
               'subtitle', 'caption', 'dialog', 'text', 'name', 'rarity')
uncov = []
for pp in lk.index:
    if pp.endswith('.patch') and pp not in ti:
        try:
            ops = json.loads(lk.read(pp).decode('utf-8'))
        except Exception:
            continue
        flat = [o for x in ops for o in (x if isinstance(x, list) else [x])]
        texty = [o for o in flat if isinstance(o.get('value'), str)
                 and any(f in o.get('path', '') for f in TEXT_FIELDS)
                 and re.search(r'[a-zA-Z]{4}', o['value'])]
        if texty:
            uncov.append((pp, len(texty)))
print('\nlustling own patch files w/ text ops not covered by translation:', len(uncov))
for p, n in uncov[:50]:
    print(' ', p, n)
