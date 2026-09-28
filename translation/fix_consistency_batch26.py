import csv
import json
import re
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
    "에이스네께서 당신을 지켜보시기를, 선장님.": "라데이스께서 당신을 지켜보시기를, 선장님.",
    "에이스네께서 당신을 지켜보시기를, 드로덴이여.": "라데이스께서 당신을 지켜보시기를, 드로덴이여.",
    "이어서, 팔케 장군이 툰드라 행성에 숨겨진 또 다른 호라이즌 시설을 발견했다고 알리며, 그 조사를 당신에게 맡긴다. 조사 도중, 당신은 이 기지가 실은 에인션트 유적 위에 자리한 발굴 현장이라는 사실을 발견한다. 호라이즌의 목표는 이른바 '프로젝트 이그제크레이션'과 더욱 얽혀 있는 것으로 보인다.":
        "이어서 팔케 장군은 툰드라 행성에 숨겨진 또 다른 호라이즌 시설을 발견했다며 조사를 맡긴다. 조사 도중, 이 기지가 실은 고대인 유적 위에 자리한 발굴 현장임을 알아낸다. 호라이즌의 목적은 이른바 '프로젝트 이그제크레이션'과 더욱 깊이 얽혀 있는 듯하다.",
    "가끔 에인션트 구조물의 룬을 읽어보려 해. 낯익은 것 같은데, 도무지 기억이 안 나...":
        "가끔 고대 구조물의 룬을 읽어보려 해. 낯익은 것 같은데, 도무지 기억이 안 나...",
    "소형 에인션트 천사풍 화병": "소형 고대 천사풍 화병",
    "에인션트? 아니, 나는 에인션트나 컬티베이터와는 아무 관계도 없다. 더 정확히 말하면, 네가 아는 이 우주의 그 어떤 존재했거나 존재하는 집단과도 관계가 없다.":
        "고대인? 아니, 나는 고대인이나 컬티베이터와는 아무 관계도 없다. 더 정확히 말하면, 네가 아는 이 우주에 존재했거나 존재하는 그 어떤 집단과도 관계가 없다.",
    "소형 에인션트 상자": "소형 고대인 상자",
    "에인션트 장치 같은 것. 엄청난 양의 에너지가 그 안을 흐른다.": "일종의 고대 장치다. 엄청난 양의 에너지가 그 안을 흐른다.",
    "둥근 에인션트 조명 (보스)": "둥근 고대인 조명 (보스)",
    "둥근 에인션트 트라이스테이트 조명": "둥근 고대인 트라이스테이트 조명",
    "그래서 ^cyan;근처 먼지의 분포를 보여주는 이 작은 장치^reset;를 만들었어, 원래는 그걸 추적하는 데 쓸 용도였지. 그리고 이미... 무력화된 상태니까, ^orange;이 장치로 저 에인션트 유적 안에서 그 흔적을 계속 추적할 수 있을 거야^reset;, 그리고 어쩌면 그 뒤에 숨겨진 비밀을 풀 수도 있고. ^yellow;솔직히 저 유적에 관심이 있다는 걸 고백해야겠어, 먼지 탐구자가 그런 곳까지 가는 건 흔치 않은 일이니까,^reset; 하지만 지금은 더 급한 일이 있어.":
        "그래서 ^cyan;근처 먼지의 분포를 보여주는 이 작은 장치^reset;를 만들었어. 원래는 그걸 추적할 용도였지. 그리고 이미... 무력화됐으니, ^orange;이 장치로 저 고대인 유적 안에서 흔적을 계속 추적할 수 있을 거야^reset;. 어쩌면 그 뒤에 숨은 비밀도 풀 수 있겠지. ^yellow;솔직히 저 유적에 관심이 있어. 먼지 탐구자가 그런 곳까지 가는 건 드문 일이니까.^reset; 하지만 지금은 더 급한 일이 있어.",
    "소문에 따르면 강력한 존재가 버리고 간 ^orange;어떤 에인션트 건축물^reset;이 ^green;에민스노우 행성^reset;에 있다고 한다. 그 안에는 내가 관심 있는 뭔가가 있어... 무슨 말인지 알지?":
        "소문에 따르면 강력한 존재가 버리고 간 ^orange;어떤 고대인 건축물^reset;이 ^green;에민스노우 행성^reset;에 있다고 한다. 그 안에는 내가 관심 있는 뭔가가 있어... 무슨 말인지 알지?",
    "일반 쿠키와 똑같지만 더 매콤합니다. ^orange;유형: 야채 + 유제품 + 계란 + 설탕^reset;":
        "일반 쿠키와 똑같지만 더 뾰족합니다. ^orange;유형: 야채 + 유제품 + 계란 + 설탕^reset;",
    "^#b9b5b2;당신의 편1를 위해 조작됨!": "^#b9b5b2;당신의 편의를 위해 조작됨!",
    "당신의 편1를 위해 조작됨!": "당신의 편의를 위해 조작됨!",
    "효과 범위 +1 증가": None,
    "색상": None,
    "알 수 없는 제작의 전통적인 칼로, 부러진 칼날로 완전히 녹슬어 있습니다. 제 정신이 아닌 자, 불사의 자, 명예를 잃은 자만이 이걸로 싸울 것입니다.^green;약탈자의 뿌리: 밀어내지 않는 공격 시 2배 피해. 마지막 공격에서 적을 밀어냅니다.^white;^#D6DFFF;대시: [SHIFT]를 눌러 앞으로 돌진하여, 강력한 상향 찌르기를 수행하여 [GiC] 보스 및 일반 적에게 출혈을 입힙니다. 하지만 부러진 검은 인상적이지 않을 것입니다. 3초 재사용 대기시간.":
        "제작자를 알 수 없는 전통 검으로, 칼날이 부러지고 녹으로 완전히 뒤덮였다. 예리함은 거의 남지 않았다. 미치광이, 불사자, 불명예를 뒤집어쓴 자만이 이걸 들고 싸울 것이다.\r\n^green;스캐빈저의 뿌리: 밀치기 이외의 공격 피해량 2배. 마지막 공격은 적을 밀쳐낸다.^white;\r\n^#D6DFFF;돌진: [SHIFT]를 눌러 앞으로 돌진한 뒤 강하게 올려 찌른다. [GiC] 보스와 일반 적에게 출혈을 일으킨다. 다만 부러진 검으로는 그다지 인상적이지 않을 것이다. 재사용 대기시간 3초.",
    "''남아있다면, 대가를 치러야 한다.''^#E2006D;다중우주 붕괴: [바닐라] 방어 값 5초 동안 무시.^white;^yellow;대부분의 이상 현상에 대한 최종 타격은 마이크로크레딧을 제공합니다.^white;^#D6DFFF;집주인의 반격: [SHIFT]로 무기의 정신을 불러와, 15초 동안 이상의 저항을 크게 증가시킵니다 | 40초 재사용 대기시간. 다른 무기의 자루치기를 중단합니다.^reset;":
        "''남는다면, 대가를 치러야 한다.''\r\n\r\n^#E2006D;다중우주 분쇄: 5초 동안 [Vanilla] 방어력 수치를 무시한다.^white;\r\n^yellow;대부분의 변칙 개체를 결정타로 처치하면 마이크로크레딧을 얻는다.^white;\r\n\r\n^#D6DFFF;집주인의 분노: [SHIFT]로 무기의 영혼을 집중해 15초 동안 변칙 개체에 대한 저항을 크게 높인다 | 재사용 대기시간 40초. 다른 무기의 자루치기를 방해한다.^reset;",
}


def corrected(english, korean):
    value = EXACT.get(korean, korean)
    if korean == "효과 범위 +1 증가":
        match = re.fullmatch(r"Increase area of effect to (\d+x\d+) tiles", english)
        if match:
            value = f"효과 범위를 {match.group(1)} 타일로 증가"
    if korean == "색상" and english == "Colour 1":
        value = "색상 1"
    for token in re.findall(r"(?<![A-Za-z0-9])T(\d+)(?![A-Za-z0-9])", english):
        model = f"T{token}"
        if model not in value:
            value = value.replace(f"{token}식", model)
    return value


def main():
    changes = defaultdict(dict)
    with PAIRS.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            new = corrected(row["english"], row["korean"])
            if new is not None and new != row["korean"]:
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
