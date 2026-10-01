import io,sys,csv,json,re
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
csv.field_size_limit(10**8)
src={}
with open('data/rest_worklist.tsv',encoding='utf-8',errors='replace',newline='') as f:
    for row in csv.reader(f, delimiter='\t', quotechar='"'):
        if row and row[0].isdigit(): src[row[0]]=row[2]

import ast
_src97 = open('gen_0597.py', encoding='utf-8').read()
_node = ast.parse(_src97)
BASE = None
for _n in _node.body:
    if isinstance(_n, ast.Assign) and getattr(_n.targets[0], 'id', '') == 'SUB':
        BASE = ast.literal_eval(_n.value); break
SUB = list(BASE) + [
 ('Manuf. Smith & Wesson','제조사: 스미스 & 웨슨'),
 ('Manuf. Soviet Union','제조사: 소련'),
 ('Manuf. Spikes Tactical','제조사: 스파이크스 택티컬'),
 ('Manuf. Springfield Armory','제조사: 스프링필드 아모리'),
 ('Manuf. Steyr Mannlicher','제조사: 슈타이어 만리허'),
 ('Manuf. Sturm, Ruger','제조사: 스터름 루거'),
 ('Manuf. Taurus International','제조사: 토러스 인터내셔널'),
 ('Manuf. Tula Arms Plant','제조사: 툴라 병기 공장'),
 ('Manuf. Tulsky Oruzheiny Zavod','제조사: 툴스키 오루제이니 자보드'),
 ('Manuf. U.S. ARMY','제조사: 미 육군'),
 ('Manuf. United States','제조사: 미국'),
 ('Manuf. Walther','제조사: 발터'),
 ('Manuf. Česká zbrojovka','제조사: 체스카 즈브로요프카'),
 ('Manuf. ffs_spanner','제조사: ffs_spanner'),
 ('Thompson/Center Contender G2','톰프슨/센터 컨텐더 G2'),
 ('U.S. Service Rifle M1 Garand','미국 제식 소총 M1 가란드'),
 ('One of a kind!','세상에 하나뿐인 물건!'),
 ('Equiping status :','장착 상태 :'),
 ('Effective Range :','유효 사거리 :'),
 ('10-rounds Cylinder','10발 실린더'),
 ('1-round Cylinder','1발 실린더'),
 ('4 barrels with a cartridge','탄환 장착 4총신'),
 ('En-block clip','엔블록 클립'),
 ('Single shot','단발'),
 ('Single-Action','싱글액션'),
 ('Blowback, closed bolt','블로우백, 폐쇄 볼트'),
 ('Blowback','블로우백'),
 ('Gas-operated','가스 작동식'),
 ('Double action','더블액션'),
 ('LMB : UDZS Impact fuze arming after 1.5secs','LMB : UDZS 충격 신관 1.5초 후 발동'),
 ('RMB : Time delay after 3.0 secs','RMB : 3.0초 지연 발사'),
 ('Impact grenade','충격 수류탄'),
 ('Time-fused grenade','시한식 수류탄'),
 ('5 Seconds to activate.','작동까지 5초.'),
 ('LMB : Throw grenade to long-distance.','LMB : 수류탄을 원거리로 투척.'),
 ('RMB : Throw 3s cooked grenade to long-distance.(2s to explode)','RMB : 3초 끓인 수류탄을 원거리로 투척.(2초 후 폭발)'),
 ('^red;Check your fire! Explosion can damage to player.','^red;사격 주의! 폭발은 플레이어에게도 피해를 준다.'),
 ("^red;If a grenadier is too close to the target, it'll be very dangerous.",'^red;유탄병이 표적에 너무 가까우면 매우 위험하다.'),
 ('2Point Sling','2점식 슬링'),
 ('Swarovski 1.5× telescopic sight','스와로브스키 1.5× 망원 조준경'),
 ('Fleschete','플레셰트'),
 ('Incendiary','소이'),
 ('EPIC battery','EPIC 배터리'),
 ('Omegacharged Plasma','오메가충전 플라즈마'),
 ('Overcharged Badassery','과충전 배대서리'),
 ('Magnetic Sling+Tactical Flash+TurboJet+Tripleshot','마그네틱 슬링+전술 섬광+터보제트+삼연발'),
 ("You beat hardcore mode!'.","하드코어 모드를 클리어했다!'."),
 ("''You deserve this weapon because you're epic.''","''네가 에픽이니까 이 무기를 받을 자격이 있다.''"),
 ('Blocks','블록'),
 ('blocks','블록'),
]
SUB.sort(key=lambda x:-len(x[0]))

ids = [str(i) for i in range(123919,123944)] + [str(i) for i in range(123945,123947)]
D={}
for rid in ids:
    if rid not in src: continue
    out=[]
    for ln in src[rid].split('\n'):
        if not ln.strip():
            out.append(ln); continue
        t=ln
        for a,b in SUB: t=t.replace(a,b)
        out.append(t)
    D[rid]='\n'.join(out)

