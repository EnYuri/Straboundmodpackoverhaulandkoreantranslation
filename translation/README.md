# Starbound 한국어화 작업 폴더

활성 모드의 미번역 문자열을 한국어로 옮기는 작업 폴더다. 번역 원본은 `translations/*.tsv`이다.
적용된 번역은 `mods/zz_translation_female.pak`(sbkor·FU_KO·localeko 계열 병합 + 신규 번역)이며,
갱신 적용은 `apply_rest.py`가 오버레이 생성과 모드 pak 재패킹으로 수행한다. 이 폴더는
2026-09-26에 `tmp/`에서 `translation/`로 이동했다.

## 문서 구성

- `README.md`(이 문서): 작업 절차, 진행 현황, 반복 실수 방지 규칙
- `../HANDOFF.md`: 한국어화 작업 인계 문서(`apply_rest.py` 적용 절차 포함, 구 인계 문서 18~35절 이력)
- `../STARBOUND_KO_GLOSSARY.md`: 용어·말투 기준 (정본)
- `../../../MOD_MAINTENANCE_HANDOFF_2026-09-21.md`: 모드 유지보수 전체 인계 문서
- `docs/batch_log.md`: 배치별 작업 메모(최신순). 새 배치 기록은 이 파일 맨 위에 추가한다.
- `docs/project_history.md`: 기준선 추출·정렬·오버레이 시험 등 초기 이력(2026-09-21 ~ 09-23)
- `data/translation_glossary.tsv`: `qa_glossary.py`가 강제하는 고정 용어
- `drafts/0359_0370/`: 배치 0359~0370의 검수된 병합 초안과 0365 긴 항목 생성 스크립트 보관
- `drafts/review_2/`: 2차 재검수 때 쓴 변환·스캔 스크립트와 검토 출력물 보관(`_` 접두사 일괄)

## 폴더 구조 (2026-09-30 재편)

루트에는 문서(`README.md`·`AGENTS.md`·`LICENSE`)와 아래 디렉터리만 둔다.

- `tools/`: 모든 파이썬 스크립트 — 유지보수 도구(`extract_pak_pairs.py`·`write_pak.py`·
  `qa_pak_*.py`·`qa_structure.py`·`qa_glossary.py`)와 이미 적용이 끝난 `fix_*_batchNN.py`
  패치 기록. 스크립트는 **반드시 이 폴더가 아닌 저장소 루트에서** 실행한다
  (`python tools/qa_pak_glossary.py`처럼). 데이터 파일 참조는 `data/` 접두사 기준.
- `data/`: 활성 데이터 — `pak_pairs.tsv`(pak 추출 쌍), `rest_worklist.tsv`·워크리스트,
  `translation_glossary.tsv`, QA 리포트, `approved_names.txt` 등 레지스트리.
- `archive/`: 참조가 끊긴 완료 캠페인 중간산출물(구 워크리스트·glitch/novakid 재작성
  출력·stale pending 스냅샷 등). 삭제 대신 보관.
- `backup_paks/`: pak 백업과 구 스테이징 산출물(`*.REVIEW_PENDING`·`*.NEW*`·
  `*.NORMALIZED`·`*.deployed-bak` 등). 2026-09-30 정리에서 내용은 전량 삭제하고
  디렉터리만 유지한다 — 롤백이 필요하면 현재 배포 pak과 git 커밋 이력이 기준점이다.
- `scratch/`: 일회성 분석 스크립트·덤프·검증 출력(`_` 접두사). 유지보수 경로에서
  참조되는 것만 남겼다(`_dialog_polite_dryrun.py` 등).
- `translations/`·`drafts/`·`docs/`·`alignment/`·`corpus/`·`inventory/`·`qa_review/`:
  기존 위치 그대로.

상위 `translation/` 폴더의 구형 작업 디렉터리 4개(`translation-fix-20260921`,
`noneki-spanedit-20260922`, `replaced-installed-20260922`, `translation-overlays-20260921`)는
`../_archive/` 아래로 통합했다가, 2026-09-30 디스크 정리에서 `_archive/`째로 전량
삭제했다. 롤백 백업까지 포함해 삭제한 근거: 모든 번역 결과가 배포 pak
(`mods/zz_translation_female.pak`)에 반영돼 있고 TSV 원본은 git 이력에 있다.
이후 `replaced-installed-20260922` 등을 참조하는 구 스크립트·문서 기술은 이력 기록으로만
취급한다.

주의: `tools/fix_dialog_polite_batch39.py`는 `scratch/_dialog_polite_dryrun.py`를
임포트하며, 그 모듈은 `data/style_mix_*.tsv`·`data/pak_pairs.tsv`·`tools/fix_race_polite.py`에
의존한다 — 루트에서 실행해야 경로가 맞다.

## 진행 현황 (최신 갱신: 2026-09-29, energyFormat MJ 단위 누락 계열 버그 전량 수정(28차) 완료)

- **[해결됨] EN/KO 단위·포맷 지정자 전면 대조(28차, 3건)**: 27차에서 발견한 `energyFormat`
  MJ 단위 누락이 다른 자산에도 반복됐는지 확인하기 위해 pak_pairs.tsv 전체
  186,213쌍에 대해 printf 포맷 지정자(%d 등, 불일치 0건)와 단위 토큰(MJ·kg·%·HP 등)
  대조를 실행. 노이즈(HP-조사 결합 시 단어 경계 정규식 오탐 등)를 걷어내고 나니
  같은 "Energy: %d MJ" → MJ 누락 패턴이 `sgspidermechstation`·`xscm_config`(2개)
  자산 3곳에 각각 독립적으로 반복돼 있던 것을 확인, 전부 수정. 이로써 pak 내
  `energyFormat` 계열 MJ 누락 버그(총 4자산)는 전량 해결됨. 상세는 `docs/batch_log.md`
  "2026-09-29 (28차): fix_glossary_batch23" 항목.
- **[해결됨] sbkor.tsv 메인 pak 전체 대조(27차, 1건)**: NonEKI 검수에서 효과를 봤던
  "바닐라 sbkor.tsv EN 원문 대조" 기법을 메인 pak(pak_pairs.tsv 326,000쌍)에 처음
  적용. EN 완전일치 640건 중 대부분은 이 pak이 독자 번역이라 생기는 정상적 문체 차이로
  확인됐고, 단위/플레이스홀더(MJ·kg·%·HP 등) 손실만 정규식으로 재필터해 진짜 버그 1건
  발견: `arcana_mechassemblygui.config.patch`의 `/energyFormat`에서 "MJ" 단위가
  누락돼 있던 것을 확인·수정(같은 자산의 `/drainFormat`은 정상 유지해 비일관성으로
  발견). 이 기법은 메인 pak 전체 대상으로는 신호 대 잡음비가 낮아(640건 중 1건) 향후
  전면 재적용보다는 좁힌 후보군에 대한 보조 기법으로 활용 예정. 상세는
  `docs/batch_log.md` "2026-09-29 (27차): fix_glossary_batch22" 항목.
