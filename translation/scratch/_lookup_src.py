import sys, io, json, re, os
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
from pak import Pak

pk = Pak(r"E:\My Games\steamapps\common\Starbound\mods\Galaxy_in_Conflict_contents_2754886445.pak")
raw = pk.read('/items/MEDICAL/gic_burnteffigy.consumable').decode('utf-8', errors='replace')
m = re.search(r'"description"\s*:\s*"((?:[^"\\]|\\.)*)"', raw)
print('burnteffigy EN:', m.group(1)[:600] if m else 'notfound')
print()

for p, path in [
    (r"E:\My Games\steamapps\common\Starbound\mods\FrackinUniverse_contents_729480149.pak", '/quests/outpost/mechunlock.questtemplate.patch'),
    (r"E:\My Games\steamapps\common\Starbound\mods\FU_KO_contents_3166424163.pak", '/quests/outpost/mechunlock.questtemplate.patch'),
    (r"E:\My Games\steamapps\common\Starbound\mods\-9998_trans_sbkor_0.98_structfix.pak", '/quests/outpost/mechunlock.questtemplate.patch'),
]:
    pk2 = Pak(p)
    raw2 = pk2.read(path).decode('utf-8', errors='replace')
    print('###', os.path.basename(p))
    for m2 in re.finditer(r'"(?:value|completionText)"\s*:\s*"((?:[^"\\]|\\.)*)"', raw2):
        s = m2.group(1)
        if len(s) > 80:
            print(' :', s[:400].replace('\\n', '|'))
    print()
