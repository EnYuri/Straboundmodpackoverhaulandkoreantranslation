# 남은 호환 패치 조사 — 2026-09-28

## 조사 범위

2026-09-28.11 통합 검사 로그의 실제 로드 순서를 사용하고, 현재 설치 파일을 다시 읽었다. 테스트용 probe를 제외한 운영 자산 소스는 818개다. 이름에 compatibility / patch / integration / addon을 명시한 소스는 160개다. 이 숫자는 미조사 패치 수가 아니며, 종족 본체나 Many Tabs처럼 이름에 해당 단어가 없는 연동도 별도로 살폈다.

이전 전체 검사는 자산을 읽을 수 있는지 확인했다. 존재하지 않는 대상의 패치는 등록되지 않으므로, 그 검사가 통과했다고 모든 연동이 적용된 것은 아니다. 이전 목록에 들어 있었어도 개별 기능과 현재 경로의 대조가 남은 항목이 있었다.

초기 조사 이후 사용자 요청에 따라 수정·배포까지 진행했다. 배포 버전은 2026-09-28.12다. 저장 파일은 수정하지 않았다.

## 추가로 확인한 미적용 패치

| 패치 / 소스 | 확인한 원인과 영향 |
| --- | --- |
| Avali Perennial Crops / `contents_869900472.pak` | `/treasure/cropharvest.tresurepools.patch`의 확장자 오타. 실제 파일은 `cropharvest.treasurepools`. kiri/nakati/piru/muli 수확의 `fill`을 제거하는 네 조건부 연산이 등록되지 않는다. 작물 단계 패치 전체가 실패한다는 뜻은 아니다. 별도의 avaliplant4 누락은 미설치 선택적 Avali 확장과 구분한다. |
| Simply Faster Followers / `contents_2881835252.pak` | `/npcs/overrides/override-follow.behavior.patch`는 잘못된 경로다. 실제 파일은 `/behaviors/npc/overrides/override-follow.behavior`이며 다른 패치가 없다. 원본 questFollowerRunSpeed는 14이고 의도한 값은 17이다. crewmember의 별도 runSpeed 패치는 정상 경로다. |
| Immersive NPC Dialogue / `contents_3088086087.pak` | penguindealer와 tarmerchant 패치가 `/npcs/nmm_tenants/`를 사용하지만 본체는 `/npcs/nuggubs_tenants/`다. 두 현재 NPC의 scripts는 `/npcs/bmain.lua`이고 현재 경로에는 번역만 있다. 대사 무작위화용 `/scripts/actions/om_INPCD.lua` 추가가 빠졌다. 나머지 누락 24개를 같은 문제로 단정하지 않는다. |
| Size of Life - Stat Modifiers / `size_stat_contents_3218827753.pak` | 축소 수류탄 패치가 `/items/throwables/`를 사용하지만 본체는 `/items/active/throwables/`다. 현재 원본 가격 50, 패치 의도 가격 500이며 현재 경로에 별도 패치가 없다. 나머지 구형 광선총 경로는 추가 대조가 필요하다. |
| Craftable Concoctions / `contents_931757634.pak` | `/npc/villager.npctype.patch`의 npc 단수 오타. 실제 `/npcs/villager.npctype`에 crewmemberconcoctions 승급 후보를 추가하려던 연산이 적용되지 않는다. FU Addon 자체의 대상 누락·조기 등록은 없었다. |

위 다섯 묶음은 현재 경로에서 복구했다. NPC 기능의 실제 플레이 실행은 검증하지 않았다.

## 오류와 구분한 비활성·빈 패치

- `[Many Tabs] Maple32 Furnace Tab`: 대상 누락 17개. `Many Tabs for Maple32`: 36개. 둘 다 includes의 `Maple32` 본체가 설치 목록에 없으므로 우선 선택적 연동 비활성으로 분류한다. 공유 설정 하나가 남아 있다고 모든 패치가 작동한다는 뜻은 아니다.
- `BK3K-Various Mods Compatibility`: 패치 43개 중 대상 42개가 없다. BK3K 본체는 설치되어 있고 설정 패치는 존재한다. 누락은 구형/선택적 개별 장비 대상이므로 로드 순서 고장으로 단정하지 않는다. 관련 Addon의 세 대상은 모두 있고 조기 등록도 없다.
- `Many Tabs for Terraforge (1/2)`: 대상 43개 누락. `(2/2)`는 대상 누락 없음. 여러 모드의 콘텐츠를 묶은 패치이므로 본체 없는 연동과 변경 경로를 추가 분리해야 한다.
- `Many Tabs for Saturnians`: 대상 한 개 누락. Saturnians 본체는 있으므로 해당 콘텐츠 이동·삭제 여부를 후속 점검 대상으로 남긴다.
- `Monster Compatibility Loader`: Shellguard sgcrystalboss 경로가 없지만 해당 패치 본문은 전부 주석인 빈 배열이다. 현재 기능 실패로 세지 않는다.
- `Black Armory Enhanced Storage`: filingcabinet/register 두 대상이 없고 같은 이름의 현재 본체 객체도 없다. 삭제된 가구일 가능성을 남기며 다른 가구에 임의로 적용하지 않는다.

