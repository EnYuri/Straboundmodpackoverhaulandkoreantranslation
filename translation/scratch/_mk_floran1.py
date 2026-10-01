# -*- coding: utf-8 -*-
import sys, io, csv

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
csv.field_size_limit(10**7)

KO = [
    "이상한 화면 판넬이다아.",
    "미끈한 고기다.",
    "플로란 알록달록한 결정체 모아야 한다.",
    "알록달록한 네온이 든 블록.",
    "사탕에 색깔 줄무늬 있다.",
    "플로란 초록 그림 좋아해엇.",
    "말랑말랑 미끈미끈한 살이다.",
    "끈적한 거미줄. 플로란은 거미가 위대한 사냥꾼이라 생각해엇!",
    "플로란 빛나는 문양 좋아해엇.",
    "새겨진 돌벽돌이다.",
    "예쁜 보라색 수정이다.",
    "놋쇠로 만든 발판이다.",
    "청동으로 만든 발판이다.",
    "플로란 별빛 통나무 벽 좋아해엇.",
    "모래 같은, 빛나는 사암 돌이다.",
    "지옥 벽돌로 만든 발판. 징그럽다.",
    "살로 만든 끈적한 더러운 발판이다.",
    "반짝이는 유리 레일. 안전한 거에엇?",
    "반짝이는 레일이다.",
    "갈색 모래다.",
    "끈적한 꿀벌 밀랍이다.",
    "플로란 초록 돌 좋아해엇.",
    "붉은 돌은 냄새가 이상해엇.",
    "플로란 초록 모래에서 놀고 싶어엇.",
    "플로란 바보 같은 갈색 돌 좋아해엇.",
    "돌은 철로 만들어졌다.",
    "플로란 버섯 뿌리 싫어해엇. 버섯은 플로란의 적이다.",
    "단단한 갈색 돌이다.",
    "버섯 냄새 이상해엇. 플로란 으깨고 싶어엇.",
]

leaf = "floranDescription"
rows = list(csv.DictReader(open("data/uncov_batch/" + leaf + ".tsv", encoding="utf-8-sig"), delimiter="\t"))
assert len(rows) == len(KO), (len(rows), len(KO))
w = csv.writer(open("data/_uncov_ko_floran1.tsv", "w", encoding="utf-8", newline=""), delimiter="\t")
w.writerow(["en", "ko"])
for r, ko in zip(rows, KO):
    w.writerow([r["en"], ko])
print("floran1", len(KO))
