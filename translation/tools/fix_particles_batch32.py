import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

PENDING_PAK = BASE / "backup_paks/female_translation.pak.REVIEW_PENDING"
PAIRS = BASE / "data/pak_pairs_pending.tsv"

REPLACEMENTS = {
    "보호국가 ": "보호국이 ",
    "연합 시스템가 ": "연합 시스템이 ",
    "트링크 서킷가 ": "트링크 서킷이 ",
    "노바키드이 ": "노바키드가 ",
    "피스키퍼이 ": "피스키퍼가 ",
    "연합 시스템를 ": "연합 시스템을 ",
    "숲의 파수꾼를 ": "숲의 파수꾼을 ",
    "제작대을 ": "제작대를 ",
    "스타더스트을 ": "스타더스트를 ",
    "피스키퍼을 ": "피스키퍼를 ",
    "얼라이언스을 ": "얼라이언스를 ",
    "숲의 파수꾼는 ": "숲의 파수꾼은 ",
    "피스키퍼은 ": "피스키퍼는 ",
    "소검와 ": "소검과 ",
    "새터니안와 ": "새터니안과 ",
    "연합 시스템와 ": "연합 시스템과 ",
    "피스키퍼과 ": "피스키퍼와 ",
    "스타더스트으로 ": "스타더스트로 ",
    "소검로 ": "소검으로 ",
    "고위 수호자으로 ": "고위 수호자로 ",
    "피스키퍼으로 ": "피스키퍼로 ",
    "얼라이언스으로 ": "얼라이언스로 ",
}

EXACT = {
    "루인드이 되지 않는 법에 관한 자기계발서.": "루인드 중 하나가 되지 않는 법에 관한 자기계발서.",
    "팅커 테이블은 다양한 제작대를 공학한다.": "팅커 테이블은 다양한 제작대를 만들어낸다.",
    "뿔은 순수 스타더스트로 됐어. 모든 색 얼룩이 어둠에서 아름답게 빛나.": "뿔은 순수한 스타더스트로 이루어졌어. 온갖 색의 반점이 어둠 속에서 아름답게 빛나.",
}


def corrected(korean):
    value = korean
    for old, new in REPLACEMENTS.items():
        value = value.replace(old, new)
    return EXACT.get(value, value)


def main():
    changes = defaultdict(dict)
    with PAIRS.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            new = corrected(row["korean"])
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
