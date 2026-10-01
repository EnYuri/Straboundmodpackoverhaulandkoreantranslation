# -*- coding: utf-8 -*-
# Mechanical quality scan over extracted pak pairs (EN -> KO).
import sys, io, csv, re, collections
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
csv.field_size_limit(sys.maxsize)

PAIRS = 'data/pak_pairs.tsv'
TAG = re.compile(r'\^[^;^\s]{1,20};')
PH = re.compile(r'%s|%\d+|\{[^}]{1,20}\}|\$\{[^}]+\}')
INPUT = re.compile(r'\[[A-Za-z0-9 +\-]{1,20}\]')
PUA = re.compile(r'[\ue000-\uf8ff]')
NUM = re.compile(r'\d+(?:\.\d+)?')
ENWORD = re.compile(r'\b[A-Za-z]{3,}\b')

# English words legitimately allowed inside KO (names, brands, units, code)
KO_EN_OK = {
    'SAIL', 'SAI', 'USBM', 'LMAO', 'NPC', 'AI', 'HP', 'MP', 'PP', 'DPS', 'EXP',
    'UI', 'BGM', 'OST', 'LMB', 'RMB', 'WASD', 'FPS', 'BYOS', 'EPP', 'RPG',
    'WiFi', 'URL', 'OK', 'NASA', 'FBI', 'CIA', 'KGB', 'GPS', 'LED', 'LCD',
    'HDMI', 'USB', 'API', 'DLC', 'MOD', 'WIP', 'TBD', 'DIY', 'ASAP',
    'HP+', 'Lv', 'MRE', 'IED', 'VTOL', 'APC', 'RPG7', 'AK', 'M4', 'M16',
    'MP5', 'SVD', 'PKM', 'PKP', 'PPSh', 'PP', 'TT', 'M9', 'Glock', 'Beretta',
    'Kalashnikov', 'Mosin', 'Nagant', 'Steyr', 'FN', 'HK', 'SIG', 'Colt',
    'Winchester', 'Remington', 'Mossberg', 'Barrett', 'Desert', 'Eagle',
    'Raytheon', 'Lockheed', 'Boeing', 'Tesla', 'Edison', 'Newton',
    'Kafka', 'Lovecraft', 'Poe', 'Shelley', 'Stoker', 'Verne', 'Wells',
    'Asimov', 'Clarke', 'Heinlein', 'Dick', 'Orwell', 'Huxley',
    'Batman', 'Superman', 'Joker', 'Mario', 'Luigi', 'Sonic', 'Pac-Man',
    'Zelda', 'Kirby', 'Pikachu', 'Godzilla', 'Gundam', 'Evangelion',
    'McDonalds', 'Coca', 'Cola', 'Pepsi', 'Nike', 'Adidas', 'Lego',
    'YouTube', 'Google', 'Facebook', 'Twitter', 'Reddit', 'Discord',
    'Steam', 'Windows', 'Linux', 'Apple', 'Samsung', 'Intel', 'AMD',
    'NVIDIA', 'Xbox', 'PlayStation', 'Nintendo', 'Sega', 'Atari',
    'Bible', 'Quran', 'Torah', 'Buddha', 'Jesus', 'Satan', 'Lucifer',
    'Thor', 'Odin', 'Zeus', 'Hades', 'Athena', 'Apollo', 'Ares',
    'Poseidon', 'Hermes', 'Aphrodite', 'Artemis', 'Hephaestus',
    'Freya', 'Loki', 'Baldur', 'Ragnarok', 'Valkyrie', 'Valhalla',
    'Samurai', 'Ninja', 'Shogun', 'Ronin', 'Katana', 'Wakizashi',
    'Tanto', 'Naginata', 'Shuriken', 'Kunai', 'Oni', 'Kappa', 'Tengu',
    'Kitsune', 'Tanuki', 'Yokai', 'Nekomata', 'Bakeneko', 'Yuki',
    'Kitsunebi', 'Anime', 'Manga', 'Otaku', 'Kawaii', 'Senpai',
    'Baka', 'Chan', 'San', 'Kun', 'Sama', 'Dono', 'Sensei', 'Sempai',
    'Taxi', 'Bus', 'Metro', 'Taxiway', 'Bistro', 'Cafe', 'Bar', 'Pub',
    'Hotel', 'Motel', 'Resort', 'Casino', 'Cinema', 'Theater',
    'Museum', 'Gallery', 'Studio', 'Garage', 'Salon', 'Clinic',
    'Lorem', 'ipsum', 'dolor', 'amet', 'consectetur', 'adipiscing',
}

