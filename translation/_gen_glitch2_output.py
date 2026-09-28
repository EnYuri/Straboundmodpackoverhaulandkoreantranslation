import csv

# old_korean -> (new_korean, note)
FIXES = {
    "당황. 할 말이 없습니다!": ("당황. 할 말이 없다!", None),
    "전시용입니다.": ("전시용이다.", "감정어 접두사 없이 사실 서술만 있는 원문(EN도 감정어 없음) - 어미만 평서체로 수정"),
    "스머그. 텔레포터. 순간이동 중에 절전 모드로 들어갈 수 있어요.": (
        "거만. 텔레포터. 순간이동 중에 절전 모드로 들어갈 수 있다.",
        "Smug 음역 '스머그'는 한국어 명사가 아님 -> '거만'으로 교체",
    ),
    "역겹네요. 썩어가는 물질입니다.": (
        "혐오. 썩어가는 물질이다.",
        "동일 EN(Disgusted)의 다른 자산은 '혐오'를 쓰는데 이 자산만 형용사형 어미 '역겹네요' -> 통일",
    ),
    "혐오. 이 상자는 구역질나는 썩은 재료로 만들어졌어요.": ("혐오. 이 상자는 구역질나는 썩은 재료로 만들어졌다.", None),
    "중립. 송신기예요.": ("중립. 송신기다.", None),
    "관찰 결과. 아발리의 깃발은 원 아이콘에 날개를 모티브로 한 것 같습니다.": (
        "관찰. 아발리의 깃발은 원 아이콘에 날개를 모티브로 한 것 같다.",
        "감정어는 명사 한 단어 규칙 -> '관찰 결과'를 '관찰'로 축약",
    ),
    "매혹적. 상단 또는 'Enable' 노드는 래치가 하단 또는 'Data' 노드를 기준으로 상태를 변경할 수 있는지 여부를 제어합니다.": (
        "매혹. 상단 또는 'Enable' 노드는 래치가 하단 또는 'Data' 노드를 기준으로 상태를 변경할 수 있는지 여부를 제어한다.",
        "본문이 EN(A Latch. Can be used to store a wire state.)보다 훨씬 상세한 실제 D-래치 핀 동작 설명으로 대체돼 있으나, "
        "실제 게임 오브젝트 동작과 일치하는 의도적 보강 설명으로 보여 내용은 유지하고 어미와 감정어 형태만 수정함",
    ),
    "관찰. 'OR'/ 게이트. 작동하려면 최소 1개의 입력이 /'켜져'/ 있어야 합니다.": (
        "기쁨. 'OR'/ 게이트. 작동하려면 최소 1개의 입력이 /'켜져'/ 있어야 한다.",
        "EN 감정어는 'Pleased'인데 번역 감정어가 무관한 '관찰'로 돼 있어 '기쁨'으로 교정 + 어미 수정",
    ),
    "신남. 이미 강력한 무기를 여기서 업그레이드할 수 있어요!": ("신남. 이미 강력한 무기를 여기서 업그레이드할 수 있다!", None),
    "편안하죠. 누구나 이런 의자를 가져야 합니다.": ("편안. 누구나 이런 의자를 가져야 한다.", None),
    "편안하죠. 누구나 이런 소파를 가져야 해요.": ("편안. 누구나 이런 소파를 가져야 한다.", None),
    "걱정. 여보세요? 여기 누구 있나요?": ("걱정. 여보세요? 여기 누구 있나?", None),
    "낙관적. 매달린 수납장. 유용합니다.": ("낙관. 매달린 수납장. 유용하다.", None),
    "정보. 표준 선박 문입니다.": ("정보. 표준 선박 문이다.", None),
    "중립. 낯익은 구릉 지대입니다.": ("중립. 낯익은 구릉 지대다.", None),
    "중립. 바람이라는 자연 원소의 상징이 그려진 커다란 색판입니다.": ("중립. 바람이라는 자연 원소의 상징이 그려진 커다란 색판이다.", None),
    "중립. 대지라는 자연 원소의 상징이 그려진 커다란 색판입니다.": ("중립. 대지라는 자연 원소의 상징이 그려진 커다란 색판이다.", None),
    "중립. 불이라는 자연 원소의 상징이 그려진 커다란 색판입니다.": ("중립. 불이라는 자연 원소의 상징이 그려진 커다란 색판이다.", None),
    "중립. 물이라는 자연 원소의 상징이 그려진 커다란 색판입니다.": ("중립. 물이라는 자연 원소의 상징이 그려진 커다란 색판이다.", None),
    "감사. 텔레비전은 진정 인류의 가장 위대한 업적 중 하나입니다.": ("감사. 텔레비전은 진정 인류의 가장 위대한 업적 중 하나다.", None),
}

NO_CHANGE = {
    "실망. 이 유리 패널은 홀로그램이 아니다.",  # already plain -다, heuristic false positive on "아니다"
    "관찰. 이 컵에 든 우유는 무시의 것이 아니다.",  # same false positive
}

rows = []
with open("glitch_rewrite_2.tsv", encoding="utf-8-sig") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        rows.append(row)

out_rows = []
unmatched = []
for row in rows:
    ko = row["korean"]
    if ko in NO_CHANGE:
        continue
    if ko in FIXES:
        new_ko, note = FIXES[ko]
        out_rows.append([row["asset"], row["pointer"], ko, new_ko, note or ""])
    else:
        unmatched.append(row)

print("total input rows:", len(rows))
print("output fix rows:", len(out_rows))
print("no-change (false positive):", sum(1 for r in rows if r["korean"] in NO_CHANGE))
print("unmatched (should be 0):", len(unmatched))
for u in unmatched:
    print("UNMATCHED:", u["asset"], u["korean"][:60])

with open("glitch_rewrite_2_output.tsv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["asset", "pointer", "old_korean", "new_korean", "note"])
    for r in out_rows:
        w.writerow(r)

print("wrote glitch_rewrite_2_output.tsv")
