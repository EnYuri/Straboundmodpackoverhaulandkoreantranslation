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
    "작은 새가이이 큰 자지를 가졌어엇!": "작은 새가 큰 자지를 가졌어엇!",
    "올리면 ^#2080f0;에너지 발전기^reset; 상태 부여.\r\n충분 빠른 블록(패링 시간) 퍼펙트 블록.":
        "방패를 들면 ^#2080f0;에너지 발전기^reset; 상태 효과를 부여한다.\r\n막기 동작을 충분히 빠르게 발동하면(패링 타이밍) 완벽하게 막는다.",
    "이 장거리 고정밀 에너지 기기 오래 지속 충격 생성, 높이 잃지 않고 이동.":
        "이 장거리 고정밀 에너지 장치는 고도를 잃지 않고 이동하는 지속성 충격파를 생성할 수 있다.",
    "외계인들도 고유 사회 있지만 다른 요괴를 인간과 혼동하는 건 놀랍게 일관적.":
        "외계인에게도 저마다 고유한 사회가 있지만, 서로 다른 요괴를 인간으로 착각한다는 점만큼은 놀랄 정도로 한결같아.",
    "텔레포터! 순간이동은 정말 급하네요.": "텔레포터! 순간이동은 정말 짜릿하네요.",
}


def main():
    changes = defaultdict(dict)
    with PAIRS.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if row["korean"] in EXACT:
                changes[(row["asset"], row["pointer"])][row["korean"]] = EXACT[row["korean"]]

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
