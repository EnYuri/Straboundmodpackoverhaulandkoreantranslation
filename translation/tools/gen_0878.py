#!/usr/bin/env python3
# gen_0878: non-description low-priority rows
import json, csv, re

T = {
'126239':'^orange;던전 1^reset; / P2C-224',
'126240':'^orange;던전 2^reset; / P6L-654',
'126241':'^orange;던전 3^reset; / P1R-441',
'126242':'^orange;던전 4^reset; / 비우스 교도소',
'126243':'^orange;던전 5^reset; / P1V-397',
'126244':'^orange;던전 6^reset; / 리플리케이터',
'126245':'^orange;던전 7^reset; / P1S-246',
'126249':'^orange;에두아르 에릭 - 완전한 광산 연금술사^reset;',
'126250':'^orange;네크로이움을 효율적으로 제련하고 호라이즌 병기를 구축합니다.^reset;',
'126259':'^orange;장착^reset;',
'126265':'^orange;더 많은 마기사이트^reset;',
'126267':'^orange;이벤트 알림 처리기',
'126268':'^orange;다른 에디션의 모든 것!',
'126269':'^orange;엑스칼리버 재림',
'126270':'^orange;엑스칼리버 재림 II',
'126271':'^orange;엑스칼리버 재림 III',
'126272':'^orange;엑스칼리버 재림 IV',
'126275':'^orange;엑셀시어 조립',
'126280':'^orange;일회용 마그네-레일 발사기^reset;',
'126282':'^orange;실험형 유탄 소총^reset;',
'126287':'^orange;추출 장치',
'126290':'^orange;깃털 가족 채우기!^reset;',
'126291':'^orange;최종 스탯.^reset;',
'126293':'^orange;노바키드 유물을 찾으세요.',
'126295':'^orange;첫 접촉...^reset;',
'126296':'^orange;대공포^reset;',
'126297':'^orange;화염포^reset;',
'126298':'^orange;조명탄 권총^reset;',
'126301':'^orange;과학을 위해 !',
'126302':'^orange;전설 벼리기',
'126303':'^orange;전설 벼리기 II',
'126304':'^orange;잊혀진 신들',
'126307':'^orange;방주 너머에서',
'126315':'^orange;은하 지도^reset;',
'126318':'^orange;장비 갖추기',
'126319':'^orange;시작하기^reset;',
'126320':'^orange;빙하의 뾰족이',
'126330':'^orange;유탄 방출기^reset;',
'126333':'^orange;미스터리 안내^reset;',
'126337':'^orange;HYLas 캐논^reset;',
'126339':'^orange;타락 다루기',
'126340':'^orange;타락 다루기 II',
'126341':'^orange;타락 다루기 III',
'126342':'^orange;정말 리플리케이터를 파괴한 걸까?',
'126346':'^orange;중형 체인 산탄총^reset;',
'126347':'^orange;중형 미니건^reset;',
'126348':'^orange;중형 미사일 발사기^reset;',
'126349':'^orange;중형 RPG 발사기^reset;',
'126350':'^orange;구인: 완벽한 농장 짓기',
'126351':'^orange;헨리의 실험',
'126353':'^orange;성스러운 브로드소드^reset;',
'126354':'^orange;성스러운 방패',
'126355':'^orange;성스러운 창',
'126361':'^orange;일람 이카, 나르엘다^reset;',
'126363':'^orange;일루미네이티드 스타 - 7등급^reset;',
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
with open('priority_0878.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
