#!/usr/bin/env python3
# gen_0861: non-description low-priority rows
import json, csv, re

T = {
'124465':'^cyan;유물 재건기^reset;',
'124472':'^cyan;상생 협력^reset;',
'124665':'^gray;위장',
'124666':'^gray;직업',
'124667':'^gray;방향감각 상실',
'124674':'^gray;그리무아 - 원소 혼합',
'124679':'^gray;입력',
'124681':'^gray;기계공',
'124689':'^gray;출력',
'124690':'^gray;패시브:^reset;',
'124691':'^gray;파일럿',
'124693':'^gray;주요:^reset;',
'124694':'^gray;아래 슬롯에 아이템을 넣어 블랙리스트에 추가하세요!\n^red;경고:^reset; 블랙리스트 아이템은 인벤토리에서 자동으로 ^red;삭제^gray;됩니다.^reset;',
'124695':'^gray;파괴공작원',
'124696':'^gray;그늘',
'124702':'^gray;특수:^reset;',
'124707':'^gray;덫사냥꾼',
'124709':'^gray;승급',
'124730':'^green;+ %15 점프 높이^reset;',
'124731':'^green;+ 0.8% 에너지 재생^reset;',
'124732':'^green;+ 1 연구 보너스^reset;',
'124733':'^green;+ 1.6% 에너지 재생^reset;',
'124734':'^green;+ 1.6% 광-에너지 재생^reset;',
'124735':'^green;+ 1/4 낙하 피해^reset;',
'124736':'^green;+ 10 방어^reset;',
'124737':'^green;+ 10 체력^reset;',
'124738':'^green;+ 10 최대 에너지^reset;',
'124739':'^green;+ 10% 치명타 확률^reset;',
'124740':'^green;+ 10% 방어^reset;',
'124741':'^green;+ 10% 전기 저항.^reset;',
'124742':'^green;+ 10% 전기 저항.^reset;\n^green;+ 감전 면역^reset;',
'124743':'^green;+ 10% 에너지 재생^reset;\n^green;- 5% 에너지 재생\n  정지^reset;',
'124744':'^green;+ 10% 화염 저항.^reset;',
'124745':'^green;+ 10% 화염 저항.^reset;\n^green;+ 연소 면역^reset;',
'124746':'^green;+ 10% 체력^reset;',
'124747':'^green;+ 10% 얼음 저항.^reset;',
'124748':'^green;+ 10% 얼음 저항.^reset;\n^green;+ 얼음 미끄러짐 면역^reset;',
'124749':'^green;+ 10% 최대 에너지^reset;',
'124750':'^green;+ 10% 최대 체력^reset;',
'124751':'^green;+ 10% 물리 저항.^reset;',
'124752':'^green;+ 10% 물리 저항.^reset;\n^green;+ 10% 넉백 저항.^reset;',
'124753':'^green;+ 10% 독 저항.^reset;',
'124754':'^green;+ 10% 방사능 저항.^reset;',
'124755':'^green;+ 10% 방사능 저항.^reset;\n^green;+ 방사능 화상 면역^reset;',
'124756':'^green;+ 10% 달리기 속도^reset;',
'124757':'^green;+ 10% 그림자 저항.^reset;',
'124758':'^green;+ 10% 그림자 저항.^reset;\n^green;+ 그림자 오염\n  면역^reset;',
'124759':'^green;+ 100% 모든 저항.^reset;',
'124760':'^green;+ 100% 체력^reset;',
'124761':'^green;+ 100% 흡혈^reset;',
'124762':'^green;+ 11.2% 에너지 재생^reset;',
'124763':'^green;+ 11.2% 광-에너지 재생^reset;',
'124764':'^green;+ 12% 체력^reset;',
'124765':'^green;+ 12% 카타나 숙련^reset;\n^green;+ 산소 공급^reset;\n^green;+ 8% 우주 저항.^reset;\n^green;+ 8% 그림자 저항.^reset;',
'124766':'^green;+ 12.5% 에너지 재생^reset;\n^green;- 6.25% 에너지 재생\n  정지^reset;',
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
with open('priority_0861.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
