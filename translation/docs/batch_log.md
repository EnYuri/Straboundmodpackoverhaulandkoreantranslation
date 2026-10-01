# 신규 번역 배치별 기록

> README.md에서 분리한 배치별 작업 메모(최신순). 반복 실수와 재사용 규칙은 README.md에 요약되어 있으며,
> 개별 고유명사 결정은 `python term.py "이름"`으로 조회한다. 새 배치 기록은 아래 배치 기록 맨 위에 추가한다.

## 2026-10-01 (11차): CAMPAIGN-53 — Otherworlds(GIC_Otherworlds_contents_3731148374) 미번역 번역

SURVEY 잔여 ~300건 → 추출 547행/유니크 481(재사용 10). `data/ow_uniq.json` +
`ow_ko_01~03.tsv`로 유니크 인덱스→KO 맵 작성, `untrans_batch.py`로 work TSV
채움 후 패치 적용.

- 구성: 인형사/천인/아야·까마귀 텐구(분분마루 신문 문맥)·폭포 캇파 포탑 조작원
  계열·닫힌 눈(사토리)·불사자(호라이)·고대 달토끼·산갈치·캇파/하얀 늑대
  텐구/야마와로 게릴라 세트·해바라기 요괴(유우카)·카이저 기사단
  (대장·기사·기술병·척탄병)·LB 키츠네/쥐 습격병/오니 돌격/통신 장교·LB
  졸병/유탄병/낙하산병/지원병/장교·먼지토끼(토끼의 트라우마)·요정 연합
  (머스킷병·정찰병·기사·자객·마법사·사제, 요정 순환 4세트 보너스)→
  흑화약 일족(BPC) 텐구군·선리스 왕국군(기사단·기사·파이크병·보병·기병,
  불사 4세트 보너스)·로즈 제국(RE)와 웨스트 스타(WS) 군복군(정치장교·
  왕립 사냥꾼/병사·보병·공병·코만도·돌격 장교·저격병·공병·전차병·
  에셜론·패스파인더·레인저)·비전 증강(오브·수집기·사이트)·완드 발사기
  7종·마기로켓 발사기·수리 킷 3종·장신구 대군(탄약 팩·비전 수정·돌격/
  정예/수류탄/기관총/소총/저격/레인저 패키지·방벽/결속 부적·전격전/성채
  교리·저주받은 총알·무녀 리본·신호 막대·부적 다발·물약 탄띠 등).
- 정착용어 유지: 텐구/캇파/요괴/사토리/야마와로/키츠네/오니/루나리안,
  라이온 대대·라이온 제국·크라운 연방·로즈 제국·웨스트 스타·대륙 전쟁·
  카이저, 빌드 오더·배치 명령·보병 소환·제압·점화, 소화기/참격/찌르기/
  타격/근접/중화기/사이킥/열/출혈/폭발/탄도, 전장식·마길록·매지샷·
  마기로켓·우드랜즈 무기 숙련·재사용 대기·장신구·능력 마나·HIT-SHIELD.
- 신규 명명: 흑화약 일족(BPC), 선리스(Sunless), 요정 순환(Fairy Cycle)·
  전쟁 요정(War Fairy), 토끼의 트라우마, 텐구 동조, 무녀 리본, 완드 발사기,
  주문 촉매, 비전 증강, 산갈치(oarfish), 분분마루 신문, 사투시오 마을.
- 교훈 재확인: 청크 작성 중 원문 미확인 구간을 추정으로 썼다가 인덱스 전면
  불일치(21~37·115~123) — 원문 덤프와의 전수 대조 후 재작성으로 해결.
- 검수: 유니크 481 전량, 태그·개행 불일치 0. 적용: 패치 303파일, 스킵 0.
  배포 pak 67,670엔트리.

## 2026-10-01 (10차): CAMPAIGN-52 — Saturnians(Saturnians_contents_1103027918) 미번역 번역

SURVEY 잔여 592건 → 추출 1,485행/유니크 1,303(재사용 91). `data/sat_work.tsv` +
`sat_ko_01~06.tsv`(+`sat_ko_04b`, `sat_names.tsv`)로 KO 맵 작성,
`untrans_batch.py`로 패치 적용.

- 구성: 새터니안 갑옷 세트 대군(로열 아처·록 슬레이어·로열 선·문 가드·
  마법사·과학·EVA·수정·병사·LN49·미드나이트·카이타·SK414·노바·
  와스프밈 등), 바닐라/커스텀 코스메틱 모자 대군, 글리치·인간 갑옷 변형,
  나방 날개·합성 날개(학명 줄바꿈 보존), 콘택트·안경·스카프·로브·염료,
  새터니안 건축재·제작 도구군.
- 정본 반영: `Saturnian`→`새터니안`(초기 `토성인` ~130건 전량 교정 후
  재적용), `Solalei`→`솔라레이`, `Kyterran`→`카이테란`.
- 식별자형 itemName 스텁은 형제 표시명의 한국어로 매핑, `^cyan;\ue012^white;`
  등 글리프 접두는 원문 그대로 보존.
- 스킵 6건(`title`/`subtitle` 중첩 `/interactData/paneLayoutOverride/
  windowtitle/` — saturnArmorTransmog·saturnFurnitureSummoner·
  saturnMagicLoom): 기존 패치 op를 유지한 채 중첩 op를 병합해 재작성
  (재적용 시 다시 덮어써지므로 병합 재실행 후 확인).
- 검수: 유니크 1,303 전량, 태그 불일치 0(날개 학명 개행 복원 포함).
  적용: 패치 592파일, 1,485필드. 배포 pak 67,367엔트리.

## 2026-10-01 (9차): CAMPAIGN-51 — skpkmn(contents_2593214277, 포켓몬 코스튬) 미번역 번역

SURVEY 잔여 444건 → 추출 447행/유니크 447(재사용 4). `data/skpkmn_uniq.json` +
`skpkmn_ko_01.tsv`(정규식 변환 스크립트 생성)로 KO 맵 작성, `untrans_batch.py`로
work TSV 채움 후 패치 적용.

- 구성: 포켓몬 1세대(001–151) 코스튬 부위 명칭 `NNN 이름 (부위)` 전량
  (Back→등·Chest→흉갑·Head→투구·Legs→각갑), ???·None·Oak(오박사) 의상,
  포켓몬 스테이션 Gen 1 작업대(이름·설명·창 제목·부제).
- 포켓몬명은 공식 한국어 명칭(이상해씨·파이리·꼬부기·피카츄·뮤츠 등),
  변형 접미(a–e 변색·암수 표기)와 공백 기행(이중 공백·괄호 앞 공백 없음·
  선행/후행 공백)은 원문 그대로 보존.
- 재사용 항목은 기존 정본 유지(`포켓몬`, `포켓몬 스테이션 1세대`, `^#b9b5b2;포켓몬`).
- 스킵 2건(`title`/`subtitle`이 `/interactData/paneLayoutOverride/windowtitle/`
  중첩)은 수동 패치로 보완 — 같은 오브젝트의 탑레벨 2필드와 병합해 4op 패치로 재작성.
- 검수: 유니크 447 전량, 태그·개행·가장자리 공백 불일치 0. 적용: 패치 444파일.
  배포 pak 66,775엔트리.

## 2026-10-01 (8차): CAMPAIGN-50 — Viera(ffxiv_viera_contents_732276079) 미번역 번역

SURVEY 잔여 444건 → 추출 889행/유니크 613(재사용 270). `data/viera_uniq.json` +
`viera_ko_01~03.tsv`로 유니크 인덱스→KO 맵 작성, `untrans_batch.py`로 work TSV
채움 후 패치 적용.

- 구성: 크리스탈 오라 4종(에어·밸런스·디퓨전·히팅 — 마기사이트), 모글 광부
  모자, 모글 잡 갑옷(애니미스트·흑마도사·초코보 기사·플린트록·퓨질리어·
  저글러·모글 기사·도적·시간 마도사·팅커), 모글 의상/정비공 세트, 모글
  티어 갑옷 10계열(팅커킨→철·가제티어→텅스텐·이노베이터→티타늄·
  아티피서→듀라스틸·에테르위버→에지솔트·기어스피너→페로지움·퍼프가드→
  바이올륨·모지니어→에지+솔라·스펠라이트→페로+솔라·바이올륨 모글),
  비에라 캐주얼/엘레멘탈리스트/펜서/적백마도사/보호국 셔츠/스카프,
  비에라 가발 ~60종(컷·앞머리·포니테일 변형), 선하 세트, 연고 제작자·
  숲 수호자, 비에라 잡 갑옷(궁사·암살자·드라군·하이윈드·녹마도사·
  스나이퍼·스펠블레이드·소환사·백마도사), 프란 세트, 가죽 세트(트리러너·
  우드트레커·실반·나트하이드·자모르), 금속 실험 갑옷(구리·다이아·황금·
  은), 티어 세트(나그네→철·여행자→텅스텐·항해자→티타늄·개척자→듀라·
  세계 주행자→에지·길잡이→페로·길 지킴이→바이오·사냥대장·길 현자·
  팔랑크스), 가발 염료 34색, 건축 재료 대군(화이트우드·마호가니·달마스칸
  벽돌/대리석/타일/스테인드글라스·판넬·울타리·지붕재·발판·함선 판재),
  크리스탈 랜턴, 도입 퀘스트 텍스트(선하·아르고·마기사이트 코어·나르엘다).
- 정본 반영: `마기사이트`(Magicite), `선하`(Seonha), `숲`(the Wood),
  `우드트레커`(Woodtrekker 보존), `달마스칸`(Dalmascan), `프란`, `아르고`,
  `나르엘다`(Naar'elda), `일람 이카`(Ilam i'Ka).
- 검수: 유니크 613 전량, 태그·개행 불일치 0. 적용: 패치 444파일, 스킵 0.
  배포 pak 66,331엔트리. 패치 샘플·qa_pak_glossary 위반 0.

## 2026-10-01 (7차): CAMPAIGN-49 — GiC 확장(contents_3117942107, ESC) 미번역 번역

SURVEY 잔여 431건 → 추출 836행/유니크 600(재사용 12). `data/gicx_uniq.json` +
`gicx_ko_01~03.tsv`로 유니크 인덱스→KO 맵 작성, `untrans_batch.py`로 work TSV
채움 후 패치 적용.

- 구성: 함재 지원 공격(113mm 정밀 타격·BM-13N·궤도 406mm 포격·파이어호크 AGM·
  개틀링 센트리·고스호크 소사·미니건 탄막·재보급·RPG-40), YFFS 슈트 증강
  (흡수 슈트·아드레노 부스터·홀로 프로젝터·배터리·부적·제세동·인공심장·
  인형), 총기 부착물(소음기·총신·전방 손잡이·유탄발사기·조준경·FCS), 정비 킷,
  승무원 계약(콥스크 소총병·루닌코 달토끼 작전원·N.I 기술자·Y.F.F.S 랜서),
  전술 팩(돌파·의료·보급), 약탈 상인 위장 세트(산적 경제학·문화 계승·기업
  캇파), 수중 기술자 세트, 연방(코세어 M3X·카스카-1M·IVAS·패턴3014·강하
  코만도), 연합체 6B 계열(945/947/702/710·VKBO·공수-스페츠나즈·스트렐치),
  콥스크 차량 승무원·야전 전사(PCV·TDL·세이버투스·지대 보병), 계약병·GOC·
  크루거 태스크포스·저항군(명사수/수호자/게릴라 [2 4 6])·역습·레인저·로보캅,
  민간복, 달토끼 세트, T51B 파워 아머(우라늄 열병), UIU 요원, USCM 구식 장비,
  스타더스트 해군 SEAL(승함전), Y.F.F.S 파워 팩/파워 아머/스카우트 아머
  (철갑 거북·상업 번영·발리스타), 사이클롭스 하층 식민지군, 지하 경찰·
  레테이아 보안, 의료 마스크·미니크녹·니토리(캇파)·늑대 텐구·루인 광신도·
  데스존 스캐브·큐텐 울프가드·크레포스트 40K·가즈리안 패턴 MK.III/IV
  (선봉대·외골격 지원·템페스투스 정예·백랑 강습병·스트레이더)·방독면군,
  니토리 CBRN/공허 갑옷/탐광 슈트·N.I.C 제복/크루원(위브필드)·달 작전원·
  보호국/코스모플롯 선외 슈트, 인공 신체(T-DOLL), 드레스군, 잡항 라벨.
- 중국어 원문 구간(삼각대·차량 승무원·캇파 흉갑·까마귀 텐구복·인공 신체
  공지문) 한국어로 자연 번역.
- 신규 정본: `콥스크`(COPSC), `연합체`(Coalition), `연방`(Commonwealth),
  `야마시로 파이낸셜`, `니토리 인더스트리즈`/`N.I.C`, `루닌코`, `큐텐 그룹`,
  `가즈리안 패턴`, `크레포스트 40K`, `스트레이더`, `GDI`/`은하 방위 보험`,
  `지대 보병`, `야전 전사`, `PCV 충전`, `전술 데이터 링크`, `위브필드`,
  `강의 해결사`, `탐욕/재능 기술자`, `현장 연구`, `철갑 거북`, `화력 보급`,
  `상업 번영`, `발리스타`, `선봉대`, `외골격 지원`, `템페스투스 정예`,
  `백랑 강습병`, `위대한 시대에 태어나`, `승함전`, `이변 요원`(UIU),
  `경보병의 행운`, `스침탄의 행운`, `쏘고 튀기`, `크루거 태스크포스`,
  `명사수/수호자/게릴라` 세트 클래스, `저항군 무장`, `공인 몰수`,
  `센트리 건`, `무한 재장전`, `건쉽`, `VOX 발신기`.
- 검수: 유니크 600 전량 커버(600행), 태그 토큰·개행 불일치 0(74·85 태그
  서열·40 개행·569/573 후행 개행 보정, 68 `통신구`→`배럴` 오역 교정).
  적용: 패치 431파일, 스킵 0. 배포 pak 65,887엔트리. 라이브 패치 샘플 +
  qa_pak_glossary 위반 0.
- 후속: Viera 444·skpkmn 444·Saturnians 592·Otherworlds 303·packed.pak
  248·기타 계속.

## 2026-10-01 (6차): CAMPAIGN-48 — GiC (Galaxy in Conflict) 미번역 번역 1차

SURVEY 실질 미번역 최대 규모(1,307건 추정 → 추출 3,917행/유니크 3,418).
유니크 인덱스→KO 맵을 `data/gic_ko_NN.tsv`로 분할 작성. 적용은
`tools/apply_gic_batch48.py` — `gic_work.tsv` 행의 `en`을 `gic_uniq.json`으로
uniq 인덱스에 매핑, test 값은 GiC pak 라이브 자산에서 재독취.

- 1차 커버: uniq 0-525(526건) → work 547행, 패치 296파일, 엔트리 →63,763.
  구간: 코덱스 제목/본문, 탄창·파워팩·스펠카드, 방어판(플레이트·바이저·헬멧
  키트), 낚시 장비(갈고리·릴), 부적·액세서리(AR 광학기·자동 치유기·오마모리·
  신센구미·마키나리우스·요괴/텐구 유물).
- 정본: `연합 시스템`(United Systems — `연합 체계` 오표기 6건 보정),
  `시스템 보안`, `왕조`, `막부`, `오컬트`, `매지샷`, `마길록`, `게슈탈트`,
  `요괴`, `텐구`, `찌르기`(THRUST), `HIT-SHIELD` 유지, `빗나갈 확률`, `점화`,
  `안정성`, `패링`, `유니탄`, `무기 숙련`, `능력 마나`, `소구경`, `탄도`.
- 신규 관례: OCCULT FORCE(자원 게이지)→`오컬트 기력`, PSYCHIC→`사이킥`,
  Muzzle-Loader→`전장식 화기`, Omamori→`오마모리`, Shinsengumi→`신센구미`,
  Machinarius→`마키나리우스`, Tech Unlocks→`기술 해금`, STATS→`제원`.
- **중대 실수 기록**: 초기 `gic_ko_02.tsv`의 444-525 구간(파트 C)이 이 데이터셋에
  없는 다른 아이템 목록(Seif·Kettlebell·Riverward 등)을 번역한 상태로 병합됐음.
  태그 카운트 QA로는 못 잡고 EN↔KO 내용 대조에서 발각 — 해당 구간 전량 재번역.
  교훈: 인덱스 청크 작성 시 반드시 그 청크의 원문 덤프를 기준으로 쓸 것.
  오탐 파일은 `scratch/_gic_misplaced_ko.tsv`에 보존(타 모드 배치에서 재활용 가능).
- 검수: 인덱스 244-525 완전 커버, 개행·태그 대조 불일치 0(425·523의 추가
  `^orange;`만 한국어 어순 재배치로 의도 유지), `__EESTR__`→330자 `이` 치환,
  용어 QA 위반 0.
- 2차 커버: uniq 526-800(275건, `gic_ko_03.tsv` = 파트 `03a`+`03b`) —
  부적·장신구·아티팩트 구간(룬·반지·인장·수호령·부적·탈리스만·
  바이저 등, Touhou/역사 플레이버 문장 + 효과 블록).
  신규 정본: `참회`(PENITENCE), `사면`(ABSOLUTION), `계시`(DIVINATION),
  `불굴`(STEADFAST), `용맹`(VALOR), `비틀림`(STAGGER), `급속 부식`
  (RAPID CORROSION), `과충전`(OVERCHARGED), `제압`(Suppression),
  `섬광탄`, `집결 소환`(Rally-Summon), `수호령:`(Patron:), `텐구 게다`,
  `피 흠뻑`(Blood-Soaked), `진형 무기`(Formation Weapon), `냉기`(FROST),
  `열`(THERMAL), `감전`(SHOCK), `미확인 환상향 물체`(UFO 드립 보존).
- **개행 관례 교정**: KO TSV의 리터럴 `\n`을 패치 작성 시 실개행으로
  풀도록 `apply_gic_batch48.py`에 `.replace("\\n","\n")` 추가 — GiC EN은
  전량 실개행(리터럴 `\n` 0건). 기존 배포분에도 리터럴로 들어간 값
  121건이 있어 이번 재적용에서 함께 교정(같은 경로 op 교체 병합).
- 검수: 인덱스 526-800 완전 커버(275행), 개행 대조 불일치 0, 태그 차이
  4건(613·693·778·782 — 어순 재배치로 추가한 `^reset;`/`^orange;`,
  의도 유지). 패치 작성 후 tmp pak 검증: 63,903엔트리, REPL 값에
  실개행 확인.
- 산출물: `data/gic_ko_01.tsv`(0-243), `data/gic_ko_02.tsv`(244-525),
  `data/gic_ko_03.tsv`(526-800, 파트 `03a/b`), `scratch/_gic_*.py` 진단군,
  `scratch/_gic_526_800.txt` 원문 덤프.
- 3차 커버(동일 배치): uniq 801-1100(300건, `gic_ko_04.tsv`) —
  반지·장화·부적·장신구 + 총기 부착물(전방 손잡이·양각대·조명·
  레이저 사이트·소염기·소음기·중총신·장총신·조준경·특수 총신·
  코디네이터·이형 무기) 구간.
  신규 관례: Foregrip→`전방 손잡이`, Bipod→`양각대`, Flashlight→`조명`,
  Flash Suppressor→`소염기`, Suppressor→`소음기`, Heavy Barrel→`중총신`,
  Long Barrel→`장총신`, Heat Shroud→`방열 덮개`, Scope→`조준경`,
  Sight→`조준기`, Recoil Recovery→`반동 회복`, Coordinator→`지정기`,
  `겐시디움`(Gensidium — 초기 `겐시듐` 10건 보정), `총 방패`,
  `대결계`, `탄도 저항`, `대전차 피해`.
- **중대 실수 기록(2)**: 초기 `gic_ko_04a/b`의 908-1100 구간이 uniq에
  `Traditional Foregrip` 명칭이 없어 desc-name 교대 패턴이 깨지면서
  KO가 +1칸씩 밀린 상태로 작성됐음(1090-1091은 인접 쌍 교환 혼재).
  EN↔KO 인덱스별 대조로 발각 — 전 구간 재정렬 + 1100 신규 번역,
  1090/1091 스왑 교정. 교훈: uniq의 desc/name 교대는 보장되지 않으므로
  항상 인덱스별 EN을 직접 대조할 것.
- 4차 커버(동일 배치): uniq 1101-1400(300건, `gic_ko_05.tsv` =
  파트 `05a`+`05b`) — 이형 하부 발사기(파편·광란·하케로·표식·
  파수꾼·메이드·베일·니들러·지뢰·미사일·들불·빗자루), GP-25/M203
  UGL 탄종 변형(캐니스터·고폭·조명탄·비닐봉지·고무·전격·연막),
  수리 킷, EWS 레거시 부착물, 공습/포격 비컨, 총기 개조 킷,
  약물·의료 킷(붕대·헤로인·보호국 의료 킷·고필), 방패군
  (라이엇·대방패·스쿠툼·타지·버클러 — 스탯 블록), 보스 잔재
  (장갑 수호자·조정자·전 신도·사토리의 눈·거짓 수호자·다이묘·
  장군·지옥까마귀·레기온·마쿠·암살자·시카리오·루슬란·폭군 재판관·
  늑대 기사단), 토큰·문서·연료봉·영혼.
  신규 정본: `스쿠툼`(Scutum), `타지`, `버클러`, `안정성`(STABILITY),
  `패링 창`(PARRY WINDOW), `방어력`(DEF/blocking power),
  `방패 강타`(Shield Bash), `방패 돌격`(Shield Rush), `퍼펙트 블록`,
  `방패벽`(Testudo), `지옥까마귀`(Hell Raven), `야마자나두`,
  `브랜드 없는`(Unbranded), `영혼 대장장이`(Soulsmith),
  `드루플로란`(Drufloran), `껍데기`(Shell 불사족), `화이트 울프`,
  `늑대 기사`, `옷니엘`, `레기온`(에르키우스 지휘관), `마쿠`,
  `시카리오`, `잔재`(Remnant), `비컨` 반환 구문, `UGL`(하부 유탄),
  `고필`(Go-Pill), `혈환 토큰`(Blood-Loop Token).
- 검수(3+4차): 인덱스 801-1400 전량 커버·EN↔KO 인덱스별 정렬 확인
  (리뷰 파일 `scratch/_gic_04_review.txt`·`_gic_05_review.txt`),
  태그·개행 불일치 0, GP-25/M203 탄종 교차 정합 전량 확인,
  배포 pak 64,221엔트리·실개행·패치 내용 샘플 검증,
  용어 QA 위반 0.
- 5차 커버(동일 배치): uniq 1401-1700(300건, `gic_ko_06.tsv` =
  파트 `06a`+`06b`) — 보호관 품목·문서·연료(글리치 강철 파편·
  익솔링 바이오 연료·살아있는 에르키우스·오카수스 인식표·군사 문서·
  페리카픽스·보호관 신분증·왕복선 일지·자유사상가·황야 수용소/
  포획 포드), 수류탄(뮬 전격·RGD-5 충격·연막·시노비·천둥 폭탄),
  아우그멘티어 총기(HMG·레이저포·권총·소총), 역사 총기(M1 개런드·
  MG 계열·모신 나강·톰슨·엔필드·보히야·후장총 54·가즈-스캐브·
  DShK·EM2·머스탱·샐리), ILWS 변형(식민지·엔필드·가즈리·유니타·
  지구·AKE-40·사이버 M4/PDS-9·XME-8·RSP-61), 활·석궁(챔피언
  전쟁활·오니 슬레이어·영혼 방출기·올빼미 사냥꾼·늑대 기사·
  라이온하트 발리스타), 탄띠군(HGMK121·LF-2·M86·메이드·화염병·
  뮬·네일·구름 수류탄·치유/유혹 술잔), 순간이동기·렐름록 제자일·
  진압 기절 창군, 유탄발사기(STGL40·M79·USM174), 중기관총(T60)·
  산탄총(트란셰야·튜르마)·화염방사기(ROKS U-500)·M16A3.
  신규 정본: `익솔링`, `페리카픽스`, `오카수스`, `아스라`,
  `레테이아 광산 식민지`, `자유사상가`(Free-Thinkers),
  `글리치 사냥꾼 결사단`, `독립 시스템 동맹`, `붉은 별 동맹`,
  `인류 연방`, `사이버`(Syber), `아우그멘티어`, `다이나미코어`,
  `콜로니야`, `페데라치야`, `레시간`, `쿠르토비나`, `체레즈-오몬드
  민간 경비`, `저세상`(OTHERWORLD 스펠카드), `렐름록/렐름스톤`,
  `제자일`, `강시 군단`, `탄띠`(Bandolier), `나이프 부채`,
  `이부키 표주박`, `유혹의 술잔`, `이상한 퍽 발사기`,
  `사이킥 순간이동기`, `스프링레이저 지뢰`, `영혼 소환`,
  `오쿠 제어봉`, `메트로 섐블러`, `바스타드 건`, `공병`(Sapper).
  러시아어 문서 제목(фея·Перемещение)은 원문 유지.
- 검수(5차): 인덱스 1401-1700 전량 커버(300행), 태그·개행 불일치 0
  (1691의 여분 `^reset;` 보정), EN↔KO 인덱스별 전수 대조 완료.
  적용: 매핑 1701, 패치 988파일/1,881op, 병합 1,446. 배포 pak
  64,455엔트리, 샘플 패치(오카수스 인식표) 검증.
- 6차 커버(동일 배치): uniq 1701-2000(300건, `gic_ko_07.tsv` =
  파트 `07a`+`07b`) — USM47 변형군, 나가시마/나가시노 화승총,
  신사 수호자 부적 6종(부식·화염·기름·과충전·표준·강철 끝),
  광충 캡슐, 나이프/부적 부채, 지뢰(모델 50·기절), 화염병·기름 병,
  방어구 세트 대군(베일리 보안 진압/전술, 돌 군단, 신스 정비,
  스위스 알펜플라주, 덴마르카 전열 보병, 선원·선원 병사,
  토마스 베인 해적, 진홍 사무라이, 시마노 기모노, 막부 악마
  사냥꾼·카치·전열 보병·농민·사무라이·신센구미·척후병),
  모자류(바라클라바·비니·베두인·부니햇·볼러·안전모·케피예·
  토킨·탑햇·삼각모·늑대 텐구 베레모), 도적군(기사·레인저·
  투석병·노상강도), 교단 로브, 중세 헬멧(바시넷·세르벨리에레·
  그레이트 헬름·케틀·얌), 전투 마법사, 시력 교정 안경, 장인,
  결투자, 포세아 졸병.
  신규 정본: 세트 보너스 체계(`방어력:`, `[풀 세트]`, 부위 태그),
  `순 막부`(Sun Shogunate), `에스카토스`(Eskhatos),
  `덴마르카`(Denmarka), `포세아`(Fossean), `아시가루`, `진가사`,
  `가부토`, `겜브슨`, `신사 수호자`(Shrine-Guardians),
  `마르키안 개혁`, `부적`(Talisman), `광충`(Brightworm),
  `전장식 숙련`(Muzzle-Loader Proficiency), `소화기`(SMALL-ARMS),
  `출혈 발동`(BLEED PROC), `웅크리기 숙련`, `사무라이의 길`,
  `총의 길`, `일심`, `통일을 위하여`, `배짱과 영광`,
  `솔선수범`, `대상습격자`, `쏘고 튀기`, `단련된 분노`,
  `근접 폭파`, `농민 식사`, `총격전 훈련`, `척후병`,
  `머스킷병`, `투석병`, `타격/참격/찌르기` 피해 유형.
- 검수(6차): 인덱스 1701-2000 전량 커버(300행), 태그·개행 불일치 0.
  적용: 매핑 2001, 패치 1,152파일/2,196op. 배포 pak 64,619엔트리.
- 7차 커버(동일 배치): uniq 2001-2300(300건, `gic_ko_08.tsv` =
  파트 `08a`+`08b`) — 포세아 하의, 자유부대 레인저, 살인자,
  하스타티/벨리테스·몬테포르티노, 줄리안, 로리카 하마타/
  세그멘타타(임페리얼 갈릭·백인대장), 광기 어릿광대, 졸병,
  용병단 기사, 추방자 넝마, 낡은 농민, 리지카 졸병,
  전술 군단병, M80 하이컷, 작전원 모자/헤드셋, 배낭군(A-Tac7·
  식민지군·스캐빈저·울프 공수), 대륙군, 가젤 토브룩·콜로니야·
  민병대 조끼, 옛 모험가/껍데기, 오퍼레이브 Sn. 수트,
  소유즈-디펜더, 워탤트, 요정·요정 근위대/메이드,
  서리 왕조·민병대, 대기록고 악마 기사, 노드의 수호자,
  월면 강습 군단, 달토끼, 뉴 론디니움 기사/병사,
  누에 소녀/전사, 환상향 왕당파, 우라기리모노의 기억,
  불교도, 까마귀/늑대 텐구, 아마노자쿠, 클라운피스,
  듀라한 마녀, 타락한 야마자나두, 수호 교사, 지옥까마귀,
  코이시, 쿠다기츠네.
  신규 정본: `다층 방어`, `이게 우리 방식이야`, `대상수호자`,
  `환영 투창`, `옛 공화국/제국은 서 있다`, `압박하라!`,
  `로마의 리듬`, `예비력 차폐`, `전신갑 수호자`,
  `경보병의 행운`, `자기보존`, `열정의 불`, `자비 없는 화염`,
  `철의 후광`, `반격 사격!`, `핏빛 흡혈자`, `강철의 신앙`,
  `변형`(Shifting Form), `사무라이 공포`, `기도의 타격`,
  `전사 계급`, `고행자`(Flagellant), `공허 보행자`,
  `두 번째 기회`/`다시 쓰인 역사`, `농민 식사`, `풀린 수류탄`;
  지명·인물: `리지카`(Rijikan→리지카인), `뉴 론디니움`,
  `텐마`, `아마노자쿠`/`아마노사구메`/`자키`, `우라기리모노`,
  `코이시`, `쿠다기츠네`, `옛 지옥`, `사천왕`/`비샤몬텐`.
- 검수(7차): 인덱스 2001-2300 전량 커버(300행), 태그·개행 불일치 0.
  EN↔KO 인덱스별 전수 대조 완료. 적용: 매핑 2301,
  패치 1,305파일/2,500op, 잔여 no-ko 1,417.
  배포 pak 64,772엔트리(잠금 재시도로 교체).
- 8차 커버(동일 배치): uniq 2301-2600(300건, `gic_ko_09.tsv` =
  파트 `09a`+`09b`) — 쿠다기츠네, 니토리/캇파, 사무라이 유령
  소녀, 사신, 하쿠레이 무녀, 타타라(코가사), 작은 지휘관,
  고대 전쟁기, 서리 방랑자, 양초 학자, 공허 기사, 시간이동,
  프로메테우스/삼손 방호복, 전술 고르카(TRT 알파), 인민군
  장비 대군(돌격 공병·정치장교·아프간카·우샨카·인형사
  탈영병·저거너트·의무병·스트렐치 6B-710·내무부 SMK·공수·
  스페츠나즈 베레모·TSh-4 전차병·보병·웨빙·스트렐치 6B-2),
  공화국 장비군(군종 장교·보병·M56/M1A1 슈탈헬름·루이스총
  사수·M/22 모피 모자·참호 기사·공병·척탄병·저격수·
  기갑 지휘관·차량 승무원·대위).
  신규 정본: `포탑 기술자`, `사이킥 베기`, `잔혹 표적`,
  `맨손 정화`, `기도에 대한 높은 응답`, `응전 타격`,
  `불굴의 보루`, `무리 소환`, `불타는 머리`, `신성 기사`,
  `스페츠나즈 작전`, `돌격 공병`, `최전방 지휘`, `신속 징집`,
  `불패의 연합`, `조국의 피`, `분노 인도자`, `일인군단`,
  `의무병`, `공포가 곧 힘`, `압도적 존재감`, `공수병`,
  `스침탄의 행운`, `전투원`, `근접전 전투원`, `조국의 빛`,
  `루이스총 사수`, `저격수의 집중`, `선봉`, `공병`,
  `척탄병`, `기계화 사단 - 설상차/소전차`, `차량 승무원`,
  `서리의 맹세`; 지명·인물: `니토리`, `캇파`, `사토리`,
  `하쿠레이 무녀`, `타타라`, `코가사`, `인민군`(People's
  Army), `공화국`(Republic), `인형사`, `베레스카`.
  `gic_s6b710gp45_NVGhead` 등 식별자 스텁은 형제 명칭과
  동일한 표시명으로 자연화.
- 검수(8차): 인덱스 2301-2600 전량 커버(300행), 태그 불일치
  5건 보정(2494/2498/2500/2504의 누락 `^reset;` 추가,
  2529의 과잉 `^reset;` 제거), 개행 불일치 0. EN↔KO 인덱스별
  전수 대조 완료. 적용: 매핑 2600, 패치 1,470파일/2,824op,
  잔여 no-ko 1,093. 배포 pak 64,937엔트리.
- 9차 커버(동일 배치): uniq 2601-2900(300건, `gic_ko_10.tsv` =
  파트 `10a`+`10b`) — 공화국 대위/의무병, 죄인 자루 작전원,
  GP-45 방독면, 레인저(공허 보행자), 베레모/M1/군 불용품
  (불굴의 적응력·부시 세트), 투명 외형 부위, 카발-6,
  AUCU(T-블록), 아웃랜드 반군 공병(통신병/지평선 너머 교리)·
  전투원(다목적 전투원/쏘고 튀기), 용병·부니햇, 식민지
  작전원, CBRN 수트, 전투 안드로이드, 점프 다이버/트루퍼,
  스캐빈저 기사/슬러거(강철 피의 스크라운저·도전자·금속
  폭풍), 아서 클랜(보병·징집병·척후병, 우리는 이렇게 한다),
  형제단 불량배(슈탈헬름·피렐리 T.35), 두더지 클랜(몸통
  갑옷·헬멧·다리갑옷·신입·특수작전, 프렌지 더스트), 옛
  암살자(무리), 시노비 암살자(초인적 반사신경), 지하 경찰
  (폭동 진압 태세), 자유사상가 도시군(경비대·퀴라시어·
  국가방위군·장교·공병), 십자군(기사·병사·배낭, 쇠사슬),
  글리치 헌터(카포테인·잘츠파이어), 강시(청 의복·누안마오·
  베두인·모자·상의, 피 흡수자), 플로란 해방 전선·그린핑거
  근위대·늙은 플로란(사시모노, 불꽃의 결의·불굴의 결의·
  피의 소원), 전격 산적, 유니타 MkIX, 슈탈헬름 현대화·
  민간 방독면·민병대/식민지 전차병, USCM 통합 전투 헬멧군,
  MIKO-95, 산적 두건, 토끼 베레모, 전 광신도, 그린핑거
  사무라이 헬멧, 화약 사냥꾼, 하이랜더 비니(데모나이트),
  사냥꾼 가면, 제국 시노비 가면, CBRN 후드, 스파르타 14T,
  스크래퍼, 스토커 후드티, 합성 고양이 귀, 변경 세계의
  목걸이.
  신규 정본: `죄인 자루`, `프리 다이버`, `전투원`(Warfighter),
  `시체 수거가`, `중무장 전투원`, `부시 용병`/`부시 전사`,
  `불굴의 적응력`/`생존주의자`, `경보병의 행운`, `군 불용품`,
  `순찰모`, `후방 병력`, `투명 [부위]` 외형 슬롯, `카발-6`,
  `첨단 도시 전투복`(AUCU), `T-블록`, `통신병`,
  `지평선 너머 교리`, `PLCE 무전기`, `정밀/미니건 타격 호출`,
  `포병/지원 비컨`, `아웃랜드(인)`, `다목적 전투원`,
  `쏘고 튀기`, `사막 전투원`, `사막 부니햇`, `CBRN`,
  `점프 다이버`/`점프 트루퍼`, `스캐브`, `스캐빈저 기사/
  슬러거`, `스크랩 메탈`, `도전자`, `금속 폭풍`,
  `강철 피의 스크라운저`, `아서 클랜`, `쇠사슬 갑옷`,
  `클랜 보병/징집병/척후병`, `우리는 이렇게 한다`,
  `형제단 불량배`, `피렐리`, `판처파우스트`, `두더지 클랜`,
  `프렌지 더스트`, `옛 암살자`, `무리`(Swarm), `전략 부적`,
  `시노비 암살자`, `초인적 반사신경`, `지하 경찰`,
  `폭동 진압 태세`, `방패 안정성`, `자유사상가`, `도시 경비대`,
  `퀴라시어`, `케틀 헬멧`, `국가방위군`, `도시 공병`,
  `십자군`, `글리치 헌터`, `카포테인`, `잘츠파이어`,
  `강시`, `피 흡수자`, `누안마오`, `탕좡`, `플로란 해방 전선`,
  `그린핑거 근위대`, `사시모노`, `불꽃/불굴의 결의`,
  `피의 소원`, `전격 산적`, `무성한 세계`(Lush)/`가든 행성`,
  `유니타 패턴`, `슈탈헬름 현대화`, `방랑 기사`, `민간 방독면`,
  `민병대 전차병`, `USCM 통합 전투 헬멧`, `USCMICH`,
  `옛 근위대`, `적응형 헬멧 밀폐 장치`, `전 광신도`,
  `화약 사냥꾼`, `삼각모`, `데모나이트`, `제국 시노비 가면`,
  `스파르타 폭동진압 헬멧`, `하부 식민지`, `변경 세계의
  목걸이`.
- 검수(9차): 인덱스 2601-2900 전량 커버(300행), 태그·개행
  불일치 0. EN↔KO 인덱스별 전수 대조 완료(2779·2800·2861·
  2886 의역 보정). 적용: 매핑 2900, 패치 1,643파일/3,149op,
  잔여 no-ko 768. 배포 pak 65,110엔트리.
- 10차 커버(동일 배치): uniq 2901-3200(300건, `gic_ko_11.tsv` =
  파트 `11a`+`11b`) — 달/붉은 태양/요괴 목걸이(라이온하트·탈리스),
  아시가루(아시가루의 결의·퍼펙트 패리), 도전자(킹슬레이어·표적),
  플라질런트(25HP 피해 시 회복), 옛 시노비(회피), 유니타 갑옷
  증강(돌핀-3·이즈크라 인터셉터·유니타 증강 헬멧), 무정부의 천사,
  장갑 보호자(B.I.R.B.), 비스트맨 산적, 식민지 생존자(몬테포르티노),
  에르키우스 증생물/슈라이크 보병/돌 센츄리온, 스타게이저 사제
  날개(클루엑스), 서리 왕조 보병(십오종군정), 페데라치야 센티널,
  유전 광신도(사막의 숨결), 공허 껍데기 기사, 유니버설리스트,
  러스트 장비, 정신 지배, 머스킷병, 형제단 지휘관(강제 징집단·
  아욱실리아), 옛 신스 경비병, 돌 기사단(에르키우스 하이브마인드
  감염), 텐구 상의/치마, 음흉한 가면, 공허 전투 강습 수트(우주
  보병·EPP), 늑대 텐구(늑대 기사/병사·까마귀 텐구·이단자·
  커튼 킬트), USCR 망명 제805 보조 소총 킷(저·중·고기술, 스치는
  행운의 총알·주머니 속 주머니), AIS 동맹군(PPCV·연방 동맹·
  근접전 전투원·MK.2·MICEVCH·오벨 리거·PLCE 배낭·통신병),
  수상한 세트(스푹), 사막 부니햇/식민지군 헬멧/군 불용품(패턴 83·
  그루트삭·자급자족·기관총수), 용병 지휘관(부시 지휘), 용병 상의군
  (소비에트 전투원), 낙하산병·AIS 공수 헬멧군, 야마 소총병,
  빈티지 경찰(발포!·대치/강습 단계).
  신규 정본: `아시가루`, `진가사`/`카사`, `아시가루의 결의`,
  `퍼펙트 패리`, `킹슬레이어`, `표적`(marked), `플라질런트`,
  `지속 피해`(DoT), `돌핀-3`, `이즈크라`, `인터셉터 방탄 시스템`,
  `유니타 증강 전투 헬멧`, `무정부의 천사`, `장갑 보호자`,
  `B.I.R.B.`(관료적으로 격리된 시정 로봇), `비스트맨 산적`,
  `식민지 생존자`, `몬테포르티노`, `제16부서`, `에르키우스 증생물`,
  `슈라이크 보병`, `돌 센츄리온`, `스타게이저 사제 날개`,
  `페데라치야 센티널`, `검치호 투구`, `유전 광신도`,
  `사막의 숨결`, `공허 껍데기 기사`, `유니버설리스트`,
  `하이퍼스펙트럴`, `우주 보병`, `산업용 등식 공기탱크`,
  `두 번째 기회`, `죽음까지`, `러스트`, `정신 지배`,
  `페데라치야 솔`, `머스킷병`, `강제 징집단`, `불량배 징집병`,
  `아욱실리아`, `옛 신스 경비병`, `무자비/무성 머리`, `파워 아머`,
  `돌 기사단`, `텐구 상의/치마`, `음흉한 가면`, `울트라 셰리프`,
  `공허 전투 강습 수트`, `늑대 텐구`/`까마귀 텐구`/`이단자`,
  `늑대 기사`/`늑대 병사`, `커튼 킬트`, `USCR 망명 제805`,
  `보조 소총 킷`, `스치는 행운의 총알`, `주머니 속 주머니`,
  `연방 동맹`, `동맹 전투 헬멧 MK.2`, `MICEVCH`(모듈형 통합 통신
  강화 공허 전투 헬멧), `오벨 리거`, `개인 휴대 장비`(PLCE),
  `전투복 튜닉`, `스푹`, `수상한 ~`, `사막 식민지군 헬멧`,
  `패턴 83`, `그루트삭`, `남아프리카 방위군`, `기관총수`,
  `자급자족`, `용병 지휘관`, `부시 지휘`, `용병 추종자`,
  `소비에트 전투원`, `낙하산병`, `AIS 공수 헬멧`, `야마 소총병`,
  `빈티지 경찰`, `발포!`, `대치 단계`/`강습 단계`, `비틀거림`.
- 검수(10차): 인덱스 2901-3200 전량 커버(300행), 태그·개행
  불일치 0(3067 여분 리터럴 `\n` 제거). EN↔KO 인덱스별 전수 대조
  완료. 적용: 매핑 3200, 패치 1,790파일, 잔여 no-ko 217.
  배포 pak 65,278엔트리. 라이브 패치 샘플 확인(목걸이·아시가루·
  플라질런트·805대·AIS·빈티지 경찰 전 부위).
- 11차 커버(동일 배치): uniq 3201-3417(217건, `gic_ko_12.tsv`) —
  탐정/부패 탐정 의상(불릿인 보드·매서운 눈 세트 효과), 오염된 경찰
  세트, 숲 교단 입문자, 블레이크 맥다몬드 수트, 네드 켈리 갑옷
  (역사 인용 산문 + HIT-SHIELD, £ 보존), 빈티지 수트/페도라 색변형,
  WWII 미 육군 GI·USMC·영 브로디·베르마흐트·소비에트 정치장교
  군복, 야마 경보병/소총병/야전 장교(불굴의 적응력 세트), 아카론
  손전등, 식민지 상인 NPC UI(무기상·채굴·정제·레드얀·배급·여가·
  스크랩 — 선행 공백 2칸 보존), 수행원 NPC(메트로 방랑자·동맹
  군수관·독립체 귀족·달토끼 모계장·평화유지군 기술자/베테랑),
  첨단 탄약 기술자 다중행 설명, 상인/교역 단말기(채굴·은하 표준
  무기·인류 의상점·산업·정제소·변경 식민지), 의료/오컬트 작업대,
  오브젝트(그래피티·후톤·프로젝션-2·타타라·박격포·라케텐베르퍼·
  바다·야콥손·이몬·난간·공중전화·쿠다기츠네), 코덱스 제목군
  (핵전쟁의 시작·대체 야마·라이온하트·보호국 신분증·죽은 행성의
  편지·FNG 은신 보너스·무녀·암살 대상·익살 떨기·스프링필드의 바·
  그랜드 개런드 보급), 퀘스트 제목(제0장 - 방주 너머/계시·충격적인
  각성), 상태이상명(방어 붕괴·방패 붕괴·참회·비틀거림·기절).
  신규 정본: `탐정의 안경`/`불릿인 보드`, `매서운 눈`, `수사 차지`,
  `부패 탐정`, `오염된 경찰`, `숲 교단 입문자`, `블레이크 맥다몬드`,
  `네드`(Ned Kelly — 보습날/양동이 헬멧/앞치마와 챕스), `LARP`,
  `브로디 철모`, `패턴 37 웨빙`, `P40 전투복`, `베르마흐트`,
  `슈탈헬름`, `펠트그라우`, `정치장교`, `야마 경보병`,
  `야마 야전 장교`(제모·죄인 방독면), `아카론 손전등`,
  `식민지 무기상`/`채굴 상인`/`정제 상인`/`레드얀 상인`/`배급 상인`/
  `여가 상인`/`스크랩 상인`, `수행원`(Retainer), `메트로 방랑자`,
  `동맹 군수관`, `독립체 귀족`, `달토끼 모계장`, `평화유지군`,
  `첨단 탄약 기술자`, `상인 단말기`/`교역 단말기`/`변경 식민지`,
  `의료 작업대`, `오컬트 작업대`, `피의 소원`, `방어 붕괴`,
  `방패 붕괴`, `참회`, `비틀거림`, `기절`.
- 검수(11차): 인덱스 3201-3417 전량 커버(217행), 태그 토큰·개행
  불일치 0(3228/3230/3232의 HIT-SHIELD 후행 `^reset;` 보정),
  선행 공백 레이아웃 보존 확인. EN↔KO 인덱스별 전수 대조 완료.
  적용: 매핑 3,417 전량, 패치 1,989파일/3,761op, 잔여 no-ko는
  uniq 외 필드 156건만. 배포 pak 65,456엔트리. 라이브 패치 샘플
  확인(탐정 셔츠·네드 헬멧·야마 경보병·공중전화 등).
  **GiC 유니크 0-3417 전량 번역 완료 — 배치48 종료.**
- 후속: 잔여 156 skip은 uniq 미포함 필드(caption/subtitle 등)로
  별도 큐에서 처리. 배치49+로 GiC확장 430·Viera 444·skpkmn 444·
  Saturnians 307·Otherworlds 300·packed.pak 248·기타 ~7,000 계속.

## 2026-10-01 (5차): CAMPAIGN-47 — Elithian 미번역 번역

SURVEY 실질 미번역 세 번째(663건 추정 → 추출 1,295행: 재사용 231 + 신규 1,064행/
유니크 964). `data/elithian_ko.tsv` 유니크 인덱스→KO 맵(0-349 본파일, 350-703
`elithian_ko2`, 704-963 `elithian_ko3`으로 분할 — heredoc EOF 절단 주의).

- 구성: 종족 태그 설명(`^green;Aegi./Akkimari./Avikan./Droden./Trink./Thelean./
  Generic. ^white;`) 아머 ~600, Type-A/M/S·r.A/M/S 티어 변형(Energetic→기력 사양,
  Powerful→파워 사양, Vigorous→활력 사양), 해로잉 가면·착륙제 의상, Trink 몸체
  부품(Mark I-IV/인포서/실용주의/뱅가드 + v2), UL-i~EH-i 실드, 증강, 상태이상 라벨.
- 용어집 정본 적용(47b): `Aegi`→에지(에이지 금지), `Aegisalt`→에지솔트,
  `Aeginian Federal Union`→에지족 연방 연합, `Terrene Protectorate`→행성 보호국 —
  첫 패스에서 에이지 계열로 잘못 쓴 134op 전량 보정. 그 외 정본: 아비칸/아키마리/
  드로덴/트링크/텔레안/노마다/켈라키/샬라카/센틀라/케프라이더/자히드/텔헌터/
  해로잉/착륙제/오큘러스/팝톱/바이올륨/듀라스틸.
- 상태이상: Burning→화상, Frozen→빙결(용어집), Poisoned→중독, Stunned→기절,
  Slowed→느려짐, Electrified→감전, Cloaked→은신, Violated→침해됨,
  Quicksand→유사, Ionized→이온화, Void-Bound→공허 속박.
- 버그 발견: `untrans_batch.py`의 `find_text`는 필드명 dict로 모아 같은 key의
  중첩 인스턴스를 덮어씀 → `thea_weapons.collection`의 `collectables/*` 87개
  title+description이 워크리스트에서 누락됐었음. `_el_collect.py`로 각 수집품을
  해당 아이템 패치 번역과 매칭해 332op 재사용 + 6건 수동(테르베 리더의 활/
  사건의 지평선 desc/겨울의 포옹/샤드브레이커), 총 345op.
- 적용: 패치 663파일 + 컬렉션 중첩 344op, 엔트리 62,804→63,467,
  용어 QA 위반 0, 태그 대조 신규분 불일치 0.
- 산출물: `data/elithian_work.tsv`, `data/elithian_ko*.tsv`,
  `scratch/_el_*.py`, `scratch/_el_collect_manual.json`.

## 2026-10-01 (4차): CAMPAIGN-46 — FrackinUniverse 미번역 번역

SURVEY 실질 미번역 두 번째(888건 추정 → 실제 1,742필드/유니크 1,472).
`tools/untrans_batch.py extract FrackinUniverse` — 재사용 40행만 매칭(FU 문자열은
기존 번역과 거의 불일치), 나머지 1,742행 수동 번역(`data/fu_ko.tsv`+`fu_ko2`+`fu_ko3`).

- 구성: 재료·가구 블록 ~1,000(Aen/다이너스트/나이타르/페글라시/스카스·테시이드/
  임페르비움/벨루이시/선구자/엘더 패밀리, 가공·장식 목재 세트), 크래프팅 스테이션
  ~200(^cyan;/^orange; 이름 + 연구 속도·전력 요구량 라인), 씨앗·식물 ~230,
  종족별 음식 반응 메시지 등 UI ~40.
- 처리 태그 신규 관례 확정: `Extractable`→`추출 가능`, `Crushable`→`분쇄 가능`,
  `Siftable`→`체질 가능`, `Centrifugable`→`원심분리 가능`, `Smeltable`→`제련 가능`,
  `+N Fuel`→`+N 연료` — 태그·색상 그대로 보존.
- X'ian 계열은 정본 `짜'이` 적용, `Precursor`→`선구자`, `Quietus`→`콰이어투스`,
  `Telebrium`→`텔레브리엄`, `Poptop`→`팝톱`(용어집 준수, 46b 보정).
- 검수: `_fu_uniq` 인덱스 대조로 누락/어긋남 확인(1134-53 구간 EN 미확인 기입분
  전량 재작성 — heredoc 확인 없이 찍어 쓰면 안 됨), 태그/개행 대조 0.
- 적용: 패치 884파일 + 중첩 GUI 포인터 9건 수동 병합(이전 배치와 동일 패턴),
  엔트리 61,919→62,804, 용어 QA 위반 0(46b: 팝톱·콰이어투스·텔레브리엄 18op).

## 2026-10-01 (3차): CAMPAIGN-45 — Arcana (contents_2359135864) 미번역 번역

SURVEY 실질 미번역 첫 번째(~860건 추정 → 추출 1,886행: 재사용 1,079 + 신규 807행/
유니크 694). `data/arcana_ko.tsv`에 유니크 인덱스→KO 맵 수동 작성 후 확장.

- 내용: 아머 세트명·설명(세트 보너스 ^orange;/^green;/^red; 구조 보존), 백 아이템,
  화장품 헤드(제작자 크레딧 `^orange;[이름]^reset;` 보존), 상태이상명, 증강(AMP·
  EPA·도금 열쇠·타로 카드), 플랫폼·바이옴 타일, UI 라벨, 식별자 스텁
  (`arcana_armor_ironFlower_head` 등 → 읽기 가능한 한국어명으로 번역).
- 시행착오: (1) 히어독 내 `'\\n'` 백슬래시 소실로 개행 이스케이프 무효화 →
  `scratch/_arcana_nl_fix.py`로 88필드 복구(교훈: 백슬래시 로직은 반드시
  스크립트 파일로). (2) 수동 인덱스 1칸 어긋남(458-460) → `_arcana_align_check`/
  `brand_check`로 발견·보정. (3) apply가 `doc.get(fld)` 상위필드만 처리해
  중첩 GUI 필드 5건 스킵 → 포인터 직접 지정 병합.
- 적용: 패치 895파일 + 중첩 5건, 엔트리 61,019→61,916(→45b-2 61,919),
  용어 QA 위반 0(45b: 로켓 발사기·면역·에르키우스 5op).
- 산출물: `data/arcana_work.tsv`, `data/arcana_ko.tsv`, `scratch/_arcana_*`.

## 2026-10-01 (2차): SURVEY — 전 모드 미번역 텍스트 전수조사

설치 pak 전부(816 프로바이더: mods/*.pak 705 + 언팩 디렉터리 11 + vanilla
packed.pak)를 대상으로 텍스트 자산 전수조사(`scratch/_all_coverage.py`).
판정: 자산의 `X.patch`가 3개 번역 pak(zz_translation_female,
zz_localeko_highpriority, -9998_trans_sbkor_structfix) 중 하나에 존재하는지 +
파일명 로드순 패치 체인을 실제 시뮬레이션.

- 텍스트 자산 60,532개 / 커버 46,403 / 미커버 12,453 / broken 1,676
- **broken 1,676 전량 오탐 확정** (`scratch/_broken_rescan.py`): 전 패치 체인
  적용 후 최종 텍스트가 전부 한국어 — 먼저 로드되는 다른 번역 pak(-9998 sbkor,
  zz_localeko)이 이미 같은 필드를 KO로 쓴 뒤 후속 번역 pak의 test(EN 기대)가
  실패하는 패턴. 실제 커버율 = 48,079/60,532 (79.4%).
- 미커버 12,453 중 dev/unused 경로 960 + 식별자 스텁 393 제외 시
  **실질 미번역 ≈ 11,100필드**. 산출: `data/coverage_survey.tsv`(전체 행),
  `data/coverage_survey_summary.txt`(프로바이더별), `data/coverage_broken_detail.tsv`.

실질 미번역 상위 제공자: Galaxy in Conflict 1,307(+dev/legacy 다수),
FrackinUniverse 888, lustbound_omnibrowser 880(몬스터걸 카드),
contents_2359135864=Arcana 860, Elithian 663, ffxiv_viera 444,
contents_2593214277=skpkmn 포켓몬 아머 444, contents_3117942107=GiC/ESC
확장 430, Saturnians 307, GIC_Otherworlds 300, packed.pak(바닐라, 대부분
unsorted/디버그 아이템) 248, Enternia 203, contents_2735634052=nuggubs 의상
161, contents_1356955138=Lucario 아머 152, RPG(ivrpg 직업) 183 등.

## 2026-10-01: LUSTLING-43/43b — 러슬링 modifyed 아머 미번역 전면 제거 (620자산)

사용자 보고 "lustling 종족 관련 미번역"을 계기로 전체 mods 디렉터리에서 `lustl`
경로 자산을 전수 스캔(`scratch/_lustl_coverage.py`). 러슬링 본체(997_sxb) 텍스트는
234/235 패치로 이미 번역 적용 가능했고, 미번역의 정체는
`items/armors/lustling/modifyed/` 아래 러슬링 전용으로 복사된 타 모드/바닐라 아머
변형 **640개 실자산**이었다.

- **43차 (재사용)**: `tools/fix_lustling_items_batch43.py` — 동일 베이스명 원본
  아이템의 기존 한국어를 test=변형 EN / replace=원본 KO 로 매칭, 276자산 적용
  (엔트리 59,519→59,795). `data/lustling_untranslated.tsv`로 잔여 목록 산출.
- **43b (신규 번역)**: 재사용 불가 344자산 688필드를 수동 번역
  (`data/lustling_batch43_ko.tsv`), `tools/apply_lustling_batch43b.py`로 적용
  (엔트리 59,795→60,139). test 값은 적용 시 라이브 자산에서 재독취해
  멀티라인 문자열 불일치 차단. 러슬링 티어 아머·코스모·나이트폴·레뎀션·USCM
  (범우주 우주 기업군)·아르카나 f-변형·ffs·kawaii·csbi·lastree·law·shellguard
  ·바닐라 로봇 모험가 전부 포함. 음성/태그(^green;^red;^#hex;)/줄바꿈 보존,
  `...res.`→`...저항`, `Dyeing possible`→`염색 가능`, floran `sss`→`쓰` 관례 적용.
- **43c (용어 보정)**: `tools/fix_lustling_glossary_batch43c.py` — 고정 용어 정합:
  `러슬링`→`러스틀링`(glossary 고정 표기), `바이올리움`→`바이올륨`, sbkor식
  `지식부`→`미니크녹`(pak 표준). ko.tsv 소스도 동일 보정해 재적용 대비.
- **검증**: 커버리지 재스캔 결과 미커버 실자산 640→**20**, 전부 비텍스트
  (particle/monsterpart/animation/blockkey.config 색상값/defaultParameters
  수치/defaultCategories 마커/lustlingnamegen 음절 규칙 — 타 종족 namegen도
  비번역 관례라 유지). 재추출 280,942쌍, 용어 QA **0위반**, pak 엔트리 60,139.

## 2026-09-29 (28차): fix_glossary_batch23 — energyFormat MJ 단위 누락 동일 버그 3건 추가 발견·수정

27차 sbkor 대조에서 발견한 `energyFormat` MJ 단위 누락 버그가 다른 자산에도 반복됐는지
확인하기 위해, 같은 벡터를 사용해 EN/KO 사이 단위 토큰(MJ·kg·%·HP 등)과 printf
포맷 지정자(%d/%s/%f 등)의 존재 여부를 pak_pairs.tsv 전체 186,213쌍(EN·KO 둘 다
있는 것만)에 대해 직접 대조했다. printf 지정자 불일치는 0건으로 안전 확인. 단위
불일치는 131건 나왔으나 대부분 "HP"가 한국어 조사와 붙어 `\b` 단어 경계 정규식이
놓치는 오탐(예: "HP를"), 또는 "HP"를 정상적으로 "체력"으로 의역한 경우였다. 이
노이즈를 걷어내고 남은 후보 중 진짜였던 것은 `/energyFormat` 자산 3건으로, 전부
26~27차와 동일한 "Energy: %d MJ" → "MJ" 누락 패턴이 각 파일에 독립적으로 반복돼
있었다:

- `/interface/scripted/sgspidermechstation/sgspidermechstation.config.patch`
- `/interface/scripted/xscm_config/_mechassemblygui.config.patch`
- `/interface/scripted/xscm_config/xscm_config_gui.config.patch`

전부 "에너지: %d" → "에너지: %d MJ"로 통일. `fix_glossary_batch23.py`, 백업
`mods/female_translation.pak.bak-20260929-prebatch23`, 변경 자산 3개 확인. 나머지
단위 불일치 후보(EPP 약어 유지, mm/kg 수치 표기, HP-조사 결합 오탐 등)는 육안 확인
결과 전부 정상 번역으로 확인, 추가 수정 없음.

## 2026-09-29 (27차): fix_glossary_batch22 — sbkor.tsv 대조 신규 기법으로 단위 표기 누락 1건 발견·수정

26차 구조 QA(색상 태그)에 이어, NonEKI 검수에서 효과를 본 "바닐라 sbkor.tsv 대조" 기법을
처음으로 메인 pak 전체(pak_pairs.tsv 326,000쌍)에 적용해봤다. EN 원문이 정확히 일치하는
행을 sbkor.tsv(23,746개 고유 EN)와 조인한 결과 640건이 한국어 번역이 서로 다르게
나왔으나, NonEKI와 달리 이 pak은 독자적으로 번역된 것이라 문체·어조 차이(반말/존댓말,
의역 방식)가 태반이었고 진짜 오류 신호가 아니었다(무작위 60건 육안 확인 결과 전부 정상
번역 차이). 노이즈를 줄이기 위해 EN에 단위/플레이스홀더 토큰(MJ, kg, %, HP 등)이 있는데
번역문에서 빠진 경우만 정규식으로 재필터해 1건으로 압축:

- `/interface/scripted/mechassembly/arcana_mechassemblygui.config.patch`
  `/energyFormat`: EN "Energy: %d MJ" → 기존 한국어 "에너지: %d"에서 "MJ" 단위가
  통째로 누락돼 있었음(같은 자산의 `/drainFormat`은 "사용량: %.02f MJ/s"로 MJ를 정상
  유지하고 있어 비일관성 확인). sbkor.tsv의 해당 값("에너지: %d MJ0")은 자체적으로
  "0" 오타가 있어 그대로 재사용하지 않고, 기존 pak 값에 " MJ"만 추가해 "에너지: %d MJ"로
  수정. `fix_glossary_batch22.py`, 백업 `mods/female_translation.pak.bak-20260929-
  prebatch22`, 변경 자산 1개 확인.

이 sbkor 대조 기법은 메인 pak 전체에서는 신호 대 잡음비가 낮음(640건 중 진짜 오류
1건, 0.16%)을 확인했으므로, 향후 전면 재적용보다는 이번처럼 정규식 등으로 후보를 좁힌
특정 QA 목적(단위·플레이스홀더 무결성 등)에 한해 보조적으로 쓰는 편이 효율적이다.

## 2026-09-29 (26차): fix_glossary_batch21 — 신규 구조 QA(색상 태그 대조)로 콘텐츠 불일치 1건 발견·수정

용어집 재스캔(25차)에 이어 `qa_pak_context.py`의 기존 카테고리(UNTRANSLATED/TRUNCATED/
DUP_PARTICLE/LITERAL/STYLE_MIX)를 재확인했으나 전부 확립된 오탐이거나(자연스러운 한국어
압축, 대괄호 UI 라벨의 의도적 번역 등) 후순위 카테고리(STYLE_MIX)였다. 대신 이번 세션에서
처음 시도하는 검증 방식으로 `^color;` 태그·`<Token>`·`[Bracket]`의 EN/KO 멀티셋 대조를
pak_pairs.tsv 279,703쌍 전체에 실행(`_qa_pak_structure.py`).

- 색상 태그 불일치 7,623건 중 7,608건은 EN test 값이 애초에 빈 문자열(해당 필드에 원래
  바닐라 영문이 없어 이 프로젝트가 새로 추가한 flavor 텍스트)이라 오탐. 실제 EN이 있는
  15건만 육안 대조.
- `<Token>` 불일치 392건은 전부 같은 빈-EN 패턴으로 오탐.
- `[Bracket]` 불일치 1,222건 중 EN이 있는 571건을 대문자 키워드 휴리스틱으로 재필터한
  52건도 전수 확인 — [NORMAL]/[GLORY]/[VERY HARD]/[ERROR]/[INTERACT TO PICK UP] 같은
  상태·UI 라벨은 원래부터 의도적으로 번역되는 것이 이 pak의 확립된 관례(대괄호 조작
  힌트 금지 규칙은 `[FIRE]`류 재매핑 가능한 조작 힌트에 한정)로 확인, 수정 없음.

**확정 오류 1건**: `/species/esc_realisticapex.species.patch` `/charCreationTooltip/
description` — 이 커스텀 종족(바닐라 에이펙스의 그래픽 리스킨)은 고유 영문 로어("A race
of highly intelligent primates. For millennia, the Apex were close to human in
appearance...")를 갖고 있으나, 한국어 값이 `/species/apex.species.patch`(영문 test가
애초에 빈 문자열이라 이 프로젝트가 자체 추가한 스탯 블록·소개문)의 값을 그대로 복사해
전혀 다른 내용("고도로 지능적인 영장류 종족입니다. 이 과학의 대가들은...")이 캐릭터 생성
화면에 노출되고 있었다. 실제 영문 고유 로어를 번역해 소개문만 교체(스탯 블록은 리스킨이
바닐라 에이펙스와 스탯을 공유하는 것으로 판단해 유지). 대조용 동일 문자열이 정확히 이
두 자산에만 존재함을 확인해 다른 종족에는 영향 없음. `fix_glossary_batch21.py`로 자산명
스코프 지정 적용(첫 실행 시 apex.species.patch까지 함께 바뀌는 것을 확인해 재수정 —
exact-value 매칭이 두 자산에서 우연히 동일했기 때문). 검증: JSON 파싱 정상, 변경 자산
1개(`esc_realisticapex.species.patch`)만 확인. 백업:
`mods/female_translation.pak.bak-20260929-prebatch21`.

## 2026-09-29 (25차): fix_glossary_batch20 — 재스캔 용어집 위반 37건 (29자산)

NonEKI 검수 직후 `extract_pak_pairs.py`/`qa_pak_glossary.py`를 현재 설치 pak(279,703쌍,
batch 34 배포 + 이번 세션 batch17~19 반영분)에 재실행해 신선한 기준선을 확인하던 중 발견.
위반 37건은 거의 전부 23차 커스텀 종족 `<raceid>Description` 캠페인(7,888종 신규 번역)
에서 나온 것으로, 그 배치가 매 항목마다 고정 용어집을 대조하지 않은 것으로 보인다.

**수정(용어집 고정 표기 기준)**: Hylotl 하일로틀→하이로틀(9), Crafting Station
작업대/제작 스테이션→제작대(5), United Systems 유나이티드 시스템즈→연합 시스템(5),
Grand Protector 그랜드 프로텍터→고위 수호자(4), Poptop 팝탑→팝톱(3), Miniknog
미니노그→미니크녹(2), Protectorate 프로텍토레이트→보호국(2), Cultivator
경작자→컬티베이터(2, 금지어 명시), Jorgasian 조르가시안→조가시안(2), Matter
Manipulator 매터 매니퓰레이터→물질 조작기(1), Shortsword 단검→소검(1, Dagger의
단검과 별도 구분 필요해 해당 1건만 스코프 지정 치환), Terrene Protectorate
테렌 보호국→행성 보호국(1).

**적용 방식**: `qa_pak_glossary_report.tsv`의 (asset, pointer) 37건에 대해
`pak_pairs.tsv`에서 전체 원문 그대로의 한국어 값을 가져와, exact-value 매칭으로만
치환(단어 전역 치환 아님) — Cultivator의 "경작자"·Shortsword의 "단검"처럼 다른 문맥에서
정당하게 쓰이는 일반 단어가 섞여 있어 전역 substring 치환은 위험했기 때문. 37개 치환
쌍 전량 needle-miss 0, JSON 파싱 전량 정상, 29자산 변경. 백업:
`mods/female_translation.pak.bak-20260929-prebatch20`. 재실행 결과 `qa_pak_glossary.py`
위반 0건으로 수렴.

## 2026-09-29 (NonEKI 별도 검수): 설치된 pak이 이미 번역돼 있음을 발견, 오역 17건 수정

README/batch_log에 여러 세션에 걸쳐 "NonEKI 전용 파이프라인(`repack_noneki_translation.py`)
미실행"으로 기록돼 있었으나, 실제 설치된 `mods/NonEKI_9_FU_compat.pak`을 직접 열어 대조한
결과 **이미 거의 전량 한국어로 번역돼 있음**을 확인했다(표시 가능한 문장 98개 중 93개가
한글 포함, 진짜 미번역은 JSON 설정 조각 5건뿐 — 실질 미번역 0). 과거 기록은 이 pak이
untranslated 상태였던 훨씬 이전 시점의 스냅샷이었던 것으로 보이며, 이후 어느 시점에
(세션 밖에서 또는 다른 경로로) 이미 번역이 적용된 것으로 추정된다. `repack_noneki_
translation.py`의 `SRC_PAK` 경로도 존재하지 않는 `E:\Desktop\...` 경로를 가리키고 있어
`mods/NonEKI_9_FU_compat.pak`으로 교정.

**QA 방법**: 표시 문자열 93건 전수 추출 후, `.patch` 자산은 중첩 test/replace 쌍에서, 없으면
원본 mod pak(FrackinUniverse/Saturnians/Felin/바닐라 packed.pak 등)에서 JSON 포인터로
패치 전 영문을 복원해 대조. 65/93건 영문 원문 확보(28건은 NonEKI 자체 신규 대사라 원본 부재
— 육안 검수만 진행, 자연스러움 이상 없음). sbkor.tsv(바닐라 기존 번역)와도 대조.

**확정 오류 17건 수정**: 함선 업그레이드 면허 퀘스트(`shipupgrade1~5`/`illegalshipupgrade1~5`.
questtemplate.patch) 9건과 미션 좌표 무전(`glitch_mission2`/`apex_mission2`/`hylotl_mission2`/
`floran_mission2`(2건)/`avian_mission2`.questtemplate.patch) 7건, `missioncultist1.aimission.
patch` 1건이 심하게 깨진 기계번역이었다(어순 붕괴, 조사 오류, `^green;...^reset;` 태그
안팎 구문이 뒤섞여 "...으로 설정합니다." 같은 의미 불명 잔여 문구가 반복 등장). 이 문자열은
전부 **바닐라 원문과 동일**해 sbkor.tsv에 이미 정평 난 고품질 번역이 존재함을 확인, sbkor의
번역을 그대로 재사용하되 이 프로젝트 용어집과 충돌하는 1건("지식부 요새"→"미니크녹 요새",
Miniknog Stronghold 고정 용어)만 치환해 적용. `noneki_sbkor_reuse.tsv`(17건)로 기록,
`_apply_noneki_sbkor_reuse.py`로 pak 직접 패치(flat/nested 패치 구조 모두 대응하는 op-level
치환, exact-value 검증 후 적용, 0 mismatch). 백업: `mods/NonEKI_9_FU_compat.pak.bak-20260929-
presbkorfix`.

**주의(오탐 방지 기록)**: AI 미션 종족별 대사(`missionavian1`/`missionglitch1`/`missionapex1`/
`missionfloran1`/`missionhylotl1`/`missionpenguin1`/`missionpenguin2`.aimission.patch)는
`op:test`에 `inverse:true`가 붙어 있어 test 값이 "이 값이 아닐 때만 적용"이라는 배제
조건이지 번역 대상 원문이 아니다. 이를 원문으로 오인해 대조하면 완전히 무관한 내용처럼
보여 오탐이 발생하므로, `inverse:true` test는 EN 소스로 신뢰하지 말 것.

**남은 76건**은 FrackinUniverse 채집물 설명·NonEKI 자체 튜토리얼 대사 등으로, 원문과 뜻이
어긋나지 않는 자연스러운 로컬라이즈(직역이 아닌 flavor 의역, NEKI 특유의 "냐옹~" 말투 포함)
로 확인돼 추가 수정 없이 종료. 상세 목록은 `noneki_needs_review.tsv`에 보관.

## 2026-09-29 (23차 자연스러움 정독 검수): 커스텀 종족 7,888종 전수 재검토, 36건 수정

- 용어 통일 자동 QA(`qa_glossary.py` 등) 완료 후에도 부자연스러운 문장이 남아있다는 지적에 따라,
  `customrace_unique.tsv` 기반 전체 7,888종을 986종씩 8개 청크로 나눠 fork 병렬 정독 리뷰를 수행
  (자동 휴리스틱이 아닌 사람 수준의 직역투/어순/조사/문체 판정 — [[qa-scale-fork-review]] 원칙 적용).
- 판정 기준: 원문이 함의하는 종족별 말투(사투리/파괴된 영어/로봇체/격식체 등)를 그대로 유지하되,
  ① 직역 콜로케이션 오류(예: "솜씨가 매혹적" → "솜씨가 감탄스러울 정도야"),
  ② 조사·어순 오류, ③ 영어 어순을 그대로 끌어온 부자연스러운 수식어 중첩,
  ④ 문체 이탈(주변이 전부 "~지/~네"체인데 홀로 "~다"체), ⑤ 실제 오역만 수정 대상으로 삼고
  의도된 사투리·파괴된 문법·거친 말투는 손대지 않음.
- 8개 청크에서 총 36건 수정(청크당 0.3~0.7%, 매우 낮은 결함률로 기존 번역 품질이 전반적으로
  양호했음을 확인): chunk_00 3건, 01 5건, 02 3건, 03 7건, 04 4건, 05 4건, 06 4건, 07 6건.
- 대표 사례: id 3619(`묶어두다`→`막아주다`, "가두다"와 "막다" 오역), id 4472(`압축된`→`콤팩트한`,
  compact 오역), id 4796/4797(수식어 중첩 어색함 + 기존 오탈자 "놀랽도록"→"놀랍도록" 동시 수정),
  id 5990(문체 이탈 "~한다"→"~하지" 통일), id 7579("Slot it all!" 오역 "다 걸렸네"→"젠장할!").
- 각 청크 산출물은 `qa_review/fixes_0N.tsv`(id/corrected_korean/note)로 남기고, 해당 id가 속한
  `translations/customrace_batch_*.tsv`에 일괄 반영.
- 재검증: `qa_customrace.py` 재실행 결과 `affected rows: 56 ([('possible-untranslated', 56)])`로
  batch_0058 완료 시점과 동일(신규 회귀 없음, 전부 기존에 확인된 오탐).
  `apply_customrace.py` 재적용 후 `extract_pak_pairs.py`로 전체 pak 재검증:
  `assets scanned: 59470`, `bad json: 0`, `pairs extracted: 279703`. pak 엔트리 59,499 → 59,519.
- 수정된 36건 중 표본 샘플(효율적이고 콤팩트한, 젠장할 등)을 `pak_pairs.tsv`에서 직접 grep으로
  대조해 실제 배포된 pak에 정확히 반영됐음을 확인.

## 2026-09-29 (23차 계속29, batch_0058): 7,888/7,888종 (100%) 완료 — 23차 캠페인 종료

- 마지막 잔여 207종(faahri 마무리, harpy, sith, skeleton, vampire, wookie, zabrak, diathim, radien, shadow,
  peglaci, woofie, elduukhar, nicemice, catus, slimenpc, slimenpchuman, nexusdroid, lamia, laustaur, nostos,
  ponex, utapaun, limako, nightar, bignorthdragnar/northdragnar, iodral, kemono, kitsune, ningen 및 1건씩만
  등장하는 약 20종의 단발성 종족)을 한 번에 덤프해 `customrace_batch_0058.tsv`(207행)로 번역.
- nicemice: 기존 확립된 z-말투("이거 냄새가 좀 이상하쥬." batch_0054/7779) 재사용 확인 후 전부 "~쥬" 종결어미로 통일.
- bignorthdragnar/northdragnar: w→v 치환 사투리(고대 영어식 산적 원정대 말투)를 "~구먼" 계열 한국어 사투리로 대응.
- laustaur: 남부 사투리(생략형 'ny, 'em)를 "~구먼" 계열로 대응.
- id 7874(faunodyne): 원문에 PUA(U+E000~U+E0FF) 아이콘 글리프 4개(``)가 텍스트 중간에
  삽입되어 있음을 QA의 `glyphs` 플래그로 발견. 번역문에도 동일한 글리프 시퀀스를 동일 개수로 삽입해 해결
  (`Do no harm, take no [아이콘].` → `해를 끼치지 말고, [아이콘]도 가져가지 말 것.`).
- id 7798(slimenpc): `<selfname>` 플레이스홀더로 인해 QA `possible-untranslated`가 베이스라인(55) 대비 +1(56)로
  올라감. 태그가 원문·번역문에 동일하게 보존되어 있음을 확인한 오탐이라 문제 없음.
- QA: `translated total: 7888`, `unknown ids: 0`, `affected rows: 56 ([('possible-untranslated', 56)])`.
- `apply_customrace.py` 적용 후 pak 엔트리 59,486 → 59,499(신규 자산 13개 반영, 터치 자산 4,892개).
- 23차 커스텀 종족 오브젝트 조사 설명문 캠페인(`customrace_unique.tsv` 고유 7,888종) 전수 번역 완료.

## 2026-09-29: Batch 34 deployment

- Promoted `female_translation.pak.REVIEW_PENDING` to `mods/female_translation.pak`.
- Saved the previous deployed pak as `female_translation.pak.bak-20260929-prebatch34`.
- Confirmed the deployed pak and reviewed pending pak have identical SHA-256:
  `458525ca71f41d73a65d5122721b302b88943e64c665a0e1b08901ff9b71b68b`.
- Re-extracted 186,163 translation pairs from 59,371 assets with zero JSON parse failures.
- Fixed-glossary QA reported zero violations across 200 fixed terms.
- OpenStarbound loaded all databases and started listening successfully with the deployed pak.
- The vanilla server's existing conditional-patch incompatibilities were reproduced with both the
  pre-deployment backup and reviewed pak; they are not a batch 34 regression.

## 2026-09-29 (batches 32-34): Particle, register, and loanword cleanup

- Corrected 53 particle errors adjacent to fixed glossary terms, including subject, object, topic,
  conjunction, and directional particles. A follow-up scan found zero remaining candidates for
  glossary terms.
- Corrected additional Floran register issues and source-content mismatches involving the Daitengu,
  Alta, Enviroprotector, and MEGA-TRINK descriptions.
- Documented `Trinkian` as a contextual adjective and normalized two confirmed spelling errors.
- Normalized `Figurine` to `피규어`, `판넬` to `패널`, and prohibited `포탈` spellings to `포털`.
- Pending pak validation remains at zero Python JSON parse failures and zero fixed-glossary
  violations. The deployed pak remains unchanged.

## 2026-09-29 (batches 29-31): World terms, repeated text, and formatting

- Normalized recurring Alta and Saturnian names after direct source-context comparison:
  `Enterash`, `Alterash`, `Solalei`, `Tonna`, `Tonnova`, `Tsay`, `Koywa`, `Faacain`,
  `Ceternia`, `Enterite`, `Alternia`, `Enternia`, and `Ceterai`.
- Distinguished `Elithian` (`엘리시안`) from the planet `Elithia` (`엘리시아`).
- Normalized Alta resource `Stardust` to `스타더스트` while preserving untranslated product and
  mod names such as `Stardust Core/Lite`.
- Corrected repeated lexical errors involving plant sprouts, buds, ionic sap, plant-based snow,
  Ember Coral, and In Jelly.
- Restored trailing runtime formatting spaces for four `%s` display format strings.
- Updated pak glossary QA to ignore glossary-like path segments inside HTTP URLs.
- Pending pak validation remains at zero Python JSON parse failures and zero fixed-glossary
  violations. The deployed pak remains unchanged.

## 2026-09-29 (batches 26-28): Consistency, register, and compact UI review

- Restored untranslated weapon model identifiers such as `T4`, `T11`, `T14`, `T22`, `T25`,
  `T30`, `T49`, and `T99` instead of localized `N식` forms.
- Corrected source-content mismatches involving Rhadeis, Ancient structures, Ancient ruins, and
  multiline GiC weapon descriptions. Restored meaningful paragraph and ability-line breaks.
- Corrected missing Glitch emotion separators and normalized confirmed Novakid, Floran, Moogle, and
  Neki register violations. Moogle `kupo` is now attached as a speech suffix rather than a detached
  interjection in the reviewed corpus.
- Corrected compact UI labels for three GIC:E stratagem cooldown effects.
- Refined ambiguous glossary entries (`Alliance`, `Old One`, `Trink`, `Spooked`, `The Ruined`, and
  `Union flag`) from unconditional fixed rules to documented contextual rules.
- Pending validation: 59,420 entries, 186,167 pairs, zero JSON parse failures, zero fixed-glossary
  violations, and zero compact UI-length candidates. The deployed pak remains unchanged.

## 2026-09-29 (batches 22-25): Pending pak re-review

- Created `female_translation.pak.REVIEW_PENDING` and stopped replacing the deployed pak during
  intermediate review batches.
- Corrected six `PIXELS AVAILABLE` labels that had inherited the unrelated materials-filter text.
  Reclassified `Materials Available` as a contextual glossary entry because `lblProduct` and
  `craftingMatAvailTxt` are headings, not filter controls.
- Normalized the Elithian proper organization `Alliance` to `얼라이언스` in twelve contextual
  occurrences and corrected `Jorgasian` to `조가시안`.
- Normalized 44 Eithne occurrences to `에이트네`, 95 `the Ancients` occurrences away from the raw
  transliteration, 136 Magicite occurrences to `마기사이트`, and remaining raw K'Rakoth spellings.
- Corrected repeated source-content mismatches in parasols, AI-chip mission text, Lucario mech body
  descriptions, Floran dialogue, Alta weapon descriptions, and two shield ability descriptions.
- Preserved runtime input tokens such as `[Special 1]`, `[Special 2]`, `[Special 3]`,
  `[Primary Fire]`, and `[Alt Fire]` rather than translating their contents.
- Improved pending-only QA arguments for `extract_pak_pairs.py`, `qa_pak_glossary.py`, and
  `qa_pak_context.py`. Current pending state: 59,420 entries, 186,167 extracted pairs, zero Python
  JSON parse failures, and 20 reviewed contextual false positives in fixed-term QA.

## 2026-09-29 (24차): 재검수 보류 2건·고정 용어 정리·JSON 패치 파싱 오류 수정

- `gic_militarytransport.object.patch`: 원본 `Galaxy_in_Conflict_contents_2754886445.pak`에서
  영문 필드 전부를 복원해 기존 추정 번역을 직접 대조했다. 바닐라 7종족 말투를 교정하고 공용
  description/shortdescription와 Avikan/Aegi 설명 누락도 test/replace 쌍으로 보완했다.
- `alta/wired/logic/latch.object.patch`: latch 원문에 다른 논리 장치의 Enable/Data 노드 설명이
  혼입된 3개 필드를 `전선 상태를 저장하는 래치`라는 실제 원문으로 복구했다.
- 고정 용어 재검수: 커스텀 종족 배치의 Aegi 35개 고유문장/162자산을 `에지`로 교정하고
  Union flag·Thelean·Saturnian도 정본으로 수정했다. Cultivator 2건은 `경작자`가 아니라
  `컬티베이터`, Terrene Protectorate는 `행성 보호국`으로 통일했다. Floran 내용 불일치 9건,
  제작대 3건, 뼈/가죽 세공대, Trink Circuit, GiC 무기 3개의 개행·`패링`·`한손`, 실제 신격을
  뜻하는 Old One 4건도 원문 대조 후 교정했다.
- `female_translation.pak` 적용 후 OpenStarbound 로그에서 JSON 패치 파싱 실패 3건
  (`RPGskillbook.activeitem.patch`, `perfectlygenericitem.object.patch`, `blindweed.item.patch`)을
  확인했다. 전체 55,789자산 평탄화 시험은 `/interface.config` 회귀를 일으켜 즉시 백업으로
  되돌렸고, 실패한 3개 자산의 과다 중첩 배열만 평탄화했다.
- 최종 검증: 활성 pak 59,420엔트리, `.patch` Python JSON 파싱 오류 0건. OpenStarbound가
  모든 데이터베이스를 로드하고 타이틀 월드까지 진입했으며 `female_translation` 파싱 오류 0건.
  생성 파이프라인은 중첩 조건부 그룹을 계속 보존하고, `extract_pak_pairs.py`만 임의 깊이 그룹을
  읽도록 보강했다.

## 2026-09-29 (23차 계속28, batch_0057): 7,681/7,888종 (97.4%) 완료

- batch_0057 (140건): fupeglaci 잔여분 완결(7건) + 다수 1회성/소량 종족 신규 착수 —
  fumantizi(24건, 퇴폐적 제국풍 "~야/~지/~군"), skath(50건, 자부심 강한 기술군체
  "~지/~야" — Vanguard→뱅가드, Impervium→임퍼비움, hydrolium→하이드롤륨, Norkumsgath→
  노르쿰스가스), fenerox(11건, 기존 확립 전보체 "명사. 명사. 짧은 문장!" 그대로 적용),
  thelusian/bothan/rodian/togruta/twilek/ithorian/mawg/moogle(쿠포 유지)/kirhos/faahri
  각 1~9건은 기존 문체 선례 확인 후 그대로 재사용하거나 원문 어조 직역 매칭. faahri→
  파흐리(신규 음역, "파리"와의 혼동 방지). QA 신규 flag 없음.
- pak 엔트리: 59,485 → 59,486.

## 2026-09-29 (23차 계속27, batch_0056): 7,541/7,888종 (95.6%) 완료

- batch_0056 (140건): satkyterran 잔여분 완결(12건) + angel 신규(ids 7214~7331, 90건,
  경건한 천사체 "~어/~지/~구나" 확립 — Cultivator→컬티베이터, Ruined→루인드,
  Archangel Xequeyzriel→대천사 제쿠에즈리엘, Halo→광륜 등 고유명사 신규 확정) + fupeglaci
  신규(ids 7334~7366, 32건, 담백한 기술 설명체 "~지/~야" — Peglaci→펠글라시, Peacekeeper→
  피스키퍼). QA 신규 flag 없음.
- pak 엔트리: 59,484 → 59,485.

## 2026-09-29 (23차 계속26, batch_0055): 7,401/7,888종 (93.8%) 완료

- batch_0055 (140건): fenron 계속(38건, "~군/~네/~지" 유지) + noolith 신규(ids 7055~7161,
  84건, 침착한 관찰형 "~군/~네" 톤) + satkyterran 신규(ids 7163~7196, 16건, 호기심 많은
  감탄체 "~네/~군/~지"). Relic Seeker 행성 등급명(흉포/초록/선홍/청록/황금/무시간/비전 등)
  batch_0054에서 확정한 표기를 그대로 재사용. QA 신규 flag 없음.
- pak 엔트리: 59,484(변동 없음).

## 2026-09-29 (23차 계속25, batch_0054): 7,261/7,888종 (92.0%) 완료

- batch_0054 (140건): saturn 계속(10건) + annelisk 계속(ids 6839~6944, 84건, 냉소적
  스캐빈저체 "~네/~야" 유지 — Relic Seeker 행성 태그라인 다수 포함, arcana 접두 행성
  등급명은 "선홍/흉포/작열/황폐/애욕/격동/질풍/초폭풍/청록/황금/무시간/비전" 등 형용사+행성
  조합으로 통일) + fenron 계속(ids 6947~7014, 46건, 거친 용병체 "~군/~네/~지" 유지).
  QA 신규 flag 없음.
- pak 엔트리: 59,484(변동 없음).

## 2026-09-29 (23차 계속24, batch_0053): 7,121/7,888종 (90.3%) 완료

- batch_0053 (140건): neki 잔여분 완결(ids 6564~6570, 성인용 섹스토이 오브젝트 설명 7건
  포함 — 원문 그대로 사실적으로 번역) + thelean(15건)·hyvon(2건) 계속 + viera 신규 착수
  (ids 6599~6736, 80건, FF14 감성 우아한 경어체 "~구나/~어/~네/~지" 기존 확립 문체 적용)
  + saturn 계속(35건). id 6783은 원문이 큰따옴표로 감싼 문답형 말장난("Mothematics"=
  math+moth)이 실제 개행 포함 멀티라인 필드라 한국어도 동일 구조로 재현하되, 말장난은
  "나방정식"(나방+방정식)으로 현지화. QA 신규 flag 없음.
- pak 엔트리: 59,483 → 59,484.

## 2026-09-29 (23차 계속23, batch_0052): 6,981/7,888종 (88.5%) 완료

- batch_0052 (140건): neki 전량(ids 6418~6563, nmm_* 모드 오브젝트 다수). 기존 "장난스러운
  고양이 밈체" 유지, "purr-" 말장난은 리듬만 살리고 직역하지 않음(예: Purrtector→수호냥,
  Manypurrlater→매터퍼퓰레이터, purrivate→은밀한). id 6430은 원문 자체에 실제 개행이
  포함된 멀티라인 필드(`"...\n..."` 형태로 customrace_unique.tsv에 저장)라, 번역도 동일하게
  따옴표+개행 포함 형태로 작성해 QA의 개행 개수 일치 검사를 통과시킴. QA 신규 flag 없음.
- pak 엔트리: 59,482 → 59,483.

## 2026-09-29 (23차 계속22, batch_0051): 6,841/7,888종 (86.7%) 완료

- batch_0051 (140건): slimeperson 계속(ids 6255~6399, 127건, nmm_* 모드 오브젝트 다수
  포함 — 캐주얼한 젊은 말투로 통일) + neki 재등장(ids 6404~6417, 13건). neki는
  batch_0017에서 확립한 "장난스러운 고양이 밈체(퍼(purr) 말장난은 리듬만 살리고 직역하지
  않음)" 그대로 적용. QA 신규 flag 없음.
- pak 엔트리: 59,480 → 59,482(neki 자산 신규 반영으로 소폭 증가).

## 2026-09-29 (23차 계속21, batch_0050): 6,701/7,888종 (85.0%) 완료

- batch_0050 (140건): draunaar 잔여분 완결(ids 6020~6178, 95건) + centens(13건)·
  dremeton(18건)·slimeperson(15건) 재등장. 4종 모두 착수 전 batch_0003~0006 grep으로
  기존 문체 확인 후 적용 — centens "오만한 고대 문명체 ~군", dremeton "온화한 ~네/~지",
  slimeperson "단순 유아어 반말". QA 신규 flag 없음.
- pak 엔트리: 59,480(변동 없음).

## 2026-09-29 (23차 계속20, batch_0049): 6,561/7,888종 (83.2%) 완료

- batch_0049 (140건): notix 잔여분 완결(ids 5789~5840, 27건) + draunaar 신규 착수
  (ids 5845~6019, 113건). 착수 전 batch_0003~0006을 grep으로 먼저 확인해 draunaar
  기존 문체("~네/~군/~지" 혼합, 호기심 많고 실용적인 어조)를 확인 후 그대로 적용 —
  문체 오류 재발 방지 절차 첫 적용. QA 신규 flag 없음.
- pak 엔트리: 59,480(변동 없음).

## 2026-09-29 (23차 문체 오류 수정): hymid/jorgasian/notix 약 645건 문체 전면 재작업

- **발견한 문제**: batch_0044~0048에서 hymid·jorgasian·notix 3개 종족을 "무선례" 신규
  종족으로 잘못 판단해 평서 반말체("~다")로 페르소나를 새로 확립했으나, 실제로는 이번
  23차 캠페인 초반 batch_0003~0006에서 이미 각 종족의 문체가 확정되어 있었음
  (hymid "~네/~지/~어" 온화한 반말체, jorgasian "~군/~네/~지" 관찰형 반말체, notix
  "~네/~지/~어" — 청각 묘사는 원래도 존재했음). batch_0015~0018 로그 기록을 놓치고 같은
  종족을 재확립한 것이 원인.
- **조치**: 사용자 확인 후 batch_0044(hymid 85건)·batch_0045(hymid 140건)·
  batch_0046(hymid 4건 + jorgasian 136건)·batch_0047(jorgasian 84건 + notix 56건)·
  batch_0048(notix 140건), 총 약 645건 전량을 기존 확정 문체로 재작성 후 재적용.
  draunaar는 아직 착수 전이었으므로 영향 없음 — batch_0049부터는 착수 전 반드시
  batch_0003~0006 등 초기 기록을 grep으로 먼저 확인하는 절차를 추가.
- QA: 5개 배치 모두 재검증, 신규 flag 없음(기존 possible-untranslated 55건 그대로).
- pak 엔트리: 5개 배치 재적용 전후 모두 59,480(변동 없음, 중복 적용 없이 정정 완료 확인).

## 2026-09-29 (23차 계속19, batch_0048): 6,421/7,888종 (81.4%) 완료

- batch_0048 (140건): notix 계속(ids 5569~5787). 청각 중심 페르소나 유지, 평서 반말체("~다").
  기존 표기 재사용: Hyverium→하이베리움, Vanguard→뱅가드, Drahl→드랄(구분 확인).
  신규 발견/정정: "Drehk"(아비칸 항공기)는 기존 선례가 "드렉"임을 batch_log에서 확인,
  초안의 "드레크"를 "드렉"으로 수정 후 적용(용어 오탐 방지 — Drahl/Krahl/Drehk 세 유사
  명칭이 서로 다른 유닛을 가리키므로 매번 구분 확인 필요). QA 신규 flag 없음.
- pak 엔트리: 59,480(변동 없음).

## 2026-09-29 (23차 계속18, batch_0047): 6,281/7,888종 (79.6%) 완료

- batch_0047 (140건): jorgasian 잔여분 완결(ids 5329~5477, 84건) + notix 신규 착수(ids
  5482~5568, 56건). jorgasian은 기존 평서 반말체("~다") 유지, 아비칸/센텐시안/트링키안 관련
  물건 다수(가구, 함선, 유물). notix는 원문이 청각에 특히 예민한 성격을 명확히 드러냄
  ("I can hear this screen buzzing lightly.", "I can almost hear the heat inside this fusion
  chamber." 등) — 평서 반말체("~다") 골격은 유지하되, 소리를 명시한 원문은 "~하는 소리가
  들린다"류 표현으로 청각 중심 페르소나를 신규 확립(무선례). 기존 표기 재사용: Covenant→
  코버넌트, Thelean→텔레안, Centens/Centensian→센텐스/센텐시안, Krahl→크랄(신규,
  아비칸 메크 명칭). QA 신규 flag 없음.
- pak 엔트리: 59,480(변동 없음).

## 2026-09-29 (23차 계속17, batch_0045~0046): 6,141/7,888종 (77.9%) 완료

- batch_0045 (140건): hymid 계속(ids 4896~5121). 평서 반말체("~다") 페르소나 유지, 물을
  좋아하는 온화한 성격 반영. "the Gods"(Ce'Tennan/센텐스를 가리키는 하이미드식 호칭)→
  신들(신규 확립, 무선례 — Elithian 계열 종족별로 센텐스를 부르는 명칭이 다르다는 세계관
  설정 반영). 기존 표기 재사용: Ce'Tennan→세테난, Hyzolia→하이졸리아, Veronas→베로나스,
  ASA→ASA(원어 유지).
- batch_0046 (140건): hymid 잔여분 완결(ids 5122~5126, 4건) + jorgasian 신규 착수(ids
  5134~5326, 136건). jorgasian(삼중 군주국 소속 종족)도 동일한 평서 반말체("~다")로
  신규 페르소나 확립. 기존 표기 재사용: Triple Monarchy→삼중 군주국, Bonecarver→뼈세공사
  (batch_0038에서 확립한 서술형 표기 재사용), Justicar→저스티카, Creon Embassy→크레온
  대사관, Hotbröd→핫브뢰드(모두 기존 확정 선례). QA 신규 flag 없음(누적
  possible-untranslated 55건 전부 기존 오탐 패턴).
- pak 엔트리: 두 배치 모두 59,480(변동 없음).

## 2026-09-29 (23차 계속16, batch_0043~0044): 5,861/7,888종 (74.3%) 완료

- batch_0043 (140건): trink 계속(ids 4444~4668). 신규 확립한 평서 반말체 + 효율성
  중심 톤 유지. "my Masters"(트링크의 창조 종족 지칭)→"내 주인들"(서술형, 무선례).
  기존 표기 재사용: Ce'Tennan→세테난, Centens→센텐스, Hyverium→하이베리움, ASA-26
  Ranger→ASA-26 레인저.
- batch_0044 (140건): trink 잔여분 완결(ids 4670~4758, 56건) + hymid 신규 착수(ids
  4760~4894, 84건). hymid(하이미드)도 동일한 평서 반말체("~다")로 신규 페르소나 확립 —
  물을 좋아하는 온화한 성격(원문 자체가 "I prefer staying wet" 등으로 이미 드러남).
  신규 음역(무선례): Hyki(하이미드 고향의 반려동물 종, Hymid 표기 규칙에 맞춰)→하이키.
  기존 표기 재사용: Hymid→하이미드, Dremeton→드레메톤, Notix→노틱스, Trangii→트랑기,
  Lyiin Atmaera→리인 아트마에라, Hotbröd→핫브뢰드(모두 기존 확정 선례). QA 신규 flag
  없음(누적 possible-untranslated 55건 전부 기존 오탐 패턴).
- pak 엔트리: 두 배치 모두 59,480(변동 없음).

## 2026-09-29 (23차 계속15, batch_0041~0042): 5,581/7,888종 (70.8%) 완료

- batch_0041 (140건): aegi 계속(ids 3993~4215). 평서 반말체("~다") 페르소나 유지. 신규
  음역(무선례): Faro(에너스 엔지니어링 차량 정비공 인명, "faro koywa" 기존 표기의 "파로"
  재사용)→파로, 해로잉(Harrowing, Starbound 커뮤니티 관용 표기)→해로잉. 기존 표기 재사용:
  Veronas→베로나스, ASA-26 Ranger→ASA-26 레인저(ASA 원어 유지), Gad'hur→가드후르,
  Centens→센텐스(모두 기존 확정 선례).
- batch_0042 (140건): aegi 잔여분 완결(ids 4216~4327, 59건) + trink 신규 착수(ids
  4329~4435, 81건). trink(트링크, 기계 종족)도 동일한 평서 반말체("~다") 페르소나로
  신규 확립 — 효율성에 집착하는 냉철한 분석 톤(원문 자체의 "efficient/inefficient" 반복
  판단이 자연히 어투를 형성). 신규 음역(무선례): Va'rahk(텔레안 정찰선급 함선명)→바락,
  Unified Alliance Crafting Station(일반 명칭)→통합 얼라이언스 제작대(서술형 번역).
  기존 표기 재사용: Circuit(Trink Circuit)→서킷, Vaash→바쉬, AAE(원어 유지), Enerth→
  에너스, Hotbröd→핫브뢰드, Lyiin Atmaera→리인 아트마에라, Creon Embassy→크레온 대사관
  (모두 기존 확정 선례). QA 신규 flag 없음(누적 possible-untranslated 55건 전부 기존
  오탐 패턴).
- pak 엔트리: 두 배치 모두 59,480(변동 없음).

## 2026-09-29 (23차 계속14, batch_0039~0040): 5,301/7,888종 (67.2%) 완료

- batch_0039 (140건): avikan 계속(ids 3564~3782). 평서 반말체("~다") 페르소나 유지. 신규
  확정(무선례, 문맥상 라데이스 전용 칭호로 판단): Uplifter(단수, 라데이스의 칭호)→격양자
  — 용어집의 "업리프터"(복수형, 무관한 타 종족 로어)와 구분해 재사용. 기존 표기 재사용:
  Old One(들)→옛 존재(Elithian/센텐시안 맥락 고정), Terve(단수형)→테르베, Vha'leihan→
  브할레이안, Vhelin(Era of)→벨린, Thell→텔, Watchers→감시자, Rhaiod→라이오드(모두 기존
  확정 선례).
- batch_0040 (140건): avikan 잔여분 완결(ids 3788~3869, 59건) + aegi 신규 착수(ids
  3871~3990, 81건). aegi(에지족)도 avikan과 동일한 평서 반말체("~다")로 신규 페르소나
  확립 — 온건한 기술 애호가 톤, 존댓말·애교체 배제. 신규 음역(무선례): Multi-Fabricator
  (기기명)→멀티 패브리케이터, hyverianite(하이베리움 계열 파생 자원, -ium/-ite 표기 규칙
  적용)→하이베리아나이트, Infospire(정보 표시 기기명)→인포스파이어. 기존 표기 재사용:
  Enerth Engineering→에너스 엔지니어링, Hydroverium→하이드로베리움, Hotbröd→핫브뢰드,
  AAE(원어 유지), Mehros Avan→메로스 아반, Aventor→아벤토르, Briggs Shipbuilding→브릭스
  조선, Froza→프로자, Allosteel→알로스틸, Lyiin Atmaera→리인 아트마에라, Creon Embassy→
  크레온 대사관(모두 기존 확정 선례). QA 신규 flag 없음(누적 possible-untranslated 55건
  전부 기존 오탐 패턴).
- pak 엔트리: batch_0039 59,480(변동 없음) → batch_0040 59,480(변동 없음).

## 2026-09-29 (23차 계속13, batch_0037~0038): 5,021/7,888종 (63.7%) 완료

- batch_0037 (140건): akkimari 계속(ids 3173~3360). 기존 피진 원칙(조사 생략+"명사-수식어"
  어순+반말 평서형+"아키"/"아키마리" 자기지칭) 유지. "god-thief/god-thieves"(Thelean
  경멸적 별칭)를 "신-창조자"(god-maker) 패턴에 맞춰 "신-도둑"으로 신규 확립(무선례).
  신규 음역: Chaseflight(차량명)→체이스플라이트. 기존 표기 재사용: SAIL(원어 유지),
  Hyverium→하이베리움, Kel'chis→켈치스, Justicar→저스티카.
- batch_0038 (140건): akkimari 잔여분 완결(ids 3361~3388, 24건) + avikan 신규 착수
  (ids 3391~3563, 116건). avikan은 이번에 처음 자체 시점(`avikanDescription`) 등장 —
  원문이 정상 문법의 1인칭 서술(유목 전사 문화, 사물에 대한 호기심·자부심)이라 무선례
  신규 페르소나로 평서 반말체("~다", "~겠다", "~인 것 같다") 채택, 존댓말·애교체 배제.
  신규 음역(무선례): Gad'hur(아비칸 씨족이 기르는 탈것용 동물)→가드후르, Bonecarvers
  (뼈 세공사 직업명, Boneworking Station 기존 표기에 맞춰 서술형으로)→뼈세공사. 기존
  표기 재사용: dunebuns→사구빵, Thell(아비칸의 적대 종족 약칭, Thelean과 별개 고정
  표기)→텔, Elithia→엘리시아, Nomada→노마다, Vanguard→뱅가드, Drahl→드랄, Sandstalker→
  샌드스토커(모두 기존 확정 선례). QA 신규 flag 없음(누적 possible-untranslated 55건
  전부 기존 오탐 패턴, SAIL 유지 포함).
- pak 엔트리: batch_0037 59,480(변동 없음) → batch_0038 59,480(변동 없음).

## 2026-09-29 (23차 계속12, batch_0035~0036): 4,741/7,888종 (60.1%) 완료

- batch_0035~0036 (280건): akkimari 계속(ids 2835~3172, alliance/avikan 오브젝트 위주).
  batch_0034에서 신규 확립한 피진 원칙 그대로 유지: 조사 생략 + "명사-수식어" 어순 유지
  (예: "무기-외계거", "드론-작은거") + 반말 평서형 어미("~함", "~됨", "~옴") + 자기 지칭
  "아키"(단수)/"아키마리"(복수·종족 전체). 신규 음역(무선례): Kelraaki(단체/인물명으로
  추정, 문맥 불명확)→켈라키. 기존 표기 재사용: Elithia→엘리시아, Nomada→노마다, Vanguard→
  뱅가드, Starfarer's Refuge→피난처-스타파러(자체 규칙에 맞춰 "명사-수식어" 어순 적용).
  QA 신규 flag 없음(누적 possible-untranslated 53건 전부 기존 오탐 패턴).
- pak 엔트리: 두 배치 모두 59,480(변동 없음). 신규 자산도 기존에 이미 다른 문자열로 손댄
  patch 그룹에 op만 추가됨.

## 2026-09-29 (23차 계속11, batch_0033~0034): 4,461/7,888종 (56.6%) 완료

- batch_0033 (140건): droden 신규 착수(ids 2368~2587, alliance/avikan 오브젝트 스캔 로그).
  droden은 기존 확정 선례대로 로봇/스캐너식 건조한 보고체("~감지", "~완료", "~불가")로
  일관 적용. 기존 표기 재사용: Elithian Alliance→엘리시안 얼라이언스, Aeginian Federal
  Union→에지족 연방 연합, Dremeton Union of Cities→드레메톤 도시 연합, Erixian Republic→
  에릭시안 공화국, Hymidian Republic of Hyzolia→하이졸리아 하이미드 공화국, Triple
  Monarchy→삼중 군주국, Notician Federation→노틱스 연방, Trink Circuit→트링크 서킷,
  Old One→옛 존재, Kadavan→카다반, Rhadeis→라데이스, Vanguard→뱅가드, Vas Vha'leih→
  바스 브할레이, Vha'leihan→브할레이안, Vhelin(Era of)→벨린, Nomada→노마다, Thelean→
  텔레안, Speakers→연사(모두 기존 확정 선례). 신규 음역(무선례): Skoff(아비칸 소형
  함선)→스코프, Sandstalker(모래 생물)→샌드스토커, Starsight Inn→스타사이트 여관.
  QA 신규 flag 없음(누적 possible-untranslated 53건 전부 기존 오탐 패턴).
- batch_0034 (140건): droden 잔여분 완결(ids 2588~2802, 118건) + akkimari 신규 착수
  (ids 2804~2831, 22건). droden 계속 보고체 유지, 신규 음역(무선례): Drehk(아비칸
  차량)→드렉(기존 다른 배치에서 이미 이 표기로 확정), Keff(아비칸 호버바이크)→케프,
  Odyin as-Rhadeis(무기 유통업자 인명)→오딘 아스라데이스, Creon Embassy→크레온 대사관,
  Thellhunter(고유 인물명)→텔헌터, Covenant(Akkimari 진영명, Akkimari Covenant로 추정)→
  코버넌트. akkimari는 이번에 처음 자체 시점(`akkimariDescription`) 등장 — 원문이 관사·
  조사 생략, "Akki"(자기 지칭, 글로서리에 이미 "아키"로 축약 확정) 및 "명사-수식어" 어순
  도치(예: "furnace-nuclear")를 쓰는 의도적 피진 영어. 대응 원칙(신규 확립, 무선례): 조사
  생략 + "명사-수식어" 어순 그대로 유지(예: "용광로-핵", "무기-새거") + 어미는 항상 반말
  평서형("~함", "~됨", "~옴") + 자기 지칭은 "아키"(단수)/"아키마리"(복수·종족 전체)로
  구분. QA 신규 flag 없음.
- 용어 수정: batch_0032 id 2240에서 "Protectorate"를 글로서리 확정 표기 "보호국" 대신
  "보호령"으로 오기했던 것을 발견해 수정 후 재적용(`apply_customrace.py`로 즉시 반영,
  pak 엔트리 수 변동 없이 정정됨).
- pak 엔트리: batch_0033 59,480(변동 없음) → batch_0034 59,480(변동 없음). 신규 자산도
  대부분 기존에 이미 다른 문자열로 손댄 patch 그룹에 op만 추가됨.

## 2026-09-29 (23차 계속10, batch_0031~0032): 4,181/7,888종 (53.0%) 완료

- batch_0031 (140건): neko 계속(ids 2040~2207, 오브젝트 설명 위주). 기존 "냥" 말투/캐주얼
  반말 유지. 신규 고유명사 없음(가구·가전·게임기 등 일반 오브젝트 설명).
- batch_0032 (140건): neko 잔여분 완결(ids 2208~2329, 122건) + droden 신규 착수(ids
  2332~2366, 18건). droden은 Elithian 계열 종족으로, 용어집에 이미 "Droden→드로덴,
  전용 규칙 없어 기본 보고체" 확정 선례가 있어 로봇/스캐너식 건조한 보고체("~감지",
  "~완료", "~불가")로 일관 적용. 신규 고유명사: Arbiter(드론 모델)→아비터, Flic(드론
  모델)→플릭(둘 다 무선례 신규 음역). 기존 표기 재사용: Akkimari→아키마리, Vaash→바쉬,
  Justicar→저스티카, Thelean→텔레안, Nomada→노마다(모두 translation_glossary.tsv 확정
  선례).
- QA: 구조 오류 0건. 신규 flag는 2312(게임 내 의도적 키보드 매싱 무의미 문자열 원어 유지),
  2318(NASA 약어 유지)뿐, 기존 오탐 패턴과 동일하여 실제 미번역 없음.
- pak 엔트리: batch_0031 59,480(변동 없음) → batch_0032 59,480(변동 없음). 신규 자산은
  전부 기존에 이미 다른 문자열로 손댄 patch 그룹에 op만 추가됨.

## 2026-09-29 (23차 계속9, batch_0030): 3,901/7,888종 (49.5%) 완료

- batch_0030 (140건): felin 잔여분 완결(felin 오브젝트/NPC 포스터·그래피티 다수, 107건) +
  neko 신규 착수(33건). felin NPC/고유명사: Chelsie→첼시, Talos→탈로스, Firrhna→피르나(모두
  기존 표기), Jalmine→잘민, Lirith→리리스, Frisky→프리스키, Laenathin→레나신, Anerae→아네라이,
  Lenirthi→레니르시, Shema→셰마, Aelir→아엘리르, Mio→미오, Wildcats→와일드캣츠, Eron→에론,
  Femine→페민(모두 무선례 신규 음역). neko는 기존에 확립된 "냥" 말투 그대로 재사용. 영어
  말장난(COCK...PIT 조종석 개그)은 원어 병기로 유지.
- QA: 구조 오류 0건. 신규 flag는 1996/1997(의도적 영어 병기)뿐, 실제 미번역 없음.
- pak 엔트리: 59,480 (변동 없음).
- 누적 진행률 49.5%로 전체 작업의 절반에 근접.

## 2026-09-29 (23차 계속8, batch_0029): 3,761/7,888종 (47.7%) 완료

- batch_0029 (140건): felin 전량 계속. 검열된 원문("[expletive]", "F°ck")은 이전 배치와 동일하게
  "[욕설]"/"씨X" 표기로 통일. 자잘한 밈·언어유희(rhyme, "shi-sit" 자체 정정 개그 등)는 한국어
  구어체로 자연스럽게 재구성.
- QA: 구조 오류 0건. 신규 flag는 1823(USCM 약어 포함, 기존 색상 태그류와 동일한 벤치마크
  오탐 패턴) 1건뿐, 실제 미번역 없음.
- pak 엔트리: 59,480 (변동 없음).

## 2026-09-29 (23차 계속7, batch_0028): 3,621/7,888종 (45.9%) 완료

- batch_0028 (140건): felin 전량 계속. 오브젝트 조사 대사 특유의 짧고 시크한 반말체 유지,
  인터넷 밈·언어유희(rhyme 패턴, "Woodn't you like to know" 말장난 등)는 자연스러운 한국어
  구어체 반말로 의역. 검열된 비속어("f°ck")는 "씨X" 표기로 원문의 검열 뉘앙스 보존.
- QA: 구조 오류 0건. 신규 flag 없음(기존 배치의 색상 태그 오탐만 잔존).
- pak 엔트리: 59,480 (변동 없음 — 이번 배치는 신규 자산 없이 기존 항목 보정 위주).

## 2026-09-29 (23차 계속6, batch_0027): 3,481/7,888종 (44.1%) 완료

- batch_0027 (140건): alta 잔여분(91건) 완료 + felin 신규 착수(49건). alta 신규 고유명사:
  nioxu→니옥수(기존 표기), vionia→비오니아(기존 표기), neiteru-1→네이테루-1, yaarizza→야리짜,
  diva→디바, chakram→차크람. felin은 이전 배치에서 확립된 톤(당당·시크한 반말, "캣닢"=catnip,
  "~네/~지/~어") 그대로 재사용 — "If I fits, I sits" 같은 인터넷 밈 대사는 "들어가면, 앉는다"로
  자연스럽게 의역.
- QA: 구조 오류 0건. possible-untranslated는 색상 태그(1412/1422/1426/1441/1444/1446/1454/
  1461/1462) 포함 기존 유형의 벤치마크 오탐이며, 전수 대조 결과 실제 미번역 없음.
- pak 엔트리: 59,477 → 59,480.

## 2026-09-29 (23차 계속5, batch_0026): 3,341/7,888종 (42.4%) 완료

- batch_0026 (140건): alta 전량 계속. 신규 고유명사: scava/scavas→스카바(기존 표기 재사용),
  bionium→바이오늄, Protea→프로테아, Erenai→에레나이, izolings→이졸링, phosphobulb→포스포벌브,
  ennia→에니아(기존 enia/에니아 계열 재사용), gil→길(기존 "ayas/gils" 선례), orbide→오르바이드,
  kuda→쿠다. Ghearun(게아룬)·Celestia(셀레스티아)·Erchius(에르키우스) 등 기존 표기 재사용.
- QA: 구조 오류 0건. possible-untranslated는 색상 태그(1244/1246/1247/1249) + 기존 다건의
  동일 유형 벤치마크 오탐이며, 전수 대조 결과 실제 미번역 없음.
- pak 엔트리: 59,473 → 59,477.

## 2026-09-29 (23차 계속4, batch_0024~0025): 3,201/7,888종 (40.6%) 완료

- batch_0024~0025 (280건): alta 전량 계속. 신규 고유명사: Elu'nya→엘루냐, bobfae→봅페이,
  gheacal→기칼, ceterfaa→세터파, Yonnur→요누르(기존 "요누르" 재사용), Tiana→티아나,
  Erchius→에르키우스(글로서리 fixed), crustoise→크러스토이즈, Hevikai→헤비카(기존 표기,
  "헤비카병"으로 문맥상 풀어씀), Unika→유니카, hevikal/altecal→헤비칼/알테칼(신규 대응쌍),
  niaton→니아톤, alterfaa→알터파, juviley→주빌리, haruplavu/venetto/ometonna/fivaldo/rimar
  등 무선례 음식명은 발음대로 신규 음역. 셀레스티아·오키드·세테라이 등 기존 인물/세력 표기는
  전량 재사용.
- QA: 구조 오류 0건. possible-untranslated는 색상 태그(944/962/976/992/1018/1079/1131/1199/
  1216)와 기존 4건의 동일 유형 벤치마크 오탐으로, 전수 대조 결과 실제 미번역 없음.
- pak 엔트리: 59,466 → 59,472(0024) → 59,473(0025).

## 2026-09-29 (23차 계속3, batch_0022~0023): 2,921/7,888종 (37.0%) 완료

- batch_0022~0023 (280건): alta 전량 계속. 신규 고유명사 다수를 기존 TM/용어집 표기로 통일 —
  Narfin→나르핀, virma→비르마, izopoi→이조포이, viona→비오나, Faradea→파라데아,
  gheatorn→게아토른, Agaranic→아가라닉, bionid→바이오니드, Tsay→차이(글로서리 fixed),
  Hevika Ordis→헤비카 오르디스, yaarings→야라열매, GSR 포드, NG5/G2 인증, alunika→알루니카,
  nivera sentia→니베라 센티아, tavriya→타브리야, Esetera→에세테라, Neiteru→네이테루,
  Ghearun→게아룬(batch_0022 최초 작성 시 "기어룬"으로 오기해 재적용 시 교정), 니아→니아(잼 표기
  선례 재사용), coroplic→코로플릭, phospholion→포스포리온, vionora→비오노라. 나머지 신규
  무선례 고유명사(felistraza/phosnail/starfly/bionfly/ela/vyralic/azura/livira/gharus/yaavis/
  yaakut/frinsh/maito·maitorish/gheamont/Cagorta/strizych/oculemon/yaarut/snowalta/dreamers/
  kaiters 등)는 원문 발음을 그대로 음역해 alta 특유의 경쾌·호기심 많은 반말체 톤으로 신규 결정.
- 색상 태그(^#...;...^reset;) 포함 항목은 번역어에 맞춰 태그 위치를 재배치 — 655/671/710/712/
  734/739/751/777(batch_0022), 797/810/824/825/829/882/905/935(batch_0023) 전부 확인 후 통과.
- QA: 구조 오류 0건. possible-untranslated는 태그 내 'reset' 토큰 및 쉼표 포함 원문에서 발생하는
  동일 유형의 벤치마크 오탐(기존 4건 + 신규 다수)이며, 전수 원문 대조로 실제 미번역 없음을 확인.
- pak 엔트리: 59,460 → 59,463(0022) → 59,466(0023, ghearun 교정 재적용 포함).

## 2026-09-29 (23차 계속2, batch_0019~0021): 2,641/7,888종 (33.5%) 완료

- batch_0019 (130건): zabrak/diathim/penguin/peglaci/woofie/elduukhar/nicemice/beldehor/cat/
  nexusdroid/erixian/kineptic/utapaun/nightar(count=2 구간 소량 다종족) + avali(count=1) 신규 착수.
  nicemice는 기존 TM 관행("Ziz vall zmellz ztrange." 류 z-화자 대사를 '쥬' 어미로 재현)을 그대로
  적용. cat 종족은 "mew/meow" 원문을 반영해 "냥/야옹" 말투로 통일. avali는 batch_0002에서 확립된
  "해체 반말, 솔직·장난스러움"(~네/~지/~야/~군) 문체를 그대로 이어감.
- batch_0020 (140건): avali 잔여(약 100건) + alta 신규 착수(10건). avali 문체 유지. alta는 기존
  TM 예문(경쾌하고 호기심 많은 반말, "~어!/~네/~지/~야!~") 대조 후 동일 톤 적용.
- batch_0021 (140건): alta 전량. 고유명사는 기존 용어집·TM 표기를 그대로 사용 — Koywa→코이와,
  Alterash→알테라시, Enterite→엔테라이트, Ceterai→세테라이, Tserera→체레라, gheatsyn→기트신,
  Alternia→알테르니아(글로서리 fixed), 그 외 Yaara→야라, Bishyn→비신, Nivera→니베라,
  Isoslime→이소슬라임, Calin→칼린, Klee→클리, Hevika→헤비카, Sonaveil→소나베일, Io→이오,
  drei→드라이, dron→드론(개인 드론) 등 batch_log 기존 표기 재확인 후 적용. 색상 태그
  (^#20f080;/^#b0e0fc;/^#3587ff;)가 포함된 5개 항목(529/539/570/585/589)은 1차 QA에서
  tags 불일치로 걸려 태그 위치를 한국어 번역어에 맞춰 재배치 후 재검증, 통과.
- QA: 매 배치 구조 오류 0건. possible-untranslated는 기존 4건(511/1154/3770/4224, 짧은 문장
  휴리스틱 오탐) + 이번 회차 신규 5건(387, 529/539/570/585/589) 모두 태그·쉼표로 인한 동일 유형의
  벤치마크 오탐으로, 원문 대조 결과 실제 미번역 없음을 확인.
- pak 엔트리: 59,420 → 59,437(0019) → 59,453(0020) → 59,460(0021).

## 2026-09-29 (23차 계속, batch_0015~0018): 2,221/7,888종 (28.2%) 완료

- batch_0015 (130건): hymid·jorgasian 최상위 빈도 원문. hymid는 "~네/~지" 온화한 반말체,
  jorgasian은 "~군" 관찰형 반말체로 구분.
- batch_0016 (130건): jorgasian 잔여 + notix·draunaar 신규. notix·draunaar 모두 "~네/~지" 계열.
- batch_0017 (130건): draunaar 잔여 + centens(오만한 고대 문명체 "~군"), dremeton("~네"),
  slimeperson(단순 유아어 반말), neki(장난스러운 고양이 밈체 — "I fits and I sleeps"→"들어가면 잔다"
  식으로 리듬만 살림), thelean(과묵하고 어두운 전사체), hyvon(오만한 경멸체 "~라. 흥."),
  viera(FF14 감성의 우아한 존대 섞인 경어체, "숲(the Wood)" 신앙 반영), saturn(캐주얼한 마법사체)
  최초 등장 및 문체 확정.
- batch_0018 (130건): saturn 잔여 + 이후 대량의 1회성 종족(annelisk 냉소적 스캐빈저체,
  fenron 거친 용병체 "~군", noolith 엄숙한 경어체, satkyterran 호기심 많은 감탄체, angel 경건한
  천사체, fupeglaci/fumantizi/skath/fukirhos/fenerox(전보체 "완벽한 기계. 불완전한 음악." 식
  끊어치기)/thelusian/bothan/rodian/togruta/mawg/moogle(쿠뽀 유지)/twilek/ithorian/kirhos(사이버펑크
  속어체)/wookie 각 1회 등장 — 종족별 고유 문체 확립 기준 없이 원문 어조를 그대로 직역해 매칭.
- QA: 매 배치 `qa_customrace.py` 실행, `possible-untranslated` 4건은 batch_0006/0010/0013에서
  기록된 기존 오탐(단문이라 휴리스틱이 오검출)으로 확인, 신규 배치와 무관.
- pak 반영: `mods/female_translation.pak` 엔트리 수 59,416 → 59,420 (신규 asset 3,168개 patch
  파일 생성/갱신 누적).

## 2026-09-29 (23차): 커스텀 종족 자기소개 조사 대사(`<raceid>Description`) 미번역 발견 및 신규 캠페인 시작

**발견 경위**: 사용자가 "게임 내에서 미번역 문자열이 나온다, Lustling 오브젝트 조사 대사가 예"라고
지적. `mods/997_sxb_Lustlings_..._clean.pak`의 `duodildo.object`를 직접 까보니 바닐라 7종족
(`apexDescription` 등)은 번역돼 있는데 러스틀링 자신이 조사할 때 뜨는 `lustlingDescription`은
원문 그대로였음.

**근본 원인**: `scan_remaining.py`의 `VISIBLE_KEYS`가 바닐라 7종족 키만 인식하고, 커스텀 종족
모드가 자기 종족용으로 추가하는 `<커스텀종족id>Description` 키는 애초에 스캔 대상에 포함된 적이
없었다. 즉 `rest_worklist.tsv` 기반 QA(고/저우선 0/0)는 이 카테고리에 대해 완전히 사각지대였음.

**규모 측정** (`scan_custom_race_desc.py`/`scan_custom_race_desc2.py`, mods 전체 803개 pak 스캔):
`.object`/`.item`/`.liquid`/`.matitem`/`.consumable`/`.activeitem` 40,088개 자산에서
`<raceid>Description` 필드 17,575건 발견, **전부 0% 번역** (이미 번역된 바닐라 설명과 원문이
겹치는 "공짜" 재사용 케이스도 0건 — 커스텀 종족 대사는 전부 그 종족 전용 신규 문장). 고유 원문
7,888종. 종족별 상위: avali 1,434 / alta 1,396 / felin 1,273 / neko 1,006 / droden 958 /
akkimari 869 / avikan 847 / aegi 799 / trink 796 / hymid·notix·jorgasian 각 686 / draunaar 671 /
centens·dremeton 각 659 / slimeperson 632 / lustling 22 등 약 90여 종족, 50개 pak.

**파이프라인 구축**: 기존 `rest_worklist.tsv`/`dump_priority.py` 체계와 독립된 ID 공간으로
`translations/customrace_unique.tsv`(원문 중복 제거 7,888행, 최초 정렬은 종족 규모 내림차순)를
신설. `dump_customrace.py`는 완료분(`translations/customrace_batch_*.tsv`)을 제외한 나머지를
**출현 빈도(count) 내림차순**으로 낸다 — 여러 자산에 재사용되는 원문(예: 범용 placeholder
"I think I'm meant to say something here." 673회 재사용)을 먼저 처리해 적은 번역량으로 최대
실적용 범위를 확보하기 위함. `apply_customrace.py`는 원문 자산의 `.patch`에 `[test,replace]` 그룹을
추가/치환(정정 시 기존 그룹 자동 교체)하고 `pak_writer.py`(신규, `build_pak.py`의 SBAsset6 이진
포맷 로직 재사용 — 기존 pak을 통째로 복제하며 대상 파일만 교체)로 `mods/female_translation.pak`을
직접 갱신한다. `qa_customrace.py`로 태그/줄바꿈/입력토큰/플레이스홀더 구조 검사.

**1~2차 배치 완료** (161개 원문, 실적용 943 op-group):
- batch_0001 (21건): Lustling 전종 — 사용자가 지적한 `duodildo.object`의
  `lustlingDescription` 포함, 완곡화 없이 원문 그대로 직역(용어집 문체 규칙 준수).
- batch_0002 (120건): Avali 최상위 빈도 원문. 글로서리 159행의 아발리 문체(해체 반말, 솔직·장난스러움)
  적용.

**QA 이슈 발견 및 수정**: batch_0002 id 105 "Grand Protector"를 `term.py` TM 조회 결과(`대보호자`)로
번역했으나, 사용자가 "용어집에 고위 수호자 아니었나" 지적 — `translation_glossary.tsv`를 직접
확인하니 10차에서 이미 `대보호자→고위 수호자`로 확정된 상태였고 `term.py`가 참조하는 TM 데이터가
그 갱신 이전 스냅샷이라 낡은 값을 반환한 것으로 확인. **교훈**: 이 캠페인처럼 최근 확정 용어가
있는 항목은 `term.py` 결과만 믿지 말고 `translation_glossary.tsv`의 `fixed` 행을 직접 grep해서
대조할 것. `apply_customrace.py`는 이미 적용된 번역도 배치 파일 값이 바뀌면 자동으로 교체하도록
구현되어 있어 정정 후 재실행만으로 pak에 반영됨.

**진행 현황(23차 종료 시점)**: batch_0001~0005, 531/7,888종 번역 완료(6.7%),
7,776/17,575행 실적용(44.3% — 고빈도 우선 정렬 덕분에 원문 종수 대비 실적용 비율이 훨씬 높음).
Elithian 계열(akkimari/avikan/aegi/trink/hymid/notix/jorgasian/draunaar/centens/dremeton)은
같은 공용 오브젝트(비콘·함장석·인터페이스·발전기 등)를 여러 종족이 각자 성격대로 조사하는
구조라 자산당 번역 효율이 특히 높음 — 드로덴은 로봇식 "분석/감지됨" 존댓 없는 기계체,
아키마리는 3인칭 파닌어투("아키 ~한다"), 나머지는 각자 personality 있는 1인칭 반말로 번역.
남은 7,357종은 계속 배치로 진행 — avali/alta/felin/neko 잔여 후 그 다음 빈도 구간 순.

**참고**: `translation_memory.tsv`/`term.py`가 참조하는 `alignment/fu.tsv`·`sbkor.tsv`에서
이 커스텀 종족 원문 7,888종 중 528종(6.7%)이 이미 FU_KO 정렬 데이터에 존재함을 확인했으나,
FU_KO는 문체 기준이 아니라 용어 기준일 뿐이고(README 124행 규칙3) 실측 결과 전부 합니다체
존댓말로 번역돼 있어(이 캠페인이 목표로 하는 반말/종족별 personality와 불일치) **그대로
가져다 쓰지 않고 전부 수동 번역했다**. 오탐 방지용 기록.

## 2026-09-29 (23차 계속): batch_0012~0013 — 1,571/7,888종(19.9%), 10,578/17,575행(60.2%)

아키마리 3인칭 파닌어투("아키 ~한다"), 아비칸/아에기 1인칭 반말 조사 대사를 Elithian 계열
공용 오브젝트(작업대/화로/텔레포터/깃발/경작물/조명 등) 전반에 걸쳐 계속 처리. QA 이슈 없음
(possible-untranslated 플래그 4건 모두 고유명사/약어 오탐, `qa_customrace_all.tsv`로 확인).

## 2026-09-29 (23차 계속): batch_0010~0011 — 1,311/7,888종(16.6%), 10,058/17,575행(57.2%)

avali/alta/felin/neko의 count=2~4 구간 대량 처리 후 드로덴 로봇식 "감지됨/분석." 계열이 다시
큰 비중을 차지하기 시작. QA 이슈 없음(옥색 헥스코드 `^#b0e0fc;` 등 색상 태그 오탐만 3건).
계속 진행 예정 — 남은 6,577종.

## 2026-09-29 (23차 계속): batch_0008~0009 — 1,051/7,888종(13.3%), 9,538/17,575행(54.3%)

Elithian 계열 공용 오브젝트(가죽/항아리/사물함/안테나/텔레포터/추진기 등)의 아키마리~드레메톤
personality 조사 대사를 계속 처리. Mantizi2/impjar·imppot·imppitcher·impbowl 계열(Star Wars
종족 다수: bothan/togruta/mawg/twilek/wookie/zabrak/tuskan/diathim/sith/beldehor 등)도 착수.
QA 이슈 없음(affected rows 0~1, 유일한 flag는 고유명사/약어 오탐).

## 2026-09-29 (23차 계속): batch_0006~0007 — 791/7,888종(10.0%), 8,762/17,575행(49.9%)

Elithian 계열 대형 공용 오브젝트(비콘/함장석/도킹필드/인터페이스/연료 해치 등, 아키마리~드레메톤
10종족이 동일 자산을 각자 personality로 조사)와 avali/alta/felin/neko/droden의 다음 빈도 구간을
계속 처리. 드로덴은 일관되게 "감지됨/분석." 기계식 명사형 종결, 아키마리는 "아키 ~한다" 3인칭
파닌어투 유지. 새 QA 이슈 없음(`qa_customrace.py` affected rows 0~1, 유일한 flag는 SAIL 등
의도적 영문 약어 오탐).

## 2026-09-28 (22차): fix_glossary_batch19 — 글리치·노바키드 조사 대사 존댓말 정규화 (1,667자산)

20~21차에서 발견한 체계적 패턴(글리치/노바키드 조사 대사에 해요체/합쇼체 존댓말이 광범위하게
섞임)을 해결. `mods/female_translation.pak.bak-20260928-prebatch19` 백업 후
`female_translation.pak.NEW23` 적용.

**스캔**: pak 전체 glitchdescription/novakiddescription 필드 13,567개를 정규식 휴리스틱
(어미 -요/-죠/-니다/-세요/-나요/-가요/-군요 등)으로 재스캔 → 글리치 1,034행·노바키드 592행
플래그(총 1,626행). 각 행을 영문 원문과 페어링(중첩 test/replace 또는, flat 패치는 원본
mod/바닐라 pak에서 JSON 포인터로 패치 전 값을 복원해 페어링 — 1,607/1,626행 성공).

**재작성**: glitch_rewrite_1~3.tsv(345/345/344행)·novakid_rewrite_1~2.tsv(296/296행)로
분할해 fork 5개에 각각 위임. 각 fork가 STARBOUND_KO_GLOSSARY.md 규칙("감정어. 본문" —
감정어는 명사 1단어, 본문은 `-다`체 또는 반말 / 노바키드는 `~구만`·`~군`·`~겠어` 계열
반말)에 맞춰 영문 원문 의미를 보존하며 문법적으로 재작성(단순 어미 치환이 아니라 활용형
교정). 1,626행 중 15행은 실제로는 규정 준수 상태였던 오탐으로 확인(예: "...아니다."가
"니다" 부분 문자열에 걸린 것) — 원문 유지. 나머지 1,611행 재작성.

**감정어 접두사 정규화도 동시 진행**: 본문뿐 아니라 접두사 자체가 형용사형이거나 어색한
음역인 경우도 명사형으로 교체(예: "아주 기뻐하는."→"기쁨.", "스머그."→"거만."/"거만함.",
"관찰 결과."→"관찰.", "분석 중."→"분석.", "진술서."→"진술.", "멜랑콜리."→"우울."/"향수.").
"당황. 할 말이 없습니다!"(약 470여 자산 공유) · "호기심. 작은 동물입니다."(critter 태그
~90여 자산 공유) 등 소수의 고빈도 문구가 수백 개 자산에 반복 사용되는 구조라, 실제 고유
문장 수는 수백 종이었지만 적용 자산 수는 1,667건으로 크게 늘어남.

**중복/충돌 처리**: 동일 원문 문자열이 청크 분할 과정에서 서로 다른 fork에 배정된 17건은
양쪽 다 문법적으로 타당한 재작성이라 먼저 처리한 fork의 표현을 정본으로 채택(`_consolidate_
rewrite.py`).

**부수 오역 수정**: `fu_vieraftldrivemk1a/2a/3a`의 "faster'n 'light drive"(초광속 드라이브의
방언 표기)가 "가벼운 드라이브"로 오역(light를 무게로 오인)돼 있던 것을 재작성 과정에서
발견해 "초광속 드라이브"로 동시 수정.

**미해결 후속 과제(이번 배치 미포함)**: fork가 재작성 중 발견한 별개 문제 2건 — ①
`/objects/STATIC_VEHICLES/gic_militarytransport/gic_militarytransport.object.patch`는
base_pak에서 영문 원문 복원 실패(추정 문맥으로만 어미 교정), 원문 대조 재확인 필요. ②
`/objects/alta/wired/logic/latch.object.patch`의 한국어("상단/하단 Enable·Data 노드...")가
영문 원문("A Latch. Can be used to store a wire state.")과 내용이 전혀 달라, 다른 래치류
문자열이 잘못 섞여 들어갔을 가능성 — 내용 오류 자체는 미해결.

**검증**: 치환 309쌍 전량 needle-miss 0, JSON 파싱 전량 정상, 자산 변경 1,667건. exact-value
매칭 방식(부분 문자열이 아닌 필드 전체값 일치)으로 적용해 의도치 않은 부분 치환 위험을
배제. 게임 부팅 검증은 최종 단계로 보류(기존 방침 유지).

**사용자 지시**: 이 배치를 끝으로 오브젝트 조사 대사(glitchDescription/novakidDescription류)
검수는 후순위로 전환. 다음 우선순위는 the Ancients/Eithne/크라코스/Magicite/NonEKI 등
기존 보류 항목.

## 2026-09-28 (20~21차): fix_crew_sailor_batch17 + fix_glossary_batch18 — 선원→승무원 전역 판단 + STYLE_MIX group2/3 재개 + 플랫 패치 사각지대 초기 검수 (41자산)

사용자 지시로 3개 과제를 병행: ①선원→승무원 전역 통일 판단, ②12차에서 보류된 STYLE_MIX
fork 정독 group2·group3(67자산/1,397행) 재개, ③플랫 패치(`.patch`의 test 가드 없는 순수
replace 구조, 전체 `.patch`의 약 6%=3,680개, 기존 `extract_pak_pairs.py` 사각지대) 최초
검수. `female_translation.pak.NEW21`→`NEW22` 순차 적용, 백업:
`mods/female_translation.pak.bak-20260928-prebatch1718`.

**①선원→승무원(`fix_crew_sailor_batch17.py`, 30자산)**: pak 전체 "선원" 54건을 전수 대조.
근거: 바닐라 sbkor.tsv가 함선 승무원 고용 기능(Expand Your Crew/승무원 복장/승무원 수 UI)을
이미 일관되게 "승무원"으로 번역해 왔음(38건 확인) — "선원"은 뱃사람이라는 뜻이라 우주선
"crew" 기능에는 오역이었던 것으로 판단. 승무원으로 교정한 대상: 함선 승무원 고용/합류 대사,
crewcontract 계약서 6종, 아르카니안 함선 승무원 설명, 함장-승무원 콘솔 설명, 우주 항해
승무원, Crewmate 포켓볼 등. **제외(그대로 선원 유지)**: om_starrycultistsailor(바다 어부
NPC, 원문이 "sailor"), 코덱스 "Sailor Set"(패션 아이템명), "Privateer's Machete"→사략선원
(사략선 소속 뱃사람, 정확). 애매해서 보류: essential_gc_captainrumbarrels(해적 선장 자신의
선원, 바다 플레이버 의도적일 수 있음), nmm_mvg "모래선원"(novelty 아이템명, 애매).
같은 조사에서 발견한 별개 오역도 동시 수정: config_scannersignals의 "건설/의료/전기 기술자/
무기상/요리사 crew"가 "선원단"(뱃사람 무리)으로 오역됐던 것 → "무리"로 교정(5건, crew 기능도
sailor도 아닌 일반 작업조 의미). summonball_crewmateF/M 포켓볼의 "(암)/(수)"는 동물
성별 표기라 인간형 승무원에 부적합 → "(여)/(남)"으로 동시 교정.

**②STYLE_MIX group2·group3 재개(fork 4개 중 2개, 나머지는 ③에 사용)**: qa_pak_context_report.tsv
재생성 결과 STYLE_MIX 중 `/dialog/`(18~19차 완료 확인) 외 나머지가 67자산/1,397행으로
축소돼 있었음(12차 추정 39자산/2,716행은 그새 다른 배치에서 축소된 것으로 보임) — 34/33
자산으로 균등 분할해 fork 2개가 전수 정독. 확정 오류 5건(`fix_glossary_batch18.py`에 포함):
mwhaddon_mission_horizon 팔케 장군 대사 중 1줄만 존댓("흥미롭군요.")으로 이탈 → "흥미롭군."로
반말 통일; lawPBImissions_M04b "surcis"(프랑스어 sursis=집행유예)를 "심사"로 오역해 뜻이
반대로 읽힘 → "유예"로 수정; ffs2 SWAT 팀 표기 불일치(레드팀은 "SWAT" 유지, 블루팀만
"특수기동대"로 번역) → SWAT으로 통일; novakidquest Butane Cassidy 표기 불일치(완료문
"부테인 캐시디" vs killBoss "부탄 캐시디", batch_log 기존 확정은 부테인) → 부테인으로 통일;
quest4pbiMission2 Mox Fulder 표기 불일치(senderName 9건은 12차에서 "펄더"로 통일됐으나
turnInDescription 1건만 "풀더" 잔존) → 펄더로 통일. 판단 보류 2건 기록만 하고 미수정: Grounded
아비안 관용구 동일성 불확실, Nemui/Neumi 철자 불일치(동일 인물 여부 불확실).

**③플랫 패치 사각지대 초기 검수(fork 2개, 3,275쌍)**: 새 스크립트로 각 flat patch가 패치하는
원본 mod/바닐라 pak을 찾아 JSON 포인터로 패치 전 영문값을 복원(`extract_flat_pairs.py` 계열,
3,680개 flat 자산 중 3,275쌍 복원 성공, 나머지는 원본 미탐지 또는 cinematic류의 비-strict
JSON이라 파싱 불가 — 기술적 한계로 기록). 절반씩 fork 2개가 전수 정독. 확정 오류 3건
(`fix_glossary_batch18.py`에 포함): abyssvortex 글리치 설명 오타 "뭔든"→"뭐든"; 캐릭터 생성
화면(`charcreation.config`) 라디오 버튼 라벨 "SPECIES"가 "원형"(prototype)으로 오역돼
있던 것 → "종족"으로 수정(매 게임 시작 시 노출되는 화면이라 우선 수정); DUELLIST 특성
계열 중 `gic_trait_duellist_pistolaffinity`만 형제 라벨들과 달리 `[DUELLIST TRAIT]`·
`SHORT-SIGHTED`가 미번역으로 남아 있던 것 → 다른 형제 라벨의 `[결투자 특성]`과 같은 계열
상태이상 자체 라벨의 "근시" 표기에 맞춰 통일.

**부수 발견(후속 과제로 이월, 이번 배치엔 미포함)**: 플랫 패치 배치B 정독 중 글리치·노바키드
조사 대사에 해요체/합쇼체 존댓말이 광범위(추정 100건 이상)하게 섞인 체계적 패턴을 발견.
전체 pak 규모로 정규식 휴리스틱(어미 -요/-죠/-니다 등) 재스캔한 결과 글리치 1,034행·
노바키드 592행이 플래그됨(총 13,567개 glitchDescription/novakidDescription 필드 중).
표본 확인 결과 다수가 GIC 모드 계열 자산에서 나온 진짜 위반으로 판단돼, fork 5개(글리치
3개·노바키드 2개)에 영문 원문과 함께 재작성을 위임해 별도 배치로 처리 예정(다음 배치록에
기록).

**검증**: op/path/test 차이 0, JSON 파싱 전량 정상, 41자산 변경. 게임 부팅 검증은 최종
단계로 보류(기존 방침 유지).

## 2026-09-28 (19차): fix_glossary_batch16 — 후속 확정 소형건 일괄 (~200자산)

대사 검수 중 누적된 소형 확정 후속건 일괄 처리. 29 치환 쌍, 누적 ~200자산 변경
(시커 오브 더스트·dunebun·접두사 소수형 + 용어집 위반 정리가 광범위 자산에 전파).
`female_translation.pak.NEW20`(76,290,134B).

- **Seeker of Dust → 먼지 탐구자**(코덱스 표제 정본): 시커 오브 더스트(2),
  더스트 탐구자(1), 먼지의 추격자(1, 오역), 먼지의 탐구자(9) 통일.
- **dunebun → 사구빵**(dune+bun 언어유흥, hotbrodstand 확립): 둔벙(3)·듄번(3)
  통일 — Crawler Dunebun 아이템·퀘스트·볼보흔 잼 묘사 일관.
- **Flare Catapult → 플레어 카타펄트**: 투석기는 공성 병기라 부적합
  (12차 GDI 카타펄트 정정과 동일 논리). 투석기 잔여 0.
- **[CORPORATE KAPPA TRAIT]/[CORPORATE KAPPA]/[Corpo Kappa] →
  [기업 캇파 특성]/[기업 캇파]**: 미번역 시스템 태그 7건 (Kappa→캇파 지배형).
- **Miniknog → 미니크녹**(용어집 고정) 위반 정리: 미니크노그 이형 31건 전역
  교정 + 지식부 현지화 19건 정본 통일 + 미션명 '지식부 요새'→'미니크녹 요새'.
  조사 입자 관리: 지식부가→미니크녹이 등 7종 선적용 + 치환 부산물
  미니크녹가/를/는(30건) 은/이/을로 재교정.
- **Fuel Hatch → 연료 해치**(고정): 'FTL 드라이브 연료 주입구' 3건.
- **Hit Shield → 피격 방패**(고정, GiC 확정): '타격 보호막' 5건
  (물약·미코 방패·피해 트리거 계열).
- **글리치 감정 접두사 소수형 마무리**: Observative 계열
  관찰함./관찰력 있음./관찰력.→관찰.(4건), Amiable 우호적.→우호.(1건).
  문장 내부 형용사(우호적인 생물)는 유지.

**검증**: 3단계 누적 적용(40→62→69 자산 단계), 매 단계 op/path/test 차이 0,
태그·플레이스홀더 차이 0. 설치 후 재추출 182,157쌍, 잔여 스캔 전량 0.
**qa_pak_glossary 위반 300→232** (Miniknog/Kappa/Fuel Hatch/Hit Shield 항목
소멸 — 잔여는 Materials Available 169·Alliance 23·Floran 9·Old One 7 등
기보류 항목). qa_pak_context 리포트 재생성 — 신규 플래그 없음.
백업: `...bak-20260928-preglossarybatch16`.

## 2026-09-28 (18차): fix_glossary_batch15 — 대형 /dialog/ 3종 정독 수정 (66자산)

마지막 대형 대사 자산 정독(`_review_dialog_large.txt` 2,638쌍): viera(1,364행),
alta(734), atprk_relicseekercrew(540). 214 치환 쌍(전역) + 3쌍(자산 스코프),
66 자산 변경(3 대사 + 용어 통일이 전파된 코덱스·아이템·오브젝트 63).
`female_translation.pak.NEW19`(76,448,462B).

**레지스터 정규화 (~150행)**: 세 자산 모두 전 섹션 casual 지배
(비에라 60~90%, 알타 80~95%, 시커 ~95%; `-합니다/-입니다` 포함 재집계로 확인).
소수 요체/합쇼체 이탈 라인을 화자별 반말로 재작성 — 초안 생성기
`_gen_register_draft.py`의 기계 변환(안녕해·어떠어·주내가 등 오류 다수)은
참조만 하고 전 라인 수동 재작성. 의도적 고어체(그대/하네 — 비에라 장로·
방랑자 시적 레지스터)와 숲 신성화 존칭(돌봐주셨다)은 유지.

**용어 통일(용어집/지배형)**:
- wood-warder→숲의 파수꾼(고정): 우드-워더/우드 워더 9건; 인격화 the Wood
  '우드'→'숲' 2건(숲께서 신성화와 일치); 대장→우두머리, 연고 제조자→제작자,
  원로→장로, '숲의 파수꾼는' 조사 2건
- caretaker→관리인(알타 코덱스 지배): 보호자·돌보미 용례 10건(대사+아이템)
- stardust 물질→별가루(코덱스 관례): 별먼지 전량; 고유명 Stardust X→스타더스트
  유지(스타더스트 오키드 복원). staris(알타어) 별개 유지
- spacedrifter→스페이스드리프터(우주 방랑자/유랑자 7건)
- alternia→알테르니아(20), enternia→에터니아(21), 크리스탈 정원→수정 정원(3),
  세터 구체→세터스피어, 알터스피어→알테르스피어(2), 5티어→티어 5,
  3등급 자격증→티어 3, 신용 화폐→크레딧, 두블론→더블룬(2), 파란 종기→블루 보일
- Green Word→녹색 언어(지배형 17:6, 코덱스 팩션 용례 포함 6건)
- vision dust→비전 가루(환영 가루 2건)
- Solalei→솔라레이(솔랄레이 7), Actias→악티아스(액티아스 4),
  drei→드라이(드레이 키트), Peglaci→페글라시(페글라치 3), Io→이오
- the Ancients→고대인(에인션트 2건 — 크라코스 코덱스 잔여 21건은 별도 패스 보류)
- crew→승무원(고정): in-scope 3건만(전역 선원 패스는 50+ 혼합 문맥이라 보류)
- 호칭: Sis→언니(동생아/자기 이탈 2건)

**오역·비문**: 'Color me surprised' 색깔 직역→'정말 놀랍네!', ava→아바
(아바타 오역), hatchlings→새끼(부화체 오역; 몬스터명 부화체는 유지),
'나미' 조사, 상자 경주 농담 '잘했다→잘했어' 레지스터, '선원 자리'→'승무원 자리'

**ASSET_SCOPED 확장**: 도와드릴까요?(6자산 공유), 도와주세요!(5자산),
너무 멀어요!(승무원 npctype 6+) — 다른 자산 레지스터 미검증이라 viera/alta
한정 적용.

**검증**: 설치본 대비 변경 66자산, op/path/test 차이 0, 태그·플레이스홀더 0,
NEEDLE-MISS 0(1차 62자산+2차 잔여 4자산+3차 우드 워더 4자산). 설치 후 재추출
182,157쌍. 잔여 스캔: 대상 요체 이탈 0, 우드 워더/별먼지/녹색 말/알터니아/
엔터니아/솔랄레이/액티아스 0. qa_pak_glossary·qa_pak_context 리포트 재생성 —
신규 플래그는 전량 검출기 오탐 또는 기존 보류 항목, 회귀 없음.
백업: `...bak-20260928-preglossarybatch15`.

## 2026-09-28 (17차): fix_glossary_batch14 — 잔여 소형 /dialog/ 자산 정독 수정 (206자산)

미검수 `/dialog/` 패치 자산 정독(`_review_dialog_small.txt` 2,659쌍) 후 확정 오류만
수술적 치환 + 말뭉치 전역 감정 접두사 명사형 규칙 일괄 정리. 181 치환 쌍(전역)
+ 3쌍(자산 스코프), 206 자산 변경. `fix_glossary_batch14.py` — 신규 pak은
`female_translation.pak.NEW18`(76,633,111B). 생성기 `_gen_batch14.py`,
스코프 쌍 산출물 `_batch14_scoped.json`.

**미니크녹가→미니크녹이** (45건): 자음종성 고유명사 뒤 '가' 입자 전역 오류.
대화·npc·오브젝트·코덱스 자산 전부 포함. 후행 공백 확인 후 일괄 치환.

**감정 접두사 명사형 정규화(10차 규칙), EN 스코프 적용**:
- Cautious: 조심./조심함./경계. → 주의. (66고유쌍; Careful/Wary의 조심은 유지)
- Alert: 경계./경보. → 경고. (8고유쌍; Alarmed/Alerted/Wary의 경계는 유지)
- Observant: 관찰적./관찰함./관측력 있음./관찰력. → 관찰. (30고유쌍)
- Neutral: 중립적./무덤덤함. → 중립. (8; 단 글리치 모루 설명 '자랑.' 4건은
  본문이 의도적 로어 개작이라 접두사도 개작에 맞음 → 유지로 기록)
- Tired 피곤하다→피곤(3), Traumatized 트라우마가 생겼다→트라우마,
  Invigorated 활기가 넘치긴→활기 넘침, Doubtful 글쎄→의심,
  Amicable 우호적→우호(4), Threatening 위협적→위협(5),
  Skeptical 회의적→회의적임(3, 유혹적임 선례), Speculative 추측이지만→추측,
  Envious 질투함→질투, Content 내용→만족(viera FTL 오브젝트 3자산 공유).
- 잔여: 'Amiable.'→우호적(whitecrow 1건), 'Observative.'→관찰함/관찰력(3건),
  'Perceptive.'→관찰력 — 별도 EN 접두사라 소수형으로 차기 마이크로 후보 기록.

**레지스터 이탈 → 각 화자 지배 레지스터로 통일**:
- allianceoutpost aegi 주민 7건(해라체/해요체/존댓말 → 해체)
- USCMdisbanded 해라체 3건(전직 해변 구어체에 맞춤)
- moogle 쿠포 구어체 7건(존댓말 이탈 정리)
- ayylien 3건, SaturnGuardMage 3건, unbound 마을 경비 3건,
  saturnWaspmim 5건(전체 지배형 반말), lustia 오락실 2건,
  samuraimerc hylotl/hylotl 1건(동족 대화부의 존댓말 이탈)
- 보류 판단: elpis 판매원 존댓말(영업 어투), trink 로봇 존댓말,
  devouttenant beacon 정중함(정중 접두사 의도), atprk 펭귄 존댓말 — 의도적.

**확정 오역·비문**:
- sgD03MU/flee 'I'm unarmed!' → '무장 해제! 도와줘!' 오역 → '난 비무장이야!'
  (해제=disarm 아님; 동 자산 '이제 안전한가요?'→'이제 안전해?' 자산스코프)
- gicexp 'Sweet profits...' → '맙소사 수익이라니...' 오역 → '달콤한 수익이여...'
  (esc_intromission의 기업체 감탄 관례와 통일)
- samuraimerc: '명예 위해!'→'명예를 위해!'(조사 누락), '내 검 널 갈가리
  자를 거야!'→'내 검이 널 갈기갈기 자를 거야!'(비문), Loyalty above all의
  afraid를 '두렵겠지'로 오역→'유감이지만 ... 죽어야 한다는 뜻이야'
- devouttenant converse/7 '우리 주인 수백 년 전 떠났지만 왕국 서있어.' 조사·
  조사 누락 복원 (visitor npctype 공유 문자열도 동시 교정)
- eldermerchant R'lyeh 괴이 발화 2건 자연어 역출 → 음차 통일
  ('이리 와!'→'크' 프응글루이 ...', '음, 아니당...'→'을을 노그 야...')
  — '이리 와!'는 5자산 공유 문자열이라 ASSET_SCOPED 도입해 자산 한정 적용.
- nakedvillager fenerox 건만증→건망증(2), 궁금한가?→궁금해?(전보체)
- rainbowent '날 무겁다 마' 비문→'날 무겁다 여기지 마'
- prisoner fenerox '이상 곳'→'이상한 곳'(2자산), '자유야.'→'자유.'(전보체, 2자산)
- P1078_M03hostile 'Don't m...ve!' 더듬이 '우...'→'움...'(음절 대응)
- shuttlepilot 여객기→여객선(Passenger Liner; '여객선 프레임' 아이템명 정본)

**소스 결함 기록(미수정)**: saturnKytaguard /hail/saturn/saturn/2 EN 원본이
"I'm here to"로 절단(모드 소스 자체 결함) — KO '여긴'은 충실 대응이라 유지.

**검증**: 설치본 대비 변경 206자산, op/path/test 차이 0건, 태그·플레이스홀더
토큰 차이 0건, NEEDLE-MISS 0건. 설치 후 재추출 182,157쌍. 잔여 스캔: 미니크녹가 0,
건만증 0, 존댓말 이탈 대상 전량 0. qa_pak_glossary 위반 300건 — 전량 기보류 항목
(Materials Available 169, Miniknog 57 등), 회귀 없음. qa_pak_context 리포트
재생성(분류: style 129그룹/6838행, literal 175, dup_particle 739, truncated 59,
untranslated 22). **게임 검증은 최종 단계로 보류(사용자 지시)**.
백업: `...bak-20260928-preglossarybatch14`.

## 2026-09-28 (16차): fix_glossary_batch13 — tentacles 성인 대화 자산 정독 수정 (23자산)

`/dialog/tentacles/` 37개 자산(1,539쌍) 정독 후 확정 오류만 수술적 치환. 53 치환 쌍,
23 자산 변경(동일 문자열을 공유하는 `npcs/furniture/naked.npctype`과 FFS 글리치
스테이지핸드도 자동 연동). `female_translation.pak.NEW17`(77,017,257B).

**글리치 감정 접두사 명사형 규칙(10차 확립) 잔여 위반 정리**: 물들었다→물듦,
피곤하다→피곤(3), 더럽혀졌다→더럽혀짐, 절박하다→절박(촉수+FFS 스테이지핸드
"Desperate."까지 2건), 지쳤다→지침, 궁금하네→호기심(4), 이상하다→이상함,
유혹적→유혹적임, 아파→아픔. 전부 문맥 바늘로 적용해 문장 내부의 정상 용례
(플로란/농부 등)는 미접촉. Kinky 킹키→음란(글리치 확립형).

**말뭉치 지배형 통일**: floran fuck-meat의 6종 변형(떡고기/박을-고기/박음-고기/
씹갯살/씹당하는 부화장/떡감)을 떡감으로 통일(코퍼스 20:5:4…, sexbound 대사군도
떡감). 촉수 문맥 hive의 벌집 4건→둥지(벌 이미지 부적합; 생물군계·재료·ttppinky의
벌집은 정상 유지, 둥지/하이브 동의어 혼용은 허용).

**확정 오역 수정**: hump→혹(엉덩이 혹→엉덩이를 박힐 때마다), EN 오타 dish→접시
(→이런 건), gestate→수정(→잉태), virility→생식력(→정력), seedbed→종자상(→씨받이
확립형), fenerox drained→다 마심/빠짐(→탈진), fur heavy→털이 잔뜩(→털 무거움),
Not...Like...This→끝날 순(→이렇게는 안 돼), 미번역 AAH→아악.

**레지스터 이탈 수정**: avian-exhausted 존댓말 2건(마세요/에요→반말),
novakid-exhausted -네요→-네, fenerox 그르렁대요→가르랑거림(전보체).

**기타**: Ook Ook Ah! 원숭이 소리 복원(우끼 우끼 아), Oook 우움→우욱 통일,
squawk 꼬끼오→꽥꽥(파티객의 실제 닭 울음 꼬끼오는 유지), 부드러운 꽉→죔,
그립→붙잡음, 촉수기는→촉수긴, 제발알→제바알, 하이브서→하이브에서 조사 누락.

**검증**: NEW16 대비 변경 23자산, 비대상 leaf 차이 0건, op/path/test 차이 0건.
설치 후 재추출 182,157쌍. 잔여 스캔: 떡고기/박을-고기 계열 0, 유혹적. 잔여 2건은
플로란 문장 내부 용례(정상). qa_pak_glossary 위반 300건 — 전량 기보류 항목.
백업: `...bak-20260928-preglossarybatch13`.

## 2026-09-28 (15차): fix_glossary_batch12 — 라디오메시지 자산 정독 수정 (62자산)

라디오메시지 자산군(덤프 734행, `_review_radio.txt`) 정독 후 확정 오류만 수술적 치환.
102 치환 쌍, 62 자산 변경, 59,062 엔트리 유지. `fix_glossary_batch12.py` — 신규 pak은
`female_translation.pak.NEW16`(77,103,629B).

**고유명·세력명 정리** (검수 자산 및 동일 퀘스트 체인 한정, 문맥 확인 후 적용):
- Aurea Seekers→아우레아 탐구자(시커 용례 정리), Aurea Collective→아우레아 콜렉티브,
  Lodestar Temple→로드스타 신전(사원 이형 소거).
- Seeker of Dust→먼지 탐구자(codex 표제 정본). 단 codex/item/monster 설명문의
  "시커 오브 더스트" 4건은 미검수 자산군이라 이번 범위 밖으로 보류.
- GICEXP 라디오의 Resistance→저항군 통일. 단 Apex 코덱·플러시·몬스터의 "레지스탕스"
  5건은 별개 맥락이라 유지(기존 결정 재확인).
- Terrene Guardians 계열은 11차 정본(가디언즈) 유지.

**맥락 한정 통일**:
- FFS 내부: drop pod→탈출 포드(생존/탈출 맥락), armory→병기고, catapult→캐터펄트.
  GICEXP 아이템명 "드롭 포드" 2건은 별개 오브젝트라 유지.
- MWHaddon: 존댓말 혼용 정리, 중단 행 "We just observed a viol-"→
  "방금 폭력적인 반응을 관측했-"(절단 구조 보존), 선하 대장→선하 선장.
- Viera/PF 튜토리얼: Stone Hearth→돌 벽난로(스톤 헤스·돌 화로 이형 소거),
  Hazard Lab Table→위험 실험 탁자, Inventor's Table→발명가의 작업대,
  Robotic Tool Table→로봇 도구 탁자, Woven Fabric→섬유 천, Regulator→조절기.
- Magicite: 라디오+동일 퀘스트 체인에서만 마기사이트로 정리(모아와라→모아오라 표기
  교정 포함). 매지사이트/마기석/마법석의 전역 분화는 아이템 정의 전용 패스로 보류.
- 기타: Timeless Planets(시간 없는 행성 잔여 소거), 유린당한 정예 드랄(Thea),
  Interception Territory→요격 영역, atprk_planetpincomments 감정 접두사 명사형
  정규화(정보 습득/불안함/경시/당혹/호기심/무감동/사색 계열을 말뭉치 지배형으로).

**검증**: NEW15 대비 변경 62자산, 비대상 leaf 차이 0건(전 diff가 치환 쌍으로 설명됨),
op/path/test 필드 차이 0건. 설치 후 재추출 182,157쌍. qa_pak_glossary 위반 300건 —
전량 기보류 항목(Materials Available 169, Miniknog 57 등). 신규 관찰: esc_ 특성 자산의
[CORPORATE KAPPA TRAIT] 미번역 태그 6건(Kappa 규칙 탐지) — 별도 자산군 보류.
잔여 스캔: 월레스 0, 시간 없는 행성 0, 선하 대장 0; 투석기 1건은 "Flare Catapult"
아이템명이라 마이크로 정리 후보로 기록. **게임 검증은 최종 단계로 보류(사용자 지시)**.
백업: `...bak-20260928-preglossarybatch12`.

## 2026-09-28 (14차): fix_glossary_batch11 — 중형 STYLE_MIX 자산 정독 수정 (53자산)

중형 대사 자산 21종(총 963쌍) 정독 후 확정 오류만 수술적 치환. 45 치환 쌍, 53 자산 변경.

**Terrene 조직명 정리** (용어 충돌 해소): Guardians 세력이 수호자/수호자들/수호자단/가디언/
가디언즈/행성 가디언/테린 수호자/테렌 가디언즈로 혼용됐는데, Protector가 이미 수호자로
확정(11차)되어 "us Guardians"→"우리 수호자들"은 Protector로 오독 가능 → union.codex의
정본 표기 "행성 가디언즈"로 통일(축약형 "가디언즈"). Electorate는 선거단 지배(13:5) →
선거국/지상 선거구를 선거단으로 통일. "행성 수호자 스티커" 등 아이템명도 연동 정리.
r-guardianconverse의 절 부착 오독("whatever destroyed our home"을 Guardians가 파괴한
것처럼 읽은 문장) 재작성.

**기타 확정 수정**: penal colony→형벌 식민지 통일(형무소 행성 잔여 2건), Aventor Galliot
갤리엇→갈리옷, Big Ape 큰형님→빅 에이프 2건, Apiarian 아피어리안→아피아리안,
K'Rakoth 크레이코스→크라코스 3건, 코덱스 카파→캇파, Officer→경관 잔여(장교다/보안관이야),
감정 접두사 잔여 위협적임(15)/유혹함(1), commands.config "I'll get that"→가져올게 오역
2건, friendlyminer의 Welcoming 접두사 누락 복원, lustiahint1 존댓말↔반말 혼용 정리,
"shaft" 중심축→대물(성적 이중의미 복원), waspmim 공격 대사 쥐이잉→윙윙.
"Don't mind if I do!"는 lounge(휴식)와 alta 요리기구(식사) 양쪽에 쓰이므로 맥락중립
"마다할 이유 없지!"로 치환.

**검증**: NEW15 파싱 정상(59,062 엔트리), NEW14 대비 변경 53자산에서 op/path/test/
토큰 차이 0건, 대상 오표기 전량 소거 확인. qa_pak_glossary 위반 301→300건(잔여는 기보류
항목). 백업: `...bak-20260928-preglossarybatch11`.

## 2026-09-28 (13차): fix_glossary_batch10 — Glitch 감정 접두사 정규화 + 대형 대사 자산 정독 수정 (214자산)

STYLE_MIX 대형 대사 자산 4종(bartenderwoofie 273, lucario 285, saturnspaceconverse 283,
avikanoutpost 268행)을 직접 정독하고 확정 오류를 수술적 패치. `fix_glossary_batch10.py`:
설치 pak을 읽어 JSON 값의 정확한 한국어 문자열만 재귀 치환 후 SBAsset6으로 재빌드.
341 치환 쌍(감정 접두사 자동 164 + 정독 확정 수동 177), 214 자산 변경, 59,062 엔트리 유지.

**감정 접두사 정규화**: 영문이 감정 단어로 시작하는 Glitch/기계 NPC 대사에서 한국어 접두사가
명사형 규칙("명사. 문장")을 벗어난 164건을 말뭉치 지배형으로 통일(위협적이긴→위협,
분개했긴→분개, 궁금하네→호기심, 감명받았긴→감명 등). 스윕 누락 잔여(희망참, 유혹적임,
불만족계열, 비위 맞추긴)도 동일 규칙으로 추가 정리. 단 "아마 안전하지 않겠지. 하지만...
위협적이긴 하죠."처럼 문장 중간의 자연 형용사는 접두사가 아니므로 유지.

**대형 자산 정독 확정 수정** (플레이스홀더·태그 보존 확인):
- Starfarer's Refuge/스타파러 계열: 파어러·파러·레퓨지 표기를 "스타페어러의 피난처"로
  통일(지명), 인칭 "스타파러"는 "스타페어러"로 통일.
- Vas Vha'leih: 바레이/브알레이 등 변형을 문맥 지배형 "브할레이"로 통일.
- The Watchers: 감시자단(편집부 어감) → 문맥상 "감시자들"로 통일. 단 몬스터명
  "Hypnotic Watcher"(히프노틱 워처)는 고유명사라 유지.
- Fluffalo: "플러팔로" 31건 전역 오표기 → TM 확정형 "플루팔로"로 통일.
- Watcher Drone 코덱 "와처 드론" → 아이템명 "감시 드론"과 통일.
- 그 외 조사 누락 비문·오역 다수(lucario: flavor→취향 오역, saturnspace·avikan 전보체 등).

**검증**: `pak.py` 파싱 정상(메타 female_translation 2026-09-27.2). 구 pak 대비 엔트리수
동일(59,062), 변경 214자산 중 op/path/test/기타 스칼라 필드 차이 0건, `^`태그·`${var}`·
`%s`·`<arg>` 토큰 차이 0건, 미변경 자산 58,848개 바이트 동일. `extract_pak_pairs.py`
재추출 182,157쌍(기존 JSON 결함 2건은 선존). `qa_pak_glossary.py` 위반 301건(기존 374건
대비 감소, 잔여는 Materials Available·Miniknog·Fuel Hatch 등 기보류 항목). 잔여 오표기
스캔 0건(히프노틱 워처만 의도 보존). **게임/서버 검증은 최종 단계로 보류(사용자 지시)**.
백업: `...bak-20260928-preglossarybatch10`.

## 2026-09-28 (12차): fork 기반 STYLE_MIX 정독 QA 그룹0·그룹1 확인 14건 수정 (15자산)

11차까지의 용어집 기반 QA가 반복 재실행에도 신규 발견이 거의 없이 정체되자, 사용자가
"우린 비효율적으로 간다" / "이 거 번역한 문자열이 수십만개다"라고 지적. 좁은 정규식·휴리스틱
스캔과, 사용자가 문제 문장을 일일이 짚어주는 방식 둘 다 18만여 행 규모에는 확장 불가능하다는
판단 아래, 방법론을 전환: `qa_pak_context_report.tsv`의 `STYLE_MIX`(다중 화자 대사) 미검토
76개 자산군(5,436행)을 4등분해 fork 서브에이전트에게 실제 정독(reading comprehension) 기반
QA를 맡기는 방식 도입. group0·group1(2개 fork, ~2,720행/39자산) 실행 완료, 실제 오류 14건
확인(내용 누락형 아님, 전부 어휘 불일치·오타·비문 계열). group2·group3(나머지 39자산,
~2,716행)은 사용자 지시("잠깐, 그거 나중에하자")로 미실행 상태로 보류.

**수정 14건** (각 항목은 pak_pairs.tsv 재조회로 fork 보고 내용을 직접 재검증 후 확정):
1. Leda Portia: senderName 전량 "레다 포르샤"(5건) vs `ttppmission2d1/text` 본문 1건만
   "레다 포르티아" → 포르샤로 통일.
2. Qingque Tea Brewer: 오브젝트 자체 `/shortdescription`(게임 내 실제 표시명)과 퀘스트5
   completionText가 "칭췌 차 우림기"로 일치 → 나머지 인터페이스/라디오메시지 2종 변형
   ("칭추에 찻주전자" x2, "칭퀘 차 양조기" x1)을 이 표준명으로 통일. ("칭취"는 차 맛 자체를
   가리키는 별개 표현이라 미변경.)
3. Officer: 경관(26건) vs 장교(3건, lawenforcementconverse.config.patch) → 경관으로 통일.
4. Beacon(atprk_fuelderguardian): 비컨(8건) vs 비콘(1건)/신호기(1건) → 비컨으로 통일.
5. Bridge(함교): ffs_whitecrow.radiomessages.patch 소속 5개 문자열이 "교두보/교두부"(군사
   용어 "교두보=bridgehead"와 혼동)로 오역 → 문맥(FTL 드라이브·핫라인·기술팀 호출)상 함선의
   "함교"가 맞아 전량 수정.
6. Mox Fulder/Agent Fulder: senderName 전량 "목스 펄더"(9건) vs 본문 "Agent Fulder" 6건이
   "폴더 요원"으로 오기 → 펄더로 통일. (별개 오브젝트 "Mox Folder's Missions"는 영문 원문
   자체가 "Folder"라 무관, 미변경.)
7. `pf_samuraimerc.config.patch` "갈갈이 자를 거야" 오타(2건) → "갈가리".
8. ffs2_radiomessages: "Sir" 호칭이 해당 파일 내 압도적 다수(10건) "대장님" vs 단독 "님"(3건)
   → 대장님으로 통일.
9. Relic Seekers: 유물 탐색단(30여 건) vs 유물 탐구자(6건, 문장 템플릿은 유지하고 용어만 교체)
   → 탐색단으로 통일.
10. `atprk_relicseekercrew.config.patch` `/converse/novakid/avali/2`: 조사 누락으로 끊어진
    비문 → 자연스러운 문장으로 재작성.
11. Arcane catalyst: 아케인 촉매(2건) vs 비전 촉매(1건, shpd_catalyst2) → 아케인으로 통일.
    같은 파일 `^oange;` 손상 태그(2건) → `^orange;` 복구.
12. `SaturnGuardMage.config.patch` `/converse/saturn/default/29`: 조사가 통째로 빠진 전보체
    비문 → 자연스러운 문장으로 재작성.
13. partner: mwhaddon_mission_sideStory 내 9건이 "파트너"인데 `horizon_4_1`만 "친구" → 파트너로
    통일.
14. target: `ffs_alice_combat.config.patch`에서 같은 개념(적 조준 실패)에 목표/과녁이 혼용 →
    목표로 통일.

`fix_glossary_batch9.py`. 15개 자산 반영(대상 14건 중 Beacon·Bridge 등 일부가 같은 자산 내
복수 항목이라 자산 수는 14보다 적고 문자열 교체 수는 더 많음). JSON 유효성 검사 결과 기존에
알려진 결함 2건(`colourful.config.patch`, `spacehero.config.patch`, 이번 수정과 무관)만 남고
신규 결함 없음. 서버 부팅 검증(`glossarybatch9_verify.log`) `[Error]` 0건, `listening` 확인 후
정상 종료. 백업: `...bak-20260928-preglossarybatch9`.

## 2026-09-28 (11차): Protector 용어 변경 — 보호자/프로텍터 → 수호자 (사용자 지시, 107자산)

10차의 Grand Protector 변경에 이어 사용자가 "'프로텍터'도 '수호자'로 통일하죠" 지시.
`translation_glossary.tsv`의 Protector 행(rule=context)을 "보호자"(구 선호)↔"수호자"(신 선호)
순서 반전.

**범위 판단**: 프로텍터(57건)는 압도적 다수가 바닐라 스타보운드의 플레이어 칭호 "Protector"
그 자체(대사/퀘스트/코덱스/아이템명 전반에 반복 등장)라 일괄 치환 대상으로 삼되, 아래 3개
예외는 치환 전 플레이스홀더로 보호 후 되돌림:
- **오토프로텍터**(Autoprotector): 이미 음역 상태인 형제 용어 오토리펠러/오토애널라이저와
  내부 일관성 유지 위해 미변경.
- **EDS 프로텍터**: 드로이드 계열 고유 지정명으로 판단, 미변경.
- **테레네 프로텍터레이트**: Terrene Protectorate 자체의 기존 허용 대안 표기(7차/배치2 조사
  때 결정)라 계속 보존.
그 김에 `esc_componentcase` 자산 2건에서 원문에 "Protectorate" 언급이 전혀 없는데도 번역이
임의로 "프로텍터레이트"를 넣어둔 무관 오류를 발견, "보호국"으로 함께 수정(오늘 Protector
변경과 별개의 기존 Protectorate 규칙 위반).

**보호자(bare, rule=context 이전 선호형) 31건 전수 확인**: 원문이 "Protector"인 16건만
정확히 "수호자"로 개별 치환(전체 문자열 단위 타겟 치환, 전역 치환 금지). 원문이 "caretaker"인
6건(알타 NPC의 "예전/옛날 보호자", `plushguardiandroid`의 "봉제 로봇 보호자", 쿠다 봉제인형·
소나베일/생명샘 음식 설명의 "보호자")은 Elithian/Protectorate 세계관과 무관한 일반 단어
"보호자(guardian/caretaker)" 용법이라 그대로 유지.

`fix_glossary_batch8.py`. JSON 유효성·플레이스홀더 잔존 0건·예외 보존 확인 후 반영. 서버 부팅
검증 진행 중. 백업: `...bak-20260928-preglossarybatch8`.

## 2026-09-28 (10차): Grand Protector 용어 변경 — 대보호자 → 고위 수호자 (사용자 지시, 92자산)

사용자가 배치4에서 통일한 "대보호자"("부자연스럽잖아요 그거")를 지적, "고위 수호자"로
바꾸도록 직접 지시. `translation_glossary.tsv`의 Grand Protector 행을 "고위 수호자"로
갱신하고, pak 전체의 기존 92건(배치4 이전부터 있던 다수파 79건 + 배치4가 통일한 13건)을
전량 재치환. `fix_glossary_batch7.py`. 서버 부팅 검증 진행 중. 백업:
`...bak-20260928-preglossarybatch7`.

## 2026-09-28 (9차): 용어집 배치6(4자산) — Elithian Alliance 배너 계열 잔여 3건

배치5 이후 재추출·재스캔한 잔여 위반 313건 중 새로 드러난 Elithian Alliance 배너/포스터
계열 롱테일 3건 확인·수정.

**수정**: Aventor(아벤터→아벤토르, 조선 기업명), Hymidian Republic of Hyzolia(하이졸리아
하이미디안 공화국→하이졸리아 하이미드 공화국, Hymid 어간 오류), Triple Monarchy(삼중
군주 배너→삼중 군주국 배너, "국" 누락). `fix_glossary_batch6.py`. 서버 부팅 검증 진행 중.
백업: `...bak-20260928-preglossarybatch6`.

이 시점 잔여 위반은 Materials Available/Miniknog/Alliance(일반 관용구)/Floran/Kappa(코덱스
그리스문자)/Old One/Pixels/Fuel Hatch/One-Handed/Terrene Protectorate/Trink/Spooked 등
전부 이전 배치에서 오탐·판단 보류로 이미 확인한 항목들이며, 아이템명/설명 대상 용어집
`rule=fixed` 기계 대조 기준으로는 실질적으로 수렴 단계에 도달했다.

## 2026-09-28 (8차): 용어집 배치5(9자산) — 잔여 롱테일 단발성 위반 정리

배치4 이후 재추출·재스캔한 잔여 위반 313건(대형 항목 정리로 롱테일 단발성 항목들이 상위
30위 안에 새로 드러남) 중 실제 오류로 확인된 9자산 수정.

**수정**: Ruin-Killer(루인 킬러→루인킬러, 공백 제거), Thrust Damage(관통 피해→찌르기 피해,
단검 투척 라벨 한정 타겟 치환 — "관통 피해"라는 표현이 다른 무관 문맥에도 1건 더 있어
전역 치환은 피함), Broadsword(대장간 재료 목록의 "(대검)"→"(브로드소드)", 용어집이 명시적으로
대검/장검 혼용을 금지), Zerchesium(제르케시움→제르세슘), United Systems(연합 체계→연합
시스템, 용어집이 "연합 체계로 쓰지 않는다"고 명시), Droden(드로든→드로덴, 다수파 212건과
합류), Knockback(강한 날려보내기→강한 넉백), Fusion Chamber(융합실→핵융합로, `alliance/`
네임스페이스 확인됨). `fix_glossary_batch5.py`. 서버 부팅 검증 통과(`[Error]` 0건). 백업:
`...bak-20260928-preglossarybatch5`.

**조사 후 유지(오탐/판단 보류)**:
- **Hit Shield**(용어집: 피격 방패, "GiC 확정 용어") — 실제 pak은 5건 전부 일관되게 "타격
  보호막"을 쓰고 있고 "피격 방패"는 pak 어디에도 실사용 0건. 아에기니안 사례와 달리 용어집에
  "사용 금지" 명시가 없어 확정 오류로 보기 어려움 — 이미 배포되어 일관되게 쓰이는 5건을
  실사용 0건인 용어로 덮어쓰는 것은 사용자 확인 후 처리하는 게 안전하다고 판단해 보류.
- **Union flag**: `flagaegipride`의 "Aeginian Federal Union flag" 설명이 영어 인접("Federal
  Union" + "flag")으로 우연히 "Union flag" 부분 문자열을 만든 것일 뿐, 용어집이 말하는 별도
  "Union" 세력과 무관 — 이미 3차 Aeginian Federal Union 수정으로 "에지족 연방 연합 깃발"로
  올바르게 되어 있음. 오탐.
- **The Ruined**: 플로란 코덱스 시가 "폐허가 된 도시"라는 일반 형용사 표현이라 용어집 주석이
  명시한 예외("일반 형용사 ruined에는 적용하지 않음")에 정확히 해당. 오탐.
- **Boneworking/Leatherworking Station**: 해당 용어집 행은 Elithian Alliance 전용 제작대를
  가리키는데, 실제 히트는 아비칸(avikan) 진영의 별개 제작 오브젝트라 다른 지시 대상. 오탐.
- **dunebuns**: 용어집은 일반 음식 아이템 "dunebuns"(사구빵)를 가리키나, 실제 히트는
  "Crawler Dunebun" 퀘스트 보상이라는 별개 생물/펫 고유명사로 판단, 미변경.

## 2026-09-28 (7차): 용어집 배치4(132자산) — Grand Protector/Relic Seeker 등 다수 소수파 오표기 통일

6차 이후 `pak_pairs.tsv` 재추출 + `qa_pak_glossary.py` 재실행으로 잔여 위반 374건을 재조사.
아래는 실제로 고친 것과, 조사했지만 의도적으로 손대지 않은 것을 구분해 기록한다.

**수정(132자산)**: Thelean 잔여 변형(텔레아/텔 단독형, 자산별 타겟 치환), Protectorate 잔여
변형("프로텍터레이트"가 Terrene Protectorate 행의 허용 대안과 겹쳐 전역 치환이 위험해
자산 내 전체 문구 단위로 타겟 치환), Elithian Alliance 잔여 변형("엘리시아 연합"), Alliance
(Elithian 고정 규칙 — `alliance/` 네임스페이스 등 세력명이 명백한 자산만 선별 치환, 일반
영어 단어 "alliance"의 소문자 관용구는 손대지 않음), Relic Seeker(렐릭 시커→유물 탐구자,
금지어인데 소수 잔존), Aegisalt(이지설트→에지솔트), Magilock(마지록/마기록→매지락),
Magishot(매직샷/마법탄→매지샷), gheatsyn(게아신→기트신, 2026-09-23 용어 확정 이전 표기),
Kel'chis(켈키스→켈치스), Jorgasian(조르가시아→조가시안), Notician Federation(노티시안
연방→노틱스 연방), Mehros Avan(메흐로스 아반→메로스 아반), **Grand Protector**(대프로텍터
11건/대호보자 스크램블 오타 1건/대수호자 이표기 1건 → 전부 대보호자로 통일, 다수파
대보호자 79건과 합쳐 완전 통일), Trink Circuit(트링크 회로→트링크 서킷), Crafting
Station(제작 스테이션→제작대), Sniper Rifle(저격 소총→저격소총, 공백 제거), Quietus(쿠에투스
→콰이어투스). `fix_glossary_batch4.py`. 서버 부팅 검증 통과(`[Error]` 0건). 백업:
`...bak-20260928-preglossarybatch4`.

**조사 후 의도적으로 유지(오탐/판단 보류)**:
- **Old One**: 리포트 매치가 전부 일반 영어 관용구("an old one"/"the old one", 신격 존재와
  무관)이거나, 코덱스 자체의 "고대인" 표현(용어집 주석이 명시적으로 "문맥에 따라 조정
  가능"이라 허용).
- **Floran**(floranDescription 필드): 바닐라 스타일 플로란 3인칭 어눌한 말투 원문을 자연스러운
  한국어 서술로 완전히 재구성한 것이라 "플로란"이라는 단어 자체가 한국어 쪽에 없어도 정상.
- **Trink**("MEGA-TRINK"): 무기/장비 모델명으로 영문 그대로 보존하는 기존 관례(다른 무기 모델명
  보존과 동일 원칙), 종족명 Trink와 무관.
- **Spooked**: "안 놀랐다"/"겁먹었다" 둘 다 올바른 어간(겁먹-)의 자연스러운 활용형/부정형이라
  금지된 "추격당함"이 아님 — 상태이상 라벨 고정 표기와 별개로 대사체에서는 허용되는 변형.
- **One-Handed**: "~: 한 손으로 사용." 태그 문구가 해당하는 모든 아이템에서 이미 완전히
  일관되게 쓰이고 있고, 용어집 주석이 규정한 "명사 앞 관형 표기" 상황(예: 한손검)이 아니라
  서술형 태그 문맥이라 규칙 범위 밖으로 판단.
- **Fuel Hatch**("연료 주입구" vs 용어집 "연료 해치"): 3건 전부 `aphroditesbow`/
  `sexbound_reassembler`/`sexbound_runicassembler` 등 성인 콘텐츠 UI 제목에 한정되어 있어,
  "주입구"가 의도된 이중적 의미(성적 뉘앙스)의 말장난일 가능성이 높다고 판단해 임의로 덮어쓰지
  않고 보류. 필요시 사용자 확인 후 처리.
- **Miniknog Stronghold**(57건, "지식부 요새"): 여전히 미해결 판단 보류 항목.

## 2026-09-28 (6차): 아이템 이름/설명 전수 용어집 검수 — 텔레포터 + 용어 불일치 배치2·3 (합계 350자산)

사용자 지시: "특정 그룹은 필요없고, 아이템 이름/그 아이템의 설명을 우선순위로 모두 검수하는
수밖에 없습니다. 앞으로 딱히 문제나 그런게 없으면 품질을 우선해서 지침과 용어집을 참조하고
검수를 계속하세요." — 5차의 STYLE_MIX 대사 뱅크 전수 검토를 중단하고, 아이템명/설명 중심
`translation_glossary.tsv` 고정 용어(rule=fixed) 일치 여부로 우선순위 전환. 이후 명백한 사고
없는 한 승인 대기 없이 계속 진행.

**도구**: `qa_pak_glossary.py` — `pak_pairs.tsv`의 모든 EN/KO 쌍에 대해 `rule=="fixed"`인
용어집 행을 전수 대조, `qa_pak_glossary_report.tsv`로 위반 후보 출력. `extract_pak_pairs.py`로
pak이 바뀔 때마다 `pak_pairs.tsv` 재추출 필요.

**알려진 한계(신규 발견, 미해결)**: `.patch` 자산 59,013개 중 약 3,680개(~6%)는 `test`/`replace`
쌍이 없는 "플랫" JSON 구조(`[{op:"replace",...}, ...]`)를 쓰는데, `extract_pak_pairs.py`의
`iter_pairs()`가 이 구조를 감지 없이 건너뛰어 `pak_pairs.tsv`/`qa_pak_glossary_report.tsv`
양쪽에 사각지대가 생긴다(`protectorateflagpole.object.patch`의 "수호령의" 오표기를 수작업
대조 중 우연히 발견해서 알게 됨 — 해당 리포트에는 전혀 안 잡혀 있었음). 원시 바이트
스캔+재귀 JSON 치환 방식의 수정 스크립트들은 이 구조에도 영향을 받지 않으므로 실제 수정에는
지장 없으나, **탐지/리포트 단계**만 이 자산군을 못 본다는 점은 후속 세션에서 참고할 것.

**텔레포터 용어 통일**: "순간이동 장치" 40건 → "텔레포터"(용어집 고정). 원시 바이트
선필터+재귀 치환으로 패치 구조 무관하게 전수 반영(`fix_teleporter_glossary.py`). 서버 검증
통과. 백업: `...bak-20260928-preteleporterfix`.

**용어 배치2(265자산)**: Poptop(팝탑→팝톱), Drahl(드라흘→드랄), Vaash(바시→바쉬),
Thelean(텔리안/델레안→텔레안), Centens(센텐/센텐즈→센텐스, 조사별 분리 처리 + 센텐시아→
센텐시안 표기 통일), Peacekeeper(평화유지군→피스키퍼), Protectorate(프로텍토레이트/보호령/
수호령→보호국), Elithian Alliance(엘리시아 동맹/엘리시안 연합/엘리시안 동맹→엘리시안
얼라이언스). `fix_glossary_batch2.py`. 서버 검증 통과(`[Error]` 0). 백업:
`...bak-20260928-preglossarybatch2`.

**용어 배치3(249자산)**: Assault Rifle(어설트 소총/어설트 라이플/어썰트 라이플/돌격 소총
(공백)→돌격소총), Grenade Launcher(유탄발사기→유탄 발사기, 공백 삽입), Erchius(에르치우스/
얼치어스→에르키우스), Novakid(노바킨/노바킨드→노바키드), Saturnian(새터니언→새터니안),
Telebrium(텔레브리움→텔레브리엄), Hymid(히미드→하이미드), Enerth Engineering(에네르스
엔지니어링→에너스 엔지니어링 음역 수정 + 에너스 공학→에너스 엔지니어링 용어 통일),
Parry 단독형(카타나 패리/독성 패리→…패링, "패링 창" 등 Parry Window 용례는 미변경).
`fix_glossary_batch3.py`. 서버 검증 통과. 백업: `...bak-20260928-preglossarybatch3`.

이 배치에서 함께 처리한 판단이 필요했던 2건:
- **Kappa**: 용어집은 "Kappa→캇파"(youkai 종족, "카파로 쓰지 않는다")로 고정하지만,
  `atprk_krakothtextkappa.item.patch`의 "K'Rakoth Codex Kappa"는 실제로는 해당 코덱스
  시리즈의 그리스 문자 챕터 명명 규칙(Alpha..Omega)이라 종족명이 아님 — "카파" 그대로 유지,
  변경하지 않음. 실제 종족 트레이트 텍스트("카파 수리 키트" 2건)만 "캇파"로 수정.
- **Two-Handed**: 4개 자산(`ffs_cultist_broadsword`, `ffs_police_baton`, 바닐라
  `meleeslash.weaponability.patch`, `z4shadowsword`)의 `/description`이 전부 원문
  "A powerful two-handed sword."와 무관한 "강력한 즉석 무기."(improvised weapon의 오역)로
  되어 있던 명백한 오역 버그(용어 불일치가 아니라 콘텐츠 오류). 용어집의 Two-Handed→양손
  관형 규칙과 pak 내 기존 관례("강력한 검", crossedge)를 참고해 "강력한 양손검."으로 수정.
- **Aeginian Federal Union / Aeginian 어간 충돌**: pak 안에 "Aeginian"을 가리키는 어간이
  세 가지 공존(아에기니안 39건 최다수·아이기니안 1건 오타·에지니안 19건·에지족 18건).
  최다수인 "아에기니안"은 Aegi 용어집 행이 명시적으로 금지한 "아에기"(구형, 사용 금지) 위에
  지어진 형태라, 사용 빈도가 아니라 용어집의 명시적 금지를 따라 이미 존재하던 올바른 어간
  "에지니안"(관형)/"에지족"(종족 명사)으로 통일. "Aeginian Federal Union" 복합어는 어느
  변형(아에기니안/아이기니안/에지니안 + 연방/연방 연합/유니온/유니언)으로 나타나든 전부
  용어집 고정 표현 "에지족 연방 연합"으로 통일. AGENTS.md의 "용어 충돌처럼 판단이 필요한
  경우" 조항에 해당하나, 용어집의 명시적 금지 지시가 이미 존재해 실질적으로는 용어집 준수
  문제로 판단해 별도 확인 없이 진행함.

**남은 작업(다음 세션 승계)**:
- "Miniknog Stronghold"(57건, "지식부 요새")가 "Miniknog→미니크녹" 고정 규칙의 허용 가능한
  지명 예외인지, 통일해야 하는지 판단 미결 — 이번 세션에서는 보류.
- 위 "플랫 패치 구조" 사각지대의 근본 해소(예: 기저 자산과 diff해 EN 문맥 복원) 여부는
  아직 미착수.
- 아이템명/설명 전수 검토(용어집 기계 대조를 넘어선 품질 문제, 예: Two-Handed 같은 콘텐츠
  오역)를 계속 이어간다.

## 2026-09-28 (5차): 전체 pak 대상 문맥/어조 QA 1차 — 실제 콘텐츠 손실 버그 2건군 + 오타 1건 발견·수정

사용자가 인게임 플레이 중 "약간 심각한 문장이 많다"고 지적, "사방에 흩어져 있으니 체계적으로"
재검수해 달라고 요청. 2026-09-28 1차 재검수의 방법론적 교훈(`translations/*.tsv` id 기반 검증은
무효, 완성된 pak을 직접 까야 함)을 전체 규모로 확장 적용.

**도구**: `extract_pak_pairs.py`(배포 중인 `mods/female_translation.pak`의 모든 `.patch` 자산에서
test/replace 쌍 182,157건을 `pak_pairs.tsv`로 추출) + `qa_pak_context.py`(구
`qa_context_review.py`를 6,700행 한정에서 전체 182k행으로 일반화: STYLE_MIX/UI_LENGTH/
LITERAL/DUP_PARTICLE/TRUNCATED/UNTRANSLATED 6개 휴리스틱 분류, `qa_pak_context_report.tsv`).

**휴리스틱별 결과 (매우 중요 — 다음 재검수에 승계할 방법론적 결론)**:
- **UNTRANSLATED(22)**: 전부 오탐. 무기 코드명 등 의도적 영문 유지, 또는 `strip_deco()`의
  대괄호 제거 정규식이 번역된 대괄호 내용까지 지워버려 EN/KO가 우연히 같아 보인 아티팩트.
- **LITERAL(175)**: 전부 오탐. "그것은/이것은"류 패턴이 정상적인 한국어 서술문에도 극히
  흔해 변별력이 없었음 (원래 `qa_context_review.py`가 6,700행 소규모에서 특정 기지 오역
  문구 몇 개를 잡을 때는 유효했지만, 182k행 전체에 그대로 확장하면 노이즈만 남음).
- **DUP_PARTICLE(737)**: 전부 오탐. "가가/이이/을을/은은/도도/만만" 등이 "누군가가",
  "외톨이이기도", "마을을", "은은하다", "속도도", "만만찮다" 같은 정상 단어의 부분 문자열과
  우연히 일치.
  - 이 세 카테고리(UNTRANSLATED/LITERAL/DUP_PARTICLE)는 **폐기** — 전체 pak 규모에서는
    신호 대 잡음비가 너무 낮아 재사용 가치가 없다.
- **STYLE_MIX(142개 자산군, 7,413행)**: 표본 확인 결과 대부분이 실제 버그가 아니라, 한 NPC
  대사 config 파일 안에 애초에 화자·말투가 다른 여러 인사말 뱅크(예: `viera.config`의
  `default`/`viera`/`human` 그룹, 장로·마을 주민·방랑자별 다른 말투)가 공존하도록 설계된
  구조였음. 이 카테고리는 자동 판정 불가 — 사람이 각 그룹을 읽어야 하며, 전수 검토는 다음
  세션 이후로 이월(아래 "남은 작업" 참고). 다만 이 표본을 읽는 과정에서 **아래 커맨드먼트
  오타를 우연히 발견**함(휴리스티드 매치가 아니라 육안 검토로 발견 — 이 카테고리의 잠재
  가치를 보여주는 사례).
- **TRUNCATED(62, en 시각 길이 120자 이상인데 ko가 35% 미만인 경우)**: 대부분 오탐(한국어가
  원래 영어보다 압축적이라 생기는 정상적 밀도 차이)이었으나, 육안 대조로 **실제 콘텐츠
  손실 버그 2건군**을 확정:
  1. **`/items/aichips/nonEKIaichip.item.patch`의 `aiData/shipStatus/0~3/text` 4건**: 함선
     AI 칩의 상태 보고 대사가 전부 "$ status"(또는 그 번역 "$ 상태") 프롬프트 줄만 남고
     뒤따르는 실제 대사(최대 5문장)가 통째로 유실돼 있었다. index 0은 첫 줄조차 번역되지
     않은 상태였다. 4건 전부 원문 맥락(고장→불안정→비행 가능→완벽)에 맞춰 기존 같은 칩의
     다른 대사와 톤을 맞춘 캐주얼체로 새로 번역해 반영.
  2. **"^red;Destroyed when broken." 경고문 누락 8건**: `sb_techstation` 7종족 변형
     (apex/avian/floran/glitch/human/hylotl/novakid) + `letheia_extra_21` 오브젝트에서
     설명문 뒷부분의 파손 경고 문장이 통째로 빠져 있었다(동일 원문을 쓰는 텔레포터 계열
     17건은 정상 반영되어 있어 대조가 됨). 기존 텔레포터 항목이 쓰는 표현("파괴하면
     부서집니다.")을 그대로 이어 붙여 8건 모두 수정.
  - 두 버그군 모두 `fix_content_drop_bugs.py`로 수술적 패치, 수정 전 정확한 기존(손상된)
    값과 일치하는지 `assert`로 검증한 뒤에만 덮어써 오적용 위험 없음. 서버 부팅 검증
    통과(`0.0.0.0:21025`, `[Error]` 0건). 백업:
    `replaced-installed-20260922/female_translation.pak.bak-20260928-precontentdropfix`.
- **커맨드먼트 오타 1건(2개 자산에 중복)**: `/codex/angel/angellore11.codex.patch`와
  `angellore5.codex.patch`의 "계명 3"이 "너는 항상 컬티베이터를 따르기라."로, 존재하지 않는
  활용형("따르기라")이었다(다른 계명들은 전부 정상적인 "-여라/-말라/-라" 명령형 어미 사용).
  "따르라"로 수정. `[가-힣]기라` 패턴 전수 검색으로 확정(다른 3건은 "조작기라...", "키우기라"
  등 정상적인 명사+라 구성이라 제외). `fix_commandment_typo.py`로 반영, 서버 검증 진행 중.
  백업: `replaced-installed-20260922/female_translation.pak.bak-20260928-precommandmentfix`.

**STYLE_MIX 추가 진행 (같은 세션 내 이어서 완료)**: `/cinematics/`·`/quests/` 하위 65개 자산군
(약 450행)을 전부 육안 검토했다(퀘스트/시네마틱은 대사가 단일 화자 위주라 `/dialog/`류 NPC
인사말 뱅크보다 실제 버그가 있을 확률이 높다고 판단해 우선 처리). 결과: 앞서 발견한
`따르기라` 오타 외 **신규 확정 버그 0건**. 확인한 "말투 혼재" 표시는 전부 다음 중 하나로 설명됨:
- 시네마틱은 원래 여러 캐릭터가 등장해 각자 다른 말투로 말하는 게 정상(예: 다이텐구/울프
  시리즈, 셀레스티알 시네마틱의 텐시·이쿠 대화).
- 퀘스트 설명(`scriptConfig/descriptions/*`)은 항상 명령형("~하세요/~해라")이라 화자의 대사
  톤과 자연히 다름 — 프로젝트 전체의 일관된 관례이지 결함이 아님.
- `fetchthecommontoy`류 3종 종족별 템플릿(플로란 "엇" 말버릇, 글리치 감정 접두사)은 문서화된
  종족별 말투 합성 규칙(`docs/batch_log.md` 25절 PREFIX_KO)에 따른 의도된 설계.
- `sgsiegebreakermission.questtemplate.patch`의 "^orange; 시지브레이커. ^reset;" 앞뒤 불필요한
  공백·마침표는 **원문 자체의 기존 결함**(`'Destroy ^orange; Siegebreaker. ^reset;'`)을 구조
  그대로 반영한 것이라 번역 버그가 아님(원문을 건드리지 않는 관례상 그대로 둠). 다만 같은
  자산 안에서 "Siegebreaker"가 한 곳은 의역(공성파괴자), 다른 두 곳은 음역(시지브레이커)으로
  갈린 사소한 표기 불일치가 있음 — 영향이 작은 부차 퀘스트라 우선순위 낮음, 필요시 후속 처리.

**남은 작업 (다음 세션 승계)**:
- STYLE_MIX 나머지 77개 자산군은 전부 `/dialog/*.config` 형태의 대형 NPC 대사 뱅크
  (`alta.config` 734행, `atprk_relicseekercrew.config` 540행, `viera.config` 1,364행(확인
  완료) 등)로, 표본 확인 결과 이런 뱅크는 원래 한 파일 안에 종족·개인별로 다른 말투가
  공존하도록 설계되어 있어 자동 판정이 불가능하고 실제 버그 적중률도 낮다(지금까지 정독한
  약 450+1,364행에서 확정 버그 0건). 시간 대비 효율이 낮으므로, 사용자가 특정 문장·NPC를
  짚어주면 그것부터 표적 확인하는 방식을 권장. 전수 육안 검토가 필요하다면 다음 세션에 이어간다.
- 이번 5차 QA는 `female_translation.pak`에 **이미 병합된** 콘텐츠만 대상으로 했다. NonEKI는
  별도 스팬 편집 파이프라인(`repack_noneki_translation.py`, 아직 미실행)이라 이 스캔에
  포함되지 않았을 가능성 — NonEKI 자체 pak도 별도로 같은 방식(추출+휴리스티브) 재검토 필요.
- `pak_pairs.tsv`/`qa_pak_context_report.tsv`는 작업 폴더에 남겨 두었으니, 다음 세션은
  재추출 없이 바로 STYLE_MIX 리뷰를 이어가면 된다(단, pak이 갱신됐으므로 이어가기 전
  `extract_pak_pairs.py` 재실행 권장).

## 2026-09-28 (4차): `zz_localeko_*_low_20260927.pak` 4종을 `female_translation.pak`에 병합

2026-09-28 (3차) 시점의 "남은 작업" 4번(zz_localeko_elithian/krakoth/nuggubs/plushbound_low
4개를 female_translation.pak에 병합, README 관례상 "새 번역 전량은 female_translation.pak으로
통일" 원칙 미이행 상태 해소)을 처리.

**병합 전 충돌 검사**: 4개 low pak 총 1,624개 고유 자산 경로 중 1,558개가 `female_translation.pak`과
겹쳤다. 두 표본(`akkimaricrate.object.patch` 등)을 직접 까본 결과 이 겹침은 전부 **같은 파일의
서로 다른 JSON 포인터**(종족별 `*Description` 필드)를 건드리는 것으로, `.patch` 자산이 독립된
patch-group 리스트(`[[{test},{replace}], [{test},{replace}], ...]`)라 그룹 단위로 안전하게
이어붙일 수 있는 구조였다. 전수 스크립트 검사로 **1,558개 공유 경로 전체에서 JSON 포인터 레벨
충돌 0건**을 확인한 뒤 병합 진행(단순 덮어쓰기였다면 기존 female_translation.pak 쪽 번역이
유실됐을 것 — 실제로 테스트 표본 하나는 여기서 기존 13개 그룹을 덮어쓸 뻔했다가 병합 방식으로
전환).

`merge_low_paks.py`(patch_female_translation_pak.py와 동일한 SBAsset6 저수준 writer 재사용)로
patch-group 리스트를 연결(concat)해 병합: 겹치는 1,558개 자산은 그룹 합치기, 겹치지 않는 66개
자산은 그대로 추가. 결과: 58,996 → 59,062개 항목(78.1MB). 병합 후 전체 `.patch` JSON 유효성
재검증 — 사전에 이미 알려진 무관한 결함 2건(`/dialog/colourful.config.patch`,
`/dialog/spacehero.config.patch`, 병합 이전 원본 pak에도 동일하게 존재)만 남고 신규 결함 0건,
`\r\r` 잔존 0건. 무작위 표본 눈으로 직접 확인해 그룹 합치기가 정확히 적용됐음을 재확인.

기존 `mods/female_translation.pak`을
`translation/replaced-installed-20260922/female_translation.pak.bak-20260928-premerge_low`로
백업 후 교체. 병합된 4개 pak은 `translation/replaced-installed-20260922/low_paks_merged_20260928/`로
이동(더 이상 `mods/`에 두면 중복 적용). `zz_localeko_highpriority_20260927.pak`은 이번 병합
대상이 아니었으므로(README 어디에도 미병합 상태로 지적된 적 없음) `mods/`에 그대로 유지.

`win64/starbound_server.exe`로 재검증(타임아웃 없이 완주 대기 — 이전 시도에서 `timeout 60`으로
자산 로딩 도중 서버가 강제 종료된 실수가 있었음, 재발 방지 차 기록): `0.0.0.0:21025` 리스닝 도달,
`[Error]` 0건(기존에 알려져 있던 K'Rakoth `nitrogendeep`/`player.config` 크래시 계열도 이번
로그에는 나타나지 않음 — 원인 미조사, 이번 병합과는 무관해 보임). 로그:
`logs/merge_low_verify2.log`.

**남은 확인 사항**: 4개 low pak의 용어집 위반 163건(2026-09-28 1차 재검수에서 발견, 대부분
Teleporter→"순간이동 장치")은 아직 실제로 female_translation.pak에 정정 반영되지 않았다 —
이번 작업은 구조적 병합만 수행했고 용어 정정은 별도 작업으로 남아 있다.


## 2026-09-28 (3차): 전체 pak 대상 "다른 치명적 오류" 전수 스캔 — 플레이스홀더 손상 87건 발견·수정

사용자 지시("다른 치명적 오류 없는지 다른 번역도 살펴보죠")로, 이번엔 `translations/*.tsv`가
아니라 **실제로 배포되는 `mods/female_translation.pak` 자체**를 `test`/`replace` op 쌍
174,095개 전수 대상으로 구조 스캔(개행 수, PUA/TAG/PLACEHOLDER/INPUT 토큰 멀티셋, `\r\r`
잔존, `<...>` 브래킷 내 한글 혼입)했다. 결과, 사용자가 우려한 "다른 치명적 오류"가 실제로
더 있었다:

1. **`<slots>` 런타임 플레이스홀더가 TM(번역 기억) 충돌로 하드코딩된 정적 숫자로 교체된
   버그, 총 63건.** 원문 `<slots> SLOTS`는 상자/액체 탱크마다 실제 용량이 런타임에 치환되는
   템플릿인데, `alignment/sbkor.tsv` 정렬 단계에서 chest60/chest64 두 자산에만 개별 번역이
   있었고 나머지 chest9~chest666(41개) + liquidtank9~liquidtank300(22개), 총 63개 서로 다른
   용량의 상자/탱크가 전부 "슬롯 60칸"(chest60의 값)으로 잘못 통일돼 있었다 — 즉 300칸
   상자도 UI에 "슬롯 60칸"이라고 표시될 뻔했다. `슬롯 <slots>칸`(플레이스홀더 보존, 기존
   translation_memory.tsv에 count=2로 이미 기록돼 있던 정답 후보)으로 전량 수정, 오답
   후보(`슬롯 60칸`/`슬롯 64칸`, count=1)는 `translation_memory.tsv`에서 제거, `alignment/
   sbkor.tsv`의 chest60/chest64 원본도 함께 수정해 재발 방지.
2. **`<role>` 플레이스홀더가 "<역할"(닫는 `>` 누락 + 한글 번역)로 깨진 버그, 18건.**
   선원 계급 목록(`Trainee Apprentice <role>`, `Last-Minute <role>`)에서 다른 43개 계급은
   전부 `<role>`/`<field>`를 정상 보존했는데 이 2개 계급만 태그 자체를 한글로 오역해 실제
   게임에서 "수련생 견습생 <역할"처럼 깨진 문자열이 그대로 노출될 뻔했다. `<role>`로 복원.
3. **`<selfname>` 플레이스홀더 오역, 4건.** Floran 하녀/관리인 대사 3건("<자기이름>")과
   Novakid 관리인 대사 1건("<자명>")에서 태그 자체가 한글로 번역돼 있었다. `<selfname>`으로 복원.
4. **존재하지 않는 가짜 태그 삽입, 1건.** `ct_plasmasword`의 `/altAbility/name`은 원문이
   평범한 "Energy Aura"인데 번역이 "<원소명> 오라"로 없는 플레이스홀더를 만들어냈다.
   "에너지 오라"로 수정(형제 항목 "Enhanced Energy Aura"→"강화된 에너지 오라"와 통일).
5. **퀘스트 진행도 플레이스홀더 오역, 1건.** `gic_rsr_hakurei_kikan` 퀘스트의 조건 설명에서
   `<itemName>`/`<current>`/`<required>`(아이템명·진행도 실시간 치환 태그)가 전부 한글로
   번역돼 있어 진행도 텍스트가 깨져 나올 뻔했다. 태그를 보존하며 자연스러운 어순으로 재번역.

총 87건을 `patch_female_translation_pak.py`와 동일한 수술적 방식(기존 pak의 해당 op만
치환)으로 수정, 매 단계 JSON 유효성·`\r\r`·태그 보존 재검증 후 `mods/female_translation.pak`
교체(백업: `.bak-20260928-prechestfix`, `.bak-20260928-pretagfix`), `starbound_server.exe`
부팅 검증에서 관련 오류 0건 확인. 전수 스캔에서 그 외 발견된 `<...>` 패턴(수백 건)은 전부
원문 자체도 장식용 꺾쇠 괄호를 쓰는 정상 사례(예: "< HEVIKA ORDIS, Confidential >",
`<Causes a specific sound when activated.>` 등)로 확인, 오탐 처리.

**남은 과제**: `apply_rest.py`의 `run_repacks()`(NonEKI류 raw-text span-edit 경로)에도 동일한
`\n`→`\r\n` 이중 변환 버그가 있어 미리 수정해 두었으나(해당 WORK 디렉터리가 현재 없어 실제
피해 범위는 확인 불가), 이 경로가 다시 사용될 때 재확인 필요. `missed_worklist.tsv`/
`rest_worklist.tsv` 원본 소스(번역 완료된 20만+ 쌍)에 대한 전수 플레이스홀더 스캔은 이번에
`female_translation.pak`을 통해 간접적으로 이미 수행됐다(위 174,095쌍 스캔에 전부 포함).

## 2026-09-28 (2차): worklist_new(batch) 고우선순위 그룹 정밀 수정 + 치명적 파이프라인 버그 발견

1차 재검수(아래 기록)에서 "고우선순위 재검수 다 했는지" 질문에 답하며 남겨뒀던 실제 작업을
이어서 완료. 대상은 사용자가 명시한 진짜 고우선순위 그룹 `worklist_new.tsv`→
`translations/batch_*.tsv`(6,700 논리행, codex/shortdescription/questtemplate 포함) 전량.

**1) qa_all.py/fix_batch_stray_lines.py의 "헤더 오인" 버그 발견·수정.** `elithian/krakoth/
nuggubs/plushbound_*.tsv`는 실제 `id\tkorean` 헤더가 있지만 `batch_*.tsv`/`missed_*.tsv`/
`rest_priority_*.tsv`/`rest_*.tsv`는 헤더가 전혀 없고 첫 줄부터 진짜 데이터(id=구간 시작
번호)다. 기존 스크립트가 무조건 `header = next(r, None)`으로 각 파일의 첫 줄을 먹어버려서,
49개 batch 파일 각각의 "구간 시작 id"(0, 80, 200, 340...)가 항상 허위로 "누락"으로 잡혔다.
`qa_all.py`는 첫 줄이 숫자 id로 시작하면 헤더로 취급하지 않도록 자동 판별하게 수정, 실제
"진짜 누락"만 재계산한 결과 **188개 허위 누락 중 187개가 이 버그였고, 진짜 누락은
`batch_5360_5499.tsv` 파일 자체가 완전히 빈 파일(140행, GiC 총기 언로드/아이템/코덱스
텍스트 위주)이었던 것 하나뿐**이었다. 140행 전량 신규 번역해 채움.

**2) 실제 콘텐츠 유실 구조 버그 2건 수정.** id 1020(북 아이템 "''편집증.''")에서 후속
`^orange;상호작용해 읽습니다.^reset;` 안내문이 통째로 누락되어 있었음 — 다른 45개 동일
패턴 항목과 대조해 표준 문구로 복원. id 1440(청산염 팩 아이템)에서 `^red;- Causes Cyanide
Poisoning.` 경고 줄이 통째로 누락 — "청화물 중독을 유발합니다."로 복원.

**3) 용어집 위반 대규모 발견·수정 (고우선순위 코덱스/로어 텍스트 위주).** 가장 심각한 건은
세력명 불일치: `Protectorate`(용어집 고정="보호국")가 "보호단"/"보호령" 두 가지 다른 오역으로
수십 개 코덱스·대사 항목에 흩어져 있었고, `United Systems`(고정="연합 시스템", "연합 체계"
표기 금지라고 용어집에 명시)가 "유나이티드 시스템즈"(음역) 또는 금지어 "연합 체계"로 쓰이고
있었다. 전량 "보호국"/"연합 시스템"으로 통일(조사 결합도 재검증, 3건 수정). 그 외
DEF(방어율/방어→방어력, 33건), Archetype(원형→아키타입, 16건), One-Handed/Two-Handed
태그 표기(반각 띄어쓰기 정규화 "(한 손)"→"(한손)" 등, 12건), Shortsword(단검/단도→소검,
용어집이 Dagger의 "단검"과 명시적으로 구분하라고 지시), Shield Bash(방패 밀치기/방패 돌진→
방패 강타, 용어집이 명시적으로 금지한 표현), Saturnian(토성인→새터니안), Hylotl(하일로틀→
하이로틀 — 이번 세션에서 직접 채운 gap-fill 번역 자체의 오타였음), Magilock/Portal/The
Ruined/Alt Fire/Sniper Rifle 표기 등 총 130여 건 수정. `worklist_new(batch)` 그룹의
`qa_all.py` gloss_issues는 190→58로, struct_issues는 38→36으로 감소(잔여 58건은 One-Handed/
Two-Handed의 자연스러운 산문 형용사 용법 등 확인된 허위 양성).

**4) 가장 중요한 발견 — 빌드 파이프라인 자체의 CSV 파싱 버그로 인한 대규모 텍스트 손상.**
`apply_new_translations.py`/`refresh_translations.py`의 `load_korean()`이 `translations/
batch_*.tsv`를 **CSV 인용 규칙을 전혀 이해하지 못하는 순수 정규식 라인 파서**
(`re.match(r"^(\d+)\t(.*)$", line)`)로 읽고 있었다. 다중 문단(개행 포함) 항목은 CSV
표준에 따라 따옴표로 감싸 저장되는데, 이 파서는 그 따옴표를 그냥 텍스트의 일부로
읽어버려 **번역문 맨 앞/맨 뒤에 리터럴 `"` 문자가 그대로 박혀 게임에 출력될 뻔했다**
(예: `gic_nazrin_planetencounter_undercolony_sicario.cinematic`의 대사가
`"히트맨이자 ... 증명하라."` 형태로 저장돼 있었음, 확인용 pak-직접-추출로 발견).
`batch_*.tsv` 전체에서 개행을 포함한 행이 1,190개— 즉 코덱스/로어처럼 긴 문단일수록
이 손상에 취약했다. 두 스크립트의 `load_korean()`을 `csv.reader` 기반으로 교체하고
`refresh_translations.py`를 재실행해 **`translation-overlays-20260921/source-v3/`의
기존 패치 1,324개 항목을 실제로 수정**, `apply_new_translations.py`를 재실행해 누락돼
있던 신규 38개 항목(청산염 팩 포함)도 새로 병합. 재실행 후 `want/updated/missing-file`이
모두 0으로 수렴해 `source-v3`가 현재 `batch_*.tsv`와 완전히 동기화됐음을 확인.
NonEKI 대상(`noneki_new_targets.tsv`, 443행)도 같은 버그의 영향권이었으나 재생성 후
따옴표 오염 0건 확인.

**5) `mods/female_translation.pak` 재조립 완료 (당초 우려했던 블로커 해소).**
`build_pak.py`가 요구하는 `E:/pakx/*`/`E:/ft_src`/premerge pak 스테이징 경로는 여전히 복구하지
못했지만(`E:/Desktop/mods/...`가 `translation/replaced-installed-20260922/`로 이미 이동해
있었고, 그 안의 `localeko_*_legacy.pak`/`-9998_trans_sbkor...pak`/`FU_KO_...pak`/
`zz_localeko_postload.pak`/`female_translation-premerge.pak`은 찾았으나 `E:/ft_src`는 끝내
찾지 못함), 대신 **훨씬 안전한 대안**을 택했다: 전체 재조립 대신 현재 배포 중인
`mods/female_translation.pak`을 베이스로 두고 `source-v3`의 GiC/Black Armory/Extended Story
3개 오버레이 디렉터리 내용만 해당 경로에 그대로 덮어써 넣는 **수술적 패치 스크립트**
(`patch_female_translation_pak.py`)를 새로 작성. sbkor/FU_KO/postload 등 손대지 않는 나머지
레이어는 원본 pak에서 바이트 그대로 유지되므로 데이터 손실 위험이 없다.

이 과정에서 **두 번째 잠재적 손상 버그를 추가로 발견**: `apply_new_translations.py`/
`refresh_translations.py`의 `value = kor.replace("\n", "\r\n") if "\r\n" in actual else kor`
로직이, `translations/batch_*.tsv` 안에 이미 리터럴 `\r\n`으로 저장돼 있던 항목(36개 파일,
5,009건)에 대해 `\n`→`\r\n` 치환을 무조건 적용해 `\r\r\n`(캐리지리턴 중복)을 만들어내고
있었다. `kor.replace("\r\n","\n")`으로 먼저 정규화한 뒤 변환하도록 두 스크립트를 모두 수정,
재실행으로 1,069건 추가 수정 확인, 전체 `source-v3`에 `\r\r` 잔존 0건 확인.

패치 스크립트 실행 결과: 기존 pak 58,970개 항목 중 **3,654개 항목 교체 + 26개 신규 항목
추가**, 총 58,996개 항목의 새 pak(76.6MB) 생성. 새 pak을 `Pak`으로 직접 재파싱해 전체
`.patch` 항목의 JSON 유효성(사전 존재하던 무관한 결함 2건 제외 전부 정상)과 `\r\r` 잔존
0건을 재확인한 뒤, 기존 pak을
`translation/replaced-installed-20260922/female_translation.pak.bak-20260928-precorrection`로
백업하고 `mods/female_translation.pak`을 교체. `win64/starbound_server.exe`로 부팅 검증—
`female_translation.pak` 및 4개 `zz_localeko_*_low_20260927.pak` 로딩 관련 오류 0건, 유일한
치명적 오류는 기존에 이미 확인된 무관한 `/player.config`(RPG_contents_1115920474.pak 기원)
크래시뿐임을 재확인.

**남은 블로커**: `E:/ft_src`의 정체(원래 이 레이어가 담고 있던 고유 콘텐츠가 있었는지)는
끝내 확인하지 못했다 — 다만 오늘 수술적 패치는 `source-v3`의 3개 GiC/BA/ES 오버레이만
반영하는 방식이라 `ft_src`가 담당했을 다른 콘텐츠(있었다면)는 이번 갱신에 포함되지 않았을
수 있다. `repack_noneki_translation.py`(NonEKI 전용 별도 파이프라인,
`NonEKI_9_FU_compat_translated.pak`)도 이번 세션엔 실행하지 않았다. 4개
`zz_localeko_*_low_20260927.pak`을 `female_translation.pak`에 통합하는 작업도 미착수.

## 2026-09-28: 신규 번역 전체 체계적 재검수 (1차) — 기존 유저번역(sbkor/FU) 제외 전량 대상

Plushbound 완주 직후, 사용자 지시로 "우리가 이번 프로젝트에서 새로 번역한 모든 것"(기존
유저번역 sbkor/FU 제외)에 대한 체계적 재검수를 시작. 범위: Elithian/K'Rakoth/nuggubs/Plushbound
(4대 완주 모드, 약 8,500행), `worklist_new.tsv`→`translations/batch_*.tsv`(9,876원본행/6,700
논리행, **codex 111 + shortdescription 1,736 + questtemplate 445 포함 — 사용자가 지정한진짜
고우선순위 그룹**), `missed_worklist.tsv`→`missed_*.tsv`(8,333행), `rest_worklist.tsv`→
`rest_priority_*.tsv`/`rest_*.tsv`(11,353행, 파일 수 기준 약 2,279개).

### 방법론적 교훈 (가장 중요, 다음 재검수 세션에 반드시 승계할 것)

- **`translations/*.tsv` 배치 파일의 "id" 컬럼으로 대응 worklist와 직접 비교하는 QA는
  `rest_worklist.tsv` 계열에는 통하지 않는다.** `rest_worklist.tsv`는 프로젝트 기간 동안최소
  3회(128,808건→19,847건→현재 11,353건) 재생성되었고, 재생성될 때마다 남은 후보의 id 번호가
  전부 다시 매겨진다. 반면 `translations/rest_*.tsv`/`rest_priority_*.tsv`는 작성 당시의스냅샷
  id를 그대로 갖고 있어, 지금의 `rest_worklist.tsv`와 id로 맞춰보면 완전히 무관한 영어·한국어
  쌍이 매칭된 것처럼 보인다(실제로 30개 무작위 표본 중 대다수가 "완전히 다른 문장"으로 나타나
  한때 "게임이 이미 망가졌다"고 오판할 뻔했다).
  - **실제 게임에 적용하는 `apply_rest.py`(`load_en2ko()`)는 id가 아니라 영어 원문 텍스트
    자체를 키로 삼아 매칭**하며(`{"op":"test","path":ptr,"value":영어원문}` 가드 포함, 값이 일치하지
    않으면 패치가 조용히 미적용됨), 그래서 id 번호가 흔들려도 최종 결과물(`female_translation.pak`)
    자체는 무사한 경우가 대부분이다.
  - **결론: 앞으로 이런 배치의 품질은 반드시 "완성된 pak을 직접 까서" 검증한다.** `pak.py`의
    `Pak` 클래스로 `.patch` 자산을 읽어 `[{"op":"test",...},{"op":"replace",...}]` 쌍을추출,
    무작위 표본(또는 전수)으로 EN/KO 쌍의 내용 일치 여부를 사람이 직접 눈으로 확인하는 방식만
    신뢰할 수 있다. `translations/*.tsv`의 raw id 매칭 결과는 참고용일 뿐 확정적 증거가아니다.
  - 실측: `female_translation.pak`은 58,921개 `.patch` 자산·200,887개 test/replace 쌍을담고
    있으며, 30개 파일(수십 개 쌍) 무작위 표본 전수 확인 결과 **오매칭 0건** — 실사용 pak은 건강하다.
    Teleporter 용어도 전체 1,503건 중 1,501건이 정상 `텔레포터`(예외 2건은 무관한 문맥의오탐).

### 완주 4대 모드(Elithian/K'Rakoth/nuggubs/Plushbound) 재검수 결과

- 구조 QA(태그/개행/플레이스홀더/PUA 글리프): Plushbound 1건(id 1169, 기존 예외) 제외 전부 0건.
- 용어집 위반: Elithian 59, K'Rakoth 46, nuggubs 34, Plushbound 24(총 163건) — 대부분
  `Teleporter`→"순간이동 장치"(정식 용어 `텔레포터` 미사용). 단, 실제 활성 `female_translation.pak`
  표본 검사에서는 이 용어가 정상 노출되고 있어(위 방법론 참고), 이 4개 `zz_localeko_*_low_*.pak`은
  아직 `female_translation.pak`에 병합되지 않은 **별도 오버레이 pak**이므로 직접 재검사가 필요했다.
  4개 pak을 무작위 표본으로 까본 결과 전부 EN/KO가 정상적으로 대응됨을 확인(오매칭 없음).
- **조사(助詞) 불일치 버그 발견 및 수정 (신규, 이번 재검수의 핵심 성과)**: Plushbound 작업 중 용어를
  `미니크노그`→`미니크녹`, `노바킨`→`노바키드`로 전량 치환할 때, 받침 유무가 바뀌면서 뒤에 붙는
  조사(은/는, 이/가, 을/를, 과/와)가 문법적으로 깨진 경우가 다수 발견됨(예: "노바키드은"— 노바키드는
  받침 없는 모음 종결이라 "노바키드는"이 맞음). `translations/*.tsv` 전체(elithian/krakoth/nuggubs/
  plushbound/batch/missed/rest 등 61+143개 파일)를 정규식으로 스캔해 75건(노바키드 11 +미니크녹
  64) 전량 수정. `build_elithian_overlay.py`/`build_krakoth_overlay.py`/`build_nuggubs_overlay.py`/
  `build_plushbound_overlay.py` 4개를 재빌드해 반영 완료(행 수 변화 없음: 2350/2098/2064/1990),
  재빌드된 pak에서 "노바키드는" 등 올바른 조사로 적용됐음을 직접 확인.

### `worklist_new.tsv`→`translations/batch_*.tsv` (진짜 고우선: codex/아이템/퀘스트, 6,700행)

- **stray line 손상 발견 및 복구**: 다중 줄(문단 구분 `\n\n`) 원문을 번역하면서 CSV 따옴표 처리 없이
  그냥 개행만 넣어, 한 항목이 id 없는 "고아 줄" 여러 개로 쪼개져 있었다(예: id18의 3줄짜리 번역이
  `18\t[]` / 빈 줄 / `^orange;상호작용해 읽습니다.^reset;` 세 물리 줄로 분리). 48개 파일에서
  3,116개 고아 줄을 원래 항목에 병합 복구(`fix_batch_stray_lines.py`, 백업:
  `drafts/batch_backup_20260928/`). 복구 전 구조오류 1,201건이 복구 후 53건으로 급감(대부분
  가짜 오류였음이 확인됨).
- 남은 53건 전수 확인 결과 실제 버그는 **`[CRIT]`/`[ALT]` 키바인드 태그 오역 20건뿐**이었다
  (예: `[치명타]`가 실제로는 게임이 표시하는 리터럴 UI 토큰 `[CRIT]`이어야 함). 11개 파일에서
  `[치명타]`→`[CRIT]`, `[보조(아이템)? | X]`→`[ALT | X]`로 38건 치환해 수정 완료, 잔존 0건 확인.
  나머지(lines 10건, tags 9건, glyphs 13건)는 전부 검토 결과 거짓양성으로 판정:
  - lines: 영문 원문의 임의 줄바꿈(가독성용 소프트랩)과 한국어 자연스러운 재배치 줄바꿈수가
    다를 뿐, 문단 구분(`\r\n\r\n`) 개수는 10건 전부 원문과 정확히 일치함 — 정상.
  - tags: Core Booster류처럼 한국어 어순 재배치로 `^orange;`를 한 번 더 열어야 했던 의도적
    조정(9건 중 확인한 표본은 전부 정당함), 혹은 원문 자체의 깨진 `^reset;` 누락을 한국어에서
    바로잡은 기존 관례(`qa_structure.py`의 `KNOWN_OK` 25930/63264와 동일 패턴).
  - glyphs: id 6456~6468 등, 원문이 PUA 아이콘 폰트 글리프로 된 "가짜 외계 문자" 아이템명을
    의미만 한국어로 옮긴 것 — Plushbound id1169와 동일한 기존 예외 유형.
- **아직 미해결**: 188행 완전 미번역(수정 안 함), `missed_worklist.tsv`(8,333행 중 4,131행 미착수,
  이 안에 codex/아이템급 콘텐츠가 얼마나 섞여 있는지 미확인), 이 그룹(2,292건 고우선 부분집합)을
  실제 `female_translation.pak`에서 표적으로 표본 검증한 적은 아직 없음(전체 pak 무작위표본에
  일부만 우연히 포함됨).

### 남은 작업 (다음 세션 이어서)

1. `worklist_new`/`batch_*` 미번역 188행 번역.
2. `missed_worklist.tsv` 미착수 4,131행 — codex/아이템 비중 파악 후 우선순위 결정.
3. `worklist_new`/`batch_*`의 고우선 부분집합(codex 111/shortdescription 1,736/questtemplate 445)을
   `female_translation.pak`에서 표적 표본 검증(현재는 전체 pak 무작위 표본만 수행됨).
4. `zz_localeko_elithian_low_20260927.pak`/`zz_localeko_krakoth_low_20260927.pak`/
   `zz_localeko_nuggubs_low_20260927.pak`/`zz_localeko_plushbound_low_20260927.pak` 4종을
   `female_translation.pak`에 병합(README 관례상 "새 번역 전량은 female_translation.pak으로 통일"
   원칙 미이행 상태) — 병합 전 `female_translation.pak`과 겹치는 자산 경로가 있는지 충돌검사 먼저.
5. `rest_*.tsv`/`rest_priority_*.tsv`는 id 기반 재검수가 근본적으로 불가능하므로, 앞으로는
   완성된 pak을 직접 까서 표본(또는 전수) 검증하는 방식만 사용할 것 — 위 "방법론적 교훈"참고.

## 2026-09-28: Plushbound 완주 (1,990/1,990)

nuggubs' Mega Mod 완료 후 우선순위 1위였던 Plushbound(`contents_2959854988.pak`)의 봉제인형/오락실
가구 등 종족별 설명을 `plushbound_low_worklist.tsv` 순서대로 100줄 단위 배치로 전량 번역완료.

- 번역 파일: `translations/plushbound_0000_0098.tsv` ~ `plushbound_1900_1989.tsv` 전체
  (id 0~1989, 1,990행)
- 오버레이 팩: `mods/zz_localeko_plushbound_low_20260927.pak` (`build_plushbound_overlay.py`로 빌드,
  339개 대상 애셋, 683,394 bytes, 1990행 반영)
- **검증 절차 변경(사용자 지시)**: 배치마다 서버 부팅 검증하던 기존 방식을 중단하고, 전량 번역 완료
  후 단 한 번만 빌드+검증하는 방식으로 전환. 이후 배치(id 199~1989)는 서버 부팅 없이 번역만 진행.
- 신규 종족: North Dragnar / Big North Dragnar(북방 드라그나르) — 영문 원문이 "v/w" 치환사투리를
  쓰는 캐릭터라, 한국어는 사투리 재현 대신 짧고 무뚝뚝한 서술체로 처리(글로서리 160행 기본 규칙).
  이 외 Faahri/Harpy/Skeleton/Vampire/Limako/Peglaci/Faunodyne 등 선례 없는 종족은 자연스러운
  한국어(가상 사투리 없음) 기본 규칙 적용.
- **용어집 오류 발견 및 전량 정정** (사용자 지적): 배치 작성 중 아래 세 용어를 글로서리와 다르게
  써서 전 배치에 걸쳐 `sed` 일괄 치환으로 수정함.
  - `미니크노그` → `미니크녹` (`translation_glossary.tsv` 158행, fixed)
  - `노바킨` → `노바키드` (`translation_glossary.tsv` 146행, fixed; 기존 번역 68건 전부 `노바키드`만 사용)
  - `재배자` → `컬티베이터` (`translation_glossary.tsv` 201행, Cultivator, "경작자/재배자 금지" 명시)
- **구조적 실수와 복구**: id 1900~1989 구간을 번역하며 파일명/행 번호를 한 차례 잘못 매겨(오프셋
  착오로 id를 100 정도 밀려서 라벨링), 그 여파로 id 1801~1899(99건)가 통째로 누락되는 사고가 있었음.
  `plushbound_low_worklist.tsv`와 번역 파일 전체를 대조하는 커버리지 스크립트로 발견해
  `plushbound_1801_1899.tsv`로 별도 보완, `plushbound_1900_1989.tsv`는 올바른 id로 재작성.
  최종적으로 worklist 1,990건 = 번역 1,990건, 결측/중복 0건 확인.
- 구조 QA(태그/개행/플레이스홀더/PUA 글리프, `qa_structure.py` 로직을 plushbound용으로 즉석 이식해
  실행): 1건만 플래그(`id 1169`) — 원문 자체가 `` 같은 깨진 아이콘 글리프를
  포함한 손상된 문자열이라 자연어로 의역 처리한 기존 예외. 그 외 이상 없음.
- **서버 부팅 검증 미완료**: 최종 빌드 후 `win64/starbound_server.exe`로 1회 부팅 시도했으나
  `RPG_contents_1115920474.pak`의 몬스터 패치 실패와 그로 인한 `/player.config` JSON 파싱 오류로
  기동 중 크래시함(`logs/plushbound_final_verify.log`). 동일 오류가 이번 세션 훨씬 이전
  시점(`logs/plushbound_batch4_verify.log`, Plushbound id 199 단계)에도 이미 있었던 것으로 확인되어,
  **Plushbound 번역과 무관한 기존 모드팩 문제**로 판단. 사용자 확인 후 원인 조사는 다음세션으로 이월.
- `scan_remaining.py`의 `load_coverage()`에 `zz_localeko_plushbound_low_20260927.pak` 추가 후
  재스캔 완료 — 잔여 저우선 백로그는 **11,353건**(유니크 영문 기준). 다음 최우선 대상은
  Enternia(1,604) → Neki(1,404) → Angel(1,379) → Voided(567).
- 다음 작업: `plushbound_low_worklist.tsv`의 id 199부터 이어서 번역 (최대 id 1989)

## 2026-09-27: nuggubs' Mega Mod 저우선순위 완주 (2,064/2,064)

K'Rakoth 완료 후 우선순위 1위였던 nuggubs' Mega Mod(`contents_2735634052.pak`)의 오브젝트/가구/
포스터/봉제인형 등 종족별 상호작용 설명(`floranDescription`, `nekoDescription`, `avaliDescription`,
`laustaurDescription` 1건 등)을 `nuggubs_low_worklist.tsv` 순서대로 100줄 단위 배치 21회로 전량
번역 완료했다.

- 번역 파일: `translations/nuggubs_0000_0099.tsv` ~ `nuggubs_1998_2063.tsv` (총 21개 파일 + 누락분
  보정 파일 `nuggubs_0797_fix.tsv` 1건, 총 2,064행)
- 오버레이 팩: `mods/zz_localeko_nuggubs_low_20260927.pak` (445개 대상 애셋에 대한 `.patch` 오버레이,
  `build_nuggubs_overlay.py`로 빌드)
- 매 배치 후 서버 부팅으로 `[Error]` 0건 및 리스닝 마커 확인 (`logs/nuggubs_batch*_verify.log`,
  최종 검증은 `logs/nuggubs_final_verify.log`)
- 스타일: 신규 등장 종족 Felin(새침하고 캐주얼한 고양잇과), Neko(귀여운 "~냥/냐/먀" 말투),
  Neki(수줍고 머뭇거리는 말투), Avali(이 모드에서는 무덤덤하고 초연한 1인칭), Slimeperson(덤덤한
  캐주얼체)을 확립했고, 기존 종족은 sbkor 관례 그대로 준수
- 중간 CSV 멀티라인 인용 처리(id 776)로 인해 오프셋이 한 칸 밀리면서 id 797 한 행이 최초배치에서
  누락됐던 것을 재스캔으로 발견해 `nuggubs_0797_fix.tsv`로 보정
- `scan_remaining.py`의 `load_coverage()` 체크 목록에 `zz_localeko_nuggubs_low_20260927.pak` 추가
- 다음 저우선 대상: Plushbound(`contents_2959854988.pak`, 1,990) → Enternia(1,604) → Neki(1,404) →
  Angel(1,379) → Voided(567) 순

## 2026-09-27: K'Rakoth Mod 저우선순위 완주 (2,098/2,098)

Elithian 완료 후 우선순위 2위였던 K'Rakoth Mod(`contents_2604255131.pak`)의 종족별
아이템/오브젝트/퀘스트 설명(`floranDescription`, `glitchDescription`, `anneliskDescription`,
`fenronDescription`, `noolithDescription` 등, 신규 커스텀 종족 Annelisk/Fenron/Noolith 포함)을
`krakoth_low_worklist.tsv` 순서대로 100줄 단위 배치 21회로 전량 번역 완료했다.

- 번역 파일: `translations/krakoth_0000_0098.tsv` ~ `krakoth_1999_2097.tsv` (총 21개 파일, 2,098행)
- 오버레이 팩: `mods/zz_localeko_krakoth_low_20260927.pak` (387개 대상 애셋에 대한 `.patch` 오버레이,
  `build_krakoth_overlay.py`로 빌드. Elithian과 동일하게 기존 팩과 병합하므로 배치마다 통째로
  재빌드해도 안전)
- 매 배치 후 서버 부팅으로 `[Error]` 0건 및 리스닝 마커 확인 (`logs/krakoth_batch*_verify.log`,
  최종 검증은 `logs/krakoth_final_verify.log`)
- 스타일: 커스텀 종족은 글로서리 기본 규칙(160행) 적용 — Annelisk(아넬리스크)는 지친/사업가형/캐주얼한
  1인칭, Fenron(펜론)은 실용적/약간 불안한 1인칭, Noolith(노올리스)는 학구적/호기심 많은1인칭,
  자연스러운 한국어 "-다"체·구어체 혼용. 기존 종족(플로란/글리치/노바킨드 등)은 sbkor 관례 그대로
  준수(플로란 3인칭·쉿소리 제거, 글리치 "[한 단어]. [문장]." 패턴 등)
- 고유명사: K'Rakoth → "크라코스", Ri'shaan → "리샨"(= 폐허/Ruin), Fenerox → "페네록스",
  Deadbeats → "데드비츠", Erchius → "에르키우스" 로 통일 (TM에 아직 없던 항목이라 이번 배치에서 확정)
- 퀘스트 turnInDescription(마지막 1행, id 2097)은 `^orange;이름^reset;` 색상 태그를 유지한 채
  자연스러운 한국어 어순으로 재배치
- `scan_remaining.py`의 `load_coverage()` 체크 목록에 `zz_localeko_krakoth_low_20260927.pak` 추가
- 재스캔 결과 잔여 백로그 17,505 → 15,407 유니크 문자열로 감소
- 다음 저우선 대상: nuggubs' Mega Mod(`contents_2735634052.pak`, 2,064) → Plushbound(1,990) →
  Enternia(1,604) → Neki(1,404) → Angel(1,379) → Voided(567) 순

## 2026-09-27: Elithian Races Mod 저우선순위 완주 (2,350/2,350)

`docs/priority_allocation_20260927.tsv`에서 저우선 최대 항목이었던 Elithian Races Mod의종족별
아이템/오브젝트 설명(`akkimariDescription`, `avikanDescription`, `drodenDescription` 등)을
`elithian_low_worklist.tsv` 순서대로 100줄 단위 배치 10회로 전량 번역 완료했다.

- 번역 파일: `translations/elithian_0000_0099.tsv` ~ `elithian_2299_2349.tsv` (총 24개 파일, 2,350행)
- 오버레이 팩: `mods/zz_localeko_elithian_low_20260927.pak` (453개 대상 애셋에 대한 `.patch` 오버레이,
  `build_elithian_overlay.py`로 빌드. 재실행 시 기존 팩과 병합하므로 배치마다 통째로 재빌드해도 안전)
- 매 배치 후 서버 부팅으로 `[Error]` 0건 및 리스닝 마커 확인 (`logs/elithian_batch*.log`,
  최종 검증은 `logs/elithian_final_verify.log`)
- 스타일: 종족별 기존 관례 준수 — 플로란 3인칭/쉿소리 제거, 글리치 "[한 단어]. [문장]."패턴,
  아키마리(아키) 자기지칭 + 자연스러운(비-broken) 한국어, 그 외 종족(아비칸/트링크/드로덴/노바킨드 등)은
  평서체 "-다" 기본, 원문에 드러난 성격만 반영
- 퀘스트 turnInDescription(마지막 51행, id 2299~2349)은 `^orange;이름^reset;` 색상 태그를 유지한 채
  "~에 있는 ~에게 돌아가라/보고하라/찾아라" 어순으로 자연스럽게 재배치
- `scan_remaining.py`의 `load_coverage()` 체크 목록에 `zz_localeko_elithian_low_20260927.pak` 추가
  (누락 시 이미 번역된 Elithian 텍스트가 다음 스캔에서 다시 미번역으로 오탐됨)
- 다음 저우선 대상(우선순위 테이블 기준): K'Rakoth Mod(2,098) → nuggubs' Mega Mod(2,064)→
  Plushbound(1,990) → Enternia(1,604) → Neki(1,404) → Angel(1,379, 주로 angeldescription) 순

## 2026-09-27: `scan_remaining.py` 재검증 버그 3종 수정 + 고우선 배치 1건 적용

이전 세션들의 "저우선 큐 완주(잔여 0건)" 기록은 **`scan_remaining.py`의 커버리지 판정 버그** 때문에
실제보다 훨씬 적게 잡힌 착시였다. 사용자가 Angel 종족 모드를 대표 사례로 지목해 재검증을요청했고,
다음 세 버그를 찾아 고쳤다(`scan_remaining.py` 자체를 수정, 원본 그대로 유지):

1. `load_coverage()`가 활성 번역 pak `mods/female_translation.pak`을 아예 확인하지 않고,이미 병합되어
   사라진 `localeko_gic_legacy.pak` 등 3개 pak만 찾고 있었다.
2. `female_translation.pak`의 패치 문서는 `[[test,replace], ...]`처럼 그룹이 한 겹 더 중첩된 배열인데,
   커버리지 로더는 평평한(flat) 배열만 인식해 58,920개 중 4건만 커버리지로 잡았다.
3. 모드 자체 경로 대소문자(`/items/MATERIALS/...`)와 번역 오버레이가 기록한 경로 대소문자
   (`/items/materials/...`)가 달라 문자열 완전일치 비교가 실패했다(Starbound 파일시스템은
   대소문자를 구분하지 않는데 비교 코드는 구분하고 있었음).
4. (부수 발견) 색상 태그 `^#09ff00;` 안의 16진수가 "영문 단어 있음" 판정에 걸려, 순수 글리치/아이콘
   대사 줄까지 미번역으로 오분류됐다. `text_only()` 헬퍼로 마크업·PUA 글리프를 제거한 뒤판정하도록
   수정.

재스캔 결과 추이(고유 영문 후보): 113,304 → (버그1 수정) → 24,437 → (버그3 대소문자 수정) →
**19,860**. 우선순위 재분류 결과 실제 고우선(로어/퀘스트/대사/기본 설명) 잔여는 3,344건이 아니라
**92건**(146개 모드 중 14개 모드에 분산)이었다.

92건 중에서도 던전 `.json.patch`의 `value`가 통째로 JSON 문자열 블롭(`messageType`/`initialItems`
등 내부 파라미터)인 경우와 `objects/09 Storage/...`류 자산 경로 식별자는 추가 오탐으로 확인,
번역 대상에서 제외(스캐너 자체는 아직 이 두 패턴을 걸러내지 못하므로 다음 세션에서 일반화 필요).

실제로 번역해 적용한 것:
- `mods/zz_localeko_highpriority_20260927.pak`(신규 오버레이, 14개 자산·20개 op): Novakid Quest Mod
  텔레포트 확인창, FrackinUniverse 함선 상태줄, Starforge 조수 자원명, Stargate Invasion행성 3종
  코크핏 텍스트, Project Redemption 무기 2종 업그레이드명, FU-Redemption 방어구 세트 보너스 5종.
- `mods/Craftable_Seeds_FU_1.1_compat.pak` 스팬 편집 재패킹: `/player.config.patch`의 묘목
  shortdescription 13종(16개 위치, `"/-` 배열 추가 연산이라 위치 기반 오버레이 불가 — NonEKI와
  동일한 사유로 원본 pak 텍스트를 직접 치환).
- 검증: `logs/highpriority_verify.log` — `0.0.0.0:21025` 리스닝 도달, `[Error]` 0건.

도구: `write_pak.py`(SBAsset6 신규 pak 작성기, 케이스 보존), `build_highpriority_overlay.py`,
`repack_craftable_seeds.py`. `docs/priority_allocation_20260927.tsv`에 모드별 고/저우선집계.

다음 세션 작업: 저우선 19,769건(대부분 Elithian/K'Rakoth 계열/Plushbound/Enternia/Neki/Angel의
종족별 부가 설명 텍스트에 집중, `docs/priority_allocation_20260927.tsv` 참고)을 이어서 배치 번역.

## 작업 정리 (2026-09-25)

배치 0359~0370의 번역 600개(배치당 50개)를 재대조했다. ID 중복과 초안·TSV 불일치는 없었고,
구조 QA는 0건, 용어 QA는 기존 오탐 4건만 남았다. 완료 TSV는 `translations/`에 유지하고
초안 JSON 13개와 긴 항목 생성 스크립트 1개는 `drafts/0359_0370/`로 옮겼다. 다음 작업은
`rest_priority_0371.tsv`의 첫 항목 ID 106641부터다.

## 배치 기록 (최신순)

### 문맥·관례 재검수 (2차, 전 코퍼스)

- 종족 말투 정규화: 플로란 금지 장음(`~해애` 등) 전 코퍼스 0건, `-다` 관례 종족 해체→`-다` 변환
  6,156건, 천사 `~군요/네요` 변환 1,317건, 네키 `~다냥` 6건 보정. 잔여 장음은 실어휘·울음소리만 확인.
- 글리치 감정 접두사 비명사형 11건 교정(`안 놀람.`→`태연함.` 등). `분석 중.`은 레거시 관례라 유지.
- 고정 용어 위반 2회 일괄 교정(총 336행): `히로틀`→`하이로틀`, `순간이동기·순간이동 장치`→`텔레포터`,
  `러슬링`→`러스틀링`, `미니크노그`→`미니크녹`, `팝탑`→`팝톱`, `숏소드·쇼트소드·단도·단검`→`소검`(문맥별),
  `그랜드 프로텍터·대수호자`→`대보호자`, `오카수스`→`오카서스`, `평화유지군`→`피스키퍼`,
  `에스터`→`에스더`, `카파`→`캇파`, `사우모스`→`타우모스`, `사투르니안·새터니언`→`새터니안`,
  `테렌 보호국`→`행성 보호국`, `트링키언`→`트링크`, `아에기·에기·에이기`→`에지`,
  `에르치우스·얼치어스`→`에르키우스`, `쿠에투스`→`콰이어투스`, `텔레브리움`→`텔레브리엄`,
  `제르케시움`→`제르세슘`, `마기록·마지록`→`매지락`, `마법탄·매직샷`→`매지샷`,
  `지식부 요새`→`미니크녹 요새`, `연합 체계`→`연합 시스템`, `MEGA-TRINK`→`메가 트링크`,
  `루인 킬러`→`루인킬러`, `제작 스테이션`→`제작대`, `사용 가능 재료`→`재료가 있는 것만 보기`,
  `관통 피해`→`찌르기 피해`, `패리`→`패링`, `타격 보호막`→`피격 방패`, `어설트`→`돌격` 계열,
  `이지설트`→`에지솔트`, `게아신`→`기트신`, `[CORPORATE KAPPA TRAIT]`→`[캇파사 특성]`,
  `[Corpo Kappa]`→`[캇파사]`, `융합실`→`핵융합로`, `뼈 가공 스테이션`→`뼈 세공대`,
  `가죽 작업대`→`가죽 세공대`, `나뭇잎족·잎-사람들`→`잎사귀 종족`.
- 플로란 3인칭 자칭 누락 6건 복원(`Floran heard...` → `플로란이 들었다` 등).
- 용어 QA 잔여 5건은 오탐으로 기록: `Spooked` 동사 용법 2건(`겁먹었다`/`겁먹지 않는다`),
  JSON 아이템명 `lustlingView-codex` 1건, 산문 형용사 `unexplored`→`미개척` 1건,
  `the ruined city`→`폐허가 된 도시` 대소문자 무시 매칭 1건.
- QA: 구조 0건, 용어 0건(오탐 제외), 중복 원문 불일치 0건.
- 후속 비-말투 스윕: 미번역 영어 문장 잔존 1건 교정(123921 마지막 줄),
  숫자 불일치 1건 교정(34598 `600HP`→`600` 오기), 종족명 통일 `아르카니아(인)`→`아르카니안` 11행.
- 라틴 문자 잔존 전수 스캔: 치환자(`<selfname>` 등)·총기 규격·약어·라틴어 인용·외계어·곡명·JSON 셀은 관례상 보존 확인.
- `<...>` 대명사 토큰 누락 14건은 전부 한국어상 자연스러운 생략으로 판정(유지).
- EN `?`/KO 무`?` 42건·KO `?`/EN 무`?` 59건은 수사의문·의문 어미라 의미 손실 없음(유지).
- 글리치 감정 접두사 누락 0건, `[...]` 괄호 수 불일치 1건(83026은 원문 잘못된 `]`라 KO에서 제거가 정상).
- 표본 40건 원문 대조 이상 없음. 참고: `batch_*`/`missed_*`/`rest_*`/`rest_priority_*`는
  서로 독립된 ID 번호 체계라, worklist EN 매핑은 `rest_priority_*`에만 유효함.

### 최종 재검수 (0889~1088 전체 19,917건)

- 자동 스윕: EMPTY 0 / 원문 동일 0 / 모지바케 0 / 리터럴 이스케이프
  전부 원문 미러 확인 / 태그·줄바꿈 불일치 0.
- 고정 용어 위반 교정: `재배자`→`컬티베이터` 18건(내 배치),
  `루인`→`루인드` 1건(118200), `아끼마리`→`아키마리`, `포탈`→`포털`,
  `러스트링`→`러스틀링` 내 파일 25건 + 구형 batch 파일 7건.
- `tesseract`: 117584 `정사입방체`→`테서랙트`로 관례 통일.
- 플레이스홀더: 122011 `[욕설]`→`[expletive]` 원문 토큰 보존으로 교정.
- 문장부호: 119354, 77824, 77825 의문형 `?` 보존으로 소폭 수정.
- `아끼` 잔여분은 전부 동사 '아끼다' 용법이라 예외 처리(변경 없음).
- 표본 40건 원문 대조: 종족 말투·용어 정상 확인.
- QA: 구조 0건, 내 파일 용어 위반 0건.

### 1088 (121056~128789, 80건) — 큐 최종

- 'undead of Felheim'~'Trink were well designed' 대사.
- 표기: 펠하임, 자완, 아우라니아, 우프, 키츠네, 하프시,
  스펙트윙, 흙성게, 니아, 랄프, 아르카니안, 트링키언.
- NL1 행(121377, 124499, 124501, 124508~125902): 실제 줄바꿈 인용 셀 유지.
- QA: 구조 0건.
- **저우선 큐 완주: 잔여 0건.**

### 1087 (119805~121025, 100건)

- 'looks pretty silly'~'nice and cool' 대사.
- 표기: 미야오 노리, 무시, 욜로틀, 욘누르, 아리오스톤, 길텐,
  헤비카, 비오니아, 워프드, 카렐, 엘리멘탈 하트.
- QA: 구조 0건.

### 1086 (119379~119804, 100건)

- 'bug blue'~'some kind of reference' 대사.
- 표기: 솔라레이, 악티아스, 울파르, 베스퍼, 야바, 세테르니아,
  얼터니아, 니아 칵테일, 섀도우 소울, 러스틀링.
- QA: 구조 0건.

### 1085 (118950~119375, 100건)

- 'modify my mech'~'monitor it all' 대사.
- 표기: 아이언워치, 베이터, 바이오니드, 비르마, 포이,
  아야 에센스, 아야 펀치, 대천사 크세퀴즈리엘.
- 용어 일괄 수정: 고정 용어 위반분 `재배자` 18건을 `컬티베이터`로 교체
  (rest_priority_1029~1082), 118200 `루인`을 `루인드`로 교정.
- QA: 구조 0건, 내 파일 용어 위반 0건.

### 1084 (118543~118949, 100건)

- 'Why would I'~'customize weapon abilities' 대사.
- 표기: 에스더 브라이트, 체리스톤, 악티아스, 루멘 과일, 팝탑,
  마이크로포머, 유물 수집가, 크라코탄, 마기사이트.
- QA: 구조 0건.

### 1083 (118333~118542, 100건)

- 'Ocassus banner'~'flyin' box' 대사.
- 표기: 오카수스, 레트룬, 돌리, 프록, 언바운드, 아넬리스크.
- 118494(NL1): 원문이 실제 줄바꿈을 포함한 인용 셀. 리터럴
이 아닌
  실제 줄바꿈 인용 셀로 맞춤(구조 QA 재확인 0건).
- QA: 구조 0건.

### 1082 (118062~118332, 100건)

- 'snowy planets'~'tall person' 대사.
- 표기: 와일드캣, 파놉티콘, 드레이, 아쿠올라이트, 모니카, DOC 하사.
- 118311 원문 끝 따옴표 불일치는 원문 그대로 미러.
- QA: 구조 0건.

### 1081 (117702~118060, 100건)

- 'not meant to find'~'grassy highlands' 대사.
- 표기: 프랙툴, 기어톤, 잡색 브리처, 일루미네이트,
  나노선반, 착색기, GZN-5-에메텍스트라.
- QA: 구조 0건.

### 1080 (117051~117701, 100건)

- 'tough door'(1078 누락분 보충)~'power-consuming' 대사.
- 표기: 대황폐, 달바위, 기트신, 누미, 오카수스,
  에르키우스, 윈드스웹트, 오리지늄, 정사입방체.
- QA: 구조 0건.

### 1079 (117122~117429, 99건)

- 'looking at'~'mushroom wardrobe' 대사. 117051은 1078과 중복 제외.
- 표기: 낸지, 와즈, 프록, 왕관 라크리마, S.I.X.,
  뇌설, 별천지(starnation), 헤일로.
- QA: 구조 0건.

### 1078 (116980~117105, 100건)

- 'great idea'~'creatures running in cold' 대사.
- 표기: 시악사(커먼스 시티 여신), 부리씨앗, 에로스,
  시네가트, 페네록스.
- 참고: 파일 첫 행 BOM으로 병합 카운트 99로 표시, 실제 100건.
- QA: 구조 0건.

### 1077 (116807~116979, 100건)

- 'grounded-no-more'~'esteemed artist' 대사.
- 표기: 커먼스 시티, 바르다스, 글립, 미니크노그.
- QA: 구조 0건.

### 1076 (116359~116806, 100건)

- 'Weak pull sword'~'plush could kill me' 대사.
- 표기: 텔헌터, 헥, 섀도우 봉제인형, 프로젝트 45.
- 감정 접두사: Weak→약함., Weary→지침., Weird→기이.
- QA: 구조 0건.

### 1075 (115610~116357, 100건)

- 'Warped plantss vicious'~'Weak plant eaten' 대사.
- 표기: 타이탄코프, 천사의 영역, 아케인 툰드라,
  본부, 헤븐송, 펠하임, 발더, 코타츠, 비에라.
- 감정 접두사: Wary→경계., Watchful→주시.
- QA: 구조 0건.

### 1074 (114656~115609, 100건)

- 'Very good party cake'~'Warped chests niishu' 대사.
- 표기: 베스퍼, 라그나, 아우라니아, 바이올륨,
  초록빛 행성, 아유린, 스타페어러의 피난처, 텔레안,
  보봇, 니슈, 레다, 물질 조작기.
- 감정 접두사: Voracious→탐욕., Wanting→갈망.,
  Warned/Warning→경고.
- QA: 구조 0건.

### 1073 (113830~114654, 100건)

- 'Unnatural blocks'~'fulfilling tasty' 대사.
- 표기: 스타리 컬티스트, 유물 탐구자 텔레포터, ST 실렉티스,
  페닉스, 웜온치, 펠하임 군단, 발더, 크래스베리,
  헤비카, 니베라, 루네바, 아야스, 에니아, 덴드라리움,
  체이스플라이트, 스켈레톤 거울, 테크 카드.
- 감정 접두사: Unnerved→초조., Unsettled→동요.,
  Unsurprised→안 놀람., Uplifted→고양., Upset→속상.
- QA: 구조 0건.

### 1072 (113319~113722, 100건)

- 'Uh, that wasn't'~'Nooliths vessels' 대사.
- 표기: MKI, 네트리마, 니아 음료, 비신, 스트리지차,
  프록, 크라코스, 종점 세계, 태양화된, 영구동토.
- 감정 접두사: Unamused→재미없음., Uncertain→불확실.,
  Uncomfortable→불편., Understanding→이해., Uneasy→불안.,
  Unimpressed/Uninterested→무관심., Uninformed→무지.
- QA: 구조 0건.

### 1071 (112654~113316, 100건)

- 'Transfurrms glowy garrden'~'Unbound looking into the Tide' 대사.
- 표기: 트링키언, 롱프로드, 오카수스 크레딧, 노블 대위,
  언바운드, 타이드, 대주권 신전, 이층 침대.
- 감정 접두사: Trusting→신뢰.(신설).
- QA: 구조 0건.

### 1070 (112036~112653, 100건)

- 'To be honest'~'Transfurrms sparkly rocks' 대사.
- 표기: 새터니언, 타우모스, 나이트폴 이니셔티브,
  알터니아, 야라 뿌리, 누리스, 체리스톤, 투아우악,
  대주권 신전, 트랑기, 카다반, 터프 가이.
- 감정 접두사: Torn→갈등.(신설), Tranquil→평온.
- QA: 구조 0건.

### 1069 (111537~112029, 100건)

- 'Thiss café'~'lustling freezer' 대사.
- 표기: 쏜윙, 가시 반지, 잘린 의회, 땅에 사는 자들,
  헬리온, 호라이즌, 아트모스, 록조, 오메토나, 알루니카,
  기트신, 포스폴리온, 시간 방랑자, 더블룬, 락샤사.
- 감정 접두사: Thoughtful→사색., Thoughtfully→사색하며.,
  Thrilled→신나., Tired→피곤.
- QA: 구조 0건.

### 1068 (111406~111536, 100건)

- 'woofie flag location'~'find other parts' 대사. 후반부 플로란 'Thiss~' 다량.
- 표기: 드레드윙, 세테라이, 섀도우 종족, 프린시,
  안드로스 갈바넥 사령관, 일렉트로켐 시설, 그린핑거, 팔.
- QA: 구조 0건.

### 1067 (111187~111405, 100건)

- 'bed seems different'~'woofie flag' 대사.
- 표기: 파라데아 레전드, 야라지기, 우피, 프로젝트 45,
  미니크노그, 아발론, 센텐/센텐시안, 복제기, 모루.
- QA: 구조 0건.

### 1066 (111030~111186, 100건)

- 'teleporter quick route'~'advanced station mech parts' 대사.
- 표기: 우누스트렐로의 스타 카페, 점프게이트, 이소슬라임,
  다크슬라임, 루인, 센텐, 팝탑, 필멸자, 쿠포(모글).
- QA: 구조 0건.

### 1065 (110894~111029, 100건)

- 'table create simple dishs'~'teleporter quick route' 대사.
- 표기: 감시자(Avikan Watchers), 선봉대(Vanguard),
  S.A.I.L, 테크 패드, 클루엑스, 쿠포(모글), 대천사.
- QA: 구조 0건.

### 1064 (110731~110893, 100건)

- 'station call helpers'~'table screw head' 대사.
- 표기: 라데이스, 세텐난/센텐, 세퀘이즈리엘,
  크라코스, 데릭, 자동기계, 아보라이트, 헤일로,
  필멸자, 재배자, USCM, 밀짚 인형([E] 태그 보존).
- QA: 구조 0건.

### 1063 (110565~110730, 100건)

- 'sign pretty invitin''~'gheatsyn upgrade station' 대사.
- 표기: 아키마리, 스펙트윙, 메카, 반군 캠프,
  미니크녹 드론, 파워 큐브, 말라키, 프로그(신설),
  초코보, 크랄, 센텐, 고대인, 정지 포드, 트링키안,
  얼라이언스, S.A.I.L, 데이터매스, 기트신 파편.
- QA: 구조 0건.

### 1062 (110424~110564, 100건)

- 'holographic flag'~'falling crates sign' 대사.
- 표기: 아키마리, 히로틀, 코어 가루, 트링크,
  얼라이언스 통신망, 노바키드, 미니크녹, 반군 캠프,
  하피, 보호막 발전기, 메카 스테이션, 테라포밍,
  셔틀, 볼트로폴리스, 곰팡이 연구실.
- QA: 구조 0건.

### 1061 (110242~110423, 100건)

- 'purrticular dirt'~'Floran commander' 대사.
- 표기: 퓨터(네키), 포드 상자, 트링크, 얼라이언스,
  마지사이트, 미니크녹, 기트신, 생명/성장/지식/파멸 룬,
  생크틸라이트, 아야카, EDS, 비오니아 이형, 서킷.
- QA: 구조 0건.

### 1060 (110096~110241, 100건)

- 'plant created in lab'~'purrson looks gritty' 대사.
- 표기: 드레메톤, 아에기니안, 미니크녹, 반군,
  보호국, 알파카, EDS, 시타델 수호자, 모함 경비,
  수도 보안, 크레온 대사관, 아발리 특수부대, 루시,
  아넬리스크, 나나이트, 프리깃, 드리머 프로젝트,
  크라코스, 트링크, 호랑가시나무.
- QA: 구조 0건.

### 1059 (109910~110095, 100건)

- 'This one ain't flying'~'alta eco chamber' 대사.
- 표기: 비오니아, 바스 브할레이, 비오니드, 고대인,
  크라코스들, 재배자, 아비칸, 대보호자, 호박,
  부비트랩, 아발론, 에로스, 펭귄, 트링크,
  알타 젤리, 이세계 구조물, 역병 텍스트 조각.
- QA: 구조 0건.

### 1058 (109757~109909, 100건)

- 'This might be useful'~'old-fashioned clock' 대사.
- 표기: 무글, 밀주, 클루엑스, 아가란, 부리 쉼터,
  재배자, 아보라이트, 우프 본부, 기트신, 태양계
  (목성/화성/수성/해왕성/토성/태양/천왕성/금성),
  네코, 레테이아, 천사의 영역, 고 에이프, 크라코스,
  아발리, 초차원 구조물.
- QA: 구조 0건.

### 1057 (109614~109753, 100건)

- 'machine scan my eyes'~'metalpurrson' 대사.
- 표기: 마지사이트(매직사이트보다 다수 표기로 채택),
  마지사이트 웨이스톤/용광로, 비에라, 무글 쿠포,
  사우모스, 사투르니안, USCM, 메카, 아보라이트,
  우프, 천 개의 벚나무 행성(직역).
- QA: 구조 0건.

### 1056 (109491~109613, 100건)

- 'little box'~'machine made from human' 대사.
- 표기: 클루엑스, 티파, 헤비카 오르디스, 비오니아,
  우프, 선봉대, 게아룬, 슈퍼 트랄가 블래스터 2,
  반려동물 그림. 1051의 비오나→비오니아 수정.
- QA: 구조 0건.

### 1055 (109364~109489, 100건)

- 'lamp flower'~'little Floran' 대사.
- 표기: 칼린, 액티아스, 억제기, 유물 탐구자,
  나이트폴 랩터, 아보스, 커먼스 시티, 메이든,
  아비칸, 악마, 플로란 재봉 도구.
- QA: 구조 0건.

### 1054 (109176~109363, 100건)

- 'pretty advanced'~'lamp green light' 대사.
- 표기: 미니크녹 억제장(신설), 재배자, 루인,
  아비안 상징(불/공기/지구), 수호자, 보호국,
  초공간 드라이브 코어, 비신 칩 쿠키, 수정 쿠키,
  점프게이트, 펠하임, 키츠네 도리이, 클리(신설),
  코도릭, 고래왕(신설), 아트모스 급 신호등.
- QA: 구조 0건.

### 1053 (108978~109175, 100건)

- 'reinforced EDS drone dispenser'~'pizza' 대사.
- 표기: EDS, 세라핌, 솔라리움(무기 계열), 신성한 불꽃,
  히라키 코랄레, 빅 에이프, 노마다, 울파르, 기트신,
  야라 뿌리, 세터니아 코어, amf 아르게 상공회의소(신설),
  플러팔로(전기/얼음), 자매(알타 말투).
- QA: 구조 0건.

### 1052 (108805~108977, 100건)

- 'This here station SAIL'~'really odd bed' 대사.
- 표기: S.A.I.L, 쉘가드, 포획 포드, 무시, 정동석,
  오카서스, 레다 퓨르티아(신설), 플러팔로(일반/불/독/방사능),
  유물 탐구자, 카파, 미니크녹, 카이테란, 사투르니안,
  펠하임, 체리스톤, 히라키 코랄레, 싱크 수정(신설),
  인포매스(신설), 자철석, 클루엑스.
- QA: 구조 0건.

### 1051 (108656~108804, 100건)

- 'This girl familiar'~'This here station' 대사.
- 표기: 비오나, 엘리시아, 톤나 스플릿, 미니크녹,
  유물 탐구자, 니옥수, 니베라, 알테라시, 이오라 게라,
  하프시, EDS, 쉘가드, 대천사 세퀘이즈리엘,
  클레어 고프, 피터 아트모스, 록조, 브레이크크리에이트.
- QA: 구조 0건.

### 1050 (108497~108651, 100건)

- 'This fabric sheet'~'This giant shell' 대사.
- 표기: 미니크녹, 노바키드, 안드로스 갈바넥,
  피스키퍼 본부, 피스키퍼, 대보호자, 비행불가자,
  야라, 아비칸, 테르베, 벨린, 에이기, 호버바이크,
  알타, 기트신, 반란, 전 전대 대보호자(첫 비인간).
- QA: 구조 0건.

### 1049 (108307~108496, 100건)

- 'This disguise'~'This eye malevolence' 대사.
- 표기: 천사의 영역, 악마, 아발리, 러스트링, 센텐,
  아키마리, AAE, 코로플릭, 톤노바, 아콜릭, 아야카,
  니베라, 아주라, 리비라(신설), 비오노라, 야라,
  아이스 플러팔로, 카다반, 대탈출, 변방.
- QA: 구조 0건.

### 1048 (108161~108305, 100건)

- 'Unbound furniture'~'This dirt' 대사.
- 표기: 언바운드, 알타, 솔랄레이, 크라코스,
  텔헌터, 악마, 벨린의 시대, 포스포리온,
  비에라 굴, 그린핑거, 전초지, 테라마트.
- QA: 구조 0건.

### 1047 (108006~108160, 100건)

- 'This chest stripes'~'Unbound equipment' 대사.
- 표기: 초코보, 레테이아, 마이크로포머, 탈라소,
  아보스, 세일/S.A.I.L, 센텐, 언바운드, EDS,
  격리장, 프로보스키.
- QA: 구조 0건.

### 1046 (107877~108005, 100건)

- 'This can't be good'~'This chest ronin' 대사.
- 표기: 카나리아, 물질 조작기, 필멸자, 스코프,
  미니크녹, 펭귄, 기트신, 로닌, 아보라이트,
  아야카, 스타리스 아야카, 프로보스키(신설),
  피냐타(신설), 아발리, 센텐, 에이기.
- QA: 구조 0건.

### 1045 (107708~107875, 100건)

- 'This bed crudely made'~'This can transmute ore' 대사.
- 표기: 울루, 아발리, 사우모스, 스타리스, 벌꿀술,
  기트신, 미라, 텔헌터/텔, 감시자(아비칸), 잎-사람,
  고대인 유물, 네키 말투(purrtec/drr 등), 노바키드 구어.
- QA: 구조 0건.

### 1044 (107558~107707, 100건)

- 'This antenna'~'This bed insect butt' 대사.
- 표기: 보봇, 아야, 아르카니안, 다트 퀘스트,
  알타 젤리, 비온, 펜론, 크라코스, 미니크녹, 반군,
  이중주화, 바쉬, 쉘가드, 아발론, 에로스, 러스트링.
- QA: 구조 0건.

### 1043 (107305~107556, 100건)

- 'This Lucario flag'~'This animal skin' 대사.
- 표기: 루카리오, 러스트링, 물질 조작기, 필멸,
  노바키드, 펭귄, 파이오니어, 팝탑, 씨앗 제작기(신설),
  쉘가드, 스코프(신설), 텔레안, 트링키안, UFO,
  통합 얼라이언스 제작대, 선봉대, 웨이스톤, 쿠포포,
  빛직조(신설), 복제기, 드랄, 액티아스, 솔랄레이,
  로크 슬레이어, 비행불가자, 대나무, 점프소총,
  재배자, 파멸의 에너지, 클루엑스, 에테르.
- QA: 구조 0건.

### 1042 (107070~107304, 100건)

- 'They're like space dogs'~'This Lucario flag' 대사.
- 깃발 경유지 패턴(way point/bookmark/save) 삼종 관례 유지.
- 표기: 프로자, 첼시, 잘민, 라에나틴, 레트룬,
  볼트스피터, 셸비, 배터죠(신설), ASA-26 레인저,
  아키마리, 알타, 천사, 대천사 세퀘이즈리엘, 루인드,
  에이펙스, 미니크녹, 필멸자, 에이비언, 아비칸,
  센텐시안, 서킷, 커버넌트, 재배자, 드로덴, 공훈 토큰,
  파아리, 플로란, 길텐, 글리치, 대보호자, 그린핑거,
  인간, 히로틀, 인포스파이어, 크라코스/크라코탄,
  릴로돈, 루카리오, 조로(신설), 화성, 미드.
- QA: 구조 0건.

### 1041 (106824~107064, 100건)

- 'These spears'~'They're gigantic' 대사.
- 표기: 센텐시안, 흑요석, 히로틀, 물질 조작기,
  아키마리, 알터니아, 야라, EDS, 드라이/드론(개인 드론),
  에이펙스 반군, 눌리스, 태양 나방, 이온불 큐브(신설),
  엠버 산호, 깃털잎(featherfrond 신설), 타이드,
  조석 서리(신설), 중무장 피스키퍼, 뼈 트로피,
  나루토 달리기(밈 유지), '엉덩이튼' 말장난.
- QA: 구조 0건.

### 1040 (106643~106823, 100건)

- 'These don't seem'~'These spears' 대사.
- 표기: 야라 관리인, 트링크, 노틱스, 로크(Roc),
  로크 슬레이어, 태양 면(solar plane), 알테라쉬 정원,
  정동, 히로틀, 미니크녹, 언바운드, 새터니안,
  부유 수정, 에이비언, 선봉대, 타브리야, 소나 병사,
  레테이아, 에르키우스 유령, 진홍 정글, 분노 물약(신설),
  뒤틀린 숲, 타우모스, 보호국, 비신, 아키마리.
- QA: 구조 0건.

### 1039 (106405~106642, 100건)

- 'There's beetle larvae'~'These doctors' 대사.
- 표기: 노틱스, 물질 조작기, 에이펙스, 기만자,
  리프콜라, 재배자, 프랙툴, 셸비(SHELL-B→셸비 유지),
  메드스토어, 아키마리, 에세테라, 테라포머,
  야라열매(yaarings), 바르다, 스카바, 보호자,
  고대인들 유물, 비오니드 익족류, 아비칸 뼈 무기,
  코만도, 알타, 별이 빛나는 행성(Starry).
- QA: 구조 0건.

### 1038 (106178~106404, 100건)

- 'There are...'~'There's been a low-power' 대사.
- 표기: 은색 타이가(argent taiga 신설), 펠하임,
  텐리, 발데르, 에이비언, 리프콜라, 에이펙스 방송,
  핏빛 정글(sanguine jungles), 코리아(Kohria 신설),
  레테이아, 에르키우스, 루나, 식민지 증서,
  대보호자, 엘리시안 경제, 초코보, 모그리,
  에스더 브라이트, 비랄릭/균병(신설),
  생태 실, 차가새(coldbird 말장난).
- QA: 구조 0건.

### 1037 (105864~106176, 100건)

- 'The true masters'~'There are vines' 대사.
- 표기: 아이소슬라임, 소나베일, 테르브, 녹색빛 유적
  (verdant ruins), 플로라스톤, 테서랙트, 에이펙스,
  히로틀, 클루엑스, 피스키퍼 본부, 메가 조드(유지),
  아발리, 스타게이저, 텔레안 강습함, 위스퍼,
  무플릭, 아르코 연구원, 노바키드 메타 농담.
- 접두사: Theoretical.→이론적.(신설).
- QA: 구조 0건.

### 1036 (105620~105862, 100건)

- 'The size of this harpoon'~'The tribute platter' 대사.
- 표기: 텔헌터, 아키마리, 엠피리언, 스너겟, 아발리,
  탈라소, 태양계, 스타더스트, 레테이아, 애니머스,
  아쿠아다람쥐(신설), 생명을 주는 자,
  테렌 수호자/테렌 보호국, 미니크녹, 불사조,
  타르 저장고, 카다(신설), 붉은 종착, 천사의 영역,
  재배자, 야라 숲, 뒤틀린 성장, 테서랙트.
- QA: 구조 0건.

### 1035 (105334~105617, 100건)

- 'The pillows~The simplest you can get' 대사.
- 표기: 에스더 브라이트, 대보호자, 알타, 에이펙스,
  에롤, 라이오드 신전, 아비칸, 붉은 종착, 타이드,
  히로틀 로닌, 테라포머, 고대인들, 베스퍼, 펠하임,
  불사조, 스타더스트 리라(신설), 생태 실, 하이올릭,
  균형(equilibrium 관례 유지), 미니크녹.
- QA: 구조 0건.

### 1034 (105031~105329, 100건)

- 'The main teleporter'~'The picturesque terrain' 대사.
- 표기: 전초기지, 신성력, 칼린, 알타, 미니크녹,
  물질 조작기, 센티아, 시간 없는 행성, 필멸자,
  얼라이언스, 유니온, 니아 칵테일, 카다반,
  슈퍼보이드, 루인, 테서랙트, 고대 천사,
  에이비언 대보호자, 알터니아 수정, 탈라 여제(신설),
  에로스, 헤븐송, 아케인 툰드라.
- 'xOliver137' 이스터에그는 로마자 유지.
- QA: 구조 0건.

### 1033 (104599~105027, 100건)

- 'The good news~The main reason' 대사. 아케이드 게임명
  연속 포함.
- 게임명 관례(음역+따옴표): '아름다운 시도!',
  '쿨 위저드 아일랜드', '사이키델릭 로데오 난투',
  '비명 패션 에이전트', '슬리지 버거 히어로즈',
  '스타바운드', '스타일리시 시프 웨이스트랜드',
  '좀비 바나나 맨션'.
- 표기: 그라운디드, 크래스베리, 기트신, ECOC-FIOC,
  에보아쿠아틱, 숲 그 자신, 펜론, 비에라, 이조 잼/포이,
  붉은 종착 행성, 케찰코아틀루스, 하피, 파아리,
  러스트링, 클루엑스, 바람부는 세계(신설),
  자철석(lodestone).
- QA: 구조 0건.

### 1032 (104349~104598, 100건)

- 'The egg of a worm-like'~'The goo is burrning' 대사.
- 표기: 카다반, 대보호자, 고대 종족, 한밤 행성,
  엠버 산호, 밤안개 세계, 아키마리 프리깃,
  센텐시안, 펜론 전쟁 짐승, 고대인들, 재배자, 루인,
  아비칸, 커버넌트, 크라코탄, 트링키안, 헤일로,
  리프콜라, 헤븐송, 파아리, 필멸자, 에로스,
  붉은따오기(scarlet ibis 신설), 여덟 번째 구체.
- 104387 원문 끝 쉼표 유지.
- QA: 구조 0건.

### 1031 (104077~104348, 100건)

- 'The ceramic~The egg of a mooshi' 대사.
- 표기: 기아룬, 세터라이, 알타, 하이드로베리움(신설),
  아보라이트(신설), 아발론, 에로스, 아비칸, 컬티스트,
  레테이아, 플롭볼, 에르키우스, 자완, 아우라니아,
  필멸자, 루인, 쉘가드, 히로틀, 라이오드,
  식민지 증서, 페네록스, 무시, 울루, 플러팔로,
  아케인 윌드(arcane wealds), 메탈냥이(metalpurrson).
- QA: 구조 0건.

### 1030 (103708~104076, 100건)

- 'The Tower-Shields'~'The centerpiece' 대사.
- 표기: 타워 실드, 트랑기, 아에기니안, 트링크/트링키안,
  언바운드, 스타포지, 호버바이크,
  통합 얼라이언스 제작대, 유니온, 선봉대, 비에라,
  와스프밈, 클루엑스의 수레바퀴, 와일드캣,
  에어로겔, 아비칸 감시자, 아모러스, 엠피리언,
  키리 열매, 시아크사, 보호국, 마우트랩,
  임페르비움, 얼음 플러팔로, 스타더스트.
- 신설: 데드비츠(Deadbeats), 찬탈자들(Usurpers,
  104991 관례), 숲 그 자신(Wood Herself), 숲의 심장,
  톱니바퀴 공방(Workshop of Gears), 우주 표류자(spacedrifter).
- QA: 구조 0건.

### 1029 (102999~103706, 100건)

- 'The Beakeasy'~'The Tide' 서술 대사, 종족 개관 연속.
- 표기: 비케이지, 이중주화, 인포스파이어, 카고르타-1,
  헤비카, 네이테루, 센텐, 얼라이언스, 고해실,
  커버넌트, 재배자, 고대 관문, 기만자, EDS,
  엘리시안 얼라이언스, 여제, 엑소시안, 버밀리언,
  파아리, 롬, 발데르, 펠린, 피르나 영사관/캣츠포,
  가드후르, 겔세미, 글리치 남작, 펜론, 성화,
  호라이즌, 마기사이트 화로, 물질 조작기, 마우트랩,
  미니크녹, 지혜의 거울, 필멸의 종족, 노마다,
  고대인들, 라이오드, 피스키퍼, 보호국, 림,
  로닌의 맹세, 아비오 필기체, 새터니안, 솔라레이,
  쉘가드, 스타게이저, 저장 매트릭스, 슈퍼보이드,
  텔레안, 텔헌터, 타이드.
- 신설: 발데르(lord Valder), 캣츠포(Catspaw).
- QA: 구조 0건.

### 1028 (102740~102998, 100건)

- 'That's not MY moss'~'The Beakeasy' 대사.
- 표기: 코먼스 도시(Commence), 메이든, AAE(로마자 유지),
  ASA-26 레인저, 아에기(Aegi), 핫브뢰드, 바쉬, 아키마리,
  천사, 수호자, 아넬리스크, 리샨, 거짓 군주,
  에이펙스 반란군, 미니크녹, 아발리, 클루엑스,
  에이비언, 새터니안, 액티아스, 아비칸 선봉대,
  드랄, 샌드스토커, 센텐시안, 세터니티, 비케이지, 넥서스.
- 'Doubloons'는 이중주화로 처리.
- QA: 구조 0건.

### 1027 (102575~102739, 100건)

- 'That penguin~That's no moon' 대사.
- 표기: 미니크녹, 클루엑스, 아키마리, 글립,
  아이소슬라임, 스타바운드 문장, 냉기화산(cryovolcano),
  리다 냐르티아(Leda Purrtia 말장난), 노바키드.
- 노바키드 'That there's~' 사투리 연속 유지.
- QA: 구조 0건.

### 1026 (102196~102574, 100건)

- 'Tents~That penguin' 대사. 'Thank~' 연속 감사문 포함.
- 접두사: Terrified.→공포.(관례), Awestruck.→경탄.(관례).
- 표기: 제비갈매기(terns), 탈라소 가구, 클루엑스,
  에르키우스, 알파카, 스타라이트, 세터라이, 이오,
  에보아쿠아틱 세계, 달 세계(lunar worlds), 스푸킷,
  빅 에이프, 일각고래(narval), 스타더스트 프리즘.
- 말장난: skele-ton→해골만큼 고마워!,
  meownster→냐괴수, mad sus→완전 수상해.
- QA: 구조 0건.

### 1025 (101500~102195, 100건)

- 'Table-~Tents' 대사 + turnin 'Talk to~' 6건.
- 접두사: Tempted.→유혹.(관례), Tense.→긴장함.(근접 관례).
- 표기: 팔케, 마리나, 노엘, 우 사부, 접수처,
  크레온 대사관, 별여행자 피난처, 템미, 아우라니아,
  텐리, 텐타츄, 테라마트, 뱅가드, 픽셀.
- 101799 semen→정액 직역 유지.
- QA: 구조 0건.

### 1024 (101149~101499, 100건)

- 'Sure~Table-' 대사. 글리치 'Surprised/Suspicious/Sympathetic' 연속.
- 접두사: Surprised(.|!)→놀람., Suspicious.→의심.,
  Sympathetic.→공감함.(근접 행 관례).
- 표기: 오레이트 형제단, USCM, 오륨(신설 음역),
  문멜론, 베리스코이와, 서킷-트링크, 무시,
  아틀라 금(atla-gold), 펠린 인사 '수르히 로미!'.
- 101160 원문 '..?' 부호 이상은 원문 그대로 유지.
- 101484 개구리 말장난(TOADaly rad)→'개굴게 멋져!'.
- QA: 구조 0건.

### 1023 (100581~101136, 100건)

- 'Strange~Supposedly' 대사. 'Such a~' 연속 감탄문 다수.
- 접두사: Stumped.→난감.(신설).
- 표기: 에기, 아볼라이트, 소나베일, 레테이아,
  팝볼(Popball, Plopball→플롭볼과 구분 유지),
  일렉트로라이트, 슈퍼스톰 익스팬스, 에세테라/아스테라,
  빛나는 세계(illuminated worlds).
- 100868 개조(Doge) 문체 → 장음 없이 어색한 어조로 재현,
  공백+
 구조 보존.
- QA: 구조 0건.

### 1022 (99866~100578, 100건)

- 'Standard~Strange' 대사. 글리치 'Statement.' 연속(진술. 통일).
- 접두사: Startled.→놀람., Statement.→진술., Stern.→엄격.,
  Straightforward.→단도직입적으로.(관례),
  Stating the obvious.→당연한 말.(신설), Realization.→깨달음.
- 표기: 스타바운드, 별숲(Starforest 신설), 스타게이저,
  스타크랩, 스노우포프, 머드맨, 미니크녹, 레테이아,
  평화유지군, 행성 수호자/행성 보호국, 저장 물질 추출기,
  언바운드 프레임, 스테이터스 포드, 센텐스, 하이베리움.
- 100162 원문 끝 마침표 없음 → 동일하게 유지.
- QA: 구조 0건.

### 1021 (99650~99863, 100건)

- 플로란 'Ss/St~' 대사 98건 + 인간/알타 2건.
- 표기: 지오모아, 펜론, 포획 포드, 슈퍼스톰 익스팬스,
  슈퍼보이드, 트랩루트, 강철 황야, 픽셀, 스팀.
- 긴 모음(Boriiiing 등)은 장음 반복('지루우우웅해애').
- QA: 구조 0건.

### 1020 (99531~99649, 100건)

- 전량 플로란 'Sss~' 대사(과장된 치찰음), '~야애/~해애' 유지.
- 표기: 스모그질라, 셸가드 문장, 펠린, 태양화된 세계
  (solarized), 슬롯머신, 픽셀.
- 긴 모음(lighhhhht, seeee throughhhh 등)은 한국어
  장음 반복으로 흉내('투어어어어어얼명해애' 등).
- 99600 dildo→딜도 직역 유지.
- QA: 구조 0건.

### 1019 (99417~99530, 100건)

- 전량 플로란 'Ss~' 대사. 말버릇 '~야애/~해애' 유지.
- 'Ssome X. Floran shell enjoy its sswetnesss' 반복문
  → 'X 좀 있어애. 플로란이 달콤함을 즐길 거야애!' 통일.
- 표기: 페네록스, 시그리드, 스푸킷, 센본자쿠라,
  휴대뇌(Portabrain), 전기소녀, 오징어인간, 서기관,
  장로들 서버 캐비닛.
- 99496 freezing→얼어가는 / 99497 frozen→얼어붙은 으로 구분.
- 99479/99480 동일 원문 → 동일 번역.
- QA: 구조 0건.

### 1018 (98870~99416, 100건)

- 'Soothin'~'Ssome fresh' 대사 + turnin 'Speak to~' 19건.
- 접두사: Sorrowful.→슬프다., Speculation.→추측.(신설),
  Speculative.→추측이지만.(관례), Spooked.→겁먹음.(신설).
- 표기: 잔쿠노, 트위터스, 윌, 제이드, ST 실렉티스,
  크리더스, 탈라소 전초지, 펭귄 피트, 언더사이드 사람,
  엔테르니아, 아이졸링, 스푸킷, 테라마트, 세지,
  오징어인간, 민달팽이개구리.
- 네키: purrtraits→초상냥, waterrr→물이야애.
- 플로란 Ss- 계열: 기존 관례대로 쌍자음 의미부여
  ('~야애/~해애') 유지.
- QA: 구조 0건.

### 1017 (98623~98869, 100건)

- 'Someone~Soossy' 대사.
- 표기: 클루엑스, 컬티베이터, 지오모아, 누리스,
  슈퍼스톰 행성, 엘린, 메크 부품.
- 네키: brricks→벼억돌, brrown→갈시액, drrop→떨굴,
  frrosty→얼어부었어(소리 흉내는 의미로 처리).
- 98869 'Soossy baki!' 원문 자체가 변형 발화라 '쑤시 바끼!'로 음역.
- QA: 구조 0건.

### 1016 (98483~98622, 100건)

- 'Some sort of~Someone' 대사. 천사/아비안 다수, 필멸자·악마 어조 유지.
- 표기: 센텐시안, 미니크녹, FTL 드라이브.
- 네키 말장난: purrfection→냐-완벽하게,
  telepurrter→순간냐동기, butt-ons→엉덩-튼.
- 98579/98580은 98328/98329와 같은 구조라 동일 어조 유지.
- QA: 구조 0건.

### 1015 (98321~98482, 100건)

- 'Some folks~Some sort' 대사. 노바키드 'Some kinda~' 연속.
- 표기: 야라, 아야카 묘목, 칼린 수프, 성진 프리즘,
  영계, 비오니드-C2-프리아스-7, 네리기드(신설 음역),
  스타리스, 이오, 포이, 애니머스 행성, 노움, 아발리/러스트링.
- 네키 말장난: papurrs→종냥, badpurrson→나쁜냥이,
  butt-on→엉덩-튼(유지), *yawns*→*하품*.
- 98449/98450 동일 원문은 동일 번역.
- QA: 구조 0건.

### 1014 (97950~98320, 100건)

- 'So much~Some flyer' 대사. 글리치 'Solemn/Somber' 시리즈 포함.
- 접두사: Solemn.→엄숙함., Somber.→침울함.(기존 관례).
- 표기: 요누르, 이온 발효물, 언바운드, 스타포지,
  유카이 대장장이, 마리코, 크라코스(K'Rakoth), 로닌,
  플롭볼, 베이터, EDS, 엔니아, 바르다스, 아쿠아리,
  데이터매스, 솔/아발론/에로스, 이오, 네키 spacesits→우주의자.
- 97972 원문 끝 고립 '«'는 오기로 보고 번역에 미반영.
- QA: 구조 0건.

### 1013 (97361~97947, 100건)

- 'Slimey~So much' 대사. 네키 'Sits/butt-ons' 말장난 계열 다수.
- 접두사: Smug.→거만함.(근접 행 관례), Sneering.→비웃음.,
  Snobbish.→오만함.(신설).
- 표기: 스킵라이플, 타브리야, 카이터, 우노나 목재,
  이조포이, 아볼라이트, 아보스, 핏빛 행성(sanguine),
  하피, 펜론, 거짓 군주들, 스모그질라, 미니크녹(용어집),
  EDS 탱크.
- 네키 말장난: butt-ons→엉덩-튼, purrple→냐라색,
  murrvellous→냐-놀라운.
- QA: 구조 0건.

### 1012 (96864~97360, 100건)

- 'Shuttlecraft~Slimey' 대사. 히로틀 '이런 표지판은 보통~' 연속 구조화 대사 포함.
- 접두사: Sickened.→역겨움., Skeptical.→회의적., Sleepy.→졸림.(기존 관례).
- 표기: 시그리드, 메르시아, 펠하임, 칼로트로닉스, 칼린,
  기트신, 아믹(아야카/비온), 비신 장식, 타워 실드,
  슬리지 버거 히어로즈(기존 음역 유지), 러스트링.
- 네키 'Sits' 시리즈 → '의자야' 통일. 'Purrfect'→'냐-완벽해!'.
- QA: 구조 0건.

### 1011 (96502~96856, 100건)

- 'She~/Shiny~/Shocked~' 대사 + turnin 'Show~' 퀘스트문.
- 접두사: Shifty.→교활.(신설), Shock./Shocked.→충격.(신설).
- 표기: 쉐마(신설), 보안관 랜더스, 문샤인, 셸가드 문장,
  노움당했어(gnomed), 조수(Tide), 프롤레타리아, 안쿠,
  천문대, 노바 스테이션, 팔케, 레이저윙, 론딘,
  임페르비움, EPP(슈퍼스톰/삼극/페일).
- 원문 미완 행(96811, 96812)은 원문 형태 유지.
- 96811: 원문이 ^orange; 미닫힘 상태로 끝남 — 번역도 ^orange;
  개방·^reset; 미삽입으로 일치시켜 QA 통과(깨진 원문 유형).
- QA: 구조 0건(수정 후).

### 1010 (95967~96499, 100건)

- 'Seems~' 마무리 + 노바키드 외계 숫자 + 'Se~/Sh~' 대사.
- 접두사: Self-assured.→자신만만.(신설), Sentimental.→감성.(신설),
  Serene.→평정.(신설), Serious.→진지.(신설),
  Shaken.→동요.(기존 재사용).
- 표기: 행성 보호국, 비오니아, 게아토른, 참매(Goshawk),
  못츠, 테크 선택 UI 문구.
- QA: 구조 0건.

### 1009 (95369~95966, 100건)

- 글리치 'Satisfied.' + 드로덴 'Scan~' 보고 + 아비안
  'Seems like~' 표지 시리즈.
- 접두사: Satisfied.→만족.(신설), Scared.→공포.(신설),
  Secured.→확보.(신설), Seduction.→매혹.(신설).
- 표기: 마리코, 솔계, 새터니안, 스카바, 프로토스피어,
  바시, 케프, 게라, 쿡 씨, 네레우스 박사, 탈라소,
  샤토 아발론, OSHA, 컬티베이터, 드라우나르.
- QA: 구조 0건.

### 1008 (94397~95368, 100건)

- turnin 마무리 + 'R~/S~' 시작 대사.
- 접두사: Reverent.→경건.(신설), Revolted.→역겨움.(신설),
  Sad./Saddened.→슬픔.(신설), Sarcasm./Sarcastic.→빈정.(신설).
- 표기: 라데이스, 격양자(Uplifter), 리서스, 리비스, 리카,
  카이테란, 드리프트라이플, 아보스톤, 루바이트, 플로라스톤,
  쏜윙, 언바운드, 료타, 라크리마, 패스파인더, 야란(신설),
  샌드크롤러, 사샤 베니코, 모르페우스, 헤븐송.
- QA: 구조 0건.

### 1007 (93779~94396, 100건)

- 글리치 'Relieved.' 대량 + turnin 퀘스트 반납문 시리즈.
- 접두사: Relief./Relieved.→안도.(신설), Reluctant.→주저.(신설),
  Repulsed.→혐오.(신설), Resentful.→원망.(신설),
  Resourceful.→기지.(신설), Respectful.→존경.(신설),
  Reminiscent.→회상.(신설).
- 표기: 크레온 대사관, 스타페어러의 피난처, 라이트헤이븐,
  갤리온, 코이치, 리인 제독, 자히드, 아라바스/아르탄/
  아비이라/아얄라/렌즈-88/마칸/네네키/레콘/세라/스노우롬
  (신규 NPC 음차), 셸가드, 초코보, 클라운킨, 아가란,
  감시자들(Watchers).
- QA: 구조 0건.

### 1006 (93138~93778, 100건)

- 'R~' 시작 대사. 노바키드 'Reckon~' 표지 시리즈,
  글리치 'Relaxed.' 대량.
- 접두사: Rapturous.→황홀.(신설), Rattled.→전율.(신설),
  Reassured.→안심.(신설), Rebellious.→반항.(신설),
  Reflective.→사색.(기존 '사색' 재사용), Relaxed.→이완.(신설).
- 표기: 라그나, 발더, 펠하임, 메르시아, 락샤사, 삼극 항성,
  레이저테일, 리클레이머, 옴니블루, 페로지움, 바이올륨,
  포이, 이온화 방사선(원문 오탈자 izonizing 교정 의미 유지).
- QA: 구조 0건.

### 1005 (92602~93124, 100건)

- 'P~' 마무리 + 'Q~/R~' 시작. 네키 '푸르(purr)' 말장난
  시리즈는 어감 살려 변환.
- 접두사: Prudent.→신중.(신설), Puzzled.→난해.(신설),
  Query.→질의.(신설), Questioning.→질문.(신설),
  Quizical/Quizzical.→의아.(원문 오탈자 포함 통일),
  Quality-Assuring.→품질보증.(신설).
- 표기: 아틀라 금, 피크노섬유, 푸스플럼, 크래스베리,
  테라마트, 앵그리터렛(신설), 스모그질라, 스바.
- QA: 구조 0건.

### 1004 (91737~92601, 100건)

- 'Poor~/Poster~/Pretty~/Pro~' 대사.
- 접두사: Positive.→긍정.(신설), Praise.→찬양.(신설),
  Prating.→확신.(신설, '인식/확신' 의미로 해석),
  Preoccupied.→몰두.(신설), Prideful.→자랑.(신설),
  Proud.→자랑.(동일 통일).
- 표기: 드라이, 팝탑, 네트리마, 프로메튬, 보호국 화폐,
  비르마, 비신, 미친 고양이 아줌마.
- QA: 구조 0건.

### 1003 (91280~91735, 100건)

- 'Platform~/Plush~/Poison~/Poor~' + 글리치 'Pleased.' 대량.
- 접두사: Playful.→장난.(신설), Pleased.→흡족.(신설),
  Poetic.→시적.(신설), Pondering.→숙고.(신설),
  Ponderous.→숙고.(동일 통일).
- 표기: 플래티넘 에이스, 트랩루트, 클레어 고프, 아트모스,
  피터 아트모스, 록조, 단조 명인, 스타포지, 매크로칩 계열
  (메가매크로칩/미니매크로칩), 네트리마, 폴리비우스,
  연사들(Speakers).
- QA: 구조 0건.

### 1002 (90787~91279, 100건)

- 'P~' 대사 계속. 네키 '식물사람(plantpurrson)' 시리즈.
- 접두사: Perturbed.→동요.(신설), Philosophical.→철학.(신설),
  Picky.→까다로움.(신설), Pitiful.→불쌍.(신설).
- 표기: 크라코스, 엘리시아, 엘리시아 동맹, 아크리스,
  익스프레스 트랜짓(신설), 피루, 슈퍼스톰, 피카, 히미드.
- QA: 구조 0건.

### 1001 (89817~90786, 100건)

- 'Out~/O~' 마무리 + 'P~' 시작 대사.
- 접두사: Outraged.→격분.(신설), Overjoyed.→기쁨.(신설),
  Overwhelmed.→압도.(신설), Panic.→공황.(신설),
  Paranoid.→편집.(신설), Peaceful.→평온.(신설),
  Pensive.→사색.(신설), Perceptive.→통찰.(신설),
  Perplexed.→당혹.(신설).
- 표기: 배터조, 파놉티콘, 로어스피크(신설), 부리씨앗,
  엑소시안, 알파카.
- QA: 구조 0건.

### 1000 (89327~89813, 100건)

- 'Only~/Ooh~/Orange~/One of~' 대사 마무리.
- 접두사: Opinion.→의견.(신설), Optimistic.→낙관.(신설).
- 표기: 심연 출생(abyssborn), 스페이스드리프터, 조리아,
  오션 서프라이즈, 베피스, 오바이드, 아야카, 오를라,
  솔라레이, 트링크, 푸리차.
- QA: 구조 0건.

### 0999 (88890~89326, 100건)

- 'Okay/Old~/On~/One~' 시작 대사. 아발론·에로스 동굴화
  5종 세트(종족별).
- 접두사: Ominous.→불길.(신설).
- 표기: 텔헌터, 아발론, 에로스, 나이트미스트, 에보아쿠아틱,
  에터니아, 드리머, 엠피리안, 아야 펀치, 비에라, 텔리안,
  플라즈마 차크람, T0/T1 패드.
- QA: 구조 0건.

### 0998 (88632~88887, 100건)

- 'Oh~' 감탄 대사 마무리.
- 표기: 에셜론, 센본자쿠라(센본...으로 어눌 표현), 제이미 도우,
  토스, 매니펄레이터, 마스터 조작기, 스타리스 포이, 피린,
  데이터매스, EDS, 가든, 크라코탄 번역기,
  슈퍼 트랄가 블래스터.
- QA: 구조 0건.

### 0997 (88240~88630, 100건)

- 'Observative/Observing~' + 'Oh~' 감탄 대사 다량.
- 접두사: Observative.도 '관찰.'로 통일. Offended.→불쾌.(신설).
- 표기: 베로스틴, 스틸블레이드, 배드랜즈, 피아니, 키라,
  이오, 클루엑스, 눈알레몬, 보리얼라이트, 센티아, 루인.
- 러슬링 성적 대사는 원문 톤 유지(수위 조절 없음).
- QA: 구조 0건.

### 0996 (88133~88238, 100건)

- 글리치 'Observant./Observation./Observational.' 마무리.
  세 변형 모두 관례 '관찰.'로 통일.
- 표기: 안드로스 갈바넥.
- QA: 구조 0건.

### 0995 (88026~88132, 100건)

- 글리치 'Observant.' 단독 배치.
- 표기: 키츠네 토리이, 스펙트윙, 우피, 생크틸라이트,
  엘리시아, 크러터, 타로니, 팝볼, 솔라리움, 니트로메탄,
  하이베리움, 더스트리움, 갈바강, 제너럴 무니션스,
  컬티베이터, 고대의 존재들, 수레국화.
- QA: 구조 0건.

### 0994 (87801~88025, 100건)

- 외계 숫자판 마무리 + 알타 'Oa~' 감탄 시리즈 +
  글리치 'Observant.' 시작.
- 접두사 관례: Obedient.→순종.(신설), Observant.→관찰.(신설).
- 표기: 누루, 아키(아키마리 자칭), 프로테아, 에레나이(신설,
  TM에 없어 음차), 아이스테리온, 크라코탄, 길텐, 코버넌트,
  파이오니어, 트링키안, 아르카니안, 하프시, 넛밋지링.
- QA: 구조 0건.

### 0993 (87431~87799, 100건)

- 'Nothing~/Now~' 시작 대사 + 외계 숫자판.
- 표기: 슈퍼보이드, 미아즈마, 아비칸, 노바킨, ST 실렉티스,
  오카서스, 무시, 윈체스타, 아야쿠트, 서티슈터.
- QA: 구조 0건.

### 0992 (87154~87427, 100건)

- 글리치 'Nostalgic.' 시리즈 + 'Not~' 시작 대사.
- 접두사 관례: Nostalgic.→향수.(기존 '향수' 용어에서 신설),
  Nonplussed.→의아.(신설).
- 표기: 노마다, 울루, 허기, 모트랩, 칼린, 드로덴,
  미니크노그, 군단 유닛.
- QA: 구조 0건.

### 0991 (86746~87153, 100건)

- 'Nice~/No~' 시작 대사. 니제마이즈 독일어체는 평어체로 흡수.
- 표기: 님보스프라이트, 니베라, 니제마이즈, 칼리오파,
  알타 샤를로트, 알탄, 야라, 캣포, ASA-26 레인저,
  발할라, 루카리오.
- QA: 구조 0건.

### 0990 (86539~86743, 100건)

- 글리치 'Neutral./Neutrally.' 나머지 + 'N' 시작 대사.
- 표기: 듀라스틸, 앤서블, 스타크랩, 스타라이트, 에민스노우,
  포크-툭, 스켈레톤 미러, 넥스테크, 넥서스 코퍼레이션,
  유물 수집가, 플래시 핀즈.
- QA: 구조 0건.

### 0989 (85793~86538, 100건)

- 'M~N' 시작 대사 + 글리치 'Neutral.' 광물 표본 시리즈.
- 접두사 관례: Mysterious.→수수께끼., Mystified.→경이.(신설),
  Nauseated.→메스.(신설), Nervous.→긴장., Negative.→부정.(신설),
  Neutral.→중립.
- 표기: 광물군(아다만타이트/아레프/아쿠올라이트/비스무트/
  클로로파이트/크림테인/크립타이트/데모나이트/에르키로사이트/
  지오리다이트/헬스톤/키레나이트/루니움/미스릴/오리할쿰/
  로푸나이트/엠버 산호/루미나이트/황/트리피사이트),
  나디아, 헤븐송 식민지, 카이테라, 페네록스.
- QA: 구조 0건.

### 0988 (85346~85790, 100건)

- 'M' 시작 대사 계속 + 드로덴 벽화 분석 시리즈.
- 접두사 관례: Musing.→심사.(신설).
- 표기: 브할레이한, 라데이스, 벨린, 바스 브할레이, 카다반,
  아릭, 스너겟, 야어링, 칼린, 아볼라이트, 물질 조작기.
- QA: 구조 0건.

### 0987 (84856~85345, 100건)

- 'M' 시작 대사 계속 + 네키 'Mrr' 다수.
- 접두사 관례: Mocking.→조롱., Mournful.→애도.(신설),
  Mouthwatering.→군침.(신설).
- 표기: 마더 셀레스티아, 못츠, 액티안, 아보스, 문멜론,
  모그리, 마기사이트, 알테라시, 크라코탄.
- QA: 구조 0건.

### 0986 (84249~84853, 100건)

- 'Me~Mm' 시작 대사 + 고양이 대사.
- 접두사 관례: Merry.→즐거움., Mesmerized.→넋을 잃음.,
  Michievious./Mischievous.→장난.(신설),
  Mildly intrigued.→약한 호기심.(신설).
- 표기: 소나베일, 아이온, 왐파, 엘리시아, 미오, ADF,
  미니크녹, 샤토 아발론, 묘신(고양이 말장난).
- QA: 구조 0건.

### 0985 (83344+83605~84248, 100건)

- 'M' 시작 대사. 글리치 'Melancholic./Melancholy.'(→우울.).
- 83344는 0984에서 미병합되어 이번 배치에 포함.
- 표기: 물질 조작기, 조수, 마사무네, 메로스 아반, 복셀,
  엑수시아, 주홍, 탈라소, 아스트랄 관측소, 플린트.
- QA: 구조 0건.

### 0984 (82731~83603, 100건)

- 'L~M' 시작 대사. 글리치 'Luxuriated.'(신설→사치.).
- 표기: 루모스, 흙성게, 리인 아트마에라, 찰스 말라키,
  마기사이트, 아보스톤, 아모러스, 루카리오, 카다반,
  나이트폴, 특사.
- QA: 구조 0건.

### 0983 (82561~82730, 100건)

- 'Looks like...' 계열 대사 계속.
- 표기: 미니크녹, USMC, 무시, 크라코탄, 키츠네, 넛밋지링,
  제너럴 뮤니션스, 아볼라이트, 지구 파괴자.
- QA: 구조 0건.

### 0982 (82419~82560, 100건)

- 'Looks like...' 계열 대사(에이펙스 근처-판별문 다수).
- 표기: 본 드래곤, 앵글루어, 파라데아, A.R.C.O. 포드,
  크라코스, 유물 탐구자.
- QA: 구조 0건.

### 0981 (81952~82418, 100건)

- 'L' 시작 대사 계속. 글리치 'Longing.' 접두사(신설→그리움.).
- 표기: 아에기니안, 센텐시안, 노마다, 라인라이플, 비신,
  보리얼라이트, 알테라시, 아든 타이가, 기트신, 아크나이트,
  유물 탐구자, 화이트우드, 모그리.
- QA: 구조 0건.

### 0980 (81232~81951, 100건)

- 'L' 시작 대사. 글리치 'Leery.' 접두사(신설→경계.).
- 표기: 레다 포르티아, 레니르시, 아투미움, 리코르,
  오큘레몬첼로, 이오, 레테이아, 유물 탐구자, 아비칸.
- QA: 구조 0건.

### 0979 (80259~81231, 100건)

- 'K~L' 시작 대사 + 글리치 'Kindled./Know-it-all./Knowledgeable./Label.' 접두사.
- 접두사 관례: Kindled.→고무.(신설), Know-it-all.→아는척.(신설),
  Knowledgeable.→지식., Label.→분류.(신설).
- 표기: 저스티카, 케프, 클렙토드, 코도릭, 코흐리아, 라에나틴,
  키리 열매, 카이테란, 코이치, 코지, 나이트폴.
- QA: 구조 0건.

### 0978 (79781~80258, 100건)

- 글리치 'Jealous./Jesting./Jocular./Joking./Jolly./Joyful./Joyous./Judgmental.'
  접두사군 + 'Just...' 계열.
- 접두사 관례: Jealous.→질투., Jesting./Joking.→농담.(신설),
  Jocular.→익살.(신설), Jolly.→즐거움., Joyful.→기쁨., Joyous.→환희.(신설),
  Judgmental.→판단.(신설).
- 표기: 잘민, 와일드캣, 데드비트, 모니카(오직 모니카만), 바르다,
  왕관 라크리마, 이오, 펜론, 크라코스, 에르키우스.
- QA: 구조 0건.

### 0977 (79520~79776, 100건)

- 다종족 'It's so/It's the/Its...' 계열 대사.
- 표기: 시아사, 스타리스, 아케인 행성, 왜곡된, 미니크녹,
  타우모스 비단, 모그리, 히로틀.
- QA: 구조 0건.

### 0976 (79321~79519, 100건)

- 다종족 'It's like/not...' 계열 대사.
- 표기: 야라, 아야카, 비르마, 텐리 여제, 나노선반, 루인,
  놈족, 크라코탄, SAIL.
- QA: 구조 0건.

### 0975 (79096~79320, 100건)

- 다종족 'It's an/It's...' 계열 대사.
- 표기: 나이트미스트, 모트랩, 드로이, 네이테루, 아야 펀치,
  첼시, 돌리, 클루엑스.
- QA: 구조 0건.

### 0974 (78953~79095, 100건)

- 다종족 'It's a...' 계열 대사.
- 표기: 드레메톤, 트링크, 노틸리치, 플래시 핀즈, 아발론,
  유물 탐구자, 쿠포, 셸-B, 프로그, 아키마리.
- QA: 구조 0건.

### 0973 (78804~78952, 100건)

- 다종족 'It's a...' 계열 대사.
- 표기: 텔란, 텔, 카렐, 울루, 머드맨, 페트리컵, 루멘 주스,
  히라키 코랄레, 플러팔로, 글룸우드, 미니크녹, 아에기.
- QA: 구조 0건.

### 0972 (78484~78800, 100건)

- 다종족 'It seems/It looks/It must...' 계열 대사.
- 표기: 레테이아, 소네바, GSR 포드, 스타포지, 에스더,
  먼치/『별에서 튀어나온』, 랄프, 크라코탄, 미니크녹, 드레이.
- QA: 구조 0건.

### 0971 (78233~78483, 100건)

- 다종족 'It feels/It looks/It is...' 계열 대사.
- 표기: 아볼라이트, 라이프스프링, 크라코탄, 모포시스,
  에보아쿠아틱, 누올리스, 나이스마이스, 미니크녹, 빅 에이프.
- QA: 구조 0건.

### 0970 (78001~78231, 100건)

- 다종족 'Is this/It...' 계열 대사.
- 표기: 크라코스, VEP, 스카바, 월드 호라이즌, 솔 수정,
  컬티베이터, 펭귄, 마이토/마이토리시, 미니크녹, 노바키드.
- QA: 구조 0건.

### 0969 (77829~78000, 100건)

- 다종족 'Is it.../Is that.../Is this...' 질문형 대사.
- 표기: 비오나 초원, 페블릿, 제노프로브, 콜드버드, 로크, 펜론,
  보호국 휘장, 포획용 포드, 빅 에이프.
- QA: 구조 0건.

### 0968 (77476~77825, 100건)

- 글리치 'Intrigued./Intriguing./Intruiged./Investigative./Invigorated./Irked./Irritated.' 다수.
- 접두사 관례: Intrigued./Intriguing./Intruiged.→호기심., Investigative.→조사.(신설),
  Invigorated.→활기., Irked./Irritated.→짜증.
- 표기: 이니셔티브, 크러스토이즈, 코로디움, 무시, 클루엑스, 미니크녹.
- QA: 구조 0건.

### 0967 (77309~77475, 100건)

- 글리치 'Interested./Interpretive./Intimidated./Intrigued.' 다수.
- 접두사 관례: Intrigued.→호기심., Interpretive.→해석.(신설),
  Intimidated.→위압., SAIL→함선, 와일드캣, 나이트폴 랩터,
  메르시아/메르시발, 텔란.
- QA: 구조 0건.

### 0966 (77072~77308, 100건)

- 글리치 'Informed./Inquisitive./Insecure./Insightful./Inspired./Insulted./Interested.'다수.
- 접두사 관례: Inquisitive.→호기심., Insecure.→불안., Insightful.→통찰.(신설),
  Inspired.→영감., Insulted.→모욕.(신설), Interest./Interested.→흥미.
- 표기: 플래티넘 에이스, 락사사, 글룸우드, 그린핑거, 로닌,
  유물 탐구자, 언바운드, 프랙툴.
- QA: 구조 0건.

### 0965 (76654~77071, 100건)

- 글리치 'Impressed./Indifferent./Indignant./Informative./Informed.' 다수.
- 접두사 관례: Informative./Informed.→정보., Indifferent.→무관심.,
  Indignant.→분개., Incensed.→격분.
- 표기: 밥페, 비신, 센본자쿠라, 미코, 액시엄, 넥스테크, 에셜론,
  제너럴 무니션스, USCM, 넥서스, 제이미 도우, 브릭스, AAE,
  아에기니안, 크라코스, 셸가드, 은방울꽃/양귀비.
- QA: 구조 0건.

### 0964 (76252~76653, 100건)

- 'If you ~' + 글리치 'Imaginative/Impartial/Impassive/Impatient/Impressed.' 다수.
- 접두사 관례: Impressed.→감탄.(62건), Impassive./Impartial.→무관심.,
  Impatient.→조급., Imaginative.→공상.(신설), Surprised.→놀람., Frightened.→공포.
- 표기: 보봇, 매지파이어 수정, 야비스, 지오모아, 보코, 아야 비르마,
  니아 요리, 트리후이, 크라코스, 셸가드, 모르페우스, 언바운드.
- QA: 구조 0건.

### 0963 (76081~76249, 100건)

- 'If ~' 조건 서술 연속.
- 표기: 야쿠트, 에보아쿠아틱, 바시, 페글라치, 애니마 파편/애니머스,
  칼린, 드레드윙, 텔란, 멀티점프 테크, 리샨, 식민지 증서.
- QA: 구조 0건.

### 0962 (75755~76078, 100건)

- 'I've never/I, uh/If ~' 서술 + 아키마리·글리치 묘사 다수.
- 표기: 에터니아 니아톤, 스모글린, 노마다, 테라포지, 고대 금고,
  연방-노틱스, 아스트랄 나르핀, 장로 존재, CNOB/ECOC-FIOC.
- QA: 구조 0건.

### 0961 (75326~75752, 100건)

- 'I'm/I've ~' 서술 연속.
- 표기: 드레메톤, 리마코, 헬리온, 아스타, 베로나스, 비오나 코르팔,
  바다 서프라이즈, 아든 타이가, 웜온치, 록 사냥꾼, 셀레스티아.
- QA: 구조 0건.

### 0960 (75058~75313, 100건)

- 'I'm ~' 서술 연속.
- 표기: 사케/꽃잎 꿀/소금물, 콜라 하트스로브, 포크툭,
  페트리큐브, 노틸리치, 센티아, 미믹, 제이 이지.
- QA: 구조 0건.

### 0959 (74655~75055, 100건)

- 'I wouldn't/I'd/I'll/I'm ~' 서술 연속.
- 표기: 못츠, 스너팔로, 라우스토르, 보호자, 비전 툰드라,
  생크틸라이트 문.
- QA: 구조 0건.

### 0958 (74478~74652, 100건)

- 'I wonder/would ~' 서술 연속.
- 표기: 오리지늄, 제네시스 코일, 알테라시, 라그나, 카이저,
  스타게이저, 태양 나방, 구더기 인간, 유물 수집가, 노틱스.
- QA: 구조 0건.

### 0957 (74151~74477, 100건)

- 'I want/was/will/wish/won't/wonder ~' 서술 연속.
- 표기: 탑파 대도서관, 나디아, 중형 피스키퍼, 타우모스 키틴,
  기트신 크리핏, 강탈자들, 릴로돈, 아키마리.
- QA: 구조 0건.

### 0956 (73943~74149, 100건)

- 'I think/thought/tried/understand/used to/wanna ~' 서술 연속.
- 표기: 우로보로스 산업 카르텔, 크림사시, 바이오니움, 세테라이,
  카고르타, 문탄트, 플릭, 아이졸링, 셀레스티아, 별가루 난초.
- QA: 구조 0건.

### 0955 (73756~73942, 100건)

- 'I should/suppose/suspect/think ~' 서술 연속.
- 표기: 유니온, 두네분, 길텐, 어베스밍고, 프리스키,
  코어 가루, 무시, 아키마리, 록 새.
- QA: 구조 0건.

### 0954 (73445~73755, 100건)

- 'I never/ought/prefer/reckon/remember/see/should ~' 서술 연속.
- 표기: 특사, 다이번, 지상인, 론딘, 쥬빌리, 블루믹스, 마리코,
  스타포지, 대수호자, 포획용 포드, 단조 명인, 팝탑, 물질 조작기.
- QA: 구조 0건.

### 0953 (73164~73444, 100건)

- 'I like/love/may/might/must/need ~' 서술 연속.
- 표기: 토나, 아야, 엔니아, 누미, 타브리야, 돌리,
  탈라소 전초지, 모르페우스, 나이스마이스(ze~억양).
- QA: 구조 0건.

### 0952 (72856~73163, 100건)

- 'I heard/hope/imagine/know/like ~' 서술 연속.
- 표기: 불러시, 프랙툴, 촘퍼, 아르막스, 리샨, 헤비카이,
  포이/포이볼, 메르시아, 자완, 미스터리 샬롯, 방사선영양.
- QA: 구조 0건.

### 0951 (72480~72855, 100건)

- 'I got/guess/had/have/heard ~' 서술 연속.
- 표기: 보호국, 레테이아 코퍼레이션, 에스터 브라이트, 체리스톤/펠하임 전쟁,
  발더, 펠 건틀릿, 대천사 세퀘이즈리엘, 아볼라이트, 아릭,
  아크나이트, 아스테라, 에바, 뇌설.
- QA: 구조 0건.

### 0950 (72257~72464, 100건)

- 'I don't want/doubt/dunno/feel ~' 서술 연속.
- 표기: 프로그, 데드비트, 글립, 울파, 알타, 테서랙트 발전기,
  미니크녹, 다윗 대 골리앗.
- QA: 구조 0건.

### 0949 (72081~72256, 100건)

- 'I don't ~' 서술 연속.
- 표기: 페네록스, 고스호크, 애널리스크, 발더, 미니크녹,
  황폐 행성(desolate planet), 아카데미, 수호자, 불모 행성.
- QA: 구조 0건.

### 0948 (71869~72080, 100건)

- 'I could/do/don't ~' 서술 연속.
- 표기: 미지링, 생크틸라이트, 옷장사, 클루엑스, 미니크녹,
  우주선 드론, 수정 골렘.
- QA: 구조 0건.

### 0947 (71676~71868, 100건)

- 'I can't/could ~' 서술 연속.
- 표기: 타우모스, 솔라레이, 언바운드, 엑소시안, 드로덴 군단,
  새터니안 가구 소환기, B.E.A.C.O.N.(유지), 엔테라시 프라임,
  라미아, 비에라, 빅 에이프.
- QA: 구조 0건.

### 0946 (71518~71675, 100건)

- 'I can ~' 기능 서술 대량 연속.
- 표기: 무플릭, 생태실(eco chamber), 페롤릭, 포스폴리온, 아크나이트,
  아스테라, 드라우나르, 조르가시아, 더블룬, 테라마트, 마그마틱 대장간,
  퍼르디움(purrdium), 셸가드, NG5/G2 인증.
- QA: 구조 0건.

### 0945 (71355~71515, 100건)

- 'I believe/can/bet~' 서술 연속 + 노바키드 'I can bookmark this X flag' 18연속.
- 표기: 엘리시아, 우프 본부, 포획 포드, 볼트스피터, 크리핏,
  셸가드, 트링키안, 아르카니안, 하프시, 키츠네 도리이, 스펙트윙, 우피,
  파이오니어, 코버넌트, 탈라소, 비에라/숲 그분, 오큘레모네이드,
  아릭 패드, 야라 멜론, 홍관조(cardinal), 마기사이트.
- QA: 구조 0건.

### 0944 (71039~71354, 100건)

- 노바키드 'I ain't ~' 연속 + 종족 혼합.
- 표기: AVN, 넥스테크, 레테이아, 유카이 단조 명인, 리브라 이클립스,
  미니크녹, 루인, 로닌, 다중우주.
- 메타 대사('아직 대사를 못 받았어', 'Crash FMV 삽입') 원문 유머 유지.
- QA: 구조 0건.

### 0943 (70543~71037, 100건)

- 종족 혼합 + 글리치 'Hungry. I should give this X a taste.' 연속 행.
- 표기: 프로젝트 45, 못츠, 루카리오, 프레시(음식명 처리), 히미드,
  히로틀로지/아발리로지/러스틀로지 종족명 유흥 음차.
- 글리치 접두사: Humble/Humbled(겸손), Humored(유머), Humorous(재밌음),
  Hungry(배고픔), Hypothesis/Hypothetical(가설).
- NL1 행(70661, 70690)
 보존.
- QA: 구조 0건.

### 0942 (70129~70540, 100건)

- 종족 혼합 + 'How ~' 의문 서술 대량.
- 표기: 핫브뢰드, 앵글루어, 파워 아머, 에스더 브라이트, 미니크녹,
  크라코탄, 센텐스, 페네록스 깨진 문장 유지.
- 글리치 접두사: Horrified(공포), Horny(흥분).
- QA: 구조 0건.

### 0941 (69652~70128, 100건)

- 종족 혼합 + 글리치 Horny 계열 성적 서술 — 원문 수위 유지.
- 표기: 캑티파, 토디알, 주빌리, 윈체스타, 비키지 술집, 크라코스,
  엘리시아, 생크틸라이트, 아르카니안, 룬 사막, 공명 연쇄(HL 인용),
  깡총깡총(Hippity hoppity 밈).
- 글리치 접두사: Hopeful(희망), Hesitant(망설임), Horny(흥분).
- NL1 행(69719)
 보존.
- QA: 구조 0건.

### 0940 (68799~69648, 100건)

- 종족 혼합; NL1 행(69510)
 보존.
- 표기: 스모그질라, 헤비카, 크리핏, 솔라라이즈드(태양화된), 텔루시안,
  하이브, 복셀, 팔(이름표), 크래시 FMV, 클루엑스 황금 토끼 전승.
- 글리치 Hesitant. → '망설임.'.
- 'Pal' 이름표/유형지 식민지(penal) 등 언어유흥 의역.
- QA: 구조 0건.

### 0939 (68138~68798, 100건)

- 아키마리 해치 시리즈 + 종족 혼합.
- 표기: 다크슬라임, 하피, 미니크녹, 발광 행성, 케프카, 슬러그프록,
  핸들러 월터, 타르바운드(Starbound 패러디), 웻 플루프(wet floor 오독).
- 글리치 Heartwarmed. → '훈훈.'.
- 'SPEEEEN'류 과장 소리 의역 유지.
- QA: 구조 0건.

### 0938 (67299~68125, 100건)

- 종족 혼합 + 아키마리 '신-도둑' 서사 연속.
- 표기: 매지파이어 크리스탈, 알테라시 헤이븐, 히라키 코랄레, 다트 퀘스트,
  해머 뮤니션스, 핸들러 월터, 세테라이, 징시즈, 그라운디드/스타게이저,
  플롭볼, 미니크녹.
- 글리치 접두사: Greedy(탐욕), Grinned(씩 웃음), Grooving(흥겨움),
  Happy(행복).
- 'HAHAHAH SPEEEEN'는 '돌아앗' 과장 표기로 의역.
- QA: 구조 0건.

### 0937 (66616~67293, 100건)

- 종족 혼합: glitch/akki(신-도둑 연속 서사)/novakid/floran/neki 등.
- 표기: 글립, 요누르, 아볼라이트, 게아몬트, 원자 용광로, 겔세미스,
  파워 큐브, 누올리스, 야옹스터(meownster).
- 글리치 Gleeful. → '기쁨.'.
- QA: 구조 0건.

### 0936 (65671~66615, 100건)

- 종족 혼합 + 퀘스트 'Give X ...' 반납문 — '~에게 X 전달' 통일.
- 표기: 프로자, 유니온, 실더, 아넬리스크, 지오모아, 게아토른, 기트신,
  길/길리카다, 길텐, 안쿠, 마리나, 엘리멘탈 하트/정수, 호라이즌 테크 카드,
  고대 회로, 강화 배터리, 레나틴 수정, 크토니안, 히미드, 제너럴 무니션스.
- 글리치 Frustrated. → '좌절.', Glad. → '다행.'.
- 'GET JINXED!' → '징크스에 걸려라!'.
- 'Geoarge!'는 원문 오탈자 → '조지!'.
- QA: 구조 0건.

### 0935 (65046~65637, 100건)

- 종족 혼합: droden/apex/floran/slimeperson/akkimari/neki/saturn/hylotl/
  human/annelisk/moogledescription 등.
- 표기: 제이미 도우, 프랙툴, 모포시스 파편, 새터니안, 루인(The Ruin),
  대수호자, 이오, 아야카/아야 가루, 무시.
- 글리치 Frightened. → '공포.'.
- QA: 구조 0건.

### 0934 (64743~65044, 100건)

- 플로란 대량 + hylotl/avali/avian/lustling/glitch 소량.
- 인명/표기: 프로자, 오를라, 에롤, 텐리, 생크틸라이트.
- 글리치 Focused. → '집중.' (TM 관례).
- 64968 alta 'Foamyy, yayy~~' → '거푸미, 예이~~'.
- QA: 구조 0건.

### 0933 (64573~64742, 100건)

- 전량 플로란 조사문 — 말투 유지.
- 표기: 에민스노우, 문멜론, 야라, S.A.I.L, 일렉트로걸(electrogirls).
- QA: 구조 0건.

### 0932 (64427~64570, 100건)

- 전량 플로란 조사문 — 말투 유지.
- 표기: 웜온치, 고스호크단, 수호자들, 러스틀링.
- 64534 skeletondescription은 스켈레톤 화자의 서술체라 평문 처리.
- QA: 구조 0건.

### 0931 (64283~64426, 100건)

- 전량 플로란 조사문 — 말투 유지.
- 표기: 루모스, 팝탑, 초코보, 모글, 펌프킹, 락사사, 하트우드.
- QA: 구조 0건.

### 0930 (64052~64282, 100건)

- 전량 플로란 조사문 — 말투 유지.
- 인명/표기: 메르시발, 메르시아, 파아리, 코지, 돌리, 와일드캣, 조지,
  그린핑거, 전기 수액.
- QA: 구조 0건.

### 0929 (63904~64051, 100건)

- 거의 전량 플로란 조사문 — 말투 유지.
- 표기: 무시(Mooshi), 착유기, 메타버스, 나디아, 컬티베이터.
- hylotl 63975 'Floran don't design tech; they consume it'는 관찰 서술체로 처리.
- QA: 구조 0건.

### 0928 (63779~63903, 100건)

- 전량 플로란 1인칭 조사문 — 기존 말투/오탈자 반영 유지.
- 원문 오탈자(deosn't, disslikesss 등)는 의도된 플로란 어투로 간주, 뜻만 반영.
- 0927 잔여 처리: 원문 63264의 누락된 ^reset;를 복구하고 qa_structure KNOWN_OK에 등록
  (25930과 동일 사례).
- QA: 구조 0건.

### 0927 (63252~63778, 100건)

- 퀘스트 'Find X at Y' 반납문 — '~에서 X 찾기' 명사형 통일.
- 지명/인명: 아스트랄 천문대, 네레우스 박사, 에메랄드 글림프스, 노엘,
  회상의 판테온, 바르노스/차차라/페이즈(크레온 대사관), 카민/자페라(라이트헤이븐),
  빈더밀, 코버넌트-켈치스(아키마리 신·고향), 플래시 핀즈.
- 표기: 에터니아/엔테라시/EDS, 플롭볼(레테이아 패러디 유지), 살주머니(flesh bag).
- 플로란 1인칭 대사 다량 — 기존 말투 유지.
- QA: 구조 0건.

### 0926 (62629~63245, 100건)

- 글리치: Fascinated(매혹), Fascination(매혹), Fatigue(피로), Fear(공포),
  Fearful(두려움 — 62808/62814 관례), Familiar(익숙).
- 표기: 파로(Enerth 정비공), 스캐버란, 포크툭, 스텔라 팬피시, 샌드스토커,
  제노프로브, 펠하임, 푸시아의 50가지 그림자(패러디), 줄무늬 깃발 도적단.
- NL1 행의
 보존.
- QA: 구조 0건.

### 0925 (62069~62620, 100건)

- 글리치 'Excited.'(흥분 — TM 관례) 대량 + Excitement(흥분), Exhausted(지침),
  Expectant(기대), Facinated(매혹 — TM), False(거짓), Familiar(익숙).
- 표기: 테라마트, 스모그질라 대 킹 스나운트도라, 연금 권총, 글림레쿠스,
  저장 물질, 프로젝트 45, USCM, 드레이(alta 동물), 라이오드 텐트,
  영구동토 행성, '동굴 속 아버지'(그린핑거 구전).
- QA: 구조 0건.

### 0924 (61671~62068, 100건)

- 글리치 'Error.'(오류) 접두사 추가. 'Even...' 계열 종족 대사 다수.
- 표기: 에스더 브라이트/아스라 녹스/전대 대보호자, 에론 수호자, 에롤,
  료타/텐리/메르시아, 텔(Thell 종족), 해골 거울, 아보스크립트, 마기사이트,
  액티안, 에보아쿠아틱, 팝탑, 세지, ASA-26 레인저, 크라코스어.
- 'butt-on' 말장난은 원문 병기로 의미 유지.
- QA: 구조 0건.

### 0923 (60826~61659, 100건)

- 글리치 E-계열 완결: Elated(의기양양 — TM), Enamored(반함), Enchanted(황홀),
  Encouraged(고무), Energetic(기운), Entertained(즐거움), Enthralled(매료),
  Enthusiastic(열광 — 15371 관례), Enticed(유혹 — 15375 관례), Entranced(넋잃음),
  Envious(부러움 — TM), Empatic(공감).
- 세력/지명: 엘리시아(행성·동맹), 에지/드레메톤/아에기니안/노틱스/드라우나르,
  엘피스, 에민스노우, 츠키카게 일족, 에메릭/펠하임/체리스톤/메르시아,
  그린핑거, 엘루냐/아엘티리, 조상족, 슬러그개구리, 에터니아, 에오르지안.
- QA: 구조 0건.

### 0922 (60185~60825, 100건)

- 글리치: Dreaming(몽상), Dumbfounded(어리둥절), Eager(열망 — 60571~92 관례),
  Dry observation(건조 관찰).
- 표기: 드렉(Drehk 차량), 셸가드, 오버클럭/오일라거(글리치 주류), 에셜론(기업),
  듀라스틸, EDS 갑옷, 아야카, 아야 가루/이조 잼/마리, 아보스, 솔 시스템.
- neko 인터넷 뉘앙스('냥' 종결) 유지, felin '그루비' 뉘앙스 반영.
- QA: 구조 0건.

### 0921 (59669~60183, 100건)

- 글리치 'Doubtful.'(의심), 'Dread.'(공포) 추가.
- 표기: 츠키카게 일족, 루미나리움, 바이오니드, 스캐비, 드레드윙,
  플레이스테이션, 전기 양(페러디 유지), 포노다인/파우노다인 없음 — faunodyne은
  이번 배치 미포함.
- QA: 구조 0건.

### 0920 (59201~59666, 100건)

- 글리치 Dis-계열 완결: Disheartened(낙담), Disinterested(무관심), Dismayed(착잡),
  Dismissive(깔봄), Displeased(불편), Disregard(무시), Distraught(비탄),
  Distressed(괴로움), Distrust(불신), Disturbed(동요), Dizzy(어지러움).
- 멸시 계열 구분: Demeaning=경멸, Derisive=조롱, Disdain=멸시, Dismissive=깔봄.
- 표기: 언바운드(세력), 스타포지, 제노프로브, 무시(생물), 지옥 돌,
  완벽주의 가문, 제이 이지, 파우노다인 글리프 코드 보존.
- QA: 구조 0건.

### 0919 (58863~59200, 100건)

- 드로덴 'Detected' 보고문 완결.
- 글리치: Determined(결단), Disappointed(실망 — TM), Disapproving(못마땅),
  Discomforted(불쾌), Disconcerted(당혹), Discontent(불만 — TM), Disdain(멸시,
  Demeaning의 경멸과 구분), Disgust/Disgusted(혐오/역겨움 — TM 혼재, 혐오로 통일).
- 표기: 라데이스(드로덴 신상), 크라코스(K'Rakoth), 레테이아, 플롭볼(ㄹ 빼기 말장난 유지),
  나이스마이스/바즈텟/나이즈마이즈(z화자 — '쥬' 어미로 재현), 포스포리온, 기트신,
  테라포머, 에코 포드, 살룬 밀주.
- 네키 외설 표현 수위 유지('좆같은').
- QA: 구조 0건.

### 0918 (58758~58862, 100건)

- 드로덴 'Detected' 보고문 연속 — 전량 '감지' 양식, '분석:/상태:/권장 행동:' 태그 통일.
- 세력 표기: 아에기니안 연방, 드레메톤 도시연합, 엘리시아 동맹, 에릭시안 공화국,
  하이졸리아 하이미디안 공화국, 노티시안 연방, 트링크 서킷, 삼중 군주국,
  감시자들의 눈, 뱅가드(크랄 격납고), 노마다.
- 인명/지명: 오딘 아스-라데이스, 엘리시아, 카다반.
- 드론 모델: 아비터, 플릭, 저스티카.
- QA: 구조 0건.

### 0917 (58295~58757, 100건)

- 글리치: Deja vu(기시감), Dejected(낙심), Delighted(기쁨 — TM 관례), Demeaning(경멸),
  Derisive(조롱), Description(설명), Destructive(파괴충동), Detachedly(무심).
- 드로덴 'Detected' 기계식 보고문 대량 — 'X 감지. 상태: Y' 양식 통일.
- 표기: 휴렛 데카드, 노바호스, 펭귄 피트, 봄박스, 포스포리온, 노마다, 텔헌터,
  라이오드, 드랄/드랄리드/크랄/레기온/스코프/텔리안 강습함, 아프로디테, 네오,
  엘리엇, 에스더, 오렌지(NPC), 중무장 평화유지군.
- 퀘스트 반납문은 '전달하기' 명사형, 색 태그 보존.
- QA: 구조 0건.

### 0916 (57597~58294, 100건)

- 글리치 'Curious.'(호기심) 완결 + 'Dazzled!'(눈부심), 'Deadpan.'(무표정, 신규),
  'Deductive.'(추론 — TM 관례), 'Cute.'(귀여움).
- fenerox 피진 말투 유지('죽은 새. 예이!'류), NL1 줄바꿈 보존.
- 표기: 메로스 아반, 테서랙트, 스노알타, 소나베일, 텔리안, 루나, 파멸(The Ruin),
  미코톡신.
- QA: 구조 0건.

### 0915 (57484~57595, 100건)

- 글리치 'Curious.'(호기심) 시리즈 계속.
- 표기: 루모스, 폴리래디시, 볼트스피터, 아쿠아리, 모트랩, 나이트폴 계획,
  루바이트/아볼라이트 대비, 태양 나방, 기잘 채소, 쿠포 너트, 엠버 산호,
  엘리시아 동맹, 하드라이트, 아틀라스/컬티베이터.
- QA: 구조 0건.

### 0914 (56934~57483, 100건)

- 글리치 'Critical.'(비평 — 14713/14714 관례), 'Crying.'(울음, 신규),
  'Curious.'(호기심 — 20행 관례) 대량 시리즈.
- 표기: 크토니안, 잿빛 행성, 대보호자, 포획 포드, 모스맨, 프로그, 유카이,
  아비칸, 루시, 오토마톤, 트링크.
- QA: 구조 0건.

### 0913 (56238~56933, 100건)

- 글리치 'Confused.'(혼란) 완결 + 'Considerate'(배려, 신규), 'Contemplation'(사색),
  'Contemplative'(생각 — TM 관례), 'Content'(만족 — 56489 관례), 'Cozy'(아늑, 신규).
- 표기: 에너스 엔지니어링, 파놉티콘, 행성 보호국, 생크틸라이트, 톤나카다,
  코버넌트 깃발(드로덴), 심비오트, 하루토 선장, 센텐시안 스테이시스 포드.
- QA: 구조 0건.

### 0912 (56069~56237, 100건)

- 글리치 'Concerned.'(걱정) 대량 시리즈, 'Conclusive'(결론, 신규), 'Confident'(자신감),
  'Conflicted'(갈등 — 1090/56180 관례), 'Confused'(혼란 — 5568/5572 관례).
- 표기: 볼트로폴리스, 코어 가루, 노상강도, 스모글린, 글립, 돌리, 첼시, 페린,
  지상 난초(Terrene orchids), 초폭풍 지대.
- QA: 구조 0건.

### 0911 (55118~56064, 100건)

- 글리치: Comfortable(편안), Comforted(편안 — 598행 관례), Comical(희극 — 14538 관례),
  Compassionate(자비), Compelled(이끌림), Concern(걱정 — 56062~68 관례).
- 손상된 글리치 문장(Co2Fus3D...)은 한글 리트 스타일로 재현.
- 표기: 크로늄, 클레어 고프, 촉수 도전 던전, 누올리스, 잭오랜턴, 세리스, 에로스.
- QA: 구조 0건.

### 0910 (54503~55108, 100건)

- 글리치 'Cautious.'(주의.) 대량 시리즈 완결, 이후 'Captivated/Cautivated'(경탄),
  'Charmed'(매혹), 'Cheeky'(짓궂음), 'Cheered up'(활기), 'Cheerful'(즐거움),
  'Cheery'(쾌활), 'Certain'(확신, 신규 — 명사형).
- 표기: 미니크녹, 호버바이크, 액체 질소, 페네록스, 우피, 알테르니아/헤비칼/알테칼,
  크레온 대사관, 유물 재건기, 데이리드(신규 인명), 첼리스/첼시 구분, 초코보.
- QA: 구조 0건.

### 0909 (53594~54502, 100건)

- 글리치 'Cautious.' 시리즈 대량(주의. 통일), 'Captivated.'(경탄), 'Careful.'(주의).
- 'Cataloguing.' → 목록화. (신규 감정 접두사, TM 없음 — 명사형 규칙 적용)
- 표기: 완더월, 세터니아, 스코프(아비칸 함선), 불가사리, 삼극 별, 화염 플러팔로,
  저온 화산, 지하감옥(oubliette), 알테라시 행성, 메카 격납고.
- lustling 외설 표현은 은유 없이 직역 수위 유지('박다').
- QA: 구조 0건.

### 0908 (52808~53589, 100건)

- 종족 조사 대사 계속(글리치 '평온' 시리즈, 아키마리, 플로란 먹이 질문).
- 표기: 메이, 키위 주스, 우롱차, 노움, 불러시, 트랩루트, 카이사르, 클룩스의 분노,
  컬티베이터/창조주/위대한 오지/무수한 진리/여왕님(신급 호칭).
- 글리치: Calm→평온, Calmed→진정 (형용사형 어미 회피, 명사형 유지).
- 신규 종족 harpy/skeleton/dremeton은 기본 조사체.
- QA: 구조 0건.

### 0907 (52511~52807, 100건)

- 종족 조사 대사 + 퀘스트 반납문(turnindescription) 다수.
- 표기: 뇌간 나무, 브릭스 조선, 유니온, 포이, 아이소슬라임, 에로스.
- 퀘스트 인명/지명: 안쿠(천문대), 수상한 상인, 노바 스테이션, 엘라나, 론딘, 윌, 캐시디,
  트위터스, 크리더스, 스트렐리치아, 크레이턴, 레이저윙, 주시 연못, 후이.
- 퀘스트 물품: 외계 잼, 아네모네 목재, 비전수, 아보스톤, 블릭 어셈블러, 빛나는 물, 네온물,
  옴트리 조각, 생 더스트리움, 강화 프레임, 레나틴 파편, 루페스사이트, 슈퍼 별, 텅스텐 주괴,
  볼타 파편, 휘장, 아크 파편, 참수검 부품, 드래곤헤드 권총, 빈 에너지 셀, 에르키우스 연료,
  헬볼, 임페르비움 검, 익소둠 발톱, 날카로운 발톱, 스타 브레이커, 티타늄 주괴, 직조 천.
- 반납문은 'X를 Y에게 가져가기.' 명사형, 색 태그 보존.
- QA: 구조 0건.

### 0906 (51661~52510, 100건)

- 종족 조사 대사 계속(플로란 '큰~' 시리즈 마무리, 글리치 '지루' 시리즈).
- 표기: 매지파이어, 볼트 구근, 바이온플라이, 청사진(Bluepints 펀), 파란 얼음,
  폭염 행성, 브릭 로드, 공성추.
- 글리치: Bored→지루, Blasé→시들.
- QA: 구조 0건.

### 0905 (51323~51660, 100건)

- 종족 조사 대사 계속(글리치 '당혹' 시리즈, 플로란 '큰~' 시리즈 대량).
- 표기: 나이트폴, 니베라 센티아, 브루트파리, 왜곡 지대, 크라코스, 코어 가루,
  방사성 플러팔로, 플래시라이트→자위기구(원어 뜻 살려 번역).
- 글리치: Befuddled→당혹, Bemused→어리둥절, Bewildered→당혹.
- QA: 구조 0건.

### 0904 (50679~51322, 100건)

- 종족 조사 대사 계속(글리치 '당혹' 시리즈, 아야/액시엄, 아키마리 단어체, 플로란).
- 표기: 액시엄 엔터프라이즈, 아야/아야 벌/아야카, 페인틀린, 머드미지, 클룩스,
  안락한 부리 술집(Beakeasy Bar), 야라, 노마다, 바시, 바이온, 베이터.
- 51297 ^#b0e0fc; 태그 보존. Beakeasy 계열은 바 이름은 TM '안락한 부리 술집' 채택.
- QA: 구조 0건.

### 0903 (50535~50676, 100건)

- 종족 조사 대사 계속('어우~' 감탄문 다수, 글리치 경탄/경외 시리즈).
- 표기: 아보스, 페닉스, 심비오트, 미코 허니(색 태그 보존), 아샬, 플라잉 버트레스,
  글리치 구브, 건십.
- 글리치: Awe/Awed→경탄, Awestruck→경외.
- neko 종족도 기본 해체 유지, nya는 냐 보존.
- QA: 구조 0건.

### 0902 (49537~50534, 100건)

- 종족 조사 대사 계속(글리치 감정어 다수, 아발리 종족 설명, 아비칸 알 시리즈).
- 표기: 모히타바, 시간 방랑자, 레테이아사, 아주리움, 엠피리언, 앵글루어, 팝탑, 휩쓸림,
  아스라 녹스, 스캐배런, 아벤토르, 무시, 아키마리 비단, 그래핀 직조 감방.
- 글리치: Astonished→경탄, Astounded→경탄, Attentive→주의, Ashamed→수치, Assuring→안심.
- QA: 구조 0건.

### 0901 (48793~49530, 100건)

- 종족 조사 대사 계속(글리치 '평가/감사/승인' 시리즈, 아르막스·네키 적절한~).
- 표기: 아볼라이트, 배드 문, 물질 조작기, 아케인 위어드, 슈퍼보이드, 새터니안,
  아르막스 시큐리티스, 아릭, EPP, 헤이븐 꽃, 48구역.
- 글리치: Appraising→평가, Appreciative→감사, Approving/Approval→승인 (TM 관례).
- QA: 구조 0건.

### 0900 (48362~48792, 100건)

- 종족 조사 대사 계속(글리치 '짜증/불안/경악/기대' 시리즈, 알타 생물학, 아키마리 단어체).
- 표기: 물고기 인간, 생크틸라이트, 지오모아, 알테라시, 플로라스톤, 해골 거울, 안토라시,
  켈치스, 아크리스, 칼린 크리핏, 아쿠아리, 오리움, 보봇, 컬티베이터, 별빛 음식, 비리데슨트.
- 글리치 감정어는 TM 관례 유지: Annoyed→짜증, Anxious→불안, Appalled→경악, Anticipating→기대.
- QA: 구조 0건. 48778은
과 ^gray; 태그 보존.

### 0899 (47936~48359, 100건)

- 종족 조사 대사 계속(글리치 '분석적.' 다수, 고대~, 천사 관련 행).
- 표기: 라인 라이플, 스타사이트 여관, 텔 사냥꾼, 보리얼라이트, 작열 타이가, 우프, 글립,
  알키어, 헬리온족, 우누스트렐로의 별빛 카페, 홍관조, 전기화학 시설.
- 글리치 'Analytical.'은 감정어 관례에 맞춰 '분석적.'으로 통일.
- QA: 구조 0건.

### 0898 (47723~47935, 100건)

- 종족 조사 대사 계속(불편한~시리즈, 드로덴 분석 보고서 다수).
- 표기: 스킵라이플, 샌드스토커, 뱅가드, 엘더, 데몬(종족명), 아키마리제, 센텐시안.
- 드로덴은 기계식 명사구 보고체(분석 완료. X 감지.), 글리치 'Analyse.'는 TM 관례 '분석 중.'.
- 신규 종족 thelean/hyvon/droden는 전용 규칙 없어 기본 조사체(드로덴은 보고체).
- QA: 구조 0건.

### 0897 (47437~47719, 100건)

- 종족 조사 대사 계속('낡은~' 사물 다수, 장식·유기물 시리즈).
- 표기: 기트신, 유물 수집가/유물 탐구자, 식민지 증서, 아발론, 트링키안, 광산 수레, 크라코스,
  방폭문, 생태실. neko 종족은 전용 규칙 없어 기본 조사체 적용.
- QA: 구조 0건.

### 0896 (47177~47436, 100건)

- 종족 조사 대사 계속(고대 유물, 흥미로운~시리즈, 노바키드 '낡은' 사물).
- 표기: 볼트스피터, 시투리아(촉매), 미니크녹 선전물, 해로잉 축제(아에기), 데몬, 바다돼지,
  비신 수정, 필멸자(엔젤이 타종족 호칭). removeditemrefund 키는 일반 서술로 처리(합니다체).
- 네키 brright -> 밝아알은, ol' -> 낡은 으로 말맛 재현.
- QA: 구조 0건.

### 0895 (46872~47169, 100건)

- 종족 조사 대사 계속(우아한~시리즈, 생태/행성 묘사, 네키).
- 표기: 엘린, 크림슨 스탠다드, 나르핀/옴니 나르핀, 바르다스, 애니머스, 릴로돈, 한밤 행성,
  에르키우스, 다크슬라임, 뉴럴링크 스캐너, 아쿠아포닉. 네키 fucky 계열은 완곡화 없이 번역.
- QA: 구조 0건.

### 0894 (46522~46871, 100건)

- 종족 조사 대사 계속(고대 유물 2차, 네키 다수, 생태실·알 시리즈).
- 표기: 센텐스/센텐시안, 평화유지군, 오세아나이트, 아르카니안, 플러팔로, 페롤릭, 하이올릭,
  톤노바(나선 용수철), 모그리, 생태실(eco chamber), 아쿠아포닉, 오라 결정화 제작대.
- 네키: ~다냥 어미 유지, 말장난은 종이냥·빙글빙글·몽글이 친구·갈아알색으로 재현.
- QA: 구조 0건.

### 0893 (46186~46515, 100건)

- 종족 조사 대사 계속(고대 유물·아비칸 가구·네키 조사).
- 표기: 엘리시아, 유카이, 마기사이트, 니베라, 앤서블, 테서랙트, 도가니, 점프소총(TM 다수파),
  고대의 존재들(Old Ones), 네키 말장난은 늘임 색(`갈아알색`)·`~다냥` 어미.
- QA: 구조 0건.

### 0892 (46013~46185, 100건)

- 종족 조사 대사 계속(외계 가구·기기류, 에어락, ECS, 크라코스 기기).
- 표기: ECS 그대로, 에어락, 페네록스, 펜론, 강습함, 크라코스(종족)/크라코탄(형용사),
  숫자 기호·숫자 판독 행은 아라비아 숫자 사용, 보호막(shield), 순수한 픽셀.
- QA: 구조 0건.

### 0891 (45701~46011, 100건)

- 종족 조사 대사 계속(아비칸·엘리시안 계열 가구/함선류, 언바운드, 천사풍).
- 신규 표기: 드렉/스코프(아비칸 함선), 센텐시안, 엘피스, 에너스 엔지니어링, 길텐, 인포스파이어,
  익소둠, 하이베리움, 언바운드, 아르코(색상 태그 보존), 스펙트윙, 배드 문, 스타마이트, 메카,
  돌격소총, 냉화산, 미아즈마, 비증강(unaugmented), 코만도/뱅가드 유닛, EDS 그대로.
- 45744·45951~45952는 색상 태그 구조 보존 확인. EDS status pod는 문맥상 스테이시스 포드로 번역.
- QA: 구조 0건, 내 기여 용어 후보 0건.

### 0890 (45547~45700, 80건)

- 종족별 조사 대사 계속. 논리 게이트 스위치(AND/OR/XOR/NAND/NOR)는 이름과 on/off를 원문표기 유지.
- 천사풍(Angelic)→천사풍, Angel→천사 구분. waypoint→순간이동 경유지(TM), hyperdrive→초공간 드라이브,
  end table→사이드 테이블, open sign→오픈 표지(TM 오픈 간판 계열), Alliance→얼라이언스.
- QA: 구조 0건, 내 기여 용어 후보 0건(코퍼스 드리프트 64건은 별도 과제).

### 0889 (45403~45546, 60건)

- 저우선 큐 개시: 종족별 조사 대사. 글리치 감정어(놀람/즐거움/감탄/야망/양면성/우호적) 규칙 재사용,
  Amorous 행성 유형은 아모러스(TM: 아모러스 테라포머), Plopball은 플롭볼, Gnome은 노움, amp는 증폭기.
- 플로란 행은 치찰음 없이 간결한 -다로, 알타는 기본 조사 규칙+원문의 물결 잔여톤(~) 유지.
- QA: 구조 0건. 용어 보고서는 64건 후보(전부 기존 배치 파일, 0889 기여 0건) — 용어집 243행 확장으로
  생긴 코퍼스 드리프트이며 35.1과 같은 별도 정리 대상.

### 0597 (123869~123918, 50건)

- 실탄/보호국 총기 사양 블록 계속(H&K~수색 구조대), 제조사명 음역 통일, 로켓 주의문·SRS코멘트·구급 키트 내용물 번역.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0607 (124442~124493, 50건)

- 세입자 종류 문서 대량(아트 위저드~솔라레이 대장장이, 0598 라벨 관례 재사용), 천사 유형코덱스, 고대인 코덱스, 하피 병 신문 2건, UI 문자열.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0608 (124494~124552, 50건)

- 효과음·음성 행(새소리, 포효 등), 무기 설명 블록(노마다/트링키안/드로덴/켈라키 등).
- QA: 구조 0건(124497 개행 정정 후 통과), 용어 오탐 4건 유지.

### 0609 (124553~124602, 50건)

- 무기 설명 블록 계속(아비칸 군 지급 무기, 트링키안 방패, 아키마리 땜질 무기 등).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0610 (124603~124652, 50건)

- 무기 설명 블록 완결, 알터-NV 플라즈마소드 장문 설명, 아르카나 검투사 문서.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0611 (124653~124718, 50건)

- 무기 설명 블록 완결, EPP/포획 포드 UI 문자열, 힌트·효과음 행.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0612 (124719~125175, 50건)

- 닭 품종 문서(아메라우카나·바드 플리머스록·블루 레이스드 와이언닷·버프 오핑턴), 크레딧페이지, 천사 신성력 코덱스 2편, 천상 회랑 개요.
- QA: 구조 0건(125087/125120/125125 태그 정정 후 통과), 용어 오탐 4건 유지.

### 0613 (125177~125311, 50건)

- 커뮤니티 에디션 인형/스티커 크레딧 대량, 하피 변화 코덱스, 천상·햄 안내 텍스트.
- QA: 구조 0건(125242 태그 정정 후 통과), 용어 오탐 4건 유지.

### 0614 (125313~125437, 50건)

- 닭 품종 문서 추가(골든 코멧·세브라이트·저지 자이언트·레그혼·라이트 브라마·말레이시아 세라마), 인형 크레딧, 천사 창세 코덱스(최초의 천사·루인킬러), 스타리 컬트 문서, 정수 출처표.
- QA: 구조 0건(크레딧 헤더 태그 정정 후 통과), 용어 오탐 4건 유지.

### 0615 (125438~125548, 50건)

- 닭 품종 문서 추가, 인형 크레딧 속편, 매지사이트/에르키우스 퀘스트 목표 문자열, 기술 설명(우루사 배낭 등).
- QA: 구조 0건(팩 헤더 태그·[Jump] 토큰 정정 후 통과), 용어 오탐 4건 유지.

### 0616 (125549~125629, 50건)

- 닭 품종 문서 추가, 스탯 마일스톤 표, 스펠오브/스펠스로어 설명, 유물 탐구자 소개, 스타리 행성 문서. (125517 `제작대` 용어는 0615 파일에서 정정)
- QA: 구조 0건(팩 헤더 태그 정정 후 통과), 용어 오탐 4건 유지.

### 0617 (125630~125790, 50건)

- 아스트랄 천문대·유물 탐구자 문서, 장신구 설명, SxB 채찍 설명, 마약류 스탯, 전원 장치명, 천사 매장·루인드 코덱스.
- QA: 구조 0건(125630 중첩 태그·125633 헤더 정정 후 통과), 용어 오탐 4건 유지.

### 0618 (125791~125900, 50건)

- 인퍼나이트/마젠타/널리움 계열 무기·물약·치료 아이템명, 표절 노래 인용 소총 설명 2건.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0619 (125903~125968, 50건)

- USCM 일지 4편, 임신 가이드 계속, ayylien 대화(자리표시자 보존), 오렌지 무기 설명 블록.
- QA: 구조 0건(125915/125916 태그 중첩 정정 후 통과), 용어 오탐 4건 유지.

### 0620 (125969~126032, 50건)

- 오렌지 무기 설명 블록 완결, 아차리 조언자·가속기 작업대 등 명명 행, AAE 소개.
- QA: 구조 0건(126018 태그 정정 후 통과), 용어 오탐 4건 유지.

### 0621 (126033~126096, 50건)

- 알타 제작 시설명 전수(아키텍트 스테이션~워크숍), 오렌지 무기 설명, 아케인 별 문서(행성유형 7종 확정).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0622 (126097~126168, 50건)

- 대천사 제케이지리엘 코덱스, 제작대·무기·세트 가방 명명 다수.
- 의도적 난독화(Buzz) 코덱스 3건: 태그 구조 보존하며 윙윙/꿀벌 토큰으로 치환(각 +2~+5 쌍보정 후 통과).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0623 (126169~126238, 50건)

- 에지니안 역사 코덱스 제0~5장(테라 탈출~연방 연합 성립), 제작대·무기·큐텐 용병 평판 시리즈.
- `Shield Bash`→`방패 강타` 고정 용어 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0624 (126246~126325, 50건)

- 에네르스 엔지니어링·엑스칼리버급 실드블레이드 코덱스, GDI 부품·제작대·무기 명명 다수.
- 태그 순서 불일치 2건 정정(126264, 126292).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0625 (126326~126407, 50건)

- 하피병 일지, FU 위키 안내, InkWarrior 크레딧 목록, 보이저 컴퍼니 소개, 바스테트 기도문등.
- 목표 지시문 태그 순서 2건 정정(126388, 126404).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0626 (126408~126472, 50건)

- 루나 총기 부품, 마지사이트 제작 시설, 메로스 아반 전시 코덱스, 미라지 별 문서.
- 126452: 몬스터 저항·무기 마스터리 대형 코덱스(NL267) 전수 번역 — 방패 강타/완전 방어/쌍수 용어 관례 적용.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0627 (126473~126542, 50건)

- 종족별 FTL/기술 스테이션 잔여, 전초기지 시설 시리즈, 페일 별 문서(행성 5종 확정 용어),Sexbound FAQ.
- 126484 태그 순서 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0628 (126543~126631, 50건)

- Sexbound FAQ 잔여, 리샨·루인드 천사 코덱스, 카다반 생물(샌드크롤러/샌드스피터), Raiizy·ShyDispatch 크레딧.
- 126631: 원문의 `#C67CEE;`(캐럿 누락) 오류 태그를 그대로 보존해 구조 일치.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0629 (126632~126682, 50건)

- "신호 탐지" 변환 힌트 시리즈 40건(오로타움/에소쿼츠/림-에레키우스/터마스린/익소사이트/오렌), 템플릿 일괄 생성.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0630 (126683~126772, 50건)

- 스팅윙 코덱스, 슈퍼스톰 별 문서(행성 6종: 익스팬스/네온 시/슈탈레른 불모지/타임리스/오토메이티드/비리데슨트), 랜딩 페스티벌·보이저 코덱스.
- 템플릿 행(126766/126767)은 원문 반복 구조를 프로그램으로 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0631 (126773~126836, 50건)

- 트라이폴라 별 문서(행성 6종 확정), 발라 코덱스, 어반 엣지·에네르스 광고, 업그레이드 총기 시리즈.
- 126802 태그 순서 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0632 (126773~126888, 50건)

- 양봉 대형 코덱스(126843), 러시아어 원문 행 한국어 번역, [Voyage] 음식 설명(토큰 리터럴유지), 러스틀링 종족 문서.
- 126840 태그·126866 키릴 [А] 토큰 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0633 (126889~126978, 50건)

- 기밀 노마다 감시자 문서 5건(바스 브할레이, 행성 보호국 침투), USCM 해산 지령, 아라사카무기, 병합 바이옴 라벨.
- `Terrene Protectorate`→`행성 보호국` 고정 용어 정정 4건.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0634 (126979~127091, 50건)

- 경고·금지 계열 문구 다수, F.F.S 임무 라디오, FFS 하드코어, 무지개 태그 명명(FREEDOM/Fervid Joy Hole), 치트 무기 스펙.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0635 (127092~127159, 50건)

- FFS 바닐라 던전·스타리 컬티스트·하피 면역 연구 코덱스, 글리치 공시, 엘레멘트리스 메커니즘, 사이버펑크 무기(캉 타오/밀리테크/미드나이트 암즈).
- `Alt Fire`→`보조 발사` 고정 용어 정정(0632 러시아 행 2건 포함). 0635에 잘못 병합된 행 2건 제거.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0636 (127160~127238, 50건)

- 케빈 위반 기록 통합본(127229): 기존 개별 번역 10건 조합 재사용. 팔라딘 이니셔티브 극비문서, 별빛 액체 연구, 루인 귀환.
- `Grand Protector`→`대보호자` 고정 용어 정정. 무지개 문자별 태그(127220) 재배치.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0637 (127241~127292, 50건)

- 행성 위험 경고 시리즈(방사선/독/황산/폭풍/전기/광채), WIP 알타 무기 설명 시리즈.
- `Stun`→`기절` 고정 용어, `stun` 오탈자 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0638 (127293~127347, 50건)

- WIP 알타 도구 잔여, 이리실 분기 보고서 시리즈(삑삑이/잘근이/리틀 빅 에이프), 하수구 골렘 일지(그림자 태그), 유물 상자 라벨.
- 127307 태그 정정(reset 추가분 제거).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0606 (124389~124441, 50건)

- ⟦E024⟧ 무기명 계속, 오파님/세라핌/세로할라핌 날개 등급표, 보호자 일지 4편, 천사 랭크업설명, UI 버튼 설명.
- QA: 구조 0건(124423 태그 정정 후 통과), 용어 오탐 4건 유지.

### 0605 (124339~124388, 50건)

- ⟦E024⟧ 무기명, 임신 안내서 코덱스(마지막 말/위험 요소), 면역 목록, 아일리엔·아비칸·트링크 의뢰 대사.
- QA: 구조 0건(124362 태그 순서 정정 후 통과), 용어 오탐 4건 유지.

### 0604 (124284~124337, 50건)

- USCM 모집 광고, 천사 종족 코덱스(규칙·장례·날개 등급표·죽음), irisil 모드 아이템 목록류.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0603 (124215~124277, 50건)

- 법 집행 함선 부품 잔여, 경찰 시설 방명, 항성명 무기(안타레스~비슈누), 잠입 작전 지시문, 대화 2건.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0602 (124165~124214, 50건)

- 법 집행 본부/키넬/연구소/함선 부품 명명 일괄.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0601 (124090~124164, 50건)

- FU 발전기 코덱스 3장 전수 번역(연료 기반/재생/붕괴 기반 — 연료 목록 전부 기존 정식 명칭 적용, 행 수·태그 수 일치 확인).
- 랭크 무기 그라디언트 태그명, 조자 간판, 키넬 함선 등 명명.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0600 (124037~124086, 50건)

- 제작대 시리즈(쿠로마츠/루예/모나크/오리온/타이탄코프 등), 소나베일 음식·스노알타·방한복 페이지, NPC 전용 경고문, 사이버펑크계 데이터 샤드, 임펄스 무기(러시아어명 포함).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0599 (123970~124036, 50건)

- 새터니안 세입자 가이드 마무리, 파라데아/아스테라 코덱스, 알터래시·타브리야 지형, 블루아카이브계 상자명, 아이템 명명 대량.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0598 (123919~123969, 50건)

- 실탄 총기 사양 블록 마무리(스미스 & 웨슨~발터), 수류탄/로켓 계열, 크로마 광석·레소나 블록 무지개 태그명, 소나베일 장식·세입자 가이드.
- QA: 구조 0건. 용어: `Tenant` 고정 용어는 `세입자` — 123964·123969 정정.

### 0596 (123817~123868, 50건)

- TC/타이탄코프 무기, 소나베일 파이, 네온 바다, 실탄 총기 사양 블록 대량(제조사별 동일 형식, 라벨 치환으로 공백행·태그 보존).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0595 (123760~123816, 50건)

- 소나베일 가이드 나머지 페이지, 스타더스트/이오 구조체 코덱스, TC 무기, 오토메이티드 행성.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0594 (123706~123759, 50건)

- 무기·아이템명 음역, S.A.I.L 탐사선 상태 메시지, 연금술 관련 아이템.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0593 (123638~123705, 50건)

- EDS 나머지 장비·함선 상태 UI, 발효·보존 라벨 시리즈, 아바의 날 코덱스(uwu 문체 재현),비리데센트·센본자쿠라 행성.
- 123657 색상 코드 오타 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0592 (123583~123637, 50건)

- EDS 장비 시리즈(기존 `EDS X` 관례 유지), 키카드, 젤리류, A.I. 합성 UI.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0591 (123531~123582, 50건)

- 작업대 시리즈, 행성 코덱스(에민스노우, 아주르 사막, 루이너스, 솔라라이즈드), 광기 대사, 포맷 문자열.
- Stock Ammo → 예비 탄약 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0590 (123469~123530, 50건)

- 총기·무기명 음역, 행성 코덱스(타임리스, 룬 사막, 엠피리언), 상점 UI 포맷.
- 123486 United Systems → 연합 시스템 정정, 123499/123500 누락 reset 태그 복원.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0589 (123409~123468, 50건)

- 행성 코덱스(슈탈레른 황야, 버밀리온, 아모러스), 세터니티 악몽 생물, 지아 회상 장면, EIA/EPF/ETMA 무기 시리즈 음역.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0588 (123230~123408, 50건)

- 실총 모델명 유지, 보호국 총기, OC 장비, 현대식 작업대 시리즈, 손상 코덱스 1건(태그 쌍 9개 보존).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0587 (123159~123229, 50건)

- 알타 요리 코덱스 시리즈(칼린·니아·야바·루네바 요리, 소나베일 안내서, 알리아나 여제 공식 발표), 함선 상태 UI, 무기명 음역.
- Gheatsyn → 기트신 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0586 (123074~123158, 50건)

- 아발론 방위 함대 총기 사양 블록 16건: 기존 번역(24840) 라벨 관례 재사용, 공백행 보존.
- 123079 원문 오기 `%25`를 자리표시자로 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0585 (122991~123073, 50건)

- 무기명 음역, 애니머스/블리스터링 행성 코덱스, 번팅 가구, 베테랑-방랑자 아키타입.
- 케빈 위반 기록 대형 코덱스 13건: 동일 내용의 개별 항목 기존 번역(48869~96196)을 재사용해 조합, 신규 9건(8/12, 8/22, 8/23, 2/10, 3/1, 5/15, 11/16, 11/17, 10/10)만 직접 번역.
- 행 수 검증: 전 행 원문 개행 수와 일치. QA: 구조 0건, 용어 오탐 4건 유지.

### 0584 (122935~122990, 50건)

- 엘리시안 동맹 마무리, 윈즈웁트 행성, 아이템·무기명 음역 일괄.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0583 (122882~122934, 50건)

- 이세 신궁 요괴 총 대사, GDI 무기명, 엘리시안 동맹 아이템 일괄.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0582 (122816~122876, 50건)

- 사이버펑크 무기 설명 대량(밀리텍/아라사카/노코타/말로리안 등).
- 워프드 숲, 슈퍼스톰 익스팬스, 대나무 숲 행성 묘사.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0581 (122758~122815, 50건)

- 아이리사 일기, 델라메인 사이버펑크 거래 텍스트, 아케인 아츠 마법서
  (약초학/마법 입문), 정령 수호자 종족 특성표, 사이버펑크 무기 설명.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0580 (122703~122757, 50건)

- 애저 해/버던트 행성, 소나베일 코덱스, 무기명 다수(라틴식 음역).
- `차원문`→`포털` 고정 용어 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0579 (122646~122702, 50건)

- 무엔즈카 로켓/미사일 사양, 세터니티 코덱스, 비오나/엔터니아 세계관 텍스트.
- 122655 원문에 없는 reset 태그 추가분 제거.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0578 (122591~122645, 50건)

- 무엔즈카 총기·방탄방패·크로스보우 설명, 스팀팩/의료키트 목록.
- 고정 용어 적용: DEF→방어력, Grenade Launcher→유탄 발사기.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0577 (122533~122590, 50건)

- 스타리 바이옴 우주 생물 도감(우주 드래곤/별게/스타라이트 등).
- 무엔즈카 총기 설명 시리즈(M4A1/SPAS-12/글록18/벡터 등) — 실총 사양 직역.
- 구 `우주 용` 표기를 `우주 드래곤`으로 정규화(20679 포함).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0576 (122477~122532, 50건)

- 캇파 코포 아키타입 대형 설명(에너지 레벨/실적 점수/페널티 체계).
- 니토리 인더스트리즈 무기·여권·Warframe식 무기명 음역.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0575 (122403~122472, 50건)

- 항성명 무기(알타이르/안타레스/카노푸스 등), 소나베일 명절 코덱스,
  어비설 우즈·터뷸런트 행성 묘사.
- 글자별 색상 분절(인시디아/모리/아자토스)은 태그 수 유지하며 음역.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0574 (122333~122402, 50건)

- 야라 숲·아야카 숲·바이오닉 복합재 코덱스, 샤이닝 시/나이트미스트 행성 묘사.
- 표기: EDS, 아야카/아야, 아르카니움, 워프드 — 기존 관례. 파라디아, 비신 등 음역.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0573 (122278~122332, 50건)

- 알테라시/알타 코덱스 페이지(세터니티, 에세테라, 완벽한 요리 가이드 등).
- 표기: 알타, 세터니티/세터니아, 엔터니아, 에세테라, 코이와, 야라 — 기존 관례 유지.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0572 (122208~122277, 50건)

- 천사 글리프 대사 후반, Big Ape/미니크녹 사양표 시리즈 번역.
- ⟦E0xx⟧ 코드 보존, 괄호 해설만 번역. 미니크녹 고정 표기 적용.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0571 (122158~122207, 50건)

- 알데론 함선 상태 블록, 천사(angel) 글리프 대사 시리즈.
- ⟦E0xx⟧ 글리프 코드는 보존, 괄호 안 영어 해설만 번역.
- 122181 에보아쿠아틱 바이옴: 태그쌍 누락 1건 수정 후 통과.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0570 (122102~122157, 50건)

- SAIL 상태창 텍스트 블록(승무원 상태/목표/함선 상태) 번역.
- Federal ARMY/Marines/Special Force 대형 무기 사양표 시리즈 —
  태그·탭 공백·줄 구조 1:1 보존, 사양 라벨 한국어화(조준 속도/탄도 사양 등).
- 스탯 블록 122134는 기존 종족 특성 관례(저항/면역/특성) 적용.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0569 (122052~122101, 50건)

- 태그 프리픽스 아이템 명명 일괄: 새터니안/타우모스 깃발,
  물약병 색상 시리즈, 마법 봉(배턴) 계열.
- 용어: 키테란, 이오, 솔, 악티아스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0568 (121999~122051, 50건)

- 장식용 물약 시리즈 + 정규식 패턴(원문 그대로) + [과학] 기구 명명
  + 태그 프리픽스 아이템 명명(`^#000000;` 등 코드 그대로 보존).
- 용어: 와스프밈, 타우모스, 새터니안, 아르카나, 유로달러.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0567 (121949~121998, 50건)

- SxB 명명 마무리 + 대괄호 군사 유닛(유니탄/웨스트 스타/Y.F.F.S)
  + 대괄호 서사 메시지 일괄.
- 용어: 웨스트 스타, 유니탄, 야마와로, 스파이넷, 늑대 텐구.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0566 (121899~121948, 50건)

- SxB 가구/테스트 아이템 명명 일괄(성별 라벨 암/수/중).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0565 (121848~121898, 50건)

- 니토리 인더스트리 유닛 + 프라임 아키타입 2종 + 라디오 트랙
  + 루인 스폰 몬스터 + SxB 가구 명명 일괄.
- 용어: 모아, 게슈탈트, 루인 스폰, 익소둠, 리페어로.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0564 (121798~121847, 50건)

- 필요 아이템 라벨(N.I.C/네시/YFFS 여권) + 사자 대대 유닛 명명
  + [ML] 요리 명명 + [기계] 리페어로 색상 시리즈.
- 용어: 리페어로, 칼리 피스키퍼 위원, 요괴/인간 루트 선택기.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0563 (121743~121797, 50건)

- 대괄호 시스템 메시지·임무 브리핑 일괄 + 블랙 옵스 총기 후반
  + 에르키우스 몬스터 명명 + 드론 전투 로그(NL22 보존)
  + GLORY 난이도 설명.
- 용어: 데스존, 스페이스 헐크, 연합 시스템, 진-글로벌, 피스키퍼 위원.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0562 (121693~121742, 50건)

- [블랙 옵스] 총기/탄창 명명 일괄(rnd→발, Magazine→탄창,
  One/Two-Handed→한손용/양손용, Slug→슬러그, Drum→드럼).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0561 (121638~121692, 50건)

- 제르세슘 무기 명명 마무리 + Z~ 대괄호 시스템 메시지/명명 일괄
  + 조로아크·적응형·전투 전문가 대형 능력치표 3종.
- 용어: 조로아크, 아키타입(=Archetype 고정), 소검(=Shortsword 고정 정정),
  지노푀르, 자사 찻주전자.
- QA: 원형→아키타입/숏소드→소검 정정 후 구조 0건, 오탐 4건 유지.

### 0560 (121565~121637, 50건)

- `Your...` 대사 마무리 + Y~Z 머리글자 명명 일괄(요괴군 후속 총기류,
  유카이/유키무라/유라구미/잔다름/자스타바/자완/제르세슘 시리즈)
  + 우우체 시 1건(표현 보존) + ZZZZ 디버그 미믹 4종.
- 용어: 제르세슘, 자완, 유카이, 유키무라.
- 고정 용어 정정: 유탄발사기→유탄 발사기(121593).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0559 (121512~121564, 50건)

- `Your...` 대사 일괄 + 알리아나 성채 승인 서신 + 엘리트 드라흘 임무.
- 용어: 자히드 사령관, 알리아나, 엘린 정원, 별관측자, 흙성게,
  침해된 엘리트 드라흘, 이브이/루카리오.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0558 (121462~121511, 50건)

- `Your kind...` 종족 잡담 + 메카 조작법 튜토리얼 + 크라코스 함선 발견 서신
  + 마법석/수정체 서사.
- 용어: 위스퍼, 나르핀, 루모스, 노틱스, 버던트 크레센트, 센텐.
- QA: 121502 `^#FF1493;` 2개 누락 수정 후 구조 0건, 용어 오탐 4건 유지.

### 0557 (121411~121461, 50건)

- `Your...` 대사 일괄 + 탐구자 첫 과제 서사(기적/플린트/로드스타)
  + 종족 특성 뷰어 인벤토리 안내.
- 용어: 지엔, 종족 특성 뷰어, 타임피스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0556 (121356~121409, 50건)

- `Your...` 종족 잡담 + FU MM 핵심 장비 설명(기능 키 태그 보존)
  + 네키 발톱/발톱 코덱스.
- 용어: 아볼라이트, 센텐시안, 빔액스, 크랄 점프제트.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0555 (121303~121355, 50건)

- 요괴군/요괴 요새 명명 일괄 + 형이상학 월간 가이드(NL8 보존)
  + 펀치 동료 설명 + 아비안 성장 코덱스.
- 용어: 요괴, 길텐, 엠피리언, 펀치, 크랄, 클루엑스, 형이상학 월간.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0554 (121253~121302, 50건)

- `You've...` 대사 일괄 + 아우레아 컬렉티브 도입 서사(카민/탐구자 시련)
  + 알타 장비/스캐너/데이터매스 발견 튜토리얼 일괄.
- 용어: 아우레아 컬렉티브, 탐구자 시련, 플린트, 갤리온, ST 실렉티스,
  솔라 화염 방출기/연막기, 변환술, 조절기.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0553 (121200~121252, 50건)

- `You're...` 후반 대사 일괄 + 종족별 고대물 수집가 안내 5종
  (에이펙스/아비안/플로란/글리치/하이로틀) + 루인 표면 도입문.
- 용어: 성점술사, 페리미터 III, 시커, 샐리/브루톨.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0552 (121150~121199, 50건)

- `You're not...` 계열 대사 일괄 + 데이터볼트 침투 안내.
- 용어: 제노톡스, 악티아스, 알타 방패.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0551 (121099~121149, 50건)

- `You're...` 대사 일괄 + 무기 업그레이드 완료 문구 2단계 7종
  (베르사 리코셰/사이펀 스포어·레이저·플럭스/블러드 에테르/프라임드 노바/
  바이탈 이지스/레이버너스 스파이라).
- 용어: 빈더밀 양, 샐리, 약탈자 습격 서사.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0550 (121045~121098, 50건)

- `You're/You'll...` 대사 일괄 + 무기 업그레이드 완료 문구 6종
  (베르사/사이펀/에테르/노바/스피라/이지스 → 개량된 모루 파생 무기).
- 용어: 엑소시안, 우주 유랑자, 흡수낭, 굶주린 스피라 등 기존 명명행 우선.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0549 (120993~121044, 50건)

- `You'd/You'll...` 대사 일괄 + 크라코스 미신 비판 코덱스 + 사막 장비 3종.
- 용어: 아스트랄 천문대, 선댄스 보이, 체이스플라이트, 엘리시아 연합.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0548 (120941~120992, 50건)

- `You will/won't...` 대사 일괄 + 출산 예고 메시지(시간 기준 6종) + 로드스타 신전 안내.
- 용어: 로드스타 신전, 하피 병, 트랜스로케이터, 석화된 촉- 교단(원문 절단 보존).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0547 (120888~120940, 50건)

- `You want/take...` 대사 일괄 + 현상금 보상 안내 + 이중 총열 산탄총 설명.
- 용어: 피스키퍼, 노바 스테이션, 노엘, 호라이즌 함대, 이중 총열.
- 120926 원문이 `^green;` 닫기 없이 끝남 — reset 추가하지 않고 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0546 (120837~120887, 50건)

- `You should/smell...` 대사 일괄 + N.I.C 네시 프록시 임무 브리핑.
- 용어: 네시 프록시, 프로토 제어 모듈, 별의 광신도들, 가짜 하피,
  비리데슨트 차, 주시 쟁반, 마그노브, 고름 자두.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0545 (120785~120836, 50건)

- `You seem/should...` 종족별 대사 일괄 + 시간을 초월한 별 시계탑 안내.
- 용어: 클루엑스, 노마다, 이온 타임피스, 탈라소 전초지, 플러그, 사이솔,
  마리코, 광기 획득.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0544 (120681범위 뒤 ~120784, 50건)

- 아키마리 경비 대사 + 종족 잡담 + 강화 팩/증강 부품 튜토리얼.
- 용어: 강화 팩, 환경 보호 팩(EPP), 증강 부품, 아에기니안, 노바라임, 프라이카스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0543 (120681~120732, 50건)

- 종족별 잡담 + 소환 의식 안내문 + 튜토리얼 이동 안내.
- 용어: 크라코스, 빅 에이프, 텔, 아야, 시녀/아프로디테/소환 의식,
  행성 보호국(`지구 보호국` 오기 1건 정정).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0542 (120630~120680, 50건)

- 종족별 잡담(`You look...`) + 스탯/득실 설명 + 팁 메시지.
- 용어: 차차라, 레테이아, 플롭볼, 아야네, 켈치스, 아키마리, 은신 테크, 대군주.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0541 (120580~120629, 50건)

- `You look...` 종족별 대사 일괄 + 사냥 퀘스트 제안 3종.
- 용어: 에너스, 회수된 나노 리셉터클, 핫브뢰드, 스타리 컬티스트.
- QA: 120597 `^white;` 누락 1건 수정 후 구조 0건, 용어 오탐 4건 유지.

### 0540 (120527~120579, 50건)

- `You know...` 잡담 일괄 + 시커 서사 2건(카민/네레우스/호라이즌).
- 용어: 불의 기적, 시커 아틀라스, 라이트헤이븐, 호라이즌, 프로그, 탑파 대도서관→대탑 도서관.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0539 (120474~120526, 50건)

- `You have...` 대사 일괄 + EMC 탁자 3종 + 알테라시 행성 착륙 안내.
- 용어: 알테라시, 스타더스트, 텐샤, 마그네타, 마기사이트, EMC 탁자,
  신비한 탑, 대천사 제케이즈리엘.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0538 (120422~120473, 50건)

- 스탯 보너스 설명(`^#<elem>;` 계열 태그 보존) + 발견 튜토리얼 + 불임 메시지.
- 용어: 펭귄 피트, 케스트렐 자격증, 블랜드프루트, 문스톤, 스틸 테크,
  착륙 축제, 감시자, 아이리스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0537 (120366~120421, 50건)

- `You don't/ever...` 대사 일괄 + 시커 구조 임무 요약 + 비밀 의식대 코덱스.
- 용어: 아나르키온, 익서크레이션, 네레우스, 하루토, 해로잉,
  이온 스트로크, 글림레쿠스 탑. `^#<elem>;` 변형 태그 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0536 (120310~120365, 50건)

- `You did/don't...` 대사 + 좀비 종족 능력치표 + 발견 튜토리얼 일괄.
- 용어: 실버 소콜로바, 연금술 가마/씨앗/다트, 코어 파편, 쏜윙,
  화염 군주, 드넬라운. 120328의 원문 오타 태그 `^oange;` 그대로 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0535 (120239~120309, 50건)

- `You can/can't...` 대사 일괄 + ITD 설정 설명서 + 필리페 8세 납치 임무 요약.
- 용어: 루이지, 에메랄드 글림프스, 필리페 8세, 진주콩, 황무지,
  위대한 인자한 자, 유물 탐구자.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0534 (120181~120238, 50건)

- `You can...` 기능 안내/대사 일괄 + 유물/차 쿠폰 교환 힌트.
- 용어: 아프로디테, 아키, 브리치 구체, 스파이크 스피어, 상구레,
  유물 특성/재료/쿠폰, 차 재료 쿠폰, 스탈리니움.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0533 (120128~120180, 50건)

- `You are...` 연속 대사 + 민속학자/올밍가/거짓의 씨앗 임무 요약 + 비공개 종족 능력치표.
- 용어: 루인에 물든 자(신규 고정, 기존 `유적에 물든` 3건+구 이형 1건 통합 정규화),
  제노톡스, 브루톨, 올밍가, 민속학자, 거짓의 씨앗, 레나틴.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0532 (120078~120127, 50건)

- `You are...` 계열 종족별 상호 대사 일괄. lastree/nebulac/mollopod 등 화자 보존.
- 용어: 레테이아, 피스키퍼, 필멸자, 몰로포드, 라스트리, 셰도우.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0531 (120027~120077, 50건)

- `You` 계열 대사 일괄 + 시커 추적 임무 요약 + 프래그먼트/반타/네불락 화자.
- 용어: 펭구킨, 노바 아웃포스트, 수상한 상인, 저장 물질, 콜트,
  대마법사 빈더밀, 시커, 브랜드(노바키드).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0530 (119962~120026, 50건)

- 마르페시아/아스테리아 코덱스 + 코아틀리카 능력치표 + 절정 대사 + Yo 계열.
- 용어: 마르페시아, 아스테리아, 에이트네, 푸른 말씀, 핏빛 달,
  코아틀리카, 요누르, 푸시아, 지하 생활.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0529 (119904~119961, 50건)

- `Yes` 계열 대사 일괄. ayylien 토큰 행(`<target>` 등) 원문 보존.
- 용어: 클루엑스, 버펄롯, 린/보이드, 먼지 탐구자, 수호자, 스타벅스/케빈,
  가짜 하피, GOV.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0528 (119841~119903, 50건)

- 노란 아이템 시리즈 일괄 + la-voe→러스틀링 서사 + Yep/Yer 구어체 대사.
- 용어: 이발리시안, 나이트폴, 글로아우라, 옐로스너겟, 모미지.
- 고정 용어 정정: 로켓발사기→로켓 발사기.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0527 (119752~119840, 50건)

- Yay/Yeah/Yeehaw 계열 대사 + 노란 가구 시리즈 + 페럴 프로젝트 코덱스.
- 용어: 페럴, 아포테오시스 프로젝트, 크라코스족, 보호국 드롭십,
  노획한 나노 리셉터클.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0526 (119682~119745, 50건)

- 야라 식물/가구 시리즈 일괄 + 야라 수호자-알타 갈등 코덱스.
- 용어: 야라, 야라 숲, 알테르니아(다수파 확정 27:5), 왜곡 억제,
  야프로그, 야잭, 야마시로.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0525 (119624~119681, 50건)

- YFFS 장비·통행증 시리즈(중국어 원문 행 119652 포함 번역, 기존 관례처럼
  중국어 병기 유지) + Ya 구어체 대사 일괄.
- 용어: 에르키우스, 제노 핸드북, 러스틀링.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0524 (119563~119622, 50건)

- 제노 가구 + 지쓰리사이트 무기 시리즈 + XS·제노사이트 명명 + Y' 구어체 대사.
- 용어: 제노사이트, 제노프로브, 지쓰리사이트, 졸로몬, 신브르베리, 사이노,
  형천, 자이언텍, 유물 수집가. 크툴루 찬트는 음차 유지.
- QA: 구조 0건, 용어 오탐 4건 유지, 미번역 0건.

### 0523 (119501~119562, 50건)

- 위버니스 능력치표 + 짜'이족 생물학 코덱스(대형) + 짜'이족 무기 + XS 메카 부품 일괄.
- 용어: 짜'이족, 위버니스, 자나피안, 브할레이한(구 `바흘레이한` 대신
  `바스 브할레이`와 일관된 형태로 통일), 그래비톤, 열정적인 탐험가.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0522 (119399~119499, 50건)

- Wow 계열 반응 대사 + 부서진 가구 + 소환 의식 실패 대사(`args`).
- 용어: 우누스트렐로, 성점술사, 레이스/레이스베일, 성난 이젤, 아발로니안.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0521 (119333~119395, 50건)

- `Would you like...` 상점/제작 제안 대사 일괄. 119386은 원문 자체가 깨진 문자열 —
  파손 바이트 그대로 보존하고 읽히는 앞부분만 번역.
- 용어: 텔리안, 가드후르, 정거장 트랜스폰더, 엘리시아, 크라코탄.
- QA: 119345 태그 중첩 수정 후 구조 0건, 용어 오탐 4건 유지.

### 0520 (119261~119332, 50건)

- 걱정/궁금 감정 라벨 대사 다수 + 컬티스트 3형 변종 + 낡은 가구.
- 용어: 프라임 바르다, 샌드스피터, 샌드크롤러, 미니크녹, 케빈, 나이타, ADF.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0519 (119195~119260, 50건)

- 작업장 아이템 이름 일괄 + 작업 드론 능력치표 + 호환 모드 팁.
- 용어: 러스틀링, 포/독성 포, 포시코어, 월드러너, 웜온치, 화려한 광채.
- 고정 용어 정정: 미니크노그→미니크녹, 마길록→매지락.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0518 (119133~119194, 50건)

- 우프 부족/우드랜즈 아이템 이름 일괄 + 고양이 귀 가구 설명 + 와시 종이 탄약 상자.
- 용어: 우드랜즈, 우프, 우피, 울루, 스포너, 과녁 허수아비, 텔레포터.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0517 (119060~119132, 50건)

- 나무 가구 이름 일괄 + 종족 특성표(물고기 인간, 식성/특성/환경/무기/약점).
- 용어: 수영 부스트, 텔레포터(정정: 순간이동기→텔레포터), 숲의 파수꾼,
  개인 트라이코더, 원시 창.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0516 (118970~119056, 50건)

- Woah 계열 짧은 반응 대사 다수 + 늑대 텐구 시리즈 + 마녀 관련.
- 화자: neki(냥), mechineki(플로란식 평서), om_harpy, woofie, shoggoth.
- 용어: 늑대 텐구, 짜'이족, 대마법사, 슈퍼스톰, 타우모스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0515 (118876~118966, 50건)

- 비에르 가이드/la-voe 서사/요리 설명 혼합. 성인 퀘스트 전달 항목은 원문 그대로 보존.
- 용어: 정수 추출기, 아케인 물, 바나나콘, 환상향, H기관, 미아즈마, 선하,
  로라타, 보에/라보에, 게류자, 은하 지도, 오메토나, 꿈토끼, 비전 가루,
  셀레스티아, 쿠포포, 컬티베이터, 필멸자.
- 고정 용어 정정: 에르치우스→에르키우스, 우드-워더→숲의 파수꾼.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0514 (118818~118875, 50건)

- 마녀 가구 시리즈 이름 일괄 + 위스테리아 원더. `Wistful` 감정 라벨은 최근 용례 `아련함`으로 통일.
- 용어: 부테인 캐시디, 선빔 리볼버, 론딘, 립스(인명), 크라코탄, 필라인 함선.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0513 (118758~118817, 50건)

- 겨울 가구 이름 일괄 + 알타 명절 인사. 종족 소원 목록("우유를 마실 수 있기를") 포함.
- 용어: 크레온, 스카바, 알타 건국기념일, 아바의 날, 소나의 베일, 위스퍼,
  위스테리아 위스커스 지구.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0512 (118697~118757, 50건)

- "Wind~/Winter~" 아이템·가구 이름 구간. 윈디 종족 특성 스탯 블록, 폭풍 행성 설명 포함.
- 용어: 윈체스터, 바람 정수, 윈드플라워, 윈디(종족), 클루엑스의 날개,
  에테르, 성지자.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0511 (118633~118696, 50건)

- 야생 씨앗·싹·꽃봉오리 이름 일괄(알타 식물군)과 적 유닛 행동 설명.
- ⟦E024⟧ 괄호 표기 보존.
- 용어: 에바라, 파아카인, 기트신, 루카, 소나바, 차이, 투란타, 베리스코이와,
  비오노라, 보다코이와, 야라, 이온 탄, EDS 드로이드, 수정 드론, 클루엑스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0510 (118569~118632, 50건)

- "Why/Wide/Wild~" 대사와 가구 이름, 야생 씨앗 시리즈, 아야(알타 복숭아) 장문 설명.
- 용어: 아키, 바르다스, 에르키우스, 클루엑스, 레테이아, 톤노바, 트링키안,
  아야/아야카, 아주라, 칼린, 코콜라, 시스튬, 알타 복숭아.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0509 (118456~118568, 50건)

- "Why~" 질문 대사 구간. 버섯이 버프 블록, 점사 개조 설명 포함.
- 용어: 스파이크버그, 버섯이, 라이지, 스트렐리치아, 스켈레트론,
  산성 화상/용해 면역, 프린트 사, 누루, 신성한 마을.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0508 (118367~118455, 50건)

- "Why~" 질문 대사 구간. 세포 벽 말장난, MOA 각주 포함.
- One-Handed → 한손 고정 용어 적용(부사 용법도 '한손으로'로 통일).
- 용어: 키테란, 무시 알, AEF, 빅 에이프, 미니크녹, 루인, 에르키우스.
- QA: 구조 0건, 용어 오탐 4건으로 복귀.

### 0507 (118242~118366, 50건)

- "Who~/Whoa~" 질문·감탄 대사 구간. 달 수정 생물 경고 편지, 저주받은 탑 쪽지 포함.
- 용어: 키르호시, 사냥(The Hunt), 모스맨, 불화의 사과, 콜트, 행성 보호국, 루인.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0506 (118153~118241, 50건)

- "White~/Who~" 가구·소품 이름과 질문 대사 구간.
- 용어: 화이트우드, 흰 늑대 대장, 흰 볏 흑색 폴란드, 페르시안(고양이),
  빅 에이프, 미니크녹, 클루엑스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0505 (118091~118152, 50건)

- "While~/Whistle/White~" 구간. 초생명체 심리학 코덱스, 에르키우스 3편,
  국방부·람다 지부, 공포 동굴 시적 서사(NL6), 다수 백색 가구/소품 이름.
- 원문 오타 `^rest;` 그대로 보존(118100).
- 용어: 람다 지부, 국방부, 에르키우스, 하베스트 쿠프, 초코보 목줄, 페르시안.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0504 (118027~118090, 50건)

- "While~" 코덱스·장문 설명 대량 구간. 클루엑스 사기 독백, 노스트OS 서사,
  게슈탈트/리샨 비판, 하피병 연구, 노멘·코덴 역사, 에르키우스 2편, IJA 소총사,
  알타 궁전·수도, 이오라 강화제, 스탯 블록 2건(마이리틀포니 패러디).
- 118064 중첩 태그 순서 수정: 원문 green→orange(내부 green)→reset 중첩 유지.
- 용어: 클루엑스, 라데이스/다스, 멀티포지, 아수라, 임페르비움, 이오라 강화제,
  알루니카, 미칼, 니베라/아르출린, 나레들라, 게슈탈트, 하피병, 노멘, 코덴,
  이와시타, 코시카 T97, 알타-1, 에르키우스, 녹스 님, 오토마타, 록하퍼.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0503 (117966~118025, 50건)

- "While~" 조건부 설명·코덱스 구간. 에르키우스 코덱스 2편, 알타 문화 서사,
  종족 특성 스탯 블록 2건(포니/사티로스), 플래시 스텝 기술 설명 포함.
- 용어: 멀티포지, M-67 솔로, 임페르비움, 아수라, 헤이븐, 이오라, 기예라,
  이발리스인, 무글 기사, 토나, 누올리스, 스포거스, 아우레아, 칼라인,
  탈리미무스, 플래시 스텝, 아릭, 에르키우스, 아가란, 그린핑거.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0502 (117826~117965, 50건)

- "Where~/Whether/While~" 질문·조건문 대사 및 패시브 효과 설명 구간.
- 용어: 컬러리스, 알테라시, 에세테라, 아스테라, 스타더스트, 모듈러 메크,
  종족 특성, 에르키우스, 새터니안 경비병 세입자, 라데이스, 스타파어러 피난처.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0501 (117826~117886, 50건)

- "When you~/Where~" 잡담·안내 구간. 농사 안내 코덱스, 슬라임 종족 특성표 포함.
- 용어: 초코보, 길리카다, 야어링, 크라코탄, 별과일, 탐험가 저항 감소.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0500 (117750~117825, 50건)

- "When~" 구절 대량 구간. 엔젤/세테난·카다반 서사, 아야 비르마 코덱스, 스타플라워
  수도회 동화, R.S.O 화기 설명, 맥비커 기사 등 장문 포함.
- `<elementN>` 컬러 토큰·`/on`/`/off` 리터럴 보존.
- 패링 윈도우 → 패링 창으로 정정(고정 용어).
- 용어: 세테난, 발라스 브할레이, 울타루빔, 엘리시아, 텔, 콘샥, 쏜윙,
  찰튼 맥비커, 아야카/아야 비르마, 스타플라워, 유황 행성, 모르페우스, 선하.
- QA: 구조 0건, 용어 오탐 4건으로 복귀.

### 0499 (117665~117748, 50건)

- "Whatever/When~" 독백·잡담 구간. 영역 창조자(엔젤) 대사, 노스트OS 서사 포함.
- 용어: 노스트OS, 프린트 사, 에센시아 옵스큐라, 피의 갈증, 팝톱, 섹스 바퀴,
  컬티베이터, 엔젤, 영역, 브이튜버.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0498 (117589~117664, 50건)

- "What's~" 잡담 구간. 아프로디테의 지팡이 발견 대사, 알키어 관련 대사 포함.
- 용어: 아프로디테의 지팡이, 사이버 구체, 크라코스, 고대인, 알키어, 하이로틀.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0497 (117517~117588, 50건)

- "What~/What's~" 잡담 구간. 포켓몬 종족 특성 스탯 블록(NL15), 알타 에너지 구체
  설명, 스캔 설명 포함. 스탯 블록 태그·항목 구조 1:1 보존.
- 용어: 포켓몬, 라데이스, 오버시어, 세터니아/알터니아/엔터니아, 알테라시,
  스타더스트, 아발론, 고대 관문, 빅 에이프, 미니크녹, 겁먹음.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0496 (117428~117516, 50건)

- "What kind~/What the~" 질문·감탄 대사. 해적 기함·루인드 월드 스캔 설명 포함.
- 용어: 오세아나이트, 낮거주자, 테네브래, 행성 보호국, 트링크, 새터니안.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0495 (117338~117426, 50건)

- "What is~" 질문 대사 구간. 스캐빈저 문명 코덱스, 감옥 역사 독백 포함.
- 용어: 스캐빈저, 웜, 마인드플레이어, 빛의 거주자, 식민지 증서,
  수수께끼의 촉수 문, 클루엑스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0494 (117258~117337, 50건)

- "What does/what if/what is~" 잡담·설명·마법사 코덱스 구간. 과학 말장난은 직역 유지.
- 용어: 클루엑스, 루인, 컬티베이터, 메이커, ADF, USCM, 무시, 프테로봄,
  혈관 문, 미드나이트, 미니크녹, 독뿌리 잼.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0493 (117203~117255, 50건)

- "What do you~" 질문 대사·과학 말장난 시리즈(세포분열, 시스테인 채플, 뉴럴 크레스트,
  케모택시, 핵 등 — 언어유희는 직역으로 의미 보존).
- 용어: 길텐, 몰로포드, 라이오드, 독뿌리, 궁극의 주스, 시커, 에지, 클루엑스,
  컬티베이터, 보호국, 미드나이트 행성.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0492 (117131~117202, 50건)

- "What are you~/What brings you~" 질문 대사 구간. 짜'이 멸종 가설 코덱스(긴 문서) 포함.
- Cultivator → 컬티베이터 정정(초안 '재배자'가 금지 표기라 수정).
- 용어: 텔레안, 짜'이, 누루, 미니크녹, 컬티베이터.
- QA: 구조 0건, 용어 오탐 4건으로 복귀.

### 0491 (116967~117130, 50건)

- "What a~/What are you~" 감탄·질문 대사. 노바키드 성별 논문 코덱스, 채찍 소문 문서 포함.
- 117102 태그 중첩 수정: 원문이 ^yellow; 내부에 ^orange;를 중첩하고 reset 1개뿐이라
  초안의 추가 reset을 제거해 원문 구조와 일치시킴.
- 용어: 폭스, 유물 탐구자, 누루, 아가란, 벤처러스 채찍, 노스탤직 채찍.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0490 (116837~116966, 50건)

- "Well~/Were~/What a~" 잡담·설명 구간. 웨스트 스타 화염방사기/헬하운드 장문 설명 포함.
- 용어: 고대 문헌, 어둠, 형이상학 연구, 드라코니스, 외곽 지역, 웨스트 스타,
  헬하운드, S1 연료 탱크, 오일라거, 웨이엔, 습지대 마이크로포머, 생 더스트리움,
  슈퍼스톰 항성, 자동화 행성, 워크숍, 타이탄코프, 센텐시안 점프소총, 점화, 클루엑스.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0489 (116733~116833, 50건)

- "Well~" 잡담·대사 구간. 화자별 말투 유지(floran 존-중 s신음, neki 냥체, saturn 카우보이 사투리).
- 용어: 슬라임, 쇼고스, 호라이즌 함대, 오토 칩, 최적화 회로, 티우니 어소시에이츠,
  라타시아, 가짜 하피, 새터니안, 타우모스, 플로란 유물, 보/라-보.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0488 (116672~116731, 50건)

- "Welcoming/Well done~" 완료 대사·환영 대사 연속 구간.
- 용어: 고대 파편, 하이퍼픽셀, A38 양식, 피스키퍼 상점, 데보트, 정예 드랄,
  자카르, 프로토 제어 모듈, 파리스, 대신전, 미니크녹, 노마다, 물질 조작기.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0487 (116622~116671, 50건)

- "Welcome~" 계열 환영 대사 연속 구간. 수호자 핸드북 도입부 2건은 cyan 태그 구조 1:1 보존.
- 용어: 회상의 판테온, 아틀란티스 바, 은하 크루즈사, 미흘리.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0486 (116572~116621, 50건)

- "Welcome to~" 환영 대사 일괄(스테이션 {STATIONNAME} 토큰, 대사관, 가게).
- 용어: 스타파어러 피난처, 아자나, 노바 스테이션, 탐구자 시련, 착륙 축제,
  아에기니안 연방, 트링크 서킷, 육감적인 봉카, 미스마 널 III, 크레온 대사관,
  마이 엔터니아, 빅 에이프, 아이스네, 그린핑거.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0485 (116515~116571, 50건)

- 스키틀즈 테스트 모드 스탯 블록 3건(NL15, 라벨 관례 동일), Ztarbound 안내문 2건
  (NL23/NL49 대형), 환영 대사 일괄, 안토라시/이오라 기에라 소개문.
- 용어: 족제비, CB! 캡슐, 웨드자트, 가중 컴패니언 큐브, 중량 저장 큐브, 노스토스,
  안토라시/알테라시/스타포레스트, 아틀란티스, 라이트헤이븐, 이오라 기에라, 루네바,
  베르살리아, 아논레쿠스, GALAXY_NAME/CLIENT_NAME/PC_SUPPORT_UNIT 런타임 토큰 유지.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0484 (116424~116514, 50건)

- 의료 스테이션 강화 팸플릿(NL37 대형, 태그 전수 보존), 환영 대사 일괄, 큐브/족제비 명명.
- 용어: CB! 캡슐(여/남), 웨드자트, 가중 컴패니언 큐브, 중량 저장 큐브,
  크레온, A38 양식, 피스키퍼(상점/스테이션), 에스컬레이션, 달의 유물, 강화(Enhancement),
  광전사의 분노, 유리 대포, 면역화, 저거너트, 독성 구름, 트롤의 피, 리너자이저,
  저혈압, 하이브마인드, 미토콘드리아, ~격퇴 시리즈, 벌침, 찌르기 피해(THRUST).
- QA: 구조 0건, 용어 오탐 4건 유지(찌르기/피스키퍼 후보 정정 완료).
- 주의: 무차별 치환 금지 — 116455의 THRUST만 찌르기, 116513의 piercing은 관통 유지.

### 0483 (116345~116422, 50건)

- 약한 물약/고서 시리즈, 무기 연격·전문화·변경로그(children) 목록 다수, 글리치 지침 대사.
- 용어: 마스터로이드, ~의 서(Tome of X), 익소사이트/터마스린/오렌, 세룰리움,
  무기명 음차(아이기스, 하트리스, 솔스티스, 사무라이의 심장, 궁니르 등),
  주 공격/보조 발사, 아드레날린 러시, 크루세이더, 그리모어, 노키마리.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0482 (116290~116344, 50건)

- 화석 복제 의뢰 후속(골격 부품 다건: 익소둠 5부위, 오피던트 5부위 등), 스파이넷 조사.
- 용어: 아비오스케일, 익소둠(척추/엉덩이/침), 오피던트(윗/중간/아랫꼬리),
  알 화석, 불명의 골격, 양전자 두뇌, 스파이넷, 먼지 탐구자, 빈더밀, 네레우스,
  에르키우스, EMF, 프리즘 파편, 약한 ~ 혼합물/물약.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0481 (116236~116289, 50건)

- 광물 40개 납품 의뢰 시리즈(11건), 화석 복제 의뢰 시리즈(13건), 퇴소 노트 등.
- 용어: 솔라리움 별, 구리/금/은/철/타이타늄/텅스텐/듀라스틸 주괴, 정제된 에지솔트/
  페로지움/바이올륨, 양치류·물고기·발자국·펭귄·암모나이트 화석, 트릴로바이트,
  티라노사우르스(해골/상체/다리/윗꼬리/아랫꼬리), 알파카, 검치호 해골, 호박, 스타리 액체, 유니온.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0480 (116185~116235, 50건)

- 일반 대사 일괄, 아비안 지상인 노래(NL8), 루시 건설·다이아몬드 의뢰 등.
- 용어: 일루미네이트, 완더러, 지상인(the Grounded), 에테르, 컬티베이터의 율법,
  노마다, USCM, 미니크녹, 우루사, 이발리스, 쿠포, 텐구.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0479 (116128~116184, 50건)

- 리샨 교리 서사(종복 종족 연료), 러브레터, 우프 해적단 현상금 등 콘텐츠 4건.
- 용어: 리샨, 씨앗, 수정족/페럴/오토마타/웜, 티우니, 텔, 스페이스드리프터,
  우울로틀, USCM, 아프로디테, 컬티베이터의 율법, 모미지, 꿈토끼, 클루엑스.
- QA: 구조 0건, 용어 오탐 4건 유지(dream hare 후보 정정 완료).

### 0478 (116076~116127, 50건)

- 벌레 표본 의뢰 시리즈 완결(35건), 일반 대사.
- 용어: 벌레 이름 전부 기존 TM 고정 표기(종울림벌레~조류벌레 등), 용암/독성/화산/눈/사막/극지/바다/외계 행성, 노마다, 오카서스, 클루엑스, 연고 제작자.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0477 (116024~116075, 50건)

- 작물 납품 의뢰 시리즈(시가 2배 + 픽셀 태그 구조), 벌레 표본 의뢰 시리즈.
- 용어: 오토마토, 부리씨앗, 볼트 구근, 본부, 전류수수, 흙성게, 에그슈트, 암초,
  독뿌리, 잿빛불이, 오로라벌, 등푸른벌레, 밝은얼룩벌레, 버터벌, 잉걸불이, 이슬깨비,
  불탄/툰드라/한밤중/숲/정글/정원/마른 초원 행성.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0476 (115968~116023, 50건)

- 시커/보호국 임무 대사, 크라코스·카다반 탈출 서사, 개행 콘텐츠 5건.
- 용어: 메탈룸나, 스파이넷, 유적살해자, 세퀘이즈리엘, 쇼군 타케시, 코토 공주,
  타케시 성, 모스 루난, 에메랄드 글림프스, 선본, 헤이븐크레스트, 크라코스,
  노마다 함대, 에라스메이르, 업리프터, 이발리스, 인딕스, 연고 제작자, 에스더.
- QA: 구조 0건, 용어 오탐 4건 유지(태그 순서·에스더 오탈자 정정 완료).
- 후속 정정: `Ruin-Killer`를 `유적살해자`에서 `루인킬러`로 전수 치환(10건+`루인 킬러` 1건).
  바닐라 대명사 루인과 연관된 칭호이므로 음차. 글로서리에 `Ruin-Killer → 루인킬러` 고정등록.

### 0475 (115915~115967, 50건)

- 리샨 교리·필연/맹렬한 자 서사, 가게·요괴 전쟁 대사, 개행 콘텐츠 4건.
- 용어: 리샨, 리샨의 씨앗, 자라나는 자, 필연, 맹렬한 자, 니일라, 트로페스, 선하, 실프의노래, 요괴, 로닌, 에지, 스타리 컬티스트, 고대의 모루, 마인드플레이어.
- QA: 구조 0건, 용어 오탐 4건 유지(Aegi 후보 정정 완료).

### 0474 (115864~115914, 50건)

- 퀘스트 요리사 의뢰 시리즈, 오카서스 대사 시리즈, 짜'이 족 언어 연구 기록 등.
- 용어: 포제스트, 궁극의 주스, 불타는 눈알, 산호초 카레, 핫 본, 핫 핫 핫팟, 네온멜론 잼,진주콩 꾸러미, 매운 깃털왕관, 매운 갈비살, 화산 살사, 사마귀초, 시커 아틀라스, 녹터니안/타우모스, 오카서스, 짜'이, 카다반, 엑소시아, 루이에, 시아사, 스타게이저, 행성 수호자, 천사 반란군, 루인드.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0473 (115792~115863, 50건)

- 물 발효 후속, 웨이페어러/웨이세이지 시리즈, 비에라 숲 대사, 개행 콘텐츠 3건.
- 용어: 파도새벌레, 외계벌레, 취약화, 센틀라, 하이로틀, 나이타, 트링크, 클루엑스, 아비안, 루인드, 알타.
- QA: 구조 0건, 용어 오탐 4건 유지(Broadsword 후보 정정 완료).

### 0472 (115721~115791, 50건)

- 물 발효 설명 시리즈(`이제 필요한 건 시간뿐` 기존 관례), 물 관련 아이템, 개행 2회 행 1건.
- 용어: 어베스밍고, 눈알레몬, 효모, 카짓, 필멸자, 알타.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0471 (115650~115718, 50건)

- 일반 대사 + 와스프밈 명명행. `The Ruined` 고정 용어 `루인드` 적용(115709).
- 용어: 와스프밈, 클루엑스, 유카이, 고대인, 선배님, 루인드, 쿠포포, 메크.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0470 (115574~115649, 50건)

- 왜곡된(Warped) 시리즈 명명행 일괄, 워런 구멍, 글리치 경계 대사.
- 용어: 왜곡된, 마이크로포머, 스포르구스, 사마귀초, 워런, 툰드라.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0469 (115502~115573, 50건)

- 경고문 시리즈(행성 위험·메크 경고), 요원 임무 경고, 가드후르·앵글루어 명명행.
- 용어: 가드후르, 앵글루어, 소닉 스피어, 칭취, 스캐빈저, 워록, 워든, 워프 대시,
  치차(고유명).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0468 (115451~115500, 50건)

- 승무원 성향 "-함" 라벨 연속(농장 시리즈 포함).
- 용어: 플러팔로(전기/화염/얼음/독), 네온멜론, 진주콩, 독뿌리, 오토마토, 어베스밍고,
  눈알레몬, 무시.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0467 (115399~115450, 50건)

- "Wanna~/Want~" 잡담 일괄, 승무원 성향 "-함" 라벨 연속.
- 용어: 나미 드라이, 야라, 케프라이더, 파리스, 무시, 고대 도서관 코덱스, 로봇 타코.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0466 (115341~115398, 50건)

- 벽 설비 명명행 일괄, 방랑 NPC 명명·대사, 알타/네키 잡담.
- 용어: 감시자(the Watchers), 월소브, 빅 에이프, 로닌, 이름표 <직함> 표기는 한국어로 유지.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0465 (115275~115340, 50건)

- "Wait..." 대사 일괄(종족별 어투 적용), 벽 명명행.
- 용어: 에지, 나이타르, 반타, 트링크, 드로덴, 쇼고스, 레피돕티안, 스카스,
  빈더밀, 별가루, <selfname>/<entityname> 토큰 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0464 (115217~115270, 50건)

- WW-LGT 가구 마무리, WW2 일본 군수품 설명, 짧은 대사 일괄.
- 용어: 아리사카, T99, 삼극 정수, 엘리엇 박사, 레나틴 수정, 질주 기술, 밴시.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0463 (115165~115216, 50건)

- WST 증원 명명, WW/WW-DRK·LGT 가구 세트 일괄, 우주(WUJU) 종족 스탯 블록(NL15).
- 용어: WW(접두 유지), 로리(마스코트), 위스테리아 분재, 종족 스탯 라벨 동일 적용.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0462 (115109~115164, 50건)

- 행성 위험 경고문 일괄(NL1~NL2, 색상 태그 보존), 차량 미인증 경고 시리즈, WIP 서술.
- 용어: 루멘, 위험도(Peril), 알리아나, 파라데아, W0LF/W28/W3/W4/W7 무기 코드명 유지.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0461 (115031~115108, 50건)

- 보다코이와/공허/화산/전압 명명행, 발칸족 종족 스탯 블록(NL15), 코덱스 단편.
- 용어: 비리데슨트, 볼트로폴리스, 볼타이트, 볼팁, 브렐리, 불페라, 발칸,
  보이저 갑옷(초코보 마갑행과 동일 명칭 재사용), 공허의 속삭임 인형.
- 용어 규칙: Voltage는 명명행만 볼티지 음역, 설명·대사는 전압 직역(글로서리 고정, 전압 허용 대체형).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0460 (114957~115030, 50건)

- 비오테크/비리데슨트 명명행, 바이탈 이지스 업그레이드 일괄, 루인 인류 코덱스, 별빛 신도안내문.
- 용어: 비리데슨트, 비르마, 보펄 버니, 비전 더스트, 라이트헤이븐, 글림레쿠스, 엑소시안,
  이즈쿠/파리투(우호적 표기), 바이탈 이지스, 심판, 바이탈리스 열매.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0459 (114897~114956, 50건)

- 빈티지 술 마무리, 유린당한 장비, 보라색 수정·비오나 명명행, 비오나/비오니아 코덱스.
- 용어: 트로포트, 울티민트, 사이노, 비오 지크, 유린당한 드라흘, 바이올륨, 비오나,
  비오니아, 비오노스테라, 미아즈마, 비오노라.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0458 (114842~114896, 50건)

- 빈티지 술 명명행 일괄(기존 Aged/Fine 음역에 맞춤), 마을 시설, 비나리즈·빈더밀·빈디 서술.
- 용어: 빌트보들 VI, 비나리즈, 빈더밀, 빈디, 어베스밍고 코디얼, 캑트IPA, 톡시사이더 등
  기존 음역 재사용.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0457 (114778~114841, 50건)

- 비에라/비에란 가구·자재 설명 일괄, 비에라 대사(숲의 품 표현), 비질란테 직업 설명.
- 용어: 비에라, 비에란, 숲(the Wood), 화이트우드, 마호가니, 비질란테, 활력 I~IV, 쿠포.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0456 (114700~114777, 50건)

- 비에라 가구 일괄, 브할레이한 지리/창 역사, 섹스바운드 바이알 시리즈, 비드완삭 설명.
- 용어: 비에라, 베스퍼, 바흘레이한(기존 음역 채택), 카바나이트, 자나피르,
  보스 아브할라스, 코이와, 정액 한 병.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0455 (114620~114699, 50건)

- 베르사 리코셰 업그레이드 5종, 총기 설명, 음식 설명, 코덱스 발췌.
- 용어: 베르사, 센텐시안, 버틴크처, 코이와, 칼린 잼, 키셀, 마이코톡신, 광폭화,
  테크 카드(기술 카드→테크 카드 정정).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0454 (114567~114619, 50건)

- 버던트·주홍·버밀리움·베리스코이와·베로스틴 명명행 일괄.
- 용어: 버던트, 주홍(Vermilion), 버밀리움, 뢰벤헤르츠, 베로나스, 스패로우,
  베리스코이와(알토/파로/미코 꽃), 베로스틴.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0453 (114494~114566, 50건)

- 바쉬크나렌 두 번째 스탯 블록, 벨루이시 무기 시리즈, 맹독/독성 친화력 업그레이드 일괄,버던트 무기.
- 용어: 바슈타, 드로덴, 바트라, 벨루이시, 베네토 프라임, 베랄타이, 중독화(Toxify),
  맹독 및 독성 친화력, 활력/민첩/기민, 버던트.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0452 (114436~114493, 50건)

- 베이퍼웨이브 가구 후반부, 바스 브할레이 인사 연작(이즈야티 아스-칼라단 코덱스), 바쉬크나렌 스탯 블록(NL19).
- 용어: 바스 브할레이, 카다반, 라데이스, 아유린의 분노, 공로 토큰, 크롤러 둔벙, 바쉬크나렌,
  드로덴, 스탯 라벨(식단/특성/저항/면역/환경/무기/약점/허기 속도/카리스마).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0451 (114374~114435, 50건)

- 뱅가드 장비 후반부·메크 파츠, 바닐라 A.I. 칩 시리즈, 베이퍼웨이브 가구, 소멸 구체 업그레이드 설명.
- 용어: 라인라이플/스킵라이플, 소멸 구체, 고스트 모드, 하이로틀(힐로틀→하이로틀 정정),
  종족 특성 미지원 안내문 기존 문구 재사용.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0450 (114312~114373, 50건)

- 발베리 음식, 발란스 시리즈, 뱅가드 장비 일괄, 미니크녹 선전문, 글리치 역사·발키리 설명.
- 용어: 발베리, 발아르, 발더, 밸리언트, 발키리, 컬티베이터, 하이마인드, 실크나방 유전자변이 프로그램,
  뱅가드(드라흘/드랄리드/크랄), 레인보우 로그.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0449 (114236~114311, 50건)

- "Using/Uses/Usually" 서술 일괄, 명명행(Uumie, V 계열 무기 등), 컬트 권유 대사 3변종.
- 용어: 어베스밍고, 포시코어, 못츠, 아야 잼, 코르팔, 엘린 정원, 우미, 오르카, 포자르,
  빈토레즈, 부활절 토끼, 세로할라핌 전사 우미.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0448 (114175~114235, 50건)

- "Used to/for..." 스테이션·도구 설명 일괄. 스탯 블록·색상 태그 보존.
- 용어: 아르카니안, 알타, 메트로캅, 러스틀링, 옴니브라우저, 낚시용 눈알, 미니크녹 소행성기지,
  추출 가능, 출혈 부여, 보조 발사(Alt Fire 고정 표기로 정정), STANAG-FEDERATSIYA 규격 보존.
- 주의: 개행 포함 셀은 따옴표 필요 — TSV 직접 재작성 금지, JSON 수정 후 add_batch 재실행.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0447 (114119~114174, 50건)

- 해금 조건문 후반부, "Use this to..." 아이템 설명 일괄(초코보 마구 시리즈 17건, 라벨 주머니 7건).
- 용어: 초코보, 헌트마스터/여행자/패스파인더/패스가드/팔랑크스/트레일위버 갑옷·방어구,
  보이저/웨이페어러/웨이세이지/월드러너 갑옷(신규 음역), 천 하우다, 여행자의 마구, 부활절 토끼,
  트라이코더, 섹스바운드 커스터마이저, 섀더스트로피, 유물 품질(일반/고급/희귀/전설).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0446 (114062~114118, 50건)

- 커맨드 사용법 일괄(Usage /... → 사용법 /...), 해금 조건문(unlocktext 기존 하십시오체 재사용), 우루사 마이너 관련 명명.
- 정정: 114087 `<foodvalue>` 토큰 복원, 우르사→우루사(고정 표기).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0445 (113997~114061, 50건)

- 에메랄드 글림프스 퀘스트 서술, 천사 일지·아프로디테 퀘스트 페이지, 어반 가구 명명행 연속.
- 용어: 에메랄드 글림프스, 빛나는 유적, 레나틴 수정, 샐리, 네레우스 박사,
  아프로디테의 활/지팡이/노끈/활시위 도구, 어반(가구 접두), 전지의 기사.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0444 (113937~113996, 50건)

- 업사이클 가구 잔여, 함선 등급 업그레이드 라벨·서술, 핸드 캐넨 개조 서술, 빅코인·엑스크레이션 로어.
- 용어: 콘도르/이글/팔콘/케스트렐/스패로우급(함선 등급), 빅코인, 미니크녹, 팔케 장군,
  엑스크레이션, 원소 기적, 민첩성. `Broadsword`는 고정 표기 `브로드소드`로 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0443 (113868~113936, 50건)

- 불안정 계열 명명행, 업사이클 가구 명명행, 리샨 교리·셀레스티아 신화 페이지, 종족 조사대사.
- 용어: 잡동사니(garble), 마그노브, 리샨, 아네모시아, 우누스트렐로 별 카페(TM 관례),
  가시 주스, 업사이클, 방사능 화상 유발.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0442 (113802~113867, 50건)

- 제련 해금 서술, 무인 전차 명명·조사행(라이온 대대/웨스트 스타), 포장 해제·개봉 화물 명명행,
  셀레스티아 동화 페이지.
- 용어: 신틸리움, 세룰리움, 임페르비움, 원자 용광로, 산업용 용광로, 라이온 대대, 웨스트스타,
  매지우드, 셀레스티아(고유명), 기괴한(eldritch).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0441 (113748~113801, 50건)

- 탄창 비우기 명명행 연속(일본계 총기), 루카리오 종족 가슴·꼬리 레시피 해금 서술.
- 용어: 비존, 칭다오, 카와무라, 코쿠라, 미나토, 나고야, 설득의 바늘(고정), 할로 포인트,
  엉블록 클립, 베타 C, 람보 벨트, 리오루/루카리오. `|Gender X|`류 템플릿 라벨은
  `|성별 X|`/`|중성 X|`로 옮김(원문 오타 Geutral은 의도대로 중성으로 처리).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0440 (113684~113747, 50건)

- Unknown 구조물 조사, Unlike~ 서술 연속, 베나흐트 종족 블록, 탄창 비우기 명명행.
- 용어: 림-에레키우스(기존 다수파), 기트신, 러스틀링, 오버록, 재배치기, 쿠르츠, 모스버그,
  니토리 산업, 야마시로 파이낸셜, 체레즈 오르망드. `Unload ~ Mag`은 `~ 탄창 비우기` 관례.
- QA 후 정정: Kappa→캇파(고정), two-handed→양손(고정).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0439 (113630~113683, 50건)

- 유닛 로봇 대사 잔여, 연합 시스템 탄약 명명행, Unknown/알 수 없는 명명·조사행.
- 용어: 연합 시스템, 유니탄 코스모플로트, 테크멜리안 연방, 공중폭발, 명사수 소총, 드라구노프.
- Unknown person 조사행은 화자별 문체 적용(페네록스 단답·네키 ~다냥·천사 격식체).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0438 (113542~113629, 50건)

- Union 깃발·인형, Unique/Unit 명명행, 유닛 로봇 대사 연속.
- 용어: 유니언 깃발(고정), 유니언 프라이드 깃발(글로서리 추가), 오로타움.
- QA: 구조 0건, 용어 오탐 4건 유지.
- 사용자 피드백 반영: `opposite gender`는 `반대 성별`이 아닌 `이성`으로 통일(0437·0280 소급 정정,
  글로서리 고정 등록). `dump_priority.py`를 개선해 원문 개행을 `NL{n}` 마커와 `
` 리터럴로
  표시하게 했다 — 이후 덤프 미표시 개행 보정 단계가 불필요해진다.

### 0437 (113462~113541, 50건)

- "Under/Unfortunately" 본문, 언데드 종족 블록, 반대 성별 전문화 스킬.
- 용어: 루카리오, 아가란, 카바나이트, 센텐시안, 칭취, 가짜 하피, 바이랄릭, 인퍼너스(고정), 진정한 깨달음.
- 덤프 미표시 개행 6건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0436 (113381~113460, 50건)

- 엄브럴/고급 무기 명명행, 기계 대사, 모리스 보스명.
- 용어: 움브라시, 블래키, 그로우플라이, 그린가드, 엠피리언, 고급(Uncommon 등급).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0435 (113300~113380, 50건)

- 짧은 대사 연속, 잉키 퀘스트 대사, 엄버스톤 가구.
- 용어: 에소쿼츠, 울티민트, 울트로늄, 엄버스톤, 엄브럴, 쿡 씨, 루스릭.
- 덤프 미표시 개행 6건 보정, 열린 태그 과잉 닫기 1건 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0434 (113221~113299, 50건)

- USCM 잔당 상황 묘사, USCM 실험 기록, 짧은 대사(성적 대사 포함).
- 용어: UPDF, USCM, 생체생성(Biogenesis), 노이미.
- 덤프 미표시 개행 4건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0433 (113165~113220, 50건)

- U.S.C.M. 비컨·장비 명명행 연속, RPG 전문화 체인지로그 2건.
- 용어: 전문화 체계(네크로맨서/저거너트/데드샷/비질란테/배틀 메이지/셰이드/메카니스트/세이지/오퍼레이터), 리프, 뼈 프테로포드, 클레이빙 메테오.
- 덤프 미표시 개행 2건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0432 (113108~113164, 50건)

- U.S.C.M. 가구 명명행, 군용 총기 역사 설명, 코볼드 종족 블록.
- 용어: 타임 빔, 코볼드, H기관, 발광(종족 특성).
- 덤프 미표시 개행 4건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0431 (113019~113106, 50건)

- 토글 라벨 잔여, 트위터스 대사, 엄니 베헤프로스트 시리즈.
- 용어: 졸트, 엄니 베헤프로스트, 트워키, 트위건, 아가라닉, 요코스카 T4, 소나베일.
- 덤프 미표시 개행 1건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0430 (112952~113018, 50건)

- 텅스텐 무기 명명행, 토글 라벨, 차이키르 종족 블록.
- 용어: 차이키르, 차이(Tsay), 신텍스(Tsyntex), 투란타, 포직, 기트신 차지.
- 덤프 미표시 개행 1건 보정(종족 스탯 블록).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0429 (112892~112951, 50건)

- 진정한 아이기스 업그레이드 설명, 트롤 종족 블록, 짧은 대사.
- 용어: 삼극성, 트리타늄, 트로포트, 진정한 아이기스, 스파이넷, 패링 창(Parry Window 고정용어).
- 덤프 미표시 개행 8건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0428 (112829~112891, 50건)

- 트링키안 부품 명명행 연속.
- 용어: 트링키안, 트리올바이트(Triolbites), 트링키안 텔레포터(Teleporter 고정 용어 적용).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0427 (112765~112828, 50건)

- 트링크/트링키안 부품 명명행 연속.
- 용어: 루네바, 트라이팽글, 트리피사이트, 트링크, 트링키안.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0426 (112707~112764, 50건)

- 여행자 대사·비에라 문체 행, 트라이앵글륨 무기.
- 용어: 트라이앵글륨, 초코보, 숲의 파수꾼, 트라이투스, 참호웜, 지진 폭발.
- 덤프 미표시 개행 1건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0425 (112612~112706, 50건)

- 마이크로포머 설명문 후반, 덫사냥꾼 무기 명명행.
- 용어: 아릭, 숲 그분, 에르키우스, 위치변환, 트랩루트, 방주 폐허.
- 덤프 미표시 개행 2건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0424 (112561~112611, 50건)

- 마이크로포머/테라포머 설명문 연속.
- 용어: 비신, 헤비카, 안식처 들판, 팝톱 계곡, 미사일꽃, 파라스프라이트, 애니머스, 배드랜드.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0423 (112508~112560, 50건)

- 테라포머 설명문 연속("행성의 기후를 X로 변환합니다" 관례), 변형 비용 라벨.
- 용어: 트랭크와일, 트랑기, 네온스케이프, 에민스노우, 아모러스, 알테라시 프라임.
- 덤프 미표시 개행 1건 보정(인터뷰 녹취록).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0422 (112428~112507, 50건)

- 전통(Traditional) 가구 명명행 연속, 키세루 설명문.
- 용어: 드로덴, 감시자(Watcher), 트레일위버, 추적기, 견습 퀵블레이드.
- 덤프 미표시 개행 3건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0421 (112359~112427, 50건)

- 독성 시리즈 아이템 명명행 연속, 짧은 대사.
- 용어: 독뿌리(Toxictop), 톡시카이트, 스모글린, 독성 크리프, 비리데슨트, 톡시닥틸, 톡시워퍼.
- 덤프 미표시 개행 2건 보정(추출/체질/제련 가능 라벨).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0420 (112255~112358, 50건)

- 톤노바 생물학 코덱스, 짧은 대사 연속, 툴팁·토글 라벨.
- 용어: 헤발토르, 바이온플라이, 엑스크리듀라, 생물결정(biocrystal).
- 덤프 미표시 개행 5건 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0419 (112196~112254, 50건)

- 염색 스위트 토글 라벨 연속, 무덤 크리터·토나 음식 명명행.
- 용어: 토나, 톤나카다, 톤노바, 토나우악, 배통, 요카트, 스푸킷, 공로의 증표, 토큰 교환소.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0418 (112109~112195, 50건)

- "To ~" 잔여문, 행성 보호국 코덱스, 뱀파이어 종족 블록, UI 토글 라벨 연속.
- 용어: 이리사, 스타포지, 선하, 아스테리아, 쌍둥이 그림자, 셸(주문), 테레네 선거국, 관리국.
- 덤프 미표시 개행 3건 보정(라에나틴 일화, 플로란 일지, 뱀파이어 스탯 블록).
- 용어 정정: Terrene Protectorate → 행성 보호국(고정 용어), 구 배치 0046 잔여 1건도 통일.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0417 (112037~112105, 50건)

- "To ~" 시작 문장 연속, 그리모어 제작 가이드, 미니크녹 레지스탕스 편지 2종.
- 용어: 시커, 시커 시험, 아눌락스 배터리, 그리모어, 스너피시, 페닉스, 글림레쿠스, 빈더밀, 마기사이트, 이온 태엽시계, 잘고, 주/보조 능력 페이지, 메카 제작 테이블.
- 덤프 미표시 개행 9건 보정(그리모어 가이드 5단락 등), 태그 연속 배열(orange→green→orange→green) 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0416 (111974~112035, 50건)

- 타이탄코프 가구·티타늄 무기 명명행 연속, 알타 감사문/테렌스 리그 공고/클루엑스 교리문.
- 용어: 타이탄(클래스), 티우니 어소시에이츠, 아바이스트, 보에(voe), 테렌스 리그, 하피병,에테르.
- 덤프 미표시 개행 3건 보정(케빈 쪽지, 알타 감사문, 지상인 교리문).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0415 (111893~111973, 50건)

- Tiny 명명행 연속, 스켈레킨/마이크로 생명체 종족 블록, 피로 대사.
- 용어: 레테이아, 코도릭, 스켈레킨, 사이폰, ADF, 타이탄코프, 둔화(Slow 면역 확정).
- 덤프 미표시 개행 3건 보정(스탯 블록 2, 광역 피해 라벨).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0414 (111838~111892, 50건)

- "시간이다/훈련 시간" 대사 연속, Timeless 아이템 시리즈, 작은 곤충 명명행.
- 용어: 이지스, 에테르, 노바, 사이폰, 스파이라, 베르사(실체 이름 음역), 피퍼피시, 공백. <seedList> 자리표시자 보존.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0413 (111762~111837, 50건)

- 티어 패드 시리즈, 알타 도시 방어선 로어, 미라/티아 일지, 시간 관련 격언.
- 용어: 에세테라, 아스테라, 이온 코어, 에지솔트, 페로지움, 루비움, 크로놀로스, 해일, 조류 왜곡자.
- 덤프 미표시 개행 4건 보정. 111792 에지솔트 표기 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0412 (111693~111761, 50건)

- "곰곰이/위협적/신나" 감정 접두 대사, 네크로맨서 로어, 문셰도우 기사단, 스로그 종족 블록.
- 용어: 골모어, 마르페시아, 문셰도우, 스타게이저, 에볼라피스, 광휘 강철, 알케믹 인서터,퍼펙트 블록, 스로그.
- 덤프 미표시 개행 4건 보정(스로그 스탯 블록, 특성표, 111740 삽화시).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0411 (111628~111690, 50건)

- 루인드/리샨/새터니안 로어 콘텐츠, 비에라 격언, 종족 외모 코멘트, 고어풍 퀘스트 대사.
- 용어: 텔, 폭스, 자라나는 자, 발할라, 발렌, 하이마인드, 요괴, 텐구, 아쿠오렌, 네레우스,트로틀리, 심장 나무, 레테이아.
- 덤프 미표시 개행 9건 보정 — 111634 체인질링 특성표(식단/특전/환경/무기/약점/저항), 111652·111674 스탯 블록.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0410 (111554~111627, 50건)

- 가시 무기/아이템 명명행, 종족 간 외모 코멘트 연속(아키마리·네키·아비안·메치네키), 콘텐츠 페이지.
- 용어: 토라이트, 가시열매 에코 포드, 쏜윙, 메가-트링크, 미니크녹(Minkong 오기 포함), 클루엑스, 에르키우스, 무시, 그린핑거, 엘리시안, 아비칸.
- 덤프 미표시 개행 3건 보정(111613 엘크 탈것 후단, 111617/111619 줄바꿈 구조).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0409 (111367~111553, 50건)

- 플로란 대사 연속, 텔레포터 시리즈, 야바/야라 묘목, 샐리·레콘 퀘스트.
- 용어: 레콘, 라인라이플, 이온 발효물, 야리자, 야바, 아야카 정원사의 노트, 데보트, 토르디알.
- 덤프 미표시 개행 2건 보정. 0406 파일의 111049 오탈자(라면멍멍이→라면 멍멍이)도 함께 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0408 (111270~111366, 50건)

- 벽지 시리즈, 텔레포터, 군용 소총 로어(ZU-23-2 후속), 길텐/에스더 퀘스트 대사.
- 용어: 알데론, 길텐, 아크 파편, 엠피리언 행성, 에스더, 보조 발사, 저격소총, 포이.
- 덤프 미표시 개행 5건 보정(체크포인트 힌트, 4차원 이론 후단, 개머리판/보조발사 조작 2건, 지뢰 조작).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0407 (111183~111268, 50건)

- "본 장치는~" 글리치 NPC 대사 연속(자리표시자 다수 보존), ZU-23-2 로어, EPP 묘사.
- 용어: 에테이움, 페롤릭/하이올릭 버섯, 미칼 수정, 공로 토큰, 노마다 토큰 교환소, 츠키카게, 셸가드, 스타리 액체.
- 덤프 미표시 개행 2건 보정(111192 종족 스탯 블록, 111226 생존자의 선택 특성표).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0406 (111037~111182, 50건)

- 텔레포터/함정 시리즈, 식품 가공기 로어 3종(메탈 기어/케모노 프렌즈/KEY 레시피), 샐리 회상문.
- 용어: 주시 연못, 시랑가, 마그마타우르, 알파카 함선, F.D. 스캐빈저, 피스키퍼 본부, 일루미네이트.
- 덤프 미표시 개행 13건 보정(레시피 블록, 부서지면 파괴 라벨, 사냥용 무기).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0405 (110859~111036, 50건)

- 기술(대시/점프/디스토션 스피어) 튜토리얼 문구, 텔레포터 시리즈, 테이블·램프 묘사.
- 용어: 게아룬, 기트신, 세터니아, 아야카, 로칸, 디스토션 스피어, 펄스 점프, 노스트OS, 피스키퍼 본부, 우누스트렐로의 별빛 카페.
- 덤프 미표시 개행 4건 + 111006 태그 순서 보정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0404 (110738~110858, 50건)

- 함선 스타일 시리즈(도장/화물칸), 스팀팩, 펭귄 아종, 타브리야 초원 로어.
- 용어: 베리스코이와, 기아나, 베랄타이, 코이와 알토스, 노스트OS, 스파이라, 아우로자, 솔라레이 스카이 시티.
- 덤프 미표시 개행 4건 보정(110771 후반부, 110820 처리 라벨, 110825 [E] 조작, 110855 RT미지원 안내).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0403 (110609~110737, 50건)

- 묘목·조명 시리즈, 솔라리움 장비, 소나베일 케이크, 플러팔로 품종, 플로란 대사.
- 용어: 솔라리움, 소나스위트, 정적 세포→식물 섬유 품종, EDS 포드, 위스퍼.
- 덤프 미표시 개행 3건 보정(110657, 110660 출혈 유발, 110609 후속 안내).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0402 (110447~110608, 50건)

- 함선 신호 스캔, 펭귄 피트 면허 시리즈, 알타 가구/방패 묘사.
- 용어: 프로테아, 솔라레이, 와스프밈, 슈탈라이트, 단탈리온, 언바운드, 호라이즌 함대, 정적 세포, 샐리, 위스퍼, 소검(숏소드 정정).
- 110484~110487 태그 순서(green→orange→green→white) 병합 전 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0401 (110324~110445, 50건)

- 펭귄 우두머리 로어, 새터니안/타우모스 제작 두루마리 시리즈, 묘목·욕조·포스터 묘사.
- 용어: 황폐해진 돌 파편, 에메랄드 글림프스, 데드비트 함, 생크틸라이트, 타우모스, 아얄라, 아우로자(리조트명).
- 덤프 미표시 개행 7건 보정(제작 두루마리 5종의 녹색 해금 조건 행, 110405 아우로자 개장공지).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0400 (110213~110320, 50건)

- 타브리야 기후 보고서, 에이스네 참회 의식, 무기 거치대 시리즈, 레시피 묘사 연속.
- 용어: 타브리야, 이조 조류, 크라이오코럴 프로젝트, 스트포지드, 에이스네(아이트리 에이스네), 칼라인, 극저온 추출물, 회상의 판테온.
- 덤프 미표시 개행 4건 보정(110226 기도 요청, 110253 RT 미지원 안내, 110269 연료 스탯, 110307 후단).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0399 (110062~110212, 50건)

- 행성 스캔 대사 연속(독성/지옥/몽환/알테라시), 툰 종족 묘사+스탯 블록, 포스터/인형/파이묘사.
- 용어: 알루니카, 칼린, 하데사이트, 콰이어투스, 파이라이트, 파라데아, 아발리, 알타 사랑의 날, 아바의 날, 플러팔로, 팝볼, 툰.
- 덤프 미표시 개행 6건 보정 — 110110/110111은 전체 스탯 블록(능력치~종족 특성)을 기존 라벨 관례 그대로 복원.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0398 (109972~110061, 50건)

- 스타페어러 패스 3종, 음식/소품 묘사, "이곳은~" 주거·자유대사 연속, 네키 다수.
- 용어: 뱅가드 사격장, 길리카다, 피조닉 에너지, 칼린, 핫브뢰드, 회상의 판테온, 먼지의 탐구자, 크레이튼.
- 덤프 미표시 개행 2건 보정(109993 코덱스 안내, 110027 씨앗 요구 목록 — 스맥루트/플래브허브 등 확정 씨앗명 재사용).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0397 (109797~109971, 50건)

- 알타 유물/소품 묘사, 스타리스 가루, 바이오니드, 네뷸라사이트 투구, 리샨 그림.
- 용어: 못츠, 엘린 정원, 아야, 포스포리온, 스타리스, 프로토스피어, 크로늄, 바이올륨, 팜워치, 미스터리 알 상자, 스타페어러의 피난처, 콜트(인명), 스타리 컬티스트, 모나크.
- 덤프 미표시 개행 4건 보정(109857 코덱스 안내, 109865 면역 블록, 109876 모나크 경고문, 109933 바이오니드 후반부).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0396 (109667~109796, 49건)

- 메크 팔 시리즈, 자기 스테이션, 루카리오 메가 생물학 로어, 세테라이 프로젝트 문서, 크토니안 위성.
- 용어: 비신, 체레라, 야라, 메테오블래스터, 별조각, 크토니안, 엔테라시, 알테르니아, 헤비카이 사건, 미스터리 알 상자.
- 덤프 미표시 개행 3건 보정. 109784 태그 순서(세테라이→헤비카이) 정정 — qa_structure가 색태그 순서 교환을 못 잡는 한계 확인, 수동 대조로 검출.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0395 (109406~109654, 50건)

- 건조기/먹이통/램프, 크라코스 안전 서신, 머신 미니게임 목록, 리샨의 씨앗 로어.
- 용어: 케프라이더, 게아네이드, 아우레아, 델파 벌집, 바이온, 미아즈마, 브레첼.
- 덤프 미표시 개행 4건 보정(`4타 콤보`, `출혈 유발`/`사냥 무기` 라벨).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0394 (109282~109403, 50건)

- 램프 시리즈, 알타 수도/군 소속 문구, 네필림 조사, 주크박스, 라타시아 아카이브.
- 용어: 네필림, 탑파 대도서관, 알리아나, RAA(정규 알타군), 아이소슬라임, 이소슬라임, 이조 잼, 문 빔 스태프, 별빛 광선 지팡이.
- 덤프 미표시 개행 1건 보정(109349 아카이브 후문).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0393 (109169~109280, 50건)

- 꽃 가게, 리코이 도적, 아비칸/코덴·노멘 로어, 스탯 블록 1건(109252), FU 도구·장비.
- 용어: 아스라/루인, 크네므 섬, 우르사, 일렉트로켐 플럭스 코어, 100-LG, 코발런스, 하드라이트, 비오니아, 알테라시, 오라클.
- 덤프 미표시 개행 4건 보정. 스탯 블록 관례(`특성/저항/면역/종족 특성`, `냉기 저항`, `방어력`) 적용.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0392 (109075~109168, 50건)

- 상점/선물 대사, 게슈탈트 컬트 로어, FU 도구 서술, 메크 본체 보상.
- 용어: 리프트다이버 메크 몸체, 아스트랄리스, 래그리스 픽셀 프린터, 2-스톱 텔레숍, 게슈탈트, 성장하는 자의 교회, 알터스피어, 베피스.
- 덤프 미표시 개행 6건 보정. 스탯 라벨 `DEF`→`방어력`, `Damage`→`피해` 관례 적용(행 9644).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0391 (108953~109074, 50건)

- 네온 종족 사인 7종, 셔틀 부품, 네키 대사, 라타시아 광고 문서, AK 계열 총기.
- 용어: 세리즈, 세피라, 빌-C48i, 이리사 상인, 스푸키 키티, 셔틀 프레임/모듈/스타일, 프로그, AK-12.
- 덤프 미표시 개행 4건 보정(`유형: 초식` 라벨, 티우니 광고 본문 등).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0390 (108854~108952, 50건)

- 하이로틀 침공 로어, 냉장고 이후 가구/요리/행성 서술, 회상의 판테온·나이트메어 캐즘 위치, 데이터매스.
- 용어: 칼린, 톤노바, 바이오니드, 아크나이트, 회상의 판테온, 나이트메어 캐즘, 아우로자,프로그 가구점, 맹독 샘플, 목스 풀더, 팔케 장군, 플라스틸.
- 덤프 미표시 개행 6건 보정. `Beacon` → `신호기`, `[LMB]/[RMB]` 토큰 보존, 러시아어 인용구 의역(`늙었지만 쓸모 없진 않다.`).
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0389 (108698~108846, 49건)

- 무기/장비 서술, 네키 대사, 임신 안내서, 루카리오 조련사 로어, 카우보이풍 대사.
- 용어: 루카리오, 빅 에이프 정권, 코버넌트, 에너스 엔지니어링, 노스토스, 네이테루, 소나병사, 스타리 컬티스트, 아바의 날, 할버드.
- 덤프 미표시 개행 2건(108698, 108771) 수정. `Hunting weapon` 라벨 `^cyan;사냥 무기^reset;`.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0388 (108548~108697, 49건)

- 냉장고 변형, 묘목 시리즈, 선물 대사, 비에라 숲 서술, 소나베일/세터니티 안내서, FU 온보딩 대형 문서.
- 용어: 보호국, 글레이브, 물질 조작기, 퀵바, 유전자, 프로테온, 광기, 인스타프로이트, 형이상학, 승무원 증서/침대, 노바키드 모나크, 극저온 추출물, 기트신, 스타더스트 오키드 오르키.
- 108697: 다중 색 태그 구조에서 순서 3건 정정(질주/비행 모드 줄, 형이상학 소비 줄, 함께사용 불가 줄) 및 미닫힘 `^yellow;` 반영.
- QA: 구조 0건, 용어 오탐 4건 유지.

### 0387 (108443~108545, 50건)

- 도구/과일/시설 서술, 스틸 사건록, 논리 평가 회로, 소나베일 축제 요리·포스터 서술.
- 용어: 알데론, 엘리시아 동맹, 요캣, 펭귄 피트, 레테이아 코퍼레이션, 전초기지, 소나스위트, 코이와, 토나, 야비, 코르팔, 눈알타, 그을린 코어, 수라-플라스마, 옴니 풀.
- 108498: 원문의 미폐쇄 태그(orange 뒤 reset 하나) 순서를 그대로 유지해 초기 과잉 `^reset;` 정정.
- QA: 구조 0건, 용어 오탐 4건 유지.

- 배치 0386(ID 108313~108428, 알타 문서 개요 시리즈 — EDS/ADMU/CEN/에너지원/장비 세트,
  문·드론 묘사) 50개는 구조·용어 QA를 통과했다. `Alternia`→`알테르니아`,
  `Ceterai project`→`세테라이 프로젝트`, `nivera sentia`→`니베라 센티아`,
  `Miara`→`미아라`, `bionical/bionicas`→`바이오니칼/바이오니카`,
  `Archangel Xequeyzriel`→`대천사 세퀘이즈리엘`, `Enviro`→`환경 세트`,
  `ADMU`→`자동 방어 기동 유닛` 적용.
- 배치 0385(ID 108178~108312, 생물·식물 묘사, 알타 요리·문서, 각종 장치 묘사,
  러스틀링 묘사) 50개는 구조·용어 QA를 통과했다. `Centensian`→`센텐시안`,
  `Iceterion`→`아이스테리온`, `Aventor`→`아벤토르`, `Veronas`→`베로나스`,
  `Staris`→`스타리스`, `calin`→`칼린`, `bishyn`→`비신`, `Capture Pod`→`포획용 포드`,
  `nidias`→`니디아`, `FIELDRON`→`필드론`, `Elin`→`엘린`, `rail-pistol`→`레일 피스톨`,
  `Strains`→`가닥` 적용. ID 108311 `depiction`도 원문이 끊긴 상태라 `이것은 보여 준다`로옮김.
- 배치 0384(ID 108019~108177, 소파·찬장 묘사, 유전자 조작 묘목 시리즈, 노바키드 무법자 광산,
  소나베일 폭죽, 마리아 봉헌 이야기) 50개는 구조·용어 QA를 통과했다. `Outlaw Mine`→`무법자 광산`,
  `bionid`→`바이오니드`, `endomorphic jelly`→`엔도모픽 젤리`, `protosystem`→`프로토시스템`,
  `moonrock`→`달 암석`, `harbinger`→`선구자`, `Seeker`→`시커`, `cloud fibre`→`구름 섬유`,
  `solstice`→`동지` 재사용·신규 확정. ID 108049 `depiction`은 원문이 문장 중간에 끊긴 상태라
  그대로 `이것은 기념한다`로 옮겼다.
- 배치 0383(ID 107822~108018, 가구 묘사 대량 — 찬장·의자·샹들리에·천장등, 알타
  식재료와 샤를로트, 아스테라 일지) 50개는 구조·용어 QA를 통과했다. `Jinxies`→`징시즈`,
  `Estria`→`에스트리아`, `caliopa`→`칼리오파`, `faro koywa`→`파로 코이와`,
  `alunika`→`알루니카`, `tonnova spring`→`톤노바 샘`, `Frozen Energy Ball`→`얼어붙은 에너지 볼`,
  `chronium`→`크로늄`, `kupo-ku`→`쿠포-쿠`, `Necotho`→`네코토`,
  `Cosmic damage`→`우주 피해` 관행 재사용. ID 108010의 마크다운 줄바꿈(행 말미 이중 공백) 보존.
- 배치 0382(ID 107718~107821, 네키 대사 `~다냥`, 비에라·모글 제작서 시리즈,
  새터니안 무기서, 루네바 요리서, 고양이 펫 상자) 50개는 구조·용어 QA를 통과했다.
  `Grand Protector`→`대보호자`, `Wood Warders`→`우드 워더`, `Moogle`→`모글`,
  `Dalmascan`→`달마스칸`, `brain extractor`→`뇌 추출기`,
  `forge (upgraded anvil)`→`대장간(개량된 모루)`, `fleabag`→`벼룩투성이`,
  고양이 품종은 `초콜릿 페르시안/레드 태비/러시안 블루/화이트 페르시안/샴 고양이`,
  루네바 요리명은 `길 타르트/소이/아야 프라임/그린 바이트/길 씨앗 쿠키/파우더 칩 쿠키/
  차이-길 잼/알테라시 브리즈/알리바나`로 신규 음차. ID 107754의 starbounder 링크 URL 보존.
- 배치 0381(ID 107571~107717, 크라코탄 종교 상징, 알타 전자책·식재료(아야·길·차이),
  가구 주괄 시리즈(물결/파멸/부유한/고요함의/임원의/기하학적), 침대 묘사, EDS 장비) 50개는
  구조·용어 QA를 통과했다. `Ri'shaan`→`리샨`, `K'Rakothan`→`크라코탄`,
  `mechineki`→`메키네키`, `frozen-fire`→`동결화염`, `phosic energen`→`포직 에너젠`,
  `arigaran`→`아리가란`, `arkanas`→`아르카나`, `Elerune CDR`→`엘러룬 CDR` 적용.
- 배치 0380(ID 107474~107567, 알타 NPC 묘사 대량 — 미니크녹 침투 프로젝트/특별팀/연구원
  시리즈, 아바의 날·세터니티 상인, 전사 코스프레) 50개는 구조·용어 QA를 통과했다.
  `aya virma`→`아야 비르마`, `Ava Day`→`아바의 날`, `Ceternity`→`세터니티`,
  `Iora Gyera Ordis`→`이오라 기에라 오르디스`, `vionia`→`비오니아`, `orbides`→`오르바이드`,
  `K'Rakoth`→`크라코스`, `Gateway`→`차원문`, `MiniKnog Infiltration`→`미니크녹 침투`,
  반복 제복 문구는 `이 제복은 알타 고유의 것은 아니지만, 임무의 일환으로 입고 있다.`로 통일.
- 배치 0379(ID 107401~107471, 함선 방문/적대 묘사 시리즈, 주문 무기(마법구·주문발사기),
  행성 묘사, 카우보이 풍 대사) 50개는 구조·용어 QA를 통과했다. `Spellorb`→`마법구`,
  `Spellthrower`→`주문발사기`, `Holy Fire`(속성 라벨)→`성화`, `Technowizard`→`테크노마법`,
  `Rebel Angel`→`반란 천사`, `chthonian`→`크토니안`, `Goa'uld`→`고아울드`,
  `Nicemice`→`나이스마이스`, `kupopo`→`쿠포포`, `abomination`→`흉물` 적용.
  ID 107420의 `<gift>`·`<target>`·`<target.pronoun.object>`는 그대로 보존했다.
- 배치 0378(ID 107333~107400, 소-플리시티 비에라 의상 도안 11종, 알타 데이터매스·전자책
  시리즈, 색상 태그 행성/식물 묘사 다수) 50개는 구조·용어 QA를 통과했다. 비에라 직업명은
  `궁수/암살자/엘리멘탈리스트/펜서/녹마법사/적마도사/스나이퍼/마검사/소환사/백마도사/드래군`으로
  정리. `Goa'uld`→`고아울드`, `Burger Fool`→`버거 바보`, `Holy Light`→`신성한 빛`,
  `Holy Power`→`신성한 힘`, `stardust`→`스타더스트`, `datamass`→`데이터매스`,
  `ebook`→`전자책`, `corplic`→`코플릭`, `haven`→`헤이븐` 재사용·신규 확정.
  `Press -`/`Hold -` 입력 힌트는 `누르기 -`/`길게 누르기 -` 관행을 따랐다. 병합 후 검수에서
  `Poptop`을 TM 표기 `팝탑`이 아닌 고정 용어 `팝톱`으로 정정하고, ID 107375의 색상 태그
  순서를 원문 순서로 교정했다.
- 배치 0377(ID 107175~107324, NPC 사고 라벨, 알타 이야기 설명, 비에라·천사·아발리·새터니안
  조사 대사, FU 시설/EPP 설명, 천사풍 솔라리움 무기, 페어리-TAC 카빈 다중행, 트링키안 중앙 서킷
  단말기, 오로타움 코덱스 페이지) 50개는 구조·용어 QA를 통과했다. `Grand Temple`→`대신전`,
  `The Circuit`→`서킷`, `Angelic`→`천사풍`, `Lodstone`→`자석석`(Lodestone 변형),
  `Orothaum`→`오로타움`, `Arma Inferia`→`아르마 인페리아`, `Unustrello`→`우누스트렐로`,
  `Stick of RAM`→`RAM 카드` 기존 표기 재사용. ID 107216의 `<selfname>`은 그대로 보존.
- 배치 0376(ID 107111~107174, 두꺼운 건축 자재·음식, 도둑 경고 대사, NPC 상태 생각 라벨)
  50개는 구조·용어 QA를 통과했다. `Sona Milk`→`소나 우유`, `Eisenite`→`아이제나이트`,
  `Kodorric`→`코도릭`, `polyradish`→`폴리래디시`, `Punisher`→`응징자`,
  `Rimdweller`→`림드웰러`(림 해치 등) 기존 표기 재사용. 상태 라벨은
  `추출 가능/체질 가능/제련 가능` 관행, statuses.config 라벨은 `~중` 관행을 따랐다.
- 자리표시자 오염 정리(2026-09-25, 사용자 지적에서 발견): 구형 번역이 런타임 토큰을 한국어로
  번역한 결함을 전수 조사·복원했다. `Feline <field> Officer`→`고양이 <필드> 장교`처럼
  `<필드>`로 번역된 승무원 계급은 설치된 `mods/FU_KO_contents_3166424163.pak`에서
  라이브로 깨져 있었다(`<역할`은 닫는 괄호까지 누락). `alignment/fu.tsv`(60)·
  `alignment/gic.tsv`(250)·`translation_memory.tsv`(33)·`legacy_translation_memory.tsv`(73)와
  코퍼스 파일들을 정리했고, FU 원본 pak에서 확인한 정답은 `<적>`→`<enemy>`,
  `<원소명>`→`<elementalName>`(패치가 `"<elementalName> Aura"`를 씀),
  `<받은아이템>`→`<receivedItems>` 등이다. `<unknown>`→`<알 수 없음>` 계열과
  `<insert subject name here>`→`<여기에 대상자 이름을 입력하세요>` 같은 서술·농담 괄호는
  토큰이 아니므로 번역을 유지했다. 바닐라 공식 번역(sbkor)의 토큰 생략은 우리 범위 밖이라
  두고, 신규 검사 `qa_tokens.py`를 추가했다(잔여 후보는 sbkor 유래 TM 12건뿐). 리팩 단계에서
  재생성되는 오버레이에 수정이 반영되는지 인게임 확인 필요.
- 배치 0375(ID 107044~107110, 세테라이·알파타우르·칼리오 종족 소개와 능력치 블록,
  두꺼운 건축 자재 시리즈) 50개는 구조·용어 QA를 통과했다. `Alpataur`→`알파타우르`,
  `Ceterai`→`세테라이`, `Calio`→`칼리오`, `Allosteel`→`알로스틸`,
  `Charisma`→`카리스마`, `Mastery`→`숙련`을 적용했다.
- 배치 0374(ID 106968~107042, 폭발물 부족 종족 소개, 참호전 보고, 인질 실종 무전) 50개는
  구조·용어 QA를 통과했다.
- 배치 0373(ID 106880~106967, 실험체 쌍둥이 보고, 해적 조우 경보, 업그레이드 장치 설명,
  알타 정예 발전기) 50개는 구조·용어 QA를 통과했다. 이 배치 작업 중 사용자가
  `Spooked`를 `겁먹음`으로 확정(`translation_glossary.tsv`에 `추격당함 금지` 명시).
- 배치 0372(ID 106773~106879, 게아룬 발굴 프로토콜, 에터니아 수정, 알타 정예 병사 장비,
  기술 도용 종족 소개) 50개는 구조·용어 QA를 통과했다.
- 사용자 용어 확정 반영(2026-09-25): `Akkimari`→`아키마리`, `Akki`→`아키`
  (동사 `아끼다` 용법은 보존). 상태이상을 부여하는 장비명은 `독성/일렉트릭 + 장비`
  (`일렉트릭 탄환`, `일렉트릭 마그노브`, `독성 뼈 가시`, `독성 마그노브`, `독성 칼날`)로
  통일하고, 실제 상태에 걸린 대상 묘사의 `중독된/감전된`은 유지한다.
- `Spooked` 후속 정리: `translation_memory.tsv`의 `추격당함`을 `겁먹음`으로 교체하고,
  면역 목록의 잔여 `공포`(id 26786, 106189)·`겁에 질림`(id 32185)을 `겁먹음`으로 통일.
  `rest_worklist`에 남은 `Spooked` 행은 번역 시 용어 QA가 `겁먹음`을 강제한다.
- 검수 지침 추가(사용자): 원문 대조 시 `우리 모두 합쳐 뇌세포가 하나다`(id 106189) 같은
  부자연스러운 문장도 잡아낼 것 — 해당 행은 `우리 모두를 합쳐도 뇌세포가 하나뿐이다.`로
  정정했다.

- 배치 0371(ID 106641~106772, 엔테르니아 코덱스·알타 용어, 종족 능력치 블록 두 건,
  플러시바운드 제작자 크레딧 두 페이지) 60개는 구조·용어 QA를 통과했다.
  `Sonaveil`→`소나베일`, `ceternia`→`세터니아`, `enternia`→`에터니아`,
  `archulin`→`아르출린`, `nebulathite`→`네뷸라사이트`, `kinetic orb cannon`→`운동 구체포`,
  `Io`→`이오`를 기존 표기대로 재사용했고, 크레딧 페이지는 배치 0237의
  `X가 만들고 다음 분들이 의뢰함` 양식과 `인형` 표기를 따랐다.

- 배치 0370(ID 106538~106640, 네뷸락·사슴족·골차르 동굴 거주자 능력치, 알타 결정·
  연구실 장비, 아바의 날 쿠키) 50개는 구조·용어 QA를 통과했다. `gheatsyn`→`기트신`,
  `Faradea`→`파라데아`, `bionid`→`바이오니드`, `Pulse Paralysis`→`펄스 마비`를 적용했다.

- 배치 0369(ID 106466~106536, 대사관 대사, 천사·루인드 대사, 메구무, 열기 장비와 하데시움
  능력치 블록) 50개는 구조·용어 QA를 통과했다. `Peacekeepers`→`피스키퍼`, `Megumu`→
  `메구무`, `Tonguile`→`통글리`, `Hadesium`→`하데시움`을 적용했다.
- 배치 0368(ID 106371~106460, 비르마술사 로어, GTC 컨테이너 퀘스트, 여족장 시,
  천사·네키 대사) 50개는 구조·용어 QA를 통과했다. `virma`→`비르마`, `Enerth`→`에너스`,
  `Miniknog`→`미니크녹`을 적용했다.
- 배치 0367(ID 106297~106370, 빅 에이프 선전시, 에지 역사, 호라이즌·미니크녹 임무,
  레나틴 수정 설명) 50개는 구조·용어 QA를 통과했다. 사용자 표기 `Aegi`→`에지`를 적용하고,
  `K'Rakoth`를 기존 표기 `크라코스`로 맞췄다.
- 배치 0366(ID 106200~106294, 타임리스 행성, 라데이스 로어, 사신·방패 산문,
  우프 본부 소문) 50개는 구조·용어 QA를 통과했다. `Aeon Timepiece`→`이온 타임피스`,
  `Rhadeis`→`라데이스`, `Letheia`→`레테이아`를 재사용했다.
- 배치 0365(ID 106112~106199, 알타 결정과 펠린의 길, 생물군계 안내서 139행,
  아비안·천사 대사) 50개는 구조·용어 QA를 통과했다. 긴 안내서는 원문의 줄바꿈과 색상 태그를
  유지하며 직접 대조했고, `Grounded`는 아비안 분파 문맥에서 `지상인`으로 옮겼다.

- 배치 0364(ID 106048~106111, 텔리안·텔루시안 명칭, 아키마리 대사, 글리치 가문 로어,
  사이버맨 설명과 사냥 재료 안내) 50개는 구조·용어 QA를 통과했다. `Thellar`→`델라`,
  `Thelean`→`텔리안`, `Thelusian`→`텔루시안`, `Arcane Water`→`아케인 물`을 적용했다.
- 배치 0363(ID 105968~106047, 에이스네 현현, 천사 날개 로어, 종족 능력치 블록 두 건,
  텔리안 명칭) 50개는 구조·용어 QA를 통과했다. 용어 QA에서 `Cultivator`와 `wood-warder`를
  각각 `컬티베이터`, `숲의 파수꾼`으로 정정했다.
- 배치 0362(ID 105891~105967, 우주 탐사 대사, 라타시아 바이러스, 불페라 능력치,
  블루 블레이드 로어, 성냥개비 건블레이드) 50개는 구조·용어 QA를 통과했다. 용어 QA에서
  `Cultivator`를 `컬티베이터`로 정정했다.

- 배치 0361(ID 105806~105890, 먼지·노스토스 로어, 브리치 구체 시험, 종족 능력치 블록,
  우주·촉수 관련 대사) 50개는 구조·용어 QA를 통과했다. `Carmain`은 기존 인명 `Carmine`의
  오기로 보고 `카민`을 썼고, `Kadavan Sandcrawler`는 `카다반 샌드크롤러`로 통일했다.
  용어 QA에서 `Cultivator`를 `컬티베이터`로 정정했다.
- 배치 0360(ID 105723~105805, 노스토스 연구, 에이펙스 함선 작전, 표적 대사, 텔리안 검,
  성인 콘텐츠) 50개는 구조·용어 QA를 통과했다. `Big Ape`→`빅 에이프`, `Breach Sphere`→
  `브리치 구체`, `Akkimari Justicar`→`아키마리 저스티카`를 재사용했다. 용어 QA에서
  `Teleporter`를 `텔레포터`로 정정했다.
- 배치 0359(ID 105643~105722, 키테란·천상 정령 로어, 다섯 특수 행성, 우주선 정착 기록,
  무기·가구 설명) 50개는 구조·용어 QA를 통과했다. `gheatsyn`→`기트신`, `Kyterran`→
  `키테란`, `Celestial Corridor`→`천상 회랑`, `Seeker of Dust`→`먼지 탐구자`를 적용했다.

- 배치 0358(ID 105560~105640, 자아 화자 대사, 센텐시안 방어막 수리, 함선 안내, 루인드·로즈 제국
  로어, 성인 콘텐츠)는 구조·용어 QA를 통과했다. `Hiraki Corale`→`히라키 코랄레`, `Centensian
  Tech/Metal`→`센텐시안 테크/금속`, `The Ruined`→`루인드`, `Seonha`→`선하`, `Parasitic
  Goo`→`기생 점액` 등 기존 표기를 사용했다.
- 배치 0357(ID 105483~105559, 테라 소행성 충돌 후 기록, VEP 실험 결과, 무기·이동 설명,
  비에라 시련과 요괴 작전 로어) 50개는 구조·용어 QA를 통과했다. `Plasma Burn`→`플라즈마화상`,
  `Downstab`→`내려찍기`, `polyradish`→`폴리래디시`, `scintillium`→`신틸리움`을 재사용했다.

- 배치 0356(ID 105409~105482, 센텐시안 액체 퀘스트, 사이버웨어 관련 장비, 에스더 브라이트 일지,
  ITN 보관 체계, R.S.O 무기 설명, 카라키녹 종족 특전)는 구조·용어 QA를 통과했다. `Centensian
  Liquid`→`센텐시안 액체`, `Esther Bright`→`에스더 브라이트`, `Asra Nox`→`아스라 녹스`,
  `ceternia`→`세터니아` 등 기존 표기를 적용했다.
- 배치 0355(ID 105330~105408, 사이버웨어 알약, 엘리시아 이주 역사, 아가란 선교사 로어,
  알타 포스터와 무기·음식 설명) 50개는 구조·용어 QA를 통과했다. `Insanity Shield`→
  `광기 보호막`, `Creon City`→`크레온 시`, `tonna`→`토나`, `nia jam`→`니아 잼` 등 기존
  표기를 재사용했다.

- 배치 0354(ID 105255~105328, 알타 로어·농법, 하이로틀 능력치 블록 두 건, 퀘스트·가구·성인
  콘텐츠 설명) 50개는 구조·용어 QA를 통과했다. `runeva`→`루네바`, `tavriya`→`타브리야`,
  `Matter Manipulator`→`물질 조작기`, `NostOS`→`노스토스` 등 기존 표기를 재사용했다.
- 배치 0353(ID 105169~105254, 악티아스 역사, 옥타리안 능력치 블록 두 건, 아가란 포자 연구
  기록과 다양한 대사·설명) 50개는 구조 QA를 통과했다. 용어 QA가 잡은 `Actian`의 지명형 오역을
  종족 표기 `액티안`으로 정정한 뒤 기존 기준선 4건만 남았다. 성인 콘텐츠는 원문의 노골적의미를
  유지했다.

- 배치 0352(ID 105097~105168, 알타 재료와 생태 챔버, 비에라 의식, 마르페시아 로어, 인명대사,
  MP5 레일 개조 설명) 50개는 구조·용어 QA를 통과했다. `Aureola`→`아우레올라`, `Eithne`→
  `에이스네`, `Green Word`→`초록의 말씀`, `Unustrello`→`우누스트렐로`, `Lana Blake`→
  `라나 블레이크` 등 기존 표기를 적용했다. 노골적인 농담은 원문 뜻을 살려 검토 중 정정했다.
- 배치 0351(ID 105024~105096, 전차·알타 농법·네키 로봇 종족 능력치·아가란 기록·무기 설명)
  50개는 구조·용어 QA를 통과했다. 종족 능력치 블록 두 건의 태그·개행을 원문대로 보존했고,
  `Magicite`→`마기사이트`, `Magnetar`→`마그네타`, `ST Syllectis`→`ST 실렉티스`,
  `Akris`→`아크리스` 등 기존 표기를 재사용했다.
- 배치 0350(ID 104934~105023, 소총·무기·루카리오 로어, 비에라와 베스페리안 종족 능력치,
  퀘스트·물약 설명) 50개는 구조 QA를 통과했다. 용어 QA가 잡은 `Two-Handed`의 `두 손`을
  고정 표기 `양손`으로 정정한 뒤 기존 기준선 4건만 남았다. `[ALT-FIRE]`, `[SHIFT]`와
  색상 태그·개행을 보존했다.

- 배치 0349(ID 104876~104933, 피규어 설명, 새터니안 역사, 착륙 지점 위험 안내, 유물 퀘스트,
  알테라시 프라임 연구 기록) 50개는 구조·용어 QA를 통과했다. `Fennix`→`페닉스`, `Yokat`→`요카트`,
  `Solalei`→`솔라레이`, `Ancient Remote`→`고대 리모컨`, `Cooling EPP`→`냉각 EPP` 등 기존용어를
  재사용했다. `83 Quadrillion`은 한국어 수 체계로 `8경 3천조`로 옮겼다.
- 배치 0348(ID 104826~104875, 피규어 표지 설명 50개)는 구조·용어 QA를 통과했다. `Algeist`→
  `알가이스트`, `Nutmidgeling`→`넛밋지링`, `Orbide`→`오바이드`, `Crippit`→`크리핏`, `Hemogoblin`→
  `헤모고블린`, `gheatsyn`→`기트신`을 재사용했다.
- 배치 0347(ID 104776~104825, 피규어 표지 설명 50개)는 구조·용어 QA를 통과했다. `Vesomeyr`→
  `베소마이어`, `Serohalaphim`→`세로할라핌`, `Ultarubim`→`울타루빔`, `Poptop`→`팝톱`을 적용했다.
  `semi-sapient`를 `반쯤 지성을 지닌`으로 검토 중 정정했다.
- 배치 0346(ID 104719~104775, 델파 하이브 무기 기록과 피규어 표지 설명 50개)는 구조·용어QA를
  통과했다. `Esoquartz`→`에소쿼츠`, `Orothaum`→`오로타움`, `Ce'Tennan`→`세테난`, `Faryth`→
  `파리스`, `Narfin`→`나르핀` 등 기존 표기를 재사용했다. `Akkimari scavengers`는 기존의
  `아키마리 약탈자들`에 맞췄다.

- 배치 0345(ID 104647~104716, 루카리오 역사, 벌집 대사, 행성·호라이즌 로어, 조로아크 종족 능력치,
  이르켄 종족 특전, 알테라시·EDS 설명) 50개는 구조·용어 QA를 통과했다. `Dreadwing`→`드레드윙`,
  `Ionic Shock`→`이온 쇼크`, `Irken`→`이르켄`, `Nereus`→`네레우스`, `Miracle of Fire`→`불의 기적`,
  `Avid Explorer`→`열정적인 탐험가` 등 기존 번역을 재사용했다. 영어의 `impulses`는 무기설명
  문맥에 맞춰 `펄스`로 정정했다.
- 배치 0344(ID 104536~104646, 혼돈 주문 단계, 루인 파편, 라이트헤이븐·회상의 판테온 로어,
  유령·무기·식물 설명, 대사) 50개는 구조·용어 QA를 통과했다. `Sear`→`작열`, `Embrittle`→
  `취약화`, `Faryth`→`파리스`, `Pantheon of Recollection`→`회상의 판테온`, `Aether Tanto`→
  `에테르 탄토`를 기존 번역에 맞췄다. `AEG-Corps`는 기존 영문 고유 표기를 유지하도록 정정했다.
- 배치 0343(ID 104452~104535, 장비·국가 역사·종족 깃발·전투·알타 발굴 규약) 50개는 구조·용어
  QA를 통과했다. 용어 재검토 중 `gheatorn`과 `gheaprism`을 각각 기존 표기 `게아토른`,
  `게아프리즘`으로 정정했다. 입력 토큰 `[E]`, `%s`, 색상 태그와 개행은 보존했다.
- 배치 0338~0342(ID 104416~104451)는 사용자의 연속 5배치 요청에 따라 각 5개씩 총 25개를
  처리했다. 구조·용어 QA는 통과했으나 배치당 양이 적다는 사용자 지적을 반영해 0343부터
  권장 검토 단위인 50개로 되돌렸다. `GelorieMate`는 기존 표기 `겔로리메이트`로 정정했다.
- 배치 0337(ID 104385~104413, 에너지 광산, 천상의 회랑, 트링키안 건물, 아우레아 콜렉티브로어)
  20개는 구조·용어 QA를 통과했다. 두 차례에 나누어 병합했지만 하나의 배치 파일로 기록했다.

- 배치 0336(ID 104357~104384, 음식·장비·대사관·행성 설명, 종족 능력치 블록, 적 출현 전투대사)는
  구조·용어 QA를 통과했다. 색상 태그와 종족 능력치 라벨을 원문 구조대로 보존했다.

- 배치 0335(ID 104300~104356, 글리치·드래곤·키츠네 대사, 문·무기 복구 퀘스트, 트링키안 제작 해금,
  브루톨 로어, 이조포이 조리법, 프리미피케이션 전자책, 플로란 전쟁 기록, 볼티지 행성 설명)는 구조·용어
  QA를 통과했다. 기존 표기 `Trinkian`→`트링키안`, `Brutol`→`브루톨`, `Miniknog`→`미니크녹`,
  `Horizon`→`호라이즌`, `izopoi`→`이조포이`, `Izo Jam`→`이조 잼`, `Biomix Ice Cream`→
  `바이오믹스 아이스크림`, `primification`→`프리미피케이션`, `Voltage`→`볼티지`를 재사용했다.

- 배치 0334(ID 104265~104296, 테라 소행성 충돌과 VEP 연구 기록, 드래곤 비행선 로어, 덴드라리움
  안내, 오토탱크·무기·음식 설명, 에지 종족 설명과 능력치 블록, NPC 대사)는 구조 QA를 통과했다.
  `Aegi` 표기는 사용자 선택에 따라 `에지`로 확정하고 글로서리와 기존 번역 63건을 함께 갱신했다.
  이후 용어 QA는 기존 기준선 4건(Miniknog/Trink/The Ruined/Kappa)만 남았다. `Elithian Alliance`는
  기존 표기 `엘리시아 동맹`, `Dendrarium`은 `덴드라리움`, `Glimmlecus Tower`는 `글림레쿠스 탑`으로
  재사용했다. 종족 능력치 블록에는 표준·커스텀 라벨과 고정 표기 `Grenade Launcher`→`유탄발사기`를
  적용했다.

- 배치 0333(ID 104228~104264, 결정·무기·폭풍 아이템 설명, 하피병 치료 장비, 광신도·드래곤·네키·섀도우
  NPC 대사, 독성 다트 소총 설명, GIC:E 데이터 기록과 리샨·크라코스 코덱스 대화)는 구조·용어 QA 모두
  첫 시도에 통과했다(기준선 4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 표기 재사용:
  `hevika`→`헤비카`, `carels`→`카렐`, `miazmas`→`미아즈마`, `viona`→`비오나`, `Ri'shaan`→`리샨`,
  `K'Rakoth Codices`→`크라코스 코덱스`, `Harpy Disease`→`하피병`. 색상 태그·개행을 원문과 정확히
  보존했고, `higher beings`은 문맥상 `상위 존재`로 옮겼다.

- 배치 0332(ID 104157~104227, 아비칸·얼라이언스 장비 설명, 알타 이온 코어 감시 기록, 텔리안 재료 수집
  퀘스트, 조류 종족 능력치 블록, 우주선 조우 설명 21건, 수정·고대 무기 설명, 짧은 로어와대사,
  성인 콘텐츠 1건)는 구조·용어 QA 모두 첫 시도에 통과했다(기준선 4건 Miniknog/Trink/The Ruined/Kappa
  유지). 기존 표기를 재사용: `Avikan`→`아비칸`, `Alliance`→`얼라이언스`, `Centensian`→`센텐시안`,
  `Thelean`→`텔리안`, `Drahl`→`드랄`, `Frogg`→`프로그`, `Agaran`→`아가란`, `Novakid`→`노바키드`,
  `Relic Seeker`→`유물 탐구자`, `Protectorate`→`보호국`, `Cosmonaut Ship`→`코스모넛 우주선`,
  `Astro Merchant Ship`→`아스트로 상선`, `Industrial Merchant Ship`→`산업 상인 함선`, `Devout Ship`→
  `데보트 우주선`, `Boneboo`→`본부`, `gil`→`길`. 종족 능력치 블록은 README의 표준 라벨 세트
  (`능력치`, `최대 체력`, `에너지 재생`, `저항`, `면역`, `종족 특성`, `수영 강화(대체)`등)를 적용했다.
  신규 표기: `Plasmic Strains`→`플라즈믹 스트레인`, `Thelean Metal Fragments`→`텔리안 금속 파편`,
  `Anarkyon`→`아나키온`, `Vera`→`베라`, `Kria`→`크리아`.

- 배치 0331(ID 103925~104156, 잡다한 아이템·가구·대사 대량("The back...", "The best...","The
  bl(a/o)...", "The c...")로 특정 주제 쏠림 없이 폭넓게 분포. 텔루시안(육식 갑각형 종족)스탯 블록,
  해로운 여우(baneful fox)/고전적 외계인(에이펙스 기원 설정) 스탯 블록 2건, 빔 다운 사이트(행성
  묘사) 텍스트 다수, 알타 수도/성채/의식 로어 3건, 에세테라 심연/알테르니아 크리스탈 로어, 유니탄
  세력 로어(리버레이터 전차, STC), 마르페시아 전투 묘사(contentpages), 실존 총기 로어(독일 연방군
  G36 카빈), 촉수(explicit) 콘텐츠 2건, 명시적 성적 콘텐츠 2건(정액 관련))는 구조·용어 QA 모두 첫
  시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 재사용:
  "Unitan"→"유니탄", "avali"→"아발리", "Aeon"→"에이언", "Occasus"→"오카서스", "Trink"→"트링크",
  "Rhadeis"→"라데이스", "the Wood"→"숲", "youkai"→"요괴", "Precursors"→"프리커서", "Alt Fire"→
  "보조 발사", "tsays"→"차이스"(모두 기존 선례). 실존 독일 총기(G36) 로어는 "Bundeswehr"→"독일
  연방군(분데스베어)"로 실존 군사 용어 관례에 따라 번역. 신규 고유명사(선례 없음, corpusgrep
  확인): "Aureola"(재료)→"아우레올라", "alternia"(에너지 결정)→"알테르니아", "Esetera"(행성명)→
  "에세테라", "Frogg"(종족명)→"프로그", "Thelusian"(종족명 형용사형)→"텔루시안", "gheatsyn"(재료)→
  "기트신", "yonnur"(생체발광 액체)→"요누르", "bionix"(재료)→"바이오닉스", "Vrelli"(식물명)→
  "브렐리", "Moli"(NPC명)→"몰리", "carels"(알타 식재료)→"카렐", "ayas/gils"(알타 식재료,tsays와
  병기)→"아야스/길스", "ayaka"(알타 식물명)→"아야카", "Bustow"(NPC명)→"버스토", "Glimmlecus
  Tower"→"글림를레쿠스 타워", "Relic Seekers"(세력명)→"유물 탐구자", "ST Syllectis"(기존"실렉티스"
  선례 활용)→"ST 실렉티스", "enterash/enterash prime"(기존 "alterash" 선례와 철자가 다른별개
  코퍼스 표기로 판단해 구분 음역)→"엔터래시/엔터래시 프라임".
- 배치 0330(ID 103732~103924, 뱅가드 세력 관련 대사·퀘스트 다수(크랄/드랄 차량, 야카르,카르마니),
  샤미드(포켓몬)/비에라(파이널 판타지) 등 실존 프랜차이즈 종족, 반타(나이타 신세대)/불페스/이드리치
  택배기사 등 오리지널 종족 스탯 블록, 워터폴 캇파 vs 야마와로 네일건 무기 로어 2건(양손/한손 변형),
  워처/라이오드/라데이스 관련 아비칸 종교 대사, 보이저 컴퍼니/인듀어런스 컴퍼니 지구 탈출 로어 2건,
  워크숍(기업 세력) 로어 3건, 행성 보호국/행성 선거국/행성 피스키퍼/행성 가디언 관련 정부 체계 로어,
  숲(the Wood)/비에라 신앙 대사 다수, 아르카니안 종족·문명 로어, 촉수(explicit) 콘텐츠 2건)는 구조
  QA 이슈 없음, 용어 QA에서 1종 발견되어 수정: "THRUST damage"를 글로서리 고정 표기 "찌르기 피해"
  대신 "관통 피해"로 옮긴 2건(id 103791/103792, 워터폴 캇파 네일건 설명)을 정정. `fix_0330.json`으로
  처리. 이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존 확립된 고정표기 재사용:
  "Kappa"→"캇파", "Tengu"→"텐구", "Yamawaro"→"야마와로", "Vanguard"→"뱅가드", "Krahl"→"크랄",
  "Arcanians"→"아르카니안", "Woolotl"→"우울로틀", "Green Word"→"초록의 말씀", "the Wood"→"숲",
  "Mycotoxin"→"마이코톡신", "Nephilim"→"네필림", "Annelisk"→"아넬리스크", "Terrene Protectorate"→
  "행성 보호국", "koywa"→"코이와"(모두 기존 선례). Pokémon·Final Fantasy 실존 프랜차이즈종족명은
  통용 한국어 표기 채택: "Vaporeon"→"샤미드", "Viera"→"비에라". 신규 고유명사(선례 없음):
  "Nightar"(종족명, 형용사형 "Nightarian"→"나이타리안"에서 역산)→"나이타", "Vanta"(나이타 신세대)→
  "반타", "Vulpes"→"불페스", "Drahl"(Krahl과 별개 유닛명)→"드랄", "Jakhar"(NPC명)→"야카르",
  "Kharmani"(행성명)→"카르마니", "Erito Security"→"에리토 시큐리티", "Zaibatsu"→"자이바츠",
  "Aurea Collective"→"아우레아 콜렉티브", "Terrene Electorate"→"행성 선거국"(Terrene Protectorate의
  "행성" 접두 패턴 적용), "Hylotl Stewardship"→"하이로틀 스튜어드십", "Oceanite"→"오셔나이트",
  "Instafreud"→"인스타프로이트"(Freud 말장난), "Nightmares"(종족명)→"나이트메어", "cerulium"→
  "세룰륨", "S.E.E.D."/"Ecolife Solutions"→ 원문 유지/"에코라이프 솔루션즈", "Graliaen"→"그랄리아엔",
  "Eithne"→"에이스네", "Marpesia"→"마르페시아", "tsays/ionice"(알타 요리 재료)→"차이스/아이오나이스".
- 배치 0329(ID 103512~103731, 로뮬런(스타트렉)/사이어인(드래곤볼)/타우렌(월드 오브 워크래프트) 등
  실존 프랜차이즈 종족 스탯 블록, 레모리안/리오피/셰이/스카스/스키피안/스펙트윙/타우르 등 오리지널
  종족 스탯 블록 다수, 실존 총기 로어(레밍턴 700·M24 SWS/레밍턴 ACR/S50/SN7P/쇠그렌 이너시아/슈타이어
  AUG) 다수, 라이오드/라데이스/바스 브할레이 관련 아비칸 종교 로어 6건, 싱킹 샌즈/라코리고지대
  아비칸 지리 로어, 텔레안/텔(Thell)/카다반 관련 대사 다수, 루인/루인드 관련 대사 다수,행성 보호국
  관련 대사 다수(오타 "Terene Protectorate" 포함, 모두 동일 표기로 통일), 독일어 억양 패러디 대사
  1건)는 구조 QA 이슈 없음, 용어 QA에서 1종 발견되어 수정: "Grenade Launcher"를 글로서리고정 표기
  "유탄 발사기"(공백 포함) 대신 "유탄발사기"(공백 없음)로 옮긴 1건(id 103680, 타우렌 무기 목록)을
  정정. `fix_0329.json`으로 처리. 이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인.
  기존 확립된 고정 표기 재사용: "The Ruined"→"루인드", "Terrene Protectorate"→"행성 보호국",
  "Thalasso"→"탈라소", "Ruinous planets"→"폐허가 된 행성", "Big Ape"→"빅 에이프", "Goblin"→"고블린",
  "lucario"→"루카리오", "Steyr"→"슈타이어", "Vas Vha'leih"→"바스 브할레이", "Rhadeis"→"라데이스",
  "Horizon"→"호라이즌", "Water Regen"→"물 재생", "Underwater Breathing"→"수중 호흡", "Swim Boost
  (Alt.)"→"수영 강화 (대체)", "Spooked"→"겁먹음", "Slow"(면역)→"둔화", "PARRY WINDOW"→"패링 창",
  "Alt Fire"→"보조 발사"(모두 기존 선례). Star Trek·Dragon Ball·World of Warcraft 실존 프랜차이즈
  용어는 통용 한국어 표기 채택: "Romulans"→"로뮬런", "Vulcans"→"벌칸", "Surak"→"수라크","Romulan
  Star Empire"→"로뮬런 스타 제국", "Saiyans"→"사이어인", "SUPER SAIYAN"→"슈퍼 사이어인",
  "Tauren"→"타우렌", "Mulgore"→"멀고어", "Azeroth"→"아제로스". 신규 고유명사(선례 없음):
  "Rhaiod"(종교명)→"라이오드", "Remorian"→"레모리안", "Ryophi"→"리오피", "Sheye"→"셰이",
  "Skath"→"스카스", "Skiffian"→"스키피안", "Spectwing"→"스펙트윙", "Taur"(반인반마 종족,
  Tauren과 별개)→"타우르", "Khanate"→"칸국", "Scyphojel"→"스키포젤", "Silent Shadows"→"사일런트
  섀도우", "Sinking Sands"→"싱킹 샌즈", "Rhakori Highlands"→"라코리 고지대", "Solalei Guild of
  Exploration/SolaEx"→"솔라레이 탐사 길드/솔라엑스", "S50 'Hurricane'"→"S50 '허리케인'",
  "SN7P"→"SN7P"(모델 코드 유지), "Sjögren"→"쇠그렌", "Creaton"(텔레안 지도자)→"크레아톤",
  "Ecumenopolis"(행성 유형명)→"에큐메노폴리스". 독일어 억양 대사(id 103525, "vonderful",
  "kooperation", "kapital")는 v/k 자음 치환 패턴을 한국어 외래어 표기(분더바/코오퍼라치온/카피탈)로
  변환해 억양을 재현.
- 배치 0328(ID 103300~103511, 실존 총기 로어(이타카 모델 37/M1 개런드/MP-155/PP-19 비존/PAT
  Mk-1/L40·LB-40 기관단총) 다수, 젬하다르(스타트렉)/마오머·오르시머(엘더스크롤)/나메크인(드래곤볼
  패러디) 등 실존 프랜차이즈 종족 스탯 블록, 카즈드라/키츠네(3종 변형)/라미아/맨티드/리루/키아니/
  펭구킨/오멘/NostOS/노바키드(3종 변형) 등 오리지널 종족 스탯 블록 다수, 올드 원/코덴/바스 브할레이/
  라데이스/라이오드 관련 아비칸 기원 로어 3건, 폭스(중국 호선/여우 요괴 설화풍 고문체 로어) 3건,
  러스틀링(성인 콘텐츠 종족) 로어 3건, 요괴산 사자 대대 로어)는 구조 QA 이슈 없음, 용어 QA에서
  2종 발견되어 수정: (1) "Lustling"을 글로서리 고정 표기 "러스틀링" 대신 "러슬링"으로 옮긴 3건(id
  103346/103347/103349)을 정정. (2) "Alt Fire"(비대괄호 평문, `[ALT-FIRE]` 입력 토큰과는별개)를
  글로서리 고정 표기 "보조 발사" 대신 영문 그대로 둔 1건(id 103473)을 정정. 둘 다 `fix_0328.json`으로
  처리. 이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존 확립된 고정표기
  재사용: "Miniknog"→"미니크녹", "Poptop"→"팝톱", "M1 Garand"→"M1 개런드", "Browning"→"브라우닝",
  "Remington"→"레밍턴", "submachine gun"→"기관단총", "pump-action"→"펌프액션", "12 Gauge"→"12게이지",
  "bullpup"→"불펍", "youkai"→"요괴", "PARRY WINDOW"→"패링 창", "STABILITY"→"안정성", "Prime
  Circuit"→"프라임 서킷", "NivRAM"→"니브램", "Vas Vha'leih"→"바스 브할레이", "Khoden"→"코덴",
  "Rhadeis"→"라데이스", "Protectorate"→"보호국", "Apex"→"에이펙스", "Avian"→"아비안", "Wet"→"젖음",
  "Spooked"→"겁먹음", "Water Regen"→"물 재생", "Swim Boost (Alt.)"→"수영 강화 (대체)", "Underwater
  Breathing"→"수중 호흡", "Lush"→"울창함", "Jungle"→"정글", "Rainforest"→"열대우림", "Hot
  biomes"→"고온 생물군계", "Ocean"→"대양"(모두 기존 선례). Star Trek·Elder Scrolls·Dragon Ball 실존
  프랜차이즈 용어는 통용 한국어 표기 채택: "Jem'Hadar"→"젬하다르", "Founders"→"파운더스",
  "Dominion"→"도미니언", "Ketracel White"→"케트라셀 화이트", "Maormer"→"마오머", "Orsimer"→"오르시머",
  "Namekians"→"나메크인". 신규 고유명사(선례 없음): "Kazdra"→"카즈드라", "Kitsune"→"키츠네",
  "Kitsunebi"→"키츠네비", "Lamia"→"라미아", "Mantid"→"맨티드", "Lyru"→"리루", "Kyani"→"키아니",
  "Pengukin"→"펭구킨", "Omen"(종족명)→"오멘", "Phox"→"폭스"(중국 고전 호선/여우 요괴 설화 문체 유지,
  팽조/서시 등 실존 고사 인명은 한자 병기), "Old Ones"→"올드 원", "Uplifters"→"업리프터",
  "Centens"→"센텐스", "Ce'Tennan"→"세테난", "Rhaiod"(종교명)→"라이오드", "Nitori Industries
  Conglomerate"→"니토리 인더스트리 컨글로머릿", "K9 Kastle"→"K9 캐슬", "Nii'lah"→"니일라",
  "Felin"→"펠린", "Symbolspeak"→"심볼스피크", "Empire Engineering"/"Superior Engineering"(무기
  등급명)→"엠파이어 엔지니어링"/"슈페리어 엔지니어링", "K9 Kastle" 등은 모두 corpus grep확인 후
  직접 결정.
- 배치 0327(ID 103076~103299, Collatse 애퍼처/이그레스/웰 3단계 제작 기계 로어, 데넬라운/드로덴(3종
  변형)/던머/드웨머/팔머/페렝기/글리치/모비우스 헤지호그/인딕스 등 종족 스탯 블록 다수,아비칸
  역사·지리 로어(이스터샌드/웨스터샌드/플로잉 듄즈, 벨린 시대, 제1차 텔레안 침공, 그레이트
  웨이스트/발라키스), 그린핑거/플로란 사냥 연작 콘텐츠페이지 3건, 길텐 종교 로어, 히야즈츠(일본
  스피것 박격포) 실존 무기 로어, 오카서스 컬트 지구 멸망 로어, 디지털 레전더리 하빈저(비표준
  "Diet:/Bonuses:/Resistances:/Environment-/Combat Perks-" 라벨 스탯 블록))는 구조·용어 QA 모두
  첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정표기 재사용:
  "Highmind"→"하이마인드", "Kadavan"→"카다반"(아비칸 지리, 이전 배치 선례), "Letheia"→"레테이아",
  "Poptop" 계열 등 글로서리 고정 표기, "Tengu"→"텐구", "Kappa"→"캇파", "Suffocate Instantly"→"즉시
  질식"(모두 기존 선례). Elder Scrolls·Star Trek 실존 프랜차이즈 종족명은 통용 한국어 표기 채택:
  "Dwemer"→"드웨머", "Falmer"→"팔머", "Nords"→"노드", "Ferengi"→"페렝기". 신규 고유명사(선례
  없음, corpus grep 확인 후 직접 결정): "Kawaski"(하이로틀 난민 로어 속 NPC명)→"카와스키",
  "Vhelin"(아비칸 시대명, "Era of Vhelin")→"벨린", "Terves"(아비칸 용어)→"테르베스", "Exousia"(명사형,
  기존 형용사형 "Exousian"→"엑소시안"에서 역산)→"엑소시아", "Lathasia"(명사형, 기존 형용사형
  "Lathasian"→"라타시안"에서 역산)→"라타시아", "Notix"(페더레이션 대사 속 종족명)→"노틱스",
  "Occasus"("Occasus Cult", 실은 코퍼스에 기존 선례 "오카서스" 있었음 — 재확인 후 재사용)→"오카서스",
  "Delamaine"(사이버펑크 세계관 패러디)→"델러메인", "Errasmeyr"(정체불명 우주 종족)→"에라스메이르".
  Digital Legendary Harbinger(id 103135) 스탯 블록은 표준 두 템플릿과 다른 비표준 라벨 구조라 원문
  그대로 "식성:/보너스:/저항:/환경-/전투 특전-" 형태로 직역, 템플릿 강제 변환하지 않음.
- 배치 0326(ID 102860~103075, "The X are a..." 형식 종족 코덱스 대량 — 아키마리/알루네/알트머/
  아일레이드/보스머/침머/바조란/보그 등 TES·스타트렉 패러디 종족 스탯 블록 다수, 알타 6등급 제작
  시설 13종 장문 설명, 서킷/비컨/클랜가드 세력 대사, K'Rakoth 코덱스(에인션트/펜론) 로어)는 구조 QA
  이슈 없음, 용어 QA에서 2종 발견되어 수정: (1) "Crafting Station"을 글로서리 고정 표기 "제작대"
  대신 "제작 시설"로 옮긴 4건(id 102889/102892/102895/102897, 원문에 generic한 "crafting
  station"이 등장한 경우만 해당 — 고유 시설명 "Alta ~ Station"의 번역은 유지)을 정정. (2) "Infernus"
  를 글로서리 고정 표기 "인퍼너스" 대신 "인페르누스"로 옮긴 1건(id 102882, "Dark Infernus"
  생물군계명)을 정정. 둘 다 `fix_0326.json`으로 처리. 이후 베이스라인 4건(Miniknog/Trink/The
  Ruined/Kappa) 유지 확인. 기존 확립된 고정 표기 재사용: "Akkimari"→"아키마리", "the Circuit"→
  "서킷", "Matter Manipulator"→"물질 조작기", "Ceternity"→"세터니티", "Sona's Veil"→"소나의 베일",
  "Ava Day"→"아바 데이", "alterash/alterash prime"→"알테라시/알테라시 프라임", "K'Rakoth"→
  "K'Rakoth"(원문 유지), "Kluex"→"클루엑스", "the Ark"→"방주", "the Ruin"→"루인", "Terrene
  Protectorate"→"행성 보호국", "Nova Station" 등(모두 기존 선례). Elder Scrolls·Star Trek 패러디
  종족명은 각 프랜차이즈의 통용 한국어 표기를 채택: "Altmer"→"알트머", "Bosmer"→"보스머",
  "Chimer"→"침머", "Dunmer"→"던머", "Ayleids"→"아일레이드", "Bajorans"→"바조란", "Cardassian"→
  "카데시안", "Borg"→"보그". 신규 고유명사(선례 없음): "Nomada"(아비칸 대적 세력)→"노마다",
  "Theleans"→"텔레안", "Alrune"(악마형 종족)→"알루네", "Clanguard"(아비칸 치안 조직)→"클랜가드",
  "Fenrons"(K'Rakoth 코덱스 종족)→"펜론", "BigCoin"→"빅코인", "Avolite"(아비안 신성 수정)→
  "아볼라이트", "Argo"(함선명)→"아르고", "Ceterai Project"→"세테라이 프로젝트".
- 배치 0325(ID 102509~102859, "That's..." 대사 대량, 실존 총기 로어(AK/.300 블랙아웃/PP-19
  비존/3011 권총 등) 다수, 아에기니안 연방 연합/드레메톤/엘리시안 법전 세계관 로어, 아가란 종족
  로어, 타우모스 아이템군)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건
  Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 재사용: "Elithia"→"엘리시아",
  "Aegi"→"아에기"(둘 다 코퍼스 다수 선례로 확인), "Io"→"이오", "Phillippe VIII"→"필리프 8세",
  "Centensian"→"센텐시안", "Vas Vha'leih"→"바스 브할레이", "Starforge"→"스타포지", "Horizon"→
  "호라이즌", "koywa"→"코이와", "Matter Manipulator"→"물질 조작기"(모두 기존 선례). 신규
  고유명사(선례 없음): "Vha'leihan"(Vas Vha'leih의 형용사형)→"브할레이안", "Aeginian Federal
  Union"→"아에기니안 연방 연합", "Dremeton"→"드레메톤", "Elithian Code/Alliance"→"엘리시안
  법전/얼라이언스"(Elithia의 형용사형, 기존 -안 패턴 적용), "Union Colonies"→"유니언 식민지",
  "Aeon"→"에이언", "Timeless"(장소명)→"타임리스", "Greenfinger"(플로란 지도자 개념)→"그린핑거",
  "White Crow"→"화이트 크로우", "Guildmaster Ramses"→"길드마스터 람세스", "Nova Station"→"노바
  스테이션", "Plushbound"(스타바운드 패러디 모드명)→"플러시바운드".
- 배치 0324(ID 102317~102504, "Thank you (for)..." 퀘스트 완료 대사 대량, 라타시안 노예서사(id
  102486, 비속어 포함 원문 그대로 번역), K'Rakoth/기계 전쟁 로어, 크레딧 페이지)는 구조 QA 1건,
  용어 QA는 이슈 없음: id 102363 원문 태그 순서 `^green;...^orange;...^green;...^orange;...^reset;`
  (5개)를 번역에서 하나 더 넣어 6개로 만든 것을 `fix_0324.json`으로 정정. 이후 베이스라인 4건
  (Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존 확립된 고정 표기 재사용: "Vas Vha'leih"→
  "바스 브할레이", "Emerald Glimpse"→"에메랄드 글림프스", "Phillippe VIII"→"필리프 8세","the
  Circuit"→"서킷", "Sword Conjurer"→"검의 소환사", "Starfarer"→"스타파러", "Matter Manipulator"→
  "물질 조작기", "K'Rakoth"→"K'Rakoth"(원문 유지), "The Ruined"→"루인드", "IPN"(원문 그대로)(모두
  기존 선례). id 102486의 비속어("cunt" 등)는 노예제 학대 서사의 일부로 완곡화하지 않고그대로
  옮김("창녀" 등). 신규 고유명사(선례 없음): "Anakhar Systems"→"아나카 시스템즈", "Ouroboros
  Drill"→"우로보로스 드릴", "Renatine"(아르카니아 에너지 저장 물질)→"레나틴", "datamass"→
  "데이터매스", "Frogg Furnishing"(상점명)→"프로그 퍼니싱", "Rondin"(NPC명)→"론딘", "Lathasian"
  (노예제 서사 속 종족명)→"라타시안", "voe/la-voe"(라타시안 신조어 계급 멸칭)→"보에/라보에".
- 배치 0323(ID 102104~102316, 촉수(Tentacle) 컬트/Sexbound 테마 아이템·대사 대량(페네록스 번식
  대사 다수 포함), 테라킨 종족 스탯 블록, 테라마트/테슬라/테서랙트 아이템군, 행성 보호국
  산하 "Terrene Guardian/Peacekeeper" 칭호)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인
  4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 재사용: "Terrene Protectorate"→
  "행성 보호국"(글로서리 고정, 지난 배치 교훈 반영), "Peacekeeper"→"피스키퍼", "Terrakin"→"테라킨",
  "Devouts"→"디바우트", "Kluex"→"클루엑스"(모두 기존 선례). "Terrene Guardian"/"Terrene
  Peacekeeper"는 "Terrene Protectorate"의 형용사 용법과 동일한 논리로 "행성 수호자"/"행성
  피스키퍼"로 일관 적용. 신규 고유명사(선례 없음): "Busty"(촉수 컬트 보스명)→"버스티", "Testa
  Viola"(보스명)→"테스타 비올라", "Terramart"(상점 브랜드)→"테라마트", "vespoid"(벌 종족명, 힌트만
  등장)→"베스포이드".
- 배치 0322(ID 101856~102103, 텔레브리엄 무기 시리즈 대량, "Tell me..." 대사 대량, 촉수(Tentacle)
  컬트 테마 아이템 대량, 텐구 증원병 시리즈, 알타 강화제/코이와 사탕 로어)는 구조 QA 이슈 없음,
  용어 QA에서 1건 발견되어 수정: "Telebrium"을 글로서리 고정 표기 "텔레브리엄" 대신 "텔레브리움"으로
  옮긴 10건 전체를 `fix_0322.json`으로 정정. 이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa)
  유지 확인. 기존 확립된 고정 표기 재사용: "koywa"→"코이와", "Tengu"→"텐구", "Knightfall"→"나이트폴",
  "Cultist/Cult"→"컬티스트/컬트"(모두 기존 선례). 신규 고유명사(선례 없음): "Ronin"→"로닌",
  "Centensian"→"센텐시안", "Technocyte"→"테크노사이트", "Kel'chis"(akkimari 종족 신격)→"켈치스",
  "Project Redemption"→"프로젝트 리뎀션", "Jetfire"(제작자 크레딧)→"제트파이어".
- 배치 0321(ID 101656~101855, "Tall ___" 가구 시리즈 대량, "Target ___" 전투 로봇 대사 대량(끊기는
  무전 포함), 타르(Tar) 테마 아이템군, "Tastes like..." 음식 플레이버 텍스트 대량, 알타/하이로틀
  차 문화 로어)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건
  Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 재사용: "dirturchin"→"흙성게"(음역이
  아닌 기존 번역어), "Horizon"→"호라이즌", "Type:"→"유형:", "MOA"(군사 용어, 원문 그대로)(모두 기존
  선례). 신규 고유명사(선례 없음): "Talos"(엘더스크롤 패러디 신격)→"탈로스", "Eisenite"→
  "아이제나이트", "Kelbet"(생물명)→"켈벳", "Tarbound"(스타바운드 패러디)→"타바운드", "50Shades of
  Green"(그레이의 50가지 그림자 패러디)→"그린의 50가지 그림자".
- 배치 0320(ID 101453~101655, T로 시작하는 실존/패러디 총기명 대량, 전부대문자(ALL CAPS)로그·방송
  텍스트 다수, "Talk to X to Y" 퀘스트 이동 안내 대량, 탈리미만 늑대인간 종족 스탯 블록,배드랜즈
  스캐빈저 로어)는 구조 QA 1건, 용어 QA는 이슈 없음: id 101642 원문이 "^orange;Gatekeeper"로 닫는
  reset 태그 없이 끝나는데 번역에 reset을 추가해 발생한 태그 불일치를 `fix_0320.json`으로 정정.
  이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존 확립된 고정 표기재사용:
  "General Falke"→"팔케 장군", "Horizon"→"호라이즌", "Talimiman"→"탈리미만", "Scavenger"(코덱스
  종족명)→"스캐빈저", "숨 소모 속도"·"배고픔 속도"(종족 스탯 라벨)(모두 기존 선례). 신규고유명사
  (선례 없음, 대부분 짧은 NPC/장소명 그대로 음역): "Badlands"→"배드랜즈", "Thell"(아비칸대적
  종족명)→"델", 그 외 "Talk to X to Y" 퀘스트 라인의 각 NPC/장소명(아유린, 카민, 차차라,아카기
  박사, 네레우스 박사, 플린트, 로드스타 사원, 모르페우스, 랜디, 로칸 등) 다수.
- 배치 0319(ID 101232~101452, 여우/뱀(라미아)/심비오트 종족 스탯 블록 대량, 디저트·음식플레이버
  텍스트 대량, "Suspect...!"(끊기는 무전) 대사, Syntek/스위퍼 탄창 무기 시리즈)는 구조 QA 이슈 없음,
  용어 QA에서 1건 발견되어 수정: id 101235 "Terrene Protectorate"를 글로서리 고정 표기(바닐라 번역
  우선) "행성 보호국" 대신 "테렌 보호국"으로 음역해 옮긴 것을 `fix_0319.json`으로 정정.이후
  베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존 확립된 고정 표기 재사용:
  "Root Pop"→"루트 팝", "poisoncreep"→"독크리프", "piru"→"피루", "Saturnian"→"새터니안","치명타
  확률", "Extractable"→"추출 가능", "Crushable"→"분쇄 가능", "Type:"→"유형:"(모두 기존 선례).
  신규 고유명사(선례 없음): "Strelitzia"(플로란 NPC명)→"스트렐리치아", "Heart of Ruin"(보스명)→
  "루인의 심장", "Ceternity"(알타 축제 관련 인물명)→"세터니티", "Lamia's Aim"(뱀 종족 전용
  스킬명)→"라미아의 조준", "Rad-Burn"(상태이상)→"방사능 화상", "Sword of Omens"(선더캣츠
  패러디)→"오멘스의 검", "Sylveon"(포켓몬)→"님피아"(공식 한국어명, 확인 근거 있음), "Syntek"(무기
  브랜드명)→"신텍", "Switz"(전 배치의 "Sweets" 국가명 변형 표기로 추정)→"스위츠"(선례 유지).
- 배치 0318(ID 100998~101231, 소환 스킬 설명 대량, 디지털 존재 종족 스탯 블록, "Sup(erior)..." 무기
  플레이버 텍스트 대량, "Surprised." 대사 대량, 펭귄 종족 기원 로어, 시아사/이몰레이터 아비안·
  피스키퍼 로어)는 구조 QA 2건, 용어 QA 2종 발견되어 각각 수정: (1) id 101196 원문 태그순서
  `^green;...^orange;...^reset; ^green;...^reset;`(5개)를 번역에서 하나 누락시켜 4개로 옮긴 것을
  `fix_0318.json`으로 정정. (2) 용어 "Violium"은 글로서리 고정 표기가 "바이올륨"인데 "바이올리움"으로,
  "Thaumoth"는 고정 표기가 "타우모스"인데 "사우모스"로 옮긴 것을 각각 `fix2_0318.json`으로 정정.
  이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존 확립된 고정 표기재사용:
  "Trink/Trinkian"→"트링크/트링키안", "Matter Manipulator"→"물질 조작기", "Kluex"→"클루엑스",
  "K'Rakoth"→"K'Rakoth"(원문 유지), "neonmelon"→"네온멜론", "Type:"→"유형:", "Protectorate"→
  "보호국", "Peacekeeper"→"피스키퍼"(모두 기존 선례). 신규 고유명사(선례 없음): "Earthcorp"→
  "어스코프", "Nocturnian"(종족명)→"녹터니안", "Kavanite"→"카바나이트", "Siaxaa"(아비안신격)→
  "시아사", "Immolator"(피스키퍼 암호명)→"이몰레이터", "MISSCHANCE"(게임 내 스탯명, 원문그대로
  유지), "nakati"(아발리 향신료)→"나카티", "Shivery"(상태이상)→"오한".
- 배치 0317(ID 100760~100997, 파충류/개미귀신 채굴 전사 종족 스탯 블록, "Subject N:" 실험체 로그
  시리즈, 황산(Sulphuric) 계열 지명, 여름(Summer) 가구 시리즈 대량, 함선 소환 아이템(Blink
  Keff/Drehk/갈리엇 등) 대량, 운문+암호문 콘텐츠페이지)는 구조 QA 이슈 없음, 용어 QA에서1건 발견되어
  수정: id 100873/100874 "Penguin Bay"를 글로서리 고정 표기 "펭귄 베이" 대신 "펭귄 만"으로 옮겨
  `fix_0317.json`으로 정정. 이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존
  확립된 고정 표기 재사용: "Trink/Trinkian"→"트링크/트링키안", "Execration"(전 배치 참조)→
  "이그제크레이션", "Galliot"→"갈리엇", "Quicksand"→"유사", "Jungle Dirt"→"정글 흙", "황산"(Sulphuric
  계열 지명, "황산성"이 아님), "Kluex"→"클루엑스", "Luye/Lvye"→"루예"(모두 기존 선례). 운문(id
  100893)은 색상 태그(^red;/^blue;)와 "Shhh" 반복 횟수(3~6회)를 원문과 동일하게 유지했고, 마지막
  줄의 기호 암호문(색칠된 글자로 "d o y o u ?" 스펠링)은 번역하지 않고 원문 그대로 보존.WebSearch로
  실제 게임 레퍼런스 확인: "Shy Guy"(마리오 시리즈)→"헤이호"(한국 공식 로컬라이제이션 통용 표기).
  신규 고유명사(선례 없음): "Ironwatch"(조직명)→"아이언워치", "Horizon"(조직명)→"호라이즌",
  "General Falke"→"팔케 장군", "Esoquartz"→"에소쿼츠", "Wood Herself"(플로란 신격 존재)→"숲 그
  자체", "Companion Punchy"/"Comfort Chamber"(포탈 패러디)→"컴패니언 펀치"/"컴포트 챔버",
  "CentComm"→"센트컴", "Fleshlight"(성인용품 브랜드)→"플레시라이트"(조명 기구 flashlight의
  "플래시라이트"와 구분).
- 배치 0316(ID 100568~100759, 래디온(rad'ion)/웨버(Webbers) 종족 스탯 블록, "Stranger. X. Discourse?"
  형식 종족 조우 대사, 줄무늬(Striped)/스튜디오(Studio) 가구 시리즈 대량, 스트롱홀드/스트라이커
  X-0N 무기 시리즈, 기절(Stun) 계열 아이템)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인
  4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 재사용: "Trink"→"트링크",
  "Trinkian"→"트링키안"(코퍼스 다수 표기, 글로서리와 별도), "U.S.C.M."→"U.S.C.M.", "Webs"(면역
  상태)→"거미줄", "Electric Immunity"→"전기 면역", "Impulse Immunity"→"충격 면역", "Aya"→"아야",
  "Gysahl"→"기살"(모두 기존 선례). 원문 자체의 태그 누락(예: "^red;Weaknesses:"에 닫는 reset 태그가
  없음, "Strategic Reminder:" 줄 끝에 reset 미포함)은 구조 QA를 통과하도록 원문 그대로 재현. 신규
  고유명사(선례 없음): "rad'ion"(종족명)→"래디온", "Webbers"(종족명)→"웨버", "Xeno"(에일리언
  패러디)→"제노", "BFG-9000"(둠 패러디, 원문 그대로), "Devouts"(적대 세력명)→"디바우트",
  "Darkdweller"(nightar 종족 별칭)→"어둠거주자", "Stronghold"→"스트롱홀드", "Stryker"→"스트라이커",
  "Magicite"→"매지사이트", "Cpt. Litznitsky"→"리츠니츠키 대위".
- 배치 0315(ID 100376~100567, 엘두우카르/스트라시란/우주 해파리/마법 구조물 종족 스탯 블록 대량,
  "Strange being/creature/person." 형식 종족 조우 대사 대량, 저장 브릿지(ITN) 로어, GIC_Otherworlds
  라이온/크라운 연방/텐구/요괴 세계관 대사)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인
  4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 다수 재사용: "tengu"→"텐구",
  "youkai/youkies"→"요괴", "Beacon"→"비컨", "Lion Empire"→"라이온 제국", "Crown Federation"→
  "크라운 연방", "Stingwing"→"스팅윙", "Embrittle"→"취화", "Storage Bridge"→"저장 브릿지",
  "Saturnian"→"새터니안", "Crushable"→"분쇄 가능", "Extractable"→"추출 가능", "Shadow"(저항
  속성)→"그림자", "Radioactive"→"방사능", "Lunari"→"루나리", "Aether Sea"→"에테르 바다",
  "Chromatic"→"크로매틱", "넉백 저항"·"거미줄"·"검은 타르"(면역 상태) (모두 기존 선례).신규
  고유명사(선례 없음): "Agaran"(종족명)→"아가란", "yaara groves"→"야라 숲", "yonnur"→"요누르",
  "Gray Knight"→"그레이 나이트", "Ironsides"→"아이언사이드", "Gray Radiance"→"그레이 라디언스",
  "Emerald Glimpse"→"에메랄드 글림프스", "Elduukhar"(종족명)→"엘두우카르", "Talimiman"(상위
  분류명)→"탈리미만", "Straciran"(종족명)→"스트라시란", "the Circuit"(전 배치 참조)→"서킷" 계열
  유지, "Stor Blåhaj/Klappar Haj/Rosahaj"(이케아 상어 인형 패러디)→"스토르 블로하이/클라파르
  하이/로사하이".
- 배치 0314(ID 100134~100375, "Statement." 로봇/드론풍 대사 대량, "Stay ___" 경고·대사 대량, 강철
  (Steel)/스틸블레이드(Steelblades) 가구·건축 시리즈 대량, 디벨라·라데이스 조각상, 사이스태프
  (scistaves) 마법 지팡이 로어)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건
  Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 다수 재사용: "Kluex"→"클루엑스",
  "Rhadeis"→"라데이스", "Grenade Launcher"→"유탄 발사기", "Broadsword"→"브로드소드", "Steyr"→
  "슈타이어", "Extractable"→"추출 가능", "Type:"→"유형:", "Shadow"(종족명)→"섀도우"(모두기존
  선례). "별빛"(Starry) 접두 가구 라인 명명 규칙을 이번 배치의 "Starry Cultist"·"Starry planets"
  대사에도 일관 적용. 네키 특유의 "-냥/-옹" 말투, 플로란 특유의 "-엇" 말투를 각 종족 힌트에 맞춰
  선택적으로 적용. 신규 고유명사(선례 없음): "Enerth Engineering"→"에너스 엔지니어링", "Dibella"
  (엘더스크롤 여신 패러디)→"디벨라", "Sword Conjurer"→"검의 소환사", "scistaves"→"사이스태프",
  "the Circuit"(조직명)→"서킷", "solusberry"→"솔루스베리", "Lastree 종족이 천사에게 오인받는
  'Demon'"→"데몬"(음역, 일반명사 악마와 구분), "Steelblades"→"스틸블레이드".
- 배치 0313(ID 99934~100133, "Star"/"Starry" 테마 가구 시리즈 대량, 스타더스트 아이템군,플로란에게
  감염된 버섯 포로의 스타데이트 일지 시리즈(99969~99973, 점진적 언어 붕괴 연출), 네뷸락관련 대사,
  스타스트라이더/스테이시스 키퍼 아이템군)는 구조 QA 1건, 용어 QA는 이슈 없음: id 100093에서 원문은
  `^green;...^orange;...^reset;`처럼 reset 태그가 한 번만 닫히는데 번역에 reset을 두 번넣어
  발생한 태그 개수 불일치를 `fix_0313.json`으로 정정. 이후 베이스라인 4건(Miniknog/Trink/The
  Ruined/Kappa) 유지 확인. 기존 확립된 고정 표기 재사용: "Starbound"→"스타바운드", "Nebulac"→
  "네뷸락", "Herbivore"(Type)→"초식", "픽셀"(화폐)→"픽셀", "Alliance"→"얼라이언스", "Starklance"→
  "스타크랜스", "Shortsword"→"소검", "Poptop"→"팝톱"(글로서리 고정, 전 배치에서 확정)(모두 기존
  선례). "Star ___"(별 ___)와 "Starry ___"(별빛 ___) 두 개의 별도 가구 아이템 라인을 구분해
  일관되게 번역. 신규 고유명사(선례 없음): "Nebulathite"→"네뷸라타이트", "Crippit"→"크리핏",
  "Narfin"→"나르핀", "Stasis Keeper"→"스테이시스 키퍼", "Starstrider"→"스타스트라이더", "neonmelon"
  →"네온멜론", "Stargazy pie"(실존 영국 요리명)→"스타가지 파이", "Luye"→"루예", "Starfarer"→
  "스타파러". 스타데이트 일지 시리즈는 화자가 못된 버섯에 감염되어 플로란어투("-엇")로 점차
  붕괴하다 최종화에서 "키스페이스"/"메스티" 같은 완전한 의미불명 음절로 무너지는 연출을그대로
  재현.
- 배치 0312(ID 99760~99932, 슈탈라이트/슈탈레른 건축 자재 시리즈, 스탠다드/스타 가구 시리즈 대량,
  미니크녹 에이펙스 무기 플랫폼 로어, U.S.C.M./UAC/나이트폴 군용 장비, friendlyname 힌트의 포즈
  라벨 대량)는 구조 QA 이슈 없음, 용어 QA에서 3건 발견되어 수정: (1) id 99850 "Magishot"을
  글로서리 고정 표기 "매지샷" 대신 "매직샷"으로 옮김. (2) id 99861 "Rocket Launcher"를 고정 표기
  "로켓 발사기"(공백 포함) 대신 "로켓발사기"(공백 없음)로 옮김. (3) id 99893 "Poptop"을글로서리
  고정 표기 "팝톱" 대신 코퍼스 다수파 표기인 "팝탑"으로 옮김 — 글로서리가 기존 다수 표기를
  의도적으로 교정하려는 규칙이므로 다수파를 따르지 않고 고정 표기를 채택. 모두 `fix_0312.json`으로
  정정 후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존 확립된 고정 표기 재사용:
  "Miniknog"→"미니크녹"(글로서리 고정, 코퍼스 다수 표기이기도 함), "Extractable"→"추출 가능"(채굴
  가능 아님), "Apex"→"에이펙스", "U.S.C.M."→"U.S.C.M."(원문 그대로), "Aurea Collective"→"아우레아
  컬렉티브", "Shortsword"→"소검", "Broadsword"→"브로드소드", "별"(stars 화폐)→"^yellow;별^reset;",
  "Milky Way Shakes"→"밀키웨이 셰이크", "Armory"→"병기고", "Star Dust"→"별가루"(모두 기존 선례).
  "Standard -" 주문 등급 접두사는 기존 "혼돈 -"/"그레이터 -" 표기 선례에 맞춰 "기본 -"으로 번역.
  신규 고유명사(선례 없음): "Trianglium"→"트라이앵글리움", "Koshka"→"코시카", "Knightfall"→
  "나이트폴", "Stahlite"→"슈탈라이트", "Stahlern"→"슈탈레른", "Stahl-Verro"→"슈탈베로",
  "Risen"(NPC 이름)→"라이즌", "St?rbucks"(스타벅스 패러디, 원문 그대로 유지), "Popball"→"팝볼".
- 배치 0311(ID 99258~99752, 아몰리안/정령/글루트 종족 스탯 블록 대량, Pokéball 아이템(얼루기·나오하
  확인), 봄/할로윈 시즌 가구 아이템군, 플로란 특유의 "Sss-" 쉿 소리 대사 대량(39건))는 구조 QA
  이슈 없음, 용어 QA에서 1건 발견되어 수정: id 99295 "Splendid Shortsword"의 "Shortsword"를
  글로서리 고정 표기 "소검"(Dagger의 단검과 구분) 대신 "숏소드"로 옮겨 `fix_0311.json`으로 정정.
  이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 플로란 "Sss-" 대사는 기존 선례
  검색으로 확립된 관례(음소 자체를 옮기지 않고 어미 "-엇"/모음 늘이기/조사 생략/3인칭 "플로란"
  자칭으로 쉿 소리 느낌을 구현, `translations/rest_1401_1750.tsv` 등 다수 확인)를 그대로적용.
  기존 확립된 고정 표기 재사용: "Halloween"→"할로윈", "Dotefruit"→"도트프루트", "Item-Network
  compatible."→"아이템 네트워크 호환.", "Gosmet"→"고스멧", "Wisper"→"위스퍼", "Spookit"→"스푸킷",
  "Gysahl"(간접)·"Letheia"→"레테이아", "Type:"→"유형:"(모두 기존 선례). WebSearch로 포켓몬 공식
  한국어명 확인: "Spinda"→"얼루기"(전국도감 327번), "Sprigatito"→"나오하". 신규 고유명사·표현(선례
  없음): "Armolian"(종족명)→"아몰리안", "fuck-meat"(플로란이 상대를 부르는 성적 멸칭)→"떡고기",
  "Gklthl"(발음 불가 설정의 행성명, 농담 유지 위해 원문 그대로 미음역), "bloob"→"블루브",
  "Cosmic"(저항 속성)→"코스믹", "Charisma"(스탯)→"매력", "Spiritwood"→"스피릿우드".
- 배치 0310(ID 99022~99257, "Sparkly Star" 아이템군, RPG_contents 모드의 전문화(Specialization)/
  칩/포핍(poptop)·위스퍼(wisper)·오르바이드(orbide) 몬스터 특수 능력 대사, 코덱스 "Species
  001~022" 종족 설명 대량, K'Rakoth 로어, addtotooltip UI 라벨 대량)는 QA 이슈 없이 구조·용어 모두
  첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정표기 다수
  재사용: "Hylotl"→"하이로틀", "Felin"→"펠린", "Novakid"→"노바키드", "lustling"→"러스틀링",
  "Shoggoth"→"쇼고스", "Kappa"→"캇파"(글로서리 고정), "youkai"→"요괴", "Unitan"→"유니탄", "Ava
  Day"→"아바 데이", "Woodland"→"우드랜드", "Gysahl"→"기살", "Bolbohn"→"볼본", "kiri"→"키리",
  "A.V.I.A.N."→"A.V.I.A.N."(원문 그대로), "phosicore"→"포시코어", "Ancients"→"에인션트",
  "Mechanist"→"메카니스트", "Sage"→"세이지", "Paladin"→"팔라딘", "Titan"→"타이탄",
  "Conquistador"→"콘키스타도르", "Turret"→"터렛", "Specialization"→"전문화", "Hunting weapon"→
  "사냥 무기"(사냥용 무기 아님), "Type:"→"유형:", "Input:"→"입력:", "On/Off Switch"→"켜기/끄기
  스위치", "Prestige"→"프레스티지"(모두 기존 선례, `translations/*.tsv` 및 특히
  `rest_priority_0241.tsv`의 RPG_contents 패치노트 전수 검색으로 확인). 신규 고유명사·표현(선례
  없음): "Gestalt"(종족명)→"게스탈트", "the Crystals"(종족명)→"크리스탈", "the Worms"(종족명)→
  "웜", "the Scavengers"(종족명)→"스캐빈저", "the Automata"(종족명)→"오토마타", "the
  Ferals"(종족명)→"페럴", "Lithia"→"리시아", "Kohria"→"코흐리아"(실존 국가명 "Korea"와 음역 충돌
  피하기 위해 "코리아" 대신 채택), "Captain"(전문화명)→"캡틴", "Exousian"→"엑소시안",
  "Kosmoflot"→"코스모플로트", "Vikhr"→"비흐르", "Shining Sea"→"샤이닝 해", "Arcanian"→"아르카니아",
  "Execration"→"이그제크레이션", "Starforge"→"스타포지", "woofie"(Woof 종족 애칭형)→"우피",
  "Demon"→"악마"(음역하지 않고 번역), "Soulsea"(이전 배치 참조)→"소울시" 계열 유지.
- 배치 0309(ID 98817~99021, "Sorry..." 대사 대량, "Space is..." 류 우주에 대한 잡담 대사대량, 소나/
  소나베일(Sonaveil, 알타 겨울 축제) 아이템군, K'Rakoth 로어, Space Dragons·Space Wolves종 스탯
  블록)는 구조 QA에서 1건, 용어 QA에서 2종 신규 위반이 발견되어 각각 수정: (1) id 98983 "Space
  Wolves." 원문은 제목과 스탯 블록 사이에 빈 줄이 없는데(대조군인 id 98963 "Space Dragons!"는 빈
  줄이 있음) 번역에 불필요한 빈 줄을 넣어 줄 수가 15→16으로 불일치, `fix_0309.json`으로수정. (2)
  용어 "Hylotl"은 글로서리 고정 표기가 "하이로틀"인데 관성적으로 "힐로틀"(코퍼스에 흔한구어체 표기)
  로 옮긴 id 98824/98880/98885 3건을 `fix2_0309.json`으로 정정. (3) 용어 "Broadsword"는글로서리
  고정 표기가 "브로드소드"(대검·장검과 혼용 금지)인데 id 98963 스탯 블록에서 "대검"으로옮겨
  `fix3_0309.json`으로 정정. 이후 베이스라인 4건(Miniknog/Trink/The Ruined/Kappa) 유지 확인. 기존
  확립된 고정 표기 재사용: "Protectorate"→"보호국", "Alliance"→"얼라이언스", "The Ruined"→"루인드",
  "the Ruin"→"루인", "Peacekeeper"→"피스키퍼", "Enhanced Battery"→"강화 배터리", "Corporation"→
  "코퍼레이션", "spacedrifter"→"스페이스드리프터", "Harpy Disease"→"하피병", "Aurea"→"아우레아",
  "Mycotoxin"→"마이코톡신", "bion"→"바이온", "Type:"→"유형:"(모두 기존 선례). 신규 고유명사(선례
  없음): "Sonaveil"(알타 겨울 축제명, Sona's Veil의 축약형)→"소나베일", "Peglaci"(적대 세력명)→
  "페글라시", "Soulsea"(아이템 브랜드명)→"소울시", "Syllectis"(우주 열차 이름)→"실렉티스",
  "virma"(가상의 요리 재료)→"비르마".
- 배치 0308(ID 98460~98816, "Some sort of...", "Somebody...", "Someone...", "Something...",
  "Sometimes..."로 시작하는 아이템 설명·대사 대량, 테라킨(Terrakin) 종족 설명 및 스탯 블록, 바스
  브할레이/아비카 산맥/코덴/다스의 자리/라데이스 관련 아비칸 기원 로어, 에르키우스·루나인류사 로어,
  스타포드·폐허가 된 성 로어)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건
  Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 다수 재사용: "Vas Vha'leih"→
  "바스 브할레이", "Khoden"→"코덴", "Avikha"→"아비카", "Ultarubim"→"울타루빔", "Erchius"→"에르키우스",
  "Irken"→"이르켄", "Starklance"→"스타크랜스", "Unustrello"→"우누스트렐로", "alterash prime"→
  "알테라시 프라임"(모두 기존 선례, `translations/*.tsv` 전수 검색으로 확인). 신규 고유명사·표현(선례
  없음): "Terrakin"(종족명)→"테라킨", "Seat of Dhas"→"다스의 자리", "Tempering Anvil"→"담금질 모루",
  "poignac"(가상의 술)→"포이냑", "cuvia/cuva"(가상의 재료)→"쿠비아/쿠바". 테라킨 스탯 블록은 기존
  Attributes/Resistances/Immunities/Racial Traits 템플릿의 확립된 한국어 필드명(능력치/저항/면역/종족
  특성 등)을 그대로 재사용.
- 배치 0307(솔라(Solar)/솔라리움(Solarium) 무기·장비 시리즈 대량, 러스틀링/러스티아 로어, 트로페스
  (리샨 모방자) 로어, "Some..."으로 시작하는 아이템 설명·대사 대량)는 QA 이슈 없이 구조·용어 모두
  첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된 고정표기 다수
  재사용: "Solarium"→"솔라리움", "Woof"(종족명)→"우프", "Lustia"→"러스티아", "Matter Manipulator"→
  "물질 조작기", "impervium"→"임퍼비움", "Reclaimer Arms"→"리클레이머 암즈", "Second Contact War"→
  "제2차 접촉 전쟁", "Distortion Sphere"→"왜곡 구체", "Dreadwing"→"드레드윙", "enternia"→"엔터니아",
  "tsay"→"차이", "Growing One"(리샨의 별칭)→"자라나는 리샨"(모두 기존 선례). "Aurea Collection"은
  기존 "Aurea Collective"(아우레아 컬렉티브)와 영문 표기가 달라 별개 표기로 판단해 "아우레아
  컬렉션"으로 옮기고 혼동하지 않았다. 신규 고유명사(음차, 선례 없음): Tro'phess→트로페스, Wisper→
  위스퍼, cystume(가상 음식명)→시스튬, ciranga(가상 과일 풍미)→시랑가.
- 배치 0306("So..."로 시작하는 NPC 대사 대량(모미지/다이텐구/백랑 중대/아야 등장), 아우레아/
  우르사/프로텍터 인트로 대사, 토양 종류 로어, 솔(Sol) 계열 아이템, 부드러움(Soft) 계열식음료·
  자재 다수)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The
  Ruined/Kappa 유지). 기존 확립된 고정 표기 다수 재사용: "Momiji"→"모미지", "daitengu"→"다이텐구",
  "White Wolf (Company)"→"백랑(중대)", "Aya"→"아야", "prisilite"→"프리실라이트", "Dustrium"→
  "더스트리움", "TTPP (Land)"→"TTPP (랜드)", "Pengukin"→"펭구킨", "Parasprite"→"패러스프라이트",
  "lucario"→"루카리오", "ambrum"→"암브럼", "Nomada"→"노마다", "Aurea"→"아우레아", "Ursa"→"우르사",
  "K'Rakoth"→"크라코스"(모두 기존 선례). 신규 고유명사(음차, 선례 없음): Precursor(종족명)→
  프리커서, Sol'thass→솔타스.
- 배치 0305(매끄러운(Smooth) 건축 자재 마무리, 눈(Snow) 계열 아이템·크리터 대량, 칼리스탄 사촌
  종족·눈표범·스너겟 능력치 블록 3건, 빈더밀/글림레쿠스 탑/옴니버설 아케인 코버넌트 로어, "So..."로
  시작하는 대사 다수(리프트다이버 메크, 테라포밍 기계/자라나는 리샨 로어 등))는 QA 이슈없이
  구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). 포켓몬
  "Snivy"→"주리비얀"은 웹 검색으로 공식 한국어 명칭을 재확인. 칼리스탄 사촌 종족 능력치블록은
  같은 계열 기존 번역(id 58597, "사막 거주 종족")의 표기(속성/공격력 배율/호흡 소모 속도등)를
  그대로 재사용해 내부 일관성을 확보했다. 기존 확립된 고정 표기 다수 재사용: "Vindermill"→
  "빈더밀", "Omniversal Arcane Covenant"→"옴니버설 아케인 코버넌트", "Growing One"(리샨의 별칭)→
  "자라나는 리샨", "Akaggy"→"아카기", "Cassidy"→"캐시디", "Seeker of Dust"→"먼지 탐구자",
  "Callistan"→"칼리스탄", "Riftdiver"→"리프트다이버", "Glimmlecus"→"글림레쿠스", "High Magus"→
  "하이 마구스", "Fleshlight"→"플레시라이트"(모두 기존 선례).
- 배치 0304("Small X" 소형 장식·가구·배너 아이템 마무리(네크로이움/오카서스/펄레스/타이탄코프/
  스카이오크 등), 스마트(Smart)/스마트링크 총기·탄약 시리즈, 냄새(Smells like) 대사 다수, 매끄러운
  (Smooth) 건축 자재 시리즈)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건Miniknog/
  Trink/The Ruined/Kappa 유지). 기존 확립된 고정 표기 다수 재사용: "Necroium"→"네크로이움",
  "Occasus"→"오카서스", "Pearlles"→"펄레스", "Titancorp"→"타이탄코프", "Skyoak"→"스카이오크",
  "Enartz"→"에나츠", "lustling"→"러스틀링", "Ammunation"(오타)→"탄약"(정상 번역), "RelicSeeker"→
  "유물 탐구자", "Woodlands"/"Restored"/"Palace"(가구 브랜드)는 기존 확립 표기 그대로 재사용.
  "Johnny Silverhand"(사이버펑크 2077)는 원어 그대로 "조니 실버핸드" 음차.
- 배치 0303(경사형(Sloped) 건축 자재 다수, 나태한 종족 능력치 블록 1건, 슬러그(Slug) 계열 아이템,
  "Small X" 소형 장식·가구·배너 아이템 대량 — 아크리스/얼라이언스/천사/아비칸/펠린/레테이아/
  나이트폴/레이크록 등 다수 세력 소형 배너·가구 세트)는 QA 이슈 없이 구조·용어 모두 첫 시도에
  통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). "유탄 발사기"는 배치 0302에서 정정한
  띄어쓰기 고정 표기를 이번에도 정확히 적용했다. 기존 확립된 고정 표기 다수 재사용: "Whitewood"→
  "화이트우드", "Sloped"→"경사형"(id 48358 선례 우선 채택), "Akris"→"아크리스", "Aetheryte"→
  "에테라이트", "Lamia"→"라미아", "Letheia"→"레테이아", "Knightfall"→"나이트폴", "Lakerock"→
  "레이크록", "Hyverium"→"하이베리움", "Deadbeat"→"데드비트", "Eisenite"→"아이제나이트",
  "Galvanic"→"갈바닉", "Elysia"→"엘리시아", "Eorzian"→"에오르지안", "Legion"→"리전", "Horizon"→
  "호라이즌", "Gilten"→"길텐", "Fenerox"→"페네록스"(모두 기존 선례). "Frogg"는 다수결 표기
  "프로그"(가구 브랜드 "프뢰그"와는 구분)를 채택. 신규 고유명사(음차, 선례 없음): Jinye→진예,
  Helyn(구역명)→헬린.
- 배치 0302(매끈한(Sleek) 가구 시리즈 34종, 스카이레일(Skyrail) 부품 시리즈, 점판암(Slate) 가구,
  슬라임(Slime) 무기·장비 시리즈, 스킬 패치노트 1건)에서 `qa_glossary.py` 고정 용어 위반1건 발생 —
  id 97343 "Grenade Launcher"를 붙여쓴 "유탄발사기"로 옮겼다가(→글로서리 고정 "유탄 발사기", 띄어
  쓰기 포함) `fix_0302.json`으로 정정, 이후 기존 4건 베이스라인으로 복귀. 구조 오류는 없었음.
  가구 어휘는 기존 "Hot Rose"/"CT-EXE"/"Artdeco"/"Autumn"/"Gothloli" 등 병렬 세트 선례(Aquarium→
  어항, Baluster→난간동자, Drape→커튼, Light Fixture→조명 기구, Tall Dresser→키 큰 서랍장, Towel→
  수건, Trash Bin→쓰레기통, Wall Fireplace→벽난로, Wall Garden→벽면 정원)를 그대로 재사용하고
  "Sleek"는 브랜드명이 아닌 일반 형용사로 판단해 "매끈한"으로 의역했다. "Slate"→"점판암"(id 29924
  등 선례), "mellowroot"→"멜로루트", "violiroot"→"바이올리루트"(신규 음차), "K'Rakothan"(형용사형)
  →"크라코스식"으로 기존 "크라코스" 표기에 맞춰 옮겼다.
- 배치 0301(알타 "언니"(Sis) 호칭 대사 약 50건, 시뮬라크럼 그룹 로그 4건, 사이펀(Siphon)강화
  설명 다수, 크라운 연방/제국 총기 로어, 은(Silver) 계열 아이템)에서 `qa_structure.py` lines 오류
  1건과 `qa_glossary.py` 고정 용어 위반 1건 발생 — id 96974는 원문에 개행이 없는데 번역에 개행을
  넣어 정정, id 96961의 "Parry Window"를 "패링 윈도우"로 옮겼다가(→글로서리 고정 "패링 창", "시간
  구간을 뜻하는 window" 주석 확인) 정정, 이후 기존 4건 베이스라인으로 복귀. "Sis"는 기존확립된
  "언니"(id 20843 등 선례)를 전체 배치에 일관 적용. "alternia"→"알터니아", "yaara"→"야라", "Blue
  Boil"→"파란 종기", "Party Fresh"→"파티 프레시", "arknights"→"아크나이트", "nami drei"→"나미
  드라이", "Al'deron"→"알데론", "Enterash"→"엔테라시", "Astera(Industries/Ordis)"→"아스테라(
  인더스트리/오르디스)", "Ghearun"→"게아룬", "Tserera"→"체레라", "Neiteru"→"네이테루", "K'Rakoth"→
  "크라코스", "Peacekeeper"→"피스키퍼", "Crown Federation"→"크라운 연방" 모두 기존 선례재사용.
  "Razor"(스킬명)는 기존 코퍼스 다수 선례(id 20375/53091/57274 등, "레이저"로 음차하는 관행)를
  그대로 따랐다.
- 배치 0300(글리치/크라코스/누올리스 반란 로어, 셰이드(Shade) 클래스 설명, 미니크녹/빅코인
  음모론 로어, 쇼와(Showa) 총기 탄약 시리즈, 실크(Silk) 계열 도구 다수, "Should"로 시작하는 대사
  다수)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/
  Kappa 유지). 기존 확립된 고정 표기를 다수 재사용: "Shoggoth"→"쇼고스", "K'Rakoth"→"크라코스",
  "Noolith"→"누올리스", "BigCoin"→"빅코인", "Ouroboros Industrial Cartel"→"우로보로스 산업
  카르텔", "Skimbus"→"스킴버스", "Ariostone"→"아리오스톤", "Agaranic"→"아가라닉", "Keysprout"→
  "키스프라우트", "Shivery"→"오한", "starfruit"→"스타프루트", "Stargazers"→"스타게이저"(모두 기존
  선례). 배치 0001~0300 누적으로 high-priority 큐가 최초 대비 절반 이하로 줄었다.
- 배치 0299(에고엔/마르페시아/선하 장문 로어 다수, 셸가드(Shellguard) 세력 아이템·대사,시즈호·
  매그넘 존슨 성인 대화 4건, 쇼크&아크 친화력(Affinity) 강화 설명 다수, 섹스본드 성인 콘텐츠,
  포켓몬 볼 2종)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The
  Ruined/Kappa 유지). 기존 확립된 고정 표기를 다수 재사용: "Shellguard"→"셸가드", "Marpesia"→
  "마르페시아", "Chiropterror"→"카이롭테러", "Trifangle"→"트라이팽글", "Affinity"→"친화력",
  "cloaca"→"총배설강", "Chelsie"→"첼시", "Freezing"→"빙결"(모두 기존 선례). id 96461의 "Ruinous
  creatures"는 행성 고유명사 "루이너스"와 무관한 일반 서술 문맥으로 판단해 "파멸적인 생물들"로
  옮기고 음차하지 않았다(다른 배치의 "Ruinous" 행성 자원 시리즈와 구분). 포켓몬 "Shinx"→"꼬링크"는
  웹 검색으로 공식 명칭 확인. 신규 고유명사(선례 없음, 음차): Firrhna→피르나, Shieldon→실드온
  (포켓몬 공식명 재확인), Shitotsubakurai→시토츠바쿠라이, Shodai kitetsu→쇼다이 키테츠.
- 배치 0298(섀도우(Shadow) 계열 가구·크리터·아이템 대량, 비신(Bishyn) 수정 시리즈, 섹스본드
  성인 콘텐츠 다수, 산시 17(Shanxi 17) 권총 설명, 팔레트 편집 UI 문자열 대량, 엑소시아 제국 로어)는
  QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지).
  기존 확립된 고정 표기를 다수 재사용: "Merling"→"머링", "Frögg Furnishing"→"프뢰그 가구"(다수결,
  "프록 퍼니싱"/"프로그 퍼니싱" 소수 표기는 배제), "Jinxies"→"징시즈", "Exousia/Exousian"→
  "엑소시아/엑소시안", "Vermilion"→"주홍", "Mirage Star"→"신기루 항성", "Bishyn"→"비신",
  "Nokkimari"→"노키마리", "Rufescite"→"루페스사이트", "Freezing"→"빙결", "Grab-Bag"→"복주머니",
  "Smeltable"→"제련 가능", "Icicle"→"고드름"(모두 기존 선례). "Shanxi"(산시)는 실존 지명표준
  표기를 사용. 신규 고유명사(음차, 선례 없음): Serval-Chan→서벌쨩, Setricub→세트리큐브,
  Moontant→문턴트, Sharkon→샤콘(패러디 명칭 그대로 음차).
- 배치 0297(선하(Seonha)/아르고 호 로어 문단 다수, 센터/센트리 장비 시리즈, 케빈 연구소일지
  코미디 콘텐츠 9월 1~19일자 대량, "선배"(Senpai) 던전 동행 대사 다수, 알타/이오/헤비카관련
  설명문 다수)에서 `qa_structure.py` lines 오류 1건 발생 — id 95913(mechineki 세 줄
  대사)의 줄바꿈을 원문 1개 대신 2개로 넣었다가 `fix_0297.json`으로 정정, 이후 `qa_glossary.py`는
  기존 4건 베이스라인 그대로 통과. "Seonha"→"선하", "Argo"→"아르고", "magicite"→"마기사이트"는
  기존 확립된 표기(id 24367 등, 이미 "선하"라는 이름 자체가 선례로 존재)를 그대로 재사용.
  "Lords of the Cosmos"→"코스모스의 군주", "Numi"→"누미", "Elin"→"엘린", "Hevikai/hevika"→
  "헤비카", "Sentias"→"센티아", "Io"→"이오", "Faradea"→"파라데아", "alterash"→"알테라시",
  "Terramart"→"테라마트", "Nitori"→"니토리", "gheatsyn"→"기트신", "Gilten"→"길텐" 모두 기존
  선례 그대로 재사용. 신규 고유명사(음차, 선례 없음): Morragh→모라그, Selach→셀라크, Lilodon→
  릴로돈, Serbu(총기 브랜드)→서르부.
- 배치 0296("바다(Sea)" 가구 시리즈 대량, 씨스톤(Seastone) 건축 자재 시리즈, 보안(Security) 장비
  시리즈, 보조 발사(Secondary Fire) 무기 설명 다수, "I5-T 구역" 장문 로어(텐레/센/멜루/에고엔
  등장), 작별 인사 대사 다수)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건
  Miniknog/Trink/The Ruined/Kappa 유지, 장문 로어 텍스트 병합 시 줄바꿈 수 불일치 없음 확인).
  "Primary Fire"→"주 발사"/"Secondary Fire"→"보조 발사"(id 6201 등 선례, "Alt Fire"의 기존 고정
  번역과 동일한 결과어를 공유), "Parry"→"패링"(배치 0270에서 확정한 고정 용어), "Sea"→"바다"(id
  2478/20695 등 선례), "Seastone"→"씨스톤"(id 31282 등 선례), "Pioneer"→"파이오니어", "Paladin"→
  "팔라딘", "Akkimari"/"Avikan"/"Centensian"/"Trinkian"/"Gungnir" 모두 기존 확립된 음차재사용.
  신규 고유명사(선례 없음, 신규 음차): Sen→센, Mellou→멜루, Tenre→텐레, Egoen→에고엔, Winter(세력)
  →윈터, Valkyrie→발키리, Warlock→마법사(대마법사로 의역), Seaguard→씨가드.
- 배치 0295(정찰 드론 스캔 로그 대사 대량, 스콜피오(Scorpio)/스캐빈저(Scavenger) 가구·장비
  시리즈, 신틸리움(Scintillium) 광물 무기 시리즈, 슈라이텐(Schreiten) 동물 조각상 시리즈, 고철
  (Scrap) 무기·등급별 재료 시리즈, 무서움/비꼼 계열 감정 대사 다수, 포켓몬 볼 2종)는 QA이슈 없이
  구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). 기존 확립된
  고정 용어를 다수 재사용: "Hylotl"→"하이로틀", "Apex"→"에이펙스", "Miniknog"→"미니크녹"(모두
  글로서리 fixed), "Protectorate"→"보호국"(배치 0294에서 정정한 규칙 재적용), "entropic"→
  "엔트로픽", "Scavenger"(종족명)→"스캐빈저", "Dragoon"→"드래군", "Scepter"→"셉터", "Lunari"→
  "루나리"(모두 기존 선례). "Thel"(텔) 세력의 형용사형 "Thelean"은 기존 "텔" 표기를 그대로 살려
  "텔의"로 옮겼다. "voltage"(색상 태그 안 소문자 고유명)는 "Voltage worlds"의 기존 음차선례를
  따라 "볼티지"로, 일반 서술적 "전압"과 구분했다. 포켓몬 "Scolipede"→"펜드라", "Scorbunny"→
  "염버니"는 웹 검색으로 공식 한국어 명칭을 확인해 확정(앞선 배치의 "Rockruff"/"Salandit"과 달리
  이번엔 공식 명칭을 확인할 수 있었음).
- 배치 0294(새터니안(Saturnian) 종족 아이템·로어·능력치 블록 대량, 버블킨/메르킨 신규 종족 소개
  능력치 블록 2건, 게이밍 버그(GSA) 종족 능력치 블록, 핏빛(Sanguine) 자원 시리즈, 스캔 로그 대사
  다수, 슬픔/비꼼 계열 감정 대사 다수)에서 `qa_glossary.py` 고정 용어 위반 1건 발생 — id95383의
  "Protectorate"를 기존 코퍼스에 흔한 "보호령"으로 옮겼다가(→글로서리 고정 "보호국", 기존 번역
  287건 기준, "프로텍토레이트" 음역 금지 규칙) `fix_0294.json`으로 정정, 이후 기존 4건 베이스라인
  으로 복귀. 구조 오류는 없었음. "Protector"(플레이어 칭호)는 "보호국"과는 별개로 기존 선례(id
  63993 "우리 중 프로텍터가 되는 이는" 등)에 따라 "프로텍터"로 음차, 두 용어를 구분했다.종족
  능력치 블록은 다수결 표기("능력치"/"저항"/"면역"/"종족 특성" 등)와 Diet/Perks/Environment/
  Weapons/Weaknesses 계열 블록("식성"/"특전"/"환경"/"무기"/"약점", id 7842 등 선례)을 모두
  기존 표기 그대로 재사용했다. "Cybermen"(Doctor Who)은 선례 없어 공식 한국어 번역명 "사이버맨"
  채택. "Scalloped"는 동일 팩(ffxiv_viera) 내 거의 동일한 기존 문장(id 24094 "Wide scallop
  carving on Vieran mahogany"→"가리비 조각")을 우선 참고해 "가리비"로 옮기고, 다른 팩의
  "스캘럽"(Dalmascan Scalloped Stone) 음차와는 구분했다.
- 배치 0293(총기·탄창 코드명 대량(S1919~SVT-40 계열), 사쿠라(Sakura) 가구/장식 시리즈, 사그라사
  (Sagrassa) 채집 자원, 새지테리어스 인터갤럭틱(Sagittarius Intergalactic) 총기 브랜드,알타
  (Alta) 메크 회수 부품 설명 4건, 슬픔·안타까움 계열 감정 대사 다수, 살몬 파브롤 닭 시리즈)는 QA
  이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa유지).
  "AP"/"HE-T" 탄약 코드는 기존 선례(id 1280/27377 등)를 따라 국문화하지 않고 그대로 유지, 일반
  서술문에서만 기존 고정 표현 "철갑탄"을 사용해 두 문맥을 구분했다. "Mayhem"은 문맥에 따라 게임
  모드 고유명일 때는 기존 선례대로 "메이헴"으로 음차하고, 일반 서술적 혼란을 뜻할 때 쓰는 기존
  "대혼란" 번역과 구분했다. "Sagrassa"→"사그라사"(id 14956 선례), "쿠포"(kupo)·"연고 제작자"
  (Salve-maker)·"알타" 모두 기존 FFXIV-Viera/Alta 고정 표기 재사용. "Salandit"은 "Rockruff"와
  마찬가지로 한국 정식 포켓몬 명칭을 확인할 수 없어 음차 "살란딧"으로 처리(추후 정정 필요할 수
  있음). 신규 고유명사: Sagittarius Intergalactic→새지테리어스 인터갤럭틱, Sakuranite→사쿠라나이트,
  Saboteur(클래스명)→새보티어, Khopesh→코페시(모두 음차, 선례 없음).
- 배치 0292(룬(Runic) 계열 가구·장식 세트 대량, 러시아제 총기 설명 다수, 러스티(Rusty)/러스트
  (Rust)/러스티드(Rusted) 계열 잡화·크리터 대량, 아키(Akki) 종족 짧은 대사, 루카(Ruka)/루네바
  (Runeva) 식물 재료, S 계열 신규 아이템 다수(S.A.I.L, 티백 시리즈, S1 화기 시리즈))는 QA 이슈
  없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). "Runic"은
  기존 "룬 아르카니움 램프"(id 20594) 등 선례를 따라 "룬"으로 통일. "Rusty"/"Rusted"는 일괄
  "녹슨"으로, "Rust"(행성/자원명)는 기존 "러스트 소드"(id 20608) 선례를 따라 "러스트"로구분해
  옮겼다. "Akki"는 기존 조사(助詞) 생략형 어투(예: id 412 "아키는 할 말이 없다") 선례를그대로
  재사용. "AP rounds loaded"는 기존 고정 표현 "철갑탄 장전됨"(수십 건 선례)을 재사용했다.
  "Skimblitz"→"스킴블리츠", "Bulbhead"→"벌브헤드"(id 37766/53018 선례), "Eminsnow"→"에민스노우",
  "Viridescent"→"비리데슨트" 모두 기존 표기 재사용. 신규 고유명사: Ruka→루카, Runeva→루네바,
  Ryuugu→류구(음차), Räva→레바(음차), S'urysk→수리스크(음차).
- 배치 0291(로제(Rosé) 가구 시리즈 나머지 34종, 미가공 암석 설명 다수(안산암·아르코스·처트·역암·
  데이사이트·반려암·편마암·그릿스톤·이암), 루거(Ruger) 총기 개머리판 변형 8종, 루인(Ruin) 계열
  가구·몬스터 세트 다수, "Ruined"(폐허가 된) 계열 잡화 다수, 루이너스(Ruinous) 행성 자원시리즈,
  왕실(Royal) 가구·장비, 루바이트/루비움 계열 광물·무기)에서 `qa_glossary.py` 고정 용어위반 2건
  발생 — id 94912 "Ruin Portal"의 "Portal"을 "포탈"로 옮겼다가(→고정 "포털", "포탈" 금지규칙)
  `fix_0291.json`으로 정정, id 94948 "Saturnian"을 기존 텍스트에 흔한 "새터니언"으로 옮겼다가
  (→글로서리 고정 "새터니안") 마찬가지로 정정, 이후 기존 4건 베이스라인으로 복귀. 구조 오류는
  없었음. "Ruin-Killer"는 기존 고정 표기 "유적살해자"(다수 선례)를 재사용했으며, 이와 별개로
  "Ruin X"(가구·몬스터 접두사)는 "루인 찔러어어!"(id 21213)·"루인 님을 위해"(id 53056) 등 기존
  선례에 따라 신 자체를 가리키는 고유명사로 보아 "루인"으로 그대로 음차. "Ruined X"(폐허가 된
  잡화)는 기존 "폐허가 된 공장" 등 다수 선례를 따라 "폐허가 된"으로 통일, "Ruinous X"(자원)는
  "루이너스"(행성명, id 34590/34791 선례)로 통일해 세 계열을 구분했다. "Rowan"은 실제 수종
  "마가목"으로, "Rockruff"류와 달리 학명이 확실해 학명 번역을 채택. 미가공 암석 9종은 지질학
  정식 명칭(안산암/아르코스/처트/역암/데이사이트/반려암/편마암/그릿스톤/이암)을 새로 확정.
  가구 세트는 기존 "핫 로즈(Hot Rose)" 병렬 세트(동일 품목 34종)의 선례를 그대로 재사용해 용어
  일관성을 확보했다.
- 배치 0290("Right ..."로 시작하는 대사·설명 다수, 림(Rim) 계열 우주선 부품 시리즈, 로봇형 외계
  종족·바퀴벌레형 외계 종족 능력치 블록, 록루프(Rockruff) 포켓볼, 로닌(Ronin) 가구 시리즈, 로제
  (Rosé) 가구 시리즈, 떠돌이 사무라이 4종, 로부타(Robutt) 요정 종족 뜻 모를 대사 1건)는 QA 이슈
  없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). "Rim"은
  기존 "림 배경 문"(id 6479) 선례를 따라 "림"으로 통일 음차, "Rimrock"은 "림록"으로 신규음차.
  "Rogue"는 "로닌"과 구분되는 별도 낭인 계열 명칭으로 보아 "떠돌이"로 옮김(로그 사무라이4종,
  아가란 함선, 그린핑거 플러시, 우루탄 화분에 일괄 적용). id 94673 "Robutt hoom! Enjoy house
  choka smashroom?"은 기존 로부타 요정 뜻모를 대사 다수 선례(id 67928 등, "smashroom"→"스매시룸"
  음차 확정)를 따라 무의미 조어는 음차하고 "robutt"는 고정 표기 "로봇엉덩이"를 재사용. 종족 능력치
  블록 하위 항목은 프로젝트 전체 다수결 표기("Attributes"→"능력치", "Resistances"→"저항"등, id별
  약 100건 이상 표본 확인)로 통일해 소수 표기("속성"/"특성"/"얼음 저항" 등)를 배제. "Poultry"→
  기존 "가금육", "Hellish"→기존 "지옥"(id 29195 "지옥 고추" 선례) 재사용. "Pokéball"은 기존 "몬스터볼"
  고정 용어를 재사용해 "록루프(암컷/수컷) 몬스터볼"로 옮겼으며, "Rockruff" 자체는 한국 정식
  포켓몬 명칭을 확인할 수 없어(웹 조회 결과 확정 불가) 음차 "록루프"로 처리(추후 공식 명칭 확인
  시 정정 필요할 수 있음). "Rosé"는 기존 "로제 찻잔"(id 20583) 선례를 따라 "로제"로 통일.
- 배치 0289("Return"/"Revisit" 계열 귀환·재방문 안내문 다수, "Reverse Cowgirl" 등 SxB 체위 아이템,
  라데이스(Rhadeis) 종교 관련 대사·로어 문단 대량, 로드아일랜드 레드 닭 시리즈, 리샨(Ri'shaan)
  숭배 대사·로어, 라인란트/라이노스틸 무기·메크 부품 시리즈)는 QA 이슈 없이 구조·용어 모두 첫
  시도에 통과(베이스라인 4건 Miniknog/Trink/The Ruined/Kappa 유지). "Rhadeis"는 기존 확립된
  "Ce'Tennan→세테난" 설정과 연결된 신규 고유명사로 "라데이스"로 음차, "Ri'shaan"은 뱀 신특유의
  쉿쉿거리는 어조(-sss 접미사)를 살려 "자라난다쓰/먹는다쓰/준다쓰"처럼 한글 구개음화 표기로
  옮기고 이름 자체는 "리샨"으로 통일. 태그가 문장 중간에 끊긴 색상 반복 패턴("Rhode Island
  D^gray;r^reset;i^gray;p^reset; Chick" 등)은 태그 구조를 그대로 보존하고 로마자 "Drip"만
  한글 음역 없이 원문 표기 그대로 유지.
- 배치 0288("Response: ^white;..." 우주선 교신 대사 나머지 약 65건, 크루세이더/루인드 로어(id
  94256), Restored 가구·오브젝트 시리즈, Retro 가구 시리즈)에서 `qa_structure.py` tags 오류 1건
  발견 — id 94274에서 ^green;/^yellow; 색상 태그 4개 중 2번째 ^yellow;를 누락해 재수정.이후
  `qa_glossary.py`는 기존 4건 베이스라인 그대로 통과. "the Ruin"(id 94256, 대문자 고유명사)은 기존
  고정 표기 "The Ruined"="루인드"와 동일한 엔젤 타락 종족을 가리키는 것으로 보아 "루인드"로 옮김
  (일반 형용사 ruined와는 구분). "Bitching Betty"(id 94325, 항공기 경보 시스템 실존 용어)는
  "비칭 베티"로 음역.
- 배치 0270(무기 Passive 설명 대량 — 궁니르/에피메테우스/랩처/노틸러스/솔스티스 등 무기고유명 다수
  포함, Peacekeeper 아이템 시리즈 대량, Pastel 가구 시리즈)에서 `qa_glossary.py` 신규 후보 1건
  발생 — id 90406의 "Poptop"을 TM에서 흔히 보이는 "팝탑"으로 옮겼다가(→고정 "팝톱", 기존스타바운드
  번역 표기) `fix_0270.json`으로 정정, 이후 기존 4건 베이스라인으로 복귀. "Peacekeeper"관련 아이템
  전부 고정 용어 "피스키퍼"로 통일 적용. 구조 오류는 없었음.
- 배치 0269(포장 탄약/유탄 시리즈, Paint Set 색상별 시리즈, Palace/Panther 가구 시리즈,판데모니움/
  회상의 판테온 로어, 공수부대 가방 3종)에서 `qa_glossary.py` 신규 후보 1건 발생 — id 90309 "Parry
  This!"를 고정 용어 "패링"을 쓰지 않고 "이거나 막아봐!"로 의역했다가(→고정 "패링") "이패링이나
  받아봐!"로 `fix_0269.json` 정정, 이후 기존 4건 베이스라인으로 복귀. 구조 오류는 없었음.
- 배치 0268("Outpost" 가구 마무리, "Over-/Ov-" 아이템 다수, 바스 브할레이/브할레이안 전쟁 로어,
  천사·루인드·컬티베이터 로어 문단, P-ASA/PMC/PP-19 계열 총기 시리즈 대량)는 QA 이슈 없이 구조·
  용어 모두 첫 시도에 통과(베이스라인 4건 유지). "Vas Vha'leih"는 TM 다수결로 "바스 브할레이"(4 대
  1 "바스 브라레이")를 재사용. 총기명 안에 등장하는 원문 큰따옴표(`"Bizon"`, `"Vityaz"`)는 프로젝트
  규칙에 따라 한글 홑따옴표로 옮김.
- 배치 0267("Our ..."로 시작하는 세계관/로어 문단 다수 — 게슈탈트·델파 하이브·트라이노큘러
  사략단·우로보로스 산업 카르텔·에인션트 시련의 문 등, "Outpost" 가구/장비 시리즈 대량)는 QA 이슈
  없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 유지). "Delpha Hive"는 TM에 "델파 벌집"·"델파
  하이브" 표기가 1:1 동률이라 "델파 하이브"로 통일. "Sunborn"은 고정 번역어가 없어(TM에 "태양에서
  태어난"/"태양의" 두 변형 존재) 문맥상 "태양에서 태어난 자들"로 신규 통일. id 89815의
  "Ceter-spheres, alter-spheres"는 "Cyberspheres"를 잘못 알아들은 말장난이라 "세터스피어,
  알터스피어"로 음차 대응.
- 배치 0266("Orion" 가구/장비 시리즈 대량, Orc/Ooze/Otter 종족 능력치 블록, PEC/테레네 선거단/
  아나차리 무기 로어, "Our ..."로 시작하는 세계관 설명 다수)는 QA 이슈 없이 구조·용어 모두 첫
  시도에 통과(베이스라인 4건 유지). "Fatal Circuit"은 TM 다수결로 "페이탈 서킷"(9 대 1 "치명적인
  회로")을 재사용. "Oshawott"는 포켓몬 공식 한글명 "수댕이", "Pokéball"은 "몬스터볼"로 옮김(둘 다
  이 프로젝트 TM에 선례가 없어 포켓몬 공식 로컬라이제이션 명칭을 기준으로 신규 확정).
- 배치 0265("Only/Ooh/Oooo/Open/Opus/Or/Orange..."류 짧은 설명·감탄사 다수, 색상별 "Orange" 아이템
  시리즈 대량)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The
  Ruined/Kappa 유지). "Fleshlight"는 TM 다수결로 "플레시라이트"(14 대 9 "자위기구")를 재사용.
  "Float Crystal"은 기존 표기가 "부유 수정"/"부유 크리스탈"로 3:3 동률이라 같은 배치 내 "Blue Float
  Crystal S"→"파란 부유 수정 S" 선례를 따라 "부유 수정"으로 통일. "Orange" 계열 아이템 중 음식류
  (빵·케이크·잼·파이·가금육·셔벗·타르트·과일)는 색상이 아닌 향미를 뜻하므로 "오렌지"로,그 외
  가구·장식·생물 이름은 색상을 뜻하므로 "주황"으로 구분해서 옮김.
- 배치 0264("One day..."/"One of..."/"One ..." 아이템 설명 다수, Oni/Dominion 등 종족 능력치 블록,
  Keys of Darkness/Echoes/Entropy 등 9종 고대 열쇠 로어 문단, Aeginian Federal Union/보이저 컴퍼니
  로어)에서 `qa_glossary.py` 신규 후보 1건 발생 — id 89291 "manipulator module"을 일반 명사처럼
  "조작 모듈"로 옮겼다가(→고정 "물질 조작기 모듈") `fix_0264.json`으로 정정, 이후 기존 4건
  베이스라인으로 복귀. 구조 오류는 없었음. "Hammer Munitions"는 TM 다수결로 "해머 뮤니션스"(12건,
  "해머 뮤니션즈"·"망치 탄약"은 각 1건뿐), "Felin"은 "펠린"(133 대 7), "Eithne"는 "에이스네"(13 대
  1 "아이스네")로 통일. Cryoguin/Pengvolt/Plaguin/Pyroguin(원소 펭귄 시리즈)은 TM 선례가없어
  각각 "크라이오귄"/"펭볼트"/"플레이귄"/"파이로귄"으로 신규 음차.
- 배치 0263("Old ..."/"Once ..."/"One ..."로 시작하는 아이템 짧은 설명·로어 문단 다수, Dominion/
  Callistan/도미니온 종족 능력치 블록, FFXIV-Viera 인사말)에서 `qa_glossary.py` 신규 후보 2건 발생 —
  id 89044 "On behalf of salve-maker, wood-warder..."에서 각각 "약제사"·"숲지기"로 의역했다가
  (→FFXIV-Viera 고정 용어 "연고 제작자"·"숲의 파수꾼") `fix_0263.json`으로 정정, 이후 기존 4건
  베이스라인으로 복귀. 구조 오류는 없었음. id 89061의 "fel"/"fela" 가상 생물학 용어 문단은 기존
  TM(id 76847)의 "펠"/"펠라"/"상위·최상위 결합" 표기를 그대로 재사용해 "하위·최하위 결합"으로
  대칭 번역. id 89087의 Jabberwocky/Raven 패러디 시는 무의미 조어를 음차하여 원문의 넌센스 어조를
  최대한 보존. id 89106처럼 태그가 닫히지 않은 원문(`^pink;Lustia`, reset 없음)은 태그 개수를
  맞추기 위해 문장 구조를 재배치하되 reset을 추가하지 않음.
- 배치 0262("Oh," "Oh?" "Oh.." "Okay,"류 감탄사 대사 다수, Sexbound SxB 콘텐츠 페이지, 여러 종족과의
  첫 대면 인사)는 QA 이슈 없이 구조·용어 모두 첫 시도에 통과(베이스라인 4건 Miniknog/Trink/The
  Ruined/Kappa 유지). "Stargazers"는 TM 다수결에 따라 "별관측자" 대신 "스타게이저"로(34대 25),
  "Arcanian"은 "아케이니안" 대신 다수 표기 "아르카니안"으로(62 대 10), "Shoggoth"는 "쇼고트" 대신
  다수 표기 "쇼고스"로(25 대 2) 통일. id 88693의 색상 태그로 음절이 쪼개진 고유명("Tray^..o
  Dhā^..tava")은 원문 로마자 표기와 태그 분할을 그대로 유지하고 주변 문장만 한글로 옮김.id 88804의
  Sexbound 설정 안내문에서는 "futanari"/"enable"/"false"/"true" 같은 설정 파일 리터럴 값을 번역하지
  않고 원문 그대로 남김(설정 키/값이므로 코드 취급).
- 배치 0261("Oh ..."로 시작하는 감탄사형 대사 다수, alta/졸티온 종족 설명, L40 기관단총변형 여러
  종, Relic Seekers/Angels 로어 문단)에서 `qa_glossary.py` 신규 후보 1건 발생 — id 88412의 종족
  설명 능력치 블록에서 "Machine Pistol"을 "머신 피스톨"로 옮겼다가(→고정 "기관권총") `fix_0261.json`
  으로 정정, 이후 기존 4건 베이스라인(Miniknog/Trink/The Ruined/Kappa)으로 복귀. 구조 오류는 없었음.
  "Relic Seekers"는 TM 다수결에 따라 "유물 탐구자"로, "Sheye"는 "시아이"가 아닌 다수 표기 "셰이"로
  통일(전수 검색 결과 59 대 4). "Crown Federation"도 다수 표기 "크라운 연방"(2건) 사용, "황관 연방"
  (1건)은 소수 표기로 배제. "The Ruined"는 고정 용어 "루인드"로 정확히 옮김(id 88566). id 88621의
  Angels 로어 문단에서 원문 큰따옴표로 인용된 "commander"·"protecting all the races"는 프로젝트
  규칙에 따라 한글 홑따옴표로 치환하여 파이썬 문자열 구문 오류를 예방.
- 배치 0259(OGS/OAS 광물 접두사, OTRINCO 총기 시리즈 다수)에서 `qa_glossary.py` 신규 후보 4건 발생
  — "Aegisalt"를 "이지실트"로(→고정 "에지솔트"), "Violium"을 "바이올리움"으로(→고정 "바이올륨"),
  "Alt Fire"를 따옴표 안 그대로 영어로 남겨서(→고정 "보조 발사"; 참고로 대괄호 입력 토큰
  `[ALT-FIRE]`는 번역하지 않지만 이번 건은 그냥 텍스트였음), "a new crafting station"을 "새 제작
  스테이션"으로(→고정 "제작대") 옮긴 것 — 모두 `fix_0259.json`으로 정정. OGS/OAS 접두사가 붙는
  광물명은 원소명 자체의 고정 번역을 그대로 따라야 하며 임의로 음역하면 안 됨을 재확인.
- 배치 0258(퀘스트 대사 다수, 긴 contentpages 다수)에서 `qa_structure.py` `tags` 실패 3건
  (id 87619, 87640 — 문장 끝에 불필요한 태그를 추가로 열어놓음; id 87674 — 원문의 `^green;` 태그
  하나가 누락됨) — `fix_0258.json`으로 정정. 긴 다중 태그 문장에서 재배치할 때 태그 개수를 다시
  세어보는 습관이 필요함(이번 세션 통틀어 가장 흔한 실수 유형). 신규 고유명사: Xanafian→자나피안,
  Xanafir→자나피르, Centensian→센텐시안, Vhos Avha'las→보스 아브할라스, the Occasus→오카서스,
  Ce'Tennan→세테난, Ayurin→아유린, Kavanite→카바나이트, Legion Switch Gear→리전 스위치 기어,
  Baiter→베이터, Praetor Cannon→프라이터 캐논, Area 48→구역 48(모두 TM 선례 확인).
  "Vas Vha'leih"는 TM에 바스 브할레이/브라레이/브알레이 세 표기가 혼재해 철자에 가장 가까운
  "바스 브할레이"로 통일. "The Conquistadors"(세력명)는 선례 없어 기존 클래스명 "콘키스타도르"를
  그대로 재사용. "BigCoin"은 선례 없어 "빅코인"으로 신규 음역.
- 배치 0257은 QA 이슈 없이 첫 시도에 통과("Not X" 계열 대사 다수). 신규 고유명사: the Lords of the
  Cosmos→코스모스의 군주(TM 다수), Terraforge→테라포지(TM), Grand Protector Esther→대보호자
  에스더(TM 다수, "그랜드 프로텍터"는 소수), Metaphysics(기술 카테고리)→형이상학(TM),
  Notician Federation→노티시안 연방(TM). 선례 없는 것은 신규 음역: Taurikin→타우리킨,
  kuva→쿠바, grineer→그라니어(둘 다 Warframe 크로스오버 참조), Legion switchblades→리전스위치블레이드.
- 배치 0256은 QA 이슈 없이 첫 시도에 통과(NonEKI/Nomada 계열 대사·아이템 다수). 신규 고유명사:
  the Gestalt→게슈탈트(TM), Archangel Xequeyzriel→대천사 세퀘이즈리엘(TM), Ruin-Killer→유적살해자
  (TM 다수), Ruin-Touched→유적에 물든 자(TM 다수), Nomada→노마다(TM), Noolith→누올리스(TM 다수),
  Annelisks→아넬리스크(TM), the Gardener→정원사(TM), the Serpent→서펀트(TM), Dreadwing→드레드윙(TM),
  Actias→악티아스(TM). 선례 없는 것은 신규 음역: Tek'mellian→테크멜리안, Shigu→시구,
  Fragmented Ruin(형용사구, 미출현 확정 고유명사는 아님)→조각난 루인, Unustrello→우누스트렐로.
- 배치 0255는 QA 이슈 없이 첫 시도에 통과. 초안 작성 중 한국어 인용구에 영어 큰따옴표를그대로 써서
  Python 문자열이 깨질 뻔한 걸 실행 전 `ast.parse`로 자체 검증해 발견/수정(id 86995) — 이제부터
  빌드 스크립트 실행 전에 `python3 -c "import ast; ast.parse(open(...).read())"`로 문법검증하는
  것을 표준 절차에 추가할 것. 신규 고유명사: Shogun Takeshi→쇼군 타케시(TM 다수), Stargazers→
  별관측자(TM 다수), Sylphs→실프, Darkdweller→다크드웰러, Nitori Industries→니토리 인더스트리.
  선례 없는 Elder Scrolls 계열 용어 "khajiit"→카짓, "skooma"→스쿠마로 신규 음역.
- **중요 발견**: `qa_glossary.py`에서 처음으로 "Floran(1)" 후보가 나타나 조사한 결과(id 86684,
  "New life inside Floran bloom slow, but strong!" 번역에서 "Floran/플로란" 자체가 누락됨),
  `fix_0254.json`으로 정정. 이 과정에서 기존에 "기준선 오탐"으로 잘못 분류해온 `gheatsyn(1)`의
  실체를 재확인: `qa_glossary.py`의 glob 패턴(`translations/rest_*.tsv`)은 확장자가 정확히 `.tsv`인
  파일만 스캔하므로 `*.tsv.unreviewed` 파일은 애초에 검사 대상이 아니었음 — 즉 배치 0224이후
  계속 "review_pending의 미검토 파일 때문"이라 여겨온 gheatsyn 후보는 사실 배치 0241의 id 83866
  (우유체 AI 편지, "gheatsyn spawkles"를 "기쁨의 반짝임"으로 의역해 고정 용어 "기트신"이번역문에서
  빠진 것)이 원인이었다. `fix_gheatsyn_83866.json`으로 정정해 실제 오류를 바로잡음.
  **교훈**: `qa_glossary.py`/`qa_structure.py`가 보고하는 후보는 파일 글롭 패턴이 정확히무엇을
  스캔하는지부터 확인하고 원인 id를 직접 추적할 것 — "이미 알려진 오탐"이라고 넘겨짚지 말 것.
  기준선이 `Miniknog(1)/Trink(1)/The Ruined(1)/Kappa(1)` 4건으로 줄어듦 (gheatsyn 제외).
- 배치 0253은 QA 이슈 없이 첫 시도에 통과(대부분 가구/무기 아이템명). "Neo Imperial"은 TM 선례
  "네오 제국"으로 통일. "Nether"는 TM 다수 표기 "네더" 사용. "Zweihander"는 TM 표기 "츠바이헨더".
- 배치 0252는 QA 이슈 없이 첫 시도에 통과(대부분 Neki 종족 쉿소리 대사와 가구/무기 아이템명).
  "Peglaci"는 재확인 결과 TM 전체에서 페글라시(52건)가 페글라치(43건)보다 실제로 더 많아배치
  0251의 선택("페글라시")이 맞았음을 확인 — 정정 불필요.
- 배치 0251에서 `qa_structure.py` `inputtoken` 실패 1건(id 86035 — 원문 `[SHIFT]`를 `[Shift]`로
  대소문자 다르게 옮김, 계속 반복되는 실수 패턴) — `fix_0251.json`으로 정정. 초안 작성 중 한국어
  인용구에 영어 큰따옴표(`"..."`)를 그대로 써서 Python 문자열 리터럴이 깨지는 걸 자체 발견/수정
  (id 86128, 86145 — 작은따옴표로 대체). 신규 고유명사: alkey→알키어, K'Rakothan→크라코탄
  (K'Rakoth=크라코스와 구분), Relic Seekers→유물 탐구자(TM 다수), Deadbeat(종족명 문맥)→데드비트,
  Peglaci→페글라시, Nebulac→네뷸락, Necroium→네크로이움, Ava Day→아바의 날, Arcane City→아케인 시티.
- 배치 0250에서 "Broadsword"를 "대검"으로 옮겨 고정 용어(→"브로드소드", 대검·장검과 혼용금지) 위반
  발생(id 85960, "NPC Shadow Broadsword") — `fix_0250.json`으로 정정. "Trink Circuit"은 TM 표기
  "트링크 서킷"/"트링크"로 통일. "Mystic Moon"은 TM에 신비 달(1)/미스틱 문(다수) 혼재, 다수인
  "미스틱 문"으로 통일. "N.I.C"류 약자 다수는 관례대로 영문 그대로 유지.
- 배치 0249에서 `qa_structure.py` `tags` 실패 1건(id 85668 — 원문이 `^green;`만 열고 안닫는데
  번역에 불필요한 `^reset;`을 추가한, 계속 반복되는 실수 패턴) — `fix_0249.json`으로 정정.
  신규 고유명사: the Argo→아르고(호), Aurea→아우레아, Trangii→트랑기, Thornwing→쏜윙(TM다수),
  GOV(Generic Omnipresent Voice)는 선례 없어 영문 약자 그대로 유지. "Grounded"가 종족/신분을
  가리키는 문맥(id 85663, "A Grounded.")에서는 "그라운디드"로 음역(TM에는 아비안 지상 마을 등
  형용사적 용례만 있고 이런 명사적 자기소개 용례 선례 없음).
- 배치 0248에서 "Peacekeeper"를 흔한 TM 표기 "평화유지군"으로 옮겼다가 고정 용어(→"피스키퍼",
  2026-09-23 사용자 지시로 변경된 값이라 TM 다수결과 다름) 위반 발생(id 85554) — `fix_0248.json`으로
  정정. 고정 용어표가 TM 다수 사용례와 다를 수 있으니 `qa_glossary.py`가 항상 최종 기준임을 재확인.
  다수의 신규 고유명사 확인: Aeginian→아에기니안, the Union→유니온, the Alliance→얼라이언스,
  the Ruin(다른 개체, the Ruined와 구분)→루인, Thell→텔, Avikan→아비칸, Kirhosi→키르호시,
  the Old Ones→고대인(TM 다수), Ri'shaan→리샨, Enternia→에터니아.
- 배치 0247에서 `qa_structure.py` `tags` 실패 1건(id 85221 — 원문이 `^blue;`만 열고 안 닫는데
  번역에 불필요한 `^reset;`을 추가한, 이번 세션 계속 반복되는 실수 패턴) — `fix_0247.json`으로 정정.
  다수의 신규 고유명사 확인: Letheia→레테이아, Gilten→길텐, Woolotl→우울로틀(TM 다수), Kyterran→키테란,
  Magnetar→마그네타, NostOS→노스토스, Thalasso→탈라소, Esetera→에세테라, Solalei→솔라레이,
  Myrasyl→미라실, Titancorp→타이탄코프, Chocobo→초코보, Gysahl→기잘, the Ruined→루인드(TM 선례).
  "MCC"(Miniknog Control Collar)는 TM에 한국어 확장 표기 없이 영문 약자 그대로 사용된 선례 있어 유지.
- 배치 0246은 QA 이슈 없이 첫 시도에 통과. "Moogle"은 TM에 무글/무구글/모글 세 표기 혼재하지만
  배치 0238에서 쿠포 대사 문맥에 "모글"로 통일하기로 한 선례를 그대로 재사용(가구 계열 아이템도 동일
  적용). "Monster Hide"/"Monster Leather"가 같은 배치에 함께 등장해 구분을 위해 각각 "몬스터 생가죽"/
  "몬스터 가죽"으로 옮김(TM에 Hide 단독 선례 없음, Leather와 병기될 때만 이렇게 구분).
- 배치 0245에서 `qa_structure.py` `tags` 실패 2건(id 84777, 84780 — 원문이 `^red;`만 열고 `^reset;`으로
  닫지 않는데 번역에 불필요한 `^reset;`을 추가함, 계속 반복되는 실수 패턴)과 `inputtoken` 실패 1건
  (id 84907 — 원문 `[SHIFT]`을 `[Shift]`로 대소문자 다르게 옮김)을 `fix_0245.json`으로 정정.
  이어서 `qa_glossary.py`에서 "Parry Window"를 "패링 윈도우"로 옮겨 고정 용어(→"패링 창") 위반
  발생(같은 id 84907) — `fix2_0245.json`으로 재정정. "Molten Knight"는 TM에 용암 기사(1)/용융 기사(2)
  혼재, 더 빈번한 "용융 기사"로 통일. "Mollopod"는 TM 표기 "몰로포드" 사용.
- 배치 0244에서 "Rocket Launcher"를 "로켓 런처"로 옮겨 고정 용어(→"로켓 발사기") 위반 발생
  (id 84625, "Mini-Rocket Launcher") — `fix_0244.json`으로 정정. "Miniknog"는 TM 고정 표기
  "미니크녹" 그대로 다수 반복 사용(무기/장비/파벌 설명 다수). "Nightar"는 TM 표기 "나이터" 사용.
- 배치 0243은 QA 이슈 없이 첫 시도에 통과. Felin 종족의 미번역 인사말("Mihli, vliromifhras")은
  기존 TM 선례가 없어 다른 종족 고유어와 동일하게 발음 그대로 음역(미흘리, 블리로미프라)함.
  "Miko"는 TM에 "무녀"로 기존 번역 있어 재사용. "Mega-Fauna"류처럼 "the Growing One"을 흉내 내는
  신규 크리처 "the Grand Impersonator"는 선례 없어 "그랜드 임퍼소네이터"로 신규 음역.
- 배치 0242에서 `qa_structure.py` `lines` 실패 1건(id 84142, "Meeting stranger. Being friendly.\nNew
  experience!" — 2줄인데 1줄로 붙여씀) — `fix_0242.json`으로 정정. "Mega-Fauna"는 TM에 기존 번역
  "거대-동물"이 있어 그대로 재사용(음역 "메가 야수" 금지). "K'Rakoth"는 TM 관례상 "크라코스"로 음역.
  "Pokéball"은 TM에 몬스터볼(8건)/포켓볼(39건) 혼재, 더 빈번한 "포켓볼"로 통일.
- 배치 0241은 QA 구조 검사 이슈 없이 첫 시도에 통과. RPG Growth 모드 대형 체인지로그 5건(id 84000~84004,
  전문화/직업/역학 패치노트)을 기존 확인된 클래스·전문화 명칭 TM(도적/개척자/마법사/트래퍼/방랑자/닌자/
  체인즐링/드래군/숙련자/암살자/버서커/배틀 메이지/워록/콘키스타도르/사무라이/엘리멘트리스/용병/기사)에
  더해, 이번 배치에서 처음 등장한 클래스명은 선례가 없어 신규 음역으로 확정: 메카니스트(Mechanist),
  네크로맨서(Necromancer), 테크노맨서(Technomancer), 타이탄(Titan), 세이지(Sage), 셰이드(Shade),
  캐노니어(Cannoneer/Canoneer), 발키리(Valkyrie), 오퍼레이티브(Operative). 이후 배치에서같은 명칭이
  나오면 이 음역을 그대로 재사용할 것.
- id 83839 "May the Byak take thee, fell fiend!"는 나이타르(Nightar) 관련 저주 문맥이므로 무관한
  크리처 "Byakhee(백희)"가 아니라 "바이악"으로 번역함 — 두 용어를 혼동하지 않도록 주의.
- `qa_glossary.py`에서 신규 후보 `gheatsyn(1)`이 나타났으나, 이는 배치 0241과 무관하게
  `translations/review_pending/rest_priority_0166.tsv.unreviewed`(미검토 대기 파일, id 66412)에
  이미 존재하던 미번역 잔여물임을 확인함. 기준선 오탐 목록에 추가: `Miniknog(1)/Trink(1)/
  The Ruined(1)/Kappa(1)/gheatsyn(1)`. 해당 unreviewed 파일이 정식 검수·병합될 때 함께 고칠 것.
- 배치 0240은 QA 이슈 없이 첫 시도에 통과. 커스텀 `Diet`/`Perks`/`Environment`/`Weapons`/`Weaknesses`
  형식 종족 블록 1건(Auroran, id 83710)이 포함되어 기존 라벨 세트를 재사용해 처리. "Eithne"는 TM에
  에이스네/아이스네 두 표기가 혼재해 더 빈번한 "에이스네"로 통일함.
- 배치 0239에서 "Manipulator Module"을 "조작기 모듈"로 옮겨 고정 용어(→"물질 조작기 모듈") 위반이
  발생했다(id 83527) — `fix_<id>.json`으로 정정. "Manipulator"류 아이템은 단독으로 나올때와 달리
  "Module"이 붙으면 "물질 조작기 모듈"로 고정되어 있으니 주의.
- 표준 종족 능력치 블록 1건(Clownkin, id 83602)이 포함되어 기존 라벨 세트를 재사용해 처리.
- 배치 0238은 QA 이슈 없이 첫 시도에 통과("Maggot Man says" 가짜 속담 잔여분, 마기사이트/매지우드
  계열 가구·아이템명 위주). "Moogle"은 기존 TM에 무글/무구글/모글 세 가지 표기가 혼재해,쿠포 대사
  문맥의 "모글" 표기를 이번 배치에서 채택함(id 83291) — 추후 재등장 시 참고.
- 배치 0237에 "Maggot Boy/Man says: ..." 형태의 뒤섞인 가짜 속담 개그 대사가 약 45개 포함되어
  있었다 — 원문이 의도적으로 진짜 속담들을 뒤섞어 만든 헛소리이므로, 매끄러운 한국 속담으로
  "고쳐서" 번역하지 않고 원문의 단어 하나하나를 직역해 그 뒤섞인 우스꽝스러움을 그대로 살렸다.
  QA 이슈 없이 첫 시도에 통과.
- 배치 0236에서 원문에 없는 `^reset;` 태그를 추가해 `tags` 불일치가 발생한 사례가 또 나왔다(id 82923,
  `^orange;chain reaction.`으로 닫는 태그 없이 끝나는 원문) — `fix_<id>.json`으로 정정.계속 반복되는
  실수이므로, 문장이 태그로 끝나는 경우 특히 주의해서 원문에 `^reset;`이 있는지 확인할 것.
- 배치 0235는 QA 이슈 없이 첫 시도에 통과. Pokémon 포켓볼 아이템명(Lopunny 등)은 TM에 기존 번역이
  있는 경우 그 표기(로퍼니 등)를 그대로 재사용할 것 — 포켓몬 이름은 임의 음역하지 말고 항상
  `term.py`로 먼저 확인.
- 배치 0234에 표준 종족 능력치 스탯 블록 5건(Karemma id 82163, Nevrean id 82193/82194, 인형 상인
  종족 id 82202, id 82346)과 커스텀 `Diet`/`Perks`/`Weapons`/`Weaknesses` 형식 블록 1건(id 82195)이
  포함되어 있었다 — 기존 라벨 세트(README 배치 0226·0227 항목 참고)를 그대로 재사용해 처리.
  "Grenade Launcher"를 "유탄발사기"(붙여쓰기)로 옮겨 고정 용어(→"유탄 발사기", 띄어쓰기포함) 위반이
  발생했다(id 82350) — `fix_<id>.json`으로 정정. 무기 고정 용어는 띄어쓰기까지 정확히 일치해야 함에
  주의.
- 배치 0233에서 "AP rounds"를 "AP탄"으로 옮겨 고정 용어(AP rounds→철갑탄) 위반이 발생했다(id 82028)
  — `fix_<id>.json`으로 정정. 총기 탄약 약어(AP/HE/FMJ 등)는 음역하지 말고 고정 한국어 용어를
  먼저 확인할 것.
- 배치 0232는 QA 이슈 없이 첫 시도에 통과(Letheia/Lethia 가구·NPC 대사, "hoom/choka" 식의성어
  대사 1건(id 81923)은 기존 TM의 "훔" 표기 관행을 따름).
- 배치 0231에서 원문에 중첩된 `^green;...^orange;...^reset;` 태그(하나의 `^reset;`이 색상 태그
  두 개를 동시에 닫는 패턴, id 81528)를 번역문에서 `^orange;`를 누락한 채 옮겨 `tags` 불일치가
  발생했다 — `fix_<id>.json`으로 정정. 색상 태그가 중첩되어 닫는 태그 하나로 여러 개를 닫는 경우,
  번역문에서도 열리는 태그를 전부 포함해야 한다.
- 배치 0230은 QA 이슈 없이 첫 시도에 통과(무기 발사 효과 설명, Legion 유닛 대사, 아이템명 위주).
- 배치 0229에서 `Novakid`를 "노바킨"으로, `Lustling`을 "러스트링"으로 오역해 고정 용어(Novakid→노바키드,
  Lustling→러스틀링) 위반이 발생했다 — `fix_<id>.json`으로 정정. Lustling 오역은 배치 0224(id 80330)에서도
  이미 저질렀던 실수임을 뒤늦게 발견해 함께 소급 정정했다 — 두 단어 모두 직관적인 표기(노바킨/러스트링)로
  잘못 적기 쉬우니 매번 고정 표기(노바키드/러스틀링)를 확인할 것.
- 배치 0228은 QA 이슈 없이 첫 시도에 통과(총기·가구 아이템명 위주, 프랑스어 플레이버 텍스트 1건
  id 80987 "La fée de toutes les couleurs"은 관례대로 한국어로 완전히 옮김).
- 배치 0227에 커스텀 형식(FFXIV Viera류) 종족 특전 블록(id 80798: `General Perks`/`BiomePerks`/
  `Weapon Perks`/`Weaknesses`/`Biome Weaknesses`, 표준 스탯 블록과 다른 형식)이 포함되어있었다 —
  TM에서 라벨 세트를 확인해 재사용: `Diet→식성`, `General Perks→일반 특전`, `Base Stats→기본 스탯`,
  `Movement→이동`, `Resists→저항`, `Immunities→면역`, `Biome Perks→지형 특전`,
  `Weapon Perks→무기 특전`, `Weaknesses→약점`, `Biome Weaknesses→지형 약점`,
  `Stomach Capacity→배 용량`, `Crit Chance→치명타 확률`, `Cosmic→우주`. 이 블록 안에서
  `Shortsword`를 `숏소드`로 옮겼다가 `qa_glossary.py`의 고정 용어(Shortsword→소검) 위반으로 걸려
  `fix_<id>.json`으로 정정 — 무기 분류 고정 용어(Dagger=단검과 구분되는 Shortsword=소검)는
  일반 서술문에서도 예외 없이 적용해야 한다.
- 배치 0226에 종족 능력치 스탯 블록 2건(id 80648 Kitsune, id 80709 Klingon)이 포함되어 있었다 —
  기존 TM에서 고정 라벨 세트를 확인해 그대로 재사용: `Attributes→능력치`, `Max Health→최대 체력`,
  `Max Energy→최대 에너지`, `Energy Regen→에너지 재생`, `Attack Multiplier→공격력 배율`,
  `Defense→방어력`, `Resistances→저항`, `Fire/Electric/Poison/Ice/Physical Resistance→화염/전기/독/
  냉기/물리 저항`(Ice는 냉기 저항이 다수, 얼음 저항은 소수 변형), `Immunities→면역`,
  `Racial Traits→종족 특성`, `Knockback Resistance→넉백 저항`, `Fall Damage→낙하 피해`,
  `Movement Speed→이동 속도`, `Breath Depletion Rate→숨 소모 속도`, `Max Breath→최대 숨`,
  `Swim Boost (Alt.)→수영 강화(대체)`, `Underwater Breathing→수중 호흡`. 이런 스탯 블록이 또 나오면
  `term.py`로 라벨 하나씩 검색하지 말고 이 목록을 그대로 재사용할 것.
- 이 라벨 세트는 `translation_glossary.tsv`에는 없는 TM 관행이라 `qa_glossary.py`가 강제하지 않으니,
  직접 위 목록과 대조해 일관성을 유지해야 한다.
- 배치 0225에서 "Adult Poptop"을 "팝탑"으로 옮겨 고정 용어(Poptop→팝톱) 위반이 재발했다(id 80443) —
  `fix_<id>.json`으로 정정. 배치 0223에서 확정한 팝톱 표기를 다른 배치에서도 계속 놓치기쉬우니
  Poptop이 나올 때마다 `팝톱` 표기를 재확인할 것.
- 배치 0224에서 `qa_glossary.py` 고정 용어 위반 3건을 잡아 정정: `King Nutmidgeling`을 "넛미지링 왕"
  → "킹 넛밋지링", `Terrene Protectorate`를 "테레인 보호국" → "행성 보호국"(공식 바닐라번역), GIC
  환상향 계열 가구 5종(Kappa Bench 등)을 "카파" → "캇파"(요괴명 고정 표기)로 수정.
  단, id 80296 `K'Rakoth Codex Kappa`는 그리스 문자 카파를 가리키므로 "카파"를 그대로 유지 —
  이는 요괴명 Kappa와 문자열이 겹치는 의도된 예외이며, 이후 `qa_glossary.py` 기준선 오탐목록에
  `Kappa(1)`로 추가해 인식한다(그리스 문자 문맥에 한함, 요괴 문맥이면 즉시 정정 필요).
- 배치 0224에서 원문에 없는 `^reset;` 태그를 추가해 `tags` 불일치가 발생한 사례(id 80185, `^green;`/
  `^white;` 두 개만 있고 `^reset;`은 없는 원문) — `fix_<id>.json`으로 정정. 태그 관련 재발 방지 주의사항에
  해당 사례 추가.
- 배치 0223에서 `qa_glossary.py`가 새 고정 용어 후보 3건(`Portal(1)`, `Poptop(1)`, `Protectorate(1)`)을
  잡아냈다 — 각각 `포탈`→`포털`, `팝탑`→`팝톱`, `프로텍토레이트`(음역)→`보호국`으로 정정. 세 단어 모두
  흔히 직관적으로 다르게 옮기기 쉬운 고정 용어이므로 재발 방지를 위해 기록.
- 배치 0221에 RPG Growth 모드의 대형 변경 로그(id 79661, 51줄)가 포함되어 있었다 — 직업/스킬/UI 용어는
  기존 TM(테이머, 소멸 구체, 제어 호버, 진정한 이해, 다크 템플러 등)을 그대로 재사용했다.
- 배치 0221에서 "Energy Regeneration"을 "에너지 재생"이 아닌 "에너지 회복"으로 옮겨 `qa_glossary.py`의
  고정 용어(Regeneration→재생) 위반으로 걸렸다 — `fix_<id>.json`으로 정정. 상태 이름은 동의어로 바꾸지 말고
  고정 용어를 그대로 쓸 것.
- 배치 0218에서 원문에 개행이 있는 두 줄(id 78664, 78703)을 처음에 한 줄로 합쳐 번역해 `qa_structure.py`의
  `lines` 불일치로 걸렸다 — `fix_<id>.json`으로 원문과 같은 개행 수로 재병합해 정정.
- 배치 0219·0220에는 Lustling(성인 콘텐츠) 관련 노골적인 설명·의성어(id 78768, 78779, 79220, 79221,
  79277 등)가 포함되어 있으며, 기존 프로젝트 관례대로 완곡화 없이 원문 그대로 충실히 번역했다.
- 배치 0220에서 원문에 없는 `^reset;` 태그를 추가로 붙여 `qa_structure.py`의 `tags` 불일치로 걸린 사례(id
  79419)가 있었다 — 장식 태그는 원문에 있는 그대로만 옮기고 임의로 닫지 않도록 주의.
- 배치 0215에서 `Peacekeeper` 용어 첫 적용 시 `평화유지군`으로 오역했다가 `qa_glossary.py`가
  잡아내 `translation_glossary.tsv`의 고정 표기 `피스키퍼`로 즉시 정정(id 77832).
- 매 배치 병합 직후 `qa_structure.py`(태그/개행/입력 토큰 정합성) 0건, `qa_glossary.py`고정 용어
  후보를 기준선 `Miniknog(1)/Trink(1)/The Ruined(1)/Kappa(1)`(모두 기존에 알려진 오탐 — Kappa는 그리스
  문자 문맥의 K'Rakoth Codex Kappa)으로 확인하는 것을
  표준 절차로 삼는다. 새로 발견되는 고정 용어 위반은 즉시 `fix_<id>.json`으로 정정하고 재검사한다.
- 이 작업 전체에서 pak 재생성·`mods` 변경·서버 실행은 한 번도 하지 않았다.
- `2026-09-23` 세션에서 `new-translation` 배치 작업과 병행해 `style_worklist.tsv` 기반 기존 초안
  자연스러움 검수도 진행했다 (`DONE` 4,505 / `OK` 1,075 / `TODO` 1,235, 이후 배치 작업에밀려 보류).
  재개 방법은 위 "2026-09-23: 기존 초안 자연스러움 검수" 절 참고.
| 0639 | 56 | 저항 라벨·크레딧 블록 | PASS(기존 후보 4) |
| 0640 | 51 | 저항/기계 라벨 + NL 대화 | PASS(기존 후보 4) |
| 0641 | 57 | NL 대화·총기명·기계 설명 | PASS(기존 후보 4) |
| 0642 | 55 | NL 대화·총기명 | PASS(기존 후보 4) |
| 0643 | 51 | NL 대화·총기명 계속 | PASS(기존 후보 4) |
| 0644 | 55 | 바닐라 감상문·UI 라벨(기존 번역 재사용) | PASS(기존 후보 4) |
| 0645 | 55 | 바닐라 감상문·UI(기존 번역 재사용) | PASS(기존 후보 4) |
| 0646 | 55 | 바닐라 감상문 계속(기존 번역 재사용) | PASS(기존 후보 4) |
| 0647 | 55 | 바닐라 감상문 계속(기존 번역 재사용·피스키퍼 정정) | PASS(기존 후보 4) |
| 0648 | 55 | 바닐라 감상문 계속(기존 번역 재사용) | PASS(기존 후보 4) |
| 0649 | 55 | FU 유머 감상문(신규 번역) | PASS(기존 후보 4) |
| 0650 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0651 | 55 | FU 감상문(신규·아키마리 정정) | PASS(기존 후보 4) |
| 0652 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0653 | 55 | FU 감상문(신규·텔리안/크랄 음차) | PASS(기존 후보 4) |
| 0654 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0655 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0656 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0657 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0658 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0659 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0660 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0661 | 55 | 행성 핀·FU 감상문(신규·볼티지 정정) | PASS(기존 후보 4) |
| 0662 | 55 | 행성 핀·FU 감상문(신규) | PASS(기존 후보 4) |
| 0663 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0664 | 55 | 인형·FU 감상문(신규) | PASS(기존 후보 4) |
| 0665 | 55 | FU 감상문(신규·포털 정정) | PASS(기존 후보 4) |
| 0666 | 55 | FU 감상문(신규) | PASS(기존 후보 4) |
| 0667 | 55 | FU 감상문(신규) | PASS |
| 0668 | 55 | FU 감상문(신규+기존 재사용) | PASS |
| 0669 | 55 | FU 감상문(신규) | PASS(팝톱 정정) |
| 0670 | 55 | FU 감상문(신규) | PASS |
| 0671 | 55 | FU 감상문(신규) | PASS(하이로틀 정정) |
| 0672 | 55 | FU 감상문(신규) | PASS |
| 0673 | 55 | FU 감상문(신규) | PASS(브할레이한 정정) |
| 0674 | 55 | FU 감상문(신규, 샌드 크롤러 표기 통일) | PASS |
| 0675 | 55 | FU 감상문(신규) | PASS |
| 0676 | 55 | FU 감상문(신규) | PASS |
| 0677 | 55 | FU 감상문(신규, 필멸자 용어 정정) | PASS |
| 0678 | 55 | FU 감상문(신규) | PASS |
| 0679 | 55 | FU 감상문(신규) | PASS |
| 0680 | 55 | FU 감상문(신규) | PASS |
| 0681 | 55 | FU 감상문(신규) | PASS(개행 보정) |
| 0682 | 55 | FU 감상문(신규) | PASS |
| 0683 | 55 | FU 감상문(신규) | PASS |
| 0684 | 55 | FU 감상문(신규) | PASS |
| 0685 | 55 | FU 감상문(신규) | PASS |
| 0686 | 55 | FU 감상문(신규) | PASS |
| 0687 | 55 | FU 감상문(신규) | PASS |
| 0688 | 55 | FU 감상문(신규) | PASS |
| 0689 | 55 | FU 감상문(신규) | PASS |
| 0690 | 55 | FU 감상문(신규) | PASS |
| 0691 | 55 | FU 감상문(신규) | PASS |
| 0692 | 55 | FU 감상문(신규) | PASS |
| 0693 | 55 | FU 감상문(신규) | PASS |
| 0694 | 55 | FU 감상문(신규) | PASS |
| 0695 | 55 | FU 감상문(신규) | PASS |
| 0696 | 55 | FU 감상문(신규) | PASS(테크 카드 정정) |
| 0697 | 55 | FU 감상문(신규) | PASS |
| 0698 | 55 | FU 감상문(신규) | PASS |
| 0699 | 55 | FU 감상문(신규) | PASS |
| 0700 | 55 | FU 감상문(신규) | PASS |
| 0701 | 55 | FU 감상문(신규) | PASS |
| 0702 | 55 | FU 감상문(신규) | PASS |
| 0703 | 55 | FU 감상문(신규) | PASS |
| 0704 | 55 | FU 감상문(신규) | PASS |
| 0705 | 55 | FU 감상문(신규) | PASS |
| 0706 | 55 | FU 감상문(신규) | PASS |
| 0707 | 55 | FU 감상문(신규) | PASS |
| 0708 | 55 | FU 감상문(오카서스 정정 포함) | PASS |
| 0709 | 55 | FU 감상문+아이템명(신규) | PASS |
| 0710 | 55 | FU 감상문+아이템명(치명타 피해 정정) | PASS |
| 0711 | 55 | 감상문+Arcana 변경로그 대형코덱스 | PASS |
| 0712 | 55 | 보스 소환+에지 NPC명 | PASS |
| 0713 | 55 | 감상문+유물 재구축 설명 | PASS |
| 0714 | 55 | FU 감상문(신규) | PASS |
| 0715 | 55 | FU 감상문(신규) | PASS |
| 0716 | 55 | 아키마리 감상문(하이픈 화법) | PASS |
| 0717 | 55 | 아키마리 감상문 계속 | PASS |
| 0718 | 55 | 아키마리 감상문 계속 | PASS |
| 0719 | 55 | 아키마리 감상문+아이템명 | PASS |
| 0720 | 55 | 외계인 감상문 시리즈 | PASS |
| 0721 | 55 | 감상문+얼라이언스 명명 | PASS |
| 0722 | 55 | 알타 NPC 명명(듀라스틸 정정) | PASS |
| 0723 | 55 | 알타 NPC 명명 계속 | PASS |
| 0724 | 55 | 알타 NPC 명명(바이올륨 정정) | PASS |
| 0725 | 55 | FU 감상문(신규) | PASS |
| 0726 | 59 | NL 미션 대사+총기명 | PASS |
| 0727 | 80 | NL 미션 대사+총기명 | PASS |
| 0728 | 11 | NL 미션 대사 | PASS |
| 0729 | 57 | NL 미션 대사+총기명 | PASS |
| 0730 | 57 | NL 대사+코덱스(알파카 민요, 버즈, 목록) | PASS |

0731 | 50 | Arcana docs, trap-guide codex ch1-5, spawners, misc | pass
0732 | 57 | codex pages (Diet/Behaviour, trap-guide intro, Irisil lore), spawners, misc | Cosmic Dragon->우주 드래곤 fixed | pass
0733 | 57 | Irisil licensing/history, reincarnation codex, rebel cell reports, spawners | Protectorate->보호국 fixed | pass
0734 | 57 | Viera/Eithne codex lore, experiment logs, credits, colony deeds | pass
0735 | 57 | Viera codex lore, commandments w/ U+E024 glyphs, microformers | pass
0736 | 57 | microformers, wordbank nouns, Space Pit flyer | pass
0737 | 57 | wordbank nouns, race-trait stat block, misc | pass
0738 | 57 | wordbank nouns, codex continuations, Ruined dialogue | pass
0739 | 57 | wordbank verbs/nouns, codex fragments, gremlin stats | Teleporter->텔레포터 fixed | pass
0740 | 57 | wordbank verbs/names, race stat blocks, codex fragments | Knockback->넉백 fixed | pass
0741 | 57 | 'the X' epithets, pokemon stat blocks, book descriptions | pass
0742 | 57 | verbs, diary entries; code parameter rows kept verbatim | pass
0743 | 57 | tentacle quest labels, RU/ZH weapon descriptions, glitch amazements | pass
0744 | 50 | non-desc low-pri: perk labels, amulets, ancient item names, stat blocks | pass
0745 | 55 | non-desc low-pri: subtitles, titles, Arborwood color names, misc | pass
0746 | 56 | Arcana collection/star names, Arctic names, arena battles, reset prompts | pass
0747 | 55 | Ark-of-X subtitles, Armor Up titles, gear labels, Asirai set | pass
0748 | 55 | Astral/Aurea sets, Asteria book titles, misc names/labels | pass
0749 | 55 | Avikan NPC titles, Avian titles | pass
0750 | 55 | alkey names, BRZRK labels, Avolite, misc | pass
0751 | 55 | perk labels, bio items, bird color names, alkey names | pass
0752 | 55 | Bishyn/Bird names, blood/buff labels, skill names | pass
0753 | 55 | skill/label names, Arcana guide values, misc | pass
0754 | 55 | burning/burst names, buy subtitles, misc | pass
0755 | 55 | CH adult-category names, alkey names, misc | pass
0756 | 55 | monster card names, alkey names, perk labels | pass
0757 | 55 | monster card names 035-089 | pass
0758 | 55 | monster card names 090-144 | pass
0759 | 55 | monster card names 145-199 | pass
0760 | 55 | monster card names 200-220, Ceterai titles, misc | pass
0761 | 55 | chaos/charge names, chat sound labels, misc | pass
0762 | 55 | resistance labels, chrono names, misc | pass
0763 | 55 | coil/bird color names, chill immunity labels, misc | pass
0764 | 55 | cosmic names, station titles, perk labels | pass
0765 | 55 | crew bonus labels, crit labels, crow names | pass
0766 | 55 | cryo/crystal names, Kappa trait labels, augment labels | pass
0767 | 55 | Dark metal material names | pass
0768 | 55 | Deep metal names, dazed tool skins, misc | pass
0769 | 55 | Deep metals cont., boss defeat quest values | pass
0770 | 55 | Delpha weapons, demon skills, desert NPCs, relic slot info | pass
0771 | 55 | dossier titles, Droden NPCs, Harrowing event desc | pass
0772 | 55 | EDS android series, EP music stage names | pass
0773 | 55 | Earthen colors, trap design codex titles, eldritch skills | pass
0774 | 55 | elemental skills, Elerune/Elin, emergency labels | pass
0775 | 55 | energy augment/skill labels, engineer titles | pass
0776 | 55 | Era weapon subs, Erchius, misc titles | pass
0777 | 55 | explosive skills, extraction missions, [EWS] labels | pass
0778 | 55 | Fate status labels, Faradea NPCs, fast rockets | pass
0779 | 55 | Fate cont., Fin color names, boss fight prompts | pass
0780 | 55 | enemy location values, Fine materials, flame skills | pass
0781 | 55 | Floran NPCs, food processor blueprints, misc | pass
0782 | 55 | Forge of Stars tiers, foundry NPCs, misc subs | pass
0783 | 55 | Frog color names, frost skills, misc | pass
0784 | 55 | GEG star titles, Gauss weapons, Ghearun NPCs | pass
0785 | 55 | Glowing dye series, Glitch NPCs, ghoul status | pass
0786 | 55 | Glowing dyes Light series, misc labels | pass
0787 | 55 | gravity skills, Grenadier Assault 12 variants | pass
0788 | 55 | gun titles, hachimaki, hazards status block | pass
0789 | 55 | healing/health augments, heavy weapons, Hevika | pass
0790 | 55 | Hevika NPCs, Hohei '60 series, holy skills | pass
0791 | 55 | Horizon NPCs, Hylotl titles, humiliation labels | pass
0792 | 55 | Hyperborean weapons, ice skills, debug strings | pass
0793 | 55 | Imperial Army/Navy labels, imbued statuses | pass
0794 | 55 | Intense colors, Into the Breach series, ion skills | pass
0795 | 55 | ionic skills, mod warnings, job armor patterns | pass
0796 | 55 | Key of X series, Kappa repair kit, misc | pass
0797 | 55 | Landing Festival NPCs, kunai skills, misc | pass
0798 | 55 | Leaf colors, Light metals start | pass
0799 | 55 | Light metal names cont., light augments | pass
0800 | 55 | Light metals end, Load ammo series, Lion packages | pass
0801 | 55 | Log series, Lost artifacts, misc | pass
0802 | 55 | Lustling history titles, MKI/MK series | pass
0803 | 55 | Magicite stations, Magatama labels, misc subs | pass
0804 | 55 | Marpesia chapters, mech parts, marked statuses | pass
0805 | 55 | Medium metal names | pass
0806 | 55 | Medium metals end, Miko armor labels, Metal colors | pass
0807 | 55 | Miniknog titles, Modern stations, misc | pass
0808 | 55 | Mycotoxin labels, NPC titles, glyph subtitle | pass
0809 | 55 | Neki pod labels, misc titles | pass
0810 | 55 | Nock arrows, Nova colors, Nomada | pass
0811 | 55 | Old metal materials, Occasus, misc | pass
0812 | 55 | Origins of the Wood, Outlaw NPCs, augments | pass
0813 | 55 | Pacific Bulwark variants, Partner types, misc | pass
0814 | 55 | Pattern blueprints, Penguin NPCs, patches | pass
0815 | 55 | Personal Guards 12 variants, Phox Hymn, phase skills | pass
0816 | 55 | plasma skills, forge upgrade guide values | pass
0817 | 55 | poison skills, Position slots, Prime alkeys | pass
0818 | 55 | Prisoners series, Profession values, Protectorate colors | pass
0819 | 55 | psionic/pulse skills, reputation tiers | pass
0820 | 55 | radiation labels, rally/RSR, rainbow NPCs | pass
0821 | 55 | Reb. weapon variants, rejection reaction labels | pass
0822 | 55 | Reminisce quest titles, repulse bosses, tool skins | pass
0823 | 55 | Rhadeis parts, Rhaiod ranks, resting/reloading labels | pass
0824 | 55 | Royal Assault labels, simulation entries, Salamandra series | pass
0825 | 55 | Saturnian titles, Scava alkeys, scavenger/scientist | pass
0826 | 55 | Seifuku quotes, teabag buffs, shop subtitles, perk guide | pass
0827 | 55 | Sells subtitles, Senninbari labels, sewer/adult titles | pass
0828 | 55 | Shadow/Shellguard color series, sexbound titles, shield labels | pass
0829 | 55 | Shock/Sinara/Singularity names, skill values, shrine labels | pass
0830 | 55 | Sky/slime/smart weapon series, snow NPCs, Solalei | pass
0831 | 55 | Solar/Sona/Soul/Space series, Spears of Vas Vha'leih | pass
0832 | 55 | Spectre Boon series, spell/staff/star names | pass
0833 | 55 | Stardust series, NL24 stat block, static/steel/stellar | pass
0834 | 55 | Stem colors, storm/stun names, stress reaction | pass
0835 | 55 | Summon/super/supply names, suspicious mushroom series | pass
0836 | 55 | Talisman/tank labels, tea makers, tactical names | pass
0837 | 55 | Tech Docs/Tengu Synchronization series, Telebrium, tepid | pass
0838 | 55 | Terminal subtitles, Tesla, The X titles | pass
0839 | 55 | The Fox armor labels, The X codex titles, Landing Festival | pass
0840 | 55 | Marpesia/Seonha sagas, The X titles, Arcanium guide | pass
0841 | 55 | Thorn/tidal/time names, Titancorp, Thelean NPCs | pass
0842 | 55 | Toggle Actor series, Tokubetsu Rikusentai, Tori colors | pass
0843 | 55 | Toxic immunity series, Triage Kit, Trapped in Caves | pass
0844 | 55 | Trink NPC series, turret operators, USCM entries | pass
0845 | 55 | Ultima/Unbound/Undying series, underbarrel parts | pass
0846 | 55 | Vaash/Varda/vanilla/vehicle series, corrupted row kept | pass
0847 | 55 | Viera crafting titles, Viona alkeys, Viridis names | pass
0848 | 55 | Void series, visit quest objectives, warp names | pass
0849 | 55 | Wave/Welcome titles, elemental placeholders, crafting guides | pass
0850 | 55 | White/wood/wizard names, wolf blood, woof titles | pass
0851 | 55 | X'i/Xithricite/Yaara/Yava series, misc You-X messages | pass
0852 | 55 | hex-tagged weapon presets, GIC:E labels, Arcana guides | pass
0853 | 55 | hex-tagged station titles, Delamain shop, glyph row | pass
0854 | 55 | cyberpsycosis guide, weapon warning labels, colored titles | pass
0855 | 55 | HUMAN/YOKAI missions, cyberware skeleton labels | pass
0856 | 55 | alta station subtitles, EDS labels, mission titles | pass
0857 | 55 | alta subtitles, UI labels, hat morph glyph row | pass
0858 | 55 | slot instructions, colored titles, encyclopedia glyph | pass
0859 | 55 | TIER glyph labels, FU Guide series, misc titles | pass
0860 | 55 | blue-tagged weapon categories, madness labels, class titles | pass
0861 | 55 | augment stat customlabels series | pass
0862 | 55 | augment stat labels continued | pass
0863 | 55 | augment stat labels continued | pass
0864 | 55 | augment stat/immunity labels | pass
0865 | 55 | augment immunity/module labels | pass
0866 | 55 | augment immunity/swim/EDS labels | pass
0867 | 55 | green quest titles, arena/delivery names | pass
0868 | 55 | Catching the X bug quest titles | pass
0869 | 55 | Cooking/Digging/Delivery quest titles | pass
0870 | 55 | quest titles E-H | pass
0871 | 55 | quest titles H-O | pass
0872 | 55 | quest titles P-S | pass
0873 | 55 | quest titles S-T | pass
0874 | 55 | quest titles T + Chap.1-3 | pass
0875 | 55 | chapters, mage titles, alta categories | pass
0876 | 55 | alta stations + orange quest titles A | pass
0877 | 55 | orange weapon categories + quest titles A-D | pass
0878 | 55 | dungeons + orange weapon categories | pass
0879 | 55 | orange quest titles I-R, artifact legends | pass
0880 | 55 | recollections + relic guide + weapon categories | pass
0881 | 55 | orange titles end + red stat labels | pass
0882 | 55 | red status labels + FFS titles | pass
0883 | 55 | FFS titles + status labels | pass
0884 | 55 | status labels end + shadow UI | pass
0885 | 55 | shadow UI + white stations | pass
0886 | 55 | yellow categories + internal names | pass
0887 | 37 | FINAL - internal names, JSON, codex titles, CJK | pass
REVIEW | 29 | sexbound euphemism/mistranslation fixes (그곳/물건/거기→보지·자지, 고양이오역, 정→정액, 정육→떡감) | pass
REVIEW | 41 | sxb addons: knot verb, whip names unification, brothel 매음굴, lewd grammar | pass
REVIEW | 51 | arcana: 엑수시아/아르카니움 통일, slash skills, workstation, +3 untranslated | pass
REVIEW | 1 | elithian: +Medical Supplies | pass
REVIEW | 1 | enternia: +Energy Aura | pass
REVIEW | 1 | krakoth: +vehicle warning | pass
REVIEW | 10 | small mods: starburst+felin+avali+woof residuals | pass
FU | 44 | fu non-desc adds (withdraw/kiros/mission/lore/kevin diary) | pass
REPAIR | 48 | multiline TSV corruption repair: 0102×14(json), 0779×2(json), 0134×13, 0142×6, 0154×13, 0745×3 tails | pass
REPAIR | 22 | dup adds removed (0751/0768/0778/0779 originals kept), 5 dup rows deduped in 0154 | pass
0888 | 41 | review-fill: small mods residuals (floran/glitch chatter, armour labels, revisit buttons) | pass
| 2026-09-27 | APPLY | - | female_translation.pak 생성·적용 완료 (58.5MB, 34,326 패치 파일/174,095 op). .patch 자산 리팩: 169 pak 재패킹, 33,172 스팬 편집, 실패 0. 구 localeko_rest.pak → backup_paks 이동.
| 2026-09-27 | MOD | - | female_overhaul 생성 (mods/zz_female_overhaul.pak, 47 파일). 비-번역 로컬 수정 통합: fu_copperarmor_price_fix·zz_modfix_refs·999999200_ffxiv_viera_blueprint_compat 흡수(원본→E:\Desktop\mods\replaced-installed-20260922\female_overhaul-absorbed). gic_4_3_compat_fixes는 로드 슬롯 충돌로 별도 유지. compat pak 13종은 구워진 수정이라유지+manifest 문서화. 파일명 zz_ 프리픽스로 기존 후반 로드 슬롯 유지.
| 2026-09-27 | MERGE | - | female_translation 통합: sbkor(5,955p)+FU_KO(14,225p)+localeko legacy 3종(6,614p)+zz_localeko_postload(12p) 병합 → 58,980 엔트리/77.7MB. op그룹 순서=legacy→ft→postload→sbkor→fuko (인간 번역 우선). 대소문자 경로 10쌍+디렉터리 케이스 충돌 해결 위해 커스텀 pak writer(build_pak.py)로 INDEX 직접 생성 — 케이스 보존·공식 unpacker 검증 통과. sbkor 비표준 JSON 2파일 원문 그대로 포함. 원본 pak 6종→female_translation-merged\ 이동.
| 2026-09-26 | MOVE | - | 문서·산출물 정리: 작업 폴더 tmp/ → translation/ 이동(스크립트·TSV·문서 경로 갱신, parents[1] 기준 ROOT 유지). 인계 문서 분리: 루트 유지보수 문서 1~17절유지, 번역 이력(구 18~35절)+현황 → translation/HANDOFF.md. 용어집 정본 → translation/STARBOUND_KO_GLOSSARY.md. 재패킹 백업 tmp/replaced-installed-20260922 → translation/ 하(E:\Desktop\mods는 현재 없음, 이 사본이 유일).
| 2026-09-26 | QA-NOTE | - | qa_structure 0건. qa_glossary 신규 후보 64건/139행(최근 배치 0742~0888 구간 미소거): 실위반 다수 포함(제작대→제작 스테이션, 찌르기 피해→관통 피해, 패링→패리, 브로드소드→대검, 돌격소총→어설트, 루인킬러→루인 킬러 등) + 오탐(아이템 ID 내 codex 등). TSV만 수정하면 게임 반영 안 됨 — 재적용 필요.
| 2026-09-29 | NAMES | - | 명칭 통일 자동 패스(퀘스트↔아이템·지명·NPC 명칭): all_pairs 378k → EN이름 레지스트리(canon_overrides 수동 정본) → align_diff 스캐너 13,707 제안 → 자동 승인 WORD/TSPAN/VARIANT만 체인 적용. 결과: 1,189 포인터/931 패치 파일, 다중명칭 체인 69, 방법별 WORD 692·TSPAN 411·VARIANT 85·MANUAL 1(안드로스 갈바넥 사령관 직함 접미 통일). 소스 pak: female 891·FU_KO 279·sbkor 18 → female pak에 같은 경로로 덮어씀. struct+verify 불일치 0. QA: pak_pairs_pending 185,378쌍, qa_pak_glossary 위반 0, qa_pak_context 신규 플래그 0(STYLE_MIX 4200→4173, DUP_PARTICLE 734→730). 서버 부팅 정상(전 DB 로드·포트 21025·에러 0). 보호 규칙: 스탯라벨(+120류)·수량(2개)·리스트항목(,·/)·복수일반명사(들)·1음절토큰·직책접미(관장령사왕님) 중복 거부, ^reset; 밖 텍스트 미매칭, 태그span은 dice 최대 유사 span 선택, 조사 자동 복구+은(는) 듀얼 표기. 잔여 수동 대기: REVIEW 8,250·AMBVAR 723·VNONE 22·JUNKCANON 337(정본이 문장형인 케이스). 배포: mods/female_translation.pak 교체(구본 deployed-bak 보존).
| 2026-09-29 | NAMES-2 | - | 명칭 통일 2차(잔여 큐 트리아지): REVIEW 승인 이름 21종(채굴 레이저·에르키우스 수정·태양광 패널·작살 총·비날리제이·피스키퍼 스테이션 등), AMBVAR→VARIANT 승격(유사도≥0.7 비증식 변형 134건 + 수동검증 11종), extra_variants.tsv 신설(레지스트리 미등록 전사 변형 39쌍: 페글라치→페글라시, 모파이트→몰파이트, 익서크레이션·엑서크레이션 등→엑세크레이션), 문장형 정본은 스캔 단계에서 억제(JUNKCANON 337→2), 수동 치환 manual_name_fixes 10건(안드로스 갈바넥 사령관·로저 레파로·팝탑→팝톱·쇼고스→쇼고트·갑옷 제작소→방어구 제작·자동 쓰레기통→자동 폐기). 추가 승인 2라운드(Poptop 팝톱·Shoggoth 쇼고트·Plasma Rifle·Moontant 등 22종)+VARIANT 반복치환(한 포인터 내 이중 발생). 최종 적용 1,752 포인터/1,241 패치 파일(VARIANT 609·WORD 715·TSPAN 418·MANUAL 10), 체인 78, verify 0. QA: glossary 0, context 신규 0(STYLE_MIX 4200→4167·DUP_PARTICLE 734→726·LITERAL 173→171). 서버 재부팅 정상. 거부 잔여: REVIEW 7,995·AMBVAR 181·VNONE 22 — 대부분 정당한 거부(일반어/문맥 의존). 배포 pak 갱신 완료.
| 2026-09-29 | NAMES-3 | - | 명칭 통일 3차(사용자 정본 보정 + 음차 우선 재조정): /monsters/ 클래스 순위 추가 + resolve_target이 오버라이드/용어집고정 시 AMB 경로해소 우회하던 버그 수정 + 이름 정의필드 자체도 변형이면 DEF 플래그로 통일(53종 함선 사물함 오브젝트명 등). 정본 교정: Shoggoth 쇼고트→쇼고스(몬스터 정의 우선, 러브크래프트 전사), The Curious Glitch 결함→글리치(종족명), Microsphere→마이크로스피어, Hive→하이브, Coffee Machine→커피 머신, Erchius Horror→에르키우스 호러, Fatal Circuit→페이탈 서킷, Ocean Surprise→오션 서프라이즈, Clipped Council→클립드 의회, Kluex Sentry→클루엑스 센트리, Solarium Star→솔라리움 스타, Crystal Erchius Fuel→크리스탈 에르키우스 연료, Clay→점토(진흙=mud 오역), Engineer→엔지니어, Oculemonade→오큘레모네이드, Claw Glove→클로우 글러브, Crystal Plant→크리스탈 식물, Grabber→그래버, Incubator→인큐베이터, Ironbeak→아이언비크, Lantern Stick→랜턴 스틱, Master Manipulator→마스터 매니퓰레이터, Mining Drone→채굴 드론, Mother Poptop→마더 팝톱, Salvaged Nano Receptacle→노획한 나노 리셉터클, Ship Door→함선 문, Solus Katana→솔루스 카타나, Timber→목재, Wraith→레이스, Yeti→예티. Incubator/Yum yum은 ambvar 승인 해제(실체 상이/종족 말투). sweep_canon_variants.py 신설: EN미포함 문자열·복합명 내부 변형까지 팩 전체 스윕(미니 쇼고트, 쇼고트 부식, 무타-문턴트, 선박 사물함입니다 등), 변형-내포-정본 재매칭 방지(정본 마스킹), 쌍용 조사 폴백, 노획한 노획한 이중접두 복구. variant_replace에도 정본 마스킹 추가(체인 이중 접두 버그 수정). 적용 1,858 포인터/1,333 패치 파일 + 스윕 251op/86 자산. QA: 추출 284,953쌍(bare-replace op 포함으로 확장), glossary 위반 0, context 신규 플래그 0(기존 대비 44건 해소). 서버 부팅 정상(전 DB·21025·에러 0). 배포 완료. 잔여: REVIEW 7,894·AMBVAR 91·VNONE 21.
| 2026-09-29 | NAMES-4 | - | 명칭 통일 4차(잔여 큐 완전 소진): REVIEW 7,894·AMBVAR 91·VNONE 21 전량 재트리아지. 정본 오버라이드 +2(Monolith→모놀리스, Burrower→버로우어 — 기존 정본 '하나로 된 돌'/'벌레랑'은 오역). extra_variants +48쌍(전사 변형), sweep 목록 +95종. 수동 치환 +29행: Expanse 바이옴 11종(뼈 육체/세포/썩은 살점/에르키우스 수정/에테르 에르키우스/크리스탈린 → ~익스팬스 — FU 원본 friendlyName이 전부 '~ Expanse'임을 확인), 제작 UI 타이틀 무기와 방어구들 통일 14행, Apex War-Born 정점 전쟁의 탄생→에이펙스 워본(퀘스트 본문-타이틀 불일치 해소), 에이펙스 피·약간의 오해·읽기 자료·아머 스피어·아머 업 등. 결과: 2,268 포인터/1,597 패치(VARIANT 1,094·WORD 711·TSPAN 412·MANUAL 51), 스윕 +148op, verify 0. 경계 확장: 용·형·들·인가(아펙스용 도끼, 아비터형 드론, 콘키스타도르들, 페녹스인가 커버). 의도적 차단 유지: 나이트미스트·데트리투스·스트래퍼·스킴버스·스노아펙스·휴먼쉽·메카라크니드(복합명), 그렉/그레가(Greg 의태어 — 정본 아님), 벌레랑(일반어), 슈정(플로란 말투), 조류/대위/선봉대(문맥 변형). 스윕 최적화: substring 선검사로 ~40배 가속. QA: 추출 283,525쌍, glossary 위반 0, context 신규 플래그 0(기존 대비 51건 해소). 서버 부팅 정상(21025 리슨·에러 0). 배포: mods/female_translation.pak 교체(구본 deployed-bak).
| 2026-09-29 | NAMES-5 | - | 명칭 통일 5차(name_conflicts 2,495행 전수 트리아지): 같은 EN 명칭에 복수 KO 표기 충돌 — 전체 필드가 변형 문자열과 정확히 일치하는 순수 명칭 필드만 자동 통일(1,109 포인터). 모호 변형 10종은 자산별 EN 조회로 개별 해결(조그마한 집→Tiny House/Tiny Flats 분기, 우주 폭발→Cosmic Blast/Burst 구분(블래스트/버스트), 넓은 항아리→Urn/Clay Pot 구분, 작은 벽 스위치→Small/Tiny 구분, 창문 격자→Aen/일반 구분, 엘더 벽돌→Brickwork/Bricks 구분, 회로 제작기→Constructor/Fabricator 구분). 정본 오버라이드 +9: Ocu Cannon→오큘 캐논(오큘 표준), Quietus Pistol→콰이어투스 권총, Zerchesium Sniper Rifle→제르세슘 스나이퍼 라이플(저체슘 오기), Irradium Whip→이리듐 채찍, Nomad Rifle→노마드 라이플, X'ian Bulb Gun→짜'이족 벌브 건, Sting Needler→스팅 니들러, Auto Trash→자동 쓰레기(아이템명과 GUI 타이틀 통일), Cosmic Blast→코스믹 블래스트. **지옥불→인페르노 오스윕 복구**: 지옥불은 Hellfire 시리즈 확립 정본(48건)인데 인페르노로 잘못 스윕한 것을 포인터 한정 복구(48행) + 스윕 규칙 제거. 정점→에이펙스 수동 8행(apexlostsoul·apexbrainmutant·스노우헤드·배경 문·유물 제단·로코코 커튼의 에이펙스 종족 참조; 일반어 pinnacle 용법은 유지). 버그 수정: nested batch op 처리(apply 크래시), MANUAL 치환값 공백-only 시 strip으로 스킵되던 버그, 수동 치환 파일 롤백으로 유실된 복구 행 48건 재추가. 결과: 3,444 포인터/2,656 패치 파일 적용, verify 불일치 0, 이중 공백 명칭 8건 정리(제르세슘 시리즈·약한 재생 II·수직 나무 판자). QA: 추출 279,937쌍, glossary 위반 0, context 신규 플래그 0(171/724/51/18 — 이전과 동일). 서버 부팅 정상(전 DB 로드·21025 리슨·에러 0). 배포: mods/female_translation.pak 교체(구본 deployed-bak). 잔여 충돌 ~1,096은 전부 프로즈 내부 발생 또는 다른 이름의 정본 문자열이라 추가 조치 없음.
| 2026-09-29 | NAMES-6 | - | 명칭 통일 5.5차(충돌 잔여·오스팬 복구): 프로즈 내부 변형 재집계 — 실잔여 3종만 존재. ① trinkcrafting st2 Circuit Fabricator=회로 제작기 확인(정상), weaponrestorationtrink2 퀘스트 'at a Circuit Fabricator'가 '프라임 회로 제작기에서'로 오역된 것 수정(프라임은 회로명이 아닌 재구축 대상 Prime Circuit임 — '프라임 회로를 재구축하는 첫 단계는 회로 제작기에서'로 정정). 단 TSPAN이 회로 제작기 안의 '회로'를 '프라임 회로'로 잘못 확장 재삽입하던 것을, 수동 치환 결과에 정본 '프라임 회로'를 선배치해 TSPAN을 스킵시키는 방식으로 해결. ② microspherebomb 퀘스트 '마이크로 스피어'(공백 변형)→마이크로스피어. ③ '디스토션 구'(구체 탈락) 4포인터→디스토션 구체(armorsphere/microsphere 퀘스트·bomb 아이템 설명). 결과: 3,450 포인터/2,667 패치, verify 0, glossary 0, context 동일(171/724/51/18). 서버 부팅 정상(21025·에러 0). 배포 완료.
| 2026-09-29 | NAMES-7 | - | 잔여 큐 완전 소진 + 정본 무결성 감사: ① Sapling 정본을 '어린 나무'→'묘목'으로 교정(묘목 607 vs 어린 나무 7 우세·전 Alta 묘목 계열이 묘목 사용) — 카테고리 라벨·Sapling·Unsmashable Sapling·smalltree1-3 EN명 확인 후 6포인터 통일. ② manual_name_fixes 역방향 구형 행 감사: 정본→변형으로 되돌리는 stale 행 5건 제거(smalltree 3건·erchiushorrorAF '호러→공포' 2건 — 호러 정본과 역행하던 것). ③ 에르키우스 호러 계열 정본 보정: 'The Erchius Horror'·'Erchius Horror Figurine'의 공포 표기를 호러로 통일(스티커/몬스터와 일치). ④ 유령 패치 자산 제거(존재하지 않는 /objects/throwable/unsmashablesapling 경로에 생성됐던 빈 패치). ⑤ 부팅 검증 교훈: win64\starbound_server.exe는 바닐라 바이너리로 이 모드 구성의 JSONC 자산을 파싱하지 못해 v-balllightning 등에서 크래시 — 실제 설치된 서버는 win\starbound_server.exe(OpenSB, 9/29 갱신). win64판으로는 이전 배포본도 동일 크래시 재현돼 우리 pak 무관 확인. OpenSB 서버로 부팅 시 에러 0·21025 리슨 확인. 결과: 3,454 포인터, verify 0, glossary 0, context 동일(171/724/51/18). 배포 완료.
| 2026-09-29 | NAMES-8 | - | 명칭 통일 6차(name_refs_missing 큐 소진): EN이름이 프로즈에 참조됐는데 KO 정본이 없는 참조 12,522건 중 퀘스트 1,036건 우선 — 실효값 재계산으로 stale 행 걸러내고 실제 불일치만 수동 치환(총 ~240행). 스테이션 통일: 채집 테이블(먹이/수렵)·연금술대(연금술 테이블)·발아 테이블(싹이 트는)·함선 부품 조립기·시프터(체/선별기)·핵분열 용광로(Fission Reactor=원자력 반응로와 명칭 충돌 해소)·전력 스테이션·전자공학 시설·모닥불. 아이템: 행성 핵 파편·은/금/프로토사이트 주괴·꿀 항아리·벌레잡이 그물·사마귀초·고대 리모컨·골분·플라스믹 수정·연구소 카탈로그·조잡한 승무원 침대·페로슘 클리버·브할레이한 창·월 점프. 음차 우선(사용자 지침): Busty Bonka→버스티 봉카(직역 '가슴 큰 봉카' 정본 교체·육감적인 봉카 변형도 통일), Precursor Microsphere→선구자 마이크로스피어. 미션: RAID Behemoth Train→베히모스 열차(거수 열차), Seeker Trial→시커 시련(추격자/탐구자 변형 — Seeker 인명 '시커'와 통일), Stealth Tech→은신 테크, Teleport Dash→블링크 대시 II, Repulsor Blast→반발 폭발. 2차 73행 배치: 세테난 오쿨루스·식당 의자/탁자·고대 차원문·엘리트 드랄·최고급 카바나이트 판금·투척 창·사냥용 라이플·핸드 밀·텅스텐 주괴·무기고·요오드화 메틸·우유(젖 오역) 등. 파이프라인: MANUAL 전용 그룹에 struct_ok 태그 변경 허용(^orange 태그 복구 '주황색 X^reset;'→'^orange;X^reset;' 9건 적용), 대문자 CRAFTING/ 경로 복제 패치 동기화. 정본 오버라이드 +9종. 결과: 3,624 포인터/2,769 패치 파일, verify 불일치 0, glossary 위반 0, context 플래그 동일(171/724/51/18). 미싱 잔여 333건→전수 재확인 결과 전부 일반어(well/Return/Captain/ruins 등)·의도적 문맥 의역·다른 레이어 자산 — 추가 조치 대상 없음. 서버 부팅 정상(win\starbound_server.exe OpenSB·21025 리슨). 배포: mods/female_translation.pak 교체(deployed-bak 보존).
| 2026-09-29 | NAMES-9 | - | Flutter Jump 음차 통일(사용자 지적): 파닥파닥 점프→플러터 점프 — FU longjump2/3/4 테크·아이템·퀘스트(I/II, 울트라 플러터! = EN Ultra Flutter!), gravityjump 설명 메가 강도 플러터 점프, 총 12포인터 수동 치환. 새터니안 플러터(기존 음차)와 통일, saloondoor의 '파닥거릴'은 일반어 문학 표현이라 유지. 정본 오버라이드 +2(Flutter Jump→플러터 점프, Ultra Flutter!→울트라 플러터!). 결과: 3,636 포인터, verify 0, glossary 0. OpenSB 서버 부팅 정상(21025). 배포 완료.
| 2026-09-29 | MT-STYLE | - | 기계번역체 전수 스캔 + 확정 오류 교정(qa_mt_style.py 신설 — pak_pairs.tsv 279,703쌍 대상 자연스러움 휴리스틱 스캐너: 조사 받침 대조·중복 조사·띄어쓰기·괄호 균형·영문 잔여·MT 직역구). 오탐 튜닝 다회(깔때기·나나/은은/도도·바나나 내부매칭·^reset;; 태그 종료자·쪽번호 괄호·<번역:>=EN <Translation: 미러·찬가/만가/분야 정상어·마기사이트으로=정상 받침 등 제외). fix_mt_style_batch35.py로 확정 오류 833필드/705자산 적용: 조사 오류(피스키퍼과→와, 중력장를→중력장을, 효능를, 배율를, 점프력를, 페로지움를, 마이코톡신를, 시스템를, 염소양를, 부품를, 로봇를, 릴로돈를, 스너겟를, 자격증를, 크레딧를, 으으로→으로, 연구실/시설/식물/반응로으로→로, 이리듐로→으로, 바삭한와→바삭하고), 붙여쓰기(수있/수없/것같/을때/릴때/일때), 안되→안 되, 면 되죠→면 돼죠, 이중 단어(인스타 인스타-, 지역 지역, 사용 사용, 방랑자의 방랑자의, 지붕 지붕, 무성한 무성한, 완전히/특히 반복), stray 괄호(연막)을·223)을·슈퍼 사격):·(중))·응답합니다.)·우박폭풍)·상상할 수 있습니다).·ZB welcome reset됩니다.) →초기화), 페이지 경계 괄호는 자산 수준에서 FP 확인(pharitu1/7·thesubstance 원문 대조 후 thesubstance c4·funightardoc1 c2·pharitu4 c1 문장 재구성 — '마을화'→'악마화' 오역 수정), 리터럴 이스케이프(\n·
·\두개골\" 6건), 태그 내 공백 TAG_SPACE 전량(내부 선행/후미 공백 정리), 이중 공백·문장부호 정규화, incoming fire 미번역 →날아오는 사격, 스타웃라이브/퀵바미니→StardutLib/QuickbarMini, '할 수 있게 됩니다'→'할 수 있습니다' 40행(ivrpg 스펙 리스트 등). 검증: 재추출 279,703쌍 JSON 오류 0, 태그 멀티셋/줄바꿈 대조 이상 1건(phaseshake 의도된 ( 추가), glossary 위반 0. 잔여 큐: EXAMINE_POLITE 6,252·TONE_MIX 3,110·PHRASE 계열(것입니다 1,953·당신 1,708·되어 있다 830·through 517·자신 489·복수 they 444·this is 368·가지고 295·로서 216·피동 193 등) — 샘플 확인 결과 대부분 문맥상 정상 또는 스타일 선택지로 개별 검수 필요. 배포: mods/female_translation.pak 교체(prestylefix bak 보존).
| 2026-09-30 | MT-STYLE-36 | - | 잔여 큐 소형 버킷 전수 트리아지 + 확정 오류 교정. fix_mt_style_batch36.py: 미번역/깨짐 5건(thelusian6 X'ians는→짜'이족은, ffs_frag_rgo_cultist description 말미 영문 문장→번역, brick description 중첩 op 영문→'찰흙으로 만든 작지만 완벽한 형태의 벽돌입니다.', gic_burnteffigy description 말미 오브젝트 경로 꼬리 제거, mechunlock completionText FU_KO 오버레이 잔여 영문 번역: spare resources→예비 자원·Engineering→엔지니어링·mech→메카 조립 스테이션) + TAG_SPACE 잔여 2건(gic_us_medkit·gic_usmifak_medkit 태그 내부 공백 — 중첩 op 리스트 순회 추가로 해결). 버킷 판정: PAREN/PARTICLE/MISSPEL/SPACE_PUNCT/DUP_PARTICLE 잔여 전량 FP(페이지 경계 괄호·이모티콘·목록 번호·찬가/만가/분야/마기사이트으로 정상어·가 되죠=정상·의도된 기호·나나/을을 의도 반복), ENG_LEFT 실오류 상기 5건 외 전량 식별자/URL/고유명 FP, DOUBLE_SPACE 451건 전량 선두/말미 패딩(EN 미러) 유지, DUP_WORD는 EN 원문 중복 미러(그렉·드론 드론·horrible horrible) 외 실오류만 정리. 배포: mods/female_translation.pak 교체.
| 2026-09-30 | MT-STYLE-RACE | - | 종족 조사 필드 존댓말 제거 일괄 패스(HANDOFF 규약: <race>Description은 플레이어 혼잣말 — 존댓말 금지; 일반 description/longDescription은 합니다체 유지로 제외). fix_race_polite.py 신설: 종결어미 변환 규칙 + 자모 단위 활용 — 습니다→다(형용사·과거·있다/없다 자동 정확), Xㅂ니다→ㅂ 탈락+ㄴ다(합니다→한다·줍니다→준다·됩니다→된다), 합니다-형용사 세트→하다(만족합니다→만족하다 등 ~90어간), 입니다→이다, 네요→네·군요→군·죠→지·지요→지, 어요/아요/해요/여요→어간 유지, 이에요→이다·예요→다, 세요/시오→단어 사전(조심하세요→조심해 등 ~60어휘), 습니까→을까, 합시다→하자. 예외 사전: 습니다 동사→는다(먹습니다→먹는다 등 16어), 르-불규칙 형용사(빠릅니다→빠르다·다릅니다→다르다·느립니다·큽니다·깁니다·예쁩니다), 아닙니다→아니다, 겁니다→거다(것+ㅂ니다), 명사+니다 동형어(바구니다·도가니다·주머니다 유지), 이+ㅂ니다 동사 오인 방지(움직입니다→움직인다 등), 명사 -요 블랙리스트(필요·주요·담요·중요·동요·고요 등), -해야합니다→-해야 한다, -합니다→-한다/-하다 분기. 적용: 12,796필드/5,243자산, 엔트리 59,519 유지. 검증: 재추출 279,703쌍·JSON 오류 0, 태그/플레이스홀더/줄바꿈 서명 대조 불일치 0(dem_* 사운드 오브젝트 <> 템플릿 35건은 내용 변경 정상 플래그), qa_pak_glossary 위반 0. 스캐너: EXAMINE_POLITE 6,252→130(잔여 전량 generic description 필드 — 합니다체 정상), TAG_SPACE 0. 산출: _conv_words.txt 변환 전어휘 2,465쌍 수동 검수 완료. 배포: mods/female_translation.pak 교체(bak_racepolite 보존).
| 2026-09-30 | MT-STYLE-37/38 | - | 잔여 큐 완전 소진: 종족 조사 필드 존댓말 최종 잔여 10건 수동 치환(fix_mt_style_batch37.py — 입니까→이는가/인가/이지, 봅시다→보자, 합시다→하자 + 플라즈마고→플라스망고 오타 교정) + DUP_WORD 실오류 4필드(fix_mt_style_batch38.py — modernshingle×2 '멋진 멋진'→'정말 멋진', effigiumhammer '유령처럼 유령처럼'→'유령처럼', fu_alienwood_flowerpot '외계인 나무 나무' 중복 제거 — FU 원본 'Miniture Alien Wood Tree' 대조). 잔여 버킷 전량 트리아지 완료: TONE_MIX 2,183=대화+서술 정상 혼용(juux 종족 텔레파시 단편 문체는 원문 의도 확인), PHRASE 계열 전량(것입니다/당신/되어 있다/을 통해/자신/they-복수/이것은/가지고 있다/로서/피동/그 녀석/많은 것들/로써/될 수 있다/무슨무슨)=문맥상 정상 표현, ENG_LEFT 304=식별자·URL·유저명·아이템ID 전량 FP, DOUBLE_SPACE 451=EN 미러 패딩 유지, EXAMINE_POLITE 130=generic description 합니다체 정상, PAREN 11·PARTICLE 16·SPACE_PUNCT 5·MISSPEL 3·DUP_PARTICLE 2=전량 FP(페이지 경계 괄호·이모티콘·찬가/만가/분야/마기사이트으로·가 되죠·을을 괴언). 종족 조사 필드 존댓말 재검증 0건. 검증: 재추출 279,703쌍·JSON 오류 0·엔트리 59,519 유지, pak 구조 대조(bak37 대비 변경 14필드 전량 의도 편집·태그/플레이스홀더/줄바꿈 불일치 0), qa_pak_glossary 위반 0. 배포: mods/female_translation.pak 교체.
| 2026-09-30 | MT-STYLE-39/40 | - | 대사 은행 존댓말 정규화(STYLE_MIX group2/3+stylemix_todo 대사 은행 큐 — 은행 내 소수 존댓 이탈 행을 은행 다수 말투로 통일, 총 396필드). _dialog_polite_dryrun.py 변환기: fix_race_polite 확장 + 자모 단위 활용 — 세요/십시오/시오/으세요/주세요 명령형 합성(오→와·우→워·이→여·으→어/아·르-불규칙 기르→길러/모르→몰라·모으→모아, 하→해), ㅂ니까→나(합니까→하나 — 이유접속 ~하니까와 ㅂ 받침으로 구분), 십니다→는다·랍니다→란다·십니까→나, 요 계열 스트립(있나요→있나·될까요→될까·거든요→거든 등). 예외 사전: 거세요→걸어·구세요→해·되세요→돼·누구세요→누구야·계십니다→계셔·마십시오 양의성 처리(하지 마십시오→마, 음료 마십시오→마셔). 인픽스 정리: 주셨/하셨/으셨/오셨/계시/드리/이신/하시계열 + 음절 내 존칭(싶으신→싶은·있으신→있는·하신→한·오신→온·주실→줄·쉬실→쉴·말씀하→말하). 안전 가드: cinematics 자산 제외, 상관호칭 스킵(선장님/대장님/경관님 등 74행 — 존댓 동기부여), 지하실/드릴(천공기) 명사 오탐 정규식 가드, 돌아가신(서거 완곡어) 유지, 반드시/표시다/주시하다 등 비존칭 유지, 은행 다수 존댓(brewmaster 전 행 존댓 등) 유지. fix_dialog_polite_batch39.py 적용 359필드(297+62 두 라운드 — POL 감지 정규식이 ~까요/나요/게요/거든요/ㅂ니까 계열 누락한 것을 END_RX로 통일해 추가분 확보). fix_dialog_polite_batch40.py 수동 잔여 37필드: 적용 행 내 음절 내 존칭 잔여(싶으신가→싶은가·있으신가→있는가·필요하신가→필요한가·주실→줄·오신 걸→온 걸·생물이실까→생물일까·자비로우셨다→자비로웠다·말씀하셨지→말했지·축복해주셨어→축복해줬어·탈출하신 걸→탈출한 걸·삼으셨던→삼았던), 전체 존댓 이탈 행(r-peacekeeperconverse 도와드리겠습니다/기회예요/바랍니다/안녕하신가, ffs2 안녕하신가, merchant 고쳐요, catgrumble 요구합니다/떠날 거예요), 개별 오역(USCM를→USCM을, severe/avian 고쳐 줘야겠다→고쳐줘 주어 오역, 네 존재 신비→네 존재가 신비롭군 전보체, 네 존재 가볍게 안 봐 조사 누락 ×2), 지할→지하실 복구(인픽스 오탐 자체수정). 검증: 재추출 279,703쌍·JSON 오류 0·엔트리 59,519 유지, bak39 대비 변경 87자산 태그/플레이스홀더 불일치 0, qa_pak_glossary 위반 0, 잔여 존칭 스캔 15행=전량 의도(건드리다/주시하다 비존칭·상관호칭·완곡어). 배포: mods/female_translation.pak 교체(bak39 보존).
| 2026-09-30 | TSV-AUDIT | - | qa_struct_all 1,074건 전수 감사 결과: 전량 id-조인 아티팩트, 실위반 0. 원인: rest_worklist.tsv가 번역 TSV(rest_*.tsv) 작성 이후 재생성돼 id↔행 매핑이 붕괴 — qa_structure의 id 조인이 서로 무관한 문자열끼리 비교(예: EN 'Set Bonuses'↔KO '할 말이 있었으면'). 검증: ① 워크리스트 EN과 의미적으로 매칭되는 TSV-KO 0건(전수 스캔). ② TSV-KO 790/1,074건이 pak_pairs에 그대로 존재 — 각자 자기 EN의 정상 번역(태그·플레이스홀더 보존, '<slots> SLOTS'↔'슬롯 <slots>칸'). ③ EN-매칭 133건에서 pak-KO는 항상 올바른 번역. TSV 번역층·배포 pak 모두 무결. 참고: rest_worklist.tsv를 TSV id 순서로 재생성하기 전까지 qa_structure의 worklist 조인은 무의미 — 향후 pak_pairs 기준 QA(qa_pak_glossary·pak 구조 대조)를 사용할 것. 산출: _audit1/2/3.txt 대조 증적.
| 2026-09-30 | MT-STYLE-41 | - | 대사 은행 큐 전수 검수 2차(_dialog_review.txt 12,603행 정독 완료) — 확정 오역·오타·용어위반 108포인터 교정(fix_dialog_errors_batch41.py, 53자산). 명칭/용어: 영주님→집주인님 14행(landlord 호칭 전량), 수호자레이트→보호국 19행, 그랜드 수호자→고위 수호자 5행, 늑고위→늑대 2행, 컬트 추종자→광신도, 홀릭스 이병→이등병, Old Protectorate Portrait→옛 보호국 초상화 2행. 아이템명 통일: 갈고리 걸이→그래플링 훅, 리로케이터→재배치기(아이템 정본 기준), 점프젯→점프제트, 시험 제작소→시험 제조 공장, 요양실→회복실, 전차 선로→트램 선로, 결정→수정(샐리 흡수 결정체), 화이트 크로→화이트 크로우 4행. 인명/오역: 내 수탉 돌려줘→내 쿡을 돌려줘(Coock 인명), 씨앗→씨받이(seedbed), 알들이이 나온다→들어간다(방향 오역), 촉수 무리→촉수의 새끼(brood)/촉수 소굴(hive)/촉수 블록(tentacleblock), 고쳐줘·찬성표를 던져→지지해(vow/vouch), 길을 비켜라→비워라, 뛰어나가서→밖으로 뛰어내려(메크 하차), 폭력적인 반응→격렬한 반응(viol- 절단 미러 유지), 또 다른 무리→또 다른 지뢰 무리(mine 문맥), 꺼내줘→빼줘(전장 이탈), 격추해→쓰러뜨려(엔진), 긴 여정→기나긴 고행(slog), 그들과 달라→그들 일당이 아니야, 자신에게→족장님께(her 지시), 쏴버릴 조사 누락, 최선의 생각→좋은 생각, 곤란 처지→곤란한 처지, 무분쟁 구역→분쟁 금지 구역, 팔지는 의심스럽군→팔 것 같지는 않군, 가볍게 안 봐→가볍게 보지 않아, 온순한 편이야→온순한 편이니(의문), 미라실 바깥의→미라실 출신의, 뱃속에 가장 쉬운→뱃속에서 가장 편할지, 칼(형틀)→형틀(pillory 오역), 따분하게 불편→끔찍하게 불편(painfully), 내 말인데?→그런 모양인데?(I guess), 튀는 탄환→통통 튀는 탄환(bouncy), 터질 것 같네→꽉 차 있네(bursting with), 더 커졌어→더 커져라(명령), 너도 그렇다→너도 마찬가지다. 오타/조사: 내나→나나, 곧네→쭉 뻗었네(straight), 나용이다→나를 위한 거다, 선배을→선배를, 에너지들→에너지, 연구개발 루나→연구개발팀에서 루나. 문체 통일: 무녀랍니다→무녀예요(문장 내 혼용), fenerox 전투 구호 보입니까/사라졌습니까→반말(은행 내 반말 통일), 탈출 포드→드롭 포드(drop pod 3행 — escape pod 문맥의 탈출 포드는 유지), 1층 지하실→지하 1층, 4층 지하→지하 4층. 유지 판정(검증 후 변경 안 함): 수정 기술 사랑·깃발 아름다워(아키/새턴 전보체), 범우주 우주 기업군(USCM 이중의미 미러), 치차/치카/치키타(별개 인명), 미라실(통일 사용), 비컨 46행(Beacon 고유물/군용 비컨 정상), 유적/폐허(문맥 구분 정상), 신병(Recruit 표준), 이방인이여(일관된 고어 호격), 여주인(레이디 호칭 대칭), 백성/부르릉/음흉/도가니다 등 전량 정상, 퀘스트(quest 원문 확인), 편애나/사이애나이더(애나 오탐). 검증: 재추출 279,703쌍·JSON 오류 0·엔트리 59,519 유지, bak41 대비 변경 53자산/108필드 전량 의도 편집·태그/플레이스홀더/줄바꿈 불일치 0, Protectorate EN 잔여 대조 보호국 누락 0. 배포: mods/female_translation.pak 교체(bak41 보존).
| 2026-09-30 | HOUSEKEEPING | - | 임시 산출물 정리: 루트의 ad-hoc 분석 스크립트·덤프·검증 출력(_* 135개)과 생성 로그(apply_out/extract_out/propose_out/scan_out/quest_fix_dump/review_pending_check/server_boot*.log 8개) → scratch/ 이동(총 143파일), __pycache__ 제거. 루트에 남긴 것: approved_names.txt/approved_ambvar.txt(propose_name_fixes.py 입력 레지스트리), 패치·QA·빌드 스크립트 전량, style_mix_*.tsv·pak_pairs.tsv·qa_struct_all.tsv 등 활성 산출물. fix_dialog_polite_batch39.py의 _dialog_polite_dryrun 임포트 경로를 scratch/로 갱신해 재실행 가능 유지. docs/ 아래 sexbound_flagged.txt·sexbound_review.tsv·priority_allocation_20260927.tsv 등 명명 산출물은 원위치 유지.
| 2026-09-30 | REORG | - | 루트 재편(구형 파일 정리): 301개 .py → tools/, 활성 TSV·레지스트리 62개 → data/, 참조 단절 중간산출물 31개 → archive/, 루트 스테이징 pak 7개(stale copy·REVIEW_PENDING·NEW24/25·NORMALIZED·deployed-bak·bak37) → backup_paks/. 루트 잔류: README·AGENTS·LICENSE + 디렉터리. tools 이동에 맞춰 HERE/BASE/ROOT 깊이 상수 일괄 수정(.parent 한 단계 추가, parents[2]→[3]), 이동 파일 리터럴에 data//backup_paks//scratch/ 접두사 부여, data/data 이중 접두사 후속 정리. scratch/_dialog_polite_dryrun.py의 fix_race_polite·style_mix·pak_pairs 경로 갱신(sys.path tools 추가). 검증: compileall 통과, 미수정 리터럴 0, qa_pak_glossary 실행 정상(279,703쌍·위반 0→data/qa_pak_glossary_report.tsv). 실행 규약: 스크립트는 저장소 루트에서 실행(README 폴더 구조 절 참조).
| 2026-09-30 | REORG-2 | - | 상위 translation/ 구형 작업 디렉터리 4개 → ../_archive/ 통합(translation-fix-20260921·noneki-spanedit-20260922·replaced-installed-20260922[롤백 백업 보존]·translation-overlays-20260921). tools/ 내 `translation/<dir>` 경로 리터럴 10개 파일 갱신(`_archive` 세그먼트 삽입). E:\Desktop\mods\replaced-installed-* 는 별개 위치라 미수정. translation-rest-20260922·rest-stage·GAME\tmp 경로는 이미 소실된 stale 참조로 유지(기록상 이력). compileall 통과.
| 2026-09-30 | MT-CODEX-42 | - | 코덱스 산문 전수 수동 검수(_codex_review.txt 23,957행 정독) + 확정 오류 교정. fix_codex_review_batch42.py: 규칙 엔진(전역 치환 + EN가드 + 자산/포인터 스코프 + 경계 정규식), 477자산·601필드 적용. 산문 교정: 전설 이상도 아니게→전설에 불과하게, 만일이 낫지 후회보다→후회하느니 미리 조심, 현 임무 네 메모→현 임무에 관한 네 메모, 방어선으로, 절단 입자 복구, 미네랄 반점→알갱이(speck), 요약된 기록 역사→기록된 역사 요약본(6), 반흔한→인기 있는(fad 생성어), 급수 용액→급수 장치, 골동품과 단지들→안토라시 관광 안내(제목 누락), excited→기대된다(자랑스럽고 오역), 천사 반란군 동어 반복→천사 반란, 암흑의 시대가 두렵다→두려운 암흑의 시대다, 국방부의 표면을 자처→계승자를 자처(mantle), 벌목 저장소→로깅 캐시, 유적 생물량→루인 생물량, 방사성 혹→방사성 구근(bulb), 묵언→벙어리(mute 오역), 에이페는→에이펙스는, 타고 있었지→있었지, 더미→묶음(stack), 단자→단말기, 브릿지→브리지, 기능 고장→걸림(jamming 목차), 핵융합→융합(elements), [보통]→[일반], EXECRATIONS(기계 복수)→엑세크레이션이, 대시들→대위더링(Great Withering), 몬스터 약탈→몬스터 루팅, 미니크녹의 발기→부상하던 시기(rise 오역 2), 스스로를 바라고→스스로에게 의지하고, 다츠→다트, 자동 물뿌리개→자동 스프링클러, 삼안경서→트라이코더(tricorder 오역), [기밀]/[검열됨]/[Redacted]→[삭제됨], 라-보→라보에, Tea-Loving Lad 비번역 유지. 용어 통일: Green Word→녹색 언어(녹색 언어씀 오타+푸른 말씀·초록의 말씀·초록 말씀), The Wood→숲(더 우드·우드, viera 스코프 — 우드트레커 보존), 엑소시안→엑수시안 76, 카이테란→키테란 16, 모그리→모글, X'i(짜이·X'i 혼용)→짜'이(가짜이길 오탐 방지), 아이리실·아이리사→이리실·이리사, 테렌→테레네(→42b에서 행성으로 재조정), 손윙·가시날개→쏜윙, 앰비리→암비리, 코럴그로워→코럴그로어, 맥비카→맥비커, 히라키 코레일→히라키 코랄레, 글림를레쿠스→글림레쿠스, 문셰도우→달그림자, 비리데센트·비리데선트→비리데슨트, 배드랜즈→배드랜드, 아케이니안→아르카니안, 로푸니→로퍼니, 시그누스→시그너스, 클룩스→클루엑스, 라에나신→라에나틴, 델타 하쿠키→델타 하쿠우키, 서펜트→서펀트, 다빈→데이빈, 매슈→매튜, 세온하→선하, 모라흐→모라그, 멍멍 무리→우프 무리, 오잉킹·오잉커서→오잉키서, 녹스 여주인→녹스 여주, 후시→후치, 놀리스→누올리스(Noolith EN가드 — 모놀리스 보존), 성점술사→아스트로맨서, 솔라 가디언→태양 수호자, 하이 마구스·상급 마법사→대마법사, 우주의 군주들→코스모스의 군주들, 잡 방어구→직업 갑옷, 여가장→여족장(동일 문서 내), 별의 광신도·별빛 신도들→스타리 컬티스트, 스타리 정원→스타리 가든, 별게→스타크랩(om_starry), 스텔라 부채물고기→스텔라 팬피시, 비에라 스나이퍼→비에라 저격수, 사기꾼의 시련→트릭스터의 시련, 달마스카→달마스칸(의·들 예외), 빛의 활→라이트 보우(새턴 아이템명), 배통→지휘봉(새턴), 세계의 지평선→월드 호라이즌, 지평선의 전투 기계→호라이즌의 전투 기계, 블러드 우프→피의 우프·핏빛 털의 늑대→블러드 울프(Blood Wolf), 선장·책임자여·대장님→대위(woofie Price 대위), 러스트풀 위프→색욕의 채찍, 아이온·이온→에이언(Aeon EN가드 — 라이온 보존), 항해자→내비게이터(Navigator 보스 EN가드), 하베스터→수확자(EN가드 — HarvesterBeam 제외), 거대기업→메가코프(EN가드), 크라코스↔크라코탄 EN가드 양방향(K'Rakoths 종족명↔K'Rakothan 형용사 구분), 무덤 수호자·무덤 경비병·묘지기→무덤지기, 잔재 진화 과정→베스티지-에보 프로세스, 통합 우주 기업 군대→범우주 우주 기업군(USCM), 누락 적용 0. 유지 판정: 정오(ERRATUM 정오 정확한 용어), 가오리(실제 가오리 동물), 유니버설 스페이스(USCM 무관 기업), (voe) 원어 병기, 별빛 행성(유형 설명어), 모글·크라코스·놀리스·라에나틴 확립 표기, 이리실/이리사 복수·단수 구분, 루인드/루인 별개 세력, 집행·더미·단자·발기·파티·핵융합 빈도 정상, 밍콩·미니크녹 별개 명칭, 이비/EB·형/동생·벌집/둥지 문맥 정상, 문체 혼용 구간(육아 안내서·prcw-betrayal·starrylore5·아프로디테) 캐릭터 보이스로 유지. 검증: 재추출 279,703쌍·JSON 오류 0·엔트리 59,519 유지, bak41 대비 변경 필드 전량 의도 편집·태그/플레이스홀더/글리프/줄바꿈 불일치 0. 배포: mods/female_translation.pak 교체(bak41 보존).
| 2026-09-30 | MT-CODEX-42b | - | Terrene 조직명 방향 수정: 용어집 고정 정본이 바닐라 번역 행성 보호국·피스키퍼이므로 42의 음역 통일(테레네 X)을 행성 X 체계로 재조정 — 테레네 보호국 157·피스키퍼 9·가디언즈 10·선거단 7·가드 3·보호령 4(Protectorate 변형)·"행성" 법 집행관·유토피아·테레네에→행성 보호국에. 알타 테레네 전시대는 행성 유형/세력 양의성으로 유지. 182필드/117자산, 재추출 후 qa_pak_glossary 위반 0.
| 2026-09-30 | DEPLOY-RENAME | - | 배포 pak 개명 + mods 백업 정리(미번역 노출 원인 해소). 진단: 파일명 로드 순서상 trans+Avali/Shellguard/Stargate/dmgfix_starforge(워크샵 모드 팩 본체)와 zz_localeko_highpriority_20260927이 female_translation.pak보다 늦게 로드돼 동일 경로 .patch를 덮어씀(trans+Avali 2,342자산 겹침). 또한 mods/에 놓인 백업 female_translation_bak39.pak(552자산)·bak41.pak(490자산)이 .pak이라 실제 로드되며 최신 수정을 구형으로 되돌림. 조치: ①백업 22개(2개 로드중 .pak + .bak* 20개)를 backup_paks/mods_backups/로 이동 ②배포 pak을 zz_translation_female.pak으로 개명해 전 pak 중 가장 늦게 로드되게 함(.metadata name female_translation 유지) — 모든 충돌 경로에서 한국어 최종 적용, 타 pak의 비텍스트 op(zz_modfix_refs 27자산 겹침·zz_female_overhaul 619자산)는 포인터가 다르면 그대로 병합 적용 ③tools/scratch 43개 스크립트의 배포 경로 상수를 신 파일명으로 갱신(과거 .NEW*/REVIEW_PENDING 스테이징 참조는 이력 유지). 검증: extract_pak_pairs가 zz_translation_female.pak에서 279,703쌍 정상 추출, 엔트리 59,519 유지, compileall 통과. 참고: 09-29 03:32/03:34 starbound.log의 /interface.config 치명 오류는 패치 적용 시뮬레이션상 병합 결과 정상(최종 JSON 유효·minInterfaceScale=1.0) — 패치 파일 중 Patch_Project/Stardust_Core/contents_2010607826이 확장 JSON 문법(주석/grammar-ext 헤더)이라 엄격 파서 기준 파싱 실패로 보이나 SB 자체 파서 허용 범위 내로 추정, 재부팅 후 재현 여부 확인 필요.
| 2026-09-30 | TRANS-48~54 | - | untranslated 큐 연속 처리(GiC 패밀리+관련 모드). 배치48 GiC 본체(contents_2754886445): uniq 3,417 전량 수동 번역(청크 01~12), 총기·부착물·방어구 세트군 대량 — 배틀 소총/소염기/스쿠툼/겐시디움/제압/점화/회피 확률 등 용어 정착, 실개행·^color;·[CHEST]/[EWS] 토큰 보존 대조 검수. 배치49 GiC 확장(contents_3117942107, ESC): 600uniq→431자산(재사용 12). 배치50 Viera(contents_?): 613uniq→444자산(모글/비에라 잡 갑옷·가발·퀘스트 도입문, 마기사이트/선하/우드트레커/달마스칸 재사용). 배치51 skpkmn(contents_2593214277): 447uniq→의상 패턴 일괄 생성 + skpkmng1craft 중첩 title/subtitle 수동 병합(덮어씀 사고 복구, 4op 공존 확인). 배치52 Saturnians(contents_1103027918): 1,303uniq 6청크, 새터니안 통일, saturnArmorTransmog/loom/summoner 중첩 op 재병합(재적용 덮어씀 복구). 배치53 GiC Otherworlds(contents_3731148374): 481uniq→303자산, 요괴 세트군(텐구/캇파/사토리/키츠네/오니/루나리안), 라이온 대대·로즈 제국·웨스트 스타·배치 명령·보병 소환 정착. 배치54 RSR(contents_2980583814, GiC WW2 일본군 장비): 426uniq→239자산(재사용 0), 미코타이/미코헤이/호헤이 '60/제국 육군·해군/여우/퍼시픽 불워크/매복 전술/두 번째 기회/설득의 바늘/잔항병 정착, DEPLOYMENT ORDER ^orange; 인라인 강조 복원(22건 태그 서열 교정). 공통 절차: untrans_batch.py extract→uniq 수동 번역→태그/개행/인덱스 정합 스크립트 검증→EN↔KO 전수 대조→apply--apply 직접 패치 병합(test=live EN 재독취). 배포: zz_translation_female.pak 67,910엔트리(48 직전 63,237 → 누적 +4,673). 잠금 다발로 tmp pak 검증 후 교체 패턴 반복. pak 용어 QA 매 배치 위반 0.
| 2026-09-30 | TRANS-55 | - | GiC LFW 무기 팩(contents_2983581962) 미번역 처리: 365필드 추출 → 214 필드 기존 번역 재사용 + 151 uniq 미번역(수동 78·정규화 재사용 72·기존분 채택 1). 수동 구간: 현대 총기/탄창/광학기/PMD 배지·스카프/조정장치/하드케이스/음악 라디오. 용어 정착 반영: 보조 발사(일부 보조 사격 교정)·완전 자동·나선형 탄창·무반동총·무기 숙련·[VANILLA] 토큰 원형 유지. 검증: uniq 150 커버리지·태그 서열·개행 대조 0, EN↔KO 수동 79건 전수 대조, apply 195패치·스킵 0. 구조 이슈 해결: 배포 pak 내 대소문자 중복 패치 163쌍 발견(구 캠페인이 /items/ 소문자, LFW 제공자 경로는 /ITEMS/ 대문자 — 게임이 케이스 무시 매칭 시 구형 번역이 신규를 가릴 수 있는 레이스) → 구형 op 평탄화 후 미커버 필드(category 등)만 보존해 제공자 경로(대문자) 패치에 병합, 소문자 중복 163엔트리 제거. 배포: 68,105 → 67,942엔트리. 잔여: pak 내 l-l형 대소문자 중복 2,070쌍은 기존 유산(MATERIALS/FARMABLES 등)이라 별도 정리 과제로 보고.
| 2026-09-30 | TRANS-56 | - | nuggubs 아이템 팩(contents_2735634052) 미번역 처리: 527필드 추출 → 146 재사용 + 365 uniq 수동 번역(의상 세트·염료 97종·바이로브 등 피규어·가구/오브젝트). 표기 정착: X염료·X피규어·라벨에 쓰임·펭귄/전초기지/에르키우스/아가란/팝톱, 모드 캐릭터 음역(벨 카탈루어·스태그볼트·네오나·설퓨라 등). 검증: uniq 365 커버·태그·개행 0, apply 266패치·스킵 0. 전 경로 소문자라 대소문자 중복 없음. 배포: 68,208엔트리(+266).
| 2026-09-30 | TRANS-57 | - | 바닐라 packed.pak 미번역 처리: 248자산 491필드 추출 → 109 재사용 + 297 uniq 수동 번역(NPC 무기·희귀 등급 무기·재료·블록·보호국 배경 부품·스포너·투명 와이어링·퀘스트 텍스트). provider가 assets/packed.pak이라 scratch/_vanilla_apply.py로 커스텀 적용(동일 test+replace 로직). 중첩 windowtitle title/subtitle 5자산(철 모루·철 제작대·연구 스테이션·고용주 스테이션·펭귄 종족)은 실제 JSON 경로 탐색 후 같은 patch 엔트리에 병합. 표기 정착: 희귀/고급 등급·생성기·보호국·펭귄·지연 게이트·벽 스위치·래치. 검증: uniq 297 커버·태그·개행 0, apply 248패치. 배포: 68,456엔트리(+248).
| 2026-09-30 | TRANS-58 | - | Enternia(contents_2006558650) 미번역 처리: 436필드 추출 → 18 재사용 + 399 uniq 수동 번역(알타 의상·방어구·EPP/증강·투척무기·음식·목걸이). 텍스트 대부분이 /presets/*/·/upgradeParameters/·/variants/0/ 중첩이라 표준 apply로 부족 — scratch/_enternia_apply.py가 leaf-key+값 일치하는 전 경로를 탐색해 test+replace 생성. 표기 정착: 알타·에터니아·알테르니아·세테라이·스타더스트·드리머·옴니블루·기트신·비신·헤비카·이소슬라임·엔터/알터/세터-EPP·증강. 검증: uniq 399 커버·태그·개행 0, apply 220패치·누락 0. 배포: 68,676엔트리(+220).
| 2026-09-30 | TRANS-59 | - | contents_2010607826(Betabound) 미번역 처리: 364필드 추출 → 106 재사용 + 234 uniq 수동 번역(무기·의상·증강·도구·염료·투척무기·작업대·UI 메시지·상태효과·수확 식별자). sb_uimessage:*/sb_*Harvest는 식별자라 원형 유지. tooltipFields/subtitle·collectables/*/variants 중첩이 다수라 leaf-key+값 일치 커스텀 적용(199패치·누락 0). 검증: uniq 234 커버·태그·개행 0. 배포: 68,875엔트리(+199).
| 2026-09-30 | TRANS-60 | - | contents_3255373921(CCG 의류) 미번역 처리: 594필드 추출 → 10 재사용 + 560 uniq(의상·방어구 대군, CCG* 식별자 스텁 195개는 형제 shortdescription KO로 자동 매핑). windowtitle title/subtitle 중첩 1건은 leaf-key 커스텀 적용. 표기: 진압·아스트로거너·부칸·호첸플로츠·그라운디드·보호국·데코 계급군. 검증: uniq 560 커버·태그·개행 0, apply 199패치·누락 0. 배포: 69,074엔트리(+199).
| 2026-09-30 | TRANS-61 | - | RPG(ivrpg, contents_1115920474) 미번역 처리: 312필드 추출 → 54 재사용 + 242 uniq 수동 번역(직업·전문화·스탯·수리검·캘트롭·장신구 세공군·소모품·상태이상). 표기 정착: 위력 배율·출혈 확률·친화도·에지솔트·페로지움·비올리움·일렉트럼·보석공·깃털 낙하·요정 가루·용의 숨결/피·강철 피부. 검증: uniq 242 커버·태그·개행 0, apply 183패치·스킵 0.
| 2026-09-30 | TRANS-62~78 | - | 잔여 미번역 큐 전량 소진(uncovered 0). 연속 배치: Lucario(260uniq, 체형 변형 태그·코드 원형 유지)·Project45(250uniq, 총기/능력/스탯)·c1145 NPC 코스튬·voided·angel(천사 계급)·c1417·Knightfall(프레임 갑옷)·c2957(아우레아/오리온/엑수시안)·c2611 네키 의상·c2070·starburst(무기/EPP)·c1945 픽셀던전·c3289(스타수트)·sexbound-reborn(섹스바운드/섹스벅스)·AvaliPlus·Felin·c2918(블루아카이브 헤일로)·c1523(마리오 -ette 크라운)·c779 라미아·c2604·c1857·c2468·c2979(급습/과충전/소음기)·c2925·gcyber(사이버펑크2077)·extstory + 1~4건 소형 큐 55개. sxb_TTPPv2 38자산은 리스트형 문서+중첩 패치 커스텀 적용으로 해결. 중첩 툴팁/콜렉터블 경로는 leaf-key+값 일치 탐색으로 병합. 검증: 배치별 uniq 커버·태그/개행/EN↔KO 대조 후 적용. 배포: 72,429엔트리. 서베이 직접 검증으로 confirmed missing 0.
| 2026-09-30 | GLOSSARY-PAK | - | 배포 pak 전수 용어 QA(extract_pak_pairs 305,174쌍 대상). 초기 위반 181건 → 0: DEF→방어력 계열 통일, 구형 번역 패치 덮어쓰기 버그 수정(같은 patch 내 다중 행이 마지막만 반영되던 병합 오류), Actian/텔레포터/플로란 오번역 5건 교정(avaliteleporter_2 화장실 유머·gaterepair '전초기지 - 메인 텔레포터'·tentbed 플로란·stealthposters 복구). 10-01 재검증 296,408쌍 위반 0.
| 2026-10-01 | REPAIR-BROKEN | - | broken 서베이 2,566쌍(제공자: FU 1,967·packed 209·c2959854988 150·AvaliPlus 51 외) 수리 완료. broken = 패치 test 값이 현재 유효 자산값과 불일치→인게임 그룹 스킵. ①Starbound JSON 파서 재작성: 문자열 내 //·/* */ 주석 오제거 버그·문자열 내 리터럴 CR/LF로 인한 JSONDecodeError 해소(quote-aware 스캐너, chr(92/13/10) 표기로 전송 손상 차단) ②test 재정합: 소스 존재 시 현재값으로 reassert 4,464, 값 이동 시 repoint 7, 소스 소실 시 그룹 드롭 151+123 ③대소문자 변형 패치 인덱스로 nopatch 206→4, 잔여 4건(Protectorate 갑옷 3·바닐라 fryingpan) 신규 패치 추가 ④유효문서 평가기 도입: 베이스+제공자측 .patch 순차 적용 후 검증(PATCHERS 맵 재구축 — FU가 바닐라 converse.config 등에 추가한 종족 대사 경로 반영) ⑤숫자 인덱스 리프는 재단정 금지 원칙(다른 항목에 오적용 방지 — celestial names 10종 소실 확인 후 드롭 정당) ⑥식별자 한국어 파괴 제거: itemName/objectName에 KO replace가 들어간 그룹 649건 제거(아이템 ID 보존).
| 2026-10-01 | DEDUP-CASE | - | pak 내 대소문자 변형 중복 패치 2,627그룹 정리. 제공자 정식 케이스 맵으로 캐논 경로 결정, 그룹 단위 병합 — 충돌 시 정렬순 나중 파일 우선(단 test 실패 확정 그룹은 가시 결과 보존을 위해 이전 유지), 패자 그룹은 data/dedupe_conflicts.tsv 로깅. 삭제 지원 커스텀 writer로 중복 엔트리 제거. 결과: 대소문자 중복 0, 72,429→69,802엔트리. 병합 재현 검증으로 현재 인게임 가시 결과와 동일 확인.
| 2026-10-01 | C946-FANOUT + FINAL-QA | - | leaf-key 팬아웃 버그 교정: 캡션 전수에 '뒤로'가 뻗친 digitalstorage_terminal/TransferNode 패치를 경로별 올바른 KO로 교정(1·10·100·Get·Sort·Craft·Replace). 전 pak 팬아웃 스캔 28의심 자산 중 실제 오류는 c946 2파일뿐임을 확인. radiomessages/quests senderName 8그룹 정리(존재확인 사자 그룹 6 드롭, test+replace를 add op으로 변환해 필드 생성). iter_groups 혼합구조 버그 수정(중첩그룹+벌어진 dict op 혼재 문서를 1그룹으로 묶던 문제 — IFD_statuseffects 등). 최종 전수 검증: 68,151패치 205,022 test op failed_ops 0, no_provider_asset 1,606은 제공자 미등록 patch-only 사자 엔트리(문서화 예외). pak 지표: 엔트리 69,806, 대소문자 중복 0, 식별자 KO 0, 용어 위반 0(296,408쌍). 루트 임시 스크립트 10개 tools/ 이동.
| 2026-10-01 | TSV-SYNC + SAT-SWAP | - | 사용자 수동 TSV 교정의 배포 pak 반영 + 관련 손상 수리. ①_drift_check.py로 편집된 ko 파일 18종과 배포 pak 대조 — 초기 305차이 중 실질 89op 적용(_apply_user_tsv.py, test=EN 검증·sat_names는 글리프/색 접두 보존). ②saturn 계열 name↔description 스왑 손상 발견·수리: ko 파일 행 순서(name,desc)와 uniq id 순서(desc,name)가 뒤집힌 구간에서 오매핑 발생 — satglitchtier1~6(14자산)·lunairobes2 head/legs·merchant/noble/ornaterobes·Demon.head·tier6separator 명칭 접두 유실까지 _fix_sat_swap.py로 65op 의미론 복원(일부는 TRANS-52 시점 기존 손상). ③안테나 변형 마커 ^yellow;҂^white;(U+0482 비PUA)가 접두 보존 정규식에서 누락돼 23명칭에서 소실 → 전량 복원, separator의 ^cyan;^white;도 복원. ④pak 전역 스왑 휴리스틱 스캔(이름필드 문장형·설명필드 단문형) — saturn 외 위반 0 확인. ⑤용어 정착 충돌 처리(사용자 판정): 방어:→방어력: 47+2op, 순간이동기→텔레포터 3op, 히로틀→하이로틀 2op, 유탄발사기→유탄 발사기 1op — TSV 행도 동기 수정해 재드리프트 차단(_fix_glossary_terms.py). 최종 상태: 용어 위반 0(296,408쌍)·패치 JSON 파싱 전량 정상·잔여 드리프트는 꼬리 개행·글리프 접두 오탐·sat 파일 id 오정렬 검사 오탐뿐(실질 불일치 0).
| 2026-10-01 | LUSTLING-DIALOG+INSPECT | - | 러스틀링 조사 대사 미번역 신고 처리. 제공자(997_sxb_Lustlings_1.2.9_clean) 패치가 추가한 lustling 섹션·/lustlingDescription 2,555필드 중 247필드(유니크 212)만 영어 잔존, 우리 pak 커버 0 → 대상 자산 패치 247개 전부 존재 확인 후 test+replace 그룹 추가. 대화: /dialog/converse.patch의 /greeting/lustling 39행 전량 EN(파일 자체가 닫히지 않은 기형 JSON이나 게임은 적용) + combat/flee/arrivedhome 흩어진 EN 7행만 보정 — test=제공자 원문 게이팅. 용어집 준수(러스틀링·고위 수호자·보호국·물질 조작기·하이로틀·흙성게·플루팔로·클루엑스·에로스), 제공자 기존 KO 2,308행의 거친 톤 유지. 검증: tmp pak 패치 69,757 파싱 0·test op 211,539(+252)·desc replace 전량 KO·엔트리 69,806. 배포: starbound.exe+server 실행으로 잠김 → _pak_replace_watch.log 3시간 재시도 루프, 게임 종료 시 자동 교체(재시작 필요).
| 2026-10-01 | LUSTLING-CODEX-REVIEW | - | 러스틀링 코덱스 11종 전면 재검수(data/lust_codex_review.txt EN/KO 병렬 덤프 → 수동 대조). 오역 교정: la-voe 주체 오역(여러분(voe)→라보에), fairer sex(더 나은 성→여성들), become a full protectorate(정식 보호국이 돼→정식 수호자가 돼)+Pro-Tect-Torate→수-호-자. 용어 통일: voe→보에, Tiuny→티우니, Naay→나이, cunt 톤 통일(창녀→년, 보지는 해부 용도 유지), Bill-C48i→빌-C48i, 이블린→에블린, 오르기→난교, 생식기→성기, 사정액→정액, Slaves-R-Us→슬레이브즈-알-어스. 스타일: 제노 핸드북 존댓말→해라체 통일(p8·p10), 광고 나레이션 다듬기(바보야→바보 같지), 참조 표기 실제 코덱스 제목과 일치(러스틀링 역사 I~VI). 레이아웃 복원: EN 제목 페이지의 선두 개행+들여쓰기 블록(수직 중앙정렬용)을 KO가 버린 10페이지 전량 복원(diary p0·p2, history1~6 p0, sorigins p0, xeno 챕터 표지 p0·6·11·15). 검수 파생 교정 2건: Piani→피아노(saloonpiano), Fuck Journal→섹스 기록(quillandink, 다이어리 코덱스 명칭과 통일). 검증: 11패치 115페이지 전수 — 악어휘 잔여 0·선두 블록 패리티 0·영문 잔여 0(DF/CSL 약어 의도 유지)·파싱 정상. tools/_lustling_codex_fix.py. 배포: zz_translation_female.pak 교체 완료(_codex_watch2.log 00:45:11).
| 2026-10-01 | LEGACY-REMAIN | rest_priority_1089 | legacy_remaining_candidates 잔여 미번역 큐 처리. 서베이 16,869행 → 필터 후 확인된 작업량 2,406필드(유니크 1,267) — GiC·Black Armory·Extended Story 중심. .behavior 런타임 파라미터·Replace Me 템플릿·식별자·기술값 제외해 실작업 2,336필드로 확정. 수동 번역 맵 tools/_legacy_ko_map.py 작성(1,267문자열): 종족 음성 관례 준수(플로란 ~엇/~샤·글리치 감정. 접두·노바키드 사투리·아비안 클루엑스·하이로틀 시적), 몬스터명 [대괄호] 번역, 용어집 정착(보호국·텔레포터·미니크녹·환상향·연합 시스템 등), ^색; 태그·%s·<placeholder>·^reset; 서열 보존, 선두 

 레이아웃 블록 유지. NYAN 마르퀴는 글자→냐 치환, 외계 문자 글리프 행 1건 의도 보존. 3개 .patch 출처 자산(제공자 패치 op 내부 문자열)은 제공자 op 경로 해석 후 동명 패치로 test+replace. 적용 tools/_legacy_apply.py: 1,124패치 파일에 2,334그룹 추가(신규 패치 248파일). 배포: 69,806→70,054엔트리, 교체 완료. 검증: 매핑 커버리지 1,266/1,267·적용 전수 실누락 0·제공자값↔test 샘플 400건 불일치 0·qa_structure 신규배치 이슈 0·qa_glossary fixed 위반 0(pak_pairs 298,921쌍)·context-rule 후보 67건은 산문 허용 범위로 문서화. 배치 TSV: translations/rest_priority_1089.tsv(1,265행, id 128808-130072), rest_worklist.tsv 동기.
| 2026-10-02 | PAK-REPAIR-STYLE | - | 배포 pak 직접 품질 수리(EN-shadow·깨진 태그·조사·잔여 EN). ①EN-shadow 신유형: test+replace KO 쌍 뒤에 무조건 EN replace가 같은 경로를 덮어 번역 무력화 — 149파일 186op의 뒤 EN write를 해당 경로의 기존 KO로 복원(eldermerchant 러브크래프트 대사·bow2 등 tooltip 20파일·무기명·greg 대사 등). KO 없이 EN만 쓰는 op 184건은 검토 후 대부분 의도값 판정(중국어 애국가 음역·R'lyehian·알타어·크레딧 명단·노래 제목·Replace Me 템플릿·ear style 스프라이트 그룹 키·Lorem ipsum·tree fiddy 유머) 유지, 실제 미번역 13op만 번역(fu_craftinfo 버그 메시지 2·akkimariscavenging 'insert item'·SkillMenu DisplayMessage|음악 다시 불러옴 6·제작대 단계명/부제 4). ②깨진 태그 전수 스캔·교정(33파일): 캐럿 없는 orange;/red;/green;/range; 9건, ^#CCD8B6 세미콜론 누락 6파일, 말미 ^reset 무세미콜론 2건(유형: Grain→곡물 병행), ^reset의→^reset;의 fu_t10 퀘스트 10파일, ^reset; 뒤 띄어쓴 조사(^reset; 를/은/을→붙임) 5건, mfgstation '^cyan이'+꼬리 파손 재번역. 단 test op 값은 상위 원문 보존이 원칙 — 첫 패스가 test까지 바꿔 MISMATCH 61건 발생 → test를 상위 final값으로 전량 재동기화하여 감사 정리. ③소량 스타일 교정: 조사 오류 4건(묶음를·숲를·숲가·숲와), '!.` 문장부호·말미 stray '.'·'..', U+200B 제로폭 공백 1건, horizonLiberator 중간 이중공백 3건, '사용을 중단하는 중입니다'→'사용이 중단되었습니다', outfitfitter_saturn 리터럴 '​' 텍스트+글리프 중복 제거, woodensifter '^cyan; 전력' 태그-공백 구조 교정. ④오탐 정리: 경계 넘는 괄호(PAREN)·번호 목록·의도적 반복(그렉체·더듬·구호)·EN 미러 손상(^white 무세미콜론·^green: 등 상위 동일)·받침 단어(찬가)·되는/돼 오탐(되죠)·로써 어법 전부 정상 판정. 검증: pak 재추출 299,485쌍·JSON 파싱 전량 정상·엄밀 test 감사 MISMATCH 0(ABSENT 21은 상위 키 소멸 정당 사자)·EN-shadow 잔여 0·용어 위반 0·동일-KO 팬아웃 잔여 0.
| 2026-10-02 | PAK-STYLE-PASS2 | - | 잔여 스타일 큐 차례 검수 완료. 교정: Stabber 계열 음차 통일(찌르기병→스태버·찌르개→스태버·적-찌르기→적 스태버, 5op/5파일), 마기사이트으로→마기사이트로 3op, outfitfitter_saturn /subtitle 리터럴  텍스트+글리프 중복 제거(object 2op·config 1op), '최고급 고급'→'고급 중의 고급' 2op(NpcMenu modConfig·v2). 검수 후 유지 판정: ENG_LEFT 잔여 330=학명(Lycoris radiata 등)·크레딧·명령어(insert/set/output)·모드명·라틴어 구절·S.A.I.L 약어 전부 의도값, DUP_PARTICLE eldermerchant '을을'=EN 'Llll' 더듬거림 미러, PAREN=페이지 경계 괄호, SPACE_PUNCT=EN 그롤릭스/??? 템플릿 미러, rosseo/geunom/many-things=정상 용법, 되어져·우리들은 류 중복 피동/복수 접미 0건. EXAMINE_POLITE 137건 유지 판정: 설명문 코퍼스의 존댓말 비율이 23%(9,969문장/43,352)이고 '세요' 지시문이 다수파 관례(1,274 vs 한다체 436)라 이질적이지 않음. TONE_MIX 잔여=인용+서술 조합·일기체 어조 변화로 자연스러움. 검증: 재추출 299,485쌍·용어 위반 0.
| 2026-10-02 | PAK-FANOUT-KOSRC + BANG | - | 재검토에서 신유형 발견·수리: 상위 제공자가 이미 한국어로 번역한 경로(test=KO)를 무관 한국어로 덮어쓴 팬아웃. test값은 검증된 상위 정본이므로 replace=test 복원. 바이그램 중첩 J<0.06 비대화 130경로 복원(avalitotem 종족검사·Icebud/피타야 씨앗·향 제단·공물·felintechstation/angeltechstation wakeUp·S.A.I.L 설명·chronicle-03 헤드라인·dem_vehicleshop 반대 의미·liquids류·broom·avaliglass·tripolarEssence 등), 중간대역 0.06~0.15 비대화 7경로 추가 복원(chronicle-02·kirikiripie 오큘레몬 오과일·techstation description·winejar·잔여 fluids). 대화 필드 132건은 의도된 재번역(상위 초벌 KO 개선) 판정 유지, 단 '수호자단'→'보호국' 용어 충돌 1건 교정. EN 말미 '!'→KO '.' 억눌림 72op를 '!' 복원. avaliplatform/stairs '아발리식 플랫폼/계단'은 객체에 정확한 서술이라 유지. 스캔 무결: 동일KO=EN 식별자열·빈KO·U+FFFD·%s+조사 접합 전부 0, 대화 저중첩 중 SAIL/재부팅 어휘 오염 0. 검증: 재추출 299,346쌍·엄밀 test 감사 213,844건 bad 0·용어 위반 0.
| 2026-10-02 | PAK-UNCOVERED | - | 커버리지 갭 번역 배치: 상위 final 47,740키 대비 pak 미커버 자연문자열 전수 번역 시작. 번역메모리 재사용 3,648필드 + 수동 배치(label/hint/okCaption 639op, caption/subtitle/senderName/npcname/petName/planetName/bookmarkName 1,402op, message 32op, completionText 29op, turnInDescription 130op). glitchDescription 1,503건 전량 번역(12청크, ~1,500op, 감정 접두 관례 유지: 분석./관찰./진술./흥미./무덤덤. 등, 고유명 알타어·학명·명령어 보존, 바이너리/이스터에그 원문 유지). 적용기 tools/_uncov_apply.py.
| 2026-10-02 | PAK-CHAIN-REPAIR + UNCOV-FINAL | - | 패치 체인 무결성 수리 + 커버리지 완결. ①원자 시뮬레이션(test 실패 시 패치 전체 중단) 기준 귀속으로 zz first-fail 자산을 반복 수리: 중첩 3단계 op 구조의 중복 writer 그룹 제거(drop_dup)·missing 경로 op 제거·test를 상위 적용 시점 상태로 재동기화 — 79+6+98+164건 누적 처리 후 zz first-fail 0·체인 중간 zz 실패 0. ②베이스 파서 보강: BOM(utf-8-sig)·문자열 내 생 제어문자 허용 — noparse 112건 해소로 숨어있던 미커버/실패 노출 후 정리. ③미커버 번역: platform2.matitem 4필드 + trans+ 계열(통째 번역팩) 잔여 영어 표시 필드 47op(이몰레이터/몰리/대응요원/제압요원 방어구·스타포지 검사문). ④타 번역팩 실패 잔재 커버: localeko/sbkor 패치 중단으로 영어로 남던 cockpit 광물·날씨·행성 표시명 25건+제작대 레이블 1건을 zz 후순위 패치로 커버. ⑤용어 QA 152위반 → 3 오탐(Def Leppard·Def'nitely): 미니크녹·에스더·새터니안·방어력·소검·바이올륨·고위 수호자·텔레포터·제작대·포털·피스키퍼·붕붕마루·연합 시스템·제르세슘·방패 강타·컬티베이터·생크틸라이트·에지·파리스·오카서스·행성 보호국·미탐험 구역·돌격소총·패링·러스틀링·바쉬·텔레안·피규어·노마다·기트신·에지솔트 교정 + 부수 실결함 r_impervious 설명 내용소실 복원·faryth 중복 op 정리·ct_onitti_cake 미완성 문장 보완·r-moonmodel Erchius 오역(예언→에르키우스). 최종: text 61,194자산 covered 60,946·uncovered 233(전부 식별자/경로/이미-KO trans+ 파일)·broken 15(타 번역팩 자체 결함, 체인 끝 영어 표시 필드 0 확인)·용어 위반 실질 0.

| 2026-10-02 | PAK-MECH-QA | - | 배포 pak 기계적 품질 검수(_qa_mech.py, 323,596쌍). 실결함 교정: ①엔진 입력토큰 번역 소실 6건 복원 — [ALT-FIRE]→[보조 사격] 된 것 3건(psychic_translocator·debug·strangepucklauncher), [SPACE]→[스페이스] 2건(gravitybubble·rocketboots), [LMB]/[RMB]→[좌클릭]/[우클릭] 1건(relicSlot). ②PUA 글리프 소실 19건 복원 —  승급 아이콘(이몰레이터·몰리·대응요원·제압요원·voidstuff 방어구),  체크 아이콘(outfitfitter_saturn). ③번역 절단 마커 손상 9파일 복원 — `|내장...`(security_helmet 프리셋 4건), `|^gray;어디...`(bandana 습득처), `^Red...`(makeshift/skathfusionreactor 냉각수·왼쪽입력 블록), `|^cyan;연구 속도^...`(precursordatabox), `계산...`(avalihammock BYOS 전용), mystichammer 설명의 ^red;물리 피해^reset; 행 소실+shortdescription에 스탯행 침입 교정. ④소비재 `^green;유형: 과일^reset;` 소실 4건(chesto/pecha 주스·베리), `^yellow;원심분리 가능^reset;` 2건(액체), gunsmithshop/medievalworkstation 색태그 복원, isn_thermalgenerator `^orange;가열...^reset;`+`^blue;왼쪽 입력^reset;` 블록 복원. ⑤`|`가 개행 대용으로 박힌 4건 
 교정(omech_Chitoy1/4·omech_shop·om_starryplush3). ⑥수치 결함: respawnhardcore 50%→30% 오기 교정(전 종족 변형 파일), missioncryotomb `(7)` 카운터 소실 복원. 오탐 판정: mmupgrade `by N%`→`N+100%로` 정확한 해석, 용어집 수사 표기(만 년·4만 등), 섭씨 환산(3,000°F→1,600°C), [NORMAL]/[CHEST]/[DEPRECATED] 등 표시 라벨 번역, changeling [Specal 1] 오타 교정, lamia/arcanian 종족 스탯 템플릿 차이(자체 완결), ^rseet;/^oange;/^EDB347; 상위 오타 정정. 검증: 재추출 323,596쌍·pua_lost 0·입력토큰 실소실 0·tag_lost 7(전부 오타 정정/템플릿 차이)·zz 체인 실패 0(잔여 10건=localeko/sbkor 자체 결함).
