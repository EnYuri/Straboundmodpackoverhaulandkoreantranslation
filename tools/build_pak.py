import os, json, zlib, struct, shutil, sys

STAR = "E:/My Games/steamapps/common/Starbound"
LAYERS = [  # merge precedence: earlier loses on same-key conflicts; human KO last
    ("E:/pakx/localeko_gic_legacy", "gic_legacy"),
    ("E:/pakx/localeko_black_armory_legacy", "ba_legacy"),
    ("E:/pakx/localeko_extended_story_legacy", "es_legacy"),
    ("E:/ft_src", "ft"),
    ("E:/pakx/zz_localeko_postload", "postload"),
    ("E:/pakx/-9998_trans_sbkor_0.98_structfix", "sbkor"),
    ("E:/pakx/FU_KO_contents_3166424163", "fuko"),
]
SKIP = {"_metadata", "_previewimage", "preview.png"}
PREMERGE = "E:/Desktop/mods/replaced-installed-20260922/female_translation-premerge.pak"
OUT_PAK = os.path.join(STAR, "mods", "female_translation.pak")

def groups(data):
    j = json.loads(data, strict=False)
    if not isinstance(j, list):
        return [[j]]
    gs, cur = [], []
    for el in j:
        if isinstance(el, list):
            if cur:
                gs.append(cur); cur = []
            gs.append(el)
        else:
            cur.append(el)
    if cur:
        gs.append(cur)
    return gs

# ---- collect entries: rel -> bytes (case preserved from each layer's own tree)
entries = {}          # rel -> bytes to store (patch entries get merged JSON)
patch_groups = {}     # rel -> list of op groups (per exact-case rel)
raw_bytes = {}        # rel -> source path (later layer wins)
malformed = []        # verbatim patch files we could not parse

for d, tag in LAYERS:
    for root, _, fs in os.walk(d):
        for f in fs:
            rel = os.path.relpath(os.path.join(root, f), d).replace(os.sep, "/")
            if rel in SKIP:
                continue
            src = os.path.join(root, f)
            if f.endswith(".patch"):
                try:
                    g = groups(open(src, encoding="utf-8-sig").read())
                except Exception:
                    malformed.append((tag, rel, src))
                    continue
                patch_groups.setdefault(rel, []).extend(g)
            else:
                raw_bytes[rel] = src

# verbatim malformed patches (engine tolerates lenient JSON)
for tag, rel, src in malformed:
    if rel not in patch_groups and rel not in raw_bytes:
        raw_bytes[rel] = src

# metadata blob: reuse the INDEX metadata bytes from the premerge pak verbatim
d0 = open(PREMERGE, "rb").read()
off0 = struct.unpack(">Q", d0[8:16])[0]
assert d0[off0:off0 + 5] == b"INDEX"

def _vlqr(d, p):
    r = 0
    while True:
        b = d[p]; p += 1
        r = (r << 7) | (b & 0x7F)
        if not b & 0x80:
            return r, p

def _key(d, p):
    l, p = _vlqr(d, p)
    return p + l

def _val(d, p):
    t = d[p]; p += 1
    if t == 0x05:
        l, p = _vlqr(d, p); return p + l
    if t == 0x04:
        _, p = _vlqr(d, p); return p
    if t == 0x06:
        c, p = _vlqr(d, p)
        for _ in range(c):
            p = _val(d, p)
        return p
    if t == 0x01:
        c, p = _vlqr(d, p)
        for _ in range(c):
            p = _key(d, p); p = _val(d, p)
        return p
    if t == 0x00:
        return p
    if t == 0x02:
        return p + 1
    if t == 0x03:
        return p + 8
    raise ValueError(f"dynval type {t:#x} at {p-1}")

p = off0 + 5
pairs, p = _vlqr(d0, p)
for _ in range(pairs):
    p = _key(d0, p)
    p = _val(d0, p)
meta_blob = d0[off0:p]  # 'INDEX' + complete metadata dynval

