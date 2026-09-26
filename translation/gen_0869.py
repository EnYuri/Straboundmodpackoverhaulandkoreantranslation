#!/usr/bin/env python3
# gen_0869: non-description low-priority rows
import json, csv, re

T = {
'125228':'^green;뜨거운 뜨거운 냄비 요리',
'125229':'^green;네온멜론 잼 요리',
'125230':'^green;포제스트 요리',
'125231':'^green;매콤 깃털관 요리',
'125232':'^green;매콤 갈비 요리',
'125233':'^green;궁극의 주스 요리',
'125234':'^green;화산 살사 요리',
'125235':'^green;사마귀풀 잼 요리',
'125236':'^green;사마귀풀 스튜 요리',
'125237':'^green;구리 주괴 배달',
'125238':'^green;코럴크립 배달',
'125239':'^green;코어 파편 배달',
'125240':'^green;옥수수 배달',
'125241':'^green;목화 문제',
'125244':'^green;크레이턴의 심부름',
'125245':'^green;진홍의 조우^reset;',
'125247':'^green;커런트콘 배달',
'125250':'^green;다트 퀘스트',
'125251':'^green;다트 퀘스트 1',
'125252':'^green;다트 퀘스트 2',
'125253':'^green;다트 퀘스트 아레나 1',
'125254':'^green;다트 퀘스트 아레나 2',
'125256':'^green;미니크녹을 물리쳐라',
'125257':'^green;미니크녹을 물리치세요.',
'125258':'^green;사막 산적',
'125259':'^green;공성파괴자를 파괴하라',
'125260':'^green;공성파괴자를 파괴하세요.',
'125261':'^green;다이아몬드 배달',
'125262':'^green;알파카 발굴',
'125263':'^green;호박 발굴',
'125264':'^green;암모나이트 발굴',
'125265':'^green;에이펙스 발굴',
'125266':'^green;에이비언 발굴',
'125267':'^green;에이비오스케일 발굴',
'125268':'^green;알 발굴',
'125269':'^green;고사리 발굴',
'125270':'^green;물고기 발굴',
'125271':'^green;플로란 발굴',
'125272':'^green;발자국 발굴',
'125273':'^green;프로그 발굴',
'125274':'^green;글리치 발굴',
'125275':'^green;인간 발굴',
'125276':'^green;하이로틀 발굴',
'125277':'^green;익소둠 발굴',
'125278':'^green;수수께끼의 외계인 발굴',
'125279':'^green;수수께끼의 발굴?',
'125280':'^green;오피던트 발굴',
'125281':'^green;펭귄 발굴',
'125282':'^green;검치호 발굴',
'125283':'^green;티라노 발굴',
'125284':'^green;삼엽충 발굴',
'125285':'^green;흙고슴도치 배달',
'125286':'^green;머나먼 별들',
'125287':'^green;감시자들의 드로덴',
'125288':'^green;듀라스틸 주괴 배달',
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
with open('priority_0869.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
