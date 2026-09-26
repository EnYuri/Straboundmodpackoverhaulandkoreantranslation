#!/usr/bin/env python3
# gen_0838: non-description low-priority rows
import json, csv, re

T = {
'102201':'터미널 빔캐논',
'102202':'터미널 글로브',
'102203':'터미널 그래플러',
'102204':'터미널 해머',
'102205':'터미널 권총',
'102206':'터미널 시저블레이드',
'102207':'터미널 포탄',
'102208':'터미널 창',
'102209':'터미널 지팡이',
'102217':'터미너스 관문',
'102218':'터미너스 작약: 치명타 확률 +10%, 초당 체력 20 회복',
'102219':'터미너스 작약: 발동 대기 중 - 치명타 확률 +10%, 초당 체력 20 회복',
'102223':'테라 노바',
'102230':'테라포밍 테스트 기록',
'102239':'테라리아 동물학자',
'102260':'테슬라 폭발',
'102263':'테슬라 수류탄',
'102266':'테슬라의 분노',
'102273':'테스트 결과',
'102275':'테스트 템플릿',
'102279':'새로운 수송 방식을 테스트하세요.',
'102280':'테스트 공격',
'102284':'도전을 완수해 힘을 시험하세요! 아래에 무작위로 생성된 세 가지 과제가 나타나며, 각각 난이도가 증가합니다.\n완료하면 \'수락\' 버튼을 눌러 보상을 받으세요.\n^red;보상 총액은 무작위이며, 하나 또는 두 개의 아이템만 선택됩니다.^reset;',
'102285':'TestTestTestTestTestTestTestTestTestTestTestTestTest\nTestTestTestTestTestTestTestTestTest\nTestTestTestTestTestTest\nTest\nTest\nTest\nTest\nTest\nTestTestTestTestTestTest',
'102297':'탈라소 요리대',
'102299':'탈라소 상점',
'102301':'탈라소 테마 가구!',
'102457':'감사합니다, 고객님!',
'102837':'당신에게 걸맞은 <role>',
'102853':'아이온',
'102856':'사후 세계',
'102858':'아가란',
'102903':'고대 문서',
'102915':'스타바운드의 천사들',
'102919':'분노한 <role>',
'102924':'에이펙스',
'102937':'유물 안정기',
'102939':'승천',
'102943':'아발리 업데이트 대참사',
'102988':'결계',
'103002':'일곱 발가락의 짐승',
'103006':'황폐한 동굴',
'103008':'푸른 검',
'103010':'시그리의 서',
'103018':'브라이트스틸 방주',
'103068':'시계탑들',
'103083':'천사 날개의 색',
'103097':'제작하는 것',
'103103':'십자군 <role>',
'103109':'별의 광신도들',
'103126':'천사들의 죽음',
'103128':'심연',
'103130':'델파 둥지',
'103132':'델파 감염',
'103151':'블러드문의 끝',
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
with open('priority_0838.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
