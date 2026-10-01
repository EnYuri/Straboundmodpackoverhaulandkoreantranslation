import sys, io, re, glob, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

for p in sorted(glob.glob(r"E:\My Games\steamapps\common\Starbound\mods\*.pak")):
    try:
        pk = Pak(p)
    except Exception:
        continue
    for k in pk.index:
        if 'items.config' in k and 'scanner' in k.lower():
            raw = pk.read(k).decode('utf-8', errors='replace')
            for m in re.finditer(r'"longdescription"\s*:\s*"((?:[^"\\]|\\.)*)"', raw):
                s = m.group(1)
                if 'terrible' in s.lower() or 'horrible' in s.lower() or 'creepy' in s.lower():
                    print(os.path.basename(p), k)
                    print('  ', s[:200])
                    print()
