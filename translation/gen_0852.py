#!/usr/bin/env python3
# gen_0852: non-description low-priority rows
import json, csv, re

T = {
'121620':'잔다름 프라임',
'121634':'제르케시움 II',
'121662':'조이 콘스텔라',
'121756':'[Cyberrpunk 2077]',
'121786':'[GIC:E] 지원 전투준비 재사용 대기 중',
'121787':'[GIC:E] 공격 전투준비 재사용 대기 중',
'121788':'[GIC:E] 방어 전투준비 재사용 대기 중',
'121790':'[GIC] 나리아키라 재사용 대기시간 - 이 상태가 끝날 때까지 전력 찌르기 불가.',
'121896':'[SxB] 부활절 토끼',
'122033':'^#000000;^reset;^yellow;아르카나^reset; - 시작하기',
'122034':'^#000000;^reset;^yellow;아르카나^reset; - 진행',
'122117':'^#0040a8;알데론 지휘 센터: 연결됨^reset;',
'122118':'^#0040a8;알리아나 지휘 센터: 연결됨^reset;',
'122119':'^#0040a8;세테라이 T. 운영체제^reset;',
'122135':'^#00BFFF;적응형 EM 카빈^reset;',
'122136':'^#00BFFF;레일 소총^reset;',
'122222':'^#0b0;0x00FF00^white;\n^shadow;^#dff;마법^white;\n^shadow;^#ddd;Silverfeelin^reset;\n^shadow;^#44d;사과^white;',
'122223':'^#0f0;연금술',
'122224':'^#0f0;도살자, 제빵사, 미망인 제조자',
'122235':'^#14e903;돌격소총^reset; | ^cyan;조준경: 레일식 ^reset;| ^green;총열: ccr ^reset;| ^cyan;총열하부: 레일식^reset;',
'122236':'^#14e903;돌격소총^reset; | ^yellow;조준경: 리시버 ^reset;|^yellow;총열하부: AK^reset;',
'122237':'^#14e903;다목적 기관총^reset; | ^cyan;고정 양각대: 접힘^reset;',
'122238':'^#14e903;다목적 기관총^reset; | ^cyan;고정 양각대^reset;',
'122239':'^#14e903;경기관총^reset; | ^yellow;조준경: 리시버^reset; | ^green;총열: KOL^reset;',
'122240':'^#14e903;기관단총^reset; | ^cyan;조준경: 레일식 ^reset;',
'122241':'^#14e903;산탄총^reset; | ^cyan;조준경: 레일 ^reset;',
'122242':'^#14e903;산탄총^reset; | ^yellow;반자동 ^reset;',
'122243':'^#14e903;산탄총^reset; | ^yellow;총열하부: 손전등',
'122244':'^#14e903;기관단총^reset; | ^cyan;조준경: 레일식 ^reset;| ^green;총열: .45 ^reset;| ^cyan;총열하부: 레일식^reset;',
'122245':'^#14e903;기관단총^reset; | ^yellow;조준경: 리시버^reset; | ^cyan;총열하부: 레일식^reset;',
'122246':'^#159753;자동 조립^reset;',
'122247':'^#190700;비용:',
'122248':'^#190700;사용 가능 재료',
'122249':'^#190700;레시피',
'122260':'^#1E90FF;플라즈마 산탄총',
'122270':'^#2020FF;블루',
'122288':'^#2080f0;C.T.^#f6f6f6;O.S.^reset;',
'122306':'^#20FF20;그린',
'122317':'^#20f080;정예^reset; 자동보호병',
'122320':'^#20f080;정예^reset; 대형',
'122323':'^#20f080;정예^reset; 보호 명령',
'122348':'^#29FFFF;파워 경기관총^reset; | ^cyan;고정 양각대^reset;',
'122349':'^#29FFFF;스마트 돌격소총^reset;',
'122350':'^#29FFFF;스마트 산탄총^reset;',
'122351':'^#29FFFF;스마트 저격소총^reset;',
'122352':'^#29FFFF;스마트 기관단총^reset;',
'122353':'^#29FFFF;테크 정밀소총^reset;',
'122354':'^#29FFFF;테크 리볼버^reset;',
'122355':'^#29FFFF;테크 저격소총^reset;',
'122356':'^#29ffff;파워 이중총열 산탄총^reset;',
'122357':'^#29ffff;파워 저격소총^reset;| ^cyan;고정 양각대^reset;',
'122358':'^#29ffff;스마트 이중총열 산탄총^reset;',
'122359':'^#29ffff;테크 이중총열 산탄총^reset;',
'122368':'^#363636;화염^reset;',
'122369':'^#363636;얼음^reset;',
}

TAG = re.compile(r'\^[a-zA-Z]+;|\^#[0-9a-fA-F]+;|\[[A-Za-z:]+\]')
src = {}
with open('rest_worklist.tsv', encoding='utf-8-sig', newline='') as f:
    for r in csv.DictReader(f, delimiter='\t'):
        if r['id'] in T:
            src[r['id']] = r['englishText']
bad = []
for i, ko in T.items():
    s = src.get(i)
    if s is None:
        bad.append(('MISSING', i)); continue
    if TAG.findall(s) != TAG.findall(ko):
        bad.append(('TAG', i))
    if s.count('\n') != ko.count('\n'):
        bad.append(('NL', i))
print('bad:', bad)
print(len(T))
with open('priority_0852.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
