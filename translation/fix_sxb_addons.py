# -*- coding: utf-8 -*-
# Sexbound addon review fixes: knot verbs, whip names, brothel terms, misc euphemism
import csv, glob

FIX = {
    # knot as reproductive verb -> 매듭지다 (was 묶다 = plain tying)
    '43':   '좋아! 매듭지어줘! 날 묶고 채워줘!',
    '144':  '응, 매듭지어줘! 날 묶고 채워줘!',
    '483':  '네가 개 자지를 가져서 다행이야. 네가 날 매듭지어주길 못 기다려!',
    '2391': '매듭지어줘! 임신시켜줘! 새끼 한가득!',
    '2567': '윽! 좋아! 네가 큰 개인 것처럼 날 매듭지어줘!',
    # whip names -> canonical set from in-game guide (125667/125670)
    '18946': ('사랑스러운 채찍:^blue;eblovelywhip^reset;\n'
              '색욕의 채찍:^blue;eblustfulwhip^reset;\n'
              '풍요의 채찍:^blue;ebfertilewhip^reset;\n'
              '후회의 채찍:^blue;ebremorsefulwhip^reset;\n'
              '모험의 채찍:^blue;ebventurouswhip^reset;\n'
              '향수의 채찍:^blue;ebnostalgicwhip^reset;\n\n'
              '^green;채팅창을 열고 ^reset;/admin^green;을 입력한 뒤 엔터를 누르면 치트를 쓸 수 있습니다. 그다음 ^reset;/spawnitem^green;을 입력하고 한 칸 띄운 뒤 ^blue;아이템 이름^green;을 적으면 ^orange;모든 채찍을 포함해^green; 게임 속 어떤 아이템이든 소환할 수 있습니다.'),
    '82743': '사랑스러운 채찍',
    '82744': '사랑스러운 채찍 안내서 요약',
    '82745': 'EB의 사랑스러운 채찍 안내서',
    '82883': '색욕의 채찍',
    '63065': '풍요의 채찍',
    '87240': '향수의 채찍',
    '38272': '충격적인 사실이 밝혀졌다. 수천 년 전, 누군가가 박물관에서 채찍을 훔쳐 갔고, 마지막으로 전해지는 소식에 따르면 그것이 지금 이 우주를 떠돌고 있다고 한다! ^orange;후회의 채찍이 은하 어딘가에 풀려나 있다!^reset;\n\n전설에 따르면 ^orange;후회의 채찍^reset;은 ^orange;임신의 효과를 되돌리는^reset; 힘을 지녔다고 한다! 마치 처음부터 수정이 되지 않았던 것처럼! 어쩌면 누군가 그 본래의 힘을 되찾아 놓았을지도 모른다...',
    '88804': '오, 이게 뭐지? ^orange;SxB 설정에 따라 ^green;모험의 채찍^orange;이 유용할 수도, 아닐 수도 있어.^reset; 흠, 그게 무슨 뜻이든 간에.\n\n^green;이건 플레이어가 자기 Sexbound 모드 폴더에 들어가서 Sexbound.config 파일을 찾아, 메모장++ 같은 프로그램으로 열고 ^blue;futanari^green; 설정을 찾아야 한다는 뜻이다. 거기서 ^blue;enable^green; 설정을 ^blue;false^green;에서 ^blue;true^reset;로 바꿔야 한다.\n\n오, 고마워.',
    '117102': '또 하나 있어? 소문에 따르면 ^orange;채찍 두 개가 더 은하계로 밀반입됐대!^reset;\n\n오, 이번 건 ^orange;여자에게 남자 부위를 준대!^reset; 오, 맘에 들어. 이름은 ^green;모험의 채찍.^reset; 좋아.\n\n음... ^yellow;향수의 채찍 ^orange;은 여자를 원래 체형으로 되돌린대.^reset; 재미없어...',
    # brothel: 매음/매춘/매춘굴/매춘업소 -> 매음굴
    '24197': '목재 매음굴 침대',
    '30186': '머리판이 달린 포근한 나무 매음굴 침대.',
    '30187': '포근한 나무 매음굴 침대.',
    '31741': '매끄러운 비단 시트가 깔린 단단한 매음굴 침대입니다.',
    '40701': '무시 가죽 시트가 깔린 튼튼한 나무 매음굴 침대.',
    '47113': '매우 조악한 건초로 만든 매음굴 침대다.',
    '59109': '지저분한 매음굴 매트리스',
    '92231': '원시 매음굴 침대',
    # Lewdbound: 음란 bare-adjective grammar
    '16533': '음란한 헤미 총',
    '18792': '음란한 장난감 상인',
    '21681': '그-그건... 음란해!',
    # TTPP
    '185':  '촉수 임신',
    '210':  '촉수가 그녀의 학대받는 엉덩이 깊숙이 들어갈 때마다, 가슴이 리듬에 맞춰 흔들린다.',
    '216':  '그녀의 보지만 드러난 채 촉수에 무자비하게 꿰뚫려 배가 불룩해진다.',
    # fuchsia
    '1708': '푸시아는 멈출 수 없어... 푸시아는 너를 영원히 박고 싶어!',
    # felinholo hologram fuck
    '42563': '나뭇결 홀로그램 프로젝터- 잠깐, 이거랑 박을 수 있다고?!',
    '42564': '나뭇결 홀로그램 프로젝터- 잠깐, 이게 날 박을 수 있다고?!',
    # AphroditesBow
    '117486': '뭐야... 씨발?! 너 때문에... 임신할 것 같아.',
    '33441': "글자 F가 새겨진 쐐기돌입니다. 아마 '떡치기'를 뜻하는 것 같습니다.",
    # Neki consistency
    '28698': '커다랗고 발정 난 말이다냥!',
    '34284': '작고 발정 난 말이다냥!',
    '87448': '지금 보지 좀 하고 싶다고 했을 때 이런 걸 생각한 건 아니었는데.',
    '117561': '너 같은 쫄보가 이런 구멍에 뭘 하러 왔냥?',
    '28677': '커다란 떡 덩어리다냥.',
    '39342': '작은 떡잎 더미다.',
    '33104': '쉭쉭 노란 벽입에 야한 낙서가 그려져 있다냥.',
}

def dump_cell(t):
    return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip()) else t

n = 0; missing = set(FIX)
for fn in glob.glob('translations/rest_*.tsv'):
    rows = []; dirty = False
    with open(fn, encoding='utf-8-sig', newline='') as f:
        for r in csv.reader(f, delimiter='\t'):
            if r and r[0] in FIX:
                r[1] = FIX[r[0]]; n += 1; dirty = True; missing.discard(r[0])
            rows.append(r)
    if dirty:
        with open(fn, 'w', encoding='utf-8-sig', newline='') as f:
            for r in rows:
                f.write('\t'.join(dump_cell(c) for c in r) + '\n')
print(n, 'fixed')
print('missing:', missing)
