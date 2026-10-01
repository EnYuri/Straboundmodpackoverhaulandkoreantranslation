"""Apply reviewed, source-aware glossary normalisations from qa_glossary_report.tsv."""
import csv
from collections import defaultdict

REPORT = "data/qa_glossary_report.tsv"


def replace_for(term, text):
    # These apply only to rows which the QA report confirmed contain the English term.
    substitutions = {
        "Shortsword": [("숏소드", "소검")],
        "Hylotl": [("하일로틀", "하이로틀")],
        "Protectorate": [("테렌 보호령", "행성 보호국"), ("프로텍토레이트", "보호국"), ("보호령", "보호국")],
        "Aegisalt": [("이지스알트", "에지솔트"), ("에기살트", "에지솔트")],
        "Aegi": [("아에기", "에지")],
        "Sniper Rifle": [("저격 소총", "저격소총")],
        "Miniknog": [("미니노그", "미니크노그")],
        "Alt Fire": [("대체 발사", "보조 발사"), ("보조 공격", "보조 발사"), ("보조 사격", "보조 발사")],
        "Peacekeeper": [("피스키퍼", "평화유지군")],
        "Violium": [("바이올리움", "바이올륨")],
        "Poptop": [("팝탑", "팝톱")],
        "Cultivator": [("재배자", "컬티베이터"), ("경작자", "컬티베이터")],
        "Teleporter": [("순간이동 장치", "텔레포터")],
        "Saturnian": [("새턴인", "새터니안")],
        "sanctilite": [("생틸라이트", "생크틸라이트")],
        "Occasus": [("오카수스", "오카서스")],
        "Crit Chance": [("치명타율", "치명타 확률")],
        "Magishot": [("마기샷", "매지샷")],
        "Stability": [("안정도", "안정성")],
        "Matter Manipulator": [("매터 매니퓰레이터", "물질 조작기")],
        "Manipulator Module": [("조작기 모듈", "물질 조작기 모듈")],
        "Novakid": [("노바킨", "노바키드")],
        "Parry": [("받아넘기기 판정 시간", "패링 창"), ("받아넘기기", "패링"), ("받아넘길 수 있다", "패링할 수 있다")],
        "Parry Window": [("받아넘기기 판정 시간", "패링 창"), ("패링 판정 시간", "패링 창")],
        "Tech Card": [("기술 카드", "테크 카드")],
        "Terrene Protectorate": [("테렌 보호령", "행성 보호국")],
        "Grand Protector": [("대보호관", "대보호자")],
        "United Systems": [("유나이티드 시스템즈", "연합 시스템")],
        "wood-warder": [("숲의 수호자", "숲의 파수꾼")],
        "Thaumoth": [("사우모스", "타우모스")],
        "The Ruined": [("폐허 인간", "루인드")],
        "Portal": [("포탈", "포털")],
        "Aurea Seekers": [("아우레아 시커", "아우레아 탐구자")],
        "Relic Seeker": [("렐릭 시커", "유물 탐구자")],
        "Union flag": [("아에기니안 연방 국기", "아에기니안 연방 유니언 깃발")],
        "Codex": [("도감", "코덱스")],
        "Perfect Block": [("완벽 방어", "퍼펙트 블록")],
        "Grenade Launcher": [("유탄발사기", "유탄 발사기")],
    }
    for before, after in substitutions.get(term, []):
        text = text.replace(before, after)
    return text


by_file = defaultdict(dict)
with open(REPORT, encoding="utf-8-sig", newline="") as f:
    for row in csv.DictReader(f, delimiter="\t"):
        updated = replace_for(row["englishTerm"], row["koreanText"])
        if updated != row["koreanText"]:
            by_file["translations/" + row["file"]][row["id"]] = updated

changed = 0
for path, replacements in by_file.items():
    with open(path, encoding="utf-8-sig", newline="") as f:
        rows = list(csv.reader(f, delimiter="\t"))
    for row in rows:
        if row and row[0] in replacements:
            row[1] = replacements[row[0]]
            changed += 1
    with open(path, "w", encoding="utf-8-sig", newline="") as f:
        csv.writer(f, delimiter="\t", lineterminator="\n").writerows(rows)

print(f"reviewed replacements: {changed}")
