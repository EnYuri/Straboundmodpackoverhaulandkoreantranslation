# FU S.A.I.L. 이미지 선택 호환성 — 2026-09-28

NonEKI의 `/zb/newSail/data.config.patch`는 FU 공용 애니메이션 템플릿의
idle/talk/refuse와 추가 표정을 `nonEKI.png`로 고정한다. FU의 [FS] 이미지
선택 메뉴는 `GUI.talker.imagePath`를 바꾸지만 고정된 템플릿에는 `<image>`가
없으므로 실제 표시 이미지가 바뀌지 않는다. 최종 엔진 자산에서 확인했다.
메뉴 콜백 자체의 예외는 이번 사용자 로그에서 발견되지 않았다.

`/zb/newSail/newSail.config.patch`가 FU의 FS 후속 스크립트 뒤에 로컬
`/female_overhaul/sail_animation_compat.lua`를 추가한다. 선택된 이미지가
NonEKI이면 원래 54프레임 idle 등 템플릿을 유지하고, 그 외에는 설치된 FU의
`<image>` 템플릿을 사용한다. NonEKI가 추가한 표정은 다른 이미지에서 FU의
refuse 애니메이션으로 대체한다. 이미지 선택 시 프레임/타이머를 초기화한다.

FU 기본 이미지 선택, FS 선택 이미지, Customisable A.I. 칩의 aiFrames를
기존 우선순위대로 사용한다. 종족 이미지·번역·칩 자산은 수정하지 않는다.
NonEKI의 다른 cinematic 프레임 누락은 이 수정의 검증 대상이 아니다.

검증 경로: `tmp/starter-sail-20260928`. 실제 엔진의 postLoad 환경에서
FS 메뉴 목록 생성과 apex/human/neki/angel 전환, NonEKI 복귀 및 칩 이미지
전환을 모의 GUI로 실행한다. 실제 플레이 화면에서 선택 후 표시 확인은 별도다.

## 새 캐릭터의 바닐라 S.A.I.L. 연결 수정 — 2026-09-28.6

Lustling의 일반 및 Tier0 콘솔에는 FU의 customtechstation.lua와 ScriptPane
설정이 없어서 바닐라 창이 열렸다. speciesShips의 실제 함선 구조와 blockKey에
등록된 콘솔 및 대응 Tier0를 기준으로 연결 누락과 FU 스크립트 중복을 보완했다.
52개 콘솔 패치에 기존 종족 스크립트를 유지하고 FU 스크립트는 한 번만 등록한다.
전용 GIC BLACKJACK/ANACONDA/CORPUS 콘솔 및 자체 상호작용 스크립트는 제외한다.
Lustling, Moogle, Arcanian 등의 기본 OpenAiInterface 콘솔은 FU ScriptPane로
연결하며 바닐라 fallback 설정도 유지한다.

검증은 tmp/sail-startup-fix-20260928에서 최종 콘솔 설정과 실제 로드된 FU
스크립트를 검사한다. 모의 함선 환경에서 init, 초기 함선 선택 창, FU 메뉴,
바닐라 fallback 경로를 실행한다. 실제 게임 화면의 확인은 별도로 필요하다.
