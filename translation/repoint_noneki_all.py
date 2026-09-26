#!/usr/bin/env python3
# Re-derive correct new-doc pointers for ALL legacy NonEKI .patch-asset rows.
# The original alignment paired strings positionally (same pointer), which is
# wrong wherever NonEKI_9 restructured the patch document. This script maps
# every legacy pointer to its semantic counterpart in the new document using
# op signatures (op, path, inverse) plus parent-element context scoring.
import csv, json, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pak import Pak
from align_merged_translations import parse_json

OLD_PAK = Path(r"E:\Desktop\mods\replaced-installed-20260921\NonEKI_5_FU_compat_intermediate.pak")
NEW_PAK = Path(r"E:\Desktop\mods\replaced-installed-20260921\noneki-spanedit-20260922\NonEKI_9_FU_compat_original.pak")
ALIGN = HERE / "alignment" / "noneki.tsv"
OUT = HERE / "repoint_noneki_all.tsv"
MATCHED = {"patch-index-string", "patch-key-string", "pointer-string"}


def node_at(doc, parts):
    n = doc
    for p in parts:
        n = n[int(p)] if isinstance(n, list) else n[p]
    return n


def split_op_pointer(doc, pointer):
    parts = pointer.lstrip("/").split("/")
    for cut in range(len(parts), 0, -1):
        try:
            node = node_at(doc, parts[:cut])
        except Exception:
            continue
        if isinstance(node, dict) and "op" in node:
            return parts[:cut], parts[cut:]
    return None, parts


def walk_ops(node, path, out):
    if isinstance(node, dict):
        if "op" in node:
            out.append((path, node))
            return
        for k, v in node.items():
            walk_ops(v, path + "/" + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_ops(v, f"{path}/{i}", out)


def sub_signature(so):
    return (so.get("op"), so.get("path"), bool(so.get("inverse")))


def parent_sig(doc, op_parts):
    pparts = op_parts[:-1]
    try:
        parent = node_at(doc, pparts) if pparts else doc
        if isinstance(parent, list):
            return Counter(sub_signature(so) for so in parent if isinstance(so, dict))
    except Exception:
        pass
    return Counter()


def main():
    old_pak, new_pak = Pak(str(OLD_PAK)), Pak(str(NEW_PAK))
    rows = [r for r in csv.DictReader(ALIGN.open(encoding="utf-8-sig", newline=""), delimiter="\t")
            if r["assetPath"].endswith(".patch")]
    new_docs, new_ops_cache = {}, {}

    out, stats = [], Counter()
    for r in rows:
        asset, lp, kor = r["assetPath"], r["legacyPointer"], r["legacyKorean"]
        status, new_pointer, new_english = "", "", ""
        if asset not in old_pak.index or asset not in new_pak.index:
            out.append((asset, lp, r["currentPointer"], "", kor, "asset-missing"))
            stats["asset-missing"] += 1
            continue
        old_doc = parse_json(old_pak.read(asset))
        if asset not in new_docs:
            new_docs[asset] = parse_json(new_pak.read(asset))
            ops = []
            walk_ops(new_docs[asset], "", ops)
            new_ops_cache[asset] = ops
        new_doc, new_ops = new_docs[asset], new_ops_cache[asset]

        op_parts, field_parts = split_op_pointer(old_doc, lp)
        if op_parts is None:
            out.append((asset, lp, r["currentPointer"], "", kor, "no-op-node"))
            stats["no-op-node"] += 1
            continue
        try:
            old_op_node = node_at(old_doc, op_parts)
            node_at(old_op_node, field_parts) if field_parts else old_op_node
        except Exception:
            out.append((asset, lp, r["currentPointer"], "", kor, "old-pointer-broken"))
            stats["old-pointer-broken"] += 1
            continue

        want_sub = sub_signature(old_op_node)
        if old_op_node.get("op") == "test":
            # never translate test values: a translated test can never match the
            # English base asset and would break the patch element
            out.append((asset, lp, r["currentPointer"], "", kor, "skip-test-op"))
            stats["skip-test-op"] += 1
            continue

        old_psig = parent_sig(old_doc, op_parts)
        cands = []
        for npath, nso in new_ops:
            if sub_signature(nso) != want_sub:
                continue
            try:
                nval = node_at(nso, field_parts) if field_parts else nso
            except Exception:
                continue
            if isinstance(nval, str):
                score = sum((old_psig & parent_sig(new_doc, npath.lstrip("/").split("/"))).values())
                cands.append((npath, nval, score))
        if not cands:
            status = "no-candidate"
            stats["no-candidate"] += 1
        elif len(cands) == 1:
            new_pointer = cands[0][0] + "/" + "/".join(field_parts)
            new_english = cands[0][1]
            status = "mapped"
            stats["mapped"] += 1
        else:
            best = max(c[2] for c in cands)
            tops = [c for c in cands if c[2] == best]
            if best > 0 and len(tops) == 1:
                new_pointer = tops[0][0] + "/" + "/".join(field_parts)
                new_english = tops[0][1]
                status = "mapped-by-context"
                stats["mapped-by-context"] += 1
            else:
                status = "ambiguous:" + "|".join(c[0] for c in cands)
                stats["ambiguous"] += 1
                new_english = " || ".join(c[1].replace("\n", " ") for c in cands)
        out.append((asset, lp, new_pointer or r["currentPointer"], new_english, kor, status))

    with open(OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(("assetPath", "legacyPointer", "newPointer", "newEnglish", "legacyKorean", "status"))
        w.writerows(out)
    print(dict(stats), "->", OUT)


if __name__ == "__main__":
    main()
