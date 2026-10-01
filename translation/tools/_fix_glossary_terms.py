# Align user edits to settled glossary terms (user confirmed 방어력/텔레포터/하이로틀).
# Fixes live pak patch values AND the source TSV rows so drift stays clean.
# - '방어:' -> '방어력:' (DEF stat label, rsr_ko_01/02 + flagged pak descriptions)
# - '순간이동기' -> '텔레포터' (gicx_ko_03 row 596 + 3 teleporter object patches)
# - '히로틀' -> '하이로틀' (sat_ko_04 row 619 + valorous/valorousB descriptions)
# - '유탄발사기' -> '유탄 발사기' (lfw_ko + lfw_ko_manual row 85 + AGL-40 patch)
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
APPLY = '--apply' in sys.argv

# --- 1) TSV edits ---
TSV_FIX = [
    (r'data\rsr_ko_01.tsv', '방어:', '방어력:'),
    (r'data\rsr_ko_02.tsv', '방어:', '방어력:'),
    (r'data\gicx_ko_03.tsv', '순간이동기', '텔레포터'),
    (r'data\sat_ko_04.tsv', '히로틀', '하이로틀'),
    (r'data\lfw_ko.tsv', '유탄발사기', '유탄 발사기'),
    (r'data\lfw_ko_manual.tsv', '유탄발사기', '유탄 발사기'),
]
for rel, old, new in TSV_FIX:
    p = BASE + '\\' + rel
    s = io.open(p, encoding='utf-8').read()
    n = s.count(old)
    if n and APPLY:
        io.open(p, 'w', encoding='utf-8', newline='').write(s.replace(old, new))
    print('TSV %s: %s x%d -> %s' % (rel, old, n, new))

# --- 2) pak edits ---
pk = Pak(TR)
def walk_ops(x, out):
    if isinstance(x, dict):
        if 'op' in x: out.append(x)
        else:
            for v in x.values(): walk_ops(v, out)
    elif isinstance(x, list):
        for v in x: walk_ops(v, out)

PK_FIX = [
    # (predicate on patch path, predicate on op, old, new)
    (lambda fn: '/items/armors/GiC IJA Uniforms/' in fn,
     lambda o: o.get('op') == 'replace' and '방어:' in str(o.get('value', '')),
     '방어:', '방어력:'),
    (lambda fn: 'teleporter' in fn.lower() and fn.endswith('.object.patch'),
     lambda o: o.get('op') == 'replace' and str(o.get('value')) == '순간이동기',
     '순간이동기', '텔레포터'),
    (lambda fn: 'saturnvalorous' in fn.lower(),
     lambda o: o.get('op') == 'replace' and '히로틀' in str(o.get('value', '')),
     '히로틀', '하이로틀'),
    (lambda fn: 'giclfw_dcagl40' in fn.lower(),
     lambda o: o.get('op') == 'replace' and '유탄발사기' in str(o.get('value', '')),
     '유탄발사기', '유탄 발사기'),
]
overrides = {}
changed = 0
for fn in pk.index:
    if not fn.endswith('.patch'): continue
    hit = [fx for fx in PK_FIX if fx[0](fn)]
    if not hit: continue
    doc = json.loads(pk.read(fn).decode('utf-8'))
    ops = []
    walk_ops(doc, ops)
    dirty = False
    for pf, pred, old, new in hit:
        for o in ops:
            if pred(o):
                o['value'] = str(o['value']).replace(old, new)
                changed += 1
                dirty = True
                print('PAK %s: %s -> %s' % (fn.rsplit('/', 1)[-1], old, new))
    if dirty:
        overrides[fn] = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

print('pak ops changed:', changed, '| patch files:', len(overrides))
if APPLY and overrides:
    sys.path.insert(0, 'tools')
    from pak_writer import write_pak
    write_pak(TR, TR, overrides)
    print('applied')
