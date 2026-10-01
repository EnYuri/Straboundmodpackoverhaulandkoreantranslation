import csv, sys, io, json, re
from collections import defaultdict

csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

ROOT = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

# Duplicate-word fixes verified against EN source (or deduped when source absent).
SUBS = {
    ('/items/MATERIALS/modernshingle.matitem.patch', '/novakidDescription'):
        [('멋진 멋진 지붕 타일.', '정말 멋진 지붕 타일.')],
    ('/tiles/materials/modernshingle.material.patch', '/novakidDescription'):
        [('멋진 멋진 지붕 타일.', '정말 멋진 지붕 타일.')],
    ('/items/active/weapons/melee/hammer/effigiumhammer.activeitem.patch', '/description'):
        [('유령처럼 유령처럼.', '유령처럼.')],
    ('/objects/generic/fu_alienwood_flowerpot/fu_alienwood_flowerpot.object.patch', '/shortdescription'):
        [('미니어처 외계인 나무 나무', '미니어처 외계인 나무')],
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