# ---- inject a very high load priority so every content-mod file already
# exists when this overlay is scanned (patches only register for targets
# present at scan time). The raw (key,value) byte spans are copied verbatim
# and the new pair is appended.
p2 = off0 + 5
npairs, p2 = _vlqr(d0, p2)
spans = []
for _ in range(npairs):
    s0 = p2
    p2 = _key(d0, p2)
    p2 = _val(d0, p2)
    spans.append(d0[s0:p2])
def _vlq(n):
    parts = []
    while True:
        parts.append(n & 0x7F)
        n >>= 7
        if not n:
            break
    out = bytearray()
    for i, b in enumerate(reversed(parts)):
        out.append(b | (0x80 if i < len(parts) - 1 else 0))
    return bytes(out)
def _wint(n):
    z = (n << 1) if n >= 0 else ((-n - 1) << 1) | 1
    return bytes([0x04]) + _vlq(z)
meta_blob = (
    b"INDEX" + _vlq(npairs + 1) + b"".join(spans)
    + _vlq(len(b"priority")) + b"priority" + _wint(999999850)
)

# ---- assemble file list
files = {}  # rel -> bytes
for rel, gs in patch_groups.items():
    files["/" + rel] = json.dumps(gs, ensure_ascii=False, indent=2).encode("utf-8")
for rel, src in raw_bytes.items():
    files["/" + rel] = open(src, "rb").read()

# ---- drop ops that target keys absent from the current merged base
# (Starbound JsonPatch is all-or-nothing per file: one bad op blocks the rest)
import re
FIXUPS = {
    "/objects/outpost/shipyardwelding/shipyardwelding.object.patch": [r"^/chatOptions"],
    "/objects/outpost/techlab/techlabscientist.object.patch": [r"^/chatOptions"],
    "/objects/crafting/woodencookingtable/woodencookingtable.object.patch": [
        r"^/(apex|avian|floran|glitch|human|hylotl|novakid)Description$",
    ],
    "/interface/windowconfig/playerinventory.config.patch": [r"^/paneLayout/labelinventory"],
    "/npcs/dungeon/aviantomb/tombguard.npctype.patch": [r"^/scriptConfig/dialog/.*/\d+$"],
    "/npcs/dungeon/glitchcastle/castlelord.npctype.patch": [r"^/scriptConfig/dialog/attack/glitch$"],
    "/npcs/dungeon/glitchcastle/friendlycastlelord.npctype.patch": [r"^/scriptConfig/dialog/attack/glitch$"],
    "/quests/story/shiprepair.questtemplate.patch": [r"^/scriptConfig/descriptions"],
    "/radiomessages/fu_madness.radiomessages.patch": [r"/senderName$"],
    "/radiomessages/tutorial.radiomessages.patch": [r"^/naturalcave2"],
}
for rel, pats in FIXUPS.items():
    if rel not in files:
        continue
    rx = [re.compile(p) for p in pats]
    j = json.loads(files[rel].decode("utf-8"))
    removed = 0
    for g in j:
        keep = []
        for o in g:
            if any(r.search(str(o.get("path", ""))) for r in rx):
                removed += 1
                continue
            keep.append(o)
        g[:] = keep
    files[rel] = json.dumps(j, ensure_ascii=False, indent=2).encode("utf-8")
    print("fixup", rel, "removed", removed, "ops")

def vlq(n):
    parts = []
    while True:
        parts.append(n & 0x7F)
        n >>= 7
        if not n:
            break
    out = bytearray()
    for i, b in enumerate(reversed(parts)):
        out.append(b | (0x80 if i < len(parts) - 1 else 0))
    return bytes(out)

# ---- write pak: SBAsset6 + u64 indexOffset + blobs + INDEX + metadata + entries
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

open(OUT_PAK, "wb").write(bytes(buf))
print("wrote", OUT_PAK, len(buf), "bytes,", len(index_entries), "entries,", len(malformed), "malformed verbatim")
