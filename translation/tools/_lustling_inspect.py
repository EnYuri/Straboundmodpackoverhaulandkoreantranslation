# Cover untranslated lustling dialog + inspect lines.
# Provider (997_sxb_Lustlings_1.2.9_clean.pak) patches add lustling sections/
# lustlingDescription fields that are still English -> our pak had 0 coverage.
# Appends [test, replace] groups to existing patch files; test uses the exact
# provider values so ops gate on the provider mod being applied.
import sys, io, json, re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, 'tools')
from pak import Pak
from pak_writer import write_pak

PROV = r"E:\My Games\steamapps\common\Starbound\mods\997_sxb_Lustlings_1.2.9_clean.pak"
TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
APPLY = '--apply' in sys.argv
KO_RE = re.compile(r'[가-힣]')

def opsof(x, out):
    if isinstance(x, dict):
        if 'op' in x: out.append(x)
        else:
            for v in x.values(): opsof(v, out)
    elif isinstance(x, list):
        for v in x: opsof(v, out)

# ---------- EN->KO map for lustlingDescription (212 unique) ----------
KO = {
"-todo-": "-할 일-",
"AHAHAHAHAHAHAHAHAHAHAHA!!!": "아하하하하하하하하하하하하!!!",
"An accurate representation of what an unaugmented lustling would look like if exposed to a world where sandstone forms naturally.": "증강되지 않은 러스틀링이 사암이 자연 형성되는 세계에 노출됐을 때의 모습을 정확히 재현한 거야.",
"An ancient anvil. It floats. Because reasons. I think I can use this to empower some weapons. No lustling ones though, because we're not special, I guess.": "고대 모루야. 떠 있어. 왜인지는 모르겠지만. 무기를 강화하는 데 쓸 수 있을 것 같아. 러스틀링 무기는 안 되지만 — 우린 그렇게 특별하지 않나 봐.",
"An eye scanner? A clit scanner is by far more secure.": "눈 스캐너? 클리토리스 스캐너가 훨씬 안전하거든.",
"An ice trap would be scary to anything not lustling. At most it's inconvenient for me.": "얼음 함정은 러스틀링이 아닌 것들한테나 무섭지. 나한텐 기껏해야 귀찮은 정도야.",
"An industrial grade workbench. Low-tech compared to Lustling stations, but I can still do a lot here.": "공업용 작업대야. 러스틀링 작업대에 비하면 저급 기술이지만, 그래도 여기서 할 수 있는 게 많아.",
"An protectorate enlistment poster, It was targed to Lustlings, Showing how open they are to our sexual needs. Don't know how they got a Hylotl to pose naked for the photo.": "보호국 입대 포스터야. 러스틀링을 겨냥한 거지 — 우리의 성적 욕구에 얼마나 개방적인지 보여주잖아. 하이로틀을 어떻게 나체로 포즈 잡게 했는지는 모르겠지만.",
"An unlocked locker! No dildos!?": "열린 사물함이다! 딜도가 없다고!?",
"Another former protector. He always looked like he has a massive buttplug up his ass...": "또 다른 전직 수호자야. 항상 엉덩이에 거대한 버트플러그를 끼고 다니는 것처럼 보였지...",
"Are these the Protectorate races? What, no lustling? Why do humans get to be on top? I'm offended!": "이게 보호국 종족들이야? 뭐, 러스틀링은 없어? 왜 인간이 위에 있는 거야? 기분 나쁜데!",
"As fun as these figures are to fuck, none of them belong to me.": "이 피겨들, 박기엔 재밌을 것 같지만 내 건 하나도 없네.",
"Avian Grand Protector I will miss him cop a feel when I walk by!": "아비안 고위 수호자. 지나갈 때마다 슬쩍 더듬던 게 그리울 거야!",
"Avian technology is completely non-interfaceable with lustling tech. Not that I care. I doubt it's any major breakthrough.": "아비안 기술은 러스틀링 테크랑 전혀 호환되지 않아. 신경 안 쓰지만. 어차피 대단한 혁신도 아닐 거야.",
"Banners of each of the Protectorate's core races. Our flag was banned for being too pornographic.": "보호국 핵심 종족들의 깃발이야. 우리 깃발은 너무 포르노 같다고 금지됐지.",
"Blech.": "웩.",
"Boltbulb. Actually softer than it looks, but not exactly an Lustling delicacy.": "볼트벌브. 보기보다 부드럽지만, 딱히 러스틀링 진미는 아니야.",
"Boltbulb. Actually softer than it looks, but not exactly an lustling delicacy.": "볼트벌브. 보기보다 부드럽지만, 딱히 러스틀링 진미는 아니야.",
"Books were just one of the few things I had to get used to as one of the first lustling Protectorate students.": "최초의 러스틀링 보호국 학생으로서, 책은 적응해야 할 몇 안 되는 것 중 하나였어.",
"Brests all bouncy and perky. Time to spread my legs and go fuck things!": "가슴이 탱탱하고 쫄깃해. 다리 벌리고 뭐든 박으러 갈 시간이야!",
"Bring the Glitch to Eros and, well, you wouldn't have to call them \"Glitch\" anymore.": "글리치를 에로스에 데려오면, 글쎄, 더는 \"글리치\"라고 부를 필요가 없어질 걸.",
"By the Great Orgy! The graduation ceremony is starting right now!": "위대한 난교시여! 졸업식이 지금 시작이야!",
"By the Queen! This way leads nowhere. Wait, is that some fabric from the banner? Maybe I should take it...": "여왕이시여! 이쪽은 막다른 길이야. 잠깐, 저건 현수막 천 아냐? 가져가야 할지도...",
"Cacti, Definitely DO NOT!! try and fuck it, very painful.": "선인장. 절대로!! 박으려고 하지 마. 엄청 아파.",
"Careful! lustling have been known to disappear entirely into the cushions of these sofas.": "조심해! 러스틀링이 이런 소파 쿠션 속으로 통째로 사라진 사례가 있어.",
"Carrots are one of the few Terran foods an lustling can naturally fuck.": "당근은 러스틀링이 자연스럽게 박을 수 있는 몇 안 되는 지구 음식이야.",
"Carrots are one of the many Terran foods an Lustling can naturally fuck.": "당근은 러스틀링이 자연스럽게 박을 수 있는 여럿 되는 지구 음식 중 하나야.",
"Chocolate is a Lustlings best friend!": "초콜릿은 러스틀링의 가장 친한 친구야!",
"Chocolate's poisonous to un-augmented lustling. It's caused my human friends no small amount of sadness.": "초콜릿은 증강 안 된 러스틀링한테 독이야. 내 인간 친구들을 꽤 슬프게 했지.",
"Cityscapes are rare on Eros. That's a shame, because they're pretty nice.": "도시 경관은 에로스에서 드물어. 꽤 멋진데 아쉬워.",
"Comfortable? Yes. Fuckable? Yessss!.": "편안해? 응. 박을 만해? 응응응!",
"Could do with bigger tits. But its a nice idol.": "가슴이 더 크면 좋겠지만, 그래도 괜찮은 우상이야.",
"Creepy!": "소름 끼쳐!",
"DIAMONDS!": "다이아몬드!",
"Despite being worthless smudges to most lustling, I guess these paintings sell for pretty good if brought to the right people?": "대부분 러스틀링한테는 무가치한 얼룩이지만, 제대로 된 사람한테 갖다 주면 꽤 비싸게 팔리나 봐?",
"Do NOT let an Lustling drink coffee.": "러스틀링한테 커피를 마시게 하지 마.",
"Do. NOT. Give an Lustling coffee. Just don't.": "러스틀링.한테.커피.주지.마. 정말 주지 마.",
"Do. NOT. Give an lustling coffee. Just don't.": "러스틀링.한테.커피.주지.마. 정말 주지 마.",
"Drat, not a porn book in sight.": "젠장, 야한 책이 하나도 안 보이네.",
"ENGAGE!": "돌입!",
"Esther Bright, the former Grand Protector. Isn't she still alive? I wonder if she would be up for a orgy?": "에스더 브라이트, 전직 고위 수호자야. 아직 살아 있지 않았나? 난교에 응해줄까?",
"Everything you need to survive, unless you're an lustling, in which case nothing here is useful.": "생존에 필요한 건 다 있어 — 러스틀링이 아니라면 말이야. 러스틀링한테는 여기 아무것도 쓸모없어.",
"Ew.": "웩.",
"Ew...": "웩...",
"Ewww.": "으웩.",
"Fake plants are all the rage on Eros as of late.": "가짜 식물이 요즘 에로스에서 대유행이야.",
"Fire fluffalo! not found on Eros.": "불꽃 플루팔로! 에로스에는 없어.",
"Floop? ": "플룹?",
"Flowers like this can only grow in places unsuitable for natural-born lustling.": "이런 꽃은 자연 태생 러스틀링한테 부적합한 곳에서만 자라.",
"For two weeks I had shoved a toy like that up my ass, fun memories.": "2주 동안 저런 장난감을 엉덩이에 쑤셔 넣고 다녔지. 좋은 추억이야.",
"Fruit from the sea, though most Lustling would probably fuck it.": "바다에서 온 과일이야. 대부분 러스틀링은 아마 박아버리겠지만.",
"Fruit from the sea. Novel, though most lustling would probably avoid it.": "바다에서 온 과일. 신기하긴 한데, 대부분 러스틀링은 피할 거야.",
"Giggle, lets see if I can scan my tits on it.": "히히, 이걸로 내 가슴을 스캔할 수 있나 보자.",
"Great for baking erotic cakes!.": "에로틱 케이크 굽기에 딱이야!",
"Heh, lustling haven't used bones for decor since our tribal days.": "헤, 러스틀링은 부족 시대 이후로 뼈를 장식으로 안 써.",
"Hello there little lantern, can I shove you up my ass?": "안녕, 작은 랜턴. 널 엉덩이에 쑤셔 넣어도 될까?",
"Here's my locker. My uniform is custom tailored to fit my massive breasts.--ugh, Wait!?, this isn't my uniform! My tits cant fit into this!": "여긴 내 사물함이야. 내 제복은 이 거대한 가슴에 맞게 맞춤 제작했거든. — 윽, 잠깐!? 이거 내 제복이 아니야! 내 가슴이 안 들어가!",
"Hm?": "음?",
"Hmmm...": "음...",
"Hylotlogy? It sound even more absurd than lustlingogy!": "하이로틀학? 러스틀링학보다 더 황당하게 들리는데!",
"I always enjoyed sitting on this when Rick plays on his guitar, It tickles my clit just right.": "릭이 기타 칠 때 여기 앉는 게 좋았어. 클리를 딱 맞게 간지럽혀주거든.",
"I always like the kind of water fountain you can fuck.": "박을 수 있는 분수는 언제나 좋아.",
"I bet this wood would feel nice on my clit.": "이 나무, 클리에 기분 좋을 것 같은데.",
"I could fuck those.": "저거 박을 수 있겠어.",
"I fucked a friend on one of these things we got from Earth.": "지구에서 가져온 저런 거 위에서 친구랑 박았었어.",
"I got to fuck on a real one back on Earth in a museum... another thing I miss about Earth.": "지구 박물관에서 진짜 것 위에서 박아봤었어... 지구가 그리운 또 하나의 이유야.",
"I had a job as a urinal on earth, A nice man told me to join the protectorate after he had finished pissing into my mouth. Best tasting that week, glad I took his advice.": "지구에서 소변기 노릇하는 일을 했었어. 어떤 좋은 분이 내 입에 오줌 다 싸고 나서 보호국에 들어가라고 하더라고. 그 주 최고의 맛이었어. 조언 따라서 잘했어.",
"I had one of these back on earth only bigger and I would get in and dance.": "지구에서도 이런 게 있었어 — 더 큰 거였지만. 안에 들어가서 춤췄지.",
"I had some of the best fucks on Earth.": "지구에서 최고의 떡을 쳤었어.",
"I have a dildo that looks like that! Moves the same way too!": "저렇게 생긴 딜도 갖고 있어! 움직이는 것도 똑같아!",
"I hear most races use flowers like this to make dye. lustling color their clothes using different moulds. These are prettier.": "대부분 종족은 이런 꽃으로 염료를 만든다더라. 러스틀링은 다른 곰팡이로 옷을 물들여. 이게 더 예쁘긴 하지만.",
"I hope this bed gets in all my crevices!": "이 침대가 내 구석구석에 다 들어왔으면 좋겠어!",
"I like to use this to dry my tits too.": "이걸로 내 가슴도 말리곤 해.",
"I love how these mushrooms looks like my dildos.": "이 버섯들, 내 딜도랑 닮아서 좋아.",
"I never get to play, I keep trying to mod boobs into the games.": "게임을 제대로 못 해. 게임에 가슴 모드 넣으려고 계속 시도만 하고 있어.",
"I suppose it'll do. I wonder if you can design this to hold multiple lustling?": "쓸 만하겠네. 러스틀링 여럿을 수용하도록 설계할 수 있을까?",
"I tried to fuck this lamp, Rick yanked it out of me and told me not to fuck it.": "이 램프 박으려다가 릭이 빼내면서 박지 말라더라고.",
"I was masterbating for too long I'm going to be late for my ceremony!!": "자위를 너무 오래 했어, 내 식에 늦겠다!!",
"I wonder if I can get porn on this?": "이걸로 야동을 볼 수 있을까?",
"I wonder what's so hazardous for an lustling here... except for everything.": "러스틀링한테 뭐가 그렇게 위험한 걸까... 전부 다 빼면 말이야.",
"I would go insane if I had to spend even an hour in this... thing. Isolation may as well be a death sentence to an lustling. And I've put up with a lot of it...": "이런... 곳에서 한 시간만 있어도 미쳐버릴 거야. 격리는 러스틀링한테 사형 선고나 다름없어. 많이 견뎌내긴 했지만...",
"Ice flufallo! not found on Eros.": "얼음 플루팔로! 에로스에는 없어.",
"If I put this near my cunt, would it guide people to it?": "이걸 내 보지 근처에 두면 사람들이 찾아오려나?",
"If I want to make a wooden dildo, this'll do the job.": "나무 딜도를 만들려면 이걸로 충분하겠어.",
"If we really wanted to, I bet lustling engineers could make good use of this crystal tech. It seems pretty versatile. In the meantime, time to press buttons!": "진심으로 원한다면 러스틀링 기술자들이 이 크리스탈 테크를 잘 활용할 수 있을 거야. 꽤 다용도 같아. 일단은 버튼이나 눌러보자!",
"If you put a neurolink on it and painted it white it would look exactly like lustling doors. Doors have pretty universal design across the universe.": "뉴로링크를 달고 하얗게 칠하면 러스틀링 문이랑 똑같아질 거야. 문 디자인은 우주 어디나 비슷하지.",
"In a moment I'll be among the first lustling to ever recieve a Matter Manipulator..This is a big moment for me, I got here on my own merits, and not because I fucked my way to the top...": "잠시 후면 난 최초로 물질 조작기를 받는 러스틀링 중 하나가 돼. 나한텐 큰 순간이야 — 위까지 박아서 온 게 아니라 내 실력으로 여기까지 왔으니까...",
"Is that crystal fuckable? Ha, what am I saying, EVERYTHING is fuckable!": "저 크리스탈은 박을 만할까? 하, 무슨 소리야. 모든 건 박을 만하지!",
"It's more comfortable than it looks, but you can't fuck many people in this.": "보기보다 편안하지만, 여기서 여럿이랑 박긴 힘들겠어.",
"It's super comfortable, and the sheets are tear resistant. The perfect bed for fucking!": "엄청 편안하고, 시트는 안 찢어져. 박기에 완벽한 침대야!",
"Kiwis grow on tropical regions and are fuzzy to the touch. A Lustling treat.": "키위는 열대 지방에서 자라고 만지면 까슬까슬해. 러스틀링 간식이야.",
"Kiwis grow on tropical regions and are fuzzy to the touch. Not an lustling treat.": "키위는 열대 지방에서 자라고 만지면 까슬까슬해. 러스틀링 간식은 아니야.",
"Large enough for one or two lustling to curl up comfortably. Bunk beds save a lot of space.": "러스틀링 한두 명이 편하게 웅크릴 정도로 커. 이층 침대는 공간을 많이 아껴주지.",
"Leda... You were the one that had faith in me to join the Protectorate and not try to fuck my way to the top... I won't forget you.": "레다... 내가 보호국에 들어갈 수 있다고 믿어준 건 너뿐이었어 — 위로 올라가려고 박지 말라고 해준 것도. 잊지 않을게.",
"Light, sleek, and stylish! It almost looks like something an Lustling would make!": "가볍고, 세련되고, 스타일리시해! 거의 러스틀링이 만든 것 같은데!",
"Little chest hope you dont mine me rubbing my clit on you while I loot your contents.": "작은 상자야, 안을 터는 동안 너한테 클리 비비는 거 이해해줘.",
"Looks kinda like Eros.": "에로스랑 좀 비슷하네.",
"Looks like a buttplug....yup its a buttplug!": "버트플러그처럼 생겼네....응, 버트플러그 맞아!",
"Looks like the tentacles that destroyed Earth was shoved through a gloryhole. Guess it found its way back.": "지구를 파괴한 촉수를 글로리홀에 쑤셔 넣은 것 같네. 돌아오는 길을 찾은 모양이야.",
"Looks soft, could fuck on that all day!": "부드러워 보여, 하루 종일 저 위에서 박을 수 있겠어!",
"Looooooooooooooot!": "전리이이이이이이품!",
"Lustling colonies that are hurting for food have been known to cultivate dirturchins. I pity them.": "식량이 부족한 러스틀링 식민지는 흙성게를 재배한다더라. 불쌍해.",
"lustling colonies that are hurting for food have been known to cultivate dirturchins. I pity them.": "식량이 부족한 러스틀링 식민지는 흙성게를 재배한다더라. 불쌍해.",
"Lustlings have huge milk producing factorys that one can go to get milked. Its a very high paying job.": "러스틀링은 직접 가서 착유당할 수 있는 거대한 우유 생산 공장이 있어. 꽤 고액 알바야.",
"Mami helped me settle in when I first arrived here... hi, Mami!": "마미가 처음 여기 왔을 때 정착을 도와줬어... 안녕, 마미!",
"Mercury, not an ideal vacation spot for an Lustling.": "수성. 러스틀링의 이상적인 휴양지는 아니야.",
"Mmm..warm to the touch, bet it would feel nice on my pussy.": "음.. 만지니까 따뜻해. 내 보지에 기분 좋을 것 같은데.",
"More sticky than cum, still taste the same.": "정액보다 끈적하지만 맛은 똑같아.",
"Movies about wariors seeking sex are pretty popular among Lustling.": "섹스를 찾는 전사들 영화는 러스틀링 사이에서 꽤 인기야.",
"NONE ARE SAFE FROM ME! THE GIANT lustling!": "누구도 나한테서 안전하지 않아! 거대 러스틀링이다!",
"Neat curve. This wouldn't be out of place on an lustling ship.": "깔끔한 곡선이네. 러스틀링 함선에 있어도 어색하지 않겠어.",
"Nice cabinet, plenty of room for my dildos.": "멋진 캐비닛이야. 내 딜도 넣을 공간이 넉넉해.",
"No lustling blood, it looks like. Thank the spirits, I would have been really concerned otherwise. I'm still concerned, of course, but not as concerned.": "러스틀링 피는 아닌 것 같아. 영혼들에게 감사를 — 아니었으면 진짜 걱정했을 거야. 지금도 걱정하긴 하는데, 그 정도는 아냐.",
"No matter how I calibrate it, this thing would give off too much heat on an lustling vessel.": "아무리 보정해도 이건 러스틀링 함선에서 열이 너무 많이 나올 거야.",
"Nobody minds if I rub one off while I wait for my turn behind this curtain, Right?": "커튼 뒤에서 내 차례 기다리는 동안 한 발 빼도 아무도 신경 안 쓰지, 그치?",
"Nobody minds if I rub one off while I wait for my turn, Right?": "내 차례 기다리는 동안 한 발 빼도 아무도 신경 안 쓰지, 그치?",
"Not an Lustling skull. Probably safe then! Nah, who am I kidding.": "러스틀링 두개골은 아니네. 그럼 안전한 건가! 아냐, 무슨 소리야.",
"Not an lustling skull. Probably safe then! Nah, who am I kidding.": "러스틀링 두개골은 아니네. 그럼 안전한 건가! 아냐, 무슨 소리야.",
"Not designed for lustling clothes, I'll tell you that.": "러스틀링 옷용으로 설계된 건 아니야, 확실히 말해줄 수 있어.",
"Oh ... Rick..., sorry about your guitar...": "아... 릭..., 네 기타는 미안하게 됐어...",
"Oh I do love me a good Piani.": "오, 좋은 피아니는 정말 좋아.",
"Oh a chest I can melt the lock off with my clit!": "오, 클리로 자물쇠를 녹일 수 있는 상자다!",
"Oh a hologram in a ancient ruin? I wonder if theres any high tech ancient didlos down here?": "오, 고대 유적에 홀로그램? 여기 어딘가 하이테크 고대 딜도가 있지 않을까?",
"Oh that looks like it would be fun to fuck!": "오, 저거 박으면 재밌을 것 같은데!",
"Oh wow this is my favorite char! It can get my G spot!": "오 와, 이건 내 최애 의자야! 내 G스폿을 건드릴 수 있어!",
"Oh wow, just think of the new kinds of sex you can do with this thing!": "오 와, 이걸로 할 수 있는 새로운 종류의 섹스를 생각해봐!",
"Oh, Earth Culture 101 taught me all about you, Pluto. You're not a planet, but by the Queen, humans sure want to believe you are.": "오, 지구 문화 101에서 너에 대해 배웠지, 명왕성. 넌 행성이 아니지만, 여왕이시여, 인간들은 널 행성이라 믿고 싶어하더라고.",
"Oh..these would be nice to have tickle all over me!": "오..이걸로 온몸을 간지럽히면 좋겠다!",
"Ohhhh... time for a little BDSM!": "오오오... 가벼운 BDSM 시간이야!",
"Old caves on Eros are often adorned with drawings like these. Floran hunters are depicted here.": "에로스의 오래된 동굴은 이런 그림으로 장식되곤 해. 여긴 플로란 사냥꾼이 그려져 있어.",
"Old caves on Eros are often adorned with drawings like these. Most of them have been lost to history and never recorded, however.": "에로스의 오래된 동굴은 이런 그림으로 장식되곤 해. 하지만 대부분 기록도 없이 역사 속으로 사라졌어.",
"Old caves on Eros are often adorned with drawings like these. This one celebrates someone giving Florans something. I don't know what it is though.": "에로스의 오래된 동굴은 이런 그림으로 장식되곤 해. 이건 누군가가 플로란한테 뭔가 주는 걸 기념하는 거야. 뭔지는 모르겠지만.",
"Old caves on Eros are often adorned with drawings like these. This one shows a religious scene from the looks of it.": "에로스의 오래된 동굴은 이런 그림으로 장식되곤 해. 이건 보아하니 종교적 장면이야.",
"Old caves on Eros are often adorned with drawings like these. Wait... is that the being that destroyed Earth?!": "에로스의 오래된 동굴은 이런 그림으로 장식되곤 해. 잠깐... 저건 지구를 파괴한 그 존재야?!",
"One of the few chests in the world I dont want to rub on my clit.": "세상에서 클리를 비비고 싶지 않은 몇 안 되는 상자 중 하나야.",
"One of the first trees I've ever seen without dildos attached to it. Seems silly, have you ever tried to fuck a tree without a dildo on it?": "딜도 안 달린 나무는 처음 봐. 바보 같잖아, 딜도 안 달린 나무를 박아본 적 있어?",
"Oooh... lets have some tickle fun!": "오오오... 간지럼 놀이 좀 해볼까!",
"Pets are traditionally too much hassle for lustling on the go. Usually we program cute little drones as pets, and even then they're still maintenance drones.": "전통적으로 애완동물은 돌아다니는 러스틀링한테 너무 번거로워. 보통 귀여운 작은 드론을 애완용으로 프로그래밍하지 — 그래도 정비용 드론이긴 해.",
"Piru, I think, is the Lustling equivalent of wheat.": "피루가 러스틀링의 밀이라고 할 수 있을 것 같아.",
"Piru, I think, is the lustling equivalent of wheat.": "피루가 러스틀링의 밀이라고 할 수 있을 것 같아.",
"Porthole!": "현창!",
"Rhesus really wanted to fuck me last semester.": "리서스는 지난 학기에 나를 정말 박고 싶어했어.",
"Rick's guitar, I pleasured myself with it before Rick found out. Heh heh.": "릭의 기타. 릭이 알기 전에 이걸로 자위했었어. 헤헤.",
"SHINY!!": "반짝여!!",
"SMAAAASH!!": "박아아아아!!",
"Shiiiiinyyyyy.": "반짝이이이이이.",
"Signs should only show the locations to glory holes.": "표지판은 글로리홀 위치만 알려줘야 해.",
"Sleeping beneath leather sheets. Just like the lustling of old.": "가죽 시트 아래서 자기. 옛날 러스틀링들처럼.",
"Smoke": "연기",
"So cold, smooth, and Hard!...just how I like it.": "차갑고, 매끄럽고, 딱딱해!...내 취향 그대로야.",
"Sol, Earth's star. Eros's is similar, just further out. Navigation AIs classify it as a \"gentle\" star.": "솔, 지구의 항성이야. 에로스 것도 비슷한데 좀 더 멀리 있어. 항법 AI는 \"온순한\" 별로 분류하더라.",
"Some old fashioned lustling tribes still use pelts for clothing or tent pieces. This isn't a half-bad example.": "일부 구식 러스틀링 부족은 아직도 옷이나 천막 재료로 가죽을 써. 이건 나쁘지 않은 예시야.",
"Someone had sex at this table! I can smell the sweet leftovers.": "이 탁자에서 누가 섹스했어! 달콤한 잔여 냄새가 나.",
"Spears, the preferred melee weapon of at least a third of known civilized life, Avians and lustling included.": "창 — 알려진 문명 종족의 적어도 3분의 1이 선호하는 근접 무기야. 아비안이랑 러스틀링 포함해서.",
"Starbound... now how can I mod this?...oh wait its been modded, and with some of the best sex mods you can find! FANTASTIC!": "스타바운드... 이걸 어떻게 모드로 만들까?...어 잠깐, 이미 모드됐네 — 찾을 수 있는 최고의 섹스 모드들로! 환상적이야!",
"Sturdy radar display. You could fuck on this all day and not break it!": "튼튼한 레이더 디스플레이야. 하루 종일 위에서 박아도 안 부서지겠어!",
"Sugar plus Lustling is just a recipe for a good time.": "설탕 더하기 러스틀링은 즐거운 시간의 레시피지.",
"Sugar plus lustling is just a recipe for disaster.": "설탕 더하기 러스틀링은 재앙의 레시피야.",
"Tee hee, oh the things ill name.": "히히, 이름 지어줄 게 이렇게 많다니.",
"That reminds me, I should write in my Fuck Journal.": "생각났어, 내 섹스 일지에 써야지.",
"That skull would make a great crotch cup": "저 두개골은 훌륭한 가랑이 컵이 되겠어",
"Thats a funny shaped dildo.": "웃긴 모양의 딜도네.",
"Thats a nice lamp.": "멋진 램프네.",
"The Avian emblem for water, according to my Nexus search. Toxic to native lustling, essential for life to everyone else.": "넥서스 검색으로는 물의 아비안 문양이래. 토착 러스틀링한테는 독이지만, 다른 모두에게는 생명의 필수 요소야.",
"The Lustling skipped this particular part of space travel.": "러스틀링은 우주 여행의 이 부분은 건너뛰었어.",
"The Protectorate teachers insisted I read these books and not to fuck them. No insult, they really did not want me to fuck the books, they use them for the next students.": "보호국 선생들이 이 책들을 읽으라고는 했지만 박지는 말라고 했어. 모욕이 아니야 — 진짜로 책을 박지 말라고 한 거야, 다음 학생들이 쓰거든.",
"The colour progression on this door is stunning. You don't see this sort of thing on Eros.": "이 문의 색 변화가 멋져. 에로스에서는 이런 걸 못 봐.",
"The first Grand Protector. Looks like he needs a good fuck.": "초대 고위 수호자야. 제대로 한 번 박아야 할 얼굴이네.",
"The first anvil discovered on Eros by a Lustling, used it to make a metal bikini with dildos for your ass and pussy, Best seller that year.": "러스틀링이 에로스에서 발견한 최초의 모루야. 엉덩이랑 보지용 딜도가 달린 금속 비키니를 이걸로 만들었지. 그 해 최고 판매였어.",
"The first non-human Grand Protector. Its going to be a long time before a Lustling becomes a Grand Protector, To hard for us to stay focused and not have sex all the time.": "최초의 비인간 고위 수호자야. 러스틀링이 고위 수호자가 되려면 한참 멀었어 — 집중을 유지하고 하루 종일 섹스 안 하는 게 우린 너무 힘들거든.",
"The lustling and Kluex don't exactly get along. Something, something, heresy.": "러스틀링과 클루엑스는 사이가 별로야. 뭐라더라, 이단 어쩌고.",
"The only war on Eros that happend was when Queen Tala became celibate. Two million joined and all fucked the Queen within two days.": "에로스에서 일어난 유일한 전쟁은 탈라 여왕이 금욕을 선언했을 때였어. 이백만 명이 참전해서 이틀 만에 전부 여왕과 했지.",
"The scanner says my clit is hot enough to melt the lock on this ice chest.": "스캐너가 내 클리 열기로 이 얼음 상자 자물쇠를 녹일 수 있대.",
"This bed emits a bioluminescent light, not unlike those you find on plants in Eros's cave systems.": "이 침대는 생체발광을 내 — 에로스 동굴 식물들처럼.",
"This bed looks like it could soak up lots of Lustling love juice.": "이 침대, 러스틀링 애액을 잔뜩 흡수할 수 있을 것 같아.",
"This doll has cameras in its eyes, Hope you got a good look at my muff.": "이 인형 눈에 카메라가 있어. 내 보지 잘 봤길 바래.",
"This door cant shock anything I havent shock before. I bet its not even at full charge.": "이 문이 나한테 새로운 감전을 줄 수는 없어. 완충도 안 됐을 걸?",
"This door completely fails to serve its purpose. At least lustling tent flaps can keep the weather out.": "이 문은 제 역할을 완전히 못 하네. 러스틀링 천막 덮개도 날씨는 막아주는데.",
"This floor seems odd....": "이 바닥 뭔가 이상해....",
"This is a really clean sink.": "정말 깨끗한 싱크대네.",
"This is really heavy. I can't imagine any lustling taking this with them.": "진짜 무거워. 이걸 들고 다니는 러스틀링은 상상이 안 가.",
"This is used to broadcast porn videos? Oh. Oh!.. I'm so horny!...": "이걸로 야동을 송출한다고? 오. 오!.. 너무 흥분돼!...",
"This looks nice and soft to fuck on.": "부드럽고 좋아 보여 — 위에서 박기 딱이네.",
"This pelt's a joke compared to some of the beasts we have back on Eros.": "에로스의 짐승들에 비하면 이 가죽은 우스운 수준이야.",
"This thing never has any lube or dildos in it, and it also took my pixels!": "이 안엔 젤도 딜도도 없어, 게다가 내 픽셀까지 뺏어갔어!",
"This tree is so beautiful, really got to remember to have a good fuck under it after my ceremony.": "이 나무 정말 아름다워. 식 끝나고 밑에서 한 번 박아야지.",
"This would be a great place to relax and fuck on.": "휴식하면서 박기에 좋은 장소겠는데.",
"Those wires are to high up to use on my pussy...shame.": "저 전선들은 내 보지에 쓰기엔 너무 높이 달렸네... 아쉽다.",
"To a native lustling, even curling up in the freezer would be too hot and dangerous for us.": "토착 러스틀링한테는 냉동실에 웅크리는 것조차 너무 뜨겁고 위험해.",
"Two large broadswords. lustling prefer spears, but if you ever need to cleave a tank in two, our broadswords can do that. Or so I've heard.": "큰 브로드소드 두 자루야. 러스틀링은 창을 선호하지만, 전차를 두 동강 낼 일 있으면 우리 브로드소드로도 돼. 그렇게 들었어.",
"Very soft on my fuckable ass.": "내 박기 좋은 엉덩이에 아주 부드러워.",
"Waz?": "왓?",
"We Lustling trust messages left behind by strangers, they usually lead to a good time.": "우리 러스틀링은 이방인이 남긴 메시지를 믿어 — 보통 좋은 시간으로 이어지거든.",
"Well this looks intresting!": "음, 이거 재밌어 보이네!",
"What a sleek server. It's cooled with liquid; something we don't have to do, considering the temperatures on Eros.": "매끄러운 서버네. 액체로 냉각해 — 에로스 온도 생각하면 우린 그럴 필요 없지만.",
"When the Illuminate discovered cotton, it became all the rage among Lustling colonies. Weavers are still finding ways to make good use of it.": "일루미네이트가 면화를 발견했을 때, 러스틀링 식민지에서 대유행이었어. 직조공들은 아직도 활용법을 찾고 있지.",
"When the Illuminate discovered cotton, it became all the rage among lustling colonies. Weavers are still finding ways to make good use of it.": "일루미네이트가 면화를 발견했을 때, 러스틀링 식민지에서 대유행이었어. 직조공들은 아직도 활용법을 찾고 있지.",
"When the lustling were first exposed to the Earth's internet, a lot of freelance hackers were tempted to cause chaos on it. They decided against it though, because they discovered that humans wreak havoc on their own.": "러스틀링이 지구 인터넷에 처음 접했을 때, 프리랜서 해커들이 혼란을 일으키고 싶어했어. 하지만 그만뒀지 — 인간들이 스스로 혼란을 일으킨다는 걸 발견했거든.",
"Why use plastic to make a plant? Just make more dildos!": "식물을 플라스틱으로 왜 만들어? 그냥 딜도를 더 만들지!",
"With a good loom, I could probably modify some of these clothes to better fit me. Might start a fashion trend back on Eros.": "좋은 직조기만 있으면 이 옷들을 내 몸에 맞게 고칠 수 있을 거야. 에로스에서 유행이 시작될지도.",
"Yellow! A popular color in Eros. ": "노란색! 에로스에서 인기 있는 색이야.",
"You don't want to know what an lustling looks like after a good electrical shock.": "감전된 러스틀링이 어떤 모습이 되는지는 모르는 게 좋아.",
"You dont have to get me drunk to fuck me, just ask!": "날 박고 싶으면 취하게 할 필요 없어, 그냥 물어봐!",
"You think a door made of tar will stop me from fucking it? Guess again door!": "타르로 만든 문이 날 박는 걸 막을 수 있다고 생각해? 다시 생각해, 문아!",
"lustling SMASH!!": "러스틀링 박아아아!!",
"lustling don't use physical clocks; we keep track of time through AR. The ticking noise is kind of soothing, though.": "러스틀링은 물리 시계를 안 써 — AR로 시간을 확인해. 그래도 똑딱 소리는 좀 편안하네.",
"lustling mining colonies usually utilize laser technology to mine tough resources. A drill works too, I guess.": "러스틀링 채광 식민지는 보통 단단한 자원을 캐는 데 레이저 기술을 써. 드릴도 되긴 하겠네.",
"lustling pixel transactions are typically handled over AR. This register won't be handling any transactions anymore, now.": "러스틀링 픽셀 거래는 보통 AR로 처리해. 이 금전등록기는 이제 거래를 못 하겠네.",
"lustling prisons are secluded, soundproof, graphene weave cells. Isolation is the worst possible punishment in our society. I should know, after Earth...": "러스틀링 감옥은 외딴 방음 그래핀 직조 감방이야. 격리는 우리 사회 최악의 형벌이지. 지구에서 겪어봐서 알아...",
"lustling recycle as much as possible, to the point where there's almost nothing we can throw in a dumpster that couldn't be re-used.": "러스틀링은 최대한 재활용해 — 쓰레기통에 버릴 만한 게 거의 없을 정도로.",
"lustling tally charts count in threes. It took me a while to get used to base ten.": "러스틀링 탈리 차트는 셋씩 세. 10진법에 익숙해지는 데 좀 걸렸어.",
"lustling wardrobes are smaller and more portable than this big, dull thing.": "러스틀링 옷장은 이 크고 칙칙한 것보다 작고 휴대성도 좋아.",
}

