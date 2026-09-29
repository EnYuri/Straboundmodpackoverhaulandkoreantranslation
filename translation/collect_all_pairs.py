"""Extract every EN/KO translation pair from ALL active translation paks.

Unlike extract_pak_pairs.py, this also resolves 'flat' ops (replace/add with
no preceding test) by reading the EN original from the base asset provided by
some other pak. This closes the flat-patch blind spot noted in batch_log
(~6% of .patch docs are flat; for name fields they are the majority).

Output: all_pairs.tsv  (pak, asset, pointer, op, english, korean)
  - english may be empty when the flat op's base value could not be resolved
    (field added by the patch itself, pointer missing in base, etc.)
"""
import csv
import json
import re
import sys
from pathlib import Path

BASE = Path(__file__).parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak  # noqa: E402
from jsonc_spans import parse_spans, navigate, _unescape  # noqa: E402

KO = re.compile(r"[가-힣]")

# patch paks carrying Korean, in assumed application order (earlier first).
# female_translation already absorbed the merged sbkor/FU_KO content but the
# originals are still in mods/; keep both, dedupe at report level.
TRANS_PAKS = [
    "-9998_trans_sbkor_0.98_structfix.pak",
    "FU_KO_contents_3166424163.pak",
    "female_translation.pak",
    "zz_localeko_highpriority_20260927.pak",
]
TRANS_SET = set(TRANS_PAKS)

MODS = STAR / "mods"

# ---------------- provider index ----------------

def build_provider_index():
    """asset path -> list of provider pak names (sorted ascending).

    Pak objects are opened lazily later; keeping 800 index dicts alive at
    once costs ~10 GB, so only the name list is retained here.
    """
    idx = {}
    paks = [p for p in MODS.iterdir() if p.suffix == ".pak"]
    paks.append(STAR / "assets" / "packed.pak")
    for p in paks:
        try:
            pk = Pak(str(p))
        except Exception:
            continue
        for a in pk.index:
            idx.setdefault(a, []).append(p.name)
        del pk
    return idx

PROVIDERS = {}       # pak name -> Pak, opened lazily
_MISS = object()


def get_pak(pname):
    pk = PROVIDERS.get(pname)
    if pk is None:
        path = MODS / pname
        if not path.exists():
            path = STAR / "assets" / pname
        pk = Pak(str(path))
        PROVIDERS[pname] = pk
    return pk


# ---------------- op collection ----------------

def collect_pak(pname):
    pak = Pak(str(MODS / pname))
    rows = []
    flat_assets = {}   # asset -> parsed patch doc list of (path, op, en, ko)
    for asset in pak.index:
        if not asset.endswith(".patch"):
            continue
        try:
            doc = json.loads(pak.read(asset))
        except Exception:
            continue
        if not isinstance(doc, list):
            continue
        tested = {}
        stack = list(reversed(doc))
        while stack:
            op = stack.pop()
            if isinstance(op, list):
                stack.extend(reversed(op))
                continue
            if not isinstance(op, dict):
                continue
            o, p, v = op.get("op"), op.get("path"), op.get("value")
            if o == "test" and isinstance(v, str):
                tested[p] = v
            elif o in ("replace", "add") and isinstance(v, str) and KO.search(v):
                en = tested.pop(p, None)
                rows.append([pname, asset, p, o, en, v])
                if en is None:
                    flat_assets.setdefault(asset, None)
    return rows, flat_assets


def main():
    global PROVIDER_INDEX
    print("building provider index over all paks...")
    PROVIDER_INDEX = build_provider_index()
    print("providers:", len(PROVIDERS), "indexed assets:", len(PROVIDER_INDEX))

    all_rows = []
    flat_needed = {}   # asset_base -> set(pointers)  for EN resolution
    for pname in TRANS_PAKS:
        rows, flat = collect_pak(pname)
        n_paired = sum(1 for r in rows if r[4] is not None)
        print(f"{pname}: {len(rows)} ko ops ({n_paired} paired, {len(rows)-n_paired} flat)")
        all_rows.extend(rows)
        for r in rows:
            if r[4] is None:
                flat_needed.setdefault(r[1][:-6], set()).add(r[2])  # strip .patch

    # resolve flat ops, grouped per base asset so each provider doc is parsed
    # once and can be evicted immediately (node trees are heavy)
    print("resolving flat ops against base assets:", len(flat_needed), "assets")
    resolved = unresolved = 0
    cache_ptr = {}     # (asset_base, pointer) -> en or None
    for i, (asset_base, pointers) in enumerate(flat_needed.items()):
        if i % 2000 == 0:
            print(f"  {i}/{len(flat_needed)} ...", flush=True)
        for pname in sorted(PROVIDER_INDEX.get(asset_base, []), reverse=True):
            if pname in TRANS_SET:
                continue
            key = (pname, asset_base)
            try:
                text = get_pak(pname).read(asset_base).decode("utf-8")
                node = parse_spans(text)
            except Exception:
                continue
            remaining = [p for p in pointers if cache_ptr.get((asset_base, p), _MISS) is _MISS]
            for p in remaining:
                try:
                    sub = navigate(node, p)
                except Exception:
                    continue
                if sub.kind != "string":
                    cache_ptr[(asset_base, p)] = None
                    continue
                val = _unescape(text[sub.start + 1:sub.end - 1])
                if KO.search(val):
                    continue  # baked-translation provider; keep digging
                cache_ptr[(asset_base, p)] = val
            if all(cache_ptr.get((asset_base, p), _MISS) is not _MISS for p in pointers):
                break
        for p in pointers:
            cache_ptr.setdefault((asset_base, p), None)

    for r in all_rows:
        if r[4] is None:
            en = cache_ptr.get((r[1][:-6], r[2]))
            if en is not None:
                r[4] = en
                resolved += 1
            else:
                unresolved += 1
    print("flat resolved:", resolved, "unresolved:", unresolved)

    with (BASE / "all_pairs.tsv").open("w", encoding="utf-8-sig", newline="") as fh:
        w = csv.writer(fh, delimiter="\t")
        w.writerow(["pak", "asset", "pointer", "op", "english", "korean"])
        for r in all_rows:
            w.writerow([r[0], r[1], r[2], r[3], r[4] or "", r[5]])
    print("wrote all_pairs.tsv:", len(all_rows), "rows")


if __name__ == "__main__":
    main()
