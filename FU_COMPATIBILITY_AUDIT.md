# FU 관련 호환 모드 점검 — 2026-09-28

설치된 메타데이터의 이름에서 FU/Frackin/BYOS 연동 모드 68개를 선정했다.
FU 본체와 대규모 번역 pak는 선정 목록에서 제외하되 실제 엔진 실행에는
전체 모드팩을 포함했다. 모드 메타데이터 목록과 개별 결과는
`tmp/fu-compat-selected-20260928.json` 및
`tmp/fu-compat-audit-20260928/inventory.json`에 있다.

## 적용한 수정

| 대상 | 문제 | 수정 |
| --- | --- | --- |
| FU RACES PATCH | 트라이코더 UI가 현재 FU에 없는 loadGPS2/loadGPS3를 호출하고 면역 목록 구조를 교체함 | female_overhaul에서 현재 FU의 statWindow.config 복구. 종족 효과 정의는 유지 |
| FU + Extended GUI Patch | craftingwheel의 lblArmorTab이 현재 FU에 없어 패치 전체 실패 | 해당 위젯이 있을 때만 구버전 레이아웃 패치 실행 |
| FU Perennial Crops | 수정 작물 두 경로에 crystalplant 폴더가 중복됨 | 실제 야생/재배 수정 작물에 원래 resetToStage 패치 적용 |
| Frackin Races Vanilla Food Patch | reefpodsurprise의 tier5 경로와 reefcola의 후행 공백 | 실제 tier4/공백 없는 파일로 원래 패치 연결 |
| Compact Crops FU | xi_bulb2 폴더 안의 파일 이름이 xi_bulb.object로 잘못 지정됨 | xi_bulb2.object에 좁은 배치 적용 |
| Improved Food Descriptions FU | plutoniumradien이 isotopes 폴더로 이동함 | 실제 경로에 설명 패치 연결 |
| Cosmic Husbandry FU Patches | 본체보다 먼저 로드되어 대상 파일 69개의 패치가 등록되지 않음 | female_overhaul에서 본체 로드 후 원래 패치 적용 |
| NPCSpawner+ FU 승무원 패치 | 본체보다 먼저 로드되어 두 메뉴 설정 패치가 등록되지 않음 | 늦은 Lua 패치로 FU 승무원 목록 추가. 중복 방지, 원래 앞/뒤 삽입 순서 유지 |
| K'Rakoth FU Addon | deadbeat rifle 본체보다 먼저 패치 로드 | 늦은 Lua 패치로 FU 툴팁·치명타 값·무기 태그 적용. 태그 중복 방지 |

## 원본 pak 수정 예외

FUExGUIPatch의 기존 `.patch` 본문을 뒤의 일반 패치로 바꿀 수는 없다.
기존 패치 파일 수정에 허용된 예외를 사용하여 이 pak만 재패킹했다.
`compat_sources/FUExGUIPatch`에 전체 재현 소스를 저장했고
`tools/repack_fu_exgui_compat.ps1`로 배포한다. 버전은
`1.2+compat20260928`; 다른 패치 및 이미지 내용은 원본과 같다.
나머지 수정은 모두 `mods_src/female_overhaul`에 있으며
`tools/repack_overhaul.py`로 배포한다. 기존 저장 파일은 수정하지 않는다.

## 겹침 및 지원 범위

- Frackin GiC race patch의 human/floran 효과는 FU RACES PATCH의 같은 파일에
  덮인다. 최종 정의는 FU RACES PATCH의 능력치·무기 특성이다. 두 모드의
  효과를 합쳐 중복 적용하지 않았다.
- More Planet Info의 구 FU 패치는 기본 MPI injections.lua와 줌 경계 값
  하나만 다르다. 공식 FU MPI 패치는 cockpitview.lua를 담당한다. 서로
  다른 역할이므로 둘을 단순 중복으로 제거하지 않았다.
- FU SAIL 종족 지원의 설치되지 않은 종족용 대상 519개는 선택적 지원이다.
- 일부 Avali 레시피, Elithian/Redemption의 폐기된 장비, 옛 melee ability,
  미설치 종족용 BYOS/종족 효과, Woof의 구 Sexbound 확장은 설치된 파일에
  대응하지 않는다. 없는 콘텐츠를 임의로 재생성하거나 동명 복제품에
  연결하지 않았다. 개별 경로는 inventory.json에 기록했다.
- OpenStarbound의 자산 맵은 대소문자를 구분하지 않는다. 대소문자만 다른
  NPC 메뉴/Elithian 함선/ore detector 경로는 무효 패치로 분류하지 않았다.

## 검증 범위

실제 OpenStarbound 엔진에서 선정 모드의 존재하는 패치 대상과 로컬 수정
대상을 강제로 읽는다. 현재 대상은 중복을 제외한 1,888개다. 기본적으로
자산이 읽혔다는 것만으로 패치 적용 성공을 단정하지 않고, 로그의 패치
실패도 함께 확인한다. 트라이코더의 등록 콜백이 실제 Lua 함수에 존재하는지,
다년생 작물·음식 분류·좁은 작물 배치·닭의 FU 식성/번식 설정·알 부화 시간·
승무원 목록·무기 태그가 최종 자산에 있는지도 확인한다.

이 검증은 모든 무기의 전투, 종족별 BYOS 건설, 모든 작물/승무원 행동을
실제 플레이로 완주한 검증은 아니다. 첫 행성 도착과 S.A.I.L. 화면 표시도
재접속 후 플레이 화면에서 최종 확인해야 한다.

최종 결과: 1,888개 자산 로드 실패 0건, 선정된 FU 호환 모드의 패치 적용
오류 0건, 기능 및 배포 내용 검사 14건 통과, 서버 21025 포트 대기 확인.
별도의 시작 행성 생성 가능성·S.A.I.L. 선택 검사도 실행했다. 목록 52개,
apex/human/neki/angel 전환, NonEKI 칩 이미지 복귀 및 null 좌표 처리 통과.

위 최초 감사에서는 FUlocaleko/female_translation의 번역 오류 4건이 남았다.
후속 2026-09-28.6 수정에서 converse의 사라진 대사 경로를 개별 검사하고,
crafting value와 quickbar의 대상 존재 여부를 보완했다. BookOfSpirits의
displayTitleAsName 누락도 함께 수정했다. 후속 별도 서버에서 이 자산들의
패치 오류 0건 및 유효한 한국어 대사 적용을 확인했다.
재현 및 배포 방식은 TRANSLATION_PATCH_COMPATIBILITY.md에 기록했다.
새 캐릭터의 콘솔 연결 누락은 FU_SAIL_COMPATIBILITY.md 후속 수정에 기록했다.
`tmp/fu-compat-audit-20260928/checks.txt`, `remaining-errors.txt`,
`starbound_server.log`에서 결과를 확인할 수 있다.
