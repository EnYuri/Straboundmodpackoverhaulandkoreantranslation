import csv
import json
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

BASE = Path(__file__).parent.parent


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


def load_targets(fname):
    out = []
    with open(fname, encoding="utf-8-sig") as f:
        r = csv.DictReader(f, delimiter="\t")
        for row in r:
            out.append(row)
    return out


def main():
    targets = load_targets("archive/glitch_polite_violations.tsv") + load_targets("archive/novakid_polite_violations.tsv")
    need = {(t["asset"], t["pointer"]) for t in targets}
    print("targets:", len(targets))

    ko_pak = Pak(str(STAR / "mods" / "zz_translation_female.pak"))

    # EN from nested test/replace, in-place in the same .patch doc
    en_map = {}

    def iter_pairs_nested(doc):
        if not isinstance(doc, list):
            return
        for group in doc:
            if not isinstance(group, list):
                continue
            tests = {}
            for op in group:
                if isinstance(op, dict) and op.get("op") == "test" and isinstance(op.get("value"), str):
                    tests[op.get("path")] = op["value"]
            for op in group:
                if isinstance(op, dict) and op.get("op") == "replace" and isinstance(op.get("value"), str):
                    path = op.get("path")
                    if path in tests:
                        yield path, tests[path]

    assets_needed = {a for a, p in need}
    flat_needed = []
    for asset in assets_needed:
        try:
            doc = json.loads(ko_pak.read(asset))
        except Exception:
            continue
        if isinstance(doc, list) and doc and all(isinstance(g, list) for g in doc):
            for path, en in iter_pairs_nested(doc):
                if (asset, path) in need:
                    en_map[(asset, path)] = en
        else:
            flat_needed.append(asset)

    print("resolved via nested test/replace:", len(en_map))
    print("flat assets needing base-pak lookup:", len(flat_needed))

    # For flat patches, find base pak + resolve original EN via JSON pointer.
    base_paths_needed = {a[: -len(".patch")] for a in flat_needed}
    candidates = {}
    pak_files = sorted(STAR.glob("mods/*.pak")) + [STAR / "packed.pak", STAR / "opensb.pak"]
    for pf in pak_files:
        if pf.name == "zz_translation_female.pak":
            continue
        try:
            pk = Pak(str(pf))
        except Exception:
            continue
        hit = base_paths_needed & set(pk.index.keys())
        for bp in hit:
            candidates.setdefault(bp, str(pf))

    pak_cache = {}
    for asset in flat_needed:
        base_path = asset[: -len(".patch")]
        pak_path = candidates.get(base_path)
        if not pak_path:
            continue
        pk = pak_cache.get(pak_path)
        if pk is None:
            pk = Pak(pak_path)
            pak_cache[pak_path] = pk
        try:
            base_doc = json.loads(pk.read(base_path))
        except Exception:
            continue
        for a, p in need:
            if a != asset:
                continue
            try:
                val = json_pointer_get(base_doc, p)
            except (KeyError, IndexError, TypeError, ValueError):
                continue
            if isinstance(val, str):
                en_map[(a, p)] = val

    print("total EN resolved:", len(en_map))

    with open("archive/polite_violations_with_en.tsv", "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["kind", "asset", "pointer", "english", "korean"])
        for t in targets:
            key = (t["asset"], t["pointer"])
            kind = "glitch" if "glitchdescription" in t["pointer"].lower() else "novakid"
            w.writerow([kind, t["asset"], t["pointer"], en_map.get(key, ""), t["korean"]])

    print("wrote polite_violations_with_en.tsv")


if __name__ == "__main__":
    main()
