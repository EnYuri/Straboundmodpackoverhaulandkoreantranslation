import io,sys,json
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
D={}
D['124284']='''^cornflowerblue;네가 필요하다! 오늘 USCM 우주 프로그램에 지원해서 별들을 탐험하라! 이 행복한 지원자의 말을 들어 봐라... 우주에서:^reset;
"결국 작은 괴물들도 큰 놈들만큼 살인적이고 치명적이더라고. 누가 알았겠어? 그냥 고양이나 입양할 걸 그랬어. 아무튼 나머지 크루는 다 죽었는데, 뭐 아쉽지만 곱씹어봤자야.
그러니까 계속 괜찮은 행성을 찾아야겠어. 촉수 없는 곳으로. 살인 식물인도 없고, 거대 거미도 없고, 세금도 없는 곳으로. 그래, 인류가 별들을 차지할 때가 됐다!"'''
D['124286']='^cyan;(파손) 매지사이트 FTL 수정^reset;'
D['124287']='''^cyan;1. 신앙심을 유지하라^reset;

우리는 ^green;강한 신앙^reset;이 천사가 ^green;신성력을 지키는^reset; 데 도움이 된다고 믿는다. ^yellow;컬티베이터^reset;와 강한 유대를 맺고 ^orange;최소 일주일에 한 번 기도하는 것^reset;을 권한다.

^cyan;2. 무리 지어 생활하라^reset;

^orange;혼자 생활하는^reset; 천사나 떠돌아다니는 천사가 ^orange;^red;루인드^reset;의 대열에 합류할 가능성이 더 높다는 것을 알아냈다. 우리가 ^green;함께 지내는^reset; 한 우리는 ^green;강하게 남을 수 있다^reset;.'''
D['124288']='''^cyan;3. 악에서 멀어져라^reset;

^red;영웅이 되려 하지 마라^reset;. ^red;데몬^reset;이나 ^red;루인드^reset; 같은 위협에 맞설 준비가 제대로 되지 않았다면 말이다. ^green;전투는 수호자에게 맡겨라^reset;.

^cyan;4. 성수^reset;

만약 네가 수호자이거나, ^red;루인드^reset;나 ^red;데몬^reset;과 접촉하게 된다면, ^green;성수를 마시고 그것으로 목욕하는 것^reset;이 ^orange;최후의 수단^reset;이다. 초기 루인화에 보통 수반되는 증상들을 늦추는 데 도움이 될 수 있다. 아니면,'''
D['124289']='^cyan;<target>은(는) 아키의 친구다. 선물하고 싶다고? 아키를 도와줄래?'
D['124290']='^cyan;<target>이(가) 계속 임무를 방해하는데, <target.pronoun.object>을(를) 그냥 둘 수 없어!'
D['124291']='^cyan;> 그것들은 ^green;커스텀 대화도 담을 수 있다!'
def wings(title,vals):
    colors=['하얀','금','빨간','보라','주황','분홍','파란','초록','갈색','검은']
    lines=['%s날개: ^green;%s%% 출력^reset;'%(c,v) for c,v in zip(colors,vals)]
    return '^cyan;%s^reset;\n\n'%title+'\n'.join(lines)