D['123947']='^#ffbe32;갈라르호른^reset;'
D['123948']='^#ffbed7;크^#f598d4;로^#ff86bf;마^#c381da; ^#937ef0;광^#6f54e5;석 ^#ff86bf;^#c381da;^#937ef0;^#reset;'
D['123949']='^#ffbed7;레^#f598d4;소^#ff86bf;나^#c381da; ^#937ef0;블^#6f54e5;록 ^#f598d4;^#ff86bf;^#c381da;^#937ef0;^#6f54e5;^#reset;'
D['123950']='^#ffc14e;KX-1 채굴기^reset; ^yellow;⟦E024⟧^reset;'
D['123951']='^#ffc800;A.A.W PL-10 이그제큐셔너'
D['123952']='^#ffc800;AC247 퍼니셔'
D['123953']='^#ffc800;AM112 사이클론'
D['123954']='^#ffc800;MS 아발란치'
D['123955']='^#ffc800;P127HR'
D['123956']='^#ffc800;P200MLRS'
D['123957']='^#ffc800;PL-10 이그제큐셔너'
D['123958']='^#ffc800;RC-88 시즈해머 (NPC 전용. GL만)'
D['123959']='^#ffc800;RC-88 시즈해머 (NPC 전용, 레일 전용)'
D['123960']='^#ffc931;보이저의 선물^reset;'
D['123961']='^#ffd080;홀리데이 스피릿^reset;\n\n소나베일 기간에는 홀리데이 스피릿 - 계절의 기쁨과 공동체의 따뜻함을 상징하는 토큰 - 을 선물로 받을지도 모른다!\n\n이 작은 물건들은 축제 분위기를 담고 있다. 농축된 축하 에너지로 만들어진다는 말도 있다!'
D['123962']='^#ffd080;스트링 라이트와 장식^reset;\n\n어디든 알록달록한 스트링 라이트를 걸어라! 길고 어두운 밤을 밝히고 따뜻하고 축제다운 분위기를 만들어 준다.\n\n벽 스카프와 천 장식은 실내에 색감과 아늑함을 더해 준다. 따뜻한 빨강, 노랑, 하양이 바깥의 차가운 푸른 눈과 아름답게 대비된다!'
D['123963']='^#ffd24c;(이 페이지에는 루모스 그림이 있고, 주변을 많은 빛이 둘러싸고 있다. 행복해 보인다.)^reset;'
D['123964']='^#ffd24c;(가이드의 나머지와 달리 이 페이지는 손글씨로 적혀 있는 것 같다.) ^reset;\n^cyan;테넌트 종류:^reset; ^#ffff73;루모스?^reset;\n빛 주세요. \n^#ffd24c;필요함:^reset;\n^#BC9262;~2x 새터니안 가구 ^#8f8f8f;(제발)^#BC9262;\n^#ffd24c;~50x ^#BC9262;광원 ^#ffd24c;(엄청 중요!!!)^reset;'
D['123965']='^#ffd24c;옐로 ^#867CAC;I^#D8608C;O^reset; 번팅 8x12-B'
D['123966']='^#ffd24c;옐로 ^#867CAC;I^#ffd24c;O^reset; 번팅 5x2'
D['123967']='^#ffd24c;옐로 ^#867CAC;I^#ffd24c;O^reset; 번팅 5x3'
D['123968']='^#ffd24c;옐로 ^#867CAC;I^#ffd24c;O^reset; 번팅 8x12'
D['123969']='^#ffd24c;~경비 테넌트~^reset;\n^cyan;테넌트 종류:^reset; ^#BC9262;마을 경비병^reset;\n마을 경비병은 다양한 무기를 가질 수 있다. 6개의 티어 가구 오브젝트나 ^cyan;방어 보석^reset;을 추가하지 않으면 Lv. 1이 된다.\n^#ffd24c;필요 오브젝트:^reset;\n^#BC9262;-6x 새터니안 가구 ^#8f8f8f;(아무거나)^#BC9262;\n-8x 전투 오브젝트 ^#8f8f8f;(무기 상자와 진열대)\n^#ffd24c;상위 레벨 경비병에 필요:^reset;\n^#BC9262;-6x 다음 ^#ff4c4d;중 하나^#BC9262;로 만든 가구:^reset;\nL2-텅스텐 L3-티타늄 L4-듀라스틸\n^reset;^#ff4c4d;또는 ^#ffd24c;-1x 페로지움/솔라리움 방어 보석(L5/L6용)'

json.dump(D, open('priority_0598.json','w',encoding='utf-8'), ensure_ascii=False, indent=0)
print('rows:',len(D))