- **[해결됨] 용어집 재스캔(25차, 37건) + 구조 QA 신규 기법 도입·콘텐츠 불일치 1건 수정(26차)**:
  23차 커스텀 종족 캠페인 이후 `qa_pak_glossary.py`를 재실행해 스캔 사각지대에 있던
  최신 위반 37건(주로 커스텀 종족 설명문에 실린 확정 용어 미준수)을 발견, `fix_glossary_
  batch20.py`로 전량 수정해 위반 0건 확인. 이어서 `qa_pak_context.py`의 기존 카테고리
  (UNTRANSLATED/TRUNCATED/DUP_PARTICLE/LITERAL)를 재점검했으나 모두 확립된 오탐 포화
  상태였고, STYLE_MIX(오브젝트 조사 대사 어조 혼입)는 사용자 지시로 후순위 처리 중이라
  새 검증 기법을 시도: pak_pairs.tsv 279,703쌍 전체에 `^color;` 태그·`<Token>`·
  `[Bracket]` 힌트의 EN/KO 멀티셋 대조(`_qa_pak_structure.py`)를 실행해, 후보 약
  9,200건 중 실제 EN이 존재하는 것만 추려 육안 검토한 결과 진짜 버그 1건을 발견:
  `esc_realisticapex.species.patch`의 캐릭터 생성 툴팁이 고유 영문 로어 대신
  `apex.species.patch`(빈-EN 자체 추가 flavor)의 한국어를 그대로 복사해 전혀 다른
  내용이 노출되고 있었음. `fix_glossary_batch21.py`로 해당 자산만 스코프 지정해 수정
  (동일 문자열이 두 자산에 우연히 일치해 첫 실행 시 둘 다 바뀌는 것을 확인 후 재수정).
  나머지 구조 QA 후보는 전부 EN 소스 자체 오탈자이거나 대괄호 UI 라벨의 의도적 번역
  관례로 확인돼 수정하지 않음. 상세는 `docs/batch_log.md` "2026-09-29 (25차):
  fix_glossary_batch20" 및 "2026-09-29 (26차): fix_glossary_batch21" 항목.
- **[해결됨] NonEKI 별도 검수**: 오랫동안 "미실행"으로 기록돼 있던 `repack_noneki_
  translation.py` 파이프라인을 재점검하려다, 설치된 `mods/NonEKI_9_FU_compat.pak`을
  직접 열어보니 **이미 거의 전량(표시 문장 93/98) 한국어로 번역돼 있음**을 발견(과거
  기록이 stale했던 것으로 추정). 바닐라/FrackinUniverse/Saturnians 등 원본 pak과 대조해
  심하게 깨진 기계번역 17건(함선 업그레이드 면허 퀘스트 9건 + 미션 좌표 무전 7건 + 1건)을
  발견, 전부 바닐라 원문과 동일함을 확인해 sbkor.tsv의 기존 고품질 번역으로 교체(용어집
  충돌 1건만 "미니크녹 요새"로 보정). 나머지 76건은 자연스러운 의역으로 확인돼 추가 수정
  없음. 상세는 `docs/batch_log.md` "2026-09-29 (NonEKI 별도 검수)" 항목.
- **[DEPLOYED] Pak re-review (batches 22-34)**: The reviewed pending pak was promoted to
  `mods/female_translation.pak` after final approval. The pass corrected contextual glossary misuse,
  proper names, source-content mismatches, malformed input tokens, repeated mistranslations,
  model-number corruption, race registers, Alta and Elithian world terminology, formatting around
  runtime placeholders, glossary-term particles, and confirmed loanword spelling errors. The
  deployed pak passes extraction and glossary QA and completes an OpenStarbound server database load.
- **[해결됨] 재검수 보류 2건 + 고정 용어/오역 정리 + JSON 패치 파싱 오류 수정(24차)**:
  `gic_militarytransport`의 원문을 원본 GiC pak에서 복원해 종족별 말투와 누락된 공용·Avikan·Aegi
  설명을 교정했고, Alta latch에 다른 논리 장치 설명이 혼입된 3개 필드를 원문에 맞게 복구했다.
  커스텀 종족 배치의 Aegi 162자산(`아에기→에지`), Union flag, Thelean, Saturnian 표기를 정본으로
  고쳤으며 Cultivator 2건, Terrene Protectorate, Floran 내용 불일치 9건, 제작대와 Elithian 제작대
  명칭, Trink Circuit, GiC 무기 설명의 개행·`패링`·`한손`, Old One 문맥을 추가 정리했다.
  OpenStarbound 로그에서 실제 실패한 `RPGskillbook`, `perfectlygenericitem`, `blindweed` 번역 패치
  3개만 평면 연산 배열로 정규화했다. 전체 패치 평탄화는 조건부 그룹 의미를 훼손하므로 폐기했다.
  최종 OpenStarbound 클라이언트 전체 데이터베이스 로딩과 타이틀 화면 진입을 확인했으며
  `female_translation` JSON 파싱 오류는 0건이다.
- **[완료] 커스텀 종족 `<raceid>Description` 신규 번역 캠페인(23차)**: 사용자가 게임 내
  실사용 중 Lustling 오브젝트 조사 대사가 미번역임을 지적, 원인 추적 결과 `scan_remaining.py`의
  `VISIBLE_KEYS`가 바닐라 7종족 키만 인식해 커스텀 종족의 자기소개 조사 대사 전체가
  스캔 사각지대였음을 발견(17,575행/고유 7,888종/약 90종족/50개 pak, 전부 0% 번역).
  `translations/customrace_unique.tsv` + `dump_customrace.py`(출현빈도 내림차순 배출) +
  `apply_customrace.py`(`pak_writer.py`로 female_translation.pak 직접 갱신) +
  `qa_customrace.py` 파이프라인 신설, 기존 `rest_*` ID 공간과는 독립. 7,888/7,888종
  (100%) 번역 완료(batch_0001~0058), pak 반영 자산 4,892개. 신규 종족 착수 전 batch_0003~0006 등
  초기 기록을 먼저 확인해 기존 문체 재확립 오류를 방지하는 절차 추가(hymid/jorgasian/notix
  약 645건 문체 오류 발견 후 전면 수정, 상세는 `docs/batch_log.md` "23차 문체 오류 수정" 항목).
  마지막 batch_0058(207종)에서 PUA 아이콘 글리프(U+E000~U+E0FF) 보존 사례(id 7874) 발견·대응.
  상세는 `docs/batch_log.md` "2026-09-29 (23차 계속29, batch_0058)" 항목.
