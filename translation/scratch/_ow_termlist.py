import sys, re, json
sys.path.insert(0, r'E:/My Games/steamapps/common/Starbound')
import pak

p = pak.Pak(r'E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak')
o = open('scratch/_ow_terms2.txt', 'w', encoding='utf-8')
targets = ['DEPLOYMENT ORDER', 'BUILD ORDER', 'Infantry Summons', 'Suppression',
           'Woodlands', 'Spell Catalyst', 'magirocket', 'Magisight', 'SET BONUS',
           'Satushio', 'War Fairy', 'Hourai', 'Lunarian', 'Daitengu', 'Bunbunmaru']
rx = re.compile(r'"op"\s*:\s*"test"\s*,\s*"path"\s*:\s*"([^"]+)"\s*,\s*"value"\s*:\s*"((?:[^"\\]|\\.)*)"')
found = set()
for name in sorted(p.index):
    if not name.endswith('.patch'):
        continue
    try:
        s = p.read(name).decode('utf-8')
    except Exception:
        continue
    for m in rx.finditer(s):
        try:
            en = json.loads('"' + m.group(2) + '"')
        except Exception:
            continue
        for t in list(targets):
            if t.lower() in en.lower() and len(en) < 400:
                tail = s[m.end():m.end() + 3000]
                mm = re.search(r'"op"\s*:\s*"replace"[^}]*?"value"\s*:\s*"((?:[^"\\]|\\.)*)"', tail)
                if mm:
                    try:
                        ko = json.loads('"' + mm.group(1) + '"')
                    except Exception:
                        ko = ''
                    o.write('[%s] %s\nEN: %s\nKO: %s\n\n' % (t, name, en[:350], ko[:350]))
                    found.add(t)
                    targets.remove(t)
                break
o.close()
print('found:', len(found))
