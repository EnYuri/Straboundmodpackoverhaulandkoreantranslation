#!/usr/bin/env python3
# gen_0882: non-description low-priority rows
import json, csv, re

T = {
'126926':'^red;- 이동 속도 35%^reset;\n^red;- 점프 높이 35%^reset;',
'126927':'^red;- 방어 40%^reset;',
'126928':'^red;- 방어 5^reset;\n^red;- 모든 저항 5%^reset;',
'126929':'^red;- 최대 체력 5%^reset;',
'126930':'^red;- 방어 50^reset;\n^red;- 모든 저항 50%^reset;',
'126931':'^red;- 방어 50%^reset;',
'126932':'^red;- 이동 속도 50%^reset;\n^red;- 점프 높이 30%^reset;',
'126933':'^red;- 둔화 70%^reset;',
'126934':'^red;- 화상^reset;',
'126935':'^red;- 감전^reset;',
'126936':'^red;- 동상^reset;',
'126937':'^red;- 심한 중독^reset;\n^red;- 이동 속도 35%^reset;\n^red;- 점프 높이 35%^reset;\n^red;- 최대 체력 20^reset;',
'126938':'^red;- 중독^reset;',
'126939':'^red;- 용해^reset;',
'126940':'^red;- 시간 루프^reset;',
'126950':'^red;10',
'126952':'^red;15',
'126955':'^red;5',
'126962':'^red;납치됨! - 완전히 움직이지 못하고 공격할 수 없다. 원소 상태이상에 걸리지 않는다.',
'126964':'^red;숙련자',
'126980':'^red;타격풍 - 기동성이 적당히 감소한다.',
'126981':'^red;전투 마법사',
'126983':'^red;광전사',
'126984':'^red;출혈',
'126986':'^red;실혈 - 지속 피해. 모든 재생이 차단된다.',
'126988':'^red;화상 - 적당한 지속 피해. 액체 안에서는 꺼지지만 타르 묻은 상태면 더 강해진다.',
'126989':'^red;타는 기름 - 빠른 지속 피해. 받는 냉기 피해가 크게 증가한다.',
'126993':'^red;촉매화 - 걸렸을 때 원소 상태이상을 강화할 수 있다.',
'126994':'^red;체인질링',
'127000':'^red;타락의 심연 - 적당한 지속 피해, 최대 에너지와 기동성 감소.',
'127002':'^red;치명타^reset;',
'127003':'^red;사이버-사이코^reset; - 가끔은 그냥 사이코가 된 기분을 느끼고 싶을 때가 있다, ^green;+근접 피해 30% | +이동 속도 20% | 억제 무시',
'127004':'^red;사이버사이코시스^reset; - 해리장애, 사이버네틱 증강 과부하로 발생. ^orange;공격성 증가 | 억제 무시 | 천천히 죽어가는 몸',
'127013':'^red;치명적 냉기 - 에너지 감소, 고갈 시 체력 감소. 기동성 감소. | 완화 시: 체력 감소가 겹치고 에너지 감소 없음.',
'127014':'^red;치명적 열기 - 느린 지속 피해. 에너지 재생 50% 감소. | 완화 시: 체력 감소가 겹침.',
'127015':'^red;치명적 방사선 - 최대 체력 75% 감소. | 완화 시: 최대 체력이 50%까지 증가.',
'127016':'^red;치명적 정전기 - 최대 에너지 -50%, 에너지 재생 없음, 에너지 없으면 지속 피해. | 완화 시: 에너지 재생이 10%로 증가.',
'127017':'^red;치명적 독성 - 느린 지속 피해, 최대 체력을 서서히 감소. | 완화 시: 최대 체력 감소 없음.',
'127018':'^red;명사수',
'127026':'^red;비활성화된 사이버웨어',
'127034':'^red;파멸 - 일정량의 피해를 받으면 폭발한다.',
'127037':'^red;감전 - 테슬라 볼트가 근처 아군으로 튄다. 젖은 상태면 더 강해진다.',
'127038':'^red;엔트로피 공허 - 방어, 공격, 기동성 감소. 모든 재생이 차단된다.',
'127048':'^red;FFS ^green;EP.0 - 메인 ^White;버려진 광산',
'127049':'^red;FFS ^green;EP.0 - 메인 ^White;S.O.S 찾기',
'127050':'^red;FFS ^green;EP.0 - 메인 ^White;생존자 찾기: 나데즈다',
'127051':'^red;FFS ^green;EP.0 - 메인 ^White;생존자 찾기: 파파치노',
'127052':'^red;FFS ^green;EP.0 - 메인 ^White;생존자 찾기: 사라',
'127053':'^red;FFS ^green;EP.0 - 메인 ^White;생존자 찾기: 월리스',
'127054':'^red;FFS ^green;EP.0 - 메인 ^White;대탈출',
'127055':'^red;FFS ^green;EP.0 - 메인 ^White;최후의 전투',
'127056':'^red;FFS ^green;EP.0 - 메인 ^White;시작!',
'127057':'^red;FFS ^green;EP.0 - 서브 ^White;병기고',
'127058':'^red;FFS ^green;EP.1 - 메인 ^White;브레드넛의 속죄 - 3',
'127059':'^red;FFS ^green;EP.1 - 메인 ^White;증거',
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
with open('priority_0882.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
