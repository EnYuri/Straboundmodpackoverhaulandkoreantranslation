# -*- coding: utf-8 -*-
# Cover fields left English because other translation paks' patches abort early.
import sys, io, os, csv, json, time
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')
sys.path.insert(0, r"E:\My Games\steamapps\common\Starbound")
sys.path.insert(0, 'tools')
import pak_writer
from pak import Pak

ZZ = r"E:\My Games\steamapps\common\Starbound\mods\zz_translation_female.pak"

pairs = [
    ('/interface/cockpit/cockpit.config', '/displayOres/psicrystal/displayName', 'Psi Crystal', '사이 크리스탈'),
    ('/interface/cockpit/cockpit.config', '/displayOres/darkmatterore/displayName', 'Dark Matter Ore', '암흑 물질 광석'),
    ('/interface/cockpit/cockpit.config', '/displayOres/abyssshard/displayName', 'Umbrium Shard', '움브리움 파편'),
    ('/interface/cockpit/cockpit.config', '/displayOres/lunariteore/displayName', 'Lunarite Ore', '루나라이트 광석'),
    ('/interface/cockpit/cockpit.config', '/displayOres/inferniumore/displayName', 'Infernium Ore', '인페르니움 광석'),
    ('/interface/cockpit/cockpit.config', '/displayOres/cryoniumore/displayName', 'Cryonium Ore', '크라이오니움 광석'),
    ('/interface/cockpit/cockpit.config', '/displayOres/radyiteore/displayName', 'Radyite Ore', '라디아이트 광석'),
    ('/interface/cockpit/cockpit.config', '/displayOres/voltagenore/displayName', 'Voltagen Ore', '볼타겐 광석'),
    ('/interface/cockpit/cockpit.config', '/displayOres/bacteriaore/displayName', 'Bacteria Ore', '박테리아 광석'),
    ('/interface/cockpit/cockpit.config', '/displayOres/tinore/displayName', 'Tin Ore', '주석 광석'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/fireshower/displayName', 'Magma Meteors', '마그마 운석'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/pumpkinrain/displayName', 'Pumpkin Rain', '호박 비'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/ghosthour/displayName', 'Ghost Hour', '유령의 시간'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/batongswarm/displayName', 'Batong Swarm', '바통 떼'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/lightningrain_es/displayName', 'Lightning Rain', '번개 비'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/chargedground/displayName', 'Electric Ground', '전기 지면'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/thunderstorm/displayName', 'Lightning Storm', '번개 폭풍'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/worldrot/displayName', 'World Rot', '세계 부패'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/rottenrain/displayName', 'Rotten Rain', '썩은 비'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/rottenrainlight/displayName', 'Mild Rotten Rain', '약한 썩은 비'),
    ('/interface/cockpit/cockpit.config', '/displayWeathers/decayingair/displayName', 'Decaying Air', '썩은 공기'),
    ('/interface/cockpit/cockpit.config', '/planetTypeNames/nitrogendeep', 'Nitrogen Deep', '질소 심해'),
    ('/interface/cockpit/cockpit.config', '/planetTypeNames/darkabyss', 'Dark Abyss', '어둠의 심연'),
    ('/interface/cockpit/cockpit.config', '/planetTypeNames/eternalfire', 'Raging Inferno', '격노한 인페르노'),
    ('/interface/cockpit/cockpit.config', '/planetTypeNames/nuclearwasteland', 'Nuclear Wasteland', '핵 폐허'),
    ('/interface/windowconfig/craftingnocategories.config', '/paneLayout/lblProduct/value', 'MATERIALS AVAILABLE', '사용 가능한 재료'),
]

per_asset = {}
for asset, field, en, ko in pairs:
    per_asset.setdefault(asset, []).append(
        [{'op': 'test', 'path': field, 'value': en},
         {'op': 'replace', 'path': field, 'value': ko}])

pk = Pak(ZZ)
overrides = {}
for asset, ops in per_asset.items():
    pp = asset + '.patch'
    try:
        existing = json.loads(pk.read(pp).decode('utf-8'))
    except Exception:
        existing = []
    if not isinstance(existing, list):
        existing = [existing]
    existing.append(ops)
    overrides[pp] = json.dumps(existing, ensure_ascii=False).encode('utf-8')
del pk

out = ZZ + '.staged'
n = pak_writer.write_pak(out, ZZ, overrides)
print('wrote', n, 'files,', len(overrides), 'patch files')
time.sleep(1)
try:
    os.replace(out, ZZ)
    print('replaced')
except PermissionError:
    print('staged kept:', out)
