#!/usr/bin/env python3
# Build the high-priority overlay pak covering the genuinely untranslated
# strings confirmed after the 2026-09-27 candidate-list correction. Each
# op-group is a [test, replace] pair on the final resolved (non-.patch)
# asset path, mirroring female_translation.pak's own overlay convention.
import sys
sys.path.insert(0, "../../")
from write_pak import write_pak, patch_bytes

def tr(path, en, ko):
    return path, [{"op": "test", "path": path, "value": en},
                  {"op": "replace", "path": path, "value": ko}]

overlays = {}  # assetPath (no .patch) -> list of op-groups

def add(asset, path, en, ko):
    overlays.setdefault(asset, []).append([
        {"op": "test", "path": path, "value": en},
        {"op": "replace", "path": path, "value": ko},
    ])

# 1. Novakid Quest Mod - teleport confirmation
add("/interface/confirmation/teleportconfirmation.config",
    "/novakidquest/subtitle", "The Scorched Planet", "타버린 행성")
add("/interface/confirmation/teleportconfirmation.config",
    "/novakidquest/message",
    "\n\nAre you ready for me to send you to the Scorched Planet?\n^red;You'll want to have good equipment for this.",
    "\n\n타버린 행성으로 보내드릴 준비가 되셨나요?\n^red;이번엔 좋은 장비를 챙기시는 게 좋을 겁니다.")

# 2. FrackinUniverse - ship status ticker line
add("/ai/ai.config", "/shipStatus/0/text", "^#6f6f6f;$ status", "^#6f6f6f;$ 상태")

# 3. The Starforge - cockpit resource friendly name
add("/interface/cockpit/cockpit.config",
    "/wordsList/starforge-tidefragment/friendlyWord", "Tidal Remnants", "조수의 잔재")

# 4. Stargate Invasion - annexed planet cockpit descriptions
add("/interface/cockpit/cockpit.config", "/visitableTypeDescription/stargate_goadesert/0",
    "This ^yellow;desert^reset; planet has been annexed by a belligerent race called ^red;Goa'uld.^reset;",
    "이 ^yellow;사막^reset; 행성은 호전적인 종족 ^red;고아울드^reset;에게 점령당했다.")
add("/interface/cockpit/cockpit.config", "/planetTypeNames/stargate_goadesert",
    "^red;Annexed^reset; ^yellow;Desert^reset;", "^red;점령됨^reset; ^yellow;사막^reset;")
add("/interface/cockpit/cockpit.config", "/visitableTypeDescription/stargate_goaforest/0",
    "This ^#15ce02;forest^reset; planet has been annexed by a belligerent race called ^red;Goa'uld.^reset;",
    "이 ^#15ce02;숲^reset; 행성은 호전적인 종족 ^red;고아울드^reset;에게 점령당했다.")
add("/interface/cockpit/cockpit.config", "/planetTypeNames/stargate_goaforest",
    "^red;Annexed^reset; ^#15ce02;Forest^reset;", "^red;점령됨^reset; ^#15ce02;숲^reset;")
add("/interface/cockpit/cockpit.config", "/visitableTypeDescription/stargate_goavolcanic/0",
    "This ^#e11212;Volcanic^reset; planet has been annexed by a belligerent race called ^red;Goa'uld.^reset;",
    "이 ^#e11212;화산^reset; 행성은 호전적인 종족 ^red;고아울드^reset;에게 점령당했다.")
add("/interface/cockpit/cockpit.config", "/planetTypeNames/stargate_goavolcanic",
    "^red;Annexed^reset; ^#e11212;Volcanic^reset;", "^red;점령됨^reset; ^#e11212;화산^reset;")

# 5. Project Redemption - weapon upgrade shortdescriptions
add("/items/active/weapons/fist/brassknuckles.activeitem",
    "/upgradeParameters/shortdescription", "Brass Knuckles ^yellow;^reset;", "황동 너클 ^yellow;^reset;")
add("/items/active/weapons/melee/axe/fryingpan.activeitem",
    "/upgradeParameters/shortdescription", "Frying Pan ^yellow;^reset;", "프라이팬 ^yellow;^reset;")

# 6. FU-Redemption integration patch - armor set-bonus descriptions
SET_30 = ("^orange;Set Bonuses^reset;: \n^yellow;^reset; +^green;30^reset;% Shield Stamina, Block, Shield Regen\n"
          "^yellow;^reset; ^cyan;Immune^reset;: All Cold, Oxygen")
