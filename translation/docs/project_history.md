# 프로젝트 초기 이력 (2026-09-21 ~ 09-23)

> README.md에서 분리한 기준선 추출·정렬·오버레이 시험 기록이다. 수치와 상태는 작성 당시 기준이다.

## 호환성 수정

- `FUlocaleko`와 `sbkor`에서 최신 자산에 존재하지 않는 패치 경로를 제거했다.
- `interface/cockpit/cockpit.config.patch`는 바닐라 cockpit 구조에 실제로 존재하는 경로만 유지했다.
  FU가 나중에 추가하는 `displayOres`, `displayWeathers`, `fu_text` 및 확장 행성 설명은 이 번역 pak의
  로드 시점에는 존재하지 않아 적용할 수 없고, 한 항목의 실패가 파일 전체 번역을 취소하므로 제외했다.
- 최종 서버 로그의 번역 오류는 0건이다. 남은 `[Error]`는 기존 K'Rakoth `nitrogendeep` 1건뿐이다.
- 검증 로그: `../translation-fix-20260921/verified_server.log`

## 기존 번역 말뭉치

활성 번역 병합본, 교체 보관본, 백업 ZIP에서 복원한 수정 전 `FU_KO`·`sbkor`까지 총 16개 출처를
스캔했다.

- 한글 포함 자산: 37,370개
- 추출 문자열: 130,689건
- 고유 한글 문자열: 57,036건
- `corpus/korean_strings.tsv`: pak·자산 경로별 한글 문자열
- `corpus/frequency.tsv`: 문자열 사용 빈도
- `corpus/sources.json`: 출처별 버전과 추출 통계

수정 전 pak 두 개는 `Starbound.zip`에서 이 폴더로 복원했다. 활성 모드가 아니며 용어 복구용이다.

## 활성 pak 자동 인벤토리

활성 pak 799개를 JSON/JSON Patch의 사용자 노출 가능성이 높은 키를 기준으로 스캔했다.

- 후보가 있는 모드: 342개
- 후보 자산: 55,522개
- 영문 후보 문자열: 193,270건
- `inventory/translatable_candidates.tsv`: pak·자산·JSON 포인터·영문 후보
- `inventory/mod_summary.json`: 모드별 후보 자산과 문자열 수

이 수치는 번역 완료율이 아니다. `name`·`value`처럼 문맥에 따라 식별자일 수 있는 키, 호환 패치가
복제한 문자열, 실제로 쓰이지 않는 자산도 포함한다. 다음 단계에서는 원본/번역본 경로 대조와
식별자 패턴 제거로 모드별 실제 번역 대상을 확정해야 한다.

우선 검토 규모가 큰 원본 콘텐츠는 FU 39,118건, GiC 13,885건, nuggubs 11,821건,
Elithian 9,757건, My Enternia 8,181건, Arcana 7,684건, K'Rakoth 6,469건 순이다.

초기 인벤토리의 정규식 주석 제거기는 문자열 안의 `http://` 등을 훼손했고 JSON Patch의 문자열
값을 두 번 셌다. 현재 수치는 문자열 인식 JSONC 파서, 리터럴 줄바꿈 허용, 패치 문서 내 실제
`value` 포인터 사용, `.radiomessages`·`.weaponability` 포함으로 다시 산출한 값이다.

## 1차 분류

`target_classification.tsv`와 `target_classification_summary.json`에 자동 분류 결과를 저장했다.

- 표시 문자열 후보 없음: 457개
- 기존 활성 번역 출처: 8개
- 구 번역과 최신본을 우선 대조할 대상: 5개
- 호환·패치·라이브러리로 추정되어 후순위: 63개
- Sexbound/성인 장면 계열로 추정되어 후순위: 25개
- 실제 콘텐츠 검토 대상: 241개

자동 분류는 이름 기반 1차 결과다. 특히 `content-review`에는 식별자 위주의 파일이 남아 있을 수
있으므로 바로 번역 패치를 생성하지 말고 경로·키 문맥을 확인한다.

