"""Fix pass over translation batches based on QA findings.

1. Global token normalization (match legacy Korean conventions):
   [보조 발사]->[ALT-FIRE], [발사]->[FIRE]/[Fire] (per source case),
   [좌클릭]->[LEFT-MOUSE], [하의]->[다리], [불이익]->[페널티],
   [발동]/[활성]->[활성화됨], 안정도->안정성
2. Per-entry rewrites for truncated/wrong translations.
3. Restore nested ^#C8FAFA; highlight tags.
4. Positional blank-line restore for newline-count mismatches.
"""
import csv, re, glob, os

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
rows = list(csv.DictReader(open(f"{BASE}/worklist_new.tsv", encoding="utf-8-sig"), delimiter="\t"))

REWRITES = {
258: "''그들은 한심한 무리였네. 밀주를 마시고 고철을 두고 싸우며 시간을 낭비했지. 술 한 단지를 바치자 바로 관심을 보였지만, 그들의 눈에서 배신을 읽었네. 돌아서는 순간 하나가 내 갑옷에 돌을 던졌지. 미친 건가?''\n\n^#FFEEC6;회피 연타 [SHIFT]: 빠른 연속 타격을 시작해 공격 중 무적 프레임 획득 | 재사용 대기 20초.^white;",
275: "다네가시마 조총을 짧게 줄인 변형으로, 피해량을 희생해 한 손으로 쓸 수 있습니다. 일 쇼구나테는 그런 권총이 원거리에서 불안정해지므로 소총 단축을 종종 금지합니다. 하지만 많은 장교와 사무라이는 그냥 '분실'로 처리하고 더 요청하면 되므로 눈감아주는 경향이 있습니다. 뭐, 예전엔 그랬죠. 산탄 장전.\n^#DD765F;적중 확률이 치명타 확률로 대체(모든 탄환이 항상 적중) | 치명타 사격이 탄환 종류에 따라 다른 효과 | 무섭도록 부정확하지만, 평균 이상의 치명타율과 피해.^reset;",
323: "군과 민간 시장 양쪽에서 널리 쓰인 견실한 9mm 권총 설계입니다. 오늘날에도 다르지 않아서, MK.3는 인류 우주의 거의 모든 곳에서 발견됩니다.\n브라우닝 9x19mm 탄창을 급탄합니다.\n^green;Shift를 두 번 눌러 다용도 한 손 그립으로 전환합니다.^reset;",
1302: "'스탯 잠금' 돌격소총입니다. 발사 시 소스 엔티티에 (설정 가능한) 상태 효과를 적용하며, 특정 스탯이 값 1이면 발사/재장전을 허용하지 않습니다.\n명시된 스탯이 활성화되면 선택적으로 다른 빗나감/명중 탄환 세트로 전환합니다.",
1435: "원래 정비 작업용이던 무거운 도구입니다. 한때 대형 채광 장비를 고쳤지만, 이제는 언데드와의 싸움에 쓰입니다.\n^orange;2번째와 마지막 타격이 반사(근접 저항). 마지막 타격은 곡괭이 머리로 전환해 대상에 스파이크를 긁어 높은 베기 피해.\n^yellow;패링 [ALT-FIRE]: 0.6초 패링 창 | 안정성 30HP.^white;\n^#FFEEC6;회전 찌르기 [SHIFT]: 잭을 빠르게 앞으로 찔러 2초 휘청임과 5초 숨가쁨 부여 | 재사용 대기 25초.^white;",
1596: ".233 레밍턴탄 한 발입니다.",
2224: "장신구를 넣을 수 있습니다. 장신구는 장신구 추출기 정거장에서 추출해야 합니다.\n\n",
4839: "아서 일족은 모든 근접 무기에 낯설지 않지만, 중철퇴는 도끼와 함께 주력 중 하나입니다.\n\n^orange;첫 타격이 2초 숨가쁨 부여 (타격 저항과 전사 피해 -25%) | 2번째와 마지막 타격이 반사(근접 저항). 마지막 타격은 더 긴 창으로 반사.\n^yellow;패링 [ALT-FIRE]: 0.6초 패링 창 | 안정성 30HP.^white;\n^#FFEEC6;회전 휩쓸기 [SHIFT]: 앞을 쓸어 3초 휘청임과 7초 숨가쁨 부여 | 재사용 대기 35초.^white;",
4840: "아서 일족은 모든 근접 무기에 낯설지 않지만, 중철퇴는 도끼와 함께 주력 중 하나입니다.\n\n^orange;2번째와 마지막 타격이 반사(근접 저항). 마지막 타격은 더 긴 창으로 반사하고 4초 숨가쁨 부여 (타격 저항과 전사 피해 -25%).\n^yellow;패링 [ALT-FIRE]: 0.6초 패링 창 | 안정성 30HP.^white;\n^#FFEEC6;회전 휩쓸기 [SHIFT]: 앞을 쓸어 3초 휘청임과 7초 숨가쁨 부여 | 재사용 대기 35초.^white;",
5645: "회전 찌르기",
2201: "영혼의 짐 - ^orange;^#C8FAFA;어떤 피격 방패든^orange; 활성이면 영혼을 소환해 적 공격^reset; | ^red;피격 방패가 재사용 대기 중이면 영혼이 대신 플레이어를 공격하려 함.^reset;",
2386: "코어 부스터 - ^orange;^#C8FAFA;활성 피격 방패^orange;마다 숙련도 +10%, 초당 HP +1, 최대 MP +10 획득^reset; | 1단 보너스.",
2387: "코어 부스터 - ^orange;^#C8FAFA;활성 피격 방패^orange;마다 숙련도 +10%, 초당 HP +1, 최대 MP +10 획득^reset; | 2단 보너스.",
2388: "코어 부스터 - ^orange;^#C8FAFA;활성 피격 방패^orange;마다 숙련도 +10%, 초당 HP +1, 최대 MP +10 획득^reset; | 3단 보너스.",
2389: "코어 부스터 - ^orange;^#C8FAFA;활성 피격 방패^orange;마다 숙련도 +10%, 초당 HP +1, 최대 MP +10 획득^reset; | 4단 보너스.",
2390: "코어 부스터 - ^orange;^#C8FAFA;활성 피격 방패^orange;마다 숙련도 +10%, 초당 HP +1, 최대 MP +10 획득^reset; | 최대 5단 보너스.",
2391: "코어 부스터 - ^orange;^#C8FAFA;활성 피격 방패^orange;마다 숙련도 +10%, 초당 HP +1, 최대 MP +10 획득^reset; | ^orange;최대 5단 보너스까지 중첩(숙련도 +75%).^reset;",
2392: "코어 부스터 - ^orange;^#C8FAFA;활성 장신구 피격 방패^orange;마다 무기 숙련도 +15% 획득^reset; | ^yellow;갑옷 피격 방패 영향 없음.^reset;",
2409: "위기 반지 - ^orange;HP가 40% 미만일 때 한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 2.5초.^reset;",
2410: "위기 반지 [활성화됨] - ^orange;HP가 40% 미만일 때 한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 2.5초.^reset;",
2500: "신성 기사 - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 15초 | 피격 방패 상태에 의존하는 다른 효과를 발동시키거나 영향 주지 않음.^reset;",
2603: "평형 엔진 - ^orange;^#C8FAFA;재사용 대기 중인 장신구 피격 방패^orange;마다 최대 HP +20과 초당 HP +2 획득^reset; | ^yellow;갑옷 피격 방패 영향 없음.^reset;",
2872: "황금 십자가 - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 55초 | 재사용 대기 진입 시 2초간 피해 면역 발동.",
3326: "보병 졸병 [흉갑] - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 60초 | 다른 ^#C8FAFA;피격 방패^reset;와 중첩.",
3328: "보병 졸병 [머리] - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 60초 | 다른 ^#C8FAFA;피격 방패^reset;와 중첩.",
3330: "보병 졸병 [다리] - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 60초 | 다른 ^#C8FAFA;피격 방패^reset;와 중첩.",
3845: "네드 켈리 [흉갑] - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 45초 | 다른 ^#C8FAFA;피격 방패^reset;와 중첩.",
3847: "네드 켈리 [머리] - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 45초 | 다른 ^#C8FAFA;피격 방패^reset;와 중첩.",
3849: "네드 켈리 [다리] - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 45초 | 다른 ^#C8FAFA;피격 방패^reset;와 중첩.",
4783: "신성한 보호의 부적 - ^orange;한 번의 피격을 흡수하는 ^#C8FAFA;피격 방패^orange; 층 획득 | 재사용 대기 70초 | 재사용 대기 진입 시 부적 탄막 생성.",
3670: "마쿠 심장 - ^orange;^#C8FAFA;피격 방패^orange;가 재사용 대기 중이면 ^#C8FAFA;2x 추가 피격 방패^orange; 층 충전 시작, 각각 재사용 대기 15초^reset;",
621: "2차 대전 나치 독일의 악명 높은 군용 기관단총으로, 국방군과 무장친위대 양쪽의 분대장과 장교가 주로 사용했습니다. 대전 후에는 독일 밖에서도 널리 쓰여 지구 거의 모든 곳에 MP-40 하나쯤은 있었습니다. 전반적으로 견실한 9mm 기관단총입니다.\n\n9x19mm 파라벨럼을 급탄합니다.",
624: "독일 연방군의 오랜 제식 소총으로, *지금도* 많은 식민지 군대가 사용합니다. 거의 어디서나 쓸 수 있는 튼튼하고 믿음직한 무기로 이름을 떨쳤습니다. 7.62x51mm는 무겁지만, G3에서 나오는 탄이라면 이보다 나쁠 순 없죠. 이것과 사촌격인 FAL이 아직 현역이라는 사실이 두 소총의 증거입니다.\n\nG3 7.62x51mm 탄창을 장전합니다.\n^green;\"보조 발사\"를 길게 누르면 완전 자동과 반자동을 전환합니다.^reset;",
4955: "수백만 나치와 왜구를 죽인 멋진 공수총. 매우 멋지고 기반 있어요. 제 유튜브와 패트리-\n\n.30 카빈(7.62x33mm) 탄창 사용.\n^orange;터무니없이 높은 기본 정확도와 적중 확률.^reset;\n^green;\"보조 발사\"를 눌러 자동과 반자동 전환.^reset;",
}

