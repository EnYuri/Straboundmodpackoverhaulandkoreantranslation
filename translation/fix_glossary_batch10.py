"""Tenth fix batch (2026-09-29). Origin: continued manual STYLE_MIX review of
group1-remainder assets — /dialog/bartenderwoofie.config.patch (273),
/dialog/lucario.config.patch (285), /dialog/saturnspaceconverse.config.patch
(283), /dialog/avikanoutpost.config.patch (268) — plus a corpus-wide Glitch
emotion-prefix scan (177 confirmed conjugated/adverbial prefixes normalized to
the nominal form required by the Glitch convention).

All pairs verified against pak_pairs.tsv before fixing.

A. Glitch emotion prefix sweep (auto-generated from _prefix_violations.json):
   every "<Emotion>. <body>" EN line whose KO prefix is a conjugated verb or
   adverb ("위협적이긴.", "궁금하네.", "감명받았긴.", ...) instead of a nominal
   ("위협.", "호기심.", "감명.", ...) is rewritten to the corpus-dominant or
   stem-nominalized form. ~166 instances across ~40 assets.

B. bartenderwoofie (8): deed->증서 unification (2), grammar fixes (4),
   Fluffalo->플루팔로 (1), "Passive or not" mistranslation (1).

C. lucario (76): the whole bank was written in a clipped telegraphic draft
   style with dropped particles; confirmed broken readings and one real
   mistranslation ("flavor" -> "취향") rewritten into natural sentences.
   Also 보호국와 -> 보호국과 particle fix, 나나 -> 내나.

D. saturnspaceconverse (26): 미니크녹다/미니크녹가 -> 미니크녹이다/미니크녹이,
   stutter rendering fix, hymenopteran "벌목" -> "막시목" (order name, not
   logging), Apiarian "어피어리언" -> "아피아리안", Nebulac "네뷸락" ->
   "네뷸랙", stims "자극제" -> "스팀" (TM), clipped sentences completed.

E. avikanoutpost (34): "I have nothing to say to you" mistranslation
   ("지금은 바쁘니 나중에 얘기하죠"), floran self-reference inserted into an
   avikan line, clipped sentences completed, plus term unification:

   - Starfarer's Refuge: 스타페어러의 피난처 (85x) vs 스타파어러 (22x) /
     스타파러 (3x) -> unified to 스타페어러.
   - Vas Vha'leih: 바스 브할레이 (48x) vs 바스 바레이 (13x) / 바스 브알레이
     (5x) -> unified to 브할레이.
   - the Watchers (Avikan org): 감시자들/감시자 (dominant, "Watcher Agent" ->
     감시자 요원, "Watchers' emblem" -> 감시자의 문장) vs 워처/와처/감시자단
     org references -> unified to 감시자들. Monster names (야라 워처,
     히프노틱 워처) untouched.
   - Avikan flaps: 덮개 (55x) vs 날개막 (1x) -> 덮개.
   - Alien Interaction Protocol: 외계인 상호작용 규약 (2x) vs 외계 상호작용
     규약/외계인 상호작용 프로토콜 -> unified to 외계인 상호작용 규약.
   - the Council: 평의회 (avikan-avikan block 3x) vs 의회 (1x) -> 평의회.
"""
import json
import re
import struct
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent
SRC_PAK = STAR / "mods" / "female_translation.pak"
OUT_PAK = BASE / "female_translation.pak.NEW14"

