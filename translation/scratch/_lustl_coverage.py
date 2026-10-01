# Scan ALL mods paks for lustl*-related assets and check translation coverage.
# Coverage rule: real asset X needs translation patch X.patch; a pak's own
# .patch files need a same-path patch to merge after them.
import sys, io, json, re, glob, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
tr = Pak(TR)
ti = set(tr.index)

TEXT_EXTS = ('npctype', 'codex', 'object', 'config', 'questtemplate', 'species',
             'activeitem', 'consumable', 'item', 'matitem', 'augments', 'legs',
             'chest', 'head', 'back', 'radiomessages', 'itemdescription',
             'tooltip', 'collectable', 'thrownitem', 'particle', 'monsterpart',
             'stagehand', 'statuseffect', 'animation')
TEXT_FIELDS = ('description', 'shortdescription', 'title', 'label', 'subtitle',
               'caption', 'dialog', 'text', 'name', 'floranDescription')

rows = []
for fn in sorted(glob.glob(r"E:\My Games\steamapps\common\Starbound\mods\*.pak")):
    pk = Pak(fn)
    hits = [p for p in pk.index if 'lustl' in p.lower() or 'lustb' in p.lower()]
    if not hits:
        continue
    uncov_real = []
    uncov_textpatch = []
    for p in hits:
        ext = p.rsplit('.', 1)[-1] if '.' in p else ''
        if ext == 'patch':
            if p not in ti:
                # does this own patch carry text ops?
                try:
                    ops = json.loads(pk.read(p).decode('utf-8'))
                except Exception:
                    continue
                flat = [o for x in ops for o in (x if isinstance(x, list) else [x])]
                t = [o for o in flat if isinstance(o.get('value'), str)
                     and any(f in o.get('path', '') for f in TEXT_FIELDS)
                     and re.search(r'[a-zA-Z]{4,}', o['value'])]
                if t:
                    uncov_textpatch.append((p, len(t)))
        elif ext in TEXT_EXTS:
            if p + '.patch' not in ti and p not in ti:
                uncov_real.append(p)
    if hits:
        rows.append((os.path.basename(fn), len(hits), len(uncov_real), uncov_real, len(uncov_textpatch), uncov_textpatch))

for name, tot, nr, rl, np_, pl in rows:
    print(f'{name}: lustl paths={tot} uncovered-real={nr} uncovered-textpatch={np_}')
    for p in rl[:15]:
        print('   REAL', p)
    for p, n in pl[:15]:
        print('   PATCH-TEXT', p, n)
