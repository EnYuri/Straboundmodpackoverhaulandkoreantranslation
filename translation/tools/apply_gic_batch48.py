# Batch48: apply GiC uniq-index translations (data/gic_ko_*.tsv) into
# zz_translation_female.pak as .patch entries for gic_work.tsv rows.
# Test values are re-read from the live GiC pak so stale/multiline strings
# can't mismatch. Existing patch entries are merged (same-path ops replaced).
import sys, io, json, re, csv, os
sys.stdout.reconfigure(encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921\tools")
from pak import Pak
from pak_writer import write_pak

BASE = r"E:\My Games\steamapps\common\Starbound\translation\translation-baseline-20260921"
TR = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"
GIC = r"E:\My Games\steamapps\common\Starbound\mods\Galaxy_in_Conflict_contents_2754886445.pak"


def parse_sb(raw):
    s = raw.decode('utf-8', errors='replace')
    s = re.sub(r'//[^\n]*', '', s)
    s = re.sub(r'/\*.*?\*/', '', s, flags=re.S)
    out = []
    ins = False
    for i, c in enumerate(s):
        if c == '"' and (i == 0 or s[i - 1] != chr(92)):
            ins = not ins
        out.append('\\r' if ins and c == '\r' else '\\n' if ins and c == '\n' else c)
    return json.loads(re.sub(r',(\s*[}\]])', r'\1', ''.join(out)))


csv.field_size_limit(10 ** 8)

# uniq idx -> EN / KO
uniq_en = {int(k): v for k, v in json.load(open(os.path.join(BASE, "data", "gic_uniq.json"), encoding="utf-8")).items()}
idx_ko = {}
for fn in ["gic_ko_01.tsv", "gic_ko_02.tsv", "gic_ko_03.tsv", "gic_ko_04.tsv", "gic_ko_05.tsv", "gic_ko_06.tsv", "gic_ko_07.tsv", "gic_ko_08.tsv", "gic_ko_09.tsv", "gic_ko_10.tsv", "gic_ko_11.tsv", "gic_ko_12.tsv"]:
    for l in open(os.path.join(BASE, "data", fn), encoding="utf-8"):
        if not l.strip():
            continue
        i, t = l.rstrip("\n").split("\t", 1)
        # TSV stores literal \n sequences; source fields use real newlines
        idx_ko[int(i)] = t.replace("\\n", "\n")
en2ko = {uniq_en[i]: idx_ko[i] for i in idx_ko if i in uniq_en}
print("ko map:", len(en2ko))

# fill work rows
work = []
for r in csv.reader(open(os.path.join(BASE, "data", "gic_work.tsv"), encoding="utf-8"), delimiter="\t"):
    if r and r[0] != "asset":
        work.append(r)
print("work rows:", len(work))

gic = Pak(GIC)
per_asset = {}
skipped = []
for a, f, en, ko, *rest in work:
    k = en2ko.get(en)
    if not k:
        skipped.append((a, f, "no-ko"))
        continue
    per_asset.setdefault(a, {})[f] = k

overrides = {}
made_ops = 0
for a, fmap in sorted(per_asset.items()):
    try:
        doc = parse_sb(gic.read(a))
    except Exception as e:
        skipped.append((a, "*", "unreadable"))
        continue
    new = []
    for f, k in fmap.items():
        cur = doc.get(f)
        if not isinstance(cur, str):
            skipped.append((a, f, "no-field"))
            continue
        new.append([{"op": "test", "path": "/" + f, "value": cur},
                    {"op": "replace", "path": "/" + f, "value": k}])
        made_ops += 1
    overrides[a + ".patch"] = new

# merge with existing patches inside translation pak
tr = Pak(TR)
merged = 0
for name, ops in list(overrides.items()):
    if name in tr.index:
        try:
            old = parse_sb(tr.read(name))
        except Exception:
            old = []
        keep = []
        newpaths = {op["path"] for grp in ops for op in grp}
        for el in old if isinstance(old, list) else []:
            grp = el if isinstance(el, list) else [el]
            if any(o.get("op") == "replace" and o.get("path") in newpaths for o in grp):
                merged += 1
                continue  # superseded by this run
            keep.append(el)
        overrides[name] = keep + ops

files = {}
for name, ops in overrides.items():
    files[name] = json.dumps(ops, ensure_ascii=False, indent=2).encode("utf-8")

print("patch entries:", len(files), "replace ops:", made_ops, "merged-over:", merged)
print("skipped:", len(skipped))
for s in skipped[:15]:
    print("  SKIP", s)

if "--apply" in sys.argv:
    n = write_pak(TR, TR, files)
    print("wrote pak entries:", n)
else:
    print("dry run — pass --apply to write")
