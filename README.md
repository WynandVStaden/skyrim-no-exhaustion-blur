# No Exhaustion Blur (Skyrim SE Survival Mode)

Removes the screen blur that Survival Mode applies when your character is tired.
The tiredness penalties themselves are untouched.

**Status:** early release. Both plugins have been checked structurally (they re-parse
cleanly and only touch the four records listed below). The vanilla Survival Mode
plugin has not been tested in game yet. Reports are welcome.

## What it changes

Creation Club Survival Mode attaches a separate "screen effect" magic effect to
each exhaustion stage, next to the stat penalties. That effect runs a small
script which applies the blur. This plugin overrides those four effects and
removes the script:

| Form ID (in Survival Mode) | Editor ID |
|---|---|
| `xx0008EF` | `Survival_ExhaustionStage2ImodEffect` |
| `xx0008F0` | `Survival_ExhaustionStage3ImodEffect` |
| `xx0008F1` | `Survival_ExhaustionStage4ImodEffect` |
| `xx0008F2` | `Survival_ExhaustionStage5ImodEffect` |

Not changed: reduced magicka and stamina regeneration, reduced disease
resistance, the skill reductions added by Survival Mode Improved, the tiredness
messages, and the cold and hunger effects (including the cold screen frost).

## Which file

There are two plugins. Use one, not both.

| Plugin | For |
|---|---|
| `No Exhaustion Blur.esp` | Setups with [Survival Mode Improved - SKSE](https://www.nexusmods.com/skyrimspecialedition/mods/78244) (built from version 1.6.6) |
| `No Exhaustion Blur - Vanilla Survival Mode.esp` | Plain Creation Club Survival Mode, without Survival Mode Improved |

Survival Mode Improved changes three of the four records, so its users need the
first file; the vanilla file would undo those changes.

## Requirements

- Skyrim Special Edition / Anniversary Edition with the Creation Club
  **Survival Mode** (`ccQDRSSE001-SurvivalMode.esl`)
- For `No Exhaustion Blur.esp` only: Survival Mode Improved - SKSE
  (`SurvivalModeImproved.esp`)

These are masters of the plugins, so the game will not load them without them.

## Install

1. Copy the plugin for your setup into your Skyrim `Data` folder, or install it
   with your mod manager.
2. Enable it. With Survival Mode Improved, make sure it loads after
   `SurvivalModeImproved.esp`; if it loads before, it does nothing. Check this
   after installing, since a mod manager may not re-sort straight away.

The plugin is light (ESL-flagged), so it does not use a full plugin slot.

If your character is already tired when you load a save, the blur that is
already applied can stay until the tiredness stage next changes. Sleep once and
it will not come back.

To uninstall, remove the plugin. It adds no new records and no scripts.

## Compatibility

Anything else that overrides the same four magic effects will conflict; load
this plugin after it. No other plugin in a 1,900-plugin Gate to Sovngarde load
order touches them.

## Building it yourself

The plugin is generated from your own game files, so nothing has to be taken on
trust:

```bash
python build.py "C:/Program Files (x86)/Steam/steamapps/common/Skyrim Special Edition/Data" all
```

`build.py` reads the four records from Survival Mode (and Survival Mode Improved
for that variant), drops their `VMAD` (script) subrecord, and writes them into a new light plugin.
It needs Python 3 and nothing else.

## Credits

- Bethesda Game Studios for Survival Mode
- colinswrath for Survival Mode Improved - SKSE, whose records three of the four
  overrides are based on

## License

`build.py` is released under the MIT License (see `LICENSE`). The plugin contains
override records derived from Survival Mode and Survival Mode Improved and is
shared as a compatibility patch for people who own and have installed both.
