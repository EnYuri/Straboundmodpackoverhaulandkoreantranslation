# -*- coding: utf-8 -*-
# Translate remaining uncovered English fields (trans+ paks etc.) into zz patch ops.
import sys, io, os, csv, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, 'tools')
import pak_writer
from pak import Pak

ZZ = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

KO = {
0: '"무기를 들고 다가올 폭풍에 대비하라. 불속에서 벼려지고 덕으로 연마되어, 수호자가 되라."',
1: '^#ff00ff;이몰레이터 갑판^reset; ^#FFB2B2;^reset;',
2: '"혼란이 다시 우주를 뒤덮었다. 그대의 주시하는 눈으로 약자를 지키고 정의를 가져올 수 있으리라."',
3: '^#ff00ff;이몰레이터 두구^reset; ^#FFB2B2;^reset;',
4: '"열정의 불길에서 재단련된 이 장화는 아무리 먼 길을 가도 닳지 않으리라."',
5: '^#ff00ff;이몰레이터 바지^reset; ^#FFB2B2;^reset;',
6: '살짝 금이 갔고 보이드의 것이었던 스카우터. 제법 많은 혹사를 견뎌낸 듯하다.',
7: '^Cyan;인내의 의지^White; ^#FFB2B2;^reset;',
8: '최악의 전투에서도 이 코트는 찢어지거나 걸리지 않는다. 이 천은 사용자에게 닥치는 대부분의 해를 막아준다.',
9: '^Cyan;생존의 의지^White; ^#FFB2B2;^reset;',
10: '바지 한 벌. 외부 요인에 노출되고 총알을 맞아도 여전히 새것처럼 보인다.',
11: '^Cyan;전진의 의지^White; ^#FFB2B2;^reset;',
12: '폭스 몰리의 마녀 셔츠. 힘이 가득 담겼지만 지나치게 거센 공격은 견디지 못한다.',
13: '몰리의 마녀 셔츠 ^yellow;^reset;',
14: '몰리가 오랜 세월 써온 두구.\n^green;야간투시^reset;',
15: '몰리의 두구',
16: '폭스 몰리의 마녀 치마. 영적인 힘이 소용돌이치고 있다.\n^blue;환경 저항 ^red;단 산소^reset;',
17: '몰리의 마녀 치마 ^yellow;^reset;',
18: '폭스 몰리의 마녀 셔츠. 부드럽고 편안한 느낌이다.\n^green;테라포지에서 마법 부여 가능.^reset;',
19: '몰리의 마녀 셔츠',
20: '몰리가 오랜 세월 써온 두구.\n^green;야간투시, HP+10^reset;',
21: '몰리의 두구',
22: '폭스 몰리의 마녀 치마. 부드럽고 편안한 느낌이다.\n^green;테라포지에서 마법 부여 가능.^reset;',
23: '몰리의 마녀 치마',
24: '폭스 몰리의 마녀 셔츠. 힘이 가득 담겼다.\n^green;키츠네비 부유 포대 발동^reset;',
25: '몰리의 마녀 셔츠 ^yellow;^reset;',
26: '영적인 힘이 소용돌이치고 있다.\n^green;재생\n^blue;환경 저항 ^red;단 산소^reset;',
27: '몰리의 마녀 치마 ^yellow;^reset;',
28: '몰리가 20세기 초에 쓰던 두구.\n^green;야간투시^reset;',
29: '몰리의 두구 (오리지널)',
30: '폭스 몰리의 사복. 부드럽고 편안한 느낌이다.',
31: '몰리의 사복 셔츠',
32: '폭스 몰리의 사복. 부드럽고 편안한 느낌이다.',
33: '몰리의 사복 치마',
34: '표준 피스키퍼 제복 위의 케블라 조끼. 화려하진 않지만 제 몫을 한다. 이제 더 큰 위험에 대처하도록 개선됐다. ^green;물리 저항 부여.^reset;',
35: '대응요원 조끼 ^yellow;^reset;',
36: '섬유에 티타늄을 짜 넣어 보호를 제공하는 모자. 이제 더 큰 위험에 대처하도록 개선됐다. ^green;물리 저항 부여.^reset;',
37: '대응요원 모자 ^yellow;^reset;',
38: '바지와 장화 한 벌. 섬유에 티타늄을 짜 넣어 더 나은 보호를 제공한다. 이제 더 큰 위험에 대처하도록 개선됐다. ^green;물리 저항 부여.^reset;',
39: '대응요원 바지 ^yellow;^reset;',
40: '검이든 총알이든 막아주는 보호용 티타늄 섬유가 들어간 롱코트. 이제 더 큰 위험에 대처하도록 개선됐다. ^green;물리 저항 부여.^reset;',
41: '제압요원 재킷 ^yellow;^reset;',
42: '어느 정도 머리를 보호하는 티타늄 섬유가 들어간 모자. 이제 더 큰 위험에 대처하도록 개선됐다. ^green;물리 저항 부여.^reset;',
43: '제압요원 모자 ^yellow;^reset;',
44: '좋은 구두가 딸린 바지. 보호에 도움되는 좋은 티타늄 직조가 들어 있다. 이제 더 큰 위험에 대처하도록 개선됐다. ^green;물리 저항 부여.^reset;',
45: '제압요원 바지 ^yellow;^reset;',
46: '언바운드가 정말 스타포지를 쓸 수 있었던 거군... 그들이 그렇게 빨리 성장한 이유가 설명되는데.',
}

rows = list(csv.reader(open('data/uncov_todo.tsv', encoding='utf-8'), delimiter='\t'))[1:]
assert len(rows) == len(KO), (len(rows), len(KO))

# group ops per asset
per_asset = {}
for i, (prov, asset, field, en) in enumerate(rows):
    per_asset.setdefault(asset, []).append(
        [{'op': 'test', 'path': field, 'value': en},
         {'op': 'replace', 'path': field, 'value': KO[i]}])

pk = Pak(ZZ)
overrides = {}
for asset, ops in per_asset.items():
    pp = asset + '.patch'
    try:
        existing = json.loads(pk.read(pp).decode('utf-8'))
    except Exception:
        existing = []
    if not isinstance(existing, list):
        existing = [existing]
    existing.append(ops)
    overrides[pp] = json.dumps(existing, ensure_ascii=False).encode('utf-8')
del pk

out = ZZ + '.staged'
n = pak_writer.write_pak(out, ZZ, overrides)
print('wrote', n, 'files,', len(overrides), 'patch files')
time.sleep(1)
try:
    os.replace(out, ZZ)
    print('replaced')
except PermissionError:
    print('staged kept:', out)
