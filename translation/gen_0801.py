#!/usr/bin/env python3
# gen_0801: non-description low-priority rows
import json, csv, re

T = {
'82273':'로드스타 신전',
'82274':'로드스톤 스탠드',
'82276':'높은 초록',
'82277':'높은 빨강',
'82278':'높은 돌 난로',
'82279':'높은 청록',
'82280':'기록 3489.#0006',
'82281':'기록 3489.#0011',
'82282':'기록 3489.#0034',
'82283':'기록 3489.#0049',
'82284':'기록 3489.#0071',
'82285':'기록 3489.#0079',
'82286':'기록 3489.#0103',
'82287':'기록 3489.#0103; 개인',
'82288':'기록 3489.#0107; 개인',
'82289':'기록 3489.#0114',
'82290':'기록 3489.#0121',
'82291':'기록 3489.#0121; 개인',
'82292':'기록 3489.#0128',
'82293':'기록 3489.#0128; 개인',
'82294':'기록 3497.#0312; 개인',
'82295':'기록 3497.#0319; 개인',
'82296':'기록 3498.#0327; 개인',
'82297':'일지 1',
'82298':'일지 2',
'82299':'일지 3',
'82300':'일지 4',
'82303':'ㅋㅋ 글쎄',
'82306':'롬박스 (뾰족)',
'82307':'롬박스 (줄무늬)',
'82382':'두 번째 구조대 대장을 찾으세요.\n^yellow;위협 등급: 6',
'82428':'튼실하고 큰 수컷을 찾으시나요?',
'82683':'엄습하는 어둠 - 가시성과 광원 효율 감소',
'82684':'제멋대로 하늘조종사 <role>',
'82687':'전리품폭발!',
'82690':'우주의 군주들',
'82694':'<field> 외교의 기록지기',
'82695':'Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry\'s standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.',
'82697':'신성함의 상실',
'82698':'분실물 상인',
'82700':'잃어버린 축복',
'82701':'잃어버린 개척자',
'82702':'잃어버린 현실 유물',
'82703':'잃어버린 공간 유물',
'82705':'잃어버린 시간 유물',
'82742':'사랑스러운 티타임',
'82744':'러블리 채찍 안내서 요약',
'82745':'EB의 러블리 채찍 안내서',
'82753':'사랑하는 <role>',
'82754':'저중력',
'82755':'저중력 - 주변 중력이 상당히 약합니다.',
'82756':'저중력 지대 - 주변 중력이 극도로 약합니다.',
'82757':'저품질 폼폼 스타일링 <field> 협상',
'82758':'저출력 모드 | 보조 발사를 눌러 사격 모드 전환 가능.',
'82766':'Lua 스크립팅',
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
    if re.findall(r'<[^>]+>', s) != re.findall(r'<[^>]+>', ko):
        bad.append(('PH', i))
print('bad:', bad)
print(len(T))
with open('priority_0801.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
