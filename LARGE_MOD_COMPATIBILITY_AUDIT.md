# Large-mod compatibility audit — 2026-09-28.11

Requested workflow: collect static findings and fixes first; run one final batched engine check. No saves are changed.

## Load order

The local engine source (`tmp/StarRoot.cpp`, lines 667–709) sorts by priority and then visits `includes` and `requires` dependencies before each dependent mod. `includes` is optional; an absent `requires` dependency is fatal. Renaming a pak does not supersede this dependency traversal.

The consolidation now explicitly includes 18 installed parent/addon metadata names, preserving its existing late priority. None of those sources depend on `female_overhaul`. This does not globally reorder the original mods. Existing Cosmic Husbandry, FU SAIL, Elithian study-list and K’Rakoth rifle late repairs remain in place.

## New repairs

39 obsolete target paths were repaired in `mods_src/female_overhaul`:

| Source | Targets | Restored behavior |
| --- | ---: | --- |
| contents_2010883172.pak | 5 | Five mission monsters: bleeding immunity (missions → mission). |
| contents_2957477338.pak | 2 | Quest objective description and spear ability type at current Arcana paths. |
| RPG_contents_1115920474.pak | 24 | 17 current Knightfall armor categories and seven moved monster RPG scripts. Removed Raptorframe equipment was not recreated. |
| contents_2980872125.pak | 1 | Voyage Covenant codex classification in Arcana tab. |
| contents_3010955719.pak | 3 | Energy tags for current Seeker SMG, police shotgun and Prime Circuit. |
| BL3_Shellguard_Addon_contents_2225814372.pak | 2 | Dragon/crystal boss immunity parameters and crystal boss health-bar script at actual boss filenames. |
| contents_1433991809.pak | 1 | Wild mellowroot harvest stage resets as intended. |
| Extended_Story_contents_899795176.pak | 1 | Cultist boss environmental immunities: corrected cultisboss typo. |

Scripts and item tags are appended only if absent. Existing entries and ordering are preserved. Armor changes affect category only. Existing source patches and parent files remain intact.

## Reviewed without additional speculative changes

Arcana, Elithian, My Enternia, K’Rakoth, Knightfall, Shellguard, Starforge, Extended Story, Betabound, RPG Growth, Cosmic Husbandry and Voyage, plus named related addons were examined for missing targets, registration order and raw overwrites. The recorded title-selected inventory covers 58 sources; this is an asset/order audit, not a full campaign test.

K’Rakoth Arcana / Extended Story / Project Redemption patches, Shellguard engineer/fullbright/storage/mech patches, digital crafting addons, Arcana FU descriptions/extraction and RPG balance/graphic patches had no unhandled early target registration in the captured load order. My Enternia storage path redirects were already present.

Absent optional planet integrations and retired equipment are left inactive. The Sexbound Arcana `pregnant.config` cannot be mapped to the unrelated `/dialog/tentacles/pregnant.config` just because the filenames match. The original Arcana/keybinds and RPG/keybinds library copies share version 1.3.5; their later override is not evidence of lost functionality. Arcana relic/vendor/name raw overrides supplied by Voyage are expected addon overrides.

## Final validation

The one final combined engine run loaded 26,864 JSON assets with zero asset-loading failures. All 53 value assertions for the 39 retained target repairs passed. The initial 40-target candidate run reported one failed assertion for obsolete Voyage relic perks; inspection confirmed an existing current patch with different units and IDs. The redundant legacy perk restoration was removed entirely (including its second old perk), then the pak was rebuilt. No second engine run was needed for that removal. The current Voyage perk patch is preserved. Gameplay/campaign coverage is not implied.