D['124292']=wings('천사',[64.2,59.2,54.2,49.2,44.2,39.2,34.2,29.2,24.2,19.2])
D['124293']=wings('대천사',[100,95,90,85,80,75,70,65,60,55])
D['124294']='^cyan;기술을 ^orange;벽에 대고^reset; 발동하면, 자동으로 벽에 달라붙는다.'
D['124295']='^cyan;고급 농업 EMC 테이블^white;'
D['124296']='^cyan;고급 수렵 EMC 테이블^white;'
D['124297']='^cyan;고급 채광 EMC 테이블^white;'
D['124298']='^cyan;이온 연료 정화기^reset;'
D['124299']='^cyan;아키가 <target>에게 잘 보이고 싶어. 아키를 도와줄래?'
D['124300']='^cyan;미지의 괴물^reset;? 흥미롭군, 이 폐허에서 미지의 생물은 본 적이 없는데. 아키라... 제2 구조대 리더는 강한 녀석이다. 오래 같이 일해 왔다. 괜찮을 거라 믿는다.'
D['124302']='^cyan;암 캐논 (얼음)^reset;'
D['124304']='^cyan;블랙 프로스트^reset; ^yellow;⟦E024⟧^reset;'
D['124305']='^cyan;블래스트캡 발사기 Mk2^reset;'
D['124306']='^cyan;블래스트마크^reset; ^yellow;⟦E024⟧^reset;'
D['124307']='^cyan;파랑 - 액체 펌프에 연결^reset;. 방출된 액체를 가압한다.'
D['124308']='^cyan;파랑 - 액체 펌프에 연결^reset;. 이 출력은 방출하는 액체를 가압한다.'
D['124309']='^cyan;브리치 블래스터^reset; ^yellow;⟦E024⟧^reset;'
D['124310']='^cyan;브리치 권총^reset; ^yellow;⟦E024⟧^reset;'
D['124311']='^cyan;브리치 리퍼^reset; ^yellow;⟦E024⟧^reset;'
D['124312']='''^cyan;장례 전통^reset;
남겨진 육신은 필멸자의 것과 거의 같다. ^orange;기형이 생기고 부패하기^reset; 시작할 수 있기 때문이다. 그 일이 일어나기 전에, 동료 천사의 친구나 가족이 ^green;부드러운 땅에 고인을 묻는다^reset;. ^yellow;지역 공동묘지^reset;에서. 우리 천사는 ^green;컬티베이터가 만든 모든 것을 지키기 위해^reset; 만들어졌으므로, 죽은 뒤에도 몸으로 ^yellow;새 생명과 양분을 제공할^reset; 수 있다. 고인이 된 천사의 몸은 우리 공동묘지에 자라는 많은 식물에 영양분을 제공할 것이다.'''
D['124313']='^cyan;버니네이터^reset; ^yellow;⟦E024⟧^reset;'
D['124314']='^cyan;C-7 채굴기^reset; ^green;⟦E024⟧^reset;'
D['124315']=wings('케루빔',[71.4,66.4,61.4,56.4,51.4,46.4,41.4,36.4,31.4,26.4])
D['124316']='''^cyan;축하합니다!^reset;
            당신은 방금 어머니가 되었습니다!

무엇보다, 이 불쌍하고 망가지고 전쟁으로 가득한 우주에 사랑과 가족을 데려와 주셔서 감사합니다! 이런 상황에서 올바른 짝을 찾는 것은 위대한 업적인데, 해내셨군요*!

(* 저자는 독자에게 발생한 비합의적 임신에 대해 책임을 지지 않습니다.)'''
D['124317']=wings('큐피드',[57.1,52.1,47.1,42.1,37.1,32.1,27.1,22.1,17.1,12.1])
D['124318']='^cyan;선하 대위^reset;는 ^orange;믿을 수 있는 동맹^reset;임을 입증했다 - 당분간은 ^green;그녀의 조언을 따르는 것^reset;이 좋을 것이다.'
D['124319']='''^cyan;챌린지 도어^reset;:

lofty_irisil_cd_threadtheneedle
^#888888;좁은 공간과 정밀한 이동에 초점을 둔 챌린지 룸. (숨겨진) 아이리사 조각상 보장.^reset;

^cyan;던전 도어^reset;:

lofty_irisil_cd_pickmeup
^#888888;(작업 중) 그래플링 훅 기믹에 초점을 둔 넓은 던전. GLHF^reset;

lofty_irisil_challengereturndoor
^#888888;던전 출구 문. GGWP.^reset;'''
D['124321']='''^cyan;복장 파츠^reset;:

lofty_irisil_clingy
^#888888;아이리사 배낭^reset;'''
D['124322']='''^cyan;플라즈마로 계산 (세트 보너스)^reset;
^yellow;기절^reset;시키고 적을 ^cyan;약화^reset;시킨다.'''
D['124323']='''^cyan;플라즈마로 계산 (세트 보너스)^reset;
^yellow;기절^reset;시키고 ^cyan;경미한 취약성^reset;을 적용한다.'''
D['124324']='''^cyan;제작 재료^reset;:

lofty_irisileye
^#888888;대부분의 아이리숍 레시피에 쓰이는 제작 재료.^reset;

lofty_irisil_ct_pickmeup
^#888888;'픽 미 업' 던전 완료 증표.^reset;'''
D['124325']='^cyan;크리스탈린 니들러^reset;'
D['124326']='^cyan;정액 생성기^white;'
D['124327']='^cyan;다라바이^reset; ^yellow;⟦E024⟧^reset;'
D['124328']='^cyan;데드아이^reset; ^yellow;⟦E024⟧^reset;'
D['124329']='''^cyan;죽음^reset;
천사는 ^green;신성력이 완전히 몸을 떠났을 때^reset;만 죽는다. 신성력은 격렬한 전투를 통해, 또는 긴 삶의 끝에 방출될 수 있다. 컬티베이터가 더는 우리와 함께하지 않기 때문에, 우리의 신성력은 ^red;언젠가 고갈된다^reset;. 죽음으로 이어지지만, 컬티베이터와 함께하는 영원으로도 이어진다 ^gray;(우리는 기도한다)^reset;.

천사가 죽으면 그들의 ^orange;헤일로는 사라진다^reset;. 마치 먼지처럼 공중으로 옅어진다. ^orange;천사의 날개는 시들기 시작하고 시든다'''
D['124330']='^cyan;데스스트라이크^reset; ^yellow;⟦E024⟧^reset;'
D['124331']='''^cyan;장식^reset; (1/5):

lofty_irisilaf
^#888888;아이리사 액션 피겨^reset;

lofty_irisil_alpacastatue
^#888888;알파카 조각상^reset;

lofty_irisil_eyetrophy
^#888888;아이리사 눈 트로피^reset;

lofty_irisil_froggoclocksomewhere
^#888888;어딘가는 개구리 시간^reset;'''
D['124332']='''^cyan;장식^reset; (2/5):

lofty_irisil_irisaplushie
^#888888;아이리사 봉제인형^reset;

lofty_irisil_irisastatue
^#888888;아이리사 조각상^reset;

lofty_irisil_lurkingirisa
^#888888;잠복한 아이리사^reset;

lofty_irisil_medievalnoticeboard
^#888888;중세풍 게시판^reset;'''
D['124333']='''^cyan;장식^reset; (3/5):

lofty_irisil_scleramite
^#888888;스클레라마이트 (포획된 곤충)^reset;

lofty_irisil_secretcactus
^#888888;비밀 선인장^reset;

lofty_irisil_smalltacklebox
^#888888;소형 태클 상자^reset;'''
D['124334']='''^cyan;장식^reset; (4/5):

lofty_irisil_stationanimalcrate
^#888888;동물 우리처럼 보이는 스테이션 상자.^reset;

lofty_irisil_stationanimalcrateeyes
^#888888;쉭쉭 소리를 내는 상호작용 상자.^reset;

lofty_irisil_stationtradesignexoticanimals
^#888888;알 로고가 있는 애니메이션 스테이션 거래품 표지판.^reset;'''
D['124335']='''^cyan;장식^reset; (5/5):

lofty_irisil_pettingzmoo
^#888888;지무 쓰다듬기 표지판.^reset;'''
D['124336']='^cyan;기본 레시피 해금기^reset;'
D['124337']='''^cyan;목적지 트랜스폰더^reset;:

lofty_irisil_exoticanimalsstationspawner
^#888888;희귀 동물 거래 상인이 있는 우주 정거장을 생성한다.^reset;

lofty_irisil_fisheyespawner
^#888888;거대 눈알 낚시 구역을 생성한다.^reset;

lofty_irisil_miniknogasteroidspawner
^#888888;미니크녹 소행성 기지를 생성한다. 위협 등급은 6으로 표시되지만 실제로는 7이다.^reset;'''
json.dump(D, open('priority_0604.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
print(len(D))
