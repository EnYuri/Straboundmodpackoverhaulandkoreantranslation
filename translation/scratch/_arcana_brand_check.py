# Cross-check that EN set/brand names map to the right KO set names per row.
import io
import re
import sys

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

ko = {}
for line in open("data/arcana_ko.tsv", encoding="utf-8"):
    p = line.rstrip("\n").split("\t")
    if len(p) == 2:
        ko[int(p[0])] = p[1]

uniq = {}
cur = None
buf = []
for line in open("scratch/_arcana_uniq.txt", encoding="utf-8"):
    m = re.match(r"### (\d+) x(\d+)", line)
    if m:
        if cur is not None:
            uniq[cur] = "\n".join(buf).rstrip("\n")
        cur = int(m.group(1))
        buf = []
    else:
        buf.append(line.rstrip("\n"))
uniq[cur] = "\n".join(buf).rstrip("\n")

BRANDS = [
 (r"Horizon","호라이즌"),(r"Aeon","에이언"),(r"Aegis","아이기스"),(r"Aeternus","에테르누스"),
 (r"Alchemilla","알케밀라"),(r"Anima","아니마"),(r"Architect","아키텍트"),(r"Ariorift","아리오리프트"),
 (r"Astraea","아스트라이아"),(r"Astromancer","아스트로맨서"),(r"Baldr","발드르"),(r"Borrhas","보르하스"),
 (r"Catalyst|Catalytic","촉매"),(r"Chevalier","슈발리에"),(r"Corekeeper","코어키퍼"),(r"Cryptspurn","크립트스펀"),
 (r"Embryonic","엠브리오닉"),(r"Evanescent","에버네선트"),(r"Frostclad","프로스트클래드"),(r"Fusang","푸상"),
 (r"Goldmonger","골드몽거"),(r"Graverotten","그레이브로튼"),(r"Heartseeker","하트시커"),(r"Horncaster","혼캐스터"),
 (r"Invisible","투명"),(r"Iron Flower","아이언 플라워"),(r"Lepidoptera","레피돕테라"),(r"Mist Rider","미스트 라이더"),
 (r"Morphosis","모포시스"),(r"Offworld","오프월드"),(r"Parasitic","파라시틱"),(r"Pearl","진주"),
 (r"Prima","프리마"),(r"Roboticist","로보티시스트"),(r"Royalty","로열티"),(r"Scholar","학자"),
 (r"Serpent","서펀트"),(r"Skullbearer","스컬베어러"),(r"Sleepwalker","슬립워커"),(r"Liberator","해방자"),
 (r"Disciple","제자"),(r"Voltabolt","볼타볼트"),(r"Ice Knight","아이스 나이트"),(r"Ice Mage","아이스 메이지"),
 (r"Ice Elite","아이스 나이트"),(r"Heishe","헤이셰"),(r"Lushe","루쉬"),(r"Shuying","슈잉"),
 (r"Scrapdiver","스크랩다이버"),(r"Scrapsewn","스크랩숀"),(r"Verrostin","베로스틴"),(r"Cradling","포대기"),
 (r"Duskkin","더스킨"),(r"Faetheri","페더리"),(r"Florahusk","플로라허스크"),(r"Greyshell","그레이셸"),
 (r"Revenant","레버넌트"),(r"Wraith","레이스"),(r"Machinist","기계공"),(r"Gearshift","기어시프트"),
 (r"Corebreaker","코어브레이커"),(r"Omenkyrie","오멘키리"),(r"Onyx","오닉스"),(r"Demise","디마이즈"),
 (r"Pyrocraze","파이로크레이즈"),(r"Cryocraze","크라이오크레이즈"),(r"Blood Assassin","블러드 어새신"),
 (r"Butcher","도살자"),(r"Erexeno","에렉세노"),(r"Nordwulf","노르드울프"),(r"Soldat","졸다트"),
 (r"Wachter","바흐터"),(r"Aurea","아우레아"),(r"Seeker","시커"),(r"Beholder","비홀더"),
 (r"Brightguard","브라이트가드"),(r"Brightlite","브라이트라이트"),(r"Inquisitor","심문관"),
 (r"Seraph","세라프"),(r"Zealot","광신도"),(r"Devotee","신도"),(r"Gralsyg","그랄시그"),
 (r"Arca","아르카"),(r"Electromage","일렉트로메이지"),(r"Technomancer","테크노맨서"),
 (r"Starglim","스타글림"),(r"Starwalker","스타워커"),(r"Magnate","매그네이트"),(r"Oceanite","오셔나이트"),
 (r"Runic","루닉"),(r"Apprentice","수습생"),(r"Titancorp","타이탄코프"),(r"Scorpio","스콜피오"),
 (r"Aneides","아네이데스"),(r"Winter Frog","윈터 프로그"),(r"Chemhyde","켐하이드"),(r"Portobell","포토벨"),
 (r"Virismoke","비리스모크"),(r"Anarkyon","아나르콘"),(r"Exousian","엑수시안"),(r"Orion","오리온"),
 (r"Gilten","길텐"),(r"Arcanian","아르카니안"),(r"Solar","태양"),(r"Azure","아주르"),
]

bad = []
for i in sorted(uniq):
    en, k = uniq[i], ko.get(i, "")
    for pat, kw in BRANDS:
        en_has = bool(re.search(pat, en, re.I))
        ko_has = kw in k
        if en_has and not ko_has:
            bad.append((i, f"EN has {pat} but KO lacks {kw}", en[:60], k[:60]))
        elif ko_has and not en_has:
            bad.append((i, f"KO has {kw} but EN lacks {pat}", en[:60], k[:60]))
for b in bad:
    print(b)
print("total:", len(bad))
