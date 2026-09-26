#!/usr/bin/env python3
# gen_0865: non-description low-priority rows
import json, csv, re

T = {
'124932':'^green;+ 불량품^reset;',
'124933':'^green;+ 결연함^reset;',
'124934':'^green;+ 이중 헤드램프^reset;',
'124935':'^green;+ 감전^reset;',
'124936':'^green;+ 전기봉쇄^reset;',
'124937':'^green;+ 응급 치유^reset;',
'124938':'^green;+ 응급 치유사^reset;',
'124939':'^green;+ 활력제^reset;',
'124940':'^green;+ 에너지 발전기^reset;',
'124941':'^green;+ 에너지 보호막^reset;',
'124942':'^green;+ 에너지 지원 시스템^reset;',
'124943':'^green;+ 에너지 상승 III^reset;',
'124944':'^green;+ 에너지 상승 II^reset;',
'124945':'^green;+ 에너지 상승 IV^reset;',
'124946':'^green;+ 에너지 상승 I^reset;',
'124947':'^green;+ 환경 보호^reset;',
'124948':'^green;+ 얼치어스 유령\n  면역^reset;',
'124949':'^green;+ 낙하 피해\n  면역^reset;',
'124950':'^green;+ 화염 가시^reset;',
'124951':'^green;+ 역장 자동보호병^reset;',
'124952':'^green;+ 역장 보호막^reset;',
'124953':'^green;+ 가스 가시^reset;',
'124954':'^green;+ 중력 비\n  면역^reset;',
'124955':'^green;+ 행복함^reset;',
'124956':'^green;+ 어둠 속 치유^reset;',
'124957':'^green;+ 빛 속 치유^reset;',
'124958':'^green;+ 헬륨-3 면역^reset;',
'124959':'^green;+ 헬륨-3 면역^reset;\n^green;+ 어두운 가스\n  면역^reset;\n^green;+ 기체 금속\n  수소 면역^reset;\n^green;+ 독가스 면역^reset;',
'124960':'^green;+ 헤비카이 블록^reset;',
'124961':'^green;+ 헤비카이 일격^reset;',
'124962':'^green;+ 헤비카이^reset;',
'124963':'^green;+ 꿀 면역^reset;',
'124964':'^green;+ 얼음 미끄러짐 면역^reset;',
'124965':'^green;+ 얼음 가시^reset;',
'124966':'^green;+ 사랑에 빠짐^reset;',
'124967':'^green;+ 광기 에너지 재생.^reset;',
'124968':'^green;+ 광기 면역^reset;',
'124969':'^green;+ 영감받음^reset;',
'124970':'^green;+ 즉시 에너지^reset;',
'124971':'^green;+ 즉시 체력\n+ 즉시 에너지^reset;',
'124972':'^green;+ 즉시 체력^reset;',
'124973':'^green;+ 의도^reset;',
'124974':'^green;+ 이온 구름^reset;',
'124975':'^green;+ 이온 마비^reset;',
'124976':'^green;+ 이온 충격^reset;',
'124977':'^green;+ 이온 일격^reset;',
'124978':'^green;+ 이온화된 공기^reset;',
'124979':'^green;+ 이온봉쇄^reset;',
'124980':'^green;+ 아이템 자석 III^reset;',
'124981':'^green;+ 아이템 자석 II^reset;',
'124982':'^green;+ 아이템 자석 I^reset;',
'124983':'^green;+ 용암 면역^reset;',
'124984':'^green;+ 부유^reset;',
'124985':'^green;+ 생명유지 모듈^reset;',
'124986':'^green;+ 생명유지 시스템^reset;',
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
with open('priority_0865.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
