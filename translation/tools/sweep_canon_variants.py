"""Sweep leftover non-canonical name variants inside the pending pak.

The main pipeline only fixes rows whose EN literally contains the entity
name. Strings where EN is empty (folded FU_KO/sbkor bare-replace ops) or
where the name appears inside a different compound entity name
('미니 쇼고트' for 'Minishoggoth') keep stale variants. This pass sweeps a
hand-curated set of PROPER-NOUN variant strings pack-wide, reusing the
same boundary/particle rules as apply_name_fixes.variant_replace.

Only transliteration/proper-noun variants are listed - never common nouns
('벌집', '진흙', '공학자' must stay, they occur as ordinary words).
"""
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
sys.path.insert(0, str(BASE))

from pak import Pak  # noqa: E402
import pak_writer  # noqa: E402
import propose_name_fixes as P  # noqa: E402
from apply_name_fixes import variant_replace  # noqa: E402

# vocative/copula endings ('쇼고트야?', '마스터 조작기네') and noun suffixes
# ('아펙스용', '아비터형') are also valid name boundaries for this sweep -
# proper nouns only, no common nouns
P.PARTICLES = tuple(P.PARTICLES) + ("야", "아", "여", "이여", "다", "네",
                                   "용", "형", "들")

# literal repairs for damage produced by earlier rounds (run before SWEEP)
REPAIR = [
    ("노획한 노획한 나노 리셉터클", "노획한 나노 리셉터클"),
    ("회수된 노획한 나노 리셉터클", "노획한 나노 리셉터클"),
]

