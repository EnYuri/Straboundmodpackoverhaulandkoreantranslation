# -*- coding: utf-8 -*-
"""Apply approved name-consistency fixes into female_translation.pak.REVIEW_PENDING.

Reads name_fix_proposals.tsv; takes rows whose method is WORD/TSPAN/VARIANT
(automatic-span replacements produced by propose_name_fixes.py) where the
proposed text differs from the current one. For each (asset, pointer) the
latest replace op wins: existing patch ops touching that pointer are dropped
and a single trailing {"op":"replace"} op is appended, mirroring the
bare-replace convention already used by this pak. Rows originating from other
translation paks (FU_KO / sbkor) are folded into the same patch path inside
this pak, which loads after them so the unified term still wins.

A structural gate re-checks each proposal before writing: tag sequence,
newline count and <placeholder>/<...> counts must match the old text.
"""
import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
TARGET_PAK = BASE / "backup_paks/female_translation.pak.REVIEW_PENDING"
PROPOSALS = BASE / "data/name_fix_proposals.tsv"
MANUAL = BASE / "data/manual_name_fixes.tsv"
REPORT = BASE / "data/name_fixes_applied.tsv"

sys.path.insert(0, str(BASE.parents[1]))
sys.path.insert(0, str(BASE))
import pak_writer  # noqa: E402
import propose_name_fixes as P  # noqa: E402
from pak import Pak  # noqa: E402

TAG_RE = re.compile(r"\^[A-Za-z0-9#]*;")
PH_RE = re.compile(r"<[^>\s]+>|\{[^}\s]*\}|%\w|%s")


def struct_ok(old, new, allow_tag_change=False):
    if old == new:
        return False
    if not new:
        return False
    if old.count("\n") != new.count("\n"):
        return False
    if not allow_tag_change:
        if Counter(TAG_RE.findall(old)) != Counter(TAG_RE.findall(new)):
            return False
    if Counter(PH_RE.findall(old)) != Counter(PH_RE.findall(new)):
        return False
    return True


def variant_replace(ko, variant, canon):
    """Re-run a VARIANT replacement on text `ko` (same rules as the
    proposer): first word-bounded occurrence of `variant` -> `canon`,
    then repair the following particle. Existing canonical text is
    masked so a variant inside it ('노획한 나노 리셉터클' contains
    '나노 리셉터클') is never matched."""
    MASK = "\x00"
    masked = canon != variant and canon in ko
    work = ko.replace(canon, MASK) if masked else ko
    clean, cmap = P.clean_with_map(work)
    start = 0
    while True:
        pos = clean.find(variant, start)
        if pos < 0:
            return None
        nxt = clean[pos + len(variant):pos + len(variant) + 1]
        prev = clean[pos - 1:pos]
        if prev and prev in "-/·_":
            start = pos + 1       # inside a longer compound ('인스타-프로이트')
            continue
        if (not prev or not ("가" <= prev <= "힣")) and \
                (not nxt or not ("가" <= nxt <= "힣")
                 or any(nxt == p[:1] for p in P.PARTICLES)):
            rs = cmap[pos]
            re_ = P.raw_end(cmap, pos + len(variant))
            new = work[:rs] + canon + work[re_:]
            new = P.repair_following_particle(new, rs + len(canon), canon)
            return new.replace(MASK, canon) if masked else new
        start = pos + 1


def chain_pointer(base_ko, rows):
    """Apply every approved name fix for one pointer sequentially.
    VARIANT first (exact substring), then TSPAN, then WORD - recomputed
    against the evolving text so each fix sees the current wording."""
    out = base_ko
    applied = []
    order = {"MANUAL": 0, "VARIANT": 1, "TSPAN": 2, "WORD": 3}
    for r in sorted(rows, key=lambda x: order.get(x["method"], 4)):
        canon = r["canonical"]
        if r["method"] != "MANUAL":
            canon = canon.strip().rstrip(".!?…")
            if not canon:
                continue
        if r["method"] == "MANUAL":
            if r["old_span"] and r["old_span"] in out:
                out = out.replace(r["old_span"], canon)
                applied.append(r)
            continue
        if r["method"] == "VARIANT":
            res = variant_replace(out, r["old_span"], canon)
            if res:
                out = res
                applied.append(r)
                # the same variant can occur twice in one pointer
                # ('팝톱을 놀래킨 적이 있다! 팝탑은 ...') - keep replacing,
                # unless the variant is inside the canon itself (would loop)
                if r["old_span"].replace(" ", "") not in canon.replace(" ", ""):
                    while True:
                        res = variant_replace(out, r["old_span"], canon)
                        if not res:
                            break
                        out = res
            continue
        if canon in out:
            # canonical already present (earlier chain step or duplicate
            # flag) - another TSPAN/WORD pass would double-insert it
            continue
        method, sim, span, new = P.propose_missing(out, canon)
        if method != "NONE" and new != out:
            out = new
            applied.append(r)
    # a canon token carrying its own particle ('경비병에게') can replace only
    # the stem of a word, leaving the original particle dangling right after
    # it - '에게에게' is never valid, collapse the duplicated particle
    out = re.sub(r"(에게|에서는|에서|으로|부터|까지|처럼|보다|조차|마저)\1",
                 r"\1", out)
    return out, applied