## 원문-번역 정렬

백업의 수정 전 번역 패치를 현재 FU 6.5.8 및 바닐라 자산과 JSON 포인터 단위로 대조했다.

- 현재 원문과 기존 한글이 정확히 정렬된 항목: 82,326건
- 고유 원문-번역 쌍: 61,555개
- 고유 원문: 54,137개
- 둘 이상의 번역형이 존재하는 원문: 5,553개
- `alignment/fu.tsv`, `alignment/sbkor.tsv`: 경로별 정렬 결과와 누락 상태
- `translation_memory.tsv`: 빈도·예시 경로를 포함한 번역 메모리
- `glossary_candidates.tsv`: 짧은 문구 및 고유명사 후보와 기존 번역형

여러 번역형이 있는 원문은 자동으로 하나를 확정하지 않는다. 화자 종족별 말투, 문맥 차이,
실제 표기 불일치가 섞여 있으므로 오버레이 생성 전에 문맥을 확인한다.

## 구 병합 번역 4종과 최신본 대조

보관된 GiC, Extended Story, Black Armory, NonEKI 번역 병합본을 최신 활성 pak과 자산 경로 및
JSON 포인터 단위로 대조했다. JSONC 주석, 후행 쉼표, 문자열 안의 리터럴 줄바꿈을 처리하며,
일반 자산은 동일 포인터로, JSON Patch는 우선 `op/path/from` 조합으로 대응시켰다.

- 최신 문자열 위치와 연결된 구 번역: 6,334건
- 고유 최신 원문-구 번역 쌍: 5,020개
- 고유 최신 원문: 4,999개
- 같은 원문의 복수 번역형: 7개
- 동일 자산·포인터의 번역 충돌: 0개
- 최신 위치에 연결되지 않은 구 번역: 2,650건
- 파싱 실패: 0개

모드별 연결 결과:

- GiC: 4,501건 연결, 22건 포인터 변경, 2,444건은 최신본에 자산이 없음
- Extended Story: 916건 전부 연결
- Black Armory: 445건 연결, 39건은 최신본에 자산이 없음
- NonEKI: 472건 연결, 144건 포인터 변경, 1건은 최신 위치가 문자열이 아님

주요 산출물:

- `alignment/gic.tsv`, `alignment/extended_story.tsv`, `alignment/black_armory.tsv`,
  `alignment/noneki.tsv`: 위치별 최신 원문과 구 번역
- `legacy_translation_memory.tsv`: 최신 위치에 연결된 고유 원문-번역 쌍
- `legacy_unresolved.tsv`: 삭제된 자산, 변경된 포인터 등 자동 재사용 불가 항목
- `legacy_location_conflicts.tsv`: 동일 위치 번역 충돌 목록(현재 0건)
- `legacy_alignment_summary.json`: 모드별 상태 집계
- `legacy_remaining_candidates.tsv`: 기존 번역이 정확한 위치에서 확인되지 않은 영문 후보
- `legacy_coverage_summary.json`: 휴리스틱 후보 대비 기존 번역 위치의 범위

인벤토리 후보와 정확한 위치가 겹치는 비율은 GiC 27.1%, Extended Story 48.7%, Black Armory
25.0%, NonEKI 24.9%다. 인벤토리에는 식별자와 내부 값도 포함되므로 이는 실제 번역률이 아니라
남은 목록을 줄이기 위한 휴리스틱 수치다.

다음 단계에서는 연결된 위치를 모드별 오버레이 후보로 변환하되, 원본의 `.patch` 자산은 별도로
취급한다. 다른 모드의 패치 파일 자체를 덮어쓰면 업데이트 내성이 낮으므로 대상 원본 자산에 안전하게
후속 패치를 적용할 수 있는지 먼저 확인한다. 이어서 `legacy_remaining_candidates.tsv`에서 식별자,
스크립트 인수, 사용되지 않는 자산을 제외해 실제 신규 번역량을 확정한다.