- **[해결됨] 글리치·노바키드 조사 대사 존댓말 정규화(22차, 1,667자산)**: 20~21차 QA 중
  발견한 체계적 패턴. 전체 pak glitchdescription/novakiddescription 필드 13,567개를
  정규식 재스캔해 해요체/합쇼체 위반 1,626행(글리치 1,034·노바키드 592) 플래그, 영문
  원문과 페어링 후 fork 5개(글리치3+노바키드2)에 재작성 위임. 15행은 오탐으로 확인돼
  원문 유지, 나머지 1,611행을 STARBOUND_KO_GLOSSARY.md 규칙("감정어. 본문" — 감정어는
  명사, 본문은 `-다`체/노바키드는 `~구만` 계열 반말)에 맞춰 재작성(단순 어미 치환이
  아닌 활용형 교정) — 고빈도 공유 문구가 다수 자산에 재사용돼 적용 자산 수는 1,667건.
  부수로 `faster'n 'light drive`(초광속) 오역("가벼운 드라이브") 1건도 동시 수정. 상세는
  `docs/batch_log.md` "2026-09-28 (22차)" 항목. **사용자 지시로 이 배치를 끝으로 오브젝트
  조사 대사(글리치/노바키드 description류) 검수는 후순위 전환**, 다음 우선순위는 아래
  보류 항목.
- **[해결됨] 선원→승무원 전역 판단 + STYLE_MIX group2/3 재개 + 플랫 패치 사각지대 초기
  검수(20~21차, 41자산)**: 사용자 지시로 3개 보류 과제 처리. ①선원→승무원은 바닐라
  sbkor의 함선 승무원 UI가 이미 "승무원"으로 일관 번역돼 있음을 근거로 함선 crew 기능
  관련 30자산을 승무원으로 교정(진짜 뱃사람 문맥 sailor/Sailor Set/Privateer는 선원
  유지). ②STYLE_MIX 비-/dialog/ 잔여 67자산/1,397행(12차 추정보다 축소돼 있었음)을
  fork 2개로 재검수, 확정 오류 5건(팔케 장군 존댓 이탈, surcis→심사 오역, SWAT 표기
  불일치, Butane Cassidy/Mox Fulder 표기 불일치) 수정. ③test 가드 없는 "플랫" 패치
  3,680개 중 원본 pak 대조로 3,275쌍 복원해 fork 2개로 첫 검수, 확정 오류 3건
  (SPECIES→원형 오역, abyssvortex 오타, DUELLIST 특성 라벨 미번역) 수정. 상세는
  `docs/batch_log.md` "2026-09-28 (20~21차)" 항목. **실게임 검증은 전체 검수 완료
  후 최종 단계로 보류(사용자 지시)**.
- **후속 보류 갱신**: the Ancients/Eithne/Magicite/K'Rakoth 표기 통일은 batches 22-25에서
  해결됐고(Eithne 44건→에이트네, the Ancients 95건, Magicite 136건→마기사이트, K'Rakoth
  잔여 표기), `gic_militarytransport.object.patch`/`alta/wired/logic/latch.object.patch`
  버그 2건은 24차, NonEKI는 2026-09-29 별도 검수에서 해결돼 이 문단의 과거 보류 목록은
  전부 소진됐다. 남은 것은 플랫 패치 3,680개 중 원본 미복원 잔여분(cinematic류 비-strict
  JSON 등 기술적 한계)뿐이며, 오브젝트 조사 대사류(글리치/노바키드 description) 검수는
  여전히 후순위다.

- **[해결됨] fork 기반 정독 QA 그룹0·그룹1(15자산, 14건)**: 용어집 기계 대조 방식이 반복
  재실행에도 신규 발견이 없이 정체되자, 사용자가 "우린 비효율적으로 간다"/"이 거 번역한
  문자열이 수십만개다"라고 지적. 좁은 휴리스틱 스캔과 사용자의 수동 지적 둘 다 확장 불가능
  하다는 판단 아래, `qa_pak_context_report.tsv`의 STYLE_MIX(다중 화자 대사) 미검토 76개
  자산군을 fork 서브에이전트가 실제로 정독(comprehension)해 확인하는 방식으로 전환. 4개
  그룹 중 group0·group1(2,720행/39자산) 실행 완료, 실제 오류 14건 확인 후 수정(Leda
  Portia/Qingque Tea Brewer 명칭 통일, Officer→경관, Beacon→비컨, Bridge→함교 오역 수정,
  Mox Fulder/Agent Fulder 인명 통일, "갈갈이"→"갈가리" 오타, "님" 단독 호칭→대장님, 유물
  탐색단/탐구자 통일, 조사 누락 비문 2건 재작성, 아케인/비전 촉매 통일 + 손상 색상 태그
  복구, partner→파트너, target→목표 통일). group2·group3(나머지 39자산, ~2,716행)는
  사용자 지시로 미실행 보류 상태. 서버 부팅 검증 통과(`[Error]` 0건). 상세는
  `docs/batch_log.md` "2026-09-28 (12차)" 항목.
- **[해결됨] Protector 용어 변경(107자산)**: 사용자 지시로 "Protector"(문맥형 용어)도
  "수호자"로 통일. 프로텍터(57건, 압도 다수) 일괄 치환 + 보호자(bare, 31건 중 원문이
  실제로 "Protector"인 16건만) 개별 타겟 치환. 오토프로텍터/EDS 프로텍터/테레네
  프로텍터레이트는 형제 용어 일관성·기존 결정 유지 위해 예외 처리, "caretaker"를 뜻하는
  일반 단어 "보호자" 6건은 무관하여 미변경. 서버 부팅 검증 진행 중. 상세는
  `docs/batch_log.md` "2026-09-28 (11차)" 항목.
- **[해결됨] Grand Protector 용어 변경(92자산)**: 사용자가 "대보호자"가 부자연스럽다고 지적,
  "고위 수호자"로 변경 지시. `translation_glossary.tsv` 갱신 + pak 전체 92건 재치환, 서버
  검증 진행 중. 상세는 `docs/batch_log.md` "2026-09-28 (10차)" 항목.
- **[해결됨] 용어 배치5(9자산)+배치6(4자산)**: Ruin-Killer/Thrust Damage/Broadsword/
  Zerchesium/United Systems/Droden/Knockback/Fusion Chamber(배치5), Aventor/Hymidian
  Republic of Hyzolia/Triple Monarchy(배치6, Elithian Alliance 배너 계열 롱테일) 수정, 서버
  부팅 검증 통과. 이 시점 잔여 용어집 위반은 전부 이전 배치에서 오탐/판단 보류로 확인된
  항목(Materials Available/Miniknog Stronghold/Alliance 일반 관용구/Floran/Kappa/Old One/
  Pixels/Fuel Hatch/One-Handed/Trink 등)이라, `rule=fixed` 용어집 기계 대조 기준으로는 사실상
  수렴했다. 상세는 `docs/batch_log.md` "2026-09-28 (8차)/(9차)" 항목.
  - 문서화 사고 및 복구: 항목 순서를 바로잡는 편집 중 실수로 `docs/batch_log.md` 전체를
    덮어써 (3차)/(2차)/(1차)/Plushbound 등 과거 이력이 삭제됐으나, 사용자가 보관 중이던
    터미널 트랜스크립트 사본으로 전량 복구했다(5,547줄, 2026-09-26까지).
