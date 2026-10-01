#!/usr/bin/env python3
# Apply translations for inventory-missed strings:
#   - regular-asset rows -> direct overlay ops
#   - .patch rows in GiC/ES/BA -> resolve final base-asset pointer, write ops
#     onto the base asset in the overlay
#   - NonEKI .patch rows -> span-edit repack targets TSV
import csv, json, sys, argparse
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pak import Pak
from align_merged_translations import parse_json

OVERLAY_DIR = {
    "GiC": ROOT / "translation" / "_archive" / "translation-overlays-20260921" / "source-v3" / "localeko_gic_legacy",
    "Extended Story": ROOT / "translation" / "_archive" / "translation-overlays-20260921" / "source-v3" / "localeko_extended_story_legacy",
    "Black Armory": ROOT / "translation" / "_archive" / "translation-overlays-20260921" / "source-v3" / "localeko_black_armory_legacy",
}
PAK = {
    "GiC": ROOT / "mods" / "Galaxy_in_Conflict_contents_2754886445.pak",
    "Extended Story": ROOT / "mods" / "Extended_Story_contents_899795176.pak",
    "Black Armory": ROOT / "mods" / "Black_Armory_4.2.5_FU_NEKI_compat.pak",
}


def load_en2ko():
    """english(normalized) -> korean from memory + missed batch files."""
    en2ko = {}
    for fn, ec, kc in (("data/legacy_translation_memory.tsv", "currentOriginal", "legacyKorean"),
                       ("data/translation_memory.tsv", "currentOriginal", "existingKorean")):
        for r in csv.DictReader(open(HERE / fn, encoding="utf-8-sig", newline=""), delimiter="\t"):
            en2ko.setdefault(r[ec].strip().replace("\r\n", "\n"), r[kc])
    # missed-translation batches: id\tkorean rows keyed against missed_worklist
    id2eng = {}
    for r in csv.DictReader(open(HERE / "data/missed_worklist.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"):
        id2eng[r["id"]] = r["englishText"].strip().replace("\r\n", "\n")
    for bf in sorted((HERE / "translations").glob("missed_*.tsv")):
        for r in csv.reader(open(bf, encoding="utf-8-sig", newline=""), delimiter="\t"):
            if len(r) < 2 or r[0] == "id":
                continue
            eng = id2eng.get(r[0])
            if eng:
                en2ko[eng] = r[1]
    return en2ko


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--write", action="store_true")
    args = ap.parse_args()
    en2ko = load_en2ko()

    rows = list(csv.DictReader(open(HERE / "data/missed_targets.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"))
    counts = Counter()
    overlay_ops = defaultdict(lambda: defaultdict(list))  # mod -> asset -> [ops]
    noneki = []  # (asset, pointer, english, korean)

    for r in rows:
        mod, asset, ptr, eng = r["sourceMod"], r["assetPath"], r["jsonPointer"], r["englishText"]
        key = eng.strip().replace("\r\n", "\n")
        kor = en2ko.get(key, "")
        if not kor:
            counts[("no-translation", mod)] += 1
            continue
        if mod == "NonEKI":
            noneki.append((asset, ptr, eng, kor))
            counts[("noneki", mod)] += 1
            continue
        pak = Pak(str(PAK[mod]))
        if asset.endswith(".patch"):
            # resolve: find the op dict containing this pointer
            doc = parse_json(pak.read(asset))
            # locate op node and value-relative suffix
            def find(n, pth):
                if isinstance(n, dict):
                    if "op" in n and "path" in n and "value" in n and ptr.startswith(pth + "/value"):
                        return (n["path"], ptr[len(pth) + len("/value"):])
                    for k, v in n.items():
                        got = find(v, pth + "/" + k)
                        if got:
                            return got
                elif isinstance(n, list):
                    for i, v in enumerate(n):
                        got = find(v, f"{pth}/{i}")
                        if got:
                            return got
                return None
            got = find(doc, "")
            if not got:
                counts[("unresolved", mod)] += 1
                continue
            base_path, suffix = got
            base_asset = asset[:-len(".patch")]
            overlay_ops[mod][base_asset].append(
                {"op": "replace", "path": base_path + suffix, "value": kor})
            counts[("patch-redirect", mod)] += 1
        else:
            overlay_ops[mod][asset].append(
                {"op": "replace", "path": ptr, "value": kor})
            counts[("direct", mod)] += 1

    for k, v in sorted(counts.items()):
        print(k, v)

    if not args.write:
        return

    # write overlay ops (merge into existing .patch overlays)
    for mod, assets in overlay_ops.items():
        for asset, ops in assets.items():
            pf = OVERLAY_DIR[mod] / (asset.lstrip("/") + ".patch")
            pf.parent.mkdir(parents=True, exist_ok=True)
            existing = json.loads(pf.read_text(encoding="utf-8")) if pf.exists() else []
            seen = {o["path"] for o in existing if isinstance(o, dict)}
            for o in ops:
                if o["path"] in seen:
                    # update existing op value in place
                    for e in existing:
                        if e.get("path") == o["path"]:
                            e["value"] = o["value"]
                else:
                    existing.append(o)
            pf.write_text(json.dumps(existing, ensure_ascii=False, indent=2), encoding="utf-8")

    # NonEKI repack targets
    with open(HERE / "data/missed_noneki_targets.tsv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(("assetPath", "jsonPointer", "englishText", "koreanText"))
        w.writerows(noneki)
    print("wrote", len(noneki), "noneki targets")


if __name__ == "__main__":
    main()
