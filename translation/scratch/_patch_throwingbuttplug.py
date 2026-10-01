# Add patch for Lustlings throwingbuttplug (last uncovered asset in that pak).
import sys, json
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

patch = [
    [{"op": "test", "path": "/shortdescription", "value": "Throwing Buttplug"},
     {"op": "replace", "path": "/shortdescription", "value": "투척용 버트플러그"}],
    [{"op": "test", "path": "/description", "value": "Its just a hard Buttplug."},
     {"op": "replace", "path": "/description", "value": "그냥 딱딱한 버트플러그다."}],
]

name = '/items/throwables/throwingbuttplug.thrownitem.patch'
overrides = {name: json.dumps(patch, ensure_ascii=False).encode('utf-8')}
out = TR + '.tmp'
write_pak(out, TR, overrides)
q = Pak(out)
print('entries:', len(q.index))
print(q.read(name).decode('utf-8')[:300])
