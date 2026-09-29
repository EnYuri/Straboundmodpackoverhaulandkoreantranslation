# FFS 호환성 점검 — 2026-09-28.10

Feast of Fire and Smoke 본체와 설치된 FFS 애드온 5개, FFS 자산을 수정하는
FU·RPG Growth·Tougher Mobs·NPC 대사·외형·번역 등의 소스 8개를 조사했다.
`tmp/ffs-compat-audit-20260928/focused.json`과 `inventory.json`에 목록,
누락 대상과 덮어쓰기 관계를 기록했다.

## 수정

| 모드 | 문제 | 수정 |
| --- | --- | --- |
| FFS Dungeons and Encounters | atropuswartfield 패치에 .biome 확장자가 없음 | 실제 FU 생물군계에 원래 조우 3개 연결 |
| FFS Dungeons and Encounters | deadwood를 deadwoord로 지정 | 실제 FU 생물군계에 원래 조우 4개 연결 |
| FFS-Ified Vanilla Dungeons | Apex 파일 3개를 존재하지 않는 missions/apexbase에서 찾음 | 실제 dungeons/apex/apexbase에 드론 교체 패치 연결 |
| FFSE Rylasasin Edition | Avali 함장 captain을 captian으로 지정 | 올바른 NPC에 원래 무기 배정 패치 연결. 선택적 data/sheathedprimary 삭제는 존재 여부 검사 |
| Coordinator and Weapon Tags + RPG Growth | 무기 84개에서 보너스 태그 중복 확인 | 해당 패치의 무기 92개에서 첫 태그와 순서를 유지하고 중복 제거 |

경로 수정 6개는 `redirects.json`에 원본 연산을 기록했다.
무기 배정에 사용한 FFS 아이템 이름도 설치 자산에서 확인했다.
모든 수정은 `mods_src/female_overhaul`에 있으며 FFS 원본 pak는 변경하지 않는다.

## 덮어쓰기 및 선택적 연동

- Expanded 무기 팩은 설치된 Rylasasin 판 하나를 확인했다.
- Dungeon Tweaks의 미션 맵·보스·이동 스크립트 덮어쓰기는 해당 애드온 기능이다.
  회복 스크립트도 본체보다 뒤에 적용된다. 예를 들어 의료 키트의 회복률은
  Tweaks가 1.0에서 0.20으로 줄이는 조정이며, 이를 본체 값으로 되돌리지 않았다.
- FFS 무기 태그와 coordinator의 NPC 전투 설정은 실제 최종 자산으로 검사한다.
- 누락된 m32 계열 등 선택적 생물군계와 `ffs_avali_treasure_dae`는 설치된
  원본 대상이 없어 다른 생물군계/보물 목록에 억지로 연결하지 않았다.
- `penumbra.biome - Copy.patch`는 복사본 이름이며 올바른 penumbra 패치도 있다.
- 구형 `/ivrpgExcludeMonsterAI.config` 패치는 현재 설치된 RPG에서 해당 원본과
  참조 코드를 찾지 못했다. 현재의 경험치 연동 패치와 구분하여 기록했다.

## 검증과 배포

Starbound 엔진에서 관련 JSON 자산 7,213개를 읽고, 수정한 6개 대상의
설정 16개, 무기 보너스 태그 118개와 coordinator 설정 102개를 확인한다.
결과와 로그는 `tmp/ffs-compat-audit-20260928`에 보관했다.
기존 게임 저장 파일을 바꾸지 않는 별도 서버 저장소로 검사했다.
모든 FFS 에피소드와 실제 NPC 전투를 플레이한 검증은 아니다.
생물군계 조우 수정은 새로 생성되는 지역에 반영된다.

재배포 명령은 `python tools/repack_overhaul.py`다. 적용 버전은
`2026-09-28.10`. 변경 전 팩은 검사 폴더의
`zz_female_overhaul-before.pak.bak`에 보관했다. `.pak.bak` 확장자를 사용하여
검사 모드 소스로 함께 로드되지 않도록 했다.
