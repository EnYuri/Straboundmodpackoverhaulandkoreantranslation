# -*- coding: utf-8 -*-
# Apply legacy_translate.tsv KO map to deployed translation pak.
# For each (asset, ptr, en) in legacy_apply.tsv add [test, replace] group ops
# into '<asset>.patch' inside zz_translation_female.pak (creating the file when
# absent). For .patch-source rows, resolve the provider patch op's target path
# on the base asset and emit ops into a patch file with the same asset name.
import sys, io, os, re, json, csv, glob, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r'E:/My Games/steamapps/common/Starbound')
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pak, sbjson
from _legacy_ko_map import MAP

MODS = r'E:/My Games/steamapps/common/Starbound/mods'
TR = os.path.join(MODS, 'zz_translation_female.pak')
DRY = '--apply' not in sys.argv

# ---------- build EN->KO ----------
KO = dict(MAP)
# NYAN marquee: translate letters, keep color tags
NYAN_KEY = None
for r in csv.DictReader(open(r'data/legacy_translate.tsv', encoding='utf-8'), delimiter='\t'):
    if r['en'].startswith('^red;N^orange;'):
        NYAN_KEY = r['en']
        KO[NYAN_KEY] = re.sub(r'(?<=;)[NYA](?=[\^ ])', '냐', r['en'])
# glyph-art string: leave untranslated
SKIP = set()
for r in csv.DictReader(open(r'data/legacy_translate.tsv', encoding='utf-8'), delimiter='\t'):
    if '\ue000' in r['en'] or re.search(r'[\ue000-\uf8ff]', r['en']):
        SKIP.add(r['en'])

unmapped = [r['en'] for r in csv.DictReader(open(r'data/legacy_translate.tsv', encoding='utf-8'), delimiter='\t')
            if r['en'] not in KO and r['en'] not in SKIP]
print('KO map:', len(KO), '| unmapped:', len(unmapped), '| skipped-glyph:', len(SKIP))
for m in unmapped[:10]: print('  UNMAPPED', repr(m[:80]))
if unmapped: sys.exit(1)

# ---------- provider patch resolver for .patch assets ----------
paks = {os.path.basename(p): p for p in glob.glob(MODS + '/*.pak')}
miss = list(csv.DictReader(open(r'data/legacy_missing.tsv', encoding='utf-8-sig'), delimiter='\t'))
# asset -> list of provider paks (from missing rows)
prov_of = {}
for r in miss:
    if r['assetPath'].endswith('.patch'):
        prov_of.setdefault(r['assetPath'], []).append(r['pak'])

def flatops(doc):
    out = []
    def rec(o):
        if isinstance(o, list):
            for x in o: rec(x)
        elif isinstance(o, dict):
            out.append(o)
    rec(doc)
    return out

patch_cache = {}
def resolve_patch_ptr(asset, ptr, en):
    """ptr like /N[/M...]/value[/sub] -> (target_base_path, actual_test_value)"""
    if asset not in patch_cache:
        ops = []
        for pk in prov_of.get(asset, []):
            if pk not in paks: continue
            try:
                raw = pak.Pak(paks[pk]).read(asset).decode('utf-8')
            except Exception:
                continue
            ops.append((pk, flatops(sbjson.parse_sb(raw))))
        patch_cache[asset] = ops
    segs = [s for s in ptr.split('/') if s != '']
    vi = segs.index('value')
    idxs = [int(s) for s in segs[:vi]]
    sub = segs[vi+1:]
    for pk, ops in patch_cache[asset]:
        node = ops
        try:
            for i in idxs: node = node[i]
        except Exception:
            continue
        if not isinstance(node, dict) or 'path' not in node: continue
        val = node.get('value')
        for s in sub:
            val = val[int(s)] if isinstance(val, list) else val[s]
        if val == en:
            tgt = node['path'] + ''.join('/' + s for s in sub)
            return tgt
    return None

# ---------- load rows, resolve ----------
rows = list(csv.DictReader(open(r'data/legacy_apply.tsv', encoding='utf-8'), delimiter='\t'))
pk = pak.Pak(TR)
byfile = {}
unresolved = []
for r in rows:
    en, asset, ptr = r['en'], r['asset'], r['ptr']
    if en in SKIP: continue
    ko = KO.get(en)
    if ko is None:
        unresolved.append(('NOKO', asset, ptr, en[:60])); continue
    if asset.endswith('.patch'):
        tgt = resolve_patch_ptr(asset, ptr, en)
        if tgt is None:
            unresolved.append(('NOPTR', asset, ptr, en[:60])); continue
        byfile.setdefault(asset, []).append((tgt, en, ko))
    else:
        byfile.setdefault(asset + '.patch', []).append((ptr, en, ko))

print('patch files to touch:', len(byfile), '| unresolved:', len(unresolved))
for u in unresolved[:15]: print('  ', u)
if unresolved and '--force' not in sys.argv: sys.exit(1)

overrides = {}
new_files = 0
for fn, items in sorted(byfile.items()):
    if fn in pk.index:
        raw = pk.read(fn).decode('utf-8')
        try:
            doc = json.loads(raw)
        except Exception:
            doc = sbjson.parse_sb(raw)
        if not isinstance(doc, list): doc = [doc]
    else:
        doc = []
        new_files += 1
    for ptr, en, ko in items:
        doc.append([{"op": "test", "path": ptr, "value": en},
                    {"op": "replace", "path": ptr, "value": ko}])
    overrides[fn] = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

print('ops to add:', sum(len(v) for v in byfile.values()), '| new patch files:', new_files)
if DRY:
    print('DRY RUN'); sys.exit(0)

import pak_writer
staged = TR + '.staged'
pak_writer.write_pak(staged, TR, overrides)
for i in range(240):
    try:
        os.replace(staged, TR); break
    except PermissionError:
        time.sleep(5)
else:
    print('LOCKED - staged pak left at', staged); sys.exit(2)
print('applied:', len(overrides), 'patch files')
