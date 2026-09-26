#!/usr/bin/env python3
# Fix euphemized/mistranslated sexbound rows identified in QA review.
import csv, glob

FIX = {
'202': '촉수가 그녀의 은밀한 곳을 애무하자, 촉수가 입구를 밀고 들어와 그녀의 보지 안을 늘렸다.',
'345': '씨발 좋아, 가득 채워줘!',
'1105': '요구. 씨발, 내 정액 받아!',
'1133': '네 끈적한 정액을 내 안에 쏟아줘~!',
'2434': '오-오~! 느껴져~! 네 에이펙스 정액을 내 안에 싸줘~!',
'2634': '넌 내 사랑스러운 작은 여우 떡감이야!',
'10219': '« 씨발',
'23955': '뭐가아아 문젠데, 떡감? 플로란이 너한테 좀... 너무 많아아?',
'24475': '강한 떡감, 플로란 존중해에에.',
'24540': '꽤 강해에에, 떡감~ 수분하자! ^red;«',
'31874': '꽃이다..향이 낯익은데... 아! 그래! 금요일에 즐겼던 그 사랑스러운 플로란 보지랑 똑같은 향이다.',
'34263': '좀 밋밥하군. 좌석 한가운데에 딜도가 있으면 좋겠다. 하기에 최고의 의자는 아니야.',
'38088': '뜨거운 플로란 자지를 빠는 섹시한 인간 소녀.',
'43645': '아아 그래, 보지를 따뜻하게 데우는 모닥불이지.',
'49457': '흥분됨. 내 자지에 딱 맞는 크기야!',
'49683': '네가 가장 차가운 정액을 그녀의 자궁 깊숙이 쏟아붓자, 그녀의 지금 임신은 성공적으로 시간 속에 얼어붙었다. 영구히.',
'49684': '네가 가장 차가운 정액을 그녀의 자궁 깊숙이 쏟아붓으면서, 그게 아기에게 좋았을지 의문이 들기 시작한다.',
'49685': '네가 뜨겁게 김이 나는 정액을 그녀의 자궁에 쏟아부으면서, 모든 종족이 이걸 받아낼 수 있게 만들어진 건 아닐지도 모른다는 걸 깨닫는다.',
'49686': '네가 뜨겁게 김이 나는 정액을 그녀의 자궁에 쏟아부으며, 타오르는 욕정이 그녀의 임신 흔적을 모조리 지워버린다.',
'58053': '새까만 보지. 느낌이 이상해.',
'69783': '흥~ 나 갈 것 같아~... 네가 내 보지를 적시고 있어~!',
'83847': '여왕님의 보지가 너를 인도하기를.',
'85701': '내 보지가 촉수 점액을 갈망해! ^red;«^white;',
'102725': '그렇지.. 그냥 긴장 풀고 푸시아가 젖은 보지를 네 단단한 자지 위에 박게 놔둬.',
}

def dump_cell(t):
    return '"' + t.replace('"', '""') + '"' if ('\n' in t or '"' in t or '\t' in t or t != t.strip()) else t

changed = {}
for fn in glob.glob('translations/rest_*.tsv'):
    rows = []
    dirty = False
    with open(fn, encoding='utf-8-sig', newline='') as f:
        for r in csv.reader(f, delimiter='\t'):
            if r and r[0] in FIX:
                r[1] = FIX[r[0]]
                changed[r[0]] = fn
                dirty = True
            rows.append(r)
    if dirty:
        with open(fn, 'w', encoding='utf-8-sig', newline='') as f:
            for r in rows:
                f.write('\t'.join(dump_cell(c) for c in r) + '\n')
print(len(changed), 'fixed')
missing = set(FIX) - set(changed)
print('missing:', missing)
