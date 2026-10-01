import csv
import json
import re
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

HERE = Path(__file__).parent.parent

NONEKI_PAK = STAR / "mods" / "NonEKI_9_FU_compat.pak"
HANGUL = re.compile(r"[\uac00-\ud7a3]")


def json_pointer_get(doc, pointer):
    if pointer == "":
        return doc
    parts = pointer.lstrip("/").split("/")
    cur = doc
    for part in parts:
        part = part.replace("~1", "/").replace("~0", "~")
        if isinstance(cur, list):
            cur = cur[int(part)]
        elif isinstance(cur, dict):
            cur = cur[part]
        else:
            raise KeyError(part)
    return cur


# ---- 1. collect NonEKI displayed KO strings with their pointer ----
pak = Pak(str(NONEKI_PAK))


def walk_paths(v, prefix=""):
    if isinstance(v, str):
        yield prefix, v
    elif isinstance(v, list):
        for i, x in enumerate(v):
            yield from walk_paths(x, f"{prefix}/{i}")
    elif isinstance(v, dict):
        for k, x in v.items():
            yield from walk_paths(x, f"{prefix}/{k}")


rows = []  # (asset, pointer, korean, en_test_if_any)
for name in pak.index:
    try:
        doc = json.loads(pak.read(name))
    except Exception:
        continue
    if name.endswith(".patch"):
        if isinstance(doc, list) and doc and all(isinstance(g, list) for g in doc):
            for group in doc:
                tests = {}
                for op in group:
                    if isinstance(op, dict) and op.get("op") == "test":
                        for subptr, s in walk_paths(op.get("value"), op.get("path", "")):
                            tests[subptr] = s
                for op in group:
                    if isinstance(op, dict) and op.get("op") == "replace":
                        for subptr, s in walk_paths(op.get("value"), op.get("path", "")):
                            if len(s) >= 15 and " " in s and HANGUL.search(s):
                                rows.append((name, subptr, s, tests.get(subptr)))
        else:
            for op in doc if isinstance(doc, list) else []:
                if isinstance(op, dict) and op.get("op") == "replace":
                    for subptr, s in walk_paths(op.get("value"), op.get("path", "")):
                        if len(s) >= 15 and " " in s and HANGUL.search(s):
                            rows.append((name, subptr, s, None))
    else:
        for ptr, s in walk_paths(doc):
            if len(s) >= 15 and " " in s and HANGUL.search(s):
                rows.append((name, ptr, s, None))

print("NonEKI korean-ish rows:", len(rows))

# ---- 2. resolve EN for rows without inline test value, via other paks ----
base_paths_needed = set()
for name, ptr, ko, en in rows:
    if en is None:
        base = name[:-len(".patch")] if name.endswith(".patch") else name
        base_paths_needed.add(base)

candidates = {}
pak_files = (sorted(STAR.glob("mods/*.pak"))
             + [STAR / "assets" / "packed.pak", STAR / "assets" / "opensb.pak"])
for pf in pak_files:
    if pf.name == "NonEKI_9_FU_compat.pak":
        continue
    try:
        pk = Pak(str(pf))
    except Exception:
        continue
    hit = base_paths_needed & set(pk.index.keys())
    for bp in hit:
        candidates.setdefault(bp, str(pf))

pak_cache = {}
resolved_en = {}
for name, ptr, ko, en in rows:
    if en is not None:
        continue
    base = name[:-len(".patch")] if name.endswith(".patch") else name
    pak_path = candidates.get(base)
    if not pak_path:
        continue
    pk = pak_cache.get(pak_path)
    if pk is None:
        pk = Pak(pak_path)
        pak_cache[pak_path] = pk
    try:
        base_doc = json.loads(pk.read(base))
    except Exception:
        continue
    try:
        val = json_pointer_get(base_doc, ptr)
    except (KeyError, IndexError, TypeError, ValueError):
        continue
    if isinstance(val, str):
        resolved_en[(name, ptr)] = (val, Path(pak_path).name)

print("resolved EN via base pak:", len(resolved_en))

# ---- 3. build sbkor EN->KO lookup ----
sbkor_map = {}
with open(HERE / "alignment" / "sbkor.tsv", encoding="utf-8-sig", newline="") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        en = row.get("currentOriginal") or ""
        ko = row.get("existingKorean") or ""
        if en and ko and en != ko:
            sbkor_map[en] = ko

print("sbkor EN->KO entries:", len(sbkor_map))

# ---- 4. cross-reference ----
out_reuse = []
out_review = []
for name, ptr, ko, en in rows:
    src = "inline-test"
    if en is None:
        r2 = resolved_en.get((name, ptr))
        if r2:
            en, base_pak_name = r2
            src = f"base:{base_pak_name}"
        else:
            en = None
            src = "unresolved"
    if en and en in sbkor_map:
        sb_ko = sbkor_map[en]
        if sb_ko != ko:
            out_reuse.append((name, ptr, en, ko, sb_ko))
    else:
        out_review.append((name, ptr, en or "", ko, src))

print("rows where sbkor has a different (better) translation:", len(out_reuse))
print("rows needing manual review (no sbkor match):", len(out_review))

with open(HERE / "archive/noneki_sbkor_reuse.tsv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["asset", "pointer", "english", "current_korean", "sbkor_korean"])
    for row in out_reuse:
        w.writerow(row)

with open(HERE / "archive/noneki_needs_review.tsv", "w", encoding="utf-8-sig", newline="") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(["asset", "pointer", "english", "current_korean", "en_source"])
    for row in out_review:
        w.writerow(row)

print("wrote noneki_sbkor_reuse.tsv, noneki_needs_review.tsv")
