#!/usr/bin/env python3
# gen_0876: non-description low-priority rows
import json, csv, re

T = {
'125865':'^noshadow;^#001054;의료 & 응급 용품',
'125866':'^noshadow;^#001054;가공 & 정제',
'125867':'^noshadow;^#001054;로봇공학 & AI',
'125868':'^noshadow;^#001054;봉제 & 섬유',
'125869':'^noshadow;^#001054;스텔라 도구 & 부품',
'125870':'^noshadow;^#001054;장난감 & 오락',
'125871':'^noshadow;^#0050c0;알타 아쿠아리움',
'125872':'^noshadow;^#0050c0;알타 건축 스테이션',
'125873':'^noshadow;^#0050c0;알타 아모리',
'125874':'^noshadow;^#0050c0;알타 베스티아리움',
'125875':'^noshadow;^#0050c0;알타 데이터센터',
'125876':'^noshadow;^#0050c0;알타 덴드라리움',
'125877':'^noshadow;^#0050c0;알타 에너지 스테이션',
'125878':'^noshadow;^#0050c0;알타 인섹타리움',
'125879':'^noshadow;^#0050c0;알타 이오노멜터',
'125880':'^noshadow;^#0050c0;알타 키치너',
'125881':'^noshadow;^#0050c0;알타 레스큐 스테이션',
'125882':'^noshadow;^#0050c0;알타 로보크래프터',
'125883':'^noshadow;^#0050c0;알타 스텔라리움',
'125884':'^noshadow;^#0050c0;알타 테일러',
'125885':'^noshadow;^#0050c0;알타 테라리움',
'125886':'^noshadow;^#0050c0;알타 토이메이커',
'125887':'^noshadow;^#0050c0;페스티브 스테이션',
'125888':'^noshadow;^#60c0fc;제작 스테이션',
'125893':'^orange; 권총',
'125909':'^orange;15 kW^reset;',
'125914':'^orange;30 kW^reset;',
'125919':'^orange;일상의 하루...^reset;',
'125920':'^orange;새로운 집',
'125921':'^orange;씨앗으로 시작...^reset;',
'125922':'^orange;보호받은 눈',
'125923':'^orange;보호받은 눈 II',
'125924':'^orange;보호받은 눈 III',
'125925':'^orange;보호받은 눈 IV',
'125926':'^orange;특별한 선물',
'125927':'^orange;특별한 선물 II',
'125928':'^orange;특별한 선물 III',
'125929':'^orange;안정된 쉴 곳...^reset;',
'125931':'^orange;복수의 맹세 II^reset;',
'125932':'^orange;복수의 맹세 I^reset;',
'125965':'^orange;중대한 발견!^reset;',
'125983':'^orange;현대식 가구와 기타 장식품을 만드는 프린터.^reset;',
'126005':'^orange;다양한 아르카나 아이템을 제작하는 작업대!^reset;',
'126006':'^orange;일어난 일에 대해^reset;',
'126007':'^orange;새로운 광물에 대해!^reset;',
'126012':'^orange;산성 전쟁',
'126013':'^orange;산성 전쟁 II',
'126014':'^orange;호흡 EPP 획득',
'126015':'^orange;냉각 EPP 획득',
'126016':'^orange;난방 EPP 획득',
'126017':'^orange;방사선 EPP 획득',
'126020':'^orange;고급 길튼 장비 제작.^reset;',
'126021':'^orange;고급 개인용 의약품',
'126026':'^orange;조준 대시 테크',
'126027':'^orange;알베르토-로타',
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
with open('priority_0876.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
