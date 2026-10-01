"""Repack NonEKI with legacy + TM translations via surgical raw-text edits.

Instead of reserializing JSON (which broke Starbound structures last time),
this edits the raw UTF-8 text of each asset: a JSONC span parser locates the
exact string literal at each JSON pointer and only that literal is replaced.
All other bytes in the pak stay identical.
"""
import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT))
from pak import Pak
from jsonc_spans import parse_spans, navigate, _unescape

SRC_PAK = ROOT / "mods" / "NonEKI_9_FU_compat.pak"
WORK = ROOT / "translation" / "_archive" / "noneki-spanedit-20260922"
UNPACKED = WORK / "unpacked"
OUT_PAK = WORK / "NonEKI_9_FU_compat_translated.pak"
ALIGN = HERE / "alignment" / "noneki.tsv"
CLEAN = HERE / "data/cleaned_translation_targets.tsv"
NEW = HERE / "data/noneki_new_targets.tsv"
REPOINT = HERE / "data/noneki_repoint_targets.tsv"
MATCHED = {"patch-index-string", "patch-key-string", "pointer-string"}


def collect_targets():
    targets = {}
    with ALIGN.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["assetPath"].endswith(".patch"):
                # positional pairing is invalid inside patch documents (NonEKI_9
                # restructured them); repoint targets below cover these rows
                continue
            if row["status"] in MATCHED and row["currentPointer"]:
                targets[(row["assetPath"], row["currentPointer"])] = (
                    row["currentOriginal"], row["legacyKorean"], "legacy")
    with CLEAN.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            if row["sourceMod"] != "NonEKI" or row["category"] != "tm-single":
                continue
            key = (row["assetPath"], row["jsonPointer"])
            if key in targets and targets[key][1] != row["suggestedKorean"]:
                print("conflict:", key)
                continue
            targets[key] = (row["englishText"], row["suggestedKorean"], "tm-single")
    if REPOINT.exists():
        with REPOINT.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                key = (row["assetPath"], row["jsonPointer"])
                if key in targets and targets[key][1] != row["korean"]:
                    print("repoint-conflict:", key)
                targets[key] = (row["englishText"], row["korean"], "repoint")
    with NEW.open(encoding="utf-8-sig", newline="") as handle:
        for row in csv.DictReader(handle, delimiter="\t"):
            key = (row["assetPath"], row["jsonPointer"])
            if key in targets and targets[key][1] != row["korean"]:
                print("conflict:", key)
                continue
            targets[key] = (row["englishText"], row["korean"], "new")
    missed = HERE / "data/missed_noneki_targets.tsv"
    if missed.exists():
        with missed.open(encoding="utf-8-sig", newline="") as handle:
            for row in csv.DictReader(handle, delimiter="\t"):
                key = (row["assetPath"], row["jsonPointer"])
                if key in targets and targets[key][1] != row["koreanText"]:
                    print("missed-conflict:", key)
                    continue
                targets[key] = (row["englishText"], row["koreanText"], "missed")
    return targets


def main():
    WORK.mkdir(parents=True, exist_ok=True)
    targets = collect_targets()
    by_asset = defaultdict(list)
    for (asset, pointer), (orig, kor, src) in targets.items():
        by_asset[asset].append((pointer, orig, kor, src))
    print(f"targets: {len(targets)} strings in {len(by_asset)} assets")

    subprocess.run([str(ROOT / "win" / "asset_unpacker.exe"),
                    str(SRC_PAK), str(UNPACKED)], check=True)

    counts = Counter()
    for asset, edits in by_asset.items():
        rel = asset.lstrip("/")
        fpath = UNPACKED / rel
        if not fpath.exists():
            counts["asset-missing"] += len(edits)
            continue
        text = fpath.read_text(encoding="utf-8")
        try:
            root = parse_spans(text)
        except ValueError as e:
            counts[f"parse-failed:{asset}"] += len(edits)
            continue
        spans = []
        for pointer, orig, kor, src in edits:
            try:
                node = navigate(root, pointer)
            except (KeyError, IndexError, ValueError):
                counts["pointer-missing"] += 1
                continue
            if node.kind != "string":
                counts["not-a-string"] += 1
                continue
            literal = text[node.start:node.end]
            plain = _unescape(literal[1:-1])
            if plain.replace("\r\n", "\n") != orig.replace("\r\n", "\n"):
                counts["text-mismatch"] += 1
                continue
            if "\r\n" in plain:
                kor = kor.replace("\n", "\r\n")
            spans.append((node.start, node.end, kor, src))
        for start, end, kor, src in sorted(spans, key=lambda s: -s[0]):
            replacement = json.dumps(kor, ensure_ascii=False)
            text = text[:start] + replacement + text[end:]
            counts[f"applied-{src}"] += 1
        fpath.write_text(text, encoding="utf-8", newline="")

    subprocess.run([str(ROOT / "win" / "asset_packer.exe"),
                    str(UNPACKED), str(OUT_PAK), "-s"], check=True)

    # verify: every untouched asset byte-identical; every target resolves Korean
    old, new = Pak(str(SRC_PAK)), Pak(str(OUT_PAK))
    changed = set(by_asset)
    identical = sum(1 for p in old.index if p not in changed
                    and p in new.index and old.read(p) == new.read(p))
    missing_in_new = sum(1 for p in old.index if p not in new.index)
    print(json.dumps({**dict(counts),
                      "untouchedIdentical": identical,
                      "missingInNew": missing_in_new,
                      "oldAssets": len(old.index),
                      "newAssets": len(new.index)},
                     ensure_ascii=False))


if __name__ == "__main__":
    main()
