# Batch43: translate Lustlings' uncovered "modifyed" armor/item variants.
# Phase A (this script): reuse — for every uncovered lustling item, look up the
# original item's KO by basename in sbkor/zz_translation_female and emit a
# .patch entry whose test values are the lustling item's CURRENT EN strings.
# Leftover items (no basename candidate) are written to
# data/lustling_untranslated.tsv for manual translation (phase B).
import sys, io, json, re, csv
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
SBKOR = r"E:\My Games\steamapps\common\Starbound\mods\-9998_trans_sbkor_0.98_structfix.pak"
LK = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"
OUT_TSV = r"data\lustling_untranslated.tsv"

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


# basename -> field -> [(en_test_or_None, ko, patch_path)]
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
                if i > 0 and ops[i - 1].get('op') == 'test' \
                        and ops[i - 1].get('path') == o['path']:
                    en = ops[i - 1].get('value')
                idx.setdefault((bn, fld), []).append((en, o['value'], p))

tr = Pak(TR)
ti = set(tr.index)
lk = Pak(LK)

overrides = {}
reused = 0
leftover = []
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
    fields = {}
    for f in FIELDS:
        v = doc.get(f)
        if isinstance(v, str) and re.search(r'[a-zA-Z]{4,}', v):
            fields[f] = v
    if not fields:
        continue
    # try exact basename, then female-variant fallback (Xf.ext -> X.ext)
    bnames = [bn]
    stem, dot, e = bn.rpartition('.')
    if stem.endswith('f') and len(stem) > 3:
        bnames.append(stem[:-1] + '.' + e)
    ko_map = {}
    for f, v in fields.items():
        for cand in bnames:
            cands = idx.get((cand, f), [])
            ko = None
            for en, k, _ in cands:
                if en == v:
                    ko = k
                    break
            if ko is None and cands:
                ko = cands[0][1]
            if ko:
                ko_map[f] = (v, ko)
                break
    if len(ko_map) == len(fields):
        ops = [[{"op": "test", "path": "/" + f, "value": v},
                {"op": "replace", "path": "/" + f, "value": ko}]
               for f, (v, ko) in ko_map.items()]
        overrides[p + '.patch'] = json.dumps(ops, ensure_ascii=False, indent=2).encode('utf-8')
        reused += 1
    else:
        leftover.append((p, fields, ko_map))

print('reused:', reused, 'leftover:', len(leftover))
with open(OUT_TSV, 'w', encoding='utf-8', newline='') as f:
    w = csv.writer(f, delimiter='\t')
    w.writerow(['asset', 'field', 'en', 'partial_ko'])
    for p, fields, ko_map in leftover:
        for f, v in fields.items():
            w.writerow([p, f, v, ko_map.get(f, ('', ''))[1]])
print('wrote', OUT_TSV)

if '--apply' in sys.argv and overrides:
    print('wrote pak; entries', write_pak(TR, TR, overrides))
elif overrides:
    print('dry run — pass --apply to write', len(overrides), 'patches')