# ---------------------------------------------------------------------------
# A. Glitch emotion-prefix nominalization (generated, full-string pairs)
# ---------------------------------------------------------------------------
PREFIX_NOMINAL = {
    "위협적이긴": "위협", "분개했긴": "분개", "환영해": "환영",
    "감명받았긴": "감명", "궁금하네": "궁금함", "궁금해": "궁금함",
    "궁금하네요": "궁금함", "궁금하긴": "호기심", "흥미롭군": "흥미",
    "흥미롭긴": "흥미", "위압적이긴": "위압", "절박해": "절박",
    "기대되네요": "기대", "실망했다": "실망", "정통하긴": "정통",
    "지루해": "지루함", "짜증 났긴": "짜증", "단호하게": "단호",
    "결심했다": "결심", "결의에 찬다": "결의", "끈질기긴": "고집",
    "동요하며": "동요", "거만하긴": "거만", "걱정되네": "걱정",
    "걱정된다": "걱정", "걱정돼": "걱정", "용감하게": "용감",
    "격분했긴": "격분", "유익하긴": "유익함", "유혹적이긴": "유혹",
    "영감이 넘치긴": "영감", "불만족스럽다": "불만", "낙담했다": "낙담",
    "속상하네": "속상함", "무관심하긴": "무관심", "무관심하게": "무관심",
    "몽롱해": "몽롱", "다정하게": "다정", "이해한다": "이해",
    "신나요": "신남", "흥분된다": "흥분", "무지하긴": "무지",
    "무표정하긴": "무표정", "열렬하네": "열렬", "친절하네": "친절",
    "역겹네요": "역겨움", "오만하군요": "오만", "무시하며": "무시",
    "무시하듯이": "무시", "반했긴": "매혹", "불안해": "불안",
    "고마워요": "감사", "안타깝네요": "안타까움", "행복해": "행복",
    "기뻐라": "환희", "조심해": "조심", "인상적이군": "인상적",
    "자랑스럽군": "자랑", "비위 맞추긴": "비위 맞춤",
}

viol = json.loads((BASE / "_prefix_violations.json").read_text("utf-8"))
AUTO = {}
skipped = []
for v in viol:
    kop = v["kop"]
    nom = PREFIX_NOMINAL.get(kop)
    if not nom:
        skipped.append((v["en_word"], kop, v["asset"], v["pointer"]))
        continue
    old = v["ko"]
    if not old.startswith(kop + "."):
        skipped.append((v["en_word"], kop, "PREFIX-NOT-AT-START", v["pointer"]))
        continue
    new = nom + old[len(kop):]
    AUTO[old] = new
for s in skipped:
    print("SKIP:", s)
print("auto prefix pairs:", len(AUTO))

