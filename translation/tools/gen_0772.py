#!/usr/bin/env python3
# gen_0772: non-description low-priority rows (EDS/EP series)
import json, csv, re

T = {
'60434':'염료 한도',
'60444':'역동적인 듀오',
'60454':'EDS 안드로이드',
'60455':'EDS 기록관',
'60456':'EDS 전투 기계',
'60457':'EDS 지휘 통신 기록',
'60458':'EDS 지휘관',
'60460':'EDS 드라이',
'60461':'EDS 드론',
'60463':'EDS 경비병',
'60464':'EDS 중무장 병사',
'60466':'EDS 이스토코어',
'60467':'EDS 장교',
'60468':'EDS 패드',
'60469':'EDS 프로티스',
'60470':'EDS 연구원',
'60473':'EDS 보안',
'60474':'EDS 서버 연결 기록',
'60475':'EDS 보호막',
'60476':'EDS 상태 분석',
'60478':'EDS 타움',
'60479':'EDS 베우스',
'60480':'EDS 바이얼',
'60483':'Starbound 자동 업데이터용 EE.',
'60484':'에페르본 부식 - 총기 저항 -35% | 방어구 방어 수치 -80%.',
'60487':'일렉트로켐 시설',
'60492':'비밀번호 입력',
'60501':'EP0 666 스테이지',
'60502':'EP0 보스 준비',
'60503':'EP0 돌파',
'60504':'EP0 입구',
'60505':'EP0 탈출 전투',
'60506':'EP0 탈출 긴장',
'60507':'EP0 최종 보스',
'60508':'EP0 1층',
'60509':'EP0 1/2층 보스',
'60510':'EP0 2층',
'60511':'EP0 3층',
'60512':'EP0 4층',
'60513':'EP0 5층',
'60514':'EP0 5층 전투',
'60515':'EP0 5층 긴장',
'60516':'EP1 최종 보스',
'60517':'EP1 스테이지 1',
'60518':'EP1 스테이지 3',
'60519':'EP1 스테이지 4',
'60520':'EP1 스테이지 5',
'60521':'EP2 동굴 스테이지',
'60522':'EP2 최종 결전',
'60523':'EP2 비밀방',
'60524':'EP2 스테이지 1',
'60525':'EP2 스테이지 10',
'60526':'EP2 스테이지 2',
'60527':'EP2 스테이지 3',
'60528':'EP2 스테이지 5',
}

TAG = re.compile(r'\^[a-zA-Z]+;|\^#[0-9a-fA-F]+;')
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
with open('priority_0772.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
