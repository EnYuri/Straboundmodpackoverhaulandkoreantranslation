#!/usr/bin/env python3
# Repoint legacy NonEKI translations whose pointers moved between the old
# (NonEKI_5 intermediate) and current (NonEKI_9) patch documents.
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
OUT = HERE / "repoint_noneki.tsv"


def node_at(doc, parts):
    n = doc
    for p in parts:
        n = n[int(p)] if isinstance(n, list) else n[p]
    return n


def split_op_pointer(doc, pointer):
    """Split a pointer into (op-node path, field path) where the op node is the
    deepest ancestor dict containing an 'op' key."""
    parts = pointer.lstrip("/").split("/")
    for cut in range(len(parts), 0, -1):
        try:
            node = node_at(doc, parts[:cut])
        except Exception:
            continue
        if isinstance(node, dict) and "op" in node:
            return parts[:cut], parts[cut:]
    return None, parts


def walk_strings(node, path, out):
    if isinstance(node, dict):
        if "op" in node:
            out.append((path, node))
            return
        for k, v in node.items():
            walk_strings(v, path + "/" + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk_strings(v, f"{path}/{i}", out)


def sub_signature(so):
    return (so.get("op"), so.get("path"), bool(so.get("inverse")))


def main():
    old_pak, new_pak = Pak(str(OLD_PAK)), Pak(str(NEW_PAK))
    rows = [r for r in csv.DictReader(open(HERE / "unresolved_triage.tsv", encoding="utf-8-sig"), delimiter="\t")
            if r["triage"] == "pointer-moved-needs-manual-relocation" and r["sourceMod"] == "NonEKI"]

    out, stats = [], Counter()
    for r in rows:
        asset, lp, kor = r["assetPath"], r["legacyPointer"], r["legacyKorean"]
        status, new_pointer = "", ""
        if asset not in old_pak.index or asset not in new_pak.index:
            out.append((asset, lp, "", kor, "asset-missing")); stats["asset-missing"] += 1; continue
        old_doc = parse_json(old_pak.read(asset))
        new_doc = parse_json(new_pak.read(asset))
        op_parts, field_parts = split_op_pointer(old_doc, lp)
        if op_parts is None:
            out.append((asset, lp, "", kor, "no-op-node")); stats["no-op-node"] += 1; continue
        try:
            old_op_node = node_at(old_doc, op_parts)
            old_val = node_at(old_op_node, field_parts) if field_parts else old_op_node
        except Exception:
            out.append((asset, lp, "", kor, "old-pointer-broken")); stats["old-pointer-broken"] += 1; continue
        field = "/" + "/".join(field_parts)
        want_sub = sub_signature(old_op_node)

        # signature of the old parent element (the top-level op list containing
        # the op node) used to disambiguate same-signature candidates
        old_parent_parts = op_parts[:-1]
        try:
            old_parent = node_at(old_doc, old_parent_parts) if old_parent_parts else old_doc
            old_parent_sig = Counter(
                sub_signature(so) for so in old_parent if isinstance(so, dict)) \
                if isinstance(old_parent, list) else Counter()
        except Exception:
            old_parent_sig = Counter()

        # collect candidate op nodes in the new doc
        cands = []
        new_ops = []
        walk_strings(new_doc, "", new_ops)
        for npath, nso in new_ops:
            if sub_signature(nso) != want_sub:
                continue
            try:
                nval = node_at(nso, field_parts) if field_parts else nso
            except Exception:
                continue
            if isinstance(nval, str):
                cands.append((npath, nval))
        if len(cands) == 1:
            new_pointer = cands[0][0] + field
            status = "mapped"
            stats["mapped"] += 1
        elif not cands:
            status = "no-candidate"; stats["no-candidate"] += 1
        else:
            # score each candidate by parent-element signature overlap
            best, best_score = None, -1
            for npath, nval in cands:
                pparts = npath.lstrip("/").split("/")[:-1]
                try:
                    nparent = node_at(new_doc, pparts) if pparts else new_doc
                    nsig = Counter(sub_signature(so) for so in nparent
                                   if isinstance(so, dict)) if isinstance(nparent, list) else Counter()
                except Exception:
                    nsig = Counter()
                score = sum((old_parent_sig & nsig).values())
                if score > best_score:
                    best, best_score = npath, score
            tied = [npath for npath, _ in cands if npath != best and True]
            if best is not None and best_score > 0:
                others = []
                for npath, nval in cands:
                    pparts = npath.lstrip("/").split("/")[:-1]
                    try:
                        nparent = node_at(new_doc, pparts) if pparts else new_doc
                        nsig = Counter(sub_signature(so) for so in nparent
                                       if isinstance(so, dict)) if isinstance(nparent, list) else Counter()
                    except Exception:
                        nsig = Counter()
                    if sum((old_parent_sig & nsig).values()) == best_score:
                        others.append(npath)
                if len(others) == 1:
                    new_pointer = best + field
                    status = "mapped-by-context"
                    stats["mapped-by-context"] += 1
                else:
                    status = "ambiguous:" + "|".join(c[0] for c in cands)
                    stats["ambiguous"] += 1
            else:
                status = "ambiguous:" + "|".join(c[0] for c in cands)
                stats["ambiguous"] += 1
        out.append((asset, lp, new_pointer, kor, status))

    with open(OUT, "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(("assetPath", "legacyPointer", "newPointer", "legacyKorean", "status"))
        w.writerows(out)
    print(dict(stats), "->", OUT)


if __name__ == "__main__":
    main()
