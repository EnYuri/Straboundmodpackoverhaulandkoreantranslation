#!/usr/bin/env python3
# Verify every missed_targets row resolves to Korean in the installed state:
#   GiC/ES/BA  -> an overlay .patch op exists for the effective pointer
#   NonEKI     -> installed pak doc contains Hangul at the pointer
import csv, json, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pak import Pak
from align_merged_translations import parse_json

HANGUL = re.compile(r"[가-힣]")
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
NONEKI = ROOT / "mods" / "NonEKI_9_FU_compat.pak"


def find_op_target(doc, ptr):
    """Resolve a patch-doc string pointer to (base asset path target, suffix)."""
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
    return find(doc, "")


def nav(doc, ptr):
    node = doc
    for part in ptr.strip("/").split("/"):
        if part == "":
            continue
        if isinstance(node, list):
            node = node[int(part)]
        elif isinstance(node, dict):
            node = node[part]
        else:
            return None
    return node


def main():
    rows = list(csv.DictReader(open(HERE / "data/missed_targets.tsv", encoding="utf-8-sig", newline=""), delimiter="\t"))
    counts = Counter()
    bad = []
    paks = {m: Pak(str(p)) for m, p in PAK.items()}
    overlay_cache = {}
    def overlay_ops(mod, asset):
        key = (mod, asset)
        if key not in overlay_cache:
            pf = OVERLAY_DIR[mod] / (asset.lstrip("/") + ".patch")
            ops = {}
            if pf.exists():
                for o in json.loads(pf.read_text(encoding="utf-8")):
                    if isinstance(o, dict) and "path" in o:
                        ops[o["path"]] = o.get("value")
            overlay_cache[key] = ops
        return overlay_cache[key]

    nk_pak = None
    nk_docs = {}

    for r in rows:
        mod, asset, ptr = r["sourceMod"], r["assetPath"], r["jsonPointer"]
        if mod == "NonEKI":
            if nk_pak is None:
                nk_pak = Pak(str(NONEKI))
            if asset not in nk_docs:
                nk_docs[asset] = parse_json(nk_pak.read(asset))
            doc = nk_docs[asset]
            # pointer inside patch doc: navigate to the op value
            val = nav(doc, ptr)
            if isinstance(val, str) and HANGUL.search(val):
                counts[("noneki-ok", mod)] += 1
            else:
                counts[("noneki-missing", mod)] += 1
                bad.append((mod, asset, ptr, repr(val)[:60]))
            continue

        if asset.endswith(".patch"):
            got = find_op_target(parse_json(paks[mod].read(asset)), ptr)
            if not got:
                counts[("unresolved", mod)] += 1
                bad.append((mod, asset, ptr, "unresolved"))
                continue
            base_path, suffix = got
            eff_ptr = base_path + suffix
            eff_asset = asset[:-len(".patch")]
        else:
            eff_ptr, eff_asset = ptr, asset

        val = overlay_ops(mod, eff_asset).get(eff_ptr)
        if isinstance(val, str) and HANGUL.search(val):
            counts[("overlay-ok", mod)] += 1
        else:
            counts[("overlay-missing", mod)] += 1
            bad.append((mod, eff_asset, eff_ptr, repr(val)[:60]))

    for k, v in sorted(counts.items()):
        print(k, v)
    if bad:
        with open(HERE / "data/verify_missed_bad.tsv", "w", encoding="utf-8", newline="") as fh:
            w = csv.writer(fh, delimiter="\t")
            w.writerows(bad)
        print("bad rows -> verify_missed_bad.tsv")
        for b in bad[:20]:
            print(b)


if __name__ == "__main__":
    main()
