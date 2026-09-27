#!/usr/bin/env python3
"""Lossless trim of a packed .pak: drops files with extensions the engine has
no loader for (authoring sources like .pdn/.psd/.xcf, archives, OS junk).
Keeps everything else byte-identical. Writes <src>.new; swap manually after
verification. Usage: python tools/trim_pak.py <pak> [more.pak ...]
Paths may be absolute or relative to the Starbound mods dir.
"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pak import Pak

MODS = 'E:/My Games/steamapps/common/Starbound/mods'

def vlq2(n):
    parts = []
    while True:
        parts.append(n & 0x7f); n >>= 7
        if not n: break
    out = bytearray()
    for i, b in enumerate(reversed(parts)):
        out.append(b | (0x80 if i < len(parts) - 1 else 0))
    return bytes(out)

def wstr(s):
    b = s.encode('utf-8')
    return vlq2(len(b)) + b

def wval(v):
    if v is None: return b'\x01'
    if isinstance(v, bool): return b'\x03' + (b'\x01' if v else b'\x00')
    if isinstance(v, float): return b'\x02' + struct.pack('>d', v)
    if isinstance(v, int):
        z = (v << 1) if v >= 0 else ((-v - 1) << 1) | 1
        return b'\x04' + vlq2(z)
    if isinstance(v, str): return b'\x05' + wstr(v)
    if isinstance(v, list): return b'\x06' + vlq2(len(v)) + b''.join(wval(x) for x in v)
    if isinstance(v, dict): return b'\x07' + vlq2(len(v)) + b''.join(wstr(k) + wval(x) for k, x in v.items())
    raise TypeError(repr(v))

# extensions with NO engine loader whatsoever (authoring sources, archives, OS junk)
HARD_EXT = ('.pdn','.psd','.xcf','.aseprite','.kra','.clip','.blend','.fbx','.obj',
            '.zip','.bak','.orig','.unused','.tmx','.tsx','.dmp','.json~',
            '.editorconfig','.gitignore','.luacheckrc','.py','.sh','.yml','.yaml',
            '.rtf','.url','.html','.htm','.js','.flp','.ai','.dcproj','.backup','.old',
            '.txt~','.lua~','.wav~','.png~','.ogg~','.sublime-project','.sublime-workspace')
# VCS/CI internals baked into paks: extensionless loose objects, pack files, hooks
HARD_DIRS = ('/.git/', '/.github/', '/.svn/', '/.hg/')

def repack(src, out):
    pk = Pak(src)
    meta_blob = b'INDEX' + vlq2(len(pk.meta)) + b''.join(wstr(k) + wval(v) for k, v in pk.meta.items())
    kept, dropped = [], []
    for n in pk.index:
        nl = n.lower()
        if nl.endswith(HARD_EXT) or any(nl.startswith(d) for d in HARD_DIRS) \
                or 'thumbs.db' in nl or 'desktop.ini' in nl:
            dropped.append(n)
        else:
            kept.append(n)
    buf = bytearray(b'SBAsset6' + b'\x00' * 8)
    entries = []
    for name in sorted(kept):
        data = pk.read(name)
        entries.append((name.encode('utf-8'), len(buf), len(data)))
        buf += data
    index_off = len(buf)
    buf += meta_blob
    buf += vlq2(len(entries))
    for name, off, n in entries:
        buf += vlq2(len(name)) + name + struct.pack('>QQ', off, n)
    buf[8:16] = struct.pack('>Q', index_off)
    open(out, 'wb').write(bytes(buf))
    old_total = sum(l for o, l in pk.index.values())
    new_total = sum(l for _, _, l in entries)
    print('%s: kept %d dropped %d | %.1f -> %.1f MB (pak %.1f MB)' % (
        os.path.basename(src), len(entries), len(dropped),
        old_total/1e6, new_total/1e6, len(buf)/1e6))

for f in sys.argv[1:]:
    src = f if os.path.isabs(f) else os.path.join(MODS, f)
    repack(src, src + '.new')