SET_30_KO = ("^orange;세트 보너스^reset;: \n^yellow;^reset; +^green;30^reset;% 실드 스태미나, 블록, 실드 재생\n"
             "^yellow;^reset; ^cyan;면역^reset;: 모든 냉기, 산소")
for item in ("r-prismatic.chest", "r-prismatic.head", "r-prismatic.legs"):
    add(f"/items/armors/other/r-prismatic/{item}", "/description", SET_30, SET_30_KO)

SET_35 = ("^orange;Set Bonuses^reset;: \n^yellow;^reset; +^green;35^reset;% Shield Stamina, Block, Shield Regen\n"
          "^yellow;^reset; ^cyan;Immune^reset;: Deadly Heat, Acid, Burning, Oxygen, Gas, Pressure")
SET_35_KO = ("^orange;세트 보너스^reset;: \n^yellow;^reset; +^green;35^reset;% 실드 스태미나, 블록, 실드 재생\n"
             "^yellow;^reset; ^cyan;면역^reset;: 치명적 열기, 산, 화상, 산소, 가스, 기압")
for item in ("r_impervious.chest", "r_impervious.head", "r_impervious.legs"):
    add(f"/items/armors/other/r_impervious/{item}", "/description", SET_35, SET_35_KO)

add("/items/armors/protectorate/protectoratearmor/protectoratearmor.chest", "/description",
    "Experimental power armor to ensure protection for all.\n^orange;Set Bonuses^reset;:\n"
    "^yellow;^reset; Power Dash Tech. Partial knockback resist;\n"
    "^yellow;^reset; Protectorate Weaponry: Damage x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;Immune^reset;: Deadly Rads, Deadly Heat/Cold, Poison, Oxygen, Gas",
    "모두의 안전을 보장하기 위한 실험적인 파워 아머다.\n^orange;세트 보너스^reset;:\n"
    "^yellow;^reset; 파워 대시 기술. 넉백 부분 저항;\n"
    "^yellow;^reset; 프로텍토레이트 병기: 피해량 x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;면역^reset;: 치명적 방사능, 치명적 열기/냉기, 독, 산소, 가스")
add("/items/armors/protectorate/protectoratearmor/protectoratearmor.head", "/description",
    "The face of a noble cause.\n^cyan;Headlamp^reset;\n^orange;Set Bonuses^reset;:\n"
    "^yellow;^reset; Protector's Sphere Tech;\n"
    "^yellow;^reset; Protectorate Weaponry: Damage x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;Immune^reset;: Deadly Rads, Deadly Heat/Cold, Poison, Oxygen, Gas",
    "고귀한 대의의 얼굴이다.\n^cyan;헤드램프^reset;\n^orange;세트 보너스^reset;:\n"
    "^yellow;^reset; 프로텍터 스피어 기술;\n"
    "^yellow;^reset; 프로텍토레이트 병기: 피해량 x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;면역^reset;: 치명적 방사능, 치명적 열기/냉기, 독, 산소, 가스")
add("/items/armors/protectorate/protectoratearmor/protectoratearmor.legs", "/description",
    "These boots march onwards to a brighter future.\n^orange;Set Bonuses^reset;:\n"
    "^yellow;^reset; Rocket Thruster. Fall Damage Immunity;\n"
    "^yellow;^reset; Protectorate Weaponry: Damage x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;Immune^reset;: Deadly Rads, Deadly Heat/Cold, Poison, Oxygen, Gas",
    "이 부츠는 더 밝은 미래를 향해 나아간다.\n^orange;세트 보너스^reset;:\n"
    "^yellow;^reset; 로켓 추진기. 낙하 피해 면역;\n"
    "^yellow;^reset; 프로텍토레이트 병기: 피해량 x^green;1.3^reset;\n"
    "^yellow;^reset; ^cyan;면역^reset;: 치명적 방사능, 치명적 열기/냉기, 독, 산소, 가스")

files = {}
for asset, groups in overlays.items():
    files[asset + ".patch"] = patch_bytes(groups)

meta = {
    "name": "zz_localeko_highpriority_20260927",
    "friendlyName": "Korean Overhaul - High Priority Batch (2026-09-27)",
    "author": "local maintenance",
    "description": "New high-priority translations found after correcting scan_remaining.py's coverage bugs (2026-09-27 session): quest dialogue, cockpit UI, and armor set-bonus text across 6 mods.",
    "version": "2026-09-27.1",
    "priority": 999999860,
}
size, n = write_pak("../../mods/zz_localeko_highpriority_20260927.pak", files, meta)
print("wrote", size, "bytes,", n, "assets,", len(overlays), "target files")
for a in sorted(overlays):
    print(" ", a, len(overlays[a]), "ops")
