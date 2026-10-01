# -*- coding: utf-8 -*-
"""Machine-translation-style naturalness scan over pak_pairs.tsv.

Distinct from earlier QA passes (structure/tags/placeholders, glossary terms,
name consistency). This pass targets *fluency*: particle mismatches, spacing,
doubled particles/endings, mixed speech levels inside one string, leftover
English, stray artifacts, and common literal-calque constructions.

Output: qa_mt_style_report.tsv  (kind, asset, pointer, detail, english, korean)
"""
import csv
import re
import sys
from collections import Counter
from pathlib import Path

csv.field_size_limit(sys.maxsize)

BASE = Path(__file__).parent.parent
IN = BASE / "data/pak_pairs.tsv"
OUT = BASE / "data/qa_mt_style_report.tsv"

TAG_RE = re.compile(r"\^[^^;]*;")
PLACEHOLDER_RE = re.compile(r"<[^>\n]{1,40}>|%[0-9]*[sdif%]|\{[^{}\n]{1,40}\}|\[[A-Za-z0-9_ +.-]{1,20}\]")


def jong(ch):
    if "가" <= ch <= "힣":
        return (ord(ch) - 0xAC00) % 28
    return -1


# ---------------------------------------------------------------- particles
# High-precision subset only. Korean words whose final syllable collides with a
# particle form (만든/뭔가/몰라/사랑/국가...) make most checks hopeless, so we
# only enforce pairs where word-internal occurrence is rare:
#   을(needs jong) / 를(needs no-jong) / 과(needs jong) / 와(needs no-jong)
#   로(no-jong or ㄹ) / 으로(jong except ㄹ) / 랑(no-jong) / 이랑(jong)
#   아(needs jong) / 야(needs no-jong) / 이(jong) / 가(no-jong) / 은(jong)
# Boundary required after the particle so word-internal syllables don't match.
# Only near-zero-FP pairs are enforced:
#   를 after jong / 와 after jong / 이랑 after no-jong / 랑 after jong
#   로 after jong(!=ㄹ) / 으로 after no-jong or ㄹ / 과 after no-jong
#   가 after jong / 야 after jong / 아 after no-jong
# (은/이/을 after no-jong and 는/이/를 verb-stem endings are too FP-prone;
#  지은/모을/부은/있는가/하는가 are all correct grammar.)
# NOTE: '이랑' is deliberately excluded -- 챠이랑/파이랑 parse as 이-final noun+랑
# and cannot be distinguished from 과이랑-style errors by regex.
PART_RE = re.compile(
    r"([가-힣])(랑|으로|로|가|를|과|와|아|야)"
    r"(?=[\s.,!?~…:;·'\"(){}<>/\[\]^*_-]|$)"
)