def tag_key(t):
    return t

def seq_diff(a, b):
    ca, cb = collections.Counter(a), collections.Counter(b)
    return list((ca - cb).elements()), list((cb - ca).elements())

issues = collections.Counter()
samples = collections.defaultdict(list)
total = 0
for r in csv.DictReader(open(PAIRS, encoding='utf-8-sig'), delimiter='\t'):
    en, ko = r['english'], r['korean']
    total += 1
    if not ko:
        issues['empty_ko'] += 1
        samples['empty_ko'].append(r)
        continue
    # 1. color/format tag parity
    m1, m2 = seq_diff(TAG.findall(en), TAG.findall(ko))
    if m1 or m2:
        issues['tag_diff'] += 1
        samples['tag_diff'].append((r, m1[:3], m2[:3]))
    # 2. placeholder parity
    m1, m2 = seq_diff(PH.findall(en), PH.findall(ko))
    if m1 or m2:
        issues['ph_diff'] += 1
        samples['ph_diff'].append((r, m1[:3], m2[:3]))
    # 3. PUA glyph parity
    m1, m2 = seq_diff(PUA.findall(en), PUA.findall(ko))
    if m1 or m2:
        issues['pua_diff'] += 1
        samples['pua_diff'].append((r, m1[:3], m2[:3]))
    # 4. input token parity ([Jump], [FIRE] etc, all-caps or known keys only)
    in_en = [t for t in INPUT.findall(en) if t[1:-1].strip() and (t[1:-1].isupper() or t[1:-1] in ('Jump', 'Shift', 'Down', 'Up', 'Special 1', 'Special 2', 'Left', 'Right', 'Fire'))]
    in_ko = INPUT.findall(ko)
    if in_en and collections.Counter(in_en) != collections.Counter(in_ko):
        issues['input_diff'] += 1
        samples['input_diff'].append((r, in_en, in_ko))
    # 5. newline count
    if en.count('\n') != ko.count('\n'):
        issues['nl_diff'] += 1
        samples['nl_diff'].append(r)
    # 6. leading/trailing whitespace parity
    if (en[:1].isspace()) != (ko[:1].isspace()) or (en[-1:].isspace()) != (ko[-1:].isspace()):
        issues['ws_edge'] += 1
        samples['ws_edge'].append(r)
    # 7. numbers in EN missing from KO (loose: every EN num should appear or be part of a translated number)
    ne, nk = NUM.findall(en), NUM.findall(ko)
    miss = [n for n in ne if n not in nk]
    if miss and ne:
        issues['num_miss'] += 1
        samples['num_miss'].append((r, miss[:5]))
    # 8. leftover English words in KO
    if re.search(r'[가-힣]', ko):
        left = [w for w in ENWORD.findall(re.sub(r'\^[a-zA-Z#0-9]{1,20};', '', ko))
                if w not in KO_EN_OK]
        if left:
            issues['ko_en_left'] += 1
            samples['ko_en_left'].append((r, left[:5]))

print('total pairs:', total)
for k, v in issues.most_common():
    print('%-14s %d' % (k, v))

w = csv.writer(open('data/qa_mech_report.tsv', 'w', encoding='utf-8', newline=''), delimiter='\t')
w.writerow(['issue', 'asset', 'pointer', 'english', 'korean', 'detail'])
for k, lst in samples.items():
    for item in lst:
        if isinstance(item, tuple):
            r, *det = item
            w.writerow([k, r['asset'], r['pointer'], r['english'], r['korean'], repr(det)[:200]])
        else:
            w.writerow([k, item['asset'], item['pointer'], item['english'], item['korean'], ''])
print('report -> data/qa_mech_report.tsv')
