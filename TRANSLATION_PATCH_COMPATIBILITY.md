# 번역 패치 호환성 수정 — 2026-09-28

FUlocaleko와 female_translation의 converse replace를 개별 경로 존재 검사로
보호한다. 사라진 대사 하나 때문에 유효한 한국어 대사 그룹 전체가 롤백되던
문제를 해결하며, 폐기된 종족 대사를 다시 만들지 않는다.

FUlocaleko crafting의 itemName/value는 replace 대신 add로 적용한다.
Betabound가 이 필드를 제거한 구성에서도 번역이 적용된다. Quickbar의 옛
frackinuniverse 항목은 해당 항목이 존재할 때만 수정한다. BookOfSpirits의
displayTitleAsName도 add로 바꿔 필드가 없는 구성에서 false를 복원한다.

기존 upstream .patch 본문 수정 예외를 사용한다. 재현 소스는
compat_patch_overrides이며 tools/repack_compat_patch_overrides.py가 원본
자산 이름과 메타데이터를 보존하여 해당 본문만 교체한다. 모든 다른 자산의
바이트 동일성을 검사한 뒤 파일을 교체하며 게임 또는 서버 실행 중에는 거부한다.
번역 pak을 다시 생성한 후에는 이 도구를 다시 실행해야 한다.

별도 서버의 tmp/sail-startup-fix-20260928에서 대사, crafting, quickbar,
BookOfSpirits의 최종 자산 및 패치 오류 로그를 확인한다. 기존 저장 파일은
수정하지 않는다.
