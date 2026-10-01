import json
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
STAR = BASE.parents[1]
sys.path.insert(0, str(STAR))

from pak import Pak
from pak_writer import write_pak

SRC_PAK = STAR / "mods" / "zz_translation_female.pak"
OUT_PAK = BASE / "backup_paks/female_translation.pak.NORMALIZED"
TARGETS = {
    "/objects/skillbook/RPGskillbook.activeitem.patch",
    "/objects/generic/perfectlygenericitem/perfectlygenericitem.object.patch",
    "/items/generic/shpd_seeds/blindweed.item.patch",
}


def main():
    pak = Pak(str(SRC_PAK))
    overrides = {}
    groups = 0
    for asset in pak.index:
        if asset not in TARGETS:
            continue
        data = pak.read(asset)
        try:
            doc = json.loads(data)
        except Exception:
            continue
        if not isinstance(doc, list) or not any(isinstance(item, list) for item in doc):
            continue
        flat = []
        stack = list(reversed(doc))
        while stack:
            item = stack.pop()
            if isinstance(item, list):
                stack.extend(reversed(item))
                groups += 1
            else:
                assert isinstance(item, dict), asset
                flat.append(item)
        overrides[asset] = json.dumps(flat, ensure_ascii=False, indent=2).encode("utf-8")
    count = write_pak(OUT_PAK, SRC_PAK, overrides)
    check = Pak(str(OUT_PAK))
    assert len(check.index) == count
    for asset in TARGETS:
        try:
            doc = json.loads(check.read(asset))
        except Exception:
            continue
        if isinstance(doc, list):
            assert all(isinstance(item, dict) for item in doc), asset
    print(f"normalized {groups} nested groups in {len(overrides)} assets; entries {count}")


if __name__ == "__main__":
    main()