# variant -> canonical (all user-overridden / glossary-fixed proper nouns)
SWEEP = {
    "쇼고트": "쇼고스",
    "호기심 많은 결함": "호기심 많은 글리치",
    "호기심 글리치": "호기심 많은 글리치",
    "마이크로 구체": "마이크로스피어",
    "커피 기계": "커피 머신",
    "에르키우스 공포": "에르키우스 호러",
    "치명적인 회로": "페이탈 서킷",
    "클루엑스 감시병": "클루엑스 센트리",
    "눈알 레모네이드": "오큘레모네이드",
    "잘린 의회": "클립드 의회",
    "솔라리움 별": "솔라리움 스타",
    "에르키우스 연료 결정": "크리스탈 에르키우스 연료",
    "선박 사물함": "함선 사물함",
    "선박 보관함": "함선 사물함",
    "배 사물함": "함선 사물함",
    "우주선 사물함": "함선 사물함",
    "우주선 보관함": "함선 사물함",
    "에르키우스 유령": "에르키우스 고스트",
    # transliteration-priority canon round 2 (canon_overrides.tsv)
    "발톱 글러브": "클로우 글러브",
    "수정 브로콜리": "크리스탈 식물",
    "부란기": "인큐베이터",
    "철부리": "아이언비크",
    "등불 달린 막대기": "랜턴 스틱",
    "마스터 조작기": "마스터 매니퓰레이터",
    "채광용 드론": "채굴 드론",
    "채광 드론": "채굴 드론",
    "채굴용 드론": "채굴 드론",
    "엄마 팝팝": "마더 팝톱",
    "엄마 팝탑": "마더 팝톱",
    "엄마 팝톱": "마더 팝톱",
    "마더 팝탑": "마더 팝톱",
    "성인 팝탑": "성체 팝톱",
    "성인 팝톱": "성체 팝톱",
    "성체 팝탑": "성체 팝톱",
    "노획한 나노 소켓": "노획한 나노 리셉터클",
    "나노 리셉터클": "노획한 나노 리셉터클",
    "배 문": "함선 문",
    "우주선 문": "함선 문",
    "솔루스 소드": "솔루스 카타나",
    "레이쓰": "레이스",
    "설인": "예티",
    "팝탑쏭": "팝톱쏭",
    "팝탑": "팝톱",
    # '팝팝' excluded: also used as onomatopoeia ('pop pop!')
    "비나리즈": "비날리제이",
    "엘'두카르": "엘드우카르",
    "무타-문탄트": "무타-문턴트",
    "문탄트": "문턴트",
    "위저드": "마법사",
    "리플리케이터": "복제기",
    # round 4: residual-queue proper nouns (transliteration audit)
    # species / demonyms (-족 keeps the suffix on purpose)
    "아펙스": "에이펙스",
    "히로틀": "하이로틀",
    "하이 로틀": "하이로틀",
    "하이롤": "하이로틀",
    "키로스": "키르호스",
    "키호시": "키르호시",
    "페녹스": "페네록스",
    "에이비언": "아비안",
    "아비앙": "아비안",
    "만티족": "만티지족",
    "스카트족": "스카스족",
    "나이트아르족": "나이터족",
    "바리투족": "파리투족",
    "휴먼": "인간",
    # SAIL full name: canon word order + 함선 prefix
    "선박 기반 격자 인공지능": "함선 기반 인공지능 격자",
    "함선 기반 격자 인공지능": "함선 기반 인공지능 격자",
    "함선기반 격자 인공지능": "함선 기반 인공지능 격자",
    "선박용 인공지능 격자": "함선 기반 인공지능 격자",
    "선박 기반 인공지능 격자": "함선 기반 인공지능 격자",
    "눈알레몬": "오큘레몬",
    # monster field-guide spellings (pandorasbox '몬스터: X - 가족: X')
    "너트미드겔링": "넛밋지링",
    "너트미즐링": "넛밋지링",
    "너트미글링": "넛밋지링",
    "너트미지": "넛밋지",
    "너트미드": "넛밋지",
    "불밥": "벌밥",
    "바통": "배통",
    "밥패": "밥페",
    "벌집벌레": "허밍버그",
    "하이프나레": "히프네어",
    "익쏠링": "익소링",
    "익솔링": "익소링",
    "미아스몹": "미아즈모프",
    "모노퍼스": "모노푸스",
    "나핀": "나르핀",
    "오큘러몬": "오큘롭",
    "오르바이드": "오바이드",
    "오글러": "오우글러",
    "우글러": "오우글러",
    "페트리큐브": "페트리컵",
    "쿼그머트": "쿼그멋",
    "링람": "링그램",
    "스케이버란": "스캐배런",
    "스카베란": "스캐배런",
    "슈룸밥": "쉬룸밥",
    "스내글러": "스네글러",
    "스나언트": "스나우트",
    "스넌트": "스나우트",
    "스포커스": "스포거스",
    "스킴": "스큄",
    "투밍고": "토우밍고",
    "트리투스": "트릭터스",
    "요캣": "요카트",
    "글랩": "글립",
    # distinct transliterations of items/NPCs/factions
    "룩시안트": "룩시언트",
    "퀘시토르": "콰지토르",
    "솔라룸": "솔라리움",
    "바리투": "파리투",
    "더트어친": "흙성게",
    "페더크라운": "깃털왕관",
    "젬글로우": "보석광",
    "테티드": "테타이드",
    "머크팽": "먹팽",
    "카바노그": "카어반노그",
    "살바록": "살발록",
    "카라크": "카락",
    "와그너": "바그너",
    "스카트": "스카스",
    "나이트아르": "나이터",
    "엘두크하르": "엘드우카르",
    "벨루쉬": "벨루이시",
    "벨루이쉬": "벨루이시",
    "무탄트": "문턴트",
    "바타락": "바스라크",
    "피닉스플라이": "불새불이",
    "리프포드": "암초",
    "리프팟": "암초",
    "코랄크립": "산호초",
    "트래퍼": "덫사냥꾼",
    "캐노니어": "포수",
    "콘키스타도르": "정복자",
    "데드샷": "명사수",
    "파이오니어": "개척자",
    "비질란테": "자경단원",
    "펜닉스": "페닉스",
    "익소돔": "익소둠",
    "스시": "초밥",
    "슈퍼 펫": "슈퍼펫",
    "유전자베리": "제네시베리",
    "맹세지기": "서약지기",
    "시안나이더": "시안화물 음료",
    "진주 완두콩": "진주콩",
    "펄피": "진주콩",
    "볼트번": "볼트 구근",
    "저거너트": "거신",
    "매드니스": "광기",
    "체인즐링": "체인질링",
    "에그슛": "에그슈트",
    "별 항해자의 피난처": "스타페어러의 피난처",
    "던스토크": "던스톡",
    "트립로드": "트라이플로드",
    "디스토션 스피어": "디스토션 구체",
    "클리핑 카운슬": "클립드 의회",
    "클립드 카운슬": "클립드 의회",
    "캡틴 노블": "캡틴 이그노블",
    "돈 마카로니 반지": "돈 마카로니 링",
    "아비터": "중재자",
    "노마딕 소울": "방랑자의 혼",
    "호크아이 행크": "매의 눈 행크",
    "이동성 II": "기동성 II",
    "초소형 구체": "마이크로스피어",
    "아머 업": "갑옷 강화",
    # round 5: residual-queue tail (monsters, items, NPC names)
    "너트미드젤링": "넛밋지링",
    "넛미드젤링": "넛밋지링",
    "오큘럽": "오큘롭",
    "페리투": "파리투",
    "바슈타": "와스타",
    "계란순": "에그슈트",
    "볼트볼브": "볼트 구근",
    "깃털관": "깃털왕관",
    "바봇": "보봇",
    "블래스트스톤": "폭발석",
    "마그마록": "마그마 암석",
    "릴로케이터": "재배치기",
    "완더러": "방랑자",
    "팅커링": "땜질",
    "요캇": "요카트",
    "이그노움": "이그놈",
    "저거노트": "거신",
    "퍼스플럼": "고름 자두",
    "비크시드": "부리씨앗",
    "둠캐넌": "둠캐논",
    "바민트": "버민트",
    "소각기": "소각로",
    "타르구체": "타르 공",
    "천상가": "헤븐송",
    "평화유지군": "피스키퍼",
    "메카라크니드": "로봇 거미",
    "벨우이시": "벨루이시",
    "팝팝": "팝톱",
    "듄스톡": "던스톡",
    "스타프룻": "별열매",
    "트리팽글": "트라이팽글",
    "익스터미네이터": "말살자",
    "오버차지": "과충전",
    "엘두우카르": "엘드우카르",
    "미스트": "안개",

    "아자스": "아자토스",
    "앨리프": "알렙",
    "브라마": "브라흐마",
    "진사": "주사",
    "시나바": "주사",
    "신나바": "주사",
    "공생체": "심비오트",
    "토치": "횃불",
    "커런트콘": "전류수수",
    "스퀨임": "스큄",
    "하나로 된 돌": "모놀리스",
}


