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
    "실험실에서 만든 아야 샘. 보통처럼 큰 아야카로 자라지는 않을 것 같아.": "실험실에서 만든 아야 새싹이네. 보통처럼 키 큰 아야카로 자라지는 않을 것 같아.",
    "실험실에서 만든 야비 샘. 보통 야비 과육과 달리 가끔씩 익는 것 같아.": "실험실에서 만든 야비 새싹이네. 보통 야비 열매와 달리 가끔씩 익는 것 같아.",
    "차이는 아마 가장 생생한 맛의 과일일 거야.": "차이는 아마 가장 강렬한 맛을 내는 과일일 거야.",
    "차이는 아마 세상에서 가장 화려한 맛을 내는 과일일 거야.": "차이는 아마 가장 강렬한 맛을 내는 과일일 거야.",
    "이 수생 식물은 젤리 속 새 생명을 낳아!": "이 수생 식물은 새로운 인젤리를 낳아!",
    "파아케인 싹! 오래 걸리지만 코어 조각으로 자랄 거야!": "파아케인 꽃봉오리네! 오래 걸리겠지만 더 많은 코어 조각으로 자랄 거야!",
    "아키 안 만져, 안 그럼 아키 화상!": "아키 만지지 않는다, 안 그러면 아키 탄다!",
    "이 실험실 식물은 순수 이온 수액을 만들 수 있어!": "실험실에서 만든 이 식물은 순수한 이온 수액을 만들어낼 수 있어!",
    "이 실험실산 식물은 순수한 이온 수액을 만들어낼 수 있어!": "실험실에서 만든 이 식물은 순수한 이온 수액을 만들어낼 수 있어!",
    "이 식물은 사실상 식물성 눈인 눈 같은 물질을 만들어!": "이 식물은 눈 같은 물질을 만들어내는데, 사실상 식물성 눈이나 마찬가지야!",
    "자라는 잔불 산호. 보통 엔테라시 프라임 행성에서 발견된다.": "자라나는 엠버 산호네. 보통 엔테라시 프라임 행성에서 발견되지.",
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
