#!/usr/bin/env python3
# gen_0886: non-description low-priority rows
import json, csv, re

T = {
'127970':'^yellow;유물^reset; - ^#8f82e9;츠키츠네^reset;',
'127971':'^yellow;유물^reset; - ^#EDA946;트라요 ^#5144A5;다^#9AEFF5;타바^reset;',
'127985':'^yellow;볼트액션 소총^reset;',
'127986':'^yellow;책^reset;',
'127987':'^yellow;튕김 - 표면에서 튕긴다. 모든 낙하 피해를 무효화한다.',
'127988':'^yellow;불펍 대물 소총^reset;',
'127990':'^yellow;치피%^reset;',
'127995':'^yellow;선장',
'128021':'^yellow;행운 상자 하나를 골라 구매하세요!\n^reset;^green;2시간마다^reset; 상자 하나만 살 수 있습니다.',
'128022':'^yellow;클레이모어^#reset;',
'128027':'^yellow;정복자',
'128029':'^yellow;이 메카 부품은 노바 스테이션 왼쪽 아래에서 제작하세요!',
'128030':'^yellow;개조 반자동 소총',
'128031':'^yellow;개조 레버액션 소총',
'128034':'^yellow;축축 - ^orange;화염^yellow; 피해 -30%, ^purple;전기^yellow; 피해 +30%.',
'128041':'^yellow;난이도 : ^red;하드코어 - 5등급',
'128042':'^yellow;난이도 : ^red;하드코어 - 7등급',
'128043':'^yellow;난이도 : ^red;하드코어 - 6등급',
'128044':'^yellow;난이도 : ^white;어려움 - 3등급',
'128045':'^yellow;난이도 : ^white;어려움 - 5등급',
'128046':'^yellow;난이도 : ^white;어려움 - 7등급',
'128047':'^yellow;난이도 : ^white;보통 - 1등급',
'128053':'^yellow;강화 질주^reset;',
'128060':'^yellow;탐험가',
'128061':'^yellow;탐험가의 일지',
'128064':'^yellow;FU 가이드^reset; : 초보자 ITN',
'128065':'^yellow;FU 가이드^reset; 아이템 네트워크',
'128072':'^yellow;츠키카게의 빛^reset;',
'128086':'^yellow;인간 경로 선택기^reset;',
'128101':'^yellow;이온 공명',
'128133':'^yellow;나노스킨 구체화^reset;',
'128135':'^yellow;다음 지역',
'128141':'^yellow;과부하',
'128151':'^yellow;개척자',
'128156':'^yellow;파워 권총^reset;',
'128164':'^yellow;종족 특성',
'128177':'^yellow;고슴도치 세이미',
'128179':'^yellow;스카우트',
'128193':'^yellow;안정된 비행^reset;',
'128196':'^yellow;물범벅 - ^cyan;냉기^yellow; 피해 -50%, ^green;독^yellow; 피해 +50%. ^green;독^yellow; 효과를 강화한다.',
'128203':'^yellow;타르 묻음 - 이동이 약간 감소, ^purple;전기^yellow; 피해 -50%, ^orange;화염^yellow; 피해 +50%. ^orange;화염^yellow; 효과를 강화한다.',
'128223':'^yellow;프레토리안 프로젝트^reset; - I',
'128224':'^yellow;프레토리안 프로젝트^reset; - II',
'128225':'^yellow;프레토리안 프로젝트^reset; - III',
'128233':'^yellow;방랑자의 꿈',
'128240':'^yellow;도둑',
'128242':'^yellow;보물',
'128254':'^yellow;젖음 - 화염 저항과 전기 감수성이 증가. 가벼운 행성 열기를 저항하고 치명적 냉기를 더 강하게 만든다.',
'128255':'^yellow;젖음 - ^orange;화염^yellow; 피해 -50%, ^purple;전기^yellow; 피해 +50%. ^orange;전기^yellow;와 ^cyan;냉기^yellow; 효과를 강화한다.',
'128261':'^yellow;요프^reset;',
'128263':'^yellow;요괴 경로 선택기^reset;',
'128266':'^yellow;[메카 부품은 노바 스테이션 왼쪽 아래에서 제작하세요!]',
'128274':'^yellow;[리다이렉트 불가]^reset;.',
'128276':'^yellow;⟦E024⟧ ^shadow;^#ffdb8a;그린의 염료 세트 ^yellow;⟦E024⟧^reset;',
'128279':'^yellow;⟦E024⟧^reset;',
'128406':'access point',
'128441':'atropus ambience 1',
'128442':'atropus ambience 2',
'128443':'atropus ambience 3',
'128444':'atropus ambience 4',
}

TAG = re.compile(r'\^[a-zA-Z]+;|\^#[0-9a-fA-F,]+;')
src = {}
with open('data/rest_worklist.tsv', encoding='utf-8-sig', newline='') as f:
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
with open('priority_0886.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
