# Gungan player race test build

Implements the Creating Player Races tutorial using the current SWLOR appearance registry.
Tutorial: https://wiki.starwarsnwn.com/Development/Creating-Player-Races

- RacialType 170; AppearanceType 10269; dynamic Elf (E) body and armor family.
- Male default head 300; female default head 303. Five distinct supplied head assemblies are available to both sexes, at Elf slots 300-304.
- Default scale 1.05; selectable body scale 1.00-1.40. The requested maximum is 1.40, below the existing Wookiee maximum of 1.50.
- The starting scale is applied and persisted on character initialization. The redundant Race login scale reset was removed; PlayerTemporaryEffects restores each saved height.
- Gungan language skill 51, translator, chat command, initial fluency, display label, and language color.
- Standard and Force Sensitive class eligibility; neutral racial ability adjustments.
- Eight male and seven female portraits, each in H/L/M/S/T DDS + TXI format. Replaced the original generated framing with all 75 individually supplied refined crops from the 15 ZIP archives; no additional cropping or resizing. Huge variants are included.
- Race icon from gungan_icon.jpg. The alternate icon and all original input files remain unchanged.
- TLK gaps 6182-6185 reused and binary TLK rebuilt.

## Source assets

The supplied Blender file remains unchanged. Its GUNGANS collection contains the five prepared helm_304 through helm_308 head assemblies; these were exported and renamed to player heads. The source MDLs and texture provenance are in this folder. Broken relative texture references were resolved to their existing local source files. No new anatomy or textures were invented.

The loose hand (Object001), foot (foot2), and additional unassembled heads remain in the source Blender file. They have not been integrated into this first test build; it currently uses Elf body parts. Heads use their original RGB texture colors; skin tinting of the heads is not implemented.

## Verified

Server build succeeds with post-build deployment disabled. Eight focused tests pass (GunganRaceTests, PlayerAppearanceTests, CharacterFullRebuildDroidTests). Ten compiled head models pass the repository compiler's full round-trip validation. tools/ValidateGunganResources.py validates the actual HAK branch's race, appearance, class, binary TLK, model, portrait, and icon links. All configured resources meet the NWSync size limit.

## In-game acceptance still required

1. Create male and female Gungans. Confirm the race name, description, icon, portraits, and both character-type choices.
2. Open appearance customization; cycle all five heads and check neck attachment, ears, blink behavior, walking, fighting, sitting, armor, robes, cloaks, and helmets.
3. Compare default Gungans directly with default Humans and Wookiees; adjust the Gungan baseline after this check. The current Wookiee code starts at 1.0 and its static reference assets are not consistently taller than Human defaults. Appearance HEIGHT=2.15 is metadata, not proof of visual size. The desired default height ordering is therefore NOT yet confirmed.
4. Check the 1.40 upper height cap and reconnect after selecting a height. Saved height is now restored by the existing PlayerTemporaryEffects handler without a competing reset to species defaults.
5. Confirm Basic and Gungan fluency and the gungan language command.
6. Confirm portraits are upright in the game UI.

## Branch and deployment notes

Changes are uncommitted on the prepared xis-gungans branches in the sibling SWLOR_NWN and SWLOR_Haks checkouts. The SWLOR_NWN/SWLOR_Haks submodule contains unrelated pre-existing head-324 changes and was not modified. Both sets of changes must be integrated together before normal deployment; the parent submodule pointer has not been advanced.

A local test package with four complete replacement HAKs (sw_2da, sw_pt_head, sw_portrait, sw_ui), sw_tlk.tlk, and the two changed server assemblies is staged under development/gungan-audit/test-package. The local debug server has received targeted resource updates with rollback copies, preserving unrelated existing resources. Its HAK/TLK directories are also the active local client aliases. The full HAKs represent the sibling xis-gungans checkout and do not include the unrelated submodule head-324 work.


## Character creation and texture correction (2026-09-16)

Added Gungan RACE 170 to cls_pres_stand.2da as well as cls_pres_force.2da. The resource validator now checks both prerequisite tables.
All five head TGAs now use bottom-left storage (descriptor 0), preserving the decoded RGB pixels exactly. This addresses the top-down texture orientation seen in the in-game screenshot; live visual confirmation is still required.
Targeted updates were deployed to debugserver/hak/sw_2da.hak and sw_pt_head.hak and the local server restarted. Rollback copies are in development/gungan-audit/server-texture-class-rollback-20260917. Restart the NWN client to reload HAK resources.

An editable Gungan_Head_Workbench/Gungan_Player_Heads.blend is beside the supplied source file in development-WIPs/GUNGANS. It includes ten independent head scenes, packed textures, locked Elf body references, and an embedded export script. Use Blender 4.0 with NeverBlender; the installed addon has a Blender 4.5 export compatibility issue. All ten exports were compiled and round-trip validated. No manual sizing changes have been made yet.


Refined portraits: `portrait_manifest.json` maps each ZIP archive to its existing portrait entry and records hashes, dimensions, conversion, and orientation checks. Originals and previous resources are backed up in development/gungan-audit/refined-portraits. The local portrait HAK was updated while preserving unrelated resources, with rollback in server-refined-portraits-rollback-20260917. Restart the client to reload portraits.