- **[해결됨] 용어 배치4(132자산)**: 6차 이후 재추출·재스캔한 잔여 위반 374건 중 Grand
  Protector(대프로텍터/대호보자/대수호자 전부 → 대보호자로 완전 통일, 79건 다수파와 합류),
  Relic Seeker(금지어 렐릭 시커 잔존분 → 유물 탐구자), Thelean/Protectorate/Elithian
  Alliance 잔여 변형, Aegisalt/Magilock/Magishot/gheatsyn/Kel'chis/Jorgasian/Notician
  Federation/Mehros Avan/Trink Circuit/Crafting Station/Sniper Rifle/Quietus 등을 수정.
  서버 부팅 검증 진행 중. 조사 후 의도적으로 유지한 항목(Old One/Floran/Trink/Spooked/
  One-Handed/Fuel Hatch의 성인 콘텐츠 말장난 가능성/Miniknog Stronghold)은
  `docs/batch_log.md` "2026-09-28 (7차)" 항목에 판단 근거와 함께 기록.
- **[해결됨] 아이템 이름/설명 우선 전수 용어집 검수로 전환** (2026-09-28, 6차). 사용자 지시로
  5차의 STYLE_MIX 대사 뱅크 전수 검토를 중단하고, `qa_pak_glossary.py`(`translation_glossary.tsv`의
  `rule=fixed` 고정 용어 전수 대조)를 아이템명/설명 검수의 주 도구로 채택. 이후 명백한 문제가
  없는 한 승인 대기 없이 계속 진행하는 방침으로 전환.
  - **텔레포터**(40건, 순간이동 장치→텔레포터), **용어 배치2**(265자산: Poptop/Drahl/Vaash/
    Thelean/Centens/Peacekeeper/Protectorate/Elithian Alliance), **용어 배치3**(249자산:
    Assault Rifle/Grenade Launcher/Erchius/Novakid/Saturnian/Telebrium/Hymid/Enerth
    Engineering/Parry단독형 + Kappa 1건 + Two-Handed 오역 4건 + Aeginian 어간 통일)까지
    총 554개 자산 수정, 각각 서버 부팅 검증 통과(`[Error]` 0건).
  - **알려진 한계(미해결)**: `.patch` 자산의 ~6%(약 3,680개)가 test/replace 쌍 없는 "플랫"
    JSON 구조를 써서 `extract_pak_pairs.py`/`qa_pak_glossary_report.tsv`에서 누락되는
    사각지대 발견(`protectorateflagpole` 수작업 대조 중 발견). 수정 스크립트 자체는 원시
    바이트 스캔 방식이라 영향 없으나, 탐지 단계 개선은 후속 과제.
  - 판단이 필요했던 용어 충돌 사례(Kappa 종족 vs 코덱스 그리스문자 표기, Aeginian 세 어간
    공존 등)의 근거와 남은 "Miniknog Stronghold" 판단 보류 건은 `docs/batch_log.md`
    "2026-09-28 (6차)" 항목 참고.
- **[해결됨] 전체 배포 pak 대상 문맥/어조 체계적 재검수** (2026-09-28, 5차). 사용자가
  인게임에서 발견한 "심각한 문장"을 계기로, `extract_pak_pairs.py`로 `mods/
  female_translation.pak`의 test/replace 쌍 182,157건을 전부 추출하고
  `qa_pak_context.py`(6개 휴리스틱: STYLE_MIX/UI_LENGTH/LITERAL/DUP_PARTICLE/TRUNCATED/
  UNTRANSLATED)로 전수 스캔했다.
  - UNTRANSLATED/LITERAL/DUP_PARTICLE 3개 카테고리는 표본 검증 결과 **전부 오탐**으로
    확정, 폐기(신호 대 잡음비가 pak 전체 규모에서는 너무 낮음).
  - TRUNCATED(62건) 육안 대조로 **실제 콘텐츠 손실 버그 2건군, 총 12개 자산**을 발견·수정:
    `nonEKIaichip` 함선 상태 대사 4건(후속 문장 전체 유실), `sb_techstation` 7종족 +
    `letheia_extra_21`의 "파괴 시 파손" 경고문 8건 누락. `fix_content_drop_bugs.py`로
    수술적 패치(수정 전 값을 `assert`로 확인 후에만 교체), 서버 검증 통과.
  - STYLE_MIX 표본(`viera.config`) 육안 검토 중 별도로 **커맨드먼트 오타 1건**(존재하지
    않는 활용형 "따르기라") 발견, `angellore5`/`angellore11` 두 codex에 중복 존재하던 것을
    `fix_commandment_typo.py`로 수정.
  - STYLE_MIX 142개 자산군 중 `/cinematics/`·`/quests/` 65개군(약 450행) + `viera.config`
    (1,364행)까지 육안 전수 검토 완료 — 위 오타 1건 외 신규 버그 0건. 나머지 77개군은 전부
    `alta.config`(734행) 등 대형 다중 화자 NPC 대사 뱅크로, 원래 종족·개인별 말투가 섞이도록
    설계돼 있어 적중률이 낮다(효율 대비 저조).
  - **남은 작업**: STYLE_MIX 나머지 77개 대형 대사 뱅크는 사용자가 특정 문장을 짚어주면
    표적 확인하는 방식을 권장. NonEKI는 별도 파이프라인이라 이번 스캔에서 빠졌을 가능성 —
    별도 재검토 필요.
  - 상세는 `docs/batch_log.md` "2026-09-28 (5차)" 항목.
- **[해결됨] `zz_localeko_elithian/krakoth/nuggubs/plushbound_low_20260927.pak` 4종을
  `female_translation.pak`에 병합 완료** (2026-09-28, 4차). 병합 전 두 pak이 공유하는 1,558개
  자산 경로 전체를 JSON 포인터 단위로 전수 대조해 충돌 0건(전부 같은 파일의 서로 다른 종족별
  설명 필드)을 확인한 뒤, patch-group 리스트를 이어붙이는 방식(`merge_low_paks.py`)으로 안전하게
  병합(58,996 → 59,062개 항목). 병합된 4개 pak은 `mods/`에서 제거해
  `translation/replaced-installed-20260922/low_paks_merged_20260928/`로 옮겼다(중복 적용 방지).
  `zz_localeko_highpriority_20260927.pak`은 이번 병합 대상이 아니라 `mods/`에 그대로 유지된다.
  서버 부팅 검증(`0.0.0.0:21025` 리스닝 도달, `[Error]` 0건) 통과. 상세는 `docs/batch_log.md`
  "2026-09-28 (4차)" 항목.
  - **남은 확인 사항**: 4개 모드의 용어집 위반 163건(주로 Teleporter→"순간이동 장치")은 이번
    작업에서 정정하지 않았다. 별도로 처리 필요.
  - `scan_remaining.py`의 `load_coverage()`는 옛 4개 pak 파일명을 그대로 두어도 무해하다(존재하지
    않으면 건너뜀, `female_translation.pak` 항목이 커버리지를 대신 제공) — 스크립트에 주석으로
    기록해 둠. 상세는 아래 "다음 세션 재스캔 전에는..." 항목 참고.
