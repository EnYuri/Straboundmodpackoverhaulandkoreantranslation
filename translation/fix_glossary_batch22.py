import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

ACTIVE_PAK = STAR / "mods" / "female_translation.pak"
PENDING_PAK = BASE / "female_translation.pak.REVIEW_PENDING"
SRC_PAK = PENDING_PAK if PENDING_PAK.exists() else ACTIVE_PAK

FIXES = {
    ("/interface/windowconfig/legioncrafting1.config.patch", "/paneLayout/lblProduct/value"): "사용 가능 픽셀",
    ("/interface/windowconfig/letheiacrafting.config.patch", "/paneLayout/lblProduct/value"): "사용 가능 픽셀",
    ("/interface/windowconfig/letheiacrafting1.config.patch", "/paneLayout/lblProduct/value"): "사용 가능 픽셀",
    ("/interface/windowconfig/letheiacrafting2.config.patch", "/paneLayout/lblProduct/value"): "사용 가능 픽셀",
    ("/interface/windowconfig/letheiacrafting3.config.patch", "/paneLayout/lblProduct/value"): "사용 가능 픽셀",
    ("/xrc_pp/config.config.patch", "/gui/lblFilterHaveMaterials/value"): "사용 가능 픽셀",
    ("/objects/avikan/tentobjects/avikanvanguardtapestry/avikanvanguardtapestry.object.patch", "/jorgasianDescription"):
        "밝은 붉은색 벽 장식이군. 조가시안 집에 잘 어울리겠어.",
    ("/objects/avikan/tentobjects/avikanvanguardtapestry1/avikanvanguardtapestry1.object.patch", "/jorgasianDescription"):
        "밝은 붉은색 벽 장식이군. 조가시안 집에 잘 어울리겠어.",
    ("/dialog/esc_grineer_empolyee.config.patch", "/converse/default/default/7"):
        "얼라이언스는 훌륭한 교역 상대야. 다만 그 인도주의적 보이콧만 좀 줄여 준다면 더 좋을 텐데.",
    ("/dialog/esc_grineer_empolyee.config.patch", "/greeting/default/default/7"):
        "얼라이언스는 훌륭한 교역 상대야. 다만 그 인도주의적 보이콧만 좀 줄여 준다면 더 좋을 텐데.",
    ("/dialog/ffs_prisoner_cultist_converse.config.patch", "/converse/aegi/default/2"):
        "얼라이언스가 이 일을 알게 될 거야. 네 영웅적인 활약도!",
    ("/dialog/ffs_prisoner_pirate_converse.config.patch", "/converse/aegi/default/3"):
        "얼라이언스가 이 일을 알게 될 거야. 네 영웅적인 활약도!",
    ("/items/craftingguides/alliancecraftingguide.item.patch", "/shortdescription"):
        "^#BA66FF;얼라이언스 제작 안내서^white;",
    ("/items/other/alliancecrewcontract.item.patch", "/shortdescription"):
        "^#BA66FF;얼라이언스 승무원 계약서^white;",
    ("/items/other/securitypass/allianceambassadorpass.item.patch", "/shortdescription"):
        "^#BA66FF;얼라이언스 대사 패스^white;",
    ("/npcs/avikanoutpost/unique/ao-aegiofficial.npctype.patch", "/scriptConfig/dialog/converse/aegi/aegi/0"):
        "반가운 얼굴이군! 얼라이언스 업무로 온 건가, 친구?",
    ("/quests/STORY/alliance/alliancestory-shield.questtemplate.patch", "/completionText"):
        "크레온에 돌아오신 걸 환영합니다, 대사님. 이걸 받아 주세요. 얼라이언스의 문장으로 장식된 방패입니다. 보호국에 줄 선물이었지만, 이제 그들이 사라졌으니 당신이 가졌으면 합니다.",
    ("/quests/alliancequests/allianceoutpost/alliancecrafting.questtemplate.patch", "/title"):
        "^green;얼라이언스 제작 기법",
    ("/quests/alliancequests/allianceoutpost/alliancemechparts.questtemplate.patch", "/title"):
        "^green;얼라이언스 메크 부품",
    ("/quests/alliancequests/allianceoutpost/allianceuniform-trink.questtemplate.patch", "/text"):
        "안녕하세요, 대사님! 얼라이언스 신체 개조가 준비됐습니다. 여기 있습니다.",
}


def main():
    pak = Pak(str(SRC_PAK))
    by_asset = {}
    for asset, pointer in FIXES:
        by_asset.setdefault(asset, {})[pointer] = FIXES[asset, pointer]
    overrides = {}
    changed = 0
    for asset, fixes in by_asset.items():
        doc = json.loads(pak.read(asset))
        seen = set()
        stack = list(doc)
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict) and item.get("op") == "replace" and item.get("path") in fixes:
                item["value"] = fixes[item["path"]]
                seen.add(item["path"])
                changed += 1
        assert seen == set(fixes), (asset, seen, set(fixes))
        overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")
    count = write_pak(PENDING_PAK, SRC_PAK, overrides)
    check = Pak(str(PENDING_PAK))
    assert len(check.index) == count
    for asset, data in overrides.items():
        assert check.read(asset) == data
    print(f"updated pending pak from {SRC_PAK.name}; changed {changed} fields in {len(overrides)} assets")


if __name__ == "__main__":
    main()
