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
    "관찰 유기농 제품을 보존하기 위해 병에 담긴 포름알데히드.": "관찰. 유기물을 보존하기 위해 포름알데히드에 담아 둔 병이다.",
    "관심 없어 표준 환기 시스템이야": "무관심. 평범한 환기 장치다.",
    "진술서 문이야": "진술. 문이다.",
    "책상입니다. 앉아서 글 쓰는 것을 좋아하는 사람들을 위해.": "책상이구만. 앉아서 글 쓰기 좋아하는 사람들한테 딱이겠어.",
    "책장입니다. 여기 자기계발서가 많네요...": "책장이구만. 자기계발서가 잔뜩 꽂혀 있네...",
    "저장. 작동하지 않습니다.": "보관함. 작동 안 한다.",
    "스토리지. 켜져 있지 않습니다.": "보관함. 꺼져 있다.",
    "크고 무거운 상자들로, 먹잇감 위에 떨어뜨리기 좋습니다.": "크고 무거운 상자다. 먹잇감 위에 떨어뜨리기 좋다.",
    "기계는 식물처럼 태양에서 전력을 얻습니다. 플로란은 그것을 좋아합니다.": "기계는 식물처럼 태양에서 힘 얻는다. 플로란 마음에 든다.",
    "비에라 친구라면 언제든 환영이다, 쿠뽀!": "비에라 친구라면 언제든 환영이다쿠포!",
    "식사하기 편안한 부스야, 쿠뽀.": "식사하기 편안한 부스다쿠포.",
    "편히 쉬며 잠자기 아늑한 공간이야, 쿠뽀.": "편히 쉴 수 있는 아늑한 잠자리다쿠포.",
    "서둘러라 쿠포포!": "서두르라쿠포포!",
    "예뿐 작은 상자다, 예뿐 작은 엉덩이를 위한.": "예쁜 작은 상자다냥. 예쁜 작은 엉덩이를 앉힐 거다냥.",
    "이상한 야옹틱한 블록이라니..?": "이상한 블록인가냥..?",
    "넘어뜨리고 싶은데, 꽤 무거워어어...": "넘어뜨리고 싶은데, 꽤 무겁다냥...",
    "이 작은 개인실 중 하나가 잠겨 있지 않네... 뒤져 볼 시간인가?": "이 작은 개인실 하나가 안 잠겼다냥... 털 시간인가냥?",
    "이 연단으로 크게 말할 수 있어. 근데 왜 그래야 하는지 모르겠고, 하고 싶지도 않아.": "이 연단으로 크게 말할 수 있다냥. 왜 그래야 하는지도 모르겠고, 그러기도 싫다냥.",
    "그런 것 같기도 하고? 몰라, 나 초상화 속 사람들 잘 기억 안 나.": "그런 것 같기도 하다냥? 몰라, 초상화 속 녀석들은 잘 기억 안 난다냥.",
    "저게 레다 퍼르티아야, 한순간엔 무대 위에 있다가 - 다음 순간엔 - 사라졌지. 와, 그거 참 짜릿했는데.": "저게 레다 퍼르티아다냥. 한순간엔 무대 위에 있다가 다음 순간엔 사라졌다냥. 와, 정말 짜릿했다냥.",
    "물로 가득한 탱크다, 지난번에 이런 걸 봤을 땐 물이 다 새어 나왔어.": "물로 가득한 탱크다냥. 지난번에 이런 걸 봤을 땐 물이 다 새어 나왔다냥.",
    "화장지 롤이 부르르르르...": "화장지 롤이 부르르르냥...",
    "나 태어나기 한참 전 예술 작품 같은 거네. 되게 지루해.": "나 태어나기 한참 전의 예술 작품 같다냥. 엄청 지루하다냥.",
    "오, 퍼- 퍼르- 퍼르리자. 뭔가 음... 음식 간판이네.": "오, 피- 피- 피자다냥. 뭔가... 음식 간판이다냥.",
}


def corrected(english, korean):
    value = EXACT.get(korean, korean)
    if "kupo" in english.lower():
        value = value.replace(", 쿠뽀", "쿠포").replace(", 쿠포", "쿠포")
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
