import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

PENDING_PAK = BASE / "female_translation.pak.REVIEW_PENDING"
PAIRS = BASE / "pak_pairs_pending.tsv"

EXACT = {
    "낙하하는 동안 열어서 부드럽게 떨어지세요. ^orange;트라이코더^reset;를 사용해 업그레이드할 수 있습니다.":
        "펼치면 낙하 중 천천히 떠내려갑니다. 집 안에서 펼치면 재수가 없다고 합니다.",
    "이 (^cyan;선택적^reset;)시설은 에르키우스 수정의 중심 공급처입니다. 구조 요청이 우리를 도와달라고 손짓합니다.":
        "이 시설은 함선의 FTL 드라이브를 업그레이드할 수 있는 에르키우스 수정의 주요 산지입니다.",
    "^cyan;면역^reset;: 극한 열/추위/방사선/독, 용암, 액체 질소":
        "이 멋진 메크 섀시로 우주를 지키세요.",
    "^cyan;면역^reset;: 열대/사막 더위, 약한 독, 냉기":
        "레테이아 코퍼레이션이 설계한 개방형 조종석의 메크 몸체 시제품입니다.",
    "방패를 들면 ^#2080f0;에너지 발전기^reset; 상태 효과를 부여한다.\r\n막기 동작을 충분히 빠르게 발동하면(패링 타이밍) 완벽하게 막는다.":
        "방패를 들면 ^#2080f0;에너지 발전기^reset; 상태 효과를 부여한다.\r\n막기 동작을 충분히 빠르게 발동하면(패링 타이밍) 퍼펙트 블록을 발동한다.",
}


def corrected(english, korean):
    value = EXACT.get(korean, korean)
    token_variants = {
        "[Special 1]": ("[특수 1]", "[스페셜 1]", "[특수 능력 1]"),
        "[Special 2]": ("[특수 2]", "[스페셜 2]", "[특수 능력 2]"),
        "[Special 3]": ("[특수 3]", "[스페셜 3]", "[특수 능력 3]"),
        "[Primary Fire]": ("[주 발사]", "[주 공격]"),
        "[Alt Fire]": ("[보조 발사]", "[보조 공격]"),
    }
    for token, variants in token_variants.items():
        if token in english:
            for variant in variants:
                value = value.replace(variant, token)
    return value


def main():
    changes = defaultdict(dict)
    with PAIRS.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            new = corrected(row["english"], row["korean"])
            if new != row["korean"]:
                changes[(row["asset"], row["pointer"])][row["korean"]] = new

    pak = Pak(str(PENDING_PAK))
    overrides = {}
    changed = 0
    for asset in {asset for asset, _ in changes}:
        doc = json.loads(pak.read(asset))
        stack = list(doc)
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict) and item.get("op") == "replace":
                replacement = changes.get((asset, item.get("path")), {}).get(item.get("value"))
                if replacement is not None:
                    item["value"] = replacement
                    changed += 1
        overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")

    expected = sum(len(values) for values in changes.values())
    assert changed == expected, (changed, expected)
    del pak
    count = write_pak(PENDING_PAK, PENDING_PAK, overrides)
    print(f"updated pending pak; changed {changed} fields in {len(overrides)} assets; entries {count}")


if __name__ == "__main__":
    main()