## 오버레이 생성 시험 및 중단 상태

`translation/translation-overlays-20260921`에 최신 위치와 연결된 6,334건의 오버레이 후보를 생성했다.
일반 자산 번역은 5,816건이고, 원본 자체가 `.patch`인 번역은 518건이다.

시험 결과 Starbound는 `.patch.patch`를 패치 문서에 적용하지 않고 최종 자산에 적용했다. 이 때문에
첫 시험은 `/player.config` 구조 오류로 실패했다. 이 방식은 사용하면 안 된다.

두 번째 시험에서는 GiC 28건과 Extended Story 23건을 원본 패치가 수정하는 최종 자산 경로로
우회했다. NonEKI는 467건 중 364건이 배열 끝 `/-` 추가 연산이라 후속 패치에서 안정적으로 지목할
수 없었다. 이에 최신 NonEKI를 풀어 472개 문자열만 바꾼 재패킹 후보도 만들었으나, 서버에서 다시
`/player.config` 및 다른 자산의 JSON 배열/객체 변환 오류가 발생했다. JSON 재직렬화가 Starbound
전용 구조나 중복 키를 훼손했을 가능성이 있어 이 재패킹본도 사용하지 않는다.

격리 시험 뒤 세 오버레이를 모두 비활성화하고 NonEKI 원본을 복원했지만, 복원 기준선에서도
`/player.config`와 `perfectlygenericitem.object` 오류 후 서버가 종료되었다. 활성 NonEKI와 보관
원본의 SHA-256은 모두
`F3686E18CF03ED7750437A1E66E6A282D3D21B81AF4C645CC43D7BADBACBC067`로 일치하므로,
현재 크래시 원인이 번역 후보인지 기존 로드 순서/다른 활성 패치인지 아직 확정할 수 없다.

정리 후 상태:

- `mods`의 시험용 `localeko_*_legacy.pak`: 0개
- `mods/NonEKI_9_FU_compat.pak`: 시험 전 원본으로 복원, 보관본과 해시 일치
- 실행 중인 `starbound_server`: 없음
- NonEKI 원본 보관:
  `E:/Desktop/mods/replaced-installed-20260921/translation-repacks-20260921/NonEKI_9_FU_compat_original.pak`
- 실패 후보와 소스, 생성 스크립트, 서버 로그는 `translation/translation-overlays-20260921`에 보존

주요 로그:

- `server-verify2.stdout.log`: `.patch.patch` 시험
- `server-final.stdout.log`: 최종 자산 우회 + NonEKI 재패킹 시험
- `server-isolate-noneki.stdout.log`: NonEKI 재패킹만 활성화한 격리 시험
- `server-baseline-restore.stdout.log`: 모든 시험 오버레이 제거 및 NonEKI 원본 복원 후 시험

다음 세션은 번역 후보를 다시 활성화하지 말고 먼저 복원 기준선의 `/player.config` 패치 출처와
로드 순서를 감사해야 한다. 기준선 서버가 다시 정상 기동한 뒤 일반 자산 전용 오버레이를 모드별로
하나씩 시험한다. `.patch.patch`와 JSON 전체 재직렬화 방식은 재사용하지 않는다.

## 후보 정리 결과 (두 번째 세션)

`clean_translation_candidates.py`로 `legacy_remaining_candidates.tsv` 12,839행을 정리했다.

- 번역 대상 확정: 10,595행 / 고유 영문 7,724건
  - `new-translation`: 8,461행 — 신규 번역 필요
  - `tm-single`: 1,285행 — 번역 메모리에 단일 번역형 존재, 자동 채우기 가능
  - `tm-multi`: 849행 — 번역형이 여러 개, 문맥 검토 필요
  - `.patch` 문서 안 후보 659행은 `inPatchAsset=1`로 표시(오버레이 시 별도 처리)
