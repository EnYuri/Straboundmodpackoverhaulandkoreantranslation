#!/usr/bin/env python3
# gen_0863: non-description low-priority rows
import json, csv, re

T = {
'124822':'^green;+ 3.2% 에너지 재생^reset;',
'124823':'^green;+ 3.2% 광-에너지 재생^reset;',
'124824':'^green;+ 30 최대 에너지^reset;',
'124825':'^green;+ 30% 방어^reset;',
'124826':'^green;+ 30% 전기 저항.^reset;',
'124827':'^green;+ 30% 전기 저항.^reset;\n^green;+ 감전 면역^reset;',
'124828':'^green;+ 30% 에너지 재생^reset;\n^green;- 15% 에너지 재생\n  정지^reset;',
'124829':'^green;+ 30% 화염 저항.^reset;',
'124830':'^green;+ 30% 화염 저항.^reset;\n^green;+ 연소 면역^reset;',
'124831':'^green;+ 30% 체력^reset;',
'124832':'^green;+ 30% 얼음 저항.^reset;',
'124833':'^green;+ 30% 얼음 저항.^reset;\n^green;+ 얼음 미끄러짐 면역^reset;',
'124834':'^green;+ 30% 물리 저항.^reset;',
'124835':'^green;+ 30% 물리 저항.^reset;\n^green;+ 30% 넉백 저항.^reset;',
'124836':'^green;+ 30% 독 저항.^reset;',
'124837':'^green;+ 30% 독 저항.^reset;\n^green;+ 독 면역^reset;',
'124838':'^green;+ 30% 방사능 저항.^reset;',
'124839':'^green;+ 30% 방사능 저항.^reset;\n^green;+ 방사능 화상 면역^reset;',
'124840':'^green;+ 30% 그림자 저항.^reset;',
'124841':'^green;+ 30% 그림자 저항.^reset;\n^green;+ 그림자 오염\n  면역^reset;',
'124842':'^green;+ 315 체력^reset;',
'124843':'^green;+ 35 체력^reset;',
'124844':'^green;+ 35% 체력^reset;',
'124845':'^green;+ 35% 점프 높이^reset;',
'124846':'^green;+ 35% 최대 에너지^reset;',
'124847':'^green;+ 35% 달리기 속도^reset;',
'124848':'^green;+ 360 체력^reset;',
'124849':'^green;+ 37.5% 에너지 재생^reset;\n^green;- 18.75% 에너지 재생\n  정지^reset;',
'124850':'^green;+ 4 방어^reset;',
'124851':'^green;+ 4.8% 에너지 재생^reset;',
'124852':'^green;+ 4.8% 광-에너지 재생^reset;',
'124853':'^green;+ 40 최대 에너지^reset;',
'124854':'^green;+ 40% 우주 저항.^reset;',
'124855':'^green;+ 40% 전기 저항.^reset;',
'124856':'^green;+ 40% 화염 저항.^reset;',
'124857':'^green;+ 40% 화염 저항.^reset;\n^green;+ 연소 면역^reset;',
'124858':'^green;+ 40% 체력^reset;',
'124859':'^green;+ 40% 얼음 저항.^reset;',
'124860':'^green;+ 40% 최대 에너지^reset;',
'124861':'^green;+ 40% 최대 체력^reset;',
'124862':'^green;+ 40% 정신 보호.^reset;',
'124863':'^green;+ 40% 독 저항.^reset;',
'124864':'^green;+ 40% 방사능 저항.^reset;',
'124865':'^green;+ 40% 그림자 저항.^reset;',
'124866':'^green;+ 42% 방어 테크\n  효율^reset;',
'124867':'^green;+ 45% 체력^reset;',
'124868':'^green;+ 5 최대 에너지^reset;',
'124869':'^green;+ 5 연구 보너스^reset;',
'124870':'^green;+ 5% 에너지 재생^reset;\n^green;- 2.5% 에너지 재생\n  정지^reset;',
'124871':'^green;+ 5% 광-에너지 재생^reset;',
'124872':'^green;+ 5% 최대 에너지^reset;',
'124873':'^green;+ 5% 최대 체력^reset;',
'124874':'^green;+ 50 체력^reset;',
'124875':'^green;+ 50% 체력^reset;',
'124876':'^green;+ 50% 최대 에너지^reset;',
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
with open('priority_0863.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
