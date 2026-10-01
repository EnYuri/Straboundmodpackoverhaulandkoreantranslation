"""Build the new-translation worklist: unique English strings across mods."""
import csv
import re
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
CLEAN = HERE / "data/cleaned_translation_targets.tsv"
MARKUP = re.compile(r"\^(?:#[0-9a-fA-F]{3,8}|[a-zA-Z]+);?")


def norm(s):
    return " ".join(MARKUP.sub("", s).lower().split())


def main():
    tm = defaultdict(set)
    for f, kc in (("data/translation_memory.tsv", "existingKorean"),
                  ("data/legacy_translation_memory.tsv", "legacyKorean")):
        with (HERE / f).open(encoding="utf-8-sig", newline="") as h:
            for r in csv.DictReader(h, delimiter="\t"):
                tm[norm(r["currentOriginal"])].add(r[kc])

    rows = [r for r in csv.DictReader(
            CLEAN.open(encoding="utf-8-sig", newline=""), delimiter="\t")
            if r["category"] == "new-translation"]

    strings = defaultdict(lambda: {"count": 0, "locs": [], "mods": set()})
    for r in rows:
        e = r["englishText"]
        s = strings[e]
        s["count"] += 1
        s["mods"].add(r["sourceMod"])
        if len(s["locs"]) < 3:
            s["locs"].append(f'{r["sourceMod"]}:{r["assetPath"]}#{r["jsonPointer"]}')

    out = HERE / "data/worklist_new.tsv"
    with out.open("w", encoding="utf-8-sig", newline="") as h:
        w = csv.writer(h, delimiter="\t", lineterminator="\n")
        w.writerow(["englishText", "occurrences", "mods", "exampleLocations",
                    "tmSuggestion", "korean"])
        for e, s in sorted(strings.items(), key=lambda kv: (-kv[1]["count"], kv[0])):
            sug = tm.get(norm(e), set())
            w.writerow([e, s["count"], "|".join(sorted(s["mods"])),
                        " | ".join(s["locs"]),
                        next(iter(sug)) if len(sug) == 1 else "", ""])
    print(f"unique strings: {len(strings)}, rows: {len(rows)}")


if __name__ == "__main__":
    main()