# ---------- 1) provider: gather EN lustlingDescription rows ----------
prov = Pak(PROV)
desc_rows = []  # (patchfile, en)
for fn in prov.index:
    if not fn.endswith('.patch'): continue
    try: raw = prov.read(fn).decode('utf-8')
    except Exception: continue
    if 'lustlingDescription' not in raw: continue
    ops = []; opsof(json.loads(raw), ops)
    for o in ops:
        if o.get('path') == '/lustlingDescription' and isinstance(o.get('value'), str):
            if not KO_RE.search(o['value']):
                desc_rows.append((fn, o['value']))
missing = [en for _, en in desc_rows if en not in KO]
print('desc rows:', len(desc_rows), '| EN missing KO map:', len(missing))
for m in missing: print('  UNMAPPED:', m[:100])

# ---------- 2) provider dialog sections: EN arrays -> KO arrays ----------
GREET_KO = [
    "안녕.", "잘 지내?", "어떻게 지내?", "만나서 반가워. 섹스할래?",
    "흥분했으면 좋겠어. 나는 그렇거든!", "여왕의 축축한 보지가 널 이끌어주길.",
    "좋은 한 판 되길.", "보니까 반갑네.", "너랑 해도 될까?", "좋은 하루야, 친구.",
    "안녕, 이방인. 마음에 드는 거 있어?", "어서 와.", "어서 와, 내 난교에 낄래?",
    "만나서 반가워.", "좀 쉬다가 섹스하고 가.", "섹스는 어떻게 해, 친구?",
    "안녕, 이방인. 어서 와.", "안녕, 재밌는 페티시 있어?", "잘 지내고 있어?",
    "좋은 하루 보내.", "내 몸을 바쳐도 될까, 친구?", "만나서 반가워, 번개 한 판 할래?",
    "좋은 한 판 해.", "편하게 있어.", "안녕!", "안녕.", "그래, 만나서 반가워.",
    "괜찮아, 친구?", "이봐, 어디선가 온 섹시한 사람.", "너도 안녕.",
    "여행하면서 재밌는 걸 박아본 적 있어?", "내 가슴 진짜 크지!",
    "내 보지 냄새 좋지? 엄청 달콤해.", "누구랑이든 섹스하는 게 좋아!",
    "쓰고 싶으면 내 보지에서 바이브레이터 빼서 써도 돼.", "우리 보지의 달콤한 냄새 맡을 수 있지.",
    "섹스 파티 뒷수습으로 혀가 항상 아파.", "성처리 도구로 팔리고 싶은데, 여긴 그런 게 없네.",
    "번개를 찾는다면, 널 위한 구멍 세 개가 준비돼 있어.",
]
STR_KO = {  # scattered EN lines inside otherwise-KO arrays
    "Uh-oh...": "이런...", "Victory": "승리야", "Phew": "휴우",
    "Heh.": "헤헤.", "Yes": "좋아", "Stop!": "멈춰!", "Hey": "이봐",
}
DIALOG = [  # (provider patch, our patch, section path, ko_transform)
    ('/dialog/converse.patch', '/dialog/converse.config.patch', '/greeting/lustling', 'greeting'),
    ('/dialog/combat.config.patch', '/dialog/combat.config.patch', '/attack/lustling', 'strmap'),
    ('/dialog/combat.config.patch', '/dialog/combat.config.patch', '/killedTarget/lustling', 'strmap'),
    ('/dialog/flee.config.patch', '/dialog/flee.config.patch', '/helpme/lustling', 'strmap'),
    ('/dialog/arrivedhome.config.patch', '/dialog/arrivedhome.config.patch', '/rent/lustling', 'strmap'),
]
def provider_value(pfn, ppath):
    raw = prov.read(pfn).decode('utf-8')
    if pfn == '/dialog/converse.patch':  # malformed: outer op object unclosed
        i = raw.find('"default"')
        # array of plain string literals to EOF
        return [json.loads('"' + s + '"') for s in
                re.findall(r'"((?:[^"\\]|\\.)*)"', raw[i + len('"default"'):])]
    ops = []; opsof(json.loads(raw), ops)
    for o in ops:
        if o.get('path') == ppath:
            v = o['value']
            return v.get('default', v) if isinstance(v, dict) else v
    return None