- 제외: 2,244행
  - `unused-or-deprecated-asset` 1,925 — UNUSED/LEGACY/OLD/DEPRECATED 경로
  - `behavior-tree-parameter` 208 — `.behavior` 매개변수 참조(`<windupTime>` 등)
  - `template-placeholder` 111 — listTemplate 스키마의 `Replace Me` 등
- 모드별: GiC 7,961 / Black Armory 1,260 / Extended Story 740 / NonEKI 634
  (NonEKI는 633행이 `.patch` 소스라 오버레이 불가, 재패킹 필요)
- `legacy_unresolved.tsv` 2,650행 분류: 삭제 콘텐츠로 복구 불가 2,483,
  포인터 이동으로 수동 재배치 후보 166, 비문자열 1.

산출물: `cleaned_translation_targets.tsv`, `excluded_candidates.tsv`,
`unresolved_triage.tsv`, `cleanup_summary.json`

### tm-single 자동 적용 완료

`apply_tm_singles.py`로 일반 자산 `tm-single` 1,094행(GiC 652, Black Armory 372,
Extended Story 70)을 `source-v3` 오버레이에 병합했다. 병합 전 각 행의 현재 원문을
소스 pak에서 다시 검증해 불일치 0건을 확인했다. NonEKI의 tm-single 191행은 전부
`.patch` 소스라 제외했다.

재패킹 후 서버 검증: `0.0.0.0:21025` 정상 기동, `[Error]`는 기존 K'Rakoth
1건뿐. 로그: `../translation-overlays-20260921/verified-v3/with-tm-singles.log`

### `.patch` 소스 우회 적용 완료

`merge_redirected_patch_ops.py`로 v2의 우회 연산을 검증 후 v3에 병합했다. 소스
pak의 패치 문서를 베이스 자산에 실제 적용한 뒤 최종 포인터를 resolve해 현재
원문과 비교하는 방식이다. GiC 27건·ES 23건 적용, GiC
`gic_mediumblizzard` 1건은 최종 값이 `Blizzard`로 바뀌어 제외.
로그: `../translation-overlays-20260921/verified-v3/with-redirected.log`

### NonEKI 스팬 편집 재패킹 완료

JSON 재직렬화 대신 `jsonc_spans.py`(JSONC 주석·후행 쉼표·리터럴 줄바꿈 지원,
중복 키는 마지막 값 유지)로 대상 문자열 리터럴만 원시 텍스트에서 교체했다.
`repack_noneki_translation.py`가 언팩→편집→재패킹→검증을 수행한다.

- 적용: 구 번역 472건 + tm-single 191건 = 663건 / 69개 자산
- 미변경 자산 159개는 원본과 바이트 동일
- 재패킹본 포인터 전수 검증 663/663 한글 일치
- 서버 정상 기동, NonEKI 오류 0건
- 산출물·로그: `../noneki-spanedit-20260922`

## 2026-09-23: 기존 초안 자연스러움 검수

번역 TSV의 기존 초안을 대상으로 문장 완결성·종족별 조사 말투를 검수하는 별도 대기열을 만들었다.
`style_worklist.tsv`의 `TODO`만 처리하며, 이 파일은 진행 관리용이고 실제 번역 원본은
`translations/rest_*.tsv`다. 재개 시 `python style_next.py <count> worst`로 저밀도·비자연문부터 확인하고,
같은 배치에서 해당 행의 상태를 `OK`로 바꾼다. 구조·용어 검사는 각 배치 후
`qa_structure.py`, `qa_glossary.py`를 실행한다.

2026-09-23 인계 시 상태: `DONE` 4,505 / `OK` 1,075 / `TODO` 1,235. 이 검수는 pak을 재생성하거나
`mods`를 바꾸지 않는다. 상세 경과와 말투 기준은 루트의 `MOD_MAINTENANCE_HANDOFF_2026-09-21.md` 34절 및
`STARBOUND_KO_GLOSSARY.md`를 따른다.
