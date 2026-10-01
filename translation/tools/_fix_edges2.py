#!/usr/bin/env python3
"""Second-pass layout repair: work on live patch ops (not the TSV) so
\\r\\n-bearing values are matched exactly. For every replace op whose
paired test value still differs in edge whitespace or newline count,
synchronise the KO leading/trailing whitespace run to EN's and convert
literal backslash-n sequences to real newlines. Remaining internal
newline mismatches are reported, not auto-edited.
"""
import csv, io, json, os, re, sys, time, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

MODS = r"E:/My Games/steamapps/common/Starbound/mods"
TR = os.path.join(MODS, "zz_translation_female.pak")
BN = "\\" + "n"
csv.field_size_limit(10 ** 8)

targets = collections.defaultdict(set)
for r in csv.DictReader(open("data/qa_struct_broken.tsv", encoding="utf-8-sig"), delimiter="\t"):
    targets[r["asset"]].add(r["pointer"])

pk = pak.Pak(TR)
ov = {}
residual = []
for fn, ptrs in targets.items():
    try:
        d = sbjson.parse_sb(pk.read(fn).decode("utf-8"))
    except Exception:
        continue
    n = 0
    for grp in d:
        if not isinstance(grp, list):
            grp = [grp]
        tv = None
        for op in grp:
            if not isinstance(op, dict):
                continue
            if op.get("op") == "test":
                tv = op.get("value")
            elif op.get("op") == "replace" and op.get("path") in ptrs and isinstance(tv, str) and isinstance(op.get("value"), str):
                e, k = tv, op["value"]
                nk = k
                if BN in nk:
                    nk = nk.replace(BN, "\n")
                lead = re.match(r"\s*", e).group(0)
                trail = re.search(r"\s*$", e).group(0)
                body = nk.strip("\r\n \t")
                if body:
                    cand = lead + body + trail
                    # keep KO's own interior; only edges synced
                    if cand != nk and (nk.startswith(lead) is False or nk.endswith(trail) is False or e[:1] != nk[:1]):
                        # only apply when edge runs actually differ
                        if re.match(r"\s*", nk).group(0) != lead or re.search(r"\s*$", nk).group(0) != trail:
                            nk = cand
                if nk != k:
                    op["value"] = nk
                    n += 1
                if (tv.count("\n") != op["value"].count("\n")):
                    residual.append((fn, op.get("path"), tv, op["value"]))
    if n:
        ov[fn] = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
        print(fn[-55:], "fixed", n)
print("files:", len(ov))
print("residual inner-nl diffs:", len(residual))
for f, p, e, k in residual[:10]:
    print("  RES", f[-45:], p[:35])
    print("    EN:", repr(e[:85]))
    print("    KO:", repr(k[:85]))
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