dialog_ops = {}  # our patch -> list of [test,replace] groups
for pfn, ofn, ppath, mode in DIALOG:
    arr = provider_value(pfn, ppath)
    if not isinstance(arr, list):
        print('SKIP (no provider value):', pfn, ppath); continue
    if mode == 'greeting':
        if len(arr) != len(GREET_KO):
            print('GREETING LEN MISMATCH', len(arr), len(GREET_KO)); continue
        ko_arr = GREET_KO
    else:
        ko_arr = [STR_KO.get(s, s) for s in arr]
        still_en = [s for s in ko_arr if not KO_RE.search(s)]
        if still_en:
            print('STILL EN in', ppath, still_en); continue
    dialog_ops.setdefault(ofn, []).append([
        {"op": "test", "path": ppath + "/default", "value": arr},
        {"op": "replace", "path": ppath + "/default", "value": ko_arr},
    ])
    print('dialog group:', ofn, ppath, len(arr), 'lines')

# ---------- 3) apply overrides ----------
pk = Pak(TR)
overrides = {}
# lustlingDescription groups: append to each asset patch
byfile = {}
for pfn, en in desc_rows:
    if en in KO: byfile.setdefault(pfn, []).append(en)
for pfn, ens in byfile.items():
    if pfn not in pk.index:
        print('NO OUR PATCH:', pfn); continue
    doc = json.loads(pk.read(pfn).decode('utf-8'))
    if not isinstance(doc, list): doc = [doc]
    for en in ens:
        doc.append([{"op": "test", "path": "/lustlingDescription", "value": en},
                    {"op": "replace", "path": "/lustlingDescription", "value": KO[en]}])
    overrides[pfn] = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
# dialog groups
for ofn, groups in dialog_ops.items():
    doc = json.loads(pk.read(ofn).decode('utf-8'))
    if not isinstance(doc, list): doc = [doc]
    doc.extend(groups)
    overrides[ofn] = json.dumps(doc, ensure_ascii=False, separators=(',', ':')).encode('utf-8')

print('patch files to rewrite:', len(overrides),
      '| desc groups:', sum(len(v) for v in byfile.values()),
      '| dialog groups:', sum(len(v) for v in dialog_ops.values()))
# filled TSV for audit
with io.open(BASE + r'\data\lust_desc_filled.tsv', 'w', encoding='utf-8', newline='') as f:
    f.write('asset\tpath\ten\tko\n')
    for pfn, en in desc_rows:
        f.write('%s\t/lustlingDescription\t%s\t%s\n' % (pfn, en, KO.get(en, '')))
if APPLY and overrides and not missing:
    write_pak(TR, TR, overrides)
    print('applied')
