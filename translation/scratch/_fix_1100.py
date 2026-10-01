import io, sys
sys.stdout.reconfigure(encoding='utf-8')
lines = open('data/gic_ko_04.tsv', encoding='utf-8').read().splitlines()
# drop the broken 1100 row and all its continuation fragments (lines without idx\t prefix)
out = []
skipping = False
for l in lines:
    parts = l.split('\t', 1)
    if len(parts) == 2 and parts[0].isdigit():
        skipping = False
        if parts[0] == '1100':
            skipping = True   # drop broken row
            continue
        out.append(l)
    elif skipping:
        continue
# correct 1100 row with literal \n sequences
row1100 = "1100\t''아무리 기술이 진보해도 머리를 꿰뚫는 날카로운 투사체가 거의 모든 것을 죽인다는 사실은 바뀌지 않는다.''\\n^yellow;극한 속도^reset;로 가시 파편 한 개를 발사해 ^green;높은 위력^reset;으로 맞는 모든 표적에 ^red;심한 출혈^reset;을 일으킨다. 단순하지만 믿음직하다.\\n^yellow;탄약: 겐시듐 파편.^reset;\\n^green;우클릭을 눌러 파편 발사기 발사/재장전.^reset; | ^yellow;네 발을 보유한다.^reset;\\n^green;호환되는 GiC 무기를 우클릭해 장착.^reset;"
out.append(row1100)
open('data/gic_ko_04.tsv', 'w', encoding='utf-8', newline='\n').write('\n'.join(out) + '\n')
print('rows:', len(out))
