# -*- coding: utf-8 -*-
"""Apply uncovered-field translations into the deployed pak.

Reads a TSV file with columns en\tko (header required), maps each EN to all
uncovered (file,path) targets from data/_uncov_rows.pkl, and appends
test+replace op groups to the corresponding patch docs inside the pak.

Usage: python tools/_uncov_apply.py <map_tsv> [--dry]
"""
import sys, io, os, re, csv, json, time, pickle, collections

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")
sys.path.insert(0, r"E:/My Games/steamapps/common/Starbound")
sys.path.insert(0, "tools")
import pak, sbjson, pak_writer

csv.field_size_limit(10**7)
TR = r"E:/My Games/steamapps/common/Starbound/mods/zz_translation_female.pak"

KEBAB = re.compile(r"^[a-z]+(-[a-z]+)+$")
IDTOK = re.compile(r"^[A-Za-z_0-9]+$")
CAMEL = re.compile(r"^[a-z]+[A-Z0-9][A-Za-z0-9_]*$")


def skipid(v):
    s = v.strip()
    if KEBAB.match(s):
        return True
    if " " not in s and IDTOK.match(s) and (
        len(s) > 12 or CAMEL.match(s) or s.islower() or s.isupper() or re.search(r"[0-9_]", s)
    ):
        return True
    return False


def load_targets():
    rows = pickle.load(open("data/_uncov_rows.pkl", "rb"))
    rows = [r for r in rows if not skipid(r[3])]
    tm = {}
    for r in csv.DictReader(open("data/pak_pairs.tsv", encoding="utf-8-sig"), delimiter="\t"):
        if r["english"] and r["korean"] and r["english"] != r["korean"] and re.search(r"[가-힣]", r["korean"]):
            tm.setdefault(r["english"], r["korean"])
    todo = collections.defaultdict(list)
    for fn, path, leaf, val in rows:
        if val not in tm:
            todo.setdefault(val, []).append((fn, path))
    return todo


def main():
    src = sys.argv[1]
    dry = "--dry" in sys.argv
    ko_map = {}
    for r in csv.DictReader(open(src, encoding="utf-8-sig"), delimiter="\t"):
        if r.get("en") and r.get("ko"):
            ko_map[r["en"]] = r["ko"]
    todo = load_targets()
    per_file = collections.defaultdict(list)
    missed = [v for v in ko_map if v not in todo]
    for v, ko in ko_map.items():
        for fn, path in todo.get(v, []):
            per_file[fn].append((path, v, ko))
    total = sum(len(v) for v in per_file.values())
    print("map entries:", len(ko_map), "| matched files:", len(per_file), "| ops:", total)
    if missed:
        print("missed:", len(missed), missed[:5])
    if dry:
        return
    pk = pak.Pak(TR)
    ov = {}
    for fn, lst in per_file.items():
        if fn in pk.index:
            try:
                d = sbjson.parse_sb(pk.read(fn).decode("utf-8-sig"))
            except Exception:
                continue
        else:
            d = []
        grp = []
        for path, en, ko in lst:
            grp.append({"op": "test", "path": path, "value": en})
            grp.append({"op": "replace", "path": path, "value": ko})
        if isinstance(d, list):
            d.append(grp)
        else:
            d = [grp]
        ov[fn] = json.dumps(d, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    pak_writer.write_pak(TR + ".staged", TR, ov)
    del pk
    for i in range(60):
        try:
            os.replace(TR + ".staged", TR)
            print("replaced")
            break
        except PermissionError:
            time.sleep(5)


if __name__ == "__main__":
    main()
