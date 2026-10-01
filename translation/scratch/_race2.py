import csv, sys, io, re
csv.field_size_limit(sys.maxsize)
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

POLITE = re.compile(r"(습니다|습니까|세요|십시오|해요|예요|이에요|예죠|이죠|군요|네요|랍니다|습니다요)(?=[.!?…\n, ]|$)")
RACE_RX = re.compile(r'/(\w+)[Dd]escription$')

per_race_end = {}
examples = {}
for row in csv.DictReader(open('data/pak_pairs.tsv', encoding='utf-8-sig'), delimiter='\t'):
    m = RACE_RX.search(row['pointer'])
    if not m:
        continue
    race = m.group(1).lower()
    ko = row['korean']
    hits = POLITE.findall(ko)
    if not hits:
        continue
    for h in hits:
        per_race_end.setdefault(race, {}).setdefault(h, 0)
        per_race_end[race][h] += 1
    if race in ('hylotl', 'apex', 'glitch', 'human', 'avian', 'novakid', 'floran') and len(examples.get(race, [])) < 4:
        mm = POLITE.search(ko)
        i = mm.start()
        examples.setdefault(race, []).append(
            (row['asset'].split('/')[-1] + row['pointer'],
             ko[max(0, i - 60):i + 50].replace('\n', ' / ')))

for r, d in sorted(per_race_end.items(), key=lambda x: -sum(x[1].values())):
    print(r, sum(d.values()), d)
print()
for r, exs in examples.items():
    print('=====', r)
    for a, c in exs:
        print(' ', a)
        print('   ', c)
