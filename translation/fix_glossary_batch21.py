import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = BASE / "female_translation.pak.NEW25"

FIXES = {
    ("/objects/alliance/crafting/alliancemechcraftingtable/alliancemechcraftingtable.object.patch", "/drodenDescription"):
        "메크 제작대 감지됨. 새 메크 부품 생산에 사용됨.",
    ("/objects/avikan/crafting/avikanmechcraftingtable/avikanmechcraftingtable.object.patch", "/drodenDescription"):
        "메크 제작대 감지됨. 새 메크 부품 생산에 사용됨.",
    ("/objects/viera/crafting/upgradeablecraftingobjects/vieraanvil/vieracraftinganvil.object.patch", "/upgradeStages/1/itemSpawnParameters/hylotlDescription"):
        "금속 장비를 만드는 데 특화된 제작대인 것 같군.",
    ("/objects/CRAFTING/sb_variants/scifianvil/scifianvil.object.patch", "/floranDescription"):
        "플로란은 여기서 강한 무기를 만든다.",
    ("/objects/CRAFTING/upgradeablecraftingobjects/auraciteAnvil/auraciteAnvil.object.patch", "/upgradeStages/1/itemSpawnParameters/floranDescription"):
        "플로란은 이 제작대에서 강한 무기를 만든다.",
    ("/objects/CRAFTING/upgradeablecraftingobjects/auraciteAnvil/auraciteAnvil.object.patch", "/upgradeStages/2/itemSpawnParameters/floranDescription"):
        "플로란은 여기서 강한 무기를 만든다.",
    ("/objects/arcana/gilded/storage_1/arcana_gilded_storage_1.object.patch", "/floranDescription"):
        "플로란은 튼튼한 상자를 찾는다.",
    ("/objects/atprk_ashworld/atprk_ashchair/atprk_ashchair.object.patch", "/floranDescription"):
        "플로란이 먼지를 닦아내면 앉을 수 있는 높은 의자다.",
    ("/objects/atprk_relicseeker/atprk_planetpins/atprk_desertpin.object.patch", "/floranDescription"):
        "플로란은 사막 행성이 싫다! 너무 덥고, 식물도 거의 없고, 고기는 너무 퍽퍽하다! 그래도 플로란은 거기서 햇빛을 충분히 쬘 수 있다.",
    ("/objects/outpost/outpostreplicator/outpostreplicator.object.patch", "/floranDescription"):
        "플로란은 여기서 강한 무기를 만든다.",
    ("/objects/viera/crafting/upgradeablecraftingobjects/vieraanvil/vieracraftinganvil.object.patch", "/upgradeStages/1/itemSpawnParameters/floranDescription"):
        "플로란은 이 제작대에서 강한 무기를 만든다.",
    ("/objects/viera/crafting/upgradeablecraftingobjects/vieraanvil/vieracraftinganvil.object.patch", "/upgradeStages/2/itemSpawnParameters/floranDescription"):
        "플로란은 여기서 강한 무기를 만든다.",
    ("/objects/stickers/misc/protectoratesticker/PBprotectoratesticker.object.patch", "/apexDescription"):
        "행성 보호국의 상징이다. 미니크녹보다 훨씬 자애로운 조직이지.",
    ("/objects/stickers/misc/protectoratesticker/PBprotectoratesticker.object.patch", "/glitchDescription"):
        "단순명료함. 저것은 행성 보호국의 상징이다.",
    ("/objects/nonEKItechstation/nonEKItechstation.object.patch", "/dialog/wakePlayer/4/0"):
        "SAIL이 행성 보호국에 문제를 보고하는 동안 기다리세요. 서버에 연결 중...",
    ("/objects/atprk_ancient/atprk_ancientstatueprop/atprk_ancientcultivatorprop.object.patch", "/noolithDescription"):
        "편히 잠드소서, 우리의 컬티베이터여. 당신의 희생은 영원히 기억될 것입니다.",
    ("/objects/atprk_breakable/atprk_ancientshardsstatue/atprk_ancientshardsstatue2.object.patch", "/noolithDescription"):
        "편히 잠드소서, 우리의 컬티베이터여. 당신의 희생은 영원히 기억될 것입니다.",
    ("/objects/avikan/crafting/avikanbonecrafting/avikanbonecrafting.object.patch", "/upgradeStages/1/interactData/paneLayoutOverride/windowtitle/title"):
        "뼈 세공대",
    ("/objects/avikan/crafting/avikanleathercrafting/avikanleathercrafting.object.patch", "/upgradeStages/1/interactData/paneLayoutOverride/windowtitle/title"):
        "가죽 세공대",
    ("/items/crafting/trinktransmitter.item.patch", "/description"):
        "중앙 트링크 서킷과 통신할 수 있는 송신기입니다.",
    ("/items/WEAPONS/MELEE/gic_kyu_gunto/gic_kyu_gunto_npc.activeitem.patch", "/description"):
        "유니탄 장교들이 사기 진작을 위해 특별히 요청한 전통 검입니다. 지구의 ''제국의 묘지''에서 유래했습니다. 이 검은 초격에 위력을 집중하지만, 후속 공격은 약해집니다. ^green;SHIFT를 길게 눌러 패링^white;.\r\n^yellow;보병의 단짝: 막기 위력 150 HP.^white;\r\n^yellow;현대식 제작: 한손.^white;\r\n^green;조잡한 인체공학: 초격 피해량 5배. ^yellow;연속으로 공격하면 공격력이 약해집니다.^white;",
    ("/items/WEAPONS/MELEE/gic_shin_gunto/gic_shin_gunto_npc.activeitem.patch", "/description"):
        "유니탄 장교들이 사기 진작을 위해 특별히 요청한 전통 검입니다. 지구의 ''제국의 묘지''에서 유래했습니다. 이 검은 초격에 위력을 집중하지만, 후속 공격은 약해집니다. ^green;SHIFT를 길게 눌러 패링^white;.\r\n^yellow;보병의 단짝: 막기 위력 150 HP.^white;\r\n^yellow;현대식 제작: 한손.^white;\r\n^green;조잡한 인체공학: 초격 피해량 5배. ^yellow;연속으로 공격하면 공격력이 약해집니다.^white;",
    ("/items/WEAPONS/MELEE/gic_dadao/gic_dadao_npc.activeitem.patch", "/description"):
        "가난한 자가 '검'을 흉내 낸 물건입니다. 이 칼도끼는 무게로 위력을 내며, 인간의 문제를 해결하기에는 우아하지 못한 수단입니다.\r\n\r\n^yellow;아마노자쿠: 한손.^white;\r\n^green;불명예: 초격 피해량 4배. 마지막 공격에 강한 넉백.^white;",
    ("/codex/avikan/avikanramblings.codex.patch", "/contentPages/3"):
        "어쨌든, 그것은 나에게 말을 걸었고, 나는 그 말을 이해했다. 그것은 텔레안 침입자가 빠르게 접근하고 있으며, 폐허 바로 바깥 모래 속에 숨겨져 있던 작은 큐브를 노리고 있다고 경고했다. 옛 존재는 그 큐브가 무엇인지 말해주지 않았지만, 그것이 어떤 식으로든 중요하다는 것은 분명했다. 그것은 나에게 그 큐브를 침입자의 손이 닿지 않는 안전한 곳으로 가져가라고 일렀고, 그러고는 옛 존재는 나타났을 때만큼이나 빠르게 사라졌다.",
    ("/codex/avikan/avikanramblings.codex.patch", "/contentPages/4"):
        "그때 나는 망설이지 않았다. 즉시 출발했고, 어쩐지 큐브를 찾으려면 정확히 어디를 파야 하는지 알고 있었다. 옛 존재가 그 위치를 내 머릿속에 투영한 게 틀림없다. 나는 몇 분 만에 그걸 찾았고, 그런 다음 내 가드후르에게 달려가 서둘러 마을로 돌아갔다. 나는 큐브를 장로에게 보여줬고, 그녀는 그것을 받아 들며 안전한 곳에 보관하겠다고 나를 안심시켰다. 아마 곧 금고들 중 하나로 보낼 것 같다. 그녀는 내게 그걸 어디서 찾았는지 물었고, 나는 여기 쓴 내용을 그대로 그녀에게 말해주었다.",
    ("/codex/avikan/avikanramblings.codex.patch", "/contentPages/6"):
        "옛 존재가 말했던 침입자가 틀림없었어. 다른 이들에게 내 이야기가 사실이라고 설득하려 했지만 믿어주지 않았지. 심지어 몇 명을 유적으로 데려가 커다란 정육면체에 있는 열린 문을 보여주기까지 했는데, 도착해보니 문은 닫혀 있었어. 내 발자국은 바람에 지워졌고, 내가 했던 말이 사실이라는 증거는 아무것도 없었지. 나조차 내 자신을 의심하기 시작했는데, 그때...",
    ("/codex/avikan/avikanrhadeis1.codex.patch", "/contentPages/1"):
        "라데이스는 한때 신으로 여겨졌다. 모든 것을 보고, 모든 것을 알며, 여러 방식으로 세상에 영향을 미치는 신화적 존재였다. 그는 생과 사의 전령이자 우리 민족의 수호자로 믿어졌다. 하지만 이는 옛 존재들의 첫 도시인 바스 브할레이가 발견되기 전의 일이다. 오늘날 우리는 라데이스가 신도, 신화적 존재도 아니었음을 안다. 그는 사실 옛 존재 중 하나였다.",
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
        for group in doc:
            ops = group if isinstance(group, list) else [group]
            for op in ops:
                if op.get("op") == "replace" and op.get("path") in fixes:
                    op["value"] = fixes[op["path"]]
                    seen.add(op["path"])
                    changed += 1
        assert seen == set(fixes), (asset, seen, set(fixes))
        overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")
    count = write_pak(OUT_PAK, SRC_PAK, overrides)
    check = Pak(str(OUT_PAK))
    assert len(check.index) == count
    for asset, data in overrides.items():
        assert check.read(asset) == data
    print(f"wrote {OUT_PAK}; changed {changed} fields in {len(overrides)} assets")


if __name__ == "__main__":
    main()
