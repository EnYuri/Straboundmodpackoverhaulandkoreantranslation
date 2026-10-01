# verify: every changed race-description field preserved tags/placeholders/newlines
import json, re, sys, io
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
from pak import Pak

OLD = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak.bak_racepolite"
NEW = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

TAG = re.compile(r'\^[^;]{1,20};')
PH = re.compile(r'\{[^}]*\}|%s|%[ds]|<[^>]+>')

def sigs(t):
    return (TAG.findall(t), PH.findall(t), t.count('\n'))

def walk(node, out=None):
    if out is None:
        out = []
    stack = [node]
    while stack:
        it = stack.pop()
        if isinstance(it, list):
            stack.extend(it)
        elif isinstance(it, dict):
            if it.get('op') == 'replace' and isinstance(it.get('value'), str):
                out.append((it.get('path', ''), it['value']))
            for k, v in it.items():
                if isinstance(v, str) and re.search(r'(\w+)[Dd]escription$', k):
                    out.append(('/' + k, v))
                elif isinstance(v, (dict, list)):
                    stack.append(v)
    return out

pk_old, pk_new = Pak(OLD), Pak(NEW)
bad = 0
changed_assets = 0
total = 0
for asset in pk_new.index.keys():
    if asset not in pk_old.index:
        continue
    try:
        d_old = json.loads(pk_old.read(asset))
        d_new = json.loads(pk_new.read(asset))
    except Exception:
        continue
    m_old = {}
    for p, v in walk(d_old):
        m_old.setdefault(p, []).append(v)
    diffs = []
    for p, v in walk(d_new):
        if p in m_old and v not in m_old[p]:
            diffs.append((p, v))
    if diffs:
        changed_assets += 1
        for p, v in diffs:
            # find original counterpart: first old value at same path not equal
            olds = m_old[p]
            for o in olds:
                if o != v:
                    total += 1
                    if sigs(o) != sigs(v):
                        bad += 1
                        print('SIG-DIFF', asset, p)
                        print('  old:', o[:120].replace('\n', ' / '))
                        print('  new:', v[:120].replace('\n', ' / '))
                    break
print('changed fields:', total, 'changed assets:', changed_assets, 'signature mismatches:', bad)