- **[중요, 해결됨] 배포 중인 `mods/female_translation.pak` 자체를 test/replace 174,095쌍 전수
  스캔해 플레이스홀더(런타임 치환 태그) 손상 87건을 추가로 발견·수정함** (2026-09-28). `<slots>`
  (상자/액체탱크 용량, 63건 — TM 정렬 충돌로 서로 다른 용량의 63개 자산이 전부 "슬롯 60칸"으로
  하드코딩돼 있었음), `<role>`(선원 계급, 18건 — 닫는 괄호까지 누락된 채 한글로 오역), `<selfname>`
  (4건), 존재하지 않는 가짜 태그 삽입(1건), 퀘스트 진행도 `<itemName>`/`<current>`/`<required>`
  (1건) — 전부 실제 게임에서 깨진 문자열이나 틀린 수치로 노출됐을 버그. `patch_female_translation_pak.py`와
  같은 수술적 방식으로 pak을 직접 수정, 서버 부팅 검증 통과. 상세는 `docs/batch_log.md`
  "2026-09-28 (3차)" 항목.
- **[중요, 해결됨] `apply_new_translations.py`/`refresh_translations.py`의 CSV 파싱 버그 +
  개행 이중변환 버그로 다중 문단 번역문 다수가 손상돼 있던 것을 발견·수정하고
  `mods/female_translation.pak`까지 재조립 완료함** (2026-09-28). ①`load_korean()`이 CSV
  인용 규칙을 모르는 정규식 라인 파서라서 개행 포함 항목(1,190행) 앞뒤에 리터럴 `"` 문자가
  번역문에 박혀 있던 문제(1,324건), ②이미 `\r\n`을 담고 있던 항목에 `\n`→`\r\n` 치환을
  중복 적용해 `\r\r\n`이 되던 문제(1,069건) 총 2건의 파이프라인 버그를 스크립트 수정으로
  해결하고 `translation-overlays-20260921/source-v3/`를 완전히 재동기화(`want/updated/
  missing-file` 0 수렴). `build_pak.py`가 요구하는 스테이징 경로(`E:/pakx/*`, premerge pak)는
  일부만 다른 경로(`translation/replaced-installed-20260922/`)에서 찾았고 `E:/ft_src`는 끝내
  못 찾았지만, 전체 재조립 대신 **현재 pak을 베이스로 GiC/BA/ES 3개 오버레이만 덮어쓰는
  수술적 패치 스크립트**(`patch_female_translation_pak.py`)로 안전하게 반영(3,654개 항목
  교체+26개 신규, 백업 후 교체, 서버 부팅 검증에서 관련 오류 0건). 상세는 `docs/batch_log.md`
  "2026-09-28 (2차)" 항목.
- **신규 번역 전체 체계적 재검수 1차 진행 중** (2026-09-28, Plushbound 완주 직후 사용자 지시로 착수,
  범위: 기존 유저번역 sbkor/FU 제외 전량). 핵심 성과와 방법론적 교훈은 `docs/batch_log.md`
  "2026-09-28: 신규 번역 전체 체계적 재검수 (1차)" 항목에 상세 기록. 요약:
  - **[매우 중요] `translations/rest_*.tsv`류를 id로 재검수하는 방식은 무효.** `rest_worklist.tsv`가
    프로젝트 기간 중 여러 번 재생성되어 id 번호가 스냅샷마다 다른 문장을 가리킨다. 실제 게임 적용
    스크립트(`apply_rest.py`)는 id가 아니라 **영어 원문 텍스트를 키**로 매칭하므로(`test` op 가드
    포함), id 불일치가 곧 게임 오류를 의미하지 않는다. **앞으로 이 계열의 품질 검증은 반드시
    완성된 pak을 `pak.py`로 직접 열어 test/replace 쌍의 EN/KO 내용을 표본 확인하는 방식으로만
    한다.** (`female_translation.pak`은 58,921개 patch 자산·200,887쌍 중 무작위 표본 검사 결과
    이상 없음 확인됨.)
  - Elithian/K'Rakoth/nuggubs/Plushbound 4대 완주 모드: 구조 QA 사실상 0건, 용어집 위반 163건
    발견(대부분 Teleporter→"순간이동 장치") 및 검토 완료.
  - **조사(助詞) 불일치 버그 75건 발견·수정**: `미니크노그`→`미니크녹`, `노바킨`→`노바키드` 용어
    일괄 치환 시 받침 변화로 뒤따르는 조사(은/는·이/가·을/를·과/와)가 깨진 사례. 61+143개 파일
    전수 스캔 후 수정, 4개 오버레이 pak 재빌드로 반영 완료.
  - `worklist_new.tsv`→`translations/batch_*.tsv`(진짜 고우선: codex 111+shortdescription
    1,736+questtemplate 445, 총 6,700행) — **stray line 손상 3,116건 복구**(CSV 따옴표 누락으로
    다중행 항목이 id 없는 고아 줄로 쪼개져 있던 문제), `[CRIT]`/`[ALT]` 키바인드 태그 오역 38건 수정.
  - **(2026-09-28 (2차)에서 완료) `batch_*` 미번역 188행 재조사·해결**: 실제로는 187건이
    `qa_all.py`의 "헤더 오인" 버그로 인한 허위 누락(수정 완료, 아래 참고)이었고 진짜 누락은
    `batch_5360_5499.tsv` 전체 140행 — 전량 번역 완료. `worklist_new(batch)` 그룹 용어집 위반도
    190→58건으로 정리(세력명 Protectorate/United Systems 등 대규모 불일치 포함). 상세는
    `docs/batch_log.md` "2026-09-28 (2차)" 항목.
  - **미해결 남은 작업**: `missed_worklist.tsv` 미착수 4,131행(고우선 비중 미확인),
    `repack_noneki_translation.py`(NonEKI 전용 파이프라인, `NonEKI_9_FU_compat_translated.pak`)
    미실행, `E:/ft_src`의 원래 내용 미확인(있었다면 이번 pak 재조립에 반영 안 됐을 가능성).
    (~~4개 `zz_localeko_*_low_*.pak`을 관례대로 `female_translation.pak`에 병합~~ — 완료,
    위 2026-09-28 (4차) 항목 참고.)
