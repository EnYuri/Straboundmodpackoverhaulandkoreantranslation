import csv, sys, io, json, re
from collections import defaultdict

csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

# Substring replacements applied only to specific (asset, pointer) rows.
# Residual polite endings in race-description fields missed by fix_race_polite.
SUBS = {
    ('/objects/CRAFTING/atprk_esupgradestationsmall/atprk_esupgradestationsmall.object.patch', '/humanDescription'):
        [('일을 합시다', '일을 하자')],
    ('/objects/generic/upgradestation/upgradestation.object.patch', '/humanDescription'):
        [('일을 합시다', '일을 하자')],
    ('/objects/FARMABLES/phasefruit/phasefruitseed.object.patch', '/humanDescription'):
        [('한번 시도해 봅시다!', '한번 시도해 보자!')],
    ('/objects/FARMABLES/plasmango/plasmangoseed.object.patch', '/glitchDescription'):
        [('망고처럼 보입니까, 아니면 망고가 플라즈마고처럼 보입니까?',
          '망고처럼 보이는가, 아니면 망고가 플라스망고처럼 보이는가?')],
    ('/objects/FARMABLES/plasmango/wildplasmangoseed.object.patch', '/glitchDescription'):
        [('망고처럼 보입니까, 아니면 망고가 플라즈마고처럼 보입니까?',
          '망고처럼 보이는가, 아니면 망고가 플라스망고처럼 보이는가?')],
    ('/objects/flowerpots/blueberrybushplanter/blueberrybushplanter.object.patch', '/hylotlDescription'):
        [('신기한 과일입니까', '신기한 과일인가')],
    ('/objects/ship/elduuteleporter/elduuteleporter.object.patch', '/novakidDescription'):
        [('한번 시승해 봅시다!', '한번 시승해 보자!')],
    ('/objects/ship/xiteleporter/byosxiteleporter.object.patch', '/novakidDescription'):
        [('한 번 사용해 봅시다!', '한 번 사용해 보자!')],
    ('/objects/trink/container/trinkweaponchest/trinkweaponchest.object.patch', '/novakidDescription'):
        [('얼른 안을 좀 봅시다!', '얼른 안을 좀 보자!')],
    ('/objects/walldecor/geoposter/geoposter.object.patch', '/avianDescription'):
        [('이 모든 모양은 무엇입니까?', '이 모든 모양은 무엇이지?')],
}

def fix(asset, pointer, ko):
    if (asset, pointer) in SUBS:
        for a, b in SUBS[(asset, pointer)]:
            ko = ko.replace(a, b)
    return ko

def main():
    changes = defaultdict(dict)
    for row in csv.DictReader(open(ROOT + r'\pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
        ko = row['korean']
        new = fix(row['asset'], row['pointer'], ko)
        if new != ko:
            changes[(row['asset'], row['pointer'])][ko] = new
    n = sum(len(v) for v in changes.values())
    print('rows to change:', n, 'in', len(changes), 'pointers')

    pk = Pak(TARGET)
    overrides = {}
    changed = 0
    for asset in {a for a, _ in changes}:
        doc = json.loads(pk.read(asset))
        stack = list(doc)
        found = False
        while stack:
            it = stack.pop()
            if isinstance(it, list):
                stack.extend(it)
            elif isinstance(it, dict) and it.get('op') == 'replace' and isinstance(it.get('value'), str):
                rep = changes.get((asset, it.get('path')), {}).get(it.get('value'))
                if rep is not None:
                    it['value'] = rep
                    changed += 1
                    found = True
        if found:
            overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
    print('changed', changed, 'fields; expected', n, '; assets untouched', len(changes) - len(overrides))
    del pk
    print('wrote pak; entries', write_pak(TARGET, TARGET, overrides))

if __name__ == '__main__':
    main()