# ---------------------------------------------------------------------------
# B-E. Manual pairs (verified against pak_pairs.tsv)
# ---------------------------------------------------------------------------
REPLACEMENTS = [
    # ---- bartenderwoofie ----
    ("내 가게 환영!", "내 가게에 온 걸 환영해!"),
    ("<selfname>이 왔다. 네 소망을 듣고 싶구나.", "<selfname>이야. 네 소망을 듣고 싶구나."),
    ("부디 감사와 이 선물 받아.", "부디 감사의 뜻으로 이 선물을 받아 줘."),
    ("그냥 수치스러워, 내 가게 고치길 요구.", "그야말로 수치스러운 일이다. 내 가게를 고치기를 요구한다."),
    ("내 가게에 또 입주 계약서가 있네. 설마 일부러 그런 건 아니겠지.",
     "내 가게에 또 증서가 있네. 설마 일부러 그런 건 아니겠지."),
    ("내 가게에 입주 계약서가 또 있다고? 분명 실수겠지?",
     "내 가게에 증서가 또 있다고? 분명 실수겠지?"),
    ("이 가게는 플러팔로가 물 먹는 곳보다도 더 허름하잖아! 당장이라도 떠날 거야.",
     "이 가게는 플루팔로 물웅덩이보다도 더 허름하잖아! 당장이라도 떠날 거야."),
    ("수동적이든 아니든, 내 가게에 두 번째 상인을 들여앉히는 걸 가만히 보고만 있을 순 없어.",
     "평화주의자이든 아니든, 내 가게에 두 번째 상인을 들여앉히는 걸 가만히 보고만 있을 순 없어."),
    ("희망참. 내 술집 좀 고쳐줄 수 있어?", "희망. 내 술집 좀 고쳐줄 수 있어?"),
    ("유혹적임. 제 바로 안내해 드릴게요.", "유혹. 제 바로 안내해 드릴게요."),
    ("유혹적임. 오세요, 사세요!", "유혹. 오세요, 사세요!"),
    ("유혹적임. 생식 행위를 시뮬레이션해 보고 싶으신가요?",
     "유혹. 생식 행위를 시뮬레이션해 보고 싶으신가요?"),
    ("불만족스럽다. 네가 바꾼 게 마음에 안 든다, 내 술집을 원래대로 되돌려놔.",
     "불만. 네가 바꾼 게 마음에 안 든다, 내 술집을 원래대로 되돌려놔."),
    ("불만족. 내 바 수리가 아직 안 됐어.", "불만. 내 바 수리가 아직 안 됐어."),

    # ---- lucario ----
    ("네 존재 환영.", "네가 와 준 걸 환영한다."),
    ("내 영혼 네 영혼 환영.", "내 영혼이 네 영혼을 환영한다."),
    ("차분한 마음은 우리 중 환영이야.", "우리는 차분한 마음을 반긴다."),
    ("균형 잡힌 오라는 환영이야.", "균형 잡힌 오라는 환영이다."),
    ("우리는 매일 수련한다. 너도 초대해도 되겠나?", "우리는 매일 수련한다. 너를 초대해도 되겠나?"),
    ("네 오라 환영받길.", "네 오라가 환영받기를."),
    ("우리 선한 마음 모두 환영.", "우리는 선한 마음으로 모두를 환영한다."),
    ("안녕, 네 오라 자라길.", "안녕, 네 오라가 자라기를."),
    ("네 도착 인사.", "네 도착에 인사를 건넨다."),
    ("오라가 우릴 묶어, 그러니 환영.", "오라가 우리를 하나로 묶으니, 그러니 환영한다."),
    ("우리 영혼 우리와 하나.", "우리의 영혼은 우리와 하나다."),
    ("최고가 되길 노려, 아무도 못 한 것처럼.", "최고가 되기를 노려라, 지금껏 아무도 이루지 못한 것처럼."),
    ("매일 수련 자신 향상.", "매일 수련해 자신을 향상한다."),
    ("실수서 배워 나아져.", "실수에서 배워 더 나아지는 거다."),
    ("우리 너에게 많이 배워, 너도 우리에게.", "우리는 너에게서 많이 배웠어. 너도 우리에게서 그랬듯이."),
    ("역사상 우리 오라 가디언이 너희 보호국와 합쳐.",
     "역사가 전하듯 우리 오라 가디언은 너희 보호국과 합쳐졌다."),
    ("네 신념 네 정신 이끌어, 좋아!", "네 신념이 네 정신을 이끄는구나, 좋아!"),
    ("별 관측 명상 같다 말해.", "별 관측이 명상과 같다고들 하지."),
    ("너희에 클루엑스, 우리에겐 전설 신들.", "너희에게 클루엑스가 있다면, 우리에겐 전설의 신들이 있다."),
    ("우리 오라사이트 수정 있어, 비교 가능.", "우리에겐 오라사이트라는 수정이 있어. 비교해 볼 수 있겠지."),
    ("너와 달리 우리 종족 절대 못 날아.", "너희와 달리 우리 종족은 절대 날 수 없어."),
    ("쉿쉿 소리로 남 못 알아들어도 난 알아들어.", "쉿쉿 소리 때문에 다른 이들이 못 알아들어도, 난 알아듣는다."),
    ("네가 마법이라 부르는 거 사실 내 오라, 내 생명 에너지.",
     "네가 마법이라 부르는 건 사실 내 오라, 내 생명 에너지야."),
    ("아니, 특별 취향 없어.", "아니, 나한테 특별한 맛 같은 건 없어."),
    ("네 과학 야망 놀라워.", "네 과학에 대한 야망이 놀랍군."),
    ("너도 털 덮였네, 꼬리만 없어..", "너도 털로 덮여 있구나. 꼬리만 없고.."),
    ("너네가 우리 오라 전자기파라 불렀다 들었어, 이해할 게 많아.",
     "너희 종족이 우리의 오라를 전자기파라고 불렀다더군. 아직 이해할 게 많아."),
    ("공포 삶 나쁜 듯, 잠깐... 아냐?", "공포 속에 사는 건 나쁠 듯한데... 잠깐, 아닌가?"),
    ("미니크녹 위협적...", "미니크녹은 위협적으로 보여..."),
    ("네 이야기서 오라 비슷한 거 봤어요.", "네 이야기에서 오라와 비슷한 걸 봤어."),
    ("우리 투쟁 절박 보여도, 우리 빛 늘 빛나.", "우리의 투쟁이 절박해 보여도, 우리의 빛은 언제나 빛나리."),
    ("네 장인정신 감상해요, 아주 화려.", "네 장인정신이 감탄스러워. 아주 화려해."),
    ("응 네 감정 느껴.", "응, 네 감정이 느껴져."),
    ("오라 사용 가르칠 수 있을지도.", "어쩌면 우리가 너에게 오라 사용법을 가르칠 수 있을지도."),
    ("너한테 오라 가르치면 위험할 듯.", "너한테 오라를 가르치면 위험할 듯해."),
    ("너만의 힘이 있으니 모든 일을 나나 다른 이에게 의존하지 마.",
     "너만의 힘이 있으니 모든 일을 내나 남에게 의존하지 마."),
    ("그래서 생물 몰이해?", "그래서 넌 짐승을 몰고 다니나?"),
    ("네 빛 내 오라 생각나.", "네 빛을 보니 내 오라가 생각나."),
    ("그 옷 스타일 익숙..", "그 옷 스타일은 익숙하군.."),
    ("이 행동 지금 멈춰!", "그 행동 지금 당장 멈춰!"),
    ("도둑질 용납 불가!", "도둑질은 용납 못 해!"),
    ("물건 지금 돌려놔!", "물건을 지금 돌려놔!"),
    ("감히 남 것 훔쳐!", "감히 남의 것을 훔치다니!"),
    ("오라 침착 절제.", "오라를 침착하고 절제하라."),
    ("남의 생활 방식 방해 마.", "남의 생활 방식을 방해하지 마."),
    ("내 힘으로 못 도와!", "내 힘만으론 안 돼! 도와줘!"),
    ("지원 감사.", "도와줘서 고마워."),
    ("여기 뭔가 달라.", "여기 뭔가가 달라."),
    ("전과 다른 물체 감지..", "전과는 다른 물체가 감지돼.."),
    ("내 질서 교란.", "내 질서가 어지러워졌어."),
    ("다른 이 있으면 명상 못 해!", "다른 이가 있으면 명상을 못 해!"),
    ("내 평화 이것으로 깨져, 두 번째 증서 치워!", "내 평화가 이걸로 깨졌어. 두 번째 증서를 치워!"),
    ("마음 고민 있어?", "마음에 고민 있어?"),
    ("빚진 선물 해야.", "빚진 건 선물로 갚아야지."),
    ("너에게 잘되길.", "이게 너에게 잘 맞기를."),
    ("이게 너에게 평화 주길.", "이게 너에게 평화를 주길."),
    ("돌아온 거 실수!", "돌아온 게 실수였다!"),
    ("적대 오라 감지.", "적대적인 오라를 느낀다."),
    ("적 없애자!", "적을 없애자!"),
    ("싸울 시간 왔어!", "싸울 시간이 왔어!"),
    ("이 싸움 못 이겨!", "이 싸움은 못 이겨!"),
    ("패배 맛볼 준비!", "패배를 맛볼 준비를 해!"),
    ("또 목숨 잃었지만 전투 승리.", "또 목숨이 스러졌지만, 전투는 승리했다."),
    ("이제 평화롭게 쉬어.", "이제 평화롭게 쉴 수 있어."),
    ("오늘 위해 훈련했어.", "오늘을 위해 훈련했다."),
    ("네 영혼 평화 있길.", "네 영혼에 평화가 깃들길."),
    ("이제 평화롭게 명상.", "이제 평화롭게 명상할 수 있겠군."),
    ("언젠가 다시 싸워!", "언젠가 다시 싸우자!"),
    ("다신 우리 평화 방해 마!", "다신 우리의 평화를 방해하지 마!"),
    ("교훈 되길.", "교훈이 되길."),
    ("다른 생서 봐!", "다른 생에서 봐!"),
    ("다치진 않았지만 괜찮아.", "다치긴 했지만 괜찮아."),
    ("적 쓰러뜨려!", "적을 쓰러뜨려!"),
    ("목표서 눈 떼지 마!", "목표에서 눈 떼지 마!"),
    ("그렇게 멀리 떨어지는 건 명예 아냐.", "그렇게 멀찍이 있는 건 명예롭지 못해."),
    ("네 영혼을 힘으로 바꾸길!", "네 영혼을 힘으로 바꾸길 바란다."),

    # ---- saturnspaceconverse ----
    ("으아아아! 미니크녹다! 음... 당신은 미니크녹가 아니죠? 미안해요!",
     "으아아아! 미니크녹이다! 음... 당신은 미니크녹이 아니죠? 미안해요!"),
    ("나-안-안 무서워. 날-날-날개 데우려 떨-떠는 거야",
     "나-나-난 안 무서워. 날-날-날개 데우려고 떨-떠는 거야"),
    ("광합성 할 수 있어요? 우주에 있으면 배고파져요?", "광합성 할 수 있어? 우주에 있으면 배고파?"),
    ("어떤 마법 널 움직여?", "어떤 마법이 널 움직여?"),
    ("글리치풍 옷 우리한테 인기 많아.", "글리치풍 옷이 우리한테 인기 많아."),
    ("아야. 네 쪽 보려면 선글라스 필요할 듯.", "아야. 네 쪽을 보려면 선글라스가 필요할 듯."),
    ("하이로틀 차 좋아하죠? 언젠가 마셔봐야.", "하이로틀은 차를 좋아하지? 언젠가 마셔 봐야지."),
    ("새터니안인 수중 건축 가능할까요.", "새터니안이 수중에도 건축할 수 있을까?"),
    ("어떤 어둠 마법 널 창조?", "어떤 어둠의 마법이 널 만들었지?"),
    ("친절해, 거미야?", "넌 온순한 편이야, 거미야?"),
    ("너도 실크로 만들어?", "너도 실크로 뭔가를 만들어?"),
    ("안녕 여행자. 어... 최근에 암모니아 다뤘어?", "안녕, 여행자. 어... 최근에 암모니아를 다뤘어?"),
    ("정말 푹신하고 깃털이 많네. 온혈이야?", "정말 푹신하고 깃털이 많네. 온혈 동물이야?"),
    ("여기서 보는 다른 종족들과 정말 달라.", "여기서 보는 다른 종족들과는 정말 달라."),
    ("우리 종족 잃은 형제 같을지도.", "우리 종족은 서로 잃어버린 형제 같을지도."),
    ("레피돕티안도 변태한다 들었어.", "레피돕티안도 변태한다고 들었어."),
    ("레피돕티안 패션 감각 뛰어나.", "레피돕티안은 패션 감각이 뛰어나."),
    ("너한테 이상한 거 감지.", "너한테서 뭔가 이상한 게 감지돼."),
    ("최근 미라실에 다녀왔어", "최근 미라실에 다녀왔어?"),
    ("우리 텔레포터를 솔라레이와 다시 연결할 수 있을까.", "우리 텔레포터를 솔라레이와 다시 연결할 수 있을까?"),
    ("네 말투 악티아스 생각나.", "네 말투를 들으니 악티아스가 생각나."),
    ("찍찍, 아-아-아니 찌이잉!", "찍찍, 아-아-아니 윙윙!"),
    ("네뷸락 마을 아름다워. 몇 시간 바라봐도.", "네뷸랙 마을은 아름다워. 몇 시간이고 바라볼 수 있어."),
    ("너무 반짝!", "너무 반짝여!"),
    ("그래서 너희는 벌목 곤충을 전부 먹는 거야, 아니면 개미만 먹는 거야?",
     "그래서 너희는 막시목 곤충을 전부 먹는 거야, 아니면 개미만 먹는 거야?"),
    ("엉?! 벌?! 근데 어피어리언은 아냐. 어디서 왔어?", "엉?! 벌?! 근데 아피아리안은 아니네. 어디서 왔어?"),
    ("글리치 연금술사는 자극제만 만든다고 들었어.", "글리치 연금술사는 스팀만 만든다고 들었어."),

    # ---- avikanoutpost ----
    ("지금은 바쁘니 나중에 얘기하죠", "할 말이 없어."),
    ("여기 열기 견디는 거 놀라워. 많은 외계인 못 견뎌.",
     "여기 열기를 견디다니 놀라워. 많은 외계인은 못 견디던데."),
    ("먹을 수 있나? 플로란, 채소 안 먹은 지 너무 오래됐다.",
     "먹을 수 있나? 채소를 안 먹은 지 너무 오래됐어."),
    ("영혼 없어, 기계.", "영혼이 없어, 기계."),
    ("감시자들 널 지켜봐.", "감시자들이 널 지켜보고 있어."),
    ("아비칸 보통법의 외계 상호작용 규약 B1은 널 무시하라 한다, 기계여.",
     "아비칸 보통법의 외계인 상호작용 규약 B1은 나더러 널 무시하라고 명한다, 기계여."),
    ("기계와 말 안 해.", "기계와는 말 안 해."),
    ("여기 친구 거의 없을 거야.", "여기선 친구가 거의 없을 거야."),
    ("기계 별로.", "기계는 별로야."),
    ("너네 참을 수 있어도 좋아하는 건 아냐.", "너희를 참아 줄 수는 있어도 좋아하는 건 아냐."),
    ("스타파어러 피난처 모두 환영, 기계도.", "스타페어러의 피난처는 모두를 환영한다, 기계도."),
    ("스타사이트 인이 네가 마실 수 있는 거 줄지 의심, 기계.",
     "스타사이트 여관이 네가 마실 수 있는 걸 팔지는 의심스럽군, 기계."),
    ("발리안 아스-나다타 차량 수리. 너도 고칠지도.", "발리안 아스-나다타는 탈것을 고친다. 너도 고쳐줄지 몰라."),
    ("자재 교환소서 네 몸 거래할 수 있을지도.", "자재 교환소에서 네 몸을 거래할 수 있을지도."),
    ("여기서 바싹 마를까 봐 겁 안 나나?", "여기서 바싹 마를까 봐 안 겁나?"),
    ("스타파어러 피난처에 온 걸 환영하네, 선장.", "스타페어러의 피난처에 온 걸 환영하네, 선장."),
    ("스타파어러 피난처에 온 걸 환영하네, 스타파어러.", "스타페어러의 피난처에 온 걸 환영하네, 스타페어러."),
    ("스타파어러 피난처에 온 걸 환영하네, 선장!", "스타페어러의 피난처에 온 걸 환영하네, 선장!"),
    ("스타파어러 피난처에 온 걸 환영하오, 드로덴.", "스타페어러의 피난처에 온 걸 환영하오, 드로덴."),
    ("말이야, 의회 곧 발라스 안드라베이 찾아!", "말이야, 평의회가 곧 발라스 안드라베이를 찾아낼 거야!"),
    ("라데이스 널 지지, 선장.", "라데이스가 널 지지한다, 선장."),
    ("최근에 날개막 청소했어요?", "최근에 덮개 청소했어요?"),
    ("기계 안 좋아하지만 너 괜찮아 보여. 기계치고는.", "기계는 안 좋아하지만 너는 괜찮아 보여. 기계치고는."),
    ("민간인 지위의 드로덴. 어떻게 얻었어?", "민간인 지위를 얻은 드로덴이라니. 어떻게 얻은 거야?"),
    ("적어도 넌 우리 편.", "적어도 넌 우리 편이네."),
    ("드로덴이면 외계인 상호작용 프로토콜 적용 안 되겠네.", "드로덴이면 외계인 상호작용 규약이 적용 안 되겠네."),
    ("외계인 상호작용 프로토... 아 맞다, 보통법상 넌 외계인 아니지...",
     "외계인 상호작용 규... 아 맞다, 보통법상 넌 외계인 아니지..."),
    ("내 사랑 못 받아.", "내 사랑은 못 받아."),
    ("너 주시 중, 기계.", "널 주시하는 중이다, 기계."),
    ("너 드로덴 사멸 종족.", "너희 드로덴은 사라져가는 종족이지."),
    ("라데이스가 드로덴 자유 동의 안 했으면 너 여기 없었을 거야.",
     "라데이스가 드로덴의 자유를 허락하지 않았다면 넌 여기 없었을 거야."),
    ("안녕, 긴 귀여.", "안녕, 귀 긴 자여."),
    ("너의 그 작은 두 눈은 뭐 하는 데 쓰는 거야?", "그 작은 눈 두 개는 뭘 하는 데 쓰는 거야?"),
    ("워처는 당신 같은 사람이 필요합니다.", "감시자들은 당신 같은 사람이 필요합니다."),
    ("워처가 당신을 맞이합니다, 선장님.", "감시자들이 당신을 맞이합니다, 선장님."),
    ("워처의 사무실은 정거장 최상층에서 찾을 수 있습니다.", "감시자들의 사무실은 정거장 최상층에서 찾을 수 있습니다."),
    ("워처 갑옷 수령함.", "감시자 갑옷 수령함."),
    ("^#BA66FF;와처 사무실 패스^white;", "^#BA66FF;감시자 사무실 패스^white;"),
    ("감시자단 자히드 사령관이 직접 내린 명령서.", "감시자들의 자히드 사령관이 직접 내린 명령서."),
    ("감시자단에 등록된 드로덴 유닛 감지.", "감시자들에 등록된 드로덴 유닛 감지."),
    ("여기서 아무것도 시도하지 마. 감시자단이 지켜보고 있어.", "여기서 아무것도 시도하지 마. 감시자들이 지켜보고 있어."),

    # ---- corpus-wide transliteration unification (contexts verified) ----
    ("스타파러 레퓨지 패스", "스타페어러의 피난처 패스"),
    ("아비칸 스타파러", "아비칸 스타페어러"),
    ("스타파러의 서신", "스타페어러의 서신"),
    ("스타파러 피난처", "스타페어러의 피난처"),
    ("스타파어러 피난처", "스타페어러의 피난처"),
    ("바레이 전쟁", "브할레이 전쟁"),
    ("바스 바레이", "바스 브할레이"),
    ("브알레이", "브할레이"),
    # leftover Glitch emotion prefixes not covered by the viol sweep
    ("비위 맞추긴. 제 가게에 오신 걸 환영합니다.", "비위 맞춤. 제 가게에 오신 걸 환영합니다."),
    ("희망참.", "희망."),
    ("유혹적임.", "유혹."),
    ("불만족스럽습니다.", "불만."),
    ("불만족함.", "불만."),
    ("불만족.", "불만."),
    ("감시자단 소속으로서", "감시자들 소속으로서"),
    ("와처 드론", "감시 드론"),
    # Fluffalo -> 플루팔로 (TM: Fluffalo Egg -> 플루팔로 알)
    ("플러팔로", "플루팔로"),
    # bare Starfarer spellings last, after the longer place-name pairs above
    ("스타파어러", "스타페어러"),
    ("스타파러", "스타페어러"),
]

