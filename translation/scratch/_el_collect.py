"""Build collectables title/description translations for thea_weapons.collection
by reusing the deployed pak's item translations (strip color tags)."""
import csv, sys, io, re, json, os
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
sys.stdout.reconfigure(encoding='utf-8')
csv.field_size_limit(10**8)
from pak import Pak
from pak_writer import write_pak

TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
SRC = r"E:\My Games\steamapps\common\Starbound\mods\-9700_Elithian_contents_850109963.pak"
ASSET = '/collections/thea_weapons.collection'
PATCH = ASSET + '.patch'

TAG = re.compile(r'\^[a-zA-Z#0-9]+;')
def strip_tags(s):
    return TAG.sub('', s).strip()

# deployed pak pairs: asset patch -> pointer -> (en,ko)
pk = Pak(TR)
src = Pak(SRC)

raw = src.read(ASSET).decode('utf-8', 'replace')
s = re.sub(r'//[^\n]*', '', raw)
s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
s = re.sub(r',(\s*[}\]])', r'\1', s)
doc = json.loads(s)

# map collectable key -> item patch asset (search deployed pairs)
pairs = {}
for r in csv.reader(open('data/pak_pairs.tsv', encoding='utf-8'), delimiter='\t', quoting=csv.QUOTE_NONE):
    if len(r) >= 4:
        pairs.setdefault(r[0], {})[r[1]] = (r[2], r[3])

# for each collectable, find KO title/desc from matching item patch
col = doc['collectables']
out_ops = []
unmatched = []
for key, entry in col.items():
    # candidate patch assets containing the key
    cand = [a for a in pairs if key in a and a.endswith(('.activeitem.patch', '.item.patch', '.object.patch'))]
    title_en = entry.get('title', '')
    desc_en = entry.get('description', '')
    ko_title = ko_desc = ''
    for a in cand:
        pm = pairs[a]
        for ptr, (en, ko) in pm.items():
            if en.strip('^white;^orange;^reset; ') == title_en:
                ko_title = strip_tags(ko)
            if en.strip('^white;^orange;^reset; ') == desc_en:
                ko_desc = strip_tags(ko)
        if ko_title and ko_desc:
            break
    if not (ko_title and ko_desc):
        # exact-match fallback on stripped EN
        for a, pm in pairs.items():
            for ptr, (en, ko) in pm.items():
                st = strip_tags(en)
                if st == title_en and not ko_title:
                    ko_title = strip_tags(ko)
                if st == desc_en and not ko_desc:
                    ko_desc = strip_tags(ko)
    if not ko_title:
        unmatched.append(('title', key, title_en))
    if not ko_desc:
        unmatched.append(('description', key, desc_en))
    if ko_title:
        out_ops.append({'op': 'test', 'path': f'/collectables/{key}/title', 'value': title_en})
        out_ops.append({'op': 'replace', 'path': f'/collectables/{key}/title', 'value': ko_title})
    if ko_desc:
        out_ops.append({'op': 'test', 'path': f'/collectables/{key}/description', 'value': desc_en})
        out_ops.append({'op': 'replace', 'path': f'/collectables/{key}/description', 'value': ko_desc})

print('ops:', len(out_ops), 'unmatched:', len(unmatched))
for u in unmatched:
    print('  MISS', u[0], u[1], u[2][:70])

# merge with existing patch (has /title op already?)
exist = json.loads(pk.read(PATCH)) if PATCH in pk.index else []
print('existing ops:', len(exist))
manual = json.load(open('scratch/_el_collect_manual.json', encoding='utf-8'))
for path, en, ko in manual:
    out_ops.append({'op': 'test', 'path': path, 'value': en})
    out_ops.append({'op': 'replace', 'path': path, 'value': ko})
merged = exist + out_ops
with open('scratch/_el_collect_unmatched.txt', 'w', encoding='utf-8') as f:
    for u in unmatched:
        f.write('\t'.join(u) + '\n')
if '--apply' in sys.argv:
    n = write_pak(TR, TR, {PATCH: json.dumps(merged, ensure_ascii=False, indent=2).encode('utf-8')})
    print('wrote pak; entries', n)
else:
    print('dry run')
