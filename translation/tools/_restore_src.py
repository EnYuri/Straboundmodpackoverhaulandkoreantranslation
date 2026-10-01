#!/usr/bin/env python3
"""Restore upstream-Korean values (the pak's own test values) for fields
where our re-translation silently dropped stat/immunity/bonus content.
Each flagged row's KO becomes its srcKO verbatim, except a small map of
garbled one-line rewrites also restored to src, and one guide page where
the dropped line is appended instead.
"""
import csv, io, json, os, re, sys, time, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

MODS = r"E:/My Games/steamapps/common/Starbound/mods"
TR = os.path.join(MODS, "zz_translation_female.pak")
csv.field_size_limit(10 ** 8)
TAG = re.compile(r"\^[^;^\s]{1,20};")
STATKW = ("면역", "저항", "투명도", "(한손)")

rows = list(csv.DictReader(open("data/upk_review.tsv", encoding="utf-8-sig"), delimiter="\t"))
restore = []
append = []  # (asset, pointer, line) -> append missing srcKO line
for r in rows:
    src, our = r["srcko"], r["ourko"]
    if "/dialog/" in r["asset"]:
        continue
    ours = TAG.sub("", our)
    need = False
    if "세트 보너스" in src and "세트 보너스" not in our:
        need = True
    for ln in src.split("\n"):
        p = TAG.sub("", ln).strip()
        if len(p) < 3 or p in ours:
            continue
        dmiss = [d for d in re.findall(r"\d+(?:\.\d+)?%?", ln) if d not in our]
        kmiss = [w for w in STATKW if w in p and w not in ours]
        if dmiss or kmiss:
            need = True
    if need:
        restore.append(r)

# garbled one-liner codex pages -> srcKO is clearly better
GARBLED = {
    ("/codex/documents/ffguide6.codex.patch", "/contentPages/0"),
    ("/codex/documents/ffguidebattle.codex.patch", "/contentPages/0"),
    ("/codex/documents/ffguidepower.codex.patch", "/contentPages/0"),
}
for r in rows:
    if (r["asset"], r["pointer"]) in GARBLED and r not in restore:
        restore.append(r)

# guideBook: ours kept line 1, dropped line 2 -> append it
for r in rows:
    if r["asset"].endswith("arcana_guideBook.config.patch") and "Voyage" in r["srcko"] and "Voyage" not in r["ourko"]:
        for ln in r["srcko"].split("\n"):
            if "Voyage" in ln:
                append.append((r["asset"], r["pointer"], r["ourko"], ln.strip()))

print("restore:", len(restore), "| append:", len(append))
byfile = collections.defaultdict(list)
for r in restore:
    byfile[r["asset"]].append((r["pointer"], r["ourko"], r["srcko"]))
for a, p, old, line in append:
    byfile[a].append((p, old, old.rstrip() + "\n" + line))

pk = pak.Pak(TR)
ov = {}
un = []
for fn, lst in byfile.items():
    try:
        d = sbjson.parse_sb(pk.read(fn).decode("utf-8"))
    except Exception:
        continue
    want = {p: (o, n) for p, o, n in lst}
    n = 0
    def rec(o):
        global n
        if isinstance(o, list):
            for x in o:
                rec(x)
        elif isinstance(o, dict):
            if o.get("op") == "replace":
                p = o.get("path"); v = o.get("value")
                if p in want and isinstance(v, str) and v == want[p][0]:
                    o["value"] = want[p][1]; n += 1
            for x in o.values():
                if isinstance(x, (list, dict)):
                    rec(x)
    rec(d)
    if n:
        ov[fn] = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    if n < len(lst):
        un.append((fn, n, len(lst)))
print("patched:", len(ov), "| unmatched:", un[:10])
del pk
if "--apply" in sys.argv and ov:
    staged = TR + ".staged"
    pak_writer.write_pak(staged, TR, ov)
    for i in range(60):
        try:
            os.replace(staged, TR)
            print("replaced")
            break
        except PermissionError:
            time.sleep(5)
else:
    print("dry-run")
