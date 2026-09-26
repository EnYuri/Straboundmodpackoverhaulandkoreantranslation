#!/usr/bin/env python3
# gen_0750: non-description low-priority rows
import json, csv, re

T = {
'50513':'아비칸 감시자',
'50516':'아비칸 물 상인',
'50520':'아비칸 무기 상인',
'50523':'아비칸 용접공',
'50550':'아볼라이트 세례',
'50555':'아볼라이트 파편',
'50681':'도끼 베기',
'50699':'아야 에린',
'50701':'아야 피리',
'50704':'아야 이조히비',
'50706':'아야 쿠이',
'50708':'아야 팝',
'50711':'아야 푸비',
'50715':"아야 브에이",
'50720':'아야-팝 이조히비',
'50722':'아야-차이 야키',
'50726':'아야카 아믹',
'50732':'아야카 패드',
'50742':'아야코이칼린 치',
'50743':'아얄라의 공포 가게',
'50745':'아야믹스 이조히비',
'50762':'아주르 블루',
'50786':'B. 화학자 승무원',
'50790':'BADS 권고',
'50793':'바트는 방귀와 라임이야',
'50800':'BL3 메이햄 테이블',
'50803':'피의 광란: 처치할 때마다 힘과 속도 증가',
'50806':'보스 전투',
'50827':'BP 수류탄 화살',
'50833':'BRZRK -1',
'50834':'BRZRK -2',
'50835':'BRZRK -3',
'50836':'BRZRK 0',
'50837':'BRZRK 1',
'50838':'BRZRK 10',
'50839':'BRZRK 2',
'50840':'BRZRK 3',
'50841':'BRZRK 4',
'50842':'BRZRK 5',
'50843':'BRZRK 6',
'50844':'BRZRK 7',
'50845':'BRZRK 8',
'50846':'BRZRK 9',
'50870':'크레온 대사관으로 귀환',
'50871':'ST 실렉티스로 귀환',
'50872':'별여행자 피난처로 귀환',
'50877':'예비 은신장',
'50880':'후진 II',
'50881':'후진 III',
'50882':'예비 비행선 장비 <role>',
'50883':'베이컨 브라운',
'50900':'배지 교환기',
'50903':'바프흐 이조히비',
'50954':'대나무 물품',
'50971':'붕대 감음 - 1초에 걸쳐 체력 50 회복.',
}

TAG = re.compile(r'\^[a-zA-Z]+;|\^#[0-9a-fA-F]+;')
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
with open('priority_0750.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
