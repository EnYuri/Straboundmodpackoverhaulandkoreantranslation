import sys, io, json, re, os, glob
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

NEEDLES = ['effigiumhammer.activeitem', 'fu_alienwood_flowerpot.object',
           'leather', 'v-toxicbubblespawnerspawner.object', 'modernshingle']

for p in sorted(glob.glob(r"E:\My Games\steamapps\common\Starbound\mods\*.pak")):
    try:
        pk = Pak(p)
    except Exception:
        continue
    for k in pk.index:
        kl = k.lower()
        if 'effigiumhammer.activeitem' in kl or 'fu_alienwood_flowerpot.object' in kl or 'toxicbubblespawnerspawner.object' in kl or 'modernshingle' in kl:
            print('###', os.path.basename(p), k)
            raw = pk.read(k).decode('utf-8', errors='replace')
            for m in re.finditer(r'"(description|shortdescription|novakidDescription|novakiddescription)"\s*:\s*"((?:[^"\\]|\\.)*)"', raw):
                print('  ', m.group(1), ':', m.group(2)[:160].replace('\\n', '|'))
