import csv, sys, io, json, re
from collections import defaultdict

csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

# Scoped value replacements: (asset, pointer) -> {exact old value: new value}
SCOPED = {
    ('/items/MATERIALS/brick.matitem.patch', '/description'): {
        'Small but perfectly formed bricks made from clay.\n^orange;분쇄 가능^reset;.':
        '찰흙으로 만든 작지만 완벽한 형태의 벽돌입니다.\n^orange;분쇄 가능^reset;.',
    },
}

# Substring replacements applied only to specific (asset, pointer) rows
SUBS = {
    ('/ffs_weapons/ffs_0_cultist/ffs_frag_rgo/ffs_frag_rgo_cultist.activeitem.patch', '/description'):
        [('^red;If a gunner is too close to the target, it\'ll be very dangerous.',
          '^red;사수가 목표물에 너무 가까우면 매우 위험합니다.')],
    ('/items/MEDICAL/gic_burnteffigy.consumable.patch', '/description'):
        [('^white;/objects/biome/gnome/smallhouse4/smallhouse4.object.patch', '^white;')],
    ('/codex/thelusian/thelusian6.codex.patch', '/contentPages/0'):
        [("X'ians는", "짜'이족은")],
    ('/quests/outpost/mechunlock.questtemplate.patch', '/completionText'):
        [('^green;spare resources^white;를', '^green;예비 자원^white;을'),
         ('^orange;Engineering^reset; 을', '^orange;엔지니어링^reset;을'),
         ('^orange;mech 조립 스테이션^white;를', '^orange;메카 조립 스테이션^white;을')],
}

def fix(asset, pointer, ko):
    if (asset, pointer) in SCOPED:
        m = SCOPED[(asset, pointer)]
        if ko in m:
            return m[ko]
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
