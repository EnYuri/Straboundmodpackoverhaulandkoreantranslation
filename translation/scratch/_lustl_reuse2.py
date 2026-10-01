# Reuse strategy v2: for each uncovered lustling modifyed item, locate the
# ORIGINAL item translation by basename: any patch */<basename>.patch in
# sbkor or zz_translation_female whose test value matches (or basename only
# if single candidate). Output coverage stats and a reuse manifest.
import sys, io, json, re, csv, glob, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
SBKOR = r"E:\My Games\steamapps\common\Starbound\mods\-9998_trans_sbkor_0.98_structfix.pak"
LK = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"

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
    def rec(x):
        if isinstance(x, dict):
            return [x]
        out = []
        for y in x:
            out.extend(rec(y))
        return out
    return rec(json.loads(raw))


# index: basename -> {field: [(en_test, ko, patch_path)]}
idx = {}
for src in (SBKOR, TR):
    pk = Pak(src)
    for p in pk.index:
        if not p.endswith('.patch'):
            continue
        base = p[:-6]
        bn = base.rsplit('/', 1)[-1]
        try:
            ops = flat_ops(pk.read(p).decode('utf-8'))
        except Exception:
            continue
        for i, o in enumerate(ops):
            fld = o.get('path', '').lstrip('/')
            if fld in FIELDS and o.get('op') == 'replace' and isinstance(o.get('value'), str):
                en = None
                if i > 0 and ops[i - 1].get('op') == 'test' and ops[i - 1].get('path') == o['path']:
                    en = ops[i - 1].get('value')
                idx.setdefault((bn, fld), []).append((en, o['value'], p))

print('basename index entries:', len(idx))

tr = Pak(TR)
ti = set(tr.index)
lk = Pak(LK)
total = full = part = none = 0
manifest = []
for p in sorted(lk.index):
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
    bn = p.rsplit('/', 1)[-1]
    got = {}
    for f in FIELDS:
        v = doc.get(f)
        if isinstance(v, str) and re.search(r'[a-zA-Z]{4,}', v):
            cands = idx.get((bn, f), [])
            ko = None
            for en, k, pp in cands:
                if en == v:
                    ko = k
                    break
            if ko is None and cands:
                ko = cands[0][1]
            if ko:
                got[f] = (v, ko)
    if not got:
        continue
    total += 1
    fields_present = sum(1 for f in FIELDS
                         if isinstance(doc.get(f), str) and re.search(r'[a-zA-Z]{4,}', doc[f]))
    if len(got) == fields_present:
        full += 1
        manifest.append((p, got))
    else:
        part += 1
        manifest.append((p, got))
none_assets = 0
for p in sorted(lk.index):
    ext = p.rsplit('.', 1)[-1] if '.' in p else ''
    if ext in ('patch', 'png', 'frames', 'ogg', 'wav', 'lua', 'json') or 'lustl' not in p.lower():
        continue
    if p + '.patch' in ti or p in ti:
        continue
    try:
        doc = parse_sb(lk.read(p))
    except Exception:
        continue
    if any(isinstance(doc.get(f), str) and re.search(r'[a-zA-Z]{4,}', doc[f]) for f in FIELDS):
        if not any(k == p for k, _ in manifest):
            none_assets += 1
print(f'text assets with reuse candidates: full={full} partial={part} no-candidate={none_assets}')
print('manifest entries:', len(manifest))
for p, g in manifest[:10]:
    print(' ', p, '->', {k: v[1][:40] for k, v in g.items()})