- **`dump_priority.py`/`rest_worklist.tsv` 기반 큐는 신뢰하지 말 것.** `rest_priority_*` 배치는
  `translations\rest_priority_0001.tsv` ~ `rest_priority_1088.tsv`까지 있고 당시 큐 기준으로는
  소진 상태였지만, 이는 `scan_remaining.py`의 커버리지 판정 버그 때문에 실제보다 훨씬 적게 잡힌
  착시였다(활성 pak 미확인 + 중첩 배열 미파싱 + 경로 대소문자 불일치). 세 버그를 모두 고쳐
  `scan_remaining.py`를 재실행한 결과가 현재의 참값이다. 상세는 `docs/batch_log.md`
  "2026-09-27" 항목.
- 재검증된 실측(2026-09-27 기준 최초 재스캔): 고유 영문 후보 **19,847건** 남음
  (`rest_worklist.tsv`, `rest_summary.json`). 진짜 고우선(로어/퀘스트/대사/기본 설명)은 재분류 후
  92건뿐이었고, 실제 번역 가능한 항목은 1차 배치로 처리 완료. 저우선(종족별 부가 설명 등)은
  Elithian·K'Rakoth 계열·Plushbound·Enternia·Neki·Angel 등 소수 모드에 집중돼 있다 —
  `docs/priority_allocation_20260927.tsv`.
- **Elithian Races Mod(2,350건) 완주** (2026-09-27, 같은 세션 내): 저우선 최대 항목이던 Elithian의
  종족별 아이템/오브젝트 설명을 전량 번역해 `mods/zz_localeko_elithian_low_20260927.pak`으로 적용,
  매 배치 서버 부팅 검증(`[Error]` 0건) 완료. 상세는 `docs/batch_log.md` 해당 항목.
- **K'Rakoth Mod(2,098건) 완주** (2026-09-27, 같은 세션 내): 커스텀 종족 Annelisk/Fenron/Noolith 및
  기존 종족의 아이템/오브젝트/퀘스트 설명을 전량 번역해 `mods/zz_localeko_krakoth_low_20260927.pak`으로
  적용, 매 배치 서버 부팅 검증(`[Error]` 0건) 완료. 상세는 `docs/batch_log.md` 해당 항목. 재스캔 결과
  잔여 저우선 백로그는 **15,407건**(유니크 영문 기준, `rest_summary.json` 최신 값).
- **nuggubs' Mega Mod(2,064건) 완주** (2026-09-27, 같은 세션 내): Felin/Neko/Neki/Avali/Slimeperson
  등 종족별 오브젝트·가구·포스터·봉제인형 설명을 전량 번역해
  `mods/zz_localeko_nuggubs_low_20260927.pak`으로 적용, 매 배치 서버 부팅 검증(`[Error]` 0건) 완료.
  상세는 `docs/batch_log.md` 해당 항목. 재스캔 결과 잔여 저우선 백로그는 **13,343건**(유니크 영문
  기준, `rest_summary.json` 최신 값).
- **Plushbound(1,990건) 완주** (2026-09-28): `plushbound_low_worklist.tsv` id 0~1989 전량 번역해
  `mods/zz_localeko_plushbound_low_20260927.pak`으로 적용(339 assets, 683,394 bytes). 구조 QA
  1건 예외(id 1169: 원문 자체에 깨진 아이콘 글리프 포함, 자연어 의역으로 처리) 외 이상 없음.
  용어집 정정: 배치 작성 중 `미니크노그`→`미니크녹`, `노바킨`→`노바키드`, `재배자`(Cultivator
  금지어)→`컬티베이터`로 전량 재치환. **서버 부팅 검증은 미완료** — `RPG_contents_1115920474.pak`의
  패치 실패와 `/player.config` JSON 파싱 오류로 서버가 기동 중 크래시하는데, 이는 배치4 검증
  시점(Plushbound 번역 착수 이전)부터 있던 기존 모드팩 문제로 확인되어 Plushbound 번역과는 무관.
  원인 조사는 다음 세션으로 이월. 상세는 `docs/batch_log.md` 해당 항목.
- 다음 저우선 대상(우선순위 테이블 기준): Enternia(1,604) → Neki(1,404) →
  Angel(1,379, 주로 angeldescription) → Voided(567) → 이하 소형 모드.
  (Plushbound 완주로 재스캔 필요 — 아래 `scan_remaining.py` 항목 참고)
- 다음 세션 재스캔 전에는 항상 `scan_remaining.py`를 다시 돌려 최신 커버리지를 반영할 것. 번역을
  새로 적용한 pak이 있으면 `load_coverage()`가 확인하는 pak 목록(`female_translation.pak`,
  `zz_localeko_postload.pak`, `zz_localeko_highpriority_20260927.pak`,
  `zz_localeko_elithian_low_20260927.pak`, `zz_localeko_krakoth_low_20260927.pak`,
  `zz_localeko_nuggubs_low_20260927.pak`, `zz_localeko_plushbound_low_20260927.pak`, 구 legacy 3종)에
  그 pak도 추가해야 다음 스캔이 정확해진다. (이 문단이 작성된 시점엔 Plushbound 완주분이 아직
  미등록이었으나, 이후 세션에서 등록 완료됐고 — **2026-09-28 (4차)에서 해당 4개 pak 자체가
  `female_translation.pak`에 병합돼 `mods/`에서 사라졌다.** `load_coverage()`는 `if not p.exists():
  continue`로 존재하지 않는 pak을 건너뛰므로 목록에 이름이 남아 있어도 무해하며, `female_translation.pak`
  항목이 이미 그 커버리지를 대신 제공한다. 상세는 `docs/batch_log.md` "2026-09-28 (4차)" 참고.)
- 게임 적용: `mods/zz_translation_female.pak`(구 `female_translation.pak`,
  2026-09-30 개명 — sbkor·FU_KO·localeko legacy 3종·
  zz_localeko_postload 병합 + `rest`/`batch`/`missed` 계열 신규 번역 + Elithian/K'Rakoth/nuggubs/
  Plushbound 4대 모드 병합, 2026-09-28 (4차))이 활성 번역 pak이다. `.patch`
  자산 속 문자열은 169개 pak을 스팬 편집으로 재패킹해 구워 넣었다(백업: `../replaced-installed-20260922/`에
  있었으나 2026-09-30 디스크 정리로 삭제 — 유일본은 현행 배포 pak).
  비번역 로컬 수정은 `mods/zz_female_overhaul.pak`으로 통합했다. 상세는 `../HANDOFF.md` 0절.
- 스타일 재검수: `style_worklist.tsv` 전량 완료(telegraphic → 자연어), 후속 성인 콘텐츠
  완곡어·오역 교정도 반영됨.
- 자리표시자 오염 정리: 원본·TSV·TM에서는 복원 완료. 구 FU_KO/localeko pak에 남아 있던
  깨진 토큰은 병합된 female_translation에도 잔존했을 수 있으므로 인게임 확인이 필요하다.
