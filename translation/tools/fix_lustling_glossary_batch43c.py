# Batch43c: align new Lustling armor translations with fixed glossary terms.
# Lustling -> 러스틀링, Violium -> 바이올륨, Miniknog -> 미니크녹 (지식부 is
# the old sbkor rendering; pak standard is 미니크녹).
import sys, io, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
RULES = [('러슬링', '러스틀링'), ('바이올리움', '바이올륨'), ('지식부', '미니크녹')]

tr = Pak(TR)
overrides = {}
changed = 0
for p in tr.index:
    if '/lustling/' not in p or not p.endswith('.patch'):
        continue
    try:
        ops = json.loads(tr.read(p).decode('utf-8'))
    except Exception:
        continue
    hit = [False]

    def walk(o):
        if isinstance(o, list):
            for x in o:
                walk(x)
        elif isinstance(o, dict):
            v = o.get('value')
            if o.get('op') == 'replace' and isinstance(v, str):
                nv = v
                for a, b in RULES:
                    nv = nv.replace(a, b)
                if nv != v:
                    o['value'] = nv
                    hit[0] = True

    walk(ops)
    if hit[0]:
        overrides[p] = json.dumps(ops, ensure_ascii=False, indent=2).encode('utf-8')
        changed += 1
print('entries to rewrite:', changed)
if '--apply' in sys.argv and overrides:
    print('wrote pak; entries', write_pak(TR, TR, overrides))
else:
    print('dry run — pass --apply to write')
