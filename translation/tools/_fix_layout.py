#!/usr/bin/env python3
"""Fix structural defects found in the deployed pak after the rest-file
realignment repair:

1. Literal backslash-n sequences in KO values where EN has real newlines
   (the two-character escape renders as text in-game). KO segments are
   re-joined using EN's newline runs verbatim.
2. Private-use glyph runs (e.g. \\ue024 tier stars) that EN shows inside
   colour-tag spans but KO dropped, plus two cases where a translator
   substituted a literal star character.
"""
import csv, io, json, os, re, sys, time

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

MODS = r"E:/My Games/steamapps/common/Starbound/mods"
TR = os.path.join(MODS, "zz_translation_female.pak")
PAIRS = "data/pak_pairs.tsv"
BN = "\\" + "n"
PUA = re.compile(r"[-]+")

csv.field_size_limit(10 ** 8)
rows = list(csv.DictReader(open(PAIRS, encoding="utf-8-sig"), delimiter="\t"))

lit_fix, gly_fix = [], []
for r in rows:
    e, k = r["english"], r["korean"]
    if not e:
        continue
    # --- literal backslash-n ---
    if BN in k:
        esegs = re.split(r"\n+", e)
        ksegs = re.split(re.escape(BN) + r"+", k)
        if len(esegs) == len(ksegs):
            nk = ksegs[0]
            for i in range(1, len(ksegs)):
                sep = re.findall(r"\n+", e)[i - 1]
                nk += sep + ksegs[i]
            lit_fix.append((r["asset"], r["pointer"], k, nk))
        else:
            print("SEGMENT MISMATCH", r["asset"], r["pointer"])
    # --- missing glyph runs ---
    eruns = PUA.findall(e)
    if eruns and PUA.findall(k) != eruns:
        nk = k
        # translate literal star back to EN glyph
        if "★" in nk:
            nk = nk.replace("★", eruns[0])
        # for each EN run missing in KO, insert before the following ^tag;
        for m in re.finditer(r"([-]+)(\^[^;^\s]{1,20};)", e):
            run, after = m.group(1), m.group(2)
            if run in nk:
                continue
            # KO position: same `after` tag whose char before isn't a glyph
            idx = nk.find(after)
            while idx != -1 and (idx > 0 and PUA.match(nk[idx - 1:idx])):
                idx = nk.find(after, idx + 1)
            if idx == -1:
                idx = nk.rfind(after)
            if idx != -1:
                nk = nk[:idx] + run + nk[idx:]
        if nk != k:
            gly_fix.append((r["asset"], r["pointer"], k, nk))

print("literal-nl fixes:", len(lit_fix), "| glyph fixes:", len(gly_fix))
for a, p, k, nk in lit_fix[:5]:
    print("  LIT", a[-45:], repr(nk[:70]))
for a, p, k, nk in gly_fix[:5]:
    print("  GLY", a[-45:], repr(nk[-40:]))

pk = pak.Pak(TR)
byfile = {}
for a, p, old, new in lit_fix + gly_fix:
    byfile.setdefault(a, []).append((p, old, new))
ov = {}
unmatched = 0
for fn, lst in byfile.items():
    d = sbjson.parse_sb(pk.read(fn).decode("utf-8"))
    want = {p: (old, new) for p, old, new in lst}
    n = 0
    def rec(o):
        global n, unmatched
        if isinstance(o, list):
            for x in o:
                rec(x)
        elif isinstance(o, dict):
            if o.get("op") == "replace":
                p = o.get("path"); v = o.get("value")
                if p in want and isinstance(v, str):
                    old, new = want[p]
                    if v == old:
                        o["value"] = new; n += 1
                    else:
                        unmatched += 1
            for x in o.values():
                if isinstance(x, (list, dict)):
                    rec(x)
    rec(d)
    if n:
        ov[fn] = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
print("files patched:", len(ov), "| unmatched:", unmatched)
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
elif not ov:
    print("nothing to write")
else:
    print("dry-run only")