EXC = {
    # real words ending in X+을 (X has no jong) -- '을' wants jong
    "가을", "마을", "나을", "지을", "가울",
    # X+은 (X no jong) -- '은' wants jong
    "나은", "사은", "고은", "다은", "오은", "모은", "가은", "희은", "도은",
    # X+이 (X no jong) -- '이' wants jong
    "차이", "아이", "나이", "사이", "가위", "누이", "마이", "다이", "타이", "바이",
    "소이", "가이", "고이", "모이", "파이", "카이", "라이", "자이", "샤이", "코이",
    "도이", "허이", "재이", "세이", "레이", "네이", "메이", "페이", "베이", "게이",
    "데이", "헤이", "제이", "케이", "테이", "웨이", "예이", "체이", "에이", "로이",
    "보이", "조이", "노이", "포이", "토이", "호이", "초이", "드이", "묘이", "루이",
    "두이", "수이", "주이", "구이", "쿠이", "푸이", "누이", "부이", "무이", "스이",
    # X+가 (X has jong) -- '가' wants no-jong: real words + anatomy terms
    "국가", "작가", "평가", "창가", "강가", "정가", "대가", "주가", "장가", "상가",
    "생가", "사가", "공가", "통가", "종가", "거가", "전가", "심가", "임가", "도가",
    "법가", "명가", "희가", "동가", "서가", "남가", "인가", "망가", "성가", "열가",
    "항가", "광가", "음가", "손가", "발가", "암가", "감가", "밤가", "석가", "화가",
    "귀가", "미가", "비가", "시가", "의가", "증가", "불가", "허가", "평가", "첨가",
    "부가", "승가", "비가", "추가", "허가", "참가", "눈가", "입가", "귓가", "콧가",
    "뭔가", "군가", "건가", "닌가", "런가", "언가", "한가", "딘가", "젠가", "톤가",
    "문가", "양가", "험가", "핀가", "윈가", "승가", "숭가", "김가", "임가", "엄가",
    "앞가", "뒷가", "윗가", "궁가", "신가", "관가", "선가", "후가", "방가", "산가",
    # adnominal/question endings ending in jong + 가: 있는가/좋은가/아닌가/었던가
    "는가", "은가", "인가", "던가", "닌가", "션가", "견가", "렸가", "겠가", "쳤가",
    "든가", "운가", "떤가", "픈가", "큰가", "반가", "짠가", "겐가", "일가", "린가",
    "론가", "텐가", "잘가", "온가", "같가", "많가", "찮가", "같가", "든가",
    # real words ending in jong+가
    "집가", "술가", "악가", "각가", "존가", "축가", "식가", "영가", "점가", "농가",
    "닷가", "냇가", "물가", "본가", "행가", "삼가", "특가", "잠가", "담가", "안가",
    "등가", "몰가", "밍가", "펑가", "랑가", "랄가", "응가", "사가", "앞가", "장가",
    # X+과 (X no jong) -- '과' wants jong
    "사과", "경과", "통과", "효과", "여과", "교과", "모과", "유과", "노과", "지과",
    "대과", "미과", "피과", "세과", "고과", "수과", "주과", "초과", "개과", "치과",
    "내과", "외과", "이과", "문과", "아과", "부과", "신과", "후과", "기과", "다과",
    "니과", "티과", "어과", "제과", "투과", "소과", "화과", "위과", "무과", "비과",
    # X+와 (X has jong) -- '와' wants no-jong
    "동와", "절와", "생와", "안와",
    # X+랑 (X has jong) -- '랑' wants no-jong
    "찰랑", "달랑", "살랑", "들랑", "날랑", "쌀랑", "골랑", "일랑", "졸랑", "알랑",
    "올랑", "울랑", "놀랑", "풀랑", "물랑", "말랑", "딸랑", "명랑", "방랑", "백랑",
    # X+를 (X has jong) -- '를' wants no-jong: ㄹ-final 르-stems (들르다->들를)
    "들를", "굴를", "돌를", "불를", "둘를", "몰를", "졸를", "골를", "물를", "풀를",
    # X+아 (X no jong) -- '아' wants jong: interjections + -ia names
    "미아", "나아", "가아", "마아", "바아", "사아", "자아", "차아", "타아", "파아",
    "하아", "다아", "아아", "카아", "리아", "디아", "시아", "니아", "피아", "키아",
    "티아", "히아", "기아", "지아", "치아", "비아", "노아", "소아", "두아", "주아",
    "루아", "무아", "수아", "유아", "윤아", "은아", "진아", "선아", "서아", "세아",
    "솔아", "승아", "영아", "예아", "채아", "허아", "현아", "혜아", "호아", "효아",
    "끄아", "으아", "흐아", "크아", "푸아", "구아", "누아", "부아", "쿠아", "투아",
    "슈아", "오아", "고아", "도아", "모아", "보아", "조아", "초아", "코아", "포아",
    "로아", "소아", "요아", "우아", "뤼아", "뷰아", "듀아", "뮤아", "뉴아", "규아",
    "이아", "레아", "야아", "데아", "테아", "베아", "제아", "케아", "네아", "페아",
    "게아", "세아", "메아", "헤아", "레아", "제아", "셰아", "체아", "에아", "오아",
    # verb-stem+아 elongations and onomatopoeia
    "쏘아", "쪼아", "와아", "라아", "까아", "캬아", "먀아", "갸아", "짜아", "냐아",
    "므아", "띠아", "태아", "뽜아", "빠아", "봐아", "놔아", "줘아", "줘아", "왜아",
    # X+야 (X has jong) -- '야' wants no-jong
    "철야", "심야", "전야", "후야", "만야", "군야", "길야", "명야", "발야", "암야",
    "총야", "흉야", "범야", "담야", "장야", "문야", "서야", "남야", "금야", "실야",
    "석야", "원야", "공야", "성야", "관야", "열야", "불야", "산야", "물야", "홍야",
    "흑야", "밤야", "초야", "대야", "노야", "신야", "인야", "운야", "명야",
    "황야", "광야", "면야", "반야", "말야", "잔야", "탄야", "할야", "철야", "깊야",
    # X+로 (X has jong != ㄹ) -- '로' wants no-jong or ㄹ
    "장로", "진로", "통로", "공로", "백로", "앞로", "항로", "광로", "난로", "경로",
    "정로", "동로", "성로", "평로", "문로", "방로", "상로", "창로", "담로", "벽로",
    "침로", "혈로", "생로", "관로", "육로", "노로", "학로", "열로", "맹로", "암로",
    "청로", "황로", "충로", "심로", "금로", "은로", "철로", "국로", "실로", "명로",
    "산로", "절로", "승로", "순로", "인로", "증로", "천로", "환로", "훈로", "각로",
    "므로", "때로", "수로", "게로", "데로", "네로", "레로", "메로", "베로", "세로",
    # real words / names ending in jong+로
    "응로", "련로", "합로", "책로", "행로", "선로", "웃로", "엣로", "향로", "원로",
    "접로", "엔로", "핀로", "젤로", "펠로", "겔로", "멜로", "셀로", "병로", "입로",
}


