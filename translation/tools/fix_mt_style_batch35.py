"""Batch 35: mechanical + verified MT-style naturalness fixes driven by
qa_mt_style_report.tsv. Applies unambiguous global fixes to every pair and
row-scoped fixes for flagged categories (double space, tag-internal spacing,
stray punctuation, space before punctuation, bad literal escapes).
"""
import csv
import json
import re
import sys
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

TARGET_PAK = STAR / "mods" / "zz_translation_female.pak"
PAIRS = BASE / "data/pak_pairs.tsv"
REPORT = BASE / "data/qa_mt_style_report.tsv"

# Unambiguous substring fixes, applied to every Korean value.
GLOBAL_SUBS = [
    # particle / jongseong mistakes (verified against originals)
    ("피스키퍼과", "피스키퍼와"),
    ("피스키퍼이 ", "피스키퍼가 "),
    ("피스키퍼은 ", "피스키퍼는 "),
    ("피스키퍼을 ", "피스키퍼를 "),
    ("피스키퍼으로", "피스키퍼로"),
    ("중력장를", "중력장을"),
    ("효능를", "효능을"),
    ("배율를", "배율을"),
    ("점프력를", "점프력을"),
    ("페로지움를", "페로지움을"),
    ("마이코톡신를", "마이코톡신을"),
    ("연합 시스템를", "연합 시스템을"),
    ("시스템를", "시스템을"),
    ("염소양를", "염소양을"),
    ("부품를", "부품을"),
    ("로봇를", "로봇을"),
    ("릴로돈를", "릴로돈을"),
    ("스너겟를", "스너겟을"),
    ("자격증를", "자격증을"),
    ("크레딧를", "크레딧을"),
    ("으으로", "으로"),
    ("연구실으로", "연구실로"),
    ("시설으로", "시설로"),
    ("식물으로", "식물로"),
    ("반응로으로", "반응로로"),
    ("이리듐로", "이리듐으로"),
    ("바삭한와 소금의 양이 적당합니다", "바삭하고 소금 양도 적당합니다"),
    # spacing glues
    ("수있", "수 있"),
    ("수없", "수 없"),
    ("것같", "것 같"),
    ("을때", "을 때"),
    ("릴때", "릴 때"),
    ("일때", "일 때"),
    # 안 되 / 돼 spelling (ordered: spacing first, then 돼 forms)
    ("안되", "안 되"),
    ("안 되요", "안 돼요"),
    ("안 되죠", "안 돼죠"),
    ("면 되죠", "면 돼죠"),
    # duplicated-word editing errors verified against English/context
    ("인스타 인스타-", "인스타-"),
    ("지역 지역 저장", "지역 저장"),
    ("씨앗 사용 사용", "씨앗 사용"),
    ("방랑자의 방랑자의", "방랑자의"),
    ("지붕 지붕 널", "지붕널"),
    ("무성한 무성한", "무성한"),
    ("완전히 완전히", "완전히"),
    ("특히 특히", "특히"),
    # stray closing parens / leftovers / misc confirmed errors
    ("연막)을", "연막을"),
    ("라이플 223)을", "라이플 223을"),
    ("슈퍼 사격):", "슈퍼 사격:"),
    ("(중))", "(중)"),
    ("응답합니다.)", "응답합니다."),
    ("헤이안 우박폭풍) 역사 문서에", "헤이안 시대의 역사 문서에"),
    ("incoming fire", "날아오는 사격"),
    ("reset됩니다.)", "초기화됩니다. :)"),
    ("스타웃라이브/퀵바미니", "StardutLib/QuickbarMini"),
    ("^gray;(^white;2분^gray;^reset;", "^gray;(^white;2분^gray;)^reset;"),
    ("불탐 ^gray;5초^gray;)", "불탐 ^gray;(^white;5초^gray;)"),
]

