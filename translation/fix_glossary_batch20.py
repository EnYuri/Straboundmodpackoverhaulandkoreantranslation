import json
import sys
from pathlib import Path

BASE = Path(__file__).parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = BASE / "female_translation.pak.NEW24"

MILITARY_TRANSPORT = "/objects/STATIC_VEHICLES/gic_militarytransport/gic_militarytransport.object.patch"
LATCH = "/objects/alta/wired/logic/latch.object.patch"

MILITARY_REPLACEMENTS = {
    "/apexDescription": (
        "장갑차입니다. 미니크녹이 써야 할 물건인데 안 쓰네요.",
        "장갑차다. 미니크녹이 사용해야 할 물건인데 그러지 않는군.",
    ),
    "/avianDescription": (
        "금속 바퀴 차량입니다.",
        "금속으로 된 바퀴 달린 차량이다.",
    ),
    "/floranDescription": (
        "플로란이 보기에 재미있는 게 없어. 지루해.",
        "플로란 눈엔 재미있는 게 없다. 지루하다.",
    ),
    "/glitchDescription": (
        "위압. 이 바퀴 달린 차량이 어떻게 이런 두려움을 주는지.",
        "위압. 이 바퀴 달린 차량은 어째서인지 두려움을 불러일으킨다.",
    ),
    "/humanDescription": (
        "좀비 영화에서 볼 법한 차예요.",
        "좀비 영화에서나 볼 법한 차네.",
    ),
    "/hylotlDescription": (
        "장갑 바퀴 차량입니다. 다목적 임무용으로 설계됐습니다.",
        "장갑을 두른 바퀴 달린 차량이다. 다목적 임무용으로 설계됐다.",
    ),
    "/novakidDescription": (
        "소형 수송 차량이구만. 병사를 싣는구만.",
        "작은 수송 차량이구만. 병사들을 나르는군.",
    ),
}

MILITARY_ADDITIONS = {
    "/description": (
        "An armored transport vehicle of some sort.",
        "어떤 종류의 장갑 수송 차량입니다.",
    ),
    "/shortdescription": (
        "Military Transport Car",
        "군용 수송차",
    ),
    "/avikanDescription": (
        "This armored vehicle is entirely mechanical and serves as a type law enforcement.",
        "이 장갑차는 전적으로 기계식이며 치안 유지 수단으로 쓰인다.",
    ),
    "/aegiDescription": (
        "Such show of force only results in more force from the opposing side.",
        "이런 무력 과시는 상대편의 더 큰 무력만 불러올 뿐이다.",
    ),
}

LATCH_REPLACEMENTS = {
    "/description": (
        "상단 또는 '사용' 노드는 래치가 하단 또는 '데이터' 노드를 기준으로 상태를 변경할 수 있는지 여부를 제어합니다.",
        "전선 상태를 저장하는 데 쓸 수 있는 래치입니다.",
    ),
    "/floranDescription": (
        "상단 또는 '사용' 노드는 래치가 하단 또는 '데이터' 노드에 따라 상태를 변경할 수 있는지 여부를 제어합니다.",
        "래치다. 전선 상태를 저장하는 데 쓸 수 있다.",
    ),
    "/glitchDescription": (
        "매혹. 상단 또는 'Enable' 노드는 래치가 하단 또는 'Data' 노드를 기준으로 상태를 변경할 수 있는지 여부를 제어한다.",
        "매혹. 전선 상태를 저장하는 데 쓸 수 있는 래치다.",
    ),
}


def operation_pairs(doc):
    for group in doc:
        if isinstance(group, list) and len(group) == 2:
            test, replace = group
            if test.get("op") == "test" and replace.get("op") == "replace":
                yield test, replace


def fix_military_transport(data):
    doc = json.loads(data)
    flat_ops = {
        op["path"]: op
        for op in doc
        if isinstance(op, dict) and op.get("op") == "replace"
    }
    for pointer, (old, new) in MILITARY_REPLACEMENTS.items():
        op = flat_ops[pointer]
        assert op["value"] == old, (pointer, op["value"])
        op["value"] = new

    existing_paths = {
        op["path"]
        for group in doc
        for op in (group if isinstance(group, list) else [group])
        if isinstance(op, dict) and "path" in op
    }
    for pointer, (english, korean) in MILITARY_ADDITIONS.items():
        assert pointer not in existing_paths, pointer
        doc.append([
            {"op": "test", "path": pointer, "value": english},
            {"op": "replace", "path": pointer, "value": korean},
        ])
    return json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")


def fix_latch(data):
    doc = json.loads(data)
    pairs = {replace["path"]: (test, replace) for test, replace in operation_pairs(doc)}
    for pointer, (old, new) in LATCH_REPLACEMENTS.items():
        test, replace = pairs[pointer]
        assert replace["value"] == old, (pointer, replace["value"])
        assert test["path"] == pointer
        replace["value"] = new
    return json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")


def main():
    pak = Pak(str(SRC_PAK))
    overrides = {
        MILITARY_TRANSPORT: fix_military_transport(pak.read(MILITARY_TRANSPORT)),
        LATCH: fix_latch(pak.read(LATCH)),
    }
    count = write_pak(OUT_PAK, SRC_PAK, overrides)
    check = Pak(str(OUT_PAK))
    assert len(check.index) == count
    for asset, data in overrides.items():
        assert check.read(asset) == data
    print(f"wrote {OUT_PAK} with {count} entries; changed {len(overrides)} assets")


if __name__ == "__main__":
    main()
