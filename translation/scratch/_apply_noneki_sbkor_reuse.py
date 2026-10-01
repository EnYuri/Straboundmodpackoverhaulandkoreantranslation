import csv
import json
import sys
from pathlib import Path

STAR = Path(r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, str(STAR))
from pak import Pak  # noqa: E402

HERE = Path(__file__).parent.parent
SRC_PAK = STAR / "mods" / "NonEKI_9_FU_compat.pak"
OUT_PAK = HERE / "NonEKI_9_FU_compat.pak.NEW1"

rows = []
with open(HERE / "archive/noneki_sbkor_reuse.tsv", encoding="utf-8-sig", newline="") as f:
    r = csv.DictReader(f, delimiter="\t")
    for row in r:
        rows.append(row)

GLOSSARY_FIXUP = {
    "지식부 요새": "미니크녹 요새",
}


def apply_glossary(s):
    for old, new in GLOSSARY_FIXUP.items():
        s = s.replace(old, new)
    return s


targets = {}
for row in rows:
    key = (row["asset"], row["pointer"])
    new_val = apply_glossary(row["sbkor_korean"])
    targets[key] = (row["current_korean"], new_val)

print("targets:", len(targets))

src = Pak(str(SRC_PAK))
files = {name: src.read(name) for name in src.index}

by_asset = {}
for (asset, ptr), (old, new) in targets.items():
    by_asset.setdefault(asset, []).append((ptr, old, new))


def set_at(doc, pointer, new_value):
    parts = pointer.lstrip("/").split("/")
    cur = doc
    for part in parts[:-1]:
        cur = cur[int(part)] if isinstance(cur, list) else cur[part]
    last = parts[-1]
    if isinstance(cur, list):
        cur[int(last)] = new_value
    else:
        cur[last] = new_value


def apply_replace_op(op, ptr, old, new, asset, mismatches):
    """op is a {"op":"replace","path":...,"value":...} dict. ptr may equal
    op['path'] exactly, or be a deeper pointer into a nested op['value']."""
    base_path = op.get("path")
    if ptr == base_path:
        if op.get("value") != old:
            mismatches.append((asset, ptr, "value-differs"))
            return False
        op["value"] = new
        return True
    if not ptr.startswith(base_path):
        return None  # not this op
    sub = ptr[len(base_path):]
    try:
        cur = op["value"]
        subparts = sub.lstrip("/").split("/")
        for part in subparts[:-1]:
            cur = cur[int(part)] if isinstance(cur, list) else cur[part]
        last = subparts[-1]
        cur_val = cur[int(last)] if isinstance(cur, list) else cur[last]
        if cur_val != old:
            mismatches.append((asset, ptr, "value-differs"))
            return False
        if isinstance(cur, list):
            cur[int(last)] = new
        else:
            cur[last] = new
        return True
    except Exception as e:
        mismatches.append((asset, ptr, f"nav-fail:{e}"))
        return False


assets_changed = 0
mismatches = []
for asset, edits in by_asset.items():
    data = files[asset]
    doc = json.loads(data)
    changed = False
    is_nested = isinstance(doc, list) and doc and all(isinstance(g, list) for g in doc)
    for ptr, old, new in edits:
        found = False
        if is_nested:
            for group in doc:
                for op in group:
                    if isinstance(op, dict) and op.get("op") == "replace" and isinstance(op.get("path"), str) \
                            and (ptr == op["path"] or ptr.startswith(op["path"])):
                        result = apply_replace_op(op, ptr, old, new, asset, mismatches)
                        if result is not None:
                            found = True
                            changed = changed or result
        else:
            for op in doc:
                if isinstance(op, dict) and op.get("op") == "replace" and isinstance(op.get("path"), str) \
                        and (ptr == op["path"] or ptr.startswith(op["path"])):
                    result = apply_replace_op(op, ptr, old, new, asset, mismatches)
                    if result is not None:
                        found = True
                        changed = changed or result
        if not found:
            mismatches.append((asset, ptr, "not-found"))
    if changed:
        files[asset] = json.dumps(doc, ensure_ascii=False).encode("utf-8")
        assets_changed += 1

print("assets changed:", assets_changed)
print("mismatches:", len(mismatches))
for m in mismatches:
    print("MISMATCH", m)

# repack using same SBAsset6 writer approach
import struct


def _vlqr(buf, p):
    v = 0
    while True:
        b = buf[p]
        p += 1
        v = (v << 7) | (b & 0x7F)
        if not (b & 0x80):
            return v, p


def vlq(v):
    stack = []
    while True:
        stack.append(v & 0x7F)
        v >>= 7
        if not v:
            break
    out = bytearray()
    for i, b in enumerate(reversed(stack)):
        out.append(b | 0x80 if i < len(stack) - 1 else b)
    return bytes(out)


def _key(buf, p):
    n, p = _vlqr(buf, p)
    return buf[p:p + n].decode("utf-8"), p + n


def _rjson_skip(buf, p):
    t = buf[p]
    p += 1
    if t == 0x01:
        return p
    if t == 0x02:
        return p + 8
    if t == 0x03:
        return p + 1
    if t == 0x04:
        _, p = _vlqr(buf, p)
        return p
    if t == 0x05:
        n, p = _vlqr(buf, p)
        return p + n
    if t == 0x06:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            p = _rjson_skip(buf, p)
        return p
    if t == 0x07:
        n, p = _vlqr(buf, p)
        for _ in range(n):
            _, p = _key(buf, p)
            p = _rjson_skip(buf, p)
        return p
    raise ValueError("unknown json type %r at %d" % (t, p))


d0 = SRC_PAK.read_bytes()
off0 = struct.unpack(">Q", d0[8:16])[0]
assert d0[off0:off0 + 5] == b"INDEX"
p = off0 + 5
nmeta, p = _vlqr(d0, p)
for _ in range(nmeta):
    _, p = _key(d0, p)
    p = _rjson_skip(d0, p)
meta_blob = d0[off0:p]

buf = bytearray(b"SBAsset6" + b"\x00" * 8)
index_entries = []
for name in sorted(files):
    data = files[name]
    off = len(buf)
    buf += data
    index_entries.append((name.encode("utf-8"), off, len(data)))

index_off = len(buf)
buf += meta_blob
buf += vlq(len(index_entries))
for name, off, n in index_entries:
    buf += vlq(len(name)) + name + struct.pack(">QQ", off, n)
buf[8:16] = struct.pack(">Q", index_off)

OUT_PAK.write_bytes(bytes(buf))
print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries")