def particle_flags(ko):
    flags = []
    for m in PART_RE.finditer(ko):
        prev, part = m.group(1), m.group(2)
        if prev + part[0] in EXC or prev + part in EXC:
            continue
        j = jong(prev)
        if j < 0:
            continue
        if part == "으로":
            ok = j != 0 and j != 8
        elif part == "로":
            ok = j == 0 or j == 8
        elif part in ("이랑", "과", "아"):
            ok = j != 0
        elif part in ("랑", "가", "를", "와", "야"):
            ok = j == 0
        else:
            continue
        if not ok:
            flags.append(prev + part)
    return flags


# ---------------------------------------------------------------- patterns
# boundary on both sides so 바나나/은은한/도도한/만만한 don't match; 나나/은은/도도
# removed entirely (나나="me or", 은은="silver is", 도도=dodo are legit tokens)
DOUBLE_PART = re.compile(
    r"(?<![가-힣])(을을|를를|는는|와와|과과|랑랑|야야|로로|"
    r"에게에게|에서에서|부터부터|까지까지|처럼처럼|보다보다|마저마저|조차조차|밖에밖에)"
    r"(?![가-힣])"
)
DUP_WORD = re.compile(r"(?<![가-힣])([가-힣]{2,4})\s+\1(?![가-힣])")
DUP_WORD_OK = {"자자", "네네", "에에", "아아", "이리", "저리", "하나", "둘둘", "빵빵"}

SPACE_BEFORE_PUNCT = re.compile(r"[가-힣] [.,!?](?![.\d])")
EN_SPACE_PUNCT = re.compile(r" [.,!?]")
DOUBLE_SPACE = re.compile(r"(?<![ \n]) {2,}(?![ \n])| $|^ ")
TAG_AFTER_OPEN = re.compile(r"\^(?!reset\b)[a-zA-Z#0-9]+; ")  # space inside colored span start
TAG_BEFORE_RESET = re.compile(r" \^reset;")                   # space inside colored span end

GLUE_SU = re.compile(r"수있|[가-힣]수없(?:다|는|을|었|지|니)")
GLUE_GEOT = re.compile(r"것같")

MISSPEL = re.compile(r"되요|되져|되죠|어떻해|금새|안되[다는지]|않되|을께")

DUP_ENDING = re.compile(
    r"니다요|니다네|입니다다|해요다|어요다|에요다|입니다요|습니다네|입니다네|했습니다다"
)
STRANGE_PUNCT = re.compile(r"(?<![.\d])\.{2}(?!\.)|[!?]\s?\.(?!\.)|,,|;;")

BADCHAR = re.compile(r"\\")
TRANSNOTE = re.compile(r"역주|(?<![가-힣<])역자|옮긴이|편역자|번역자|번역가|(?<![<은])번역 ?:|\(역 ?:|※")

