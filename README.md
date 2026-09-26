# Starbound Modpack Overhaul & Korean Translation

Local maintenance mods for a Starbound/OpenStarbound modpack, plus the
Korean overhaul translation.

## Contents

- `mods/zz_female_overhaul.pak` — consolidated non-translation compatibility
  fixes (reference repairs, FU copper armor price type fix, Viera blueprint
  unlock). See `FEMALE_OVERHAUL.txt` inside the pak for the full manifest.
  **All future local modifications to any mod are made as overrides inside
  this pak** — edit the source tree at `mods_src/female_overhaul/` and run
  `python tools/repack_overhaul.py` to rebuild the pak (case-preserving
  writer). Upstream paks are only repacked when a change cannot be expressed
  as a patch (removals, in-place patch edits, binary assets).
- `mods/gic_4_3_compat_fixes/` — must load immediately after the GiC core mod
  and before its addon patches (provides empty `interactData.recipes` and a
  restored deprecated magazine asset).
- `tools/build_pak.py` — case-preserving SBAsset6 pak writer used to build the
  merged translation pak on Windows (bypasses NTFS case folding).
- `tools/pak.py` — minimal SBAsset6 pak reader.
- `translation/` — Korean translation workspace (pipeline scripts, batch TSVs
  under `translation/translations/`, translation memory, worklists, glossary
  TSV, alignment/corpus/inventory data). Documents are kept out of the repo;
  the packing inputs are all here.

## Releases

Maintained pak binaries are published as release assets, not in git history:

- `StarboundKoreanTranslation_v1.0.0.zip` — everything below plus
  `install.bat` in one bundle: extract anywhere, run `install.bat`
  (auto-detects the Starbound folder; a mods/ or Starbound folder can also
  be dragged onto it)
- `female_translation.pak` — merged Korean translation overlay (~78 MB)
- `zz_female_overhaul.pak` — consolidated compatibility fixes
- `gic_4_3_compat_fixes.zip` — the directory mod zipped for drop-in install
- `install.bat` — standalone installer; works with the loose assets too if
  all files sit in the same folder

Install: run `install.bat` from the bundle, or drop the pak/dir entries
under `mods/` into `Starbound/mods/` manually.