- 정리 검증(2026-09-25): 배치 0359~0370의 600개 ID가 각 50개씩이며, 배치 간 중복과 초안·TSV
  불일치가 없었다. 완료된 TSV는 `translations/`에 두고 초안 JSON 13개와 생성 스크립트 1개는
  `drafts/0359_0370/`에 보관했다. 전체 구조 QA 0건, 용어 QA는 아래 기존 오탐 4건뿐이다.

## 신규 번역 배치 작업

`rest_worklist.tsv`의 `new-translation` 행(빈 `suggestedKorean`)을 로어·퀘스트·대사·아이템 기본 설명
우선순위로 번역하는 반복 배치 루프다. `dump_priority.py`가 종족별 부가 조사(`nekidescription` 등)를
저순위로 미루고, 아이템 기본 설명(`description`/`shortdescription`/`longdescription`)과 로어·퀘스트·
대사(`label`/`title`류가 아닌 나머지 전부)를 고순위로 먼저 낸다.

> **배치 크기:** 자유롭게 정한다. 작은 수정 JSON은 이미 병합한 배치의 QA 오류를 고치는 용도로만
> 사용하며, 독립적인 신규 번역 배치로 취급하지 않는다.

> **품질 게이트:** 한 번에 번역하거나 기계 초안만으로 완료 처리하지 않는다. 배치는 내부 검토
> 묶음(권장 100개 이하)으로 나누어 원문·문맥을 직접 대조한다. 각 묶음에서 구조·고정 용어 검사뿐
> 아니라 미번역 영문, 뜻 반전, 화자 말투, 자연스러운 한국어 문장을 수동 확인한다. 이 검토가 끝난
> 항목만 완료로 기록한다.

### 반복 절차 (batch N)

1. `python dump_priority.py <count>`로 미번역 목록과 라이브 큐 수치를 확인한다. 선택한 묶음의
   **전체** 원문을 읽고 문맥과 용어를 확인한다. 권장 검토 묶음은 100개 이하다.
2. `priority_NNNN.json`에 `{ "id": "한국어" }` 형식으로 번역 초안을 작성한다. 긴 항목은 별도 생성
   스크립트를 써도 된다. 초안 키가 선택한 원문 ID와 정확히 일치하고 중복이 없는지 병합 전에 확인한다.
3. `python add_batch.py translations/rest_priority_NNNN.tsv priority_NNNN.json`으로 병합한다. 초안을
   나눴다면 JSON 파일을 여러 개 인자로 전달한다. 이 명령은 TSV를 직접 만들거나 갱신하고
   `qa_structure.py`를 실행한다. 원문의 비공개 글리프는 초안에
   `⟦E024⟧`처럼 적을 수 있으며 병합 시 복원된다.
4. `affected rows > 0`이면 `qa_struct_all.tsv`(id, 파일명, 이슈유형)를 읽어 실패한 id와 원인을 특정:
   - `tags`: `^color;...^reset;` 태그의 개수·순서·종류가 원문과 다름
   - `inputtoken`: `[FIRE]`, `[SHIFT]`, `[Alt-Fire]`, `[LMB]` 같은 대괄호 조작 힌트를 번역해버림 —
     반드시 영문 그대로 보존
   - `lines`: 원문의 개행(`\n`) 수와 번역문의 개행 수가 다름

   초안을 수정해 재병합하고 `affected rows: 0`이 될 때까지 반복한다.
5. 원문·문맥과 번역문을 직접 대조하고 `python qa_glossary.py`를 실행해 결과가 아래 기준선과 같은지
   확인한다. 새 위반을 고친 뒤 구조·용어 검사를 다시 수행한다.
6. `docs/batch_log.md` 맨 위와 이 문서의 "진행 현황"을 갱신한다. 완료된 TSV는 `translations/`에
   유지하고, 확인된 초안은 `drafts/` 아래에 보관해 작업 폴더 최상위를 정리한다.

### QA 기준선

- `qa_structure.py`: 0건
- `qa_glossary.py`: `Spooked(2)/Codex(1)/Unexplored(1)/The Ruined(1)` — 모두 알려진 오탐, 이 외 새 항목이 나오면 위반
  - `Spooked`: id 61820·75249는 동사 용법(`겁먹었다`/`겁먹지 않는다`)이라 상태이상 고정형 `겁먹음` 불가
  - `Codex`: id 128726은 JSON 아이템명 `lustlingView-codex` 내부 문자열
  - `Unexplored`: id 60335는 산문 형용사(`미개척`), 행성 UI 용어가 아님
  - `The Ruined`: id 53140 일반 서술 "ruined city"(폐허가 된 도시)
- ID 주의: `batch_*`/`missed_*`/`rest_*`/`rest_priority_*`는 서로 독립된 ID 번호 체계다.
  같은 ID가 다른 원문을 가리키므로(충돌 7천여 건) `rest_worklist.tsv`의 원문 매핑은
  `rest_priority_*` 파일에만 유효하다. EN↔KO 대조 스크립트를 짤 때 파일 집합을 한정할 것.

## 반복 실수 방지 규칙

### 태그·구조

- 원문에 없는 `^reset;`을 임의로 붙이지 않는다. 문장이 `^orange;...`처럼 닫는 태그 없이 끝나는
  원문에서 가장 자주 재발했다(id 79419, 80185, 82923 등).
- 색상 태그가 중첩되어 `^reset;` 하나가 여러 태그를 닫는 경우(`^green;...^orange;...^reset;`),
  번역문에도 열리는 태그를 전부 포함한다.
- 원문의 개행 수를 그대로 맞춘다. 여러 줄 원문을 한 줄로 합치거나, 줄바꿈을 더 넣지 않는다.
- 대괄호 조작 힌트(`[FIRE]` 등)는 번역하지 않는다.

### 고정 표기 오역 정정 이력

`qa_glossary.py`가 잡아낸 고정 용어 오역 목록이다 (원문 → 정식 한글 표기, 실제로 있었던 오역형).
글로서리 고정 표기는 TM 다수파 표기와 달라도 고정 표기를 따른다(예: 팝톱).

- `Miniknog` → `미니크녹` (`미니크노그`에서 사용자 지시로 정정, 이후에도 `미니노그`로 오기한 사례 있음)
- `Hylotl` → `하이로틀` (`하일로틀`/`히로틀` 오기 있었음)
- `Novakid` → `노바키드` (`노바킨`으로 오역)
- `Lustling` → `러스틀링` (`러스트링`/`러슬링`으로 여러 번 오역)
- `Manipulator Module` → `물질 조작기 모듈` (`조작기 모듈`/`조종기 모듈`로 축약 오역 있었음)
- `Terrene Protectorate` → `행성 보호국` (`테린 보호국`/`테렌 보호국`/`테레인 보호국`으로 오역. 음역
  `테레네 프로텍터레이트`는 일부 NonEKI 대사에만 한정 허용)