REPLACEMENTS = list(AUTO.items()) + REPLACEMENTS
print("total replacement pairs:", len(REPLACEMENTS))


def _vlqr(buf, p):
    # MSB-first base-128 varint, matching pak.py rvu()
    v = 0
    while True:
        b = buf[p]
        p += 1
        v = (v << 7) | (b & 0x7F)
        if not (b & 0x80):
            return v, p


def vlq(v):
    # MSB-first base-128 varint, matching pak.py rvu() (no zigzag)
    stack = []
    while True:
        stack.append(v & 0x7F)
        v >>= 7
        if not v:
            break
    out = bytearray()
    for i, b in enumerate(reversed(stack)):
        out.append(b | 0x80 if i < len(stack) - 1 else b)
    return bytes(out)


def _key(buf, p):
    n, p = _vlqr(buf, p)
    return p + n


def _rjson_skip(buf, p):
    t = buf[p]
    p += 1
    if t == 1:
        return p
    if t == 2:
        return p + 8
    if t == 3:
        return p + 1
    if t == 4:
        _, p = _vlqr(buf, p)
        return p
    if t == 5:
        n, p = _vlqr(buf, p)
        return p + n
    if t == 6:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _rjson_skip(buf, p)
        return p
    if t == 7:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _key(buf, p)
            p = _rjson_skip(buf, p)
        return p
    raise ValueError("bad json type %d at %d" % (t, p))


