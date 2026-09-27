#!/usr/bin/env python3
"""Lossless trim of FrackinUniverse pak: drops files the engine can never
open (authoring sources, CI leftovers, docs, dev directories) plus a
verified-unreferenced dev test map. Writes <pak>.new; swap manually after
verification. Re-run against a fresh upstream pak when FU updates.

Usage: python tools/repack_fu_trim.py [src_pak] [out_pak]
"""
import sys, os, struct
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pak import Pak

STAR = 'E:/My Games/steamapps/common/Starbound'
SRC = sys.argv[1] if len(sys.argv) > 1 else STAR + '/mods/FrackinUniverse_contents_729480149.pak'
OUT = sys.argv[2] if len(sys.argv) > 2 else SRC + '.new'


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


def wstr(s):
    b = s.encode('utf-8')
    return vlq(len(b)) + b


def wval(v):
    if v is None:
        return b'\x01'
    if isinstance(v, bool):
        return b'\x03' + (b'\x01' if v else b'\x00')
    if isinstance(v, float):
        return b'\x02' + struct.pack('>d', v)
    if isinstance(v, int):
        z = (v << 1) if v >= 0 else ((-v - 1) << 1) | 1
        return b'\x04' + vlq(z)
    if isinstance(v, str):
        return b'\x05' + wstr(v)
    if isinstance(v, list):
        return b'\x06' + vlq(len(v)) + b''.join(wval(x) for x in v)
    if isinstance(v, dict):
        return b'\x07' + vlq(len(v)) + b''.join(wstr(k) + wval(x) for k, x in v.items())
    raise TypeError(f'unsupported metadata value: {v!r}')


INERT_EXT = ('.txt', '.md', '.js', '.pdn', '.xcf', '.bak', '.aseprite', '.unused',
             '.fuck', '.zip', '.psd', '.au', '.tsx', '.json~', '.editorconfig',
             '.gitignore', '.luacheckrc', '.py', '.sh', '.yml', '.dmp')
INERT_DIRS = ('/a_notyetadded/', '/a_modders/', '/tests/', '/.github/')
INERT_FILES = {
    '/.editorconfig', '/.gitignore', '/.luacheckrc', '/license.txt',
    '/dungeons/missions/testlunar.json', '/dungeons/missions/testlunar.dungeon',
    '/dungeons/npcrangetest.json', '/zb/questlist/banners/fu_test.png',
    '/sfx/npc/monsters/pandorasboxnocttop_aggro1old.ogg',
    '/sfx/npc/monsters/nocttop_aggro1old.ogg',
    '/objects/farmables/glarestalk/glarestalkseedold.png',
    '/interface/title/firstlogo.png.bak',
    '/objects/colonysystem2/addons/communitygarden/communitygardenold.lua',
    '/monsters/walkers/fleshleech/old/fleshleechold.animation',
    '/monsters/walkers/fleshleech/old/fleshleechold.monstertype',
}


def drop(name):
    low = name.lower()
    if low in INERT_FILES:
        return True
    if any(low.startswith(d) for d in INERT_DIRS):
        return True
    if 'thumbs.db' in low or 'desktop.ini' in low:
        return True
    if low.endswith(INERT_EXT):
        return True
    return False


pk = Pak(SRC)
meta = pk.meta
meta_blob = b'INDEX' + vlq(len(meta)) + b''.join(
    wstr(k) + wval(v) for k, v in meta.items())

kept, dropped = [], []
for n in pk.index:
    (dropped if drop(n) else kept).append(n)

buf = bytearray(b'SBAsset6' + b'\x00' * 8)
entries = []
for name in sorted(kept):
    data = pk.read(name)
    entries.append((name.encode('utf-8'), len(buf), len(data)))
    buf += data

index_off = len(buf)
buf += meta_blob
buf += vlq(len(entries))
for name, off, n in entries:
    buf += vlq(len(name)) + name + struct.pack('>QQ', off, n)
buf[8:16] = struct.pack('>Q', index_off)

open(OUT, 'wb').write(bytes(buf))
old_total = sum(l for o, l in pk.index.values())
new_total = sum(l for _, _, l in entries)
print(f'kept {len(entries)} dropped {len(dropped)}')
print(f'payload {old_total/1e6:.1f} -> {new_total/1e6:.1f} MB, pak {len(buf)/1e6:.1f} MB')
for n in sorted(dropped)[:60]:
    print('  -', n)
