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
    "그것은 빛으로 죽인다. 불처럼.": "빛으로 죽인다. 불처럼.",
    "플로란은 어떤 먹잇감도 두렵지 않지만, 저것은? 플로란도 무섭다는 느낌이 든다...": "플로란 어떤 먹잇감도 안 무섭다. 하지만 저건? 플로란 무섭다...",
    "네가 바로 아야가 계속 떠들어대던 그 애구나. 혼자서 마을을 정리했다고 재잘거리더라고. 그 새를 아는 걸로 봐서는 진실을 말하는 건지 의심스럽지만, 다이텐구들이 우리가 한동안 함께 일하게 될 거라고 확실히 못을 박더라. 이름은 모미지야. 제6 백랑 중대의 대장이지.": "네가 바로 아야가 계속 떠들어대던 그 애구나. 혼자서 마을을 정리했다고 재잘거리더라고. 그 새를 아는 걸로 봐서는 진실을 말하는 건지 의심스럽지만, 다이텐구가 우리가 한동안 함께 일하게 될 거라고 확실히 못을 박더라. 이름은 모미지야. 제6 백랑 중대의 대장이지.",
    "메가트링크 갑옷은 트링키안 운용자가 사용하도록 설계되었다.": "MEGA-TRINK 방어구는 트링크 운용자가 사용하도록 설계되었다.",
    "메가-트링크 메카 몸체": "MEGA-TRINK 메카 몸체",
    "메가-트링크-00 메카 몸체": "MEGA-TRINK-00 메카 몸체",
    "MEGA-TRINK 방어구는 트링크 운용자가 사용하도록 설계되었다.": "MEGA-TRINK 방어구는 트링키안 운용자가 사용하도록 설계되었다.",
    "^yellow;트랭기안 콜로니 증서": "^yellow;트링키안 콜로니 증서",
    "트린키안 양식의 안테나입니다.": "트링키안 양식의 안테나입니다.",
}

PARTIAL = {
    "마지막으로, 아틀라스의 수호자인 그녀의 반응형 초중량 초기능성 메크 실드가 그녀를 부르고 있었다.": "마지막으로, 알타의 수호자인 그녀의 반응형 초중량 초기능성 메크 실드가 그녀를 부르고 있었다.",
    "엔바이로수호자 - 생명 유지와 비상 포스 실드를 제공한다.": "엔바이로프로텍터 - 생명 유지와 비상 포스 실드를 제공한다.",
}


def corrected(korean):
    value = EXACT.get(korean, korean)
    for old, new in PARTIAL.items():
        value = value.replace(old, new)
    return value


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