# Row-scoped substring fixes keyed by (asset, pointer).
SCOPED = {
    ("/codex/pharitu/pharitu4.codex.patch", "/contentPages/1"): [(
        "하지만 모든 파리투가 다른 사람들과 소통하는 방식입니다), 또는 극한의 거리에서 서로 (그들의 샤크타에 큰 소모가 있습니다) 돌과 금속을 형성하고 심지어 배의 연료 역할을 할 수 있는 고체 물질로 만든 구조물 (배, 물질로 만든 배)을 만들기도합니다.",
        "(불안한 일이지만, 이것이 모든 파리투가 타인과 소통하는 방식입니다). 극한의 거리에 있는 서로와도 소통하고(샤크타에 큰 부담이 되긴 하지만), 돌과 금속을 빚어내며, 심지어 함선의 연료가 될 수 있는 고체 물질 구조물(물질로 만든 함선)을 만들기도 합니다.")],
    ("/codex/pharitu/pharitu4.codex.patch", "/contentPages/4"): [(
        "상상할 수 있습니다). 따라서",
        "상상할 수 있습니다. 따라서")],
    ("/codex/elder/thesubstance.codex.patch", "/contentPages/4"): [(
        "(어쨌든 대부분). 정신이 덜 안정된 사람들에게는 상황이 훨씬 더 어두울 수 있다는 이야기를 들었습니다).",
        "(어쨌든 대부분은요. 정신이 덜 안정된 사람들에게는 상황이 훨씬 더 어두워진다는 이야기를 들었습니다).")],
    ("/codex/nightar/funightardoc1.codex.patch", "/contentPages/2"): [(
        "특색(특히 종교와 관련하여)이 생겼습니다. 이들은 태양을 신격화하지 않고 마을화하는 유일한 종족으로 알려져 있습니다.)",
        "특색(특히 종교 면에서요. 이들은 태양의 측면을 신격화하기는커녕 오히려 악마화하는 유일한 알려진 종족입니다)이 생겼습니다.")],
    ("/codex/other/eblovelywhipscodex.codex.patch", "/contentPages/3"): [
        ("분홍색,^reset;,", "분홍색^reset;,"),
        ("러스트풀 위프,^reset;라", "러스트풀 위프^reset;라")],
    ("/items/throwables/neutronbomb.thrownitem.patch", "/description"): [(
        "절대!^reset;.", "절대!^reset;")],
    ("/interface/objectcrafting/fu_warped1.config.patch", "/gui/lblText/value"): [(
        "??? 를", "???를")],
    ("/interface/objectcrafting/fu_warped3.config.patch", "/gui/lblText/value"): [(
        "??? 를", "???를")],
    # literal escape artifacts (decoded-value level)
    ("/items/generic/crafting/fusioncore.item.patch", "/description"): [(
        "\\\\n", "\n")],
    ("/items/tools/miningtools/darkmatterpickaxe.activeitem.patch", "/description"): [(
        "\\\\n", "\n")],
    ("/objects/CCR/terrariums/critters/glitchscab/crittercage.object.patch", "/description"): [(
        "\\두개골\\\"", "\"두개골\"")],
    ("/objects/CCR/terrariums/critters/glitchscab/wallcage.object.patch", "/description"): [(
        "\\두개골\\\"", "\"두개골\"")],
    ("/objects/nmm_generic/rooftopbillboards/billboardbeautifulattempt.object.patch", "/hylotlDescription"): [(
        "\\n", "\n")],
    ("/objects/upgrade/techconsole/techconsole.object.patch", "/description"): [(
        "\\n", "\n")],
}


def fix_double_space(ko):
    return re.sub(r"(?<=[^ \n]) {2,}(?=[^ \n])", " ", ko)


def fix_tag_space(ko):
    # space before ^reset; followed by tag/colon/end: stray inside-span tail space
    ko = re.sub(r" \^reset;(?=[\s^:]|$)", "^reset;", ko)
    # space before ^reset; followed by text: relocate separator outside the span
    ko = re.sub(r" \^reset;", "^reset; ", ko)
    # space right after an opening tag: inside-span leading space
    ko = re.sub(r"(\^(?!reset\b)[a-zA-Z#0-9]+;) ", r"\1", ko)
    return re.sub(r" {2,}", " ", ko)


def fix_punct(ko):
    ko = re.sub(r"\.{2}(?!\.)", "...", ko)
    ko = re.sub(r"[!?]\.(?!\.)", lambda m: m.group(0)[0], ko)
    ko = ko.replace(",,", ",")
    ko = ko.replace(";;", ";")
    # stray period immediately after a colour tag (KO added; EN had none)
    ko = re.sub(r"(\^[a-zA-Z#0-9]+;)\.", r"\1", ko)
    return ko


def fix_space_punct(ko):
    ko = re.sub(r" (\^[a-zA-Z#0-9]+;)([.,!?])", r"\1\2", ko)
    ko = re.sub(r" ([.,])(?=[ \n^]|$)", r"\1", ko)
    return ko


RULES = {
    "DOUBLE_SPACE": fix_double_space,
    "TAG_SPACE": fix_tag_space,
    "PUNCT": fix_punct,
    "SPACE_PUNCT": fix_space_punct,
}


def main():
    flagged = defaultdict(list)
    with REPORT.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            if row["kind"] in RULES:
                flagged[(row["asset"], row["pointer"])].append(row["kind"])

    changes = defaultdict(dict)
    with PAIRS.open(encoding="utf-8-sig", newline="") as fh:
        for row in csv.DictReader(fh, delimiter="\t"):
            ko = row["korean"]
            new = ko
            # scoped fixes first: their anchors may contain text that global rules alter
            for old, rep in SCOPED.get((row["asset"], row["pointer"]), ()):
                if old in new:
                    new = new.replace(old, rep)
            for old, rep in GLOBAL_SUBS:
                if old in new:
                    new = new.replace(old, rep)
            for kind in flagged.get((row["asset"], row["pointer"]), ()):
                new = RULES[kind](new)
            if new != ko:
                changes[(row["asset"], row["pointer"])][ko] = new

    print(f"rows to change: {sum(len(v) for v in changes.values())} in {len(changes)} pointers")

    pak = Pak(str(TARGET_PAK))
    overrides = {}
    changed = 0
    missed = []
    for asset in {a for a, _ in changes}:
        doc = json.loads(pak.read(asset))
        stack = list(doc)
        found = False
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(item)
            elif isinstance(item, dict) and item.get("op") == "replace" and isinstance(item.get("value"), str):
                rep = changes.get((asset, item.get("path")), {}).get(item.get("value"))
                if rep is not None:
                    item["value"] = rep
                    changed += 1
                    found = True
        if found:
            overrides[asset] = json.dumps(doc, ensure_ascii=False, indent=2).encode("utf-8")
        else:
            missed.append(asset)

    expected = sum(len(values) for values in changes.values())
    print(f"changed {changed} fields; expected {expected}; assets untouched {len(missed)}")
    for a in missed:
        print("  MISS", a)
    del pak
    count = write_pak(TARGET_PAK, TARGET_PAK, overrides)
    print(f"wrote pak; entries {count}")


if __name__ == "__main__":
    main()
