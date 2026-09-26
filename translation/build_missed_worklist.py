#!/usr/bin/env python3
# Build a worklist of translatable strings the original inventory missed
# (array-of-strings fields like converse/contentPages/wakeUp, and patch-op
# values with non-visible leaf keys or array/object values).
import csv, json, re, sys
from collections import Counter
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(HERE))
from pak import Pak
from align_merged_translations import parse_json

HANGUL = re.compile(r"[가-힣]")
BAD_DIR = re.compile(r"/(UNUSED|LEGACY|DEPRECATED|SCRAPPED)/", re.I)
EXTS = (".activeitem", ".animation", ".cinematic", ".codex", ".config",
        ".consumable", ".item", ".liquid", ".liqitem", ".matitem",
        ".monstertype", ".npctype", ".object", ".projectile",
        ".questtemplate", ".recipe", ".species", ".stagehand",
        ".statuseffect", ".tech", ".tenant", ".tooltip", ".vehicle",
        ".weather", ".radiomessages", ".aimission", ".patch")

PARK = {
    "GiC": "mods/Galaxy_in_Conflict_contents_2754886445.pak",
    "Extended Story": "mods/Extended_Story_contents_899795176.pak",
    "Black Armory": "mods/Black_Armory_4.2.5_FU_NEKI_compat.pak",
}
NONEKI = "mods/NonEKI_9_FU_compat.pak"
DEAD_PATCH_BASES = {"/interface/cockpit/cockpit.config-old"}  # no base asset exists

# leaf keys that are never display text
NON_TEXT_LEAF = re.compile(
    r"(image|icon|path|file|sound|music|script|name|id|type|projectile|item|"
    r"liquid|material|block|dungeon|quest|mission|recipe|tenant|pool|table|"
    r"frames?|palette|color|status|effect|animation|particle|emitter|slot|"
    r"parameter|key|flag|tag)$", re.I)


def is_text(v):
    t = v.strip() if isinstance(v, str) else ""
    if len(t) < 4 or HANGUL.search(t) or " " not in t:
        return False
    if not re.search(r"[a-zA-Z]", t) or t.startswith(("/", "~", "?")):
        return False
    return True


def walk(node, path, out):
    if isinstance(node, dict):
        for k, v in node.items():
            walk(v, path + "/" + k, out)
    elif isinstance(node, list):
        for i, v in enumerate(node):
            walk(v, f"{path}/{i}", out)
    elif isinstance(node, str):
        out.append((path, node))


def main():
    known = set()
    for fn in ("cleaned_translation_targets.tsv", "excluded_candidates.tsv"):
        for r in csv.DictReader(open(HERE / fn, encoding="utf-8-sig", newline=""), delimiter="\t"):
            known.add((r["sourceMod"], r["assetPath"], r["jsonPointer"]))

    rows = []  # (mod, assetPath, pointer, english)
    for mod, pakpath in PARK.items():
        pak = Pak(str(ROOT / pakpath))
        for a in pak.index:
            if not a.endswith(EXTS) or BAD_DIR.search(a):
                continue
            try:
                doc = parse_json(pak.read(a))
            except Exception:
                continue
            strs = []
            walk(doc, "", strs)
            # for .patch docs, skip strings inside test ops
            test_spans = set()
            if a.endswith(".patch"):
                def find_tests(n, pth):
                    if isinstance(n, dict):
                        if n.get("op") == "test":
                            test_spans.add(pth)
                        for k, v in n.items():
                            find_tests(v, pth + "/" + k)
                    elif isinstance(n, list):
                        for i, v in enumerate(n):
                            find_tests(v, f"{pth}/{i}")
                find_tests(doc, "")
            for p, v in strs:
                if not is_text(v):
                    continue
                if (mod, a, p) in known:
                    continue
                if a.endswith(".patch"):
                    if any(p.startswith(ts + "/") or p == ts for ts in test_spans):
                        continue
                    leaf = p.rstrip("/").split("/")[-1]
                    if NON_TEXT_LEAF.search(leaf):
                        continue
                rows.append((mod, a, p, v))

    # NonEKI: scan the ORIGINAL doc via installed pak (same pointers); skip
    # test ops and dead patches
    nk = Pak(str(ROOT / NONEKI))
    for a in nk.index:
        if not a.endswith(".patch"):
            continue
        if a[:-len(".patch")] in DEAD_PATCH_BASES:
            continue
        try:
            doc = parse_json(nk.read(a))
        except Exception:
            continue
        strs = []
        walk(doc, "", strs)
        test_spans = set()
        def find_tests(n, pth):
            if isinstance(n, dict):
                if n.get("op") == "test":
                    test_spans.add(pth)
                for k, v in n.items():
                    find_tests(v, pth + "/" + k)
            elif isinstance(n, list):
                for i, v in enumerate(n):
                    find_tests(v, f"{pth}/{i}")
        find_tests(doc, "")
        for p, v in strs:
            if not is_text(v):
                continue
            if any(p.startswith(ts + "/") or p == ts for ts in test_spans):
                continue
            leaf = p.rstrip("/").split("/")[-1]
            if NON_TEXT_LEAF.search(leaf):
                continue
            rows.append(("NonEKI", a, p, v))

    # global dedupe by normalized english (keep all pointer rows, first wins
    # for the worklist id assignment)
    uniq = {}
    for m, a, p, v in rows:
        key = v.strip().replace("\r\n", "\n")
        uniq.setdefault(key, []).append((m, a, p, v))
    freq = sorted(uniq.items(), key=lambda kv: -len(kv[1]))
    with open(HERE / "missed_targets.tsv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(("sourceMod", "assetPath", "jsonPointer", "englishText", "inPatchAsset"))
        for eng, lst in freq:
            for m, a, p, v in lst:
                w.writerow((m, a, p, v, "1" if a.endswith(".patch") else "0"))
    with open(HERE / "missed_worklist.tsv", "w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t", lineterminator="\n")
        w.writerow(("id", "count", "englishText"))
        for i, (eng, lst) in enumerate(freq):
            w.writerow((i, len(lst), eng))
    print("rows:", len(rows), "unique:", len(freq), dict(Counter(m for m, a, p, v in rows)))


if __name__ == "__main__":
    main()