## 후속 전체 정적 조사와 수정

이전 문서·manifest에 개별 근거가 명시되지 않은 pak 후보 480개에서 JSON 패치 23,505개와 Lua 패치 6개를 조사했다. 이는 실제 미조사 모드 수를 뜻하지 않는다. 이미 넓은 자산 검사에 포함되거나 다른 조사에서 일부 다뤄진 본체·번역도 후보에 포함되어 있다. 별도로 loose 폴더 6개에서 패치 394개를 파싱했고 문법 오류는 없었다.

최종 복구는 서로 다른 현재 자산 68개이며, 원본 소스별 복구 기록은 89개다. 중복된 구형 Felin 경로처럼 여러 기록이 같은 자산을 가리킬 수 있다. 별도로 기존 패치 본문 23개를 수정했다.

| 묶음 | 수정 내용 |
| --- | --- |
| Felin | 지하 생물군계 8개의 조우 목록과 Apex 반군 대사 한 경로를 복구. 바뀐 배열 번호를 사용하지 않고 undergroundencounterdungeons가 있는 목록에 중복 없이 추가한다. |
| Missing Music Addition | 잘못된 biome 단수 폴더의 패치 18개를 biomes의 실제 파일에 연결. 실제 설치된 음원만 추가하고 기존 재생 목록을 유지한다. |
| DRG Underground Music Replace | 실제 제공된 음원은 decieved.ogg인데 21개 패치가 deceived.ogg를 참조했다. 해당 파일들에서 낮·밤 참조 42곳을 수정했다. |
| Armok's Assorted Mod Fixes | 현재 주방 레시피 7개, 퀘스트 한 개, 인형 5개의 대상 경로를 복구. 새 본체에서 사라진 인형의 종족별 설명 필드는 추가 연산으로 전환했다. 기존 한국어 설명은 영문으로 덮지 않는다. 기존 조건이 현재 FU 설정과 다르면 그 연산은 건너뛴다. |
| Sexbound 종족/특수 객체 | 현재 twoactors 위치 설정으로 대사 연결을 복구. 침대 변형처럼 대사 필드를 base에서 상속하는 설정에는 필요한 override 테이블만 추가한다. 본체의 util_mergeConfig가 중첩 테이블을 병합하는 것을 확인했다. 동일 대사 등록은 중복하지 않는다. |
| Sexbound 임신 설정 | 현재 파일은 /sxb_plugin.pregnant.config이고 compatibleMates가 아닌 compatibleSpecies를 읽는다. 설치된 Kitsune, Viera, Arcana 3종의 대칭적인 구형 관계를 현재 whitelist에 병합한다. 현재 API는 아버지 종족으로 허용된 어머니 목록을 찾으므로 교차 종족 관계는 양방향으로 병합한다. 현행 새 형식 패치가 있는 Lucario는 그 패치를 우선한다. 미설치 Kemono는 복원하지 않는다. |
| Sexbound Mimic Support | 이미 현재 status 스크립트를 추가하면서 삭제된 /stats/sexbound/monster_primary.lua도 중복 호출하던 연산만 제거했다. |
| Betabound | 검사 도구 패치의 누락 쉼표와 중복 조건 그룹을 고치고 현재 도구 경로로 연결했다. 물 튀김 발사체의 기존 actionOnReap에 관개 효과를 중복 없이 추가한다. |
| 기타 | Starbound Patch Project의 Frozen Bow, Saturnians의 찻잔 설명, Customizable Shuttlecraft, Fixed Critters, Hop On Shops 및 Tougher Mobs의 이동된 대상에 원래 연산을 연결했다. Tougher Mobs의 sourceJSONAddress도 현재 경로로 바꿨다. |

후보는 파일명뿐 아니라 실제 itemName/objectName/type 및 현재 구조를 대조했다. 다른 UI 도구의 categories.config, WEdit 목록과 Tiled tileset, 일반 NPC 대사와 Sexbound 대사처럼 이름만 같고 스키마가 다른 파일은 연결하지 않았다. retired/선택적 콘텐츠가 없다고 본체 파일을 새로 만들지도 않았다.

