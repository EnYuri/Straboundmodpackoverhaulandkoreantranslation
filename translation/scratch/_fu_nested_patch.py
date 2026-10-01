# Add manual patch entries for the 9 nested-pointer fields skipped by
# untrans_batch apply (GUI captions/titles inside paneLayout overrides).
import io
import json
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, "tools")
from pak import Pak  # noqa: E402
from pak_writer import write_pak  # noqa: E402

DEPLOY = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
p = Pak(DEPLOY)

MODS = [
    ("/objects/crafting/extraavianaugments/extraavianaugments.object",
     "/interactData/paneLayoutOverride/windowtitle/title", "Svetlana's Stall", "스베틀라나의 노점"),
    ("/objects/crafting/extraavianaugments/extraavianaugments.object",
     "/interactData/paneLayoutOverride/windowtitle/subtitle", "Repurchase Past Rewards!", "지난 보상 재구매!"),
    ("/objects/crafting/fu_growingtray/fu_growingtray.config",
     "/gui/clear/caption", "Take All", "전부 가져가기"),
    ("/objects/crafting/petpicrepair/petpicrepair.config",
     "/gui/scanButton/caption", "Repair Image", "이미지 복구"),
    ("/objects/crafting/servitorloader/servitorloader.config",
     "/gui/scanButton/caption", "Load Servitor", "서비터 적재"),
    ("/objects/crafting/shrineofsouls/shrineofsouls.object",
     "/interactData/paneLayoutOverride/windowtitle/title", "Shrine of Lost Souls", "잃어버린 영혼의 제단"),
    ("/objects/crafting/xenostation/xenolab.config",
     "/paneLayout/windowtitle/title", " XENO RESEARCH LAB", " 제노 연구 실험실"),
    ("/objects/crafting/xenostation/xenolab.config",
     "/paneLayout/windowtitle/subtitle", " Xenobiology Research", " 외계생물학 연구"),
    ("/objects/crafting/xenostation/xenolab.config",
     "/paneLayout/btnCraft/caption", "Craft", "제작"),
]

overrides = {}
for asset, ptr, en, ko in MODS:
    pn = asset + ".patch"
    pair = [{"op": "test", "path": ptr, "value": en},
            {"op": "replace", "path": ptr, "value": ko}]
    if pn in p.index:
        doc = json.loads(p.read(pn))
        flat = []
        for o in doc:
            if isinstance(o, dict):
                flat.append(o.get("path"))
            elif isinstance(o, list):
                flat += [x.get("path") for x in o if isinstance(x, dict)]
        if ptr not in flat:
            if doc and isinstance(doc[0], list):
                doc.append(pair)
            else:
                doc += pair
        overrides[pn] = json.dumps(doc, ensure_ascii=False).encode("utf-8")
        print("merge", pn[-60:])
    else:
        overrides[pn] = json.dumps(pair, ensure_ascii=False).encode("utf-8")
        print("add", pn[-60:])

try:
    print("entries:", write_pak(DEPLOY, DEPLOY, overrides))
except PermissionError:
    print("locked; tmp:", len(Pak(DEPLOY + ".tmp_write").index))
    sys.exit(3)