def fix_tokens(dst, src):
    dst = dst.replace("[보조 발사]", "[ALT-FIRE]")
    dst = dst.replace("[좌클릭]", "[LEFT-MOUSE]")
    dst = dst.replace("[하의]", "[다리]")
    dst = dst.replace("[불이익]", "[페널티]")
    dst = dst.replace("[발동]", "[활성화됨]").replace("[활성]", "[활성화됨]")
    dst = dst.replace("안정도", "안정성")
    if "[발사]" in dst:
        if "[FIRE]" in src: dst = dst.replace("[발사]", "[FIRE]")
        elif "[Fire]" in src: dst = dst.replace("[발사]", "[Fire]")
    return dst

def align_newlines(src, dst):
    """Reinsert blank lines positionally to match src structure."""
    sl, dl = src.split("\n"), dst.split("\n")
    s_ne = [l for l in sl if l.strip()]
    d_ne = [l for l in dl if l.strip()]
    if len(s_ne) != len(d_ne):
        return None
    it = iter(d_ne)
    return "\n".join("" if not l.strip() else next(it) for l in sl)

# load batches into {file: {idx: text}}
files = sorted(glob.glob(f"{BASE}/translations/batch_*.tsv"))
changed = []
for path in files:
    entries = {}
    order = []
    cur = None
    for line in open(path, encoding="utf-8"):
        line = line.rstrip("\n")
        m = re.match(r"^(\d+)\t(.*)$", line)
        if m:
            cur = int(m.group(1)); entries[cur] = m.group(2); order.append(cur)
        elif cur is not None:
            entries[cur] += "\n" + line
    dirty = False
    for idx in order:
        src, dst = rows[idx]["englishText"], entries[idx]
        orig = dst
        if idx in REWRITES:
            dst = REWRITES[idx]
        else:
            dst = fix_tokens(dst, src)
            if src.count("\n") != dst.count("\n"):
                fixed = align_newlines(src, dst)
                if fixed is not None:
                    dst = fixed
                else:
                    print(f"NEWLINE-UNRESOLVED {idx} src={src.count(chr(10))} dst={dst.count(chr(10))}")
        if dst != orig:
            entries[idx] = dst; dirty = True
    if dirty:
        with open(path, "w", encoding="utf-8", newline="") as f:
            for idx in order:
                f.write(f"{idx}\t{entries[idx]}\r\n")
        changed.append(os.path.basename(path))

print("changed files:", len(changed))
for c in changed: print(" ", c)