Lua 원본 덮어쓰기 후보 88개도 현재 승자와 비교했다. 20개는 바이트가 같았다. 함수 이름 차이 후보 5개는 비행/차량 동작을 의도적으로 대체하는 애드온과 이미 적용한 FU 중심 상태 효과 통합에서 발생했다. 원본 함수가 사라졌다는 사실만으로 기능 손실로 단정하여 되돌리지 않았다. 모든 Lua 실행 경로를 실제 플레이로 검증한 것은 아니다.

남은 JSON 파싱 오류 세 개는 Tougher Mobs의 '- Copy' 백업 패치이며 대상 자산이 없다. 별도의 evilknightlord '- Copy' 스크립트 참조도 같은 유형이다. 사용 중인 leveling 설정으로 강제로 재연결하지 않는다. 없는 sourceJSONAddress 대부분도 미설치 Pandoras Box 등 대상 자체가 없는 패치에서 나왔다.

## 보류한 콘텐츠

Perennial Crops의 없어진 작물, More Planet Info의 미설치 행성 연동, BK3K/Many Tabs의 구형 장비·분류는 현재 대응하는 콘텐츠를 확인할 수 없는 경우 비활성 상태로 남긴다. 이름/파일명만 같은 자산으로 재연결하지 않는다. 특히 `/scripts/sexbound/plugins/pregnant.config`를 `/dialog/tentacles/pregnant.config`에 연결하는 것은 잘못된 후보다.

원래 소스에 남아 있는 조기 등록 목록에는 이미 통합 패치에서 늦게 재적용한 FU SAIL, Cosmic Husbandry, NPCSpawner, K'Rakoth 소총 등이 포함된다. 원본의 조기 등록 숫자를 새로운 오류 개수로 세지 않는다.

## 기록

`compat_sources/remaining_patch_inventory.json`에는 현재 파일 존재 여부와 이전 실제 로드 순서를 대조한 소스별 목록이 있다. 실행 기능 검증이나 모든 누락 대상의 고장 판정 목록은 아니다.

추가 근거는 `tmp/remaining-compat-audit-20260928/confirmed-evidence.json`, `remaining-path-candidates.json`, `current-explicit-patches.json`에 남겼다. `unreviewed-candidates.json`은 문서·기존 manifest에 이름이 명시되지 않은 소스를 찾는 휴리스틱 후보 목록이므로 실제 미조사 수로 사용하지 않는다.

재현 소스는 mods_src/female_overhaul와 compat_patch_overrides에 있다. compat_sources/remaining_patch_repairs.json에는 원본 경로, 현재 경로, 연산, 후보별 판단을 기록했다. 기존 패치 본문 수정은 tools/repack_compat_patch_overrides.py, 통합 수정은 tools/repack_overhaul.py로 배포한다. 실행 중인 게임/서버가 없을 때 교체했으며 수정 전 네 pak 사본은 tmp/remaining-compat-audit-20260928/before-paks의 .bak 파일이다.

## 최종 검증

실제 엔진의 최종 검사에서 자산 26,890개를 읽어 실패 0건, 수정 값 검사 224개에서 실패 0건, 복구 연산의 참조 파일 누락 0건을 확인했다. 정적으로 없는 대상 2,107개를 실행 중 생성된 자산과 다시 대조한 결과도 0개였다. Terraforge/Saturnians의 누락 파일명과 일치하는 다른 동적 경로도 발견되지 않았다.

배포 pak의 1,011개 항목은 재현 소스와 바이트 및 메타데이터가 일치한다. 기존 pak 본문 수정 도구는 메타데이터·자산 이름·수정하지 않은 바이트를 보존한 것도 확인한다. 로그는 tmp/remaining-compat-audit-20260928/starbound_server.log에 있다.

초기 기동에서는 probe 디렉터리 경로를 잘못 지정해 기능 검사가 제외되어 이를 수정했다. 첫 실제 검사에서는 인형 설명 필드 두 개와 미설치 Muli 작물에 대한 부적절한 단정이 드러났다. 인형 연산과 검사를 수정하고, 새 종족 API의 관계 방향도 보완한 후 최종 검사가 통과했다. 이 과정의 중간 결과를 최종 통과 결과로 세지 않는다.

이 검증은 자산·설정 및 서버 기동 범위다. 모든 NPC 상호작용, 조우 생성, 무기 사용, 종족·퀘스트·멀티플레이를 실제 플레이로 검증한 것은 아니다. 조건부 원본 패치가 현행 설정에서 의도적으로 건너뛰는 경우까지 강제로 적용하지 않았다.
