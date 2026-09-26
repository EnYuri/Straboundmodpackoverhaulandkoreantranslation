#!/usr/bin/env python3
# gen_0880: non-description low-priority rows
import json, csv, re

T = {
'126561':'^orange;회상: 코스모 네메시스^reset;',
'126562':'^orange;회상: 에르키우스 전령^reset;',
'126563':'^orange;회상: 에볼라피스^reset;',
'126564':'^orange;회상: 마법왕^reset;',
'126565':'^orange;회상: 샌드바타르^reset;',
'126566':'^orange;회상: 먼지의 탐구자^reset;',
'126567':'^orange;회상: 항해사^reset;',
'126568':'^orange;회상: 역병 의사^reset;',
'126569':'^orange;회상: 보이드 디포미티^reset;',
'126570':'^orange;회상: 보이드 메리시스^reset;',
'126571':'^orange;회상: 몰튼 나이트^reset;',
'126572':'^orange;회상: 사신^reset;',
'126573':'^orange;회상: 솔라 가디언^reset;',
'126575':'^orange;아스라 녹스 영입',
'126577':'^orange;비행의 힘 되찾기',
'126578':'^orange;유물 재조합기^reset;는 ^cyan;일반 유물의 퍽을 편집^reset;할 수 있는 기계다.\n일반 유물의 퍽을 편집하려면 ^green;왼쪽 아이템 슬롯에 놓아야 한다^reset;. 놓으면 아래에 퍽의 모든 정보가 보이고, ^green;^orange;레벨^green;이 쌓인 블록으로 표시^reset;된다. 유물의 첫 번째 퍽은 ^orange;메인 퍽^reset;으로 편집할 수 없다.\n오른쪽 아이템 슬롯에는 ^cyan;다른 일반 유물이나 각인 글리프를 놓을 수 있다^reset;. 놓으면 그 퍽이 오른쪽 아이템 슬롯 아래의 ^orange;퍽 선택 영역^reset;에 표시된다.',
'126579':'^orange;유물^reset;\n유물은 아르카나 지하에서 드물게 만나는 조우에서 얻을 수 있다. 유물을 활성화하려면 사용 가능한 슬롯 중 하나에 넣어라.',
'126582':'^orange;리플리케이터가 돌아왔다...',
'126583':'^orange;과거 복원',
'126584':'^orange;과거 복원 II',
'126585':'^orange;과거 복원 III',
'126588':'^orange;로이 헌트스탕 - 화염 연금술사^reset;',
'126594':'^orange;또 다른 임무에 안장 올리고...^reset;',
'126596':'^orange;샌드크롤러의 기쁨',
'126598':'^orange;모래 여정^reset;',
'126602':'^orange;새첼 차지^reset;',
'126606':'^orange;산악 오르기',
'126609':'^orange;탐구자 아틀라스^reset;',
'126610':'^orange;탐구자 레벨^reset;',
'126612':'^orange;탐구자 권총 업그레이드^reset;',
'126613':'^orange;반자동 소총',
'126614':'^orange;반자동 산탄총^reset;',
'126628':'^orange;산탄총^reset;',
'126678':'^orange;소음 저격소총^reset;',
'126686':'^orange;태양 폭발',
'126689':'^orange;군인',
'126691':'^orange;특수전술 공기소총^reset;',
'126692':'^orange;특수 군용 활^reset;',
'126697':'^orange;시작 퀘스트 템플릿',
'126701':'^orange;아직 초기 시절^reset;',
'126706':'^orange;타락 저지',
'126710':'^orange;기절',
'126711':'^orange;기관단총^reset;',
'126712':'^orange;기관단총 | UGL 미지원.^reset;',
'126713':'^orange;자폭형 대전차 무기^white;',
'126714':'^orange;소환 의식',
'126717':'^orange;슈퍼스톰 스타 - 8등급^reset;',
'126719':'^orange;스시스퀴드',
'126727':'^orange;테크 카빈^reset;',
'126729':'^orange;기술 지원',
'126731':'^orange;빛과 어둠의 신전',
'126736':'^orange;마름병 동굴',
'126740':'^orange;군단의 검',
'126741':'^orange;군단의 검 II',
'126742':'^orange;로드스타 신전^reset;',
}

TAG = re.compile(r'\^[a-zA-Z]+;|\^#[0-9a-fA-F,]+;')
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
with open('priority_0880.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
