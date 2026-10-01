#!/usr/bin/env python3
# gen_0887: final non-description low-priority rows
import json, csv, re

T = {
'128476':'cute event',
'128479':'dark ambient 1',
'128480':'dark ambient 2',
'128488':'eight magics',
'128515':'https://loverslab.com/',
'128524':'insert item',
'128528':'ixoling grounds',
'128529':'japanese ruins',
'128576':'penguin highway',
'128584':'pistol Combo',
'128591':'ruined monastery',
'128596':'shores of tranquility',
'128609':'stage clear',
'128614':'tactical mace',
'128657':'the invasion',
'128664':'the tower invincible',
'128677':'tileBroken Workaround',
'128679':'tree fiddy',
'128680':'trieste forest',
'128689':'warlords might',
'128727':'{ "initialItems" : [ { "name" : "protectoratechest", "count" : 1 }, { "name" : "protectoratepants", "count" : 1 },  { "name" : "money", "count" : 20 }, { "name" : "protectorateflyer", "count" : 1 } ] }',
'128728':'{ "initialItems" : [ { "name" : "salve", "count" : 3 }, { "name" : "bandage", "count" : 2 }] }',
'128768':'«어른의 입문',
'128769':'«세 다리 팝톱의 춤',
'128770':'«반체제자 심문 #XXX',
'128771':'«클루엑스 사절 의식',
'128774':'«이브 부인, 19번',
'128775':'«새로운 굶주림',
'128776':'«교도관 오디오로그',
'128780':'«무서운 모닥불 이야기',
'128781':'«촉수 재앙 기원',
'128784':'«정욕의 하이로틀 승무원 1',
'128785':'«정욕의 하이로틀 승무원 2',
'128786':'«배고픈, 배고픈 플로란',
'128802':'홀로그램 기록: 코퍼스 기술자',
'128806':'샐리 보스전',
'128807':'음진 기록: ADF 팀',
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
with open('priority_0887.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