def replace_in_value(v):
    if isinstance(v, str):
        changed = False
        for old, new in REPLACEMENTS:
            if old in v:
                v = v.replace(old, new)
                changed = True
        return v, changed
    if isinstance(v, list):
        out = []
        changed = False
        for x in v:
            x, c = replace_in_value(x)
            out.append(x)
            changed = changed or c
        return out, changed
    if isinstance(v, dict):
        out = {}
        changed = False
        for k, x in v.items():
            x, c = replace_in_value(x)
            out[k] = x
            changed = changed or c
        return out, changed
    return v, False


def main():
    d0 = SRC_PAK.read_bytes()
    off0 = struct.unpack(">Q", d0[8:16])[0]
    assert d0[off0:off0 + 5] == b"INDEX"
    p = off0 + 5
    nmeta, p = _vlqr(d0, p)
    for _ in range(nmeta):
        p = _key(d0, p)
        p = _rjson_skip(d0, p)
    meta_blob = d0[off0:p]

    src = Pak(str(SRC_PAK))
    files = {name: src.read(name) for name in src.index}
    print("base pak entries:", len(files))

    # needles must match the raw (JSON-escaped) bytes inside .patch files
    needles = [json.dumps(old, ensure_ascii=False)[1:-1].encode("utf-8")
               for old, _ in REPLACEMENTS]
    # verify each needle exists in the source before rewriting
    for old, needle in zip([r[0] for r in REPLACEMENTS], needles):
        if not any(needle in files[n] for n in files if n.endswith(".patch")):
            print("NEEDLE-MISS (source):", old[:80])
    assets_changed = 0
    for name in sorted(files):
        if not name.endswith(".patch"):
            continue
        data = files[name]
        if not any(n in data for n in needles):
            continue
        try:
            doc = json.loads(data)
        except Exception:
            continue
        new_doc, changed = replace_in_value(doc)
        if changed:
            files[name] = json.dumps(new_doc, ensure_ascii=False).encode("utf-8")
            assets_changed += 1
            print("fixed", name)

    buf = bytearray(b"SBAsset6" + b"\x00" * 8)
    index_entries = []
    for name in sorted(files):
        data = files[name]
        off = len(buf)
        buf += data
        index_entries.append((name.encode("utf-8"), off, len(data)))

    index_off = len(buf)
    buf += meta_blob
    buf += vlq(len(index_entries))
    for name, off, n in index_entries:
        buf += vlq(len(name)) + name + struct.pack(">QQ", off, n)
    buf[8:16] = struct.pack(">Q", index_off)

    OUT_PAK.write_bytes(bytes(buf))
    print("assets changed:", assets_changed)
    print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")


if __name__ == "__main__":
    main()