ENG_LEFT = re.compile(r"(?<![A-Za-z])[a-z][a-z]{3,}(?![A-Za-z])")
# common legit lowercase loans/onomatopoeia kept minimal; triage by frequency
ENG_ALLOW = {
    "kupo", "kupopo", "bzzt", "nyaa", "nya", "meow", "woof", "arf", "mew",
    "purr", "grr", "hiss", "rawr", "bleep", "whirr", "beep", "boop", "zap",
    "pew", "bang", "boom", "crash", "splash", "splat", "wham", "thud", "thump",
    "snap", "crack", "fizz", "buzz", "heh", "hehe", "haha", "hoho", "ehehe",
    "fufu", "ahem", "gulp", "sigh", "yawn", "sniff", "shiver", "twitch",
    "blush", "drool", "pant", "wheeze", "whine", "whimper", "growl", "snarl",
    "roar", "howl", "yelp", "bark", "meep", "moo", "oink", "cluck", "quack",
    "ribbit", "chirp", "tweet", "hoot", "caw", "screech", "squeak", "squeal",
    "debug", "null", "true", "false", "item", "quest", "items", "config",
    "slot", "slots", "http", "https", "www", "com", "json", "lua", "png",
    "wav", "ogg", "ttf", "font", "icon", "file", "path", "name", "type",
    "this", "that", "with", "from", "your", "will", "would", "could", "have",
}

MT_PHRASES = [
    ("dangsin", re.compile(r"당신")),
    ("plural-they", re.compile(r"그들은|그녀들은|우리들은|너희들은")),
    ("this-is", re.compile(r"(?<![가-힣])(?:그것은|이것은|저것은)")),
    ("passive", re.compile(r"에 의해|에 의해서|에 의한")),
    ("geot-imnida", re.compile(r"것입니다|것이다")),
    ("doeeo-is", re.compile(r"되어 있|되어져|되어진|되어지")),
    ("can-become", re.compile(r"할 수 있게 되|할 수 있게 됩니|할 수 있게 됐")),
    ("through", re.compile(r"[을를] 통해")),
    ("have-gajigo", re.compile(r"[을를] 가지고 있")),
    ("many-things", re.compile(r"많은 것들|몇몇 것들")),
    ("roseo", re.compile(r"로서")),
    ("rosseo", re.compile(r"로써")),
    ("geunom", re.compile(r"그 녀석|그녀석|저 녀석|저녀석")),
    ("jashin", re.compile(r"자신의|자신을|자신이")),
    ("musimushi", re.compile(r"하는 중입니다|하는 중이다")),
    ("geot-boin", re.compile(r"것으로 보입니다|것으로 보인다|것 같습니다")),
]

POLITE_RE = re.compile(r"(습니다|습니까|세요|십시오|해요|예요|이에요|예죠|이죠|군요|네요|랍니다|습니다요)(?=[.!?…\n, ]|$)")
PLAIN_RE = re.compile(r"(한다|했다|이다|였다|된다|됐다|없다|있다|하라|해라|인가|겠다|왔다|갔다|냐)(?=[.!?…\n, ]|$)")
CASUAL_RE = re.compile(r"(해|야|거야|잖아|겠어|했어|됐어|없어|있어|구나|야지)(?=[.!?…\n, ]|$)")

EXAMINE_KEY = re.compile(r"/(\w+)description$", re.I)


def clean(ko):
    t = TAG_RE.sub("", ko)
    t = PLACEHOLDER_RE.sub(" ", t)
    return t


