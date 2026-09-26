#!/usr/bin/env python3
# gen_0877: non-description low-priority rows
import json, csv, re

T = {
'126054':'^orange;항상 과학을 위해 !',
'126070':'^orange;알 수 없는 유물...^reset;',
'126075':'^orange;고대 요새',
'126081':'^orange;동물 실험',
'126082':'^orange;대물 소총^reset;',
'126083':'^orange;대물 소총^reset;',
'126084':'^orange;대물 소총^reset;',
'126085':'^orange;대물 소총 | UGL 장착 불가.^reset;',
'126087':'^orange;에이펙스 루이스 - 강력한 농장 연금술사^reset;',
'126090':'^orange;아프로디테의 활',
'126091':'^orange;아프로디테의 지팡이',
'126093':'^orange;아르카나 업데이트^reset;',
'126094':'^orange;아르카나 v1.4.2, 밤요정의 만가^#ffffff;',
'126095':'^orange;아케인 스타 - 6등급^reset;',
'126100':'^orange;팔 미사일 발사기^reset;',
'126101':'^orange;팔 소총^reset;',
'126104':'^orange;포병 대포^reset;',
'126107':'^orange;어설트 EM 소총 | UGL 미지원.^reset;',
'126108':'^orange;어설트 EM 소총^reset;',
'126109':'^orange;어설트 기관총',
'126110':'^orange;어설트 소총.^reset;',
'126114':'^orange;아우라 재앙',
'126118':'^orange;자동 대포^reset;',
'126119':'^orange;자동 석궁^reset;',
'126121':'^orange;자동 볼트액션 소총^reset;',
'126128':'^orange;나무를 깨우며...^reset;',
'126129':'^orange;아유린의 보급품',
'126131':'^orange;반',
'126132':'^orange;기본 길튼 장비 제작.^reset;',
'126144':'^orange;볼트 발사기^reset;',
'126149':'^orange;용감한 기사와 당돌한 군마^reset;',
'126155':'^orange;나만의 함선 만들기^reset;',
'126156':'^orange;헛간 짓기',
'126157':'^orange;버즈^reset; ^orange;버즈^reset; 가이드',
'126166':'^orange;카빈 | UGL 장착 불가.^reset;',
'126173':'^orange;차차라의 은신 테크 I',
'126174':'^orange;차차라의 은신 테크 II',
'126185':'^orange;화학 무기^reset;',
'126189':'^orange;클래식',
'126190':'^orange;루인드 소탕',
'126193':'^orange;석탄^reset;',
'126197':'^orange;전투 산탄총^reset;',
'126198':'^orange;은닉 권총^reset;',
'126202':'^orange;별을 집어삼키며',
'126203':'^orange;별을 집어삼키며 II',
'126204':'^orange;별을 집어삼키며 III',
'126205':'^orange;별을 집어삼키며 IV',
'126219':'^orange;여기서 고급 메카 부품을 제작합니다!^reset;',
'126220':'^orange;연못 만들기',
'126222':'^orange;수정 연대기^reset;',
'126224':'^orange;목표를 향한 대시',
'126230':'^orange;지정 사수 소총^reset;',
'126232':'^orange;자세한 변경로그^#ffffff;',
'126233':'^orange;차원 터널 탐험',
'126236':'^orange;용기사',
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
with open('priority_0877.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