def main():
    rows = []
    with open(PROPOSALS, encoding="utf-8-sig", newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            rows.append(r)

    auto = [r for r in rows
            if r["method"] in ("WORD", "TSPAN", "VARIANT")
            and r["new_ko"] and r["new_ko"] != r["korean"]]

    # group by (asset, pointer); chain fixes for multi-name pointers
    groups = {}
    for r in auto:
        groups.setdefault((r["asset"], r["pointer"]), []).append(r)

    # verbatim manual overrides (asset, pointer, find, replace) - useful
    # for reorder fixes the aligner refuses, e.g. title suffix/prefix swaps
    manual_rows = []
    if MANUAL.exists():
        with open(MANUAL, encoding="utf-8-sig", newline="") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                manual_rows.append({"pak": "manual", "asset": r["asset"],
                                    "pointer": r["pointer"],
                                    "en_name": "(manual)",
                                    "canonical": r["replace"],
                                    "method": "MANUAL", "sim": "",
                                    "old_span": r["find"],
                                    "korean": r["korean"], "new_ko": ""})
    for r in manual_rows:
        groups.setdefault((r["asset"], r["pointer"]), []).append(r)

    target = {}
    rejected = 0
    for key, grows in groups.items():
        base_ko = grows[0]["korean"]
        final, applied = chain_pointer(base_ko, grows)
        # pure-manual groups may legitimately repair broken colour tags
        manual_only = all(r["method"] == "MANUAL" for r in applied)
        if not applied or not struct_ok(base_ko, final,
                                        allow_tag_change=manual_only):
            rejected += len(grows)
            continue
        rec = dict(applied[-1])
        rec["new_ko"] = final
        rec["chained"] = str(len(applied))
        target[key] = rec

    print("pointers targeted:", len(groups), "| applied:", len(target),
          "| struct/chain-rejected rows:", rejected)
    by_method = Counter(r["method"] for r in target.values())
    by_srcpak = Counter(r["pak"] for r in target.values())
    multi = sum(1 for r in target.values() if int(r["chained"]) > 1)
    print("methods:", dict(by_method), "| multi-name pointers:", multi)
    print("source paks:", dict(by_srcpak))

    base_pak = Pak(str(TARGET_PAK))
    by_asset = {}
    for (asset, pointer), r in target.items():
        by_asset.setdefault(asset, {})[pointer] = r["new_ko"]

    overrides = {}
    patch_missing = 0
    for asset, ptr_map in by_asset.items():
        if asset in base_pak.index:
            existing = json.loads(base_pak.read(asset).decode("utf-8-sig"))
        else:
            patch_missing += 1
            existing = []

        def touches(item):
            ops = item if isinstance(item, list) else [item]
            flat = []
            for op in ops:
                flat += op if isinstance(op, list) else [op]
            return any(isinstance(op, dict) and op.get("path") in ptr_map
                       for op in flat)

        kept = [g for g in existing if not touches(g)]
        for pointer, ko in ptr_map.items():
            kept.append({"op": "replace", "path": pointer, "value": ko})
        overrides[asset] = json.dumps(kept, ensure_ascii=False,
                                      separators=(",", ":")).encode("utf-8")

    print("patch files touched:", len(overrides),
          "| new patch files:", patch_missing)
    del base_pak

    n = pak_writer.write_pak(str(TARGET_PAK), str(TARGET_PAK), overrides)
    print("wrote", TARGET_PAK.name, "entries:", n)

    with open(REPORT, "w", encoding="utf-8-sig", newline="") as f:
        w = csv.writer(f, delimiter="\t")
        w.writerow(["pak", "asset", "pointer", "en_name", "canonical",
                    "method", "sim", "old_span", "old_korean", "new_ko",
                    "chained"])
        for r in target.values():
            w.writerow([r["pak"], r["asset"], r["pointer"], r["en_name"],
                        r["canonical"], r["method"], r["sim"], r["old_span"],
                        r["korean"], r["new_ko"], r.get("chained", "1")])
    print("wrote", REPORT.name)

    # verify: every touched pointer's last op equals the new value
    verify = Pak(str(TARGET_PAK))
    bad = 0
    for (asset, pointer), r in list(target.items()):
        ops = json.loads(verify.read(asset).decode("utf-8-sig"))
        val = None
        for item in ops:
            for op in (item if isinstance(item, list) else [item]):
                if not isinstance(op, dict):
                    continue
                if op.get("path") == pointer and op.get("op") == "replace":
                    val = op["value"]
        if val != r["new_ko"]:
            bad += 1
            if bad < 8:
                print("MISMATCH:", asset, pointer, repr((val or "")[:60]))
    print("verify mismatches:", bad, "of", len(target))


if __name__ == "__main__":
    main()
