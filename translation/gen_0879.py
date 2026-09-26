#!/usr/bin/env python3
# gen_0879: non-description low-priority rows
import json, csv, re

T = {
'126365':'^orange;뱀의 소굴에서!^reset;',
'126366':'^orange;소이탄 저격소총^reset;',
'126373':'^orange;소개^reset;',
'126375':'^orange;친구 초대하기',
'126376':'^orange;이온 천둥',
'126381':'^orange;저스티카를 위한 정의',
'126384':'^orange;카타헬의 유산',
'126386':'^orange;키',
'126394':'^orange;유물의 전설 - ^#7a34cb;섀더^#c570f7;스트로피^reset;',
'126395':'^orange;유물의 전설 - ^#8f82e9;츠키츠네^reset;',
'126396':'^orange;유물의 전설 - ^#EDA946;트라요 ^#5144A5;다^#9AEFF5;타바^reset;',
'126397':'^orange;유물의 전설 - ^yellow;에스카톤 탐구자^reset;',
'126401':'^orange;레버액션 EM 소총^reset;',
'126402':'^orange;경기관총',
'126424':'^orange;마그네-코일 소총^reset;',
'126426':'^orange;밭 만들기',
'126429':'^orange;옛 사람들의 필사본',
'126430':'^orange;사수 소총 | UGL 장착 불가.^reset;',
'126431':'^orange;재료 조립^reset;',
'126432':'^orange;최대 레벨 도달!^reset;',
'126438':'^orange;위협적인 악몽^reset;',
'126440':'^orange;금속 거미 ?',
'126446':'^orange;광부의 불편',
'126447':'^orange;채광^reset;',
'126454':'^orange;마기사이트 소동^reset;',
'126455':'^orange;멀티 점프 Mk II 테크',
'126456':'^orange;다중 로켓 발사기^reset;',
'126462':'^orange;새 이벤트: ^gray;해로잉^reset;',
'126463':'^orange;새 이벤트: ^gray;착륙제^reset;',
'126478':'^orange;하늘의 천문대',
'126481':'^orange;징조^reset; - 간헐적 기억상실과 폭력성 증가. ^red;조치를 취하지 않으면 상황이 더 심각해진다.',
'126483':'^orange;모두를 위한 하나',
'126502':'^orange;낙하산병 볼트액션 소총^reset;',
'126503':'^orange;후원자들',
'126504':'^orange;사람들',
'126506':'^orange;퍽 이전^reset;',
'126508':'^orange;개인용 자동포 시스템^reset;',
'126509':'^orange;개인용 포 시스템^reset;',
'126510':'^orange;개인 방어 무기^reset; | ^orange;UGL이나 전방 손잡이 장착 불가.^reset;',
'126517':'^orange;플라스마 수류탄^reset;',
'126521':'^orange;동력^reset;',
'126523':'^orange;프라임 회로',
'126525':'^orange;프라임 회로 II',
'126526':'^orange;프라임 회로 III',
'126527':'^orange;프라임 회로 IV',
'126531':'^orange;진행^reset;',
'126534':'^orange;자신을 증명하라',
'126535':'^orange;펄스 PDW^reset;',
'126536':'^orange;성가신 피라미드 해충 퇴치',
'126546':'^orange;RPG 발사기^reset;',
'126548':'^orange;분노 의식 I',
'126549':'^orange;분노 의식 II',
'126554':'^orange;레일 소총^reset;',
'126559':'^orange;유물 재건^reset;',
'126560':'^orange;회상: 이온 타임피스^reset;',
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
with open('priority_0879.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
