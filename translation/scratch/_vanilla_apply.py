"""Apply vanilla (packed.pak) translations: same logic as untrans_batch.apply
but resolves the provider to assets/packed.pak."""
import sys, io, os, re, json, csv
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r'E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools')
sys.path.insert(0, r'E:\My Games\steamapps\common\Starbound\translation\modpack-overhaul-repo\tools')
from pak import Pak
from pak_writer import write_pak

code = open('tools/untrans_batch.py', encoding='utf-8').read()
ns = {}
exec(compile(code.split("if sys.argv[1] == 'extract'")[0], 'ub', 'exec'), ns)
parse_sb = ns['parse_sb']

SB = r'E:\My Games\steamapps\common\Starbound'
TR = SB + r'\mods\zz_translation_female.pak'
csv.field_size_limit(10 ** 8)

rows = [r for r in csv.reader(open('data/vanilla_work_filled.tsv', encoding='utf-8'), delimiter='\t')]
prov_map = {}
for r in rows[1:]:
    if len(r) >= 4 and r[3].strip():
        prov_map.setdefault(r[0], {})[r[1]] = r[3]

pk = Pak(SB + r'\assets\packed.pak')
overrides = {}
bad = 0
for path, fmap in prov_map.items():
    try:
        doc = parse_sb(pk.read(path))
    except Exception:
        print('  unreadable', path)
        continue
    ops = []
    for fld, ko in fmap.items():
        cur = doc.get(fld)
        if not isinstance(cur, str):
            bad += 1
            continue
        ops.append([{"op": "test", "path": "/" + fld, "value": cur},
                    {"op": "replace", "path": "/" + fld, "value": ko}])
    if ops:
        overrides[path + '.patch'] = json.dumps(ops, ensure_ascii=False, indent=2).encode('utf-8')

# nested title/subtitle ops the flat apply can't reach
NESTED = {
    '/objects/crafting/ironanvil/ironanvil.object': [
        ('/interactData/paneLayoutOverride/windowtitle/title', ' Iron Anvil', '철 모루'),
        ('/interactData/paneLayoutOverride/windowtitle/subtitle', ' ^#b9b5b2;Armour and weapons', '^#b9b5b2;무기와 방어구들')],
    '/objects/crafting/ironcraftingtable/ironcraftingtable.object': [
        ('/interactData/paneLayoutOverride/windowtitle/title', '  Iron Crafting Table', '철 제작대'),
        ('/interactData/paneLayoutOverride/windowtitle/subtitle', '  Heavy duty crafting!', '헤비듀티 제작!')],
    '/objects/ship/researchstation/researchstation.object': [
        ('/interactData/paneLayoutOverride/windowtitle/title', ' Research Station', ' 연구 스테이션'),
        ('/interactData/paneLayoutOverride/windowtitle/subtitle', ' Develop specialised technologies', ' 특화 기술 개발')],
    '/objects/spawner/spawnerstation/spawnerstation.object': [
        ('/interactData/paneLayoutOverride/windowtitle/title', " Employer's Station", ' 고용주 스테이션'),
        ('/interactData/paneLayoutOverride/windowtitle/subtitle', ' Use employment beacons to call in help', ' 고용 비컨으로 지원을 불러오기')],
    '/species/penguin.species': [
        ('/charCreationTooltip/title', 'Penguin', '펭귄'),
        ('/charCreationTooltip/description', 'No idea what to put here', '여기에 뭘 써야 할지 모르겠다')],
}
for path, nops in NESTED.items():
    try:
        doc = parse_sb(pk.read(path))
    except Exception:
        continue
    cur_ops = []
    key = path + '.patch'
    if key in overrides:
        cur_ops = json.loads(overrides[key].decode('utf-8'))
        cur_ops = [o for e in cur_ops for o in (e if isinstance(e, list) else [e])]
    ok = True
    for jpath, en, _ in nops:
        node = doc
        for seg in [s for s in jpath.split('/') if s]:
            node = node.get(seg) if isinstance(node, dict) else node[int(seg)] if isinstance(node, list) and seg.isdigit() else None
        if node != en:
            print('  nested test mismatch', path, jpath, repr(node)[:80])
            ok = False
    if not ok:
        continue
    for jpath, en, ko in nops:
        cur_ops.append({"op": "test", "path": jpath, "value": en})
        cur_ops.append({"op": "replace", "path": jpath, "value": ko})
    overrides[key] = json.dumps(cur_ops, ensure_ascii=False, indent=2).encode('utf-8')
    print('  nested merged', path)

print('patches:', len(overrides), 'fields skipped:', bad)
if '--apply' in sys.argv and overrides:
    print('wrote pak; entries', write_pak(TR, TR, overrides))
else:
    print('dry run')