- `Protectorate` → `보호국` (음역 `프로텍토레이트` 금지)
- `Peacekeeper` → `피스키퍼` (`평화유지군`으로 오역)
- `United Systems` → `연합 시스템` (`유나이티드 시스템즈`로 오역, "연합 체계"로도 쓰지 않음)
- `Broadsword` → `브로드소드` (대검·장검과 혼용 금지, `얼음 장검`처럼 의역했다가 정정한 사례 있음)
- `Shortsword` → `소검` (Dagger의 "단검"과 구분, `숏소드`로 여러 번 오역)
- `Sniper Rifle` → `저격소총` (붙여쓰기, `저격 소총`으로 오역)
- `Grenade Launcher` → `유탄 발사기`, `Rocket Launcher` → `로켓 발사기` (띄어쓰기 포함, 붙여 쓴 오역 반복)
- `AP rounds` → `철갑탄` (`AP탄`으로 오역. 탄약 약어는 음역 전에 고정 용어 확인)
- `THRUST damage` → `찌르기 피해` (`관통 피해`로 오역)
- `Alt Fire` → `보조 발사` (영문 그대로 둔 사례 있음)
- `Regeneration` → `재생` (`회복`으로 바꿔 쓴 사례 있음. 상태 이름은 동의어로 바꾸지 않음)
- `Crafting Station` → `제작대` (`제작 시설`로 오역)
- `Parry Window` → `패링 창` (`패링 윈도우`로 오역)
- `Perfect Block` → `퍼펙트 블록` (완벽 블록·완벽 방어·완벽 막기로 쓰지 않음)
- `wood-warder` → `숲의 파수꾼` (FFXIV 비에라 직책명, `숲지기`로 오역)
- `Cultivator` → `컬티베이터` (`경작자`로 오역)
- `Teleporter` → `텔레포터` (`순간이동기`로 오역)
- `Saturnian` → `새터니안` (`새턴인`으로 오역)
- `Occasus` → `오카서스` (`오카수스`로 오기)
- `Portal` → `포털` (장치·현상명; 문학적 문맥은 `관문` 허용, `포탈` 금지)
- `Poptop` → `팝톱` (`팝탑`으로 3회 반복 오역, TM 다수파가 `팝탑`이라 특히 주의)
- `Kappa` → `캇파` (GIC 환상향 계열 요괴, `카파`로 쓰지 않음)
- `Telebrium` → `텔레브리엄` (`텔레브륨`/`텔레브리움`으로 오기)
- `Infernus` → `인퍼너스` (`인페르누스`로 오기)
- `Magishot` → `매지샷` (`매직샷`으로 오기)
- `Penguin Bay` → `펭귄 베이` (`펭귄 만`으로 의역)
- `Avikan` ↔ `Avali` 혼동 주의: 각각 `아비칸`/`아발리`이며 `아발리칸`으로 뒤섞어 오기한 사례 있음
- `Akkimari` → `아키마리`, `Akki` → `아키` (`아끼마리`/`아끼`로 오역했으나 사용자가 `아키`로 확정 2026-09-25. 한국어 동사 `아끼다` 용법은 건드리지 않음)
- 상태이상을 **부여하는** 장비명은 `중독된/감전된 + 장비`가 아니라 속성 형용사 `독성/일렉트릭 + 장비`로 쓴다 (`중독된 마그노브`는 장비가 중독된 것처럼 읽히고, `중독 마그노브`는 상태명 나열이라 어색). 실제로 상태에 걸린 대상·지형 묘사는 `-된` 유지 (사용자 확정 2026-09-25)

이 목록에 없는 새 고정 용어 후보가 나오면 `translation_glossary.tsv`를 먼저 확인하고, 없으면
`term.py "이름"`으로 기존 번역 메모리를 조회해 다수결로 판단한다.

### 혼동하기 쉬운 용어

- `Byak`(나이타르 저주 문맥) → `바이악`. 크리처 `Byakhee`(`백희`)와 다르다.
- `Miniknog Stronghold` → `지식부 요새`(바닐라 공식 번역). 단독 `Miniknog`는 `미니크녹`.
- `Mega-Fauna` → `거대-동물`(TM 재사용, `메가 야수` 금지). `K'Rakoth` → `크라코스`.
- `Pokéball` → `포켓볼`. 포켓몬 이름은 임의 음역하지 말고 `term.py`로 기존 표기(예: 로퍼니)를 확인한다.

### 종족 스탯 블록 라벨 세트

종족 능력치 블록이 나오면 `term.py`로 하나씩 찾지 말고 아래 라벨을 그대로 쓴다. 이 라벨은
`translation_glossary.tsv`에 없어 `qa_glossary.py`가 강제하지 않으므로 직접 대조한다.

- 표준 블록: `Attributes→능력치`, `Max Health→최대 체력`, `Max Energy→최대 에너지`,
  `Energy Regen→에너지 재생`, `Attack Multiplier→공격력 배율`, `Defense→방어력`, `Resistances→저항`,
  `Fire/Electric/Poison/Ice/Physical Resistance→화염/전기/독/냉기/물리 저항`, `Immunities→면역`,
  `Racial Traits→종족 특성`, `Knockback Resistance→넉백 저항`, `Fall Damage→낙하 피해`,
  `Movement Speed→이동 속도`, `Breath Depletion Rate→숨 소모 속도`, `Max Breath→최대 숨`,
  `Swim Boost (Alt.)→수영 강화(대체)`, `Underwater Breathing→수중 호흡`
- 커스텀 블록(Viera류 등): `Diet→식성`, `General Perks→일반 특전`, `Base Stats→기본 스탯`,
  `Movement→이동`, `Resists→저항`, `Biome Perks→지형 특전`, `Weapon Perks→무기 특전`,
  `Weaknesses→약점`, `Biome Weaknesses→지형 약점`, `Stomach Capacity→배 용량`,
  `Crit Chance→치명타 확률`, `Cosmic→우주`

### RPG Growth 클래스·전문화명

기존: 도적/개척자/마법사/트래퍼/방랑자/닌자/체인즐링/드래군/숙련자/암살자/버서커/배틀 메이지/워록/
콘키스타도르/사무라이/엘리멘트리스/용병/기사. 배치 0241에서 확정: 메카니스트, 네크로맨서,
테크노맨서, 타이탄, 세이지, 셰이드, 캐노니어(Cannoneer/Canoneer), 발키리, 오퍼레이티브.

### 문체

- 원문이 의도적으로 뒤섞은 가짜 속담("Maggot Man says: ...")은 매끄러운 속담으로 고치지 않고 직역해
  우스꽝스러움을 살린다.
- 성인 콘텐츠(Lustling, 촉수 등)는 완곡화하지 않고 원문 그대로 번역한다.
- 외국어 플레이버 텍스트(프랑스어 등)도 한국어로 옮긴다.

### 신규 고유명사

TM에 없어 새로 확정한 고유명사는 전부 `translations/rest_*.tsv`에 반영되어 있으므로
`python term.py "이름"`으로 조회해 재사용한다. 개별 결정 근거는 `docs/batch_log.md`에 있다.