def main():
    rows = []
    with IN.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            rows.append(row)
    print("pairs:", len(rows))

    out = []
    for row in rows:
        asset, pointer, en, ko = row["asset"], row["pointer"], row["english"], row["korean"]
        if not ko or not re.search(r"[가-힣]", ko):
            continue
        c = clean(ko)

        fl = particle_flags(ko)
        if fl:
            out.append(("PARTICLE", asset, pointer, ",".join(dict.fromkeys(fl)), en, ko))

        m = DOUBLE_PART.search(c)
        if m:
            out.append(("DUP_PARTICLE", asset, pointer, m.group(1), en, ko))

        for m in DUP_WORD.finditer(c):
            if m.group(1) not in DUP_WORD_OK:
                out.append(("DUP_WORD", asset, pointer, m.group(1), en, ko))
                break

        # spaced punctuation mirrors the EN source (". . .") -- only flag if EN
        # itself has no space-punct
        m = SPACE_BEFORE_PUNCT.search(c)
        if m and not EN_SPACE_PUNCT.search(en):
            out.append(("SPACE_PUNCT", asset, pointer, m.group(0), en, ko))

        if DOUBLE_SPACE.search(ko) and not DOUBLE_SPACE.search(en):
            out.append(("DOUBLE_SPACE", asset, pointer, "", en, ko))

        if TAG_AFTER_OPEN.search(ko) and not TAG_AFTER_OPEN.search(en):
            out.append(("TAG_SPACE", asset, pointer, "open", en, ko))
        elif TAG_BEFORE_RESET.search(ko) and not TAG_BEFORE_RESET.search(en):
            out.append(("TAG_SPACE", asset, pointer, "close", en, ko))

        m = GLUE_SU.search(ko)
        if m:
            out.append(("GLUE_SU", asset, pointer, m.group(0), en, ko))
        if GLUE_GEOT.search(ko):
            out.append(("GLUE_GEOT", asset, pointer, GLUE_GEOT.search(ko).group(0), en, ko))

        # 'ㄹ받침+때' glued (할때/올때/될때...); 때 is a real morpheme inside
        # 깔때기/때문 -- exclude those continuations
        for m in re.finditer(r"([가-힣])때(?!문|기|안|도리|리|무)", ko):
            prev = m.group(1)
            if jong(prev) == 8 and prev != "를":
                out.append(("GLUE_TTAE", asset, pointer, prev + "때", en, ko))
                break

        m = MISSPEL.search(ko)
        if m:
            out.append(("MISSPEL", asset, pointer, m.group(0), en, ko))

        m = DUP_ENDING.search(ko)
        if m:
            out.append(("DUP_ENDING", asset, pointer, m.group(0), en, ko))

        # dot-type oddities ('..', '?.', '!.') mirror EN ellipsis style; scan
        # the tag-stripped text so tag-adjacent ';' doesn't double with a real
        # semicolon. Skip when the same token exists in EN.
        en_has_dots = ".." in en or "…" in en
        for m in STRANGE_PUNCT.finditer(c):
            tok = m.group(0)
            if tok in en:
                continue
            if tok in (",,", ";;") or not en_has_dots:
                out.append(("PUNCT", asset, pointer, tok, en, ko))
                break

        if ko.count("\\") > en.count("\\"):
            out.append(("BADCHAR", asset, pointer, f"\\x{ko.count(chr(92))}", en, ko))
        if "�" in ko:
            out.append(("BADCHAR", asset, pointer, "U+FFFD", en, ko))

        # strip common emoticons before paren balance check (:) :( :-( (:)
        # require a non-word char before ':' so "작성:)" list markers survive
        ko_noemo = re.sub(r"(?<![가-힣A-Za-z0-9]):-?[()DdPp]|(?<![가-힣A-Za-z0-9])=-?[()]|\(:", "", ko)
        if ko_noemo.count("(") != ko_noemo.count(")"):
            out.append(("PAREN", asset, pointer,
                        f"({ko_noemo.count('(')}/{ko_noemo.count(')')})", en, ko))

        m = TRANSNOTE.search(ko)
        if m:
            out.append(("TRANSNOTE", asset, pointer, m.group(0), en, ko))

        leftovers = [w for w in ENG_LEFT.findall(c) if w not in ENG_ALLOW]
        if leftovers:
            out.append(("ENG_LEFT", asset, pointer, ",".join(dict.fromkeys(leftovers)), en, ko))

        pol = len(POLITE_RE.findall(c))
        pla = len(PLAIN_RE.findall(c))
        cas = len(CASUAL_RE.findall(c))
        if pol and (pla or cas):
            out.append(("TONE_MIX", asset, pointer, f"pol={pol},plain={pla},cas={cas}", en, ko))

        if EXAMINE_KEY.search(pointer) and pol:
            out.append(("EXAMINE_POLITE", asset, pointer, f"pol={pol}", en, ko))

        for name, rx in MT_PHRASES:
            if rx.search(c):
                out.append(("PHRASE:" + name, asset, pointer, "", en, ko))

    counts = Counter(k for k, *_ in out)
    for k, v in counts.most_common():
        print(f"{k:24s} {v}")

    with OUT.open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["kind", "asset", "pointer", "detail", "english", "korean"])
        for row in out:
            w.writerow(row)
    print("wrote", OUT)


if __name__ == "__main__":
    main()
