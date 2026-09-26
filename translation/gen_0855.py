#!/usr/bin/env python3
# gen_0855: non-description low-priority rows
import json, csv, re

T = {
'123054':'^#EEA92A;안개 이슬: 국내 전선^reset;',
'123059':'^#F0523C;[HUMAN-1] 예상 못한 브리핑',
'123060':'^#F0523C;[HUMAN-2] 텐구 요새 강습',
'123061':'^#F0523C;[HUMAN-3A] 하얀 늑대들의 운명',
'123062':'^#F0523C;[HUMAN-3] 하얀 늑대들',
'123063':'^#F0523C;[HUMAN-4] 천상의 말',
'123064':'^#F0523C;[HUMAN-5] 타오르는 열정',
'123065':'^#F0523C;[HUMAN-6A] 무녀',
'123066':'^#F0523C;[HUMAN-6] 짧은 휴식',
'123067':'^#F0523C;[HUMAN-INTRO] 최후의 결정',
'123068':'^#F0523C;[TRIAL-1] 무너지는 왕국',
'123069':'^#F0523C;[YOKAI-1] 마법과 철',
'123070':'^#F0523C;[YOKAI-2A] 최후의 준비',
'123071':'^#F0523C;[YOKAI-2] 연방 강습',
'123072':'^#F0523C;[YOKAI-INTRO] 최후의 결정',
'123098':'^#FF2020;레드',
'123105':'^#FF9000;총기 상점',
'123106':'^#FF9000;상품',
'123108':'^#FF9000;프로젝트 45 매뉴얼',
'123111':'^#FFAAAA;페이',
'123112':'^#FFAAAA;쿠노이치',
'123114':'^#FFAD12;고급 진정제^white;',
'123115':'^#FFAD12;향정신성 물질^white;',
'123118':'^#FFBC47;글리치의 군주^reset; - I',
'123119':'^#FFBC47;글리치의 군주^reset; - II',
'123120':'^#FFBC47;글리치의 군주^reset; - III',
'123121':'^#FFD83F;에피모픽 골격^reset; - ^green;[EWS] 중형 갑옷 이동 페널티 무효 | 최대 체력 +30%^reset; | ^red;이동 속도 -15%',
'123122':'^#FFD83F;고릴라 팔^reset; - 이제 \'중화기\'를 다룰 수 있습니다.',
'123123':'^#FFD83F;너머의 지식^reset; - 테크 무기를 완벽하게 다룰 수 있습니다. ^orange;정지 시 [EWS]적중 확률 20% 증가^reset;',
'123124':'^#FFD83F;미래의 지식^reset; - 이 까다로운 무기를 완벽하게 다룰 수 있습니다.',
'123125':'^#FFD83F;나노 재생 골격^reset; - ^green;대부분의 상해 면역 | 최대 체력 +10%^reset; | ^red;이동 속도 -5%',
'123126':'^#FFD83F;프로토타입 SLS^reset; - SLS 활성화. ^orange;이동 시 [EWS]명중률 20% 증가 | 정지 시 10%^reset;',
'123127':'^#FFD83F;프로토타입 골격^reset; - ^green;[EWS] 사이버웨어 페널티 감소 | 최대 체력 +15%^reset;',
'123128':'^#FFD83F;강화 티타늄 골격^reset; - ^green;[EWS] 갑옷 이동 페널티 무효 | 최대 체력 +15%^reset; | ^red;이동 속도 -10%',
'123129':'^#FFD83F;스마트 링크 시스템^reset; - 시스템 활성화. 자기유도 마이크로 발사체로 표적을 추적.',
'123130':'^#FFD83F;무허가 외골격^reset; - 이제 \'중화기\'를 다룰 수 있습니다. ^green;[EWS] 무기 이동 페널티 무효.',
'123135':'^#FFDD00;장거리 수류탄 투척 시스템',
'123141':'^#FFEEC6;건액스 | 타격 6x | 찌르기 0x | 베기 8x^white;',
'123142':'^#FFEEC6;건블레이드 | 타격 1x | 찌르기 3x | 베기 4x^white;',
'123143':'^#FFEEC6;건블레이드 | 타격 1x | 찌르기 4x | 베기 4x^white;',
'123144':'^#FFEEC6;중형 검 | 타격 2x | 찌르기 0x | 베기 5x^white;',
'123145':'^#FFEEC6;중형 둔기 | 타격 5x | 찌르기 0x | 베기 0x^white;',
'123146':'^#FFEEC6;경량 둔기 | 타격 3x | 찌르기 0x | 베기 0x | 전기 4x^white;',
'123147':'^#FFEEC6;마법검 | 열 1-7x^white;',
'123148':'^#FFEEC6;마법검 | 타격 3x | 찌르기 5x | 베기 5x^white;',
'123149':'^#FFEEC6;레이피어 | 타격 0x | 찌르기 8x | 베기 3x | 출혈 4x^white;',
'123150':'^#FFEEC6;다용도 검 | 타격 0x | 찌르기 5x | 베기 6x | 출혈 2x^white;',
'123151':'^#FFEEC6;다용도 검 | 타격 0x | 찌르기 4x | 베기 6x^white;',
'123152':'^#FFFF40;옐로우',
'123155':'^#FFFFFF;화이트',
'123160':'^#a43dc1;T8^reset;',
'123167':'^#a8fff9;크로노 포^reset;',
'123168':'^#a8fff9;크로노 캐논^reset;',
'123184':'^#b0e0fc;알타 ^#f6f6f6;보안 통신^reset;',
'123185':'^#b0e0fc;알타 ^#f6f6f6;함선 A.I.^reset;',
}

TAG = re.compile(r'\^[a-zA-Z]+;|\^#[0-9a-fA-F]+;|\[[A-Z0-9\- ]+\]')
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
with open('priority_0855.json', 'w', encoding='utf-8') as f:
    json.dump(T, f, ensure_ascii=False, indent=0)
