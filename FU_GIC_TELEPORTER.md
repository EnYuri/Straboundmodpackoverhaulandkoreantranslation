# 공용 텔레포터 창 점검 — 2026-09-28

보고된 증상: 함선·설치형 등 모든 텔레포터에서 목적지 목록이 비어 보임.

## FU 외에 관여하는 모드

- GIC: 공용 `teleportdialog.config`를 전체 대체하고 3열 목록을 지정한다.
- Extended GUI: 공용 창 높이와 목록 영역을 늘린다.
- Bigger Teleporter GUI (4x), Workshop 2494853338: 마지막으로 4열·큰 창
  배치와 전역 `warpheader/body/footer.png`를 적용한다.
- 한국어 번역: 공용 창 문구를 수정한다. 목적지 목록은 삭제하지 않는다.
- More Teleportz: 추가 텔레포터 물체를 제공한다. 확인한 2stopteleporter는
  정상적인 `OpenTeleportDialog` 및 공용 remoteteleporter 설정을 사용한다.
- Law Enforcement와 Cosmic Husbandry: 조건부 목적지를 추가한다.
- Anom's Outpost: 전초기지 목적지의 이름·도착점을 보정한다.

FU 본체는 공용 `teleportdialog.config`를 제공하지 않는다. FU BYOS
텔레포터는 정상적인 `OpenTeleportDialog`와 shipteleporter 설정을 사용한다.

## 데이터 점검

현재 플레이어 저장 파일을 읽기 전용으로 추출했다. 현재 우주에 속한
텔레포트 북마크 3개가 존재하며 플레이어와 universe.dat의 우주 UUID가
일치한다. 북마크 삭제나 우주 UUID 변경은 관측되지 않았다.
목적지 설정을 전부 비우는 활성 패치도 관측되지 않았다.

[설치 버전에 대응하는 엔진의 텔레포터 코드](https://github.com/OpenStarbound/OpenStarbound/blob/v0.1.15.1/source/frontend/StarTeleportDialog.cpp)는
고정 목적지·파티원·플레이어 북마크를 공용 목록에 추가한다.
따라서 목록 데이터와 목록 UI를 별도로 확인했다. 실제 빈 목록 증상의
원인을 특정 모드로 확정한 것은 아니다.

## 적용한 표시 호환성 수정

사용자 지정에 따라 `female_overhaul`의 늦은 JSON 패치로 공용 창을
Bigger Teleporter GUI (4x)의 4열·16행 배치로 통일했다.
해당 모드의 배경 이미지 3개에는 전용 경로를 사용해
GIC와 Bigger Teleporter GUI의 전역 이미지 대체에 영향을 받지 않는다.
목적지·북마크·텔레포터 물체·스크립트는 수정하지 않았다.

최종 엔진 자산과 서버 검증은 `tmp/fu-gic-teleporter-20260928`에 기록한다.
게임 재실행 후 실제 텔레포터 목록을 확인해야 증상 해결 여부를 확정할 수 있다.