def iter_ops(node):
    for op in node:
        if isinstance(op, list):
            yield from iter_ops(op)
        elif isinstance(op, dict):
            yield op


def main():
    src = BASE / "backup_paks/female_translation.pak.REVIEW_PENDING"
    pak = Pak(str(src))
    overrides = {}
    total = 0
    for asset in pak.index:
        if not asset.endswith(".patch"):
            continue
        try:
            doc = json.loads(pak.read(asset))
        except Exception:
            continue
        n = 0
        for op in iter_ops(doc):
            if not isinstance(op.get("value"), str):
                continue
            v = op["value"]
            for find, rep in REPAIR:
                if find in v:
                    m = v.count(find)
                    v = v.replace(find, rep)
                    n += m
            for var, canon in SWEEP.items():
                if var not in v:
                    continue
                # variant_replace masks existing canon internally, so a
                # variant inside the canon never re-triggers a replacement
                while True:
                    new = variant_replace(v, var, canon)
                    if not new:
                        break
                    v, n = new, n + 1
                # variant_replace's particle list doesn't cover copulas
                # ('선박 사물함입니다') - fall back to a copula lookahead
                v2, m = re.subn(r"(?<![가-힣])" + re.escape(var) +
                                r"(?=입니|이다|였|이었|인가)", canon, v)
                if m:
                    v, n = v2, n + m
            if v != op["value"]:
                op["value"] = v
        if n:
            overrides[asset] = json.dumps(
                doc, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
            print(" ", n, asset)
            total += n
    print("swept ops:", total, "across", len(overrides), "assets")
    if overrides:
        pak.f.close()  # release read handle before in-place rewrite
        n = pak_writer.write_pak(str(src), str(src), overrides)
        print("rewrote", src.name, "entries:", n)


if __name__ == "__main__":
    main()
