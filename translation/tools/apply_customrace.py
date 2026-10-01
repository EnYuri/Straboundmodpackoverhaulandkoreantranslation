"""Merge translated translations/customrace_batch_*.tsv into mods/zz_translation_female.pak.

For every unique english string with a korean translation, find all
(asset, pointer) occurrences from custom_race_desc_need.tsv and append a
[test,replace] op-group to that asset's .patch entry (existing or new),
then rewrite female_translation.pak in place via pak_writer.
"""
import csv, glob, json, sys
from pathlib import Path
from collections import defaultdict

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
from pak import Pak
import pak_writer

UNIQ = HERE / "translations" / "customrace_unique.tsv"
NEED = HERE / "data/custom_race_desc_need.tsv"
TARGET_PAK = ROOT / "mods" / "zz_translation_female.pak"


def load_translated():
    id2en = {}
    for r in csv.DictReader(open(UNIQ, encoding="utf-8-sig", newline=""), delimiter="\t"):
        id2en[int(r["id"])] = r["english"]
    id2ko = {}
    for f in glob.glob(str(HERE / "translations" / "customrace_batch_*.tsv")):
        with open(f, encoding="utf-8-sig", newline="") as fh:
            for row in csv.reader(fh, delimiter="\t"):
                if row and row[0].isdigit():
                    idx = int(row[0])
                    ko = row[1] if len(row) > 1 else ""
                    if ko:
                        id2ko[idx] = ko
    en2ko = {}
    dupes = 0
    for idx, ko in id2ko.items():
        en = id2en.get(idx)
        if en is None:
            print(f"WARN: unknown id {idx} in batch files", file=sys.stderr)
            continue
        if en in en2ko and en2ko[en] != ko:
            dupes += 1
        en2ko[en] = ko
    if dupes:
        print(f"WARN: {dupes} conflicting duplicate english->korean mappings", file=sys.stderr)
    return en2ko


def main():
    en2ko = load_translated()
    print("translated unique strings:", len(en2ko))

    by_asset = defaultdict(list)  # asset -> [(pointer, english)]
    with open(NEED, encoding="utf-8-sig", newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["english"] in en2ko:
                by_asset[r["asset"]].append((r["pointer"], r["english"]))

    print("assets touched:", len(by_asset))

    base_pak = Pak(str(TARGET_PAK))
    overrides = {}
    new_groups_total = 0

    for asset, occs in by_asset.items():
        patch_rel = asset + ".patch"
        if patch_rel in base_pak.index:
            existing = json.loads(base_pak.read(patch_rel).decode("utf-8-sig"))
        else:
            existing = []

        our_paths = {}  # pointer -> (english, korean), de-duped, last-write-wins
        for pointer, english in occs:
            our_paths[pointer] = (english, en2ko[english])

        # drop any existing item (bare op dict, or grouped op list) that touches
        # one of our target pointers, so corrections to already-applied
        # translations take effect; keep everything else untouched
        def touches_ours(item):
            ops = item if isinstance(item, list) else [item]
            return any(op.get("path") in our_paths for op in ops)

        kept = [g for g in existing if not touches_ours(g)]

        for pointer, (english, ko) in our_paths.items():
            kept.append([
                {"op": "test", "path": pointer, "value": english},
                {"op": "replace", "path": pointer, "value": ko},
            ])
            new_groups_total += 1
        overrides[patch_rel] = json.dumps(kept, ensure_ascii=False, indent=2).encode("utf-8")

    print("op-groups written (new + corrected):", new_groups_total)
    print("patch files created/updated:", len(overrides))

    if not overrides:
        print("nothing to write")
        return

    del base_pak

    n = pak_writer.write_pak(str(TARGET_PAK), str(TARGET_PAK), overrides)
    print("wrote", TARGET_PAK, "total entries:", n)


if __name__ == "__main__":
    main()
