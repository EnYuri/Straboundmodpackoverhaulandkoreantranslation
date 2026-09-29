# 전체 호환 패치 점검 — 2026-09-28.9

실제 클라이언트 로그의 818개 자산 소스와 로드 순서를 기준으로 조사했다.
FU/GIC 연동, 메타데이터에 호환·패치·연동을 명시한 소스, 소규모 패치 소스를
합쳐 666개를 검사 대상으로 선정했다. 본체 및 번역도 실제 엔진 실행에는
모두 포함했다. `tmp/all-compat-audit-20260928/inventory.json`에 전체 목록,
없는 대상 경로, 너무 이른 패치 등록, 덮어쓴 원본, 누락 require를 기록했다.

## 이번 수정

| 대상 | 원인 및 수정 |
| --- | --- |
| 첫 음식 S.A.I.L. 무전 | NonEKI가 공백 애니메이션에 설정한 초당 0.1자 속도를 번역된 대사가 이어받음. 해당 값만 초당 40자로 복구하며 번역·초상화 유지 |
| naturalcave2 | NonEKI FU 패치가 삭제한 메시지를 동굴이 계속 호출함. 누락된 경우 한국어 경고와 현재 초상화로 복구 |
| 도구·씨앗·차량 설명 | Betabound의 toolLabel → subTitle 변경을 번역이 반영하지 못함. 실제 존재하는 위젯에 한국어 적용 |
| 다른 번역 오류 | eyeguard/eyepatch의 JSON 포인터, merchant/statuses 배열 범위, gun/staff/magnorb의 삭제된 위젯, craftingnocategories의 구형 버튼 경로를 수정·조건 검사 |
| colourful/spacehero 대사 | sbkor와 통합 번역의 따옴표·쉼표 오류 수정 |
| Shattered Alchemy/FU Fruit Press | 잘못된 후행 쉼표와 중복 selected 키를 제거한 동일 설정 제공 |
| Starvisuals/Essential 희귀도 필터 | 없는 lineSpacing 삭제를 조건 검사하고 Avali Loom 버튼을 실제 배열 끝에 추가 |
| Black Armory 미션 | FU가 바꾼 Tiled 객체 위치·속성 형식을 지원. 기존 무전 목록에 Black Armory 메시지를 추가하여 FU 메시지 유지 |
| Reuss 해양 상자 | 배열 번호 대신 원래 상자 ID를 찾아 누락된 기본 보물 설정 추가. 기존 FU 보물 설정 유지 |
| GIC 확장·Storage Convenience | 이동된 작업대·상점·탄약·NPC 경로에 원래 패치 재연결. Red Sun Rising의 누락 확장자와 잘못된 탄창 태그 형식 수정 |
| GIC FU Armor Augment | 같은 방어구로 확인된 이동 경로 및 잘못된 이중 .patch 확장자를 복구. FU EPP 56개의 원래 강화 타입 유지 |
| Enhanced Storage 연동 | Angels, 누적 패치, My Enternia, nuggubs 가구의 이동 경로 재연결 |
| 다른 연동 | ERM FU 고기 청사진, Elithian Book of Spirits, Magic Labels, More Canned Food 설명, FU Redemption 및 이동된 번역 경로 수정 |
| 로드 순서 | FU의 transmutation study·종족 설명, SxB Relayer, Irisil 상인, 기존 참조 수정의 늦은 적용 복구 |

GIC 경로 재연결/확장자 수정 기록 187개와 기타 경로 재연결/늦은 재적용
187개는 각각 `gic-redirects.json`, `remaining-redirects.json`에 원본 경로,
새 대상, 원래 연산을 기록했다. 같은 대상에 여러 소스가 적용될 수 있다.
GIC 구형 탄약 작업대는 recipes 초기화뿐 아니라 필터도 복구했다.
재연결 후보 레시피 427개 중 설치된 아이템 ID가 없는 구형 레시피 153개는
재적용에서 제외했다. 실제 재연결한 레시피는 274개다. 제외 목록과 원래 비용은
`gic-redirects.json`의 `unsupportedRecipes`에 남겼다.
이 수정이 GIC의 모든 구형 거래 단말을 신형 작업장으로 재설계하는 것은 아니다.

## 배포 및 재현

일반 수정은 `mods_src/female_overhaul`에 있다. 기존 `.patch` 본문 수정은
`compat_patch_overrides/<pak 이름>/<자산 경로>`에 있다. 다음 순서로 배포한다.

```powershell
python tools/repack_compat_patch_overrides.py
python tools/repack_overhaul.py
```

기존 패치 수정 도구는 실행 중인 게임/서버를 거부하며, 메타데이터·자산 이름·
수정하지 않은 모든 자산 바이트가 그대로인지 확인한다. 번역 pak를 재생성한
경우에도 이 순서로 다시 적용한다. 이번 변경 전 pak 사본은
`tmp/all-compat-audit-20260928/before-paks`에 보관했다. 저장 파일은 수정하지 않았다.

## 검증 범위와 남는 한계

실제 Starbound 엔진으로 패치 대상 26,840개를 읽고, GIC 최종 설정 447개와
EPP 슬롯 56개, 음식 속도·동굴 안내·도구 번역·두 미션 무전을 별도로 검사한다.
추가로 저장소 연동, ERM 청사진, transmutation study, Irisil 상인과 기존 FU
트라이코더·작물·NPC·무기·SAIL 이미지 목록·애니메이션·좌표 방어를 검사한다.
실행 로그는 `tmp/all-compat-audit-20260928/starbound_server.log`에 있다.

최종 기능 검사에서 저장소 122개, GIC 설정 447개, FU EPP 56개와 SAIL 선택
목록 52개를 확인했다. 복구한 레시피 274개의 재료·결과물 ID도 설치 자산과
대조하여 누락 0건을 확인했다. 배포 pak 805개 항목은 재현 소스와 바이트 및
메타데이터가 일치한다. 기동 완료 및 오류 수는 같은 폴더의 `verification.json`
으로 확인한다.

존재하지 않는 선택적 종족/모드 대상은 곧바로 오류로 취급하지 않았다.
이름만 비슷한 다른 종족 방어구, FU EPP 타입을 바꿀 수 있는 잘못된 등 장비
경로, 이미 제거된 콘텐츠는 억지로 연결하지 않았다. `.patch.patch`가 가리키는
패치 배열을 일반 게임 설정처럼 강제 로드하는 검사는 제외했다.
오래된 조건부 require 경로는 호출 조건과 사용 여부를 구분해야 하므로
누락 목록을 모든 기능의 실행 실패로 단정하지 않는다.
모든 종족·아이템·퀘스트·멀티플레이를 실제 플레이로 검증한 것은 아니다.
