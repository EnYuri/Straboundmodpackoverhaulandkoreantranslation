import io, sys, json
sys.stdout.reconfigure(encoding='utf-8')
LIT = bytes([0x5C, 0x6E])          # backslash + n
for fn in ['gic_ko_01.tsv','gic_ko_02.tsv','gic_ko_03.tsv']:
    raw = open('data/'+fn,'rb').read()
    rows = [l for l in raw.decode('utf-8').splitlines() if l.strip()]
    lit_rows = sum(1 for l in rows if '\\n' in l)
    print(fn, 'rows:', len(rows), 'literal-backslash-n bytes:', raw.count(LIT), 'rows w/ lit:', lit_rows)
# deployed: count GiC patch replace-values containing literal backslash-n vs real nl
sys.path.insert(0, r'E:\My Games\steamapps\common\Starbound')
from pak import Pak
tr = Pak(r'E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak')
def flat(o):
    if isinstance(o, dict): yield o
    elif isinstance(o, list):
        for e in o: yield from flat(e)
lit = reall = 0
for name in tr.index:
    if 'gic_' not in name and '/items/' not in name: continue
    if not name.endswith('.patch'): continue
    try: ops = json.loads(tr.read(name))
    except Exception: continue
    for o in flat(ops):
        if o.get('op') == 'replace' and isinstance(o.get('value'), str):
            v = o['value']
            if '\\n' in v: lit += 1
            elif '\n' in v: reall += 1
print('gic patches: literal-bsn values:', lit, '| real-nl values:', reall)
