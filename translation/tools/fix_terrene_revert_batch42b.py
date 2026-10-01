# -*- coding: utf-8 -*-
# Batch42b: glossary correction — the registered standard is the vanilla
# rendering "행성 X" (Terrene Protectorate -> 행성 보호국), so all
# 테렌/테레네 faction-name variants unify to the 행성 scheme instead of
# the transliteration introduced in batch42.
import sys, io, json, re

sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak
from pak_writer import write_pak

TARGET = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

SUBS = [
    ('테레네 보호국', '행성 보호국'),
    ('테레네 피스키퍼', '행성 피스키퍼'),
    ('테레네 가디언즈', '행성 가디언즈'),
    ('테레네 선거단', '행성 선거단'),
    ('테레네 가드', '행성 수호대'),
    ('테레네 보호령', '행성 보호국'),
    ('"테레네" 법', '"행성" 법'),
    ('테레네 유토피아', '행성 유토피아'),
    ('테레네에 직접적인', '행성 보호국에 직접적인'),
]


def main():
    pk = Pak(TARGET)
    overrides = {}
    total = 0
    counts = {a: 0 for a, _ in SUBS}
    for asset in pk.index:
        if not asset.endswith('.patch'):
            continue
        try:
            doc = json.loads(pk.read(asset))
        except Exception:
            continue
        if not isinstance(doc, list):
            continue
        touched = False
        stack = list(doc)
        while stack:
            it = stack.pop()
            if isinstance(it, list):
                stack.extend(it)
                continue
            if not (isinstance(it, dict) and it.get('op') in ('replace', 'add')
                    and isinstance(it.get('value'), str)):
                continue
            v = it['value']
            nv = v
            for a, b in SUBS:
                if a in nv:
                    counts[a] += nv.count(a)
                    nv = nv.replace(a, b)
            if nv != v:
                it['value'] = nv
                touched = True
                total += 1
        if touched:
            overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
    for a, c in counts.items():
        print(f'{c:4d}  {a}')
    print('ops changed:', total, '| assets:', len(overrides))
    pk.f.close()
    if '--apply' in sys.argv:
        print('wrote pak; entries', write_pak(TARGET, TARGET, overrides))
    else:
        print('dry run — pass --apply to write')


if __name__ == '__main__':
    main()
