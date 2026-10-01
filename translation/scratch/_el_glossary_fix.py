"""Batch47b: fix Elithian glossary violations in deployed pak.
Scoped by EN guard: only ops whose test EN actually contains the term."""
import sys, io, json, re, os
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
sys.stdout.reconfigure(encoding='utf-8')
from pak import Pak
from pak_writer import write_pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
pk = Pak(TR)
changed_files = 0
changed_ops = 0
overrides = {}

def fix(en, ko):
    """Return fixed ko or None."""
    out = ko
    if re.search(r'aegisalt', en, re.I):
        out = out.replace('에이지솔트', '에지솔트')
    if re.search(r'aeginian federal union', en, re.I):
        out = out.replace('에이지니언 연합', '에지족 연방 연합')
    if re.search(r'aegi', en, re.I):
        # standalone Aegi/Aeginian adjective -> 에지/에지족
        out = out.replace('에이지니언', '에지족').replace('에이지', '에지')
    if 'Terrene Protectorate' in en:
        out = re.sub(r'(?<!행성 )보호국', '행성 보호국', out)
    return out if out != ko else None

for name in pk.index:
    if not name.endswith('.patch'):
        continue
    try:
        doc = json.loads(pk.read(name))
    except Exception:
        continue
    mod = False
    def ops_of(node):
        for x in node:
            if isinstance(x, dict) and 'op' in x:
                yield x
            elif isinstance(x, list):
                yield from ops_of(x)
    # group into test/replace sequences
    seq = list(ops_of(doc)) if isinstance(doc, list) else []
    i = 0
    while i < len(seq):
        if seq[i].get('op') == 'test' and i + 1 < len(seq) and seq[i + 1].get('op') == 'replace':
            en, rop = seq[i].get('value'), seq[i + 1]
            ko = rop.get('value')
            if isinstance(en, str) and isinstance(ko, str):
                new = fix(en, ko)
                if new:
                    rop['value'] = new
                    mod = True
                    changed_ops += 1
            i += 2
        else:
            i += 1
    if mod:
        overrides[name] = json.dumps(doc, ensure_ascii=False, indent=2).encode('utf-8')
        changed_files += 1

print('changed ops:', changed_ops, 'files:', changed_files)
if '--apply' in sys.argv and overrides:
    print('entries:', write_pak(TR, TR, overrides))
else:
    print('dry run')
