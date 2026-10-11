# No Exhaustion Blur (Skyrim SE Survival Mode)

Removes the screen blur that Survival Mode applies when your character is tired.
The tiredness penalties themselves are untouched.

**Status:** early release. The plugin has been checked structurally (it re-parses
cleanly and only touches the four records listed below) but has had little
in-game testing so far. Reports are welcome.

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

## Requirements

- Skyrim Special Edition / Anniversary Edition with the Creation Club
  **Survival Mode** (`ccQDRSSE001-SurvivalMode.esl`)
- [Survival Mode Improved - SKSE](https://www.nexusmods.com/skyrimspecialedition/mods/78244)
  (`SurvivalModeImproved.esp`)

Both are masters of the plugin, so the game will not load it without them.

## Install

1. Copy `No Exhaustion Blur.esp` into your Skyrim `Data` folder, or install it
   with your mod manager.
2. Enable it and make sure it loads after `SurvivalModeImproved.esp`. LOOT and
   Vortex's automatic sorting do this on their own because of the masters.

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
python build.py "C:/Program Files (x86)/Steam/steamapps/common/Skyrim Special Edition/Data"
```

`build.py` reads the four records from Survival Mode and Survival Mode Improved,
drops their `VMAD` (script) subrecord, and writes them into a new light plugin.
It needs Python 3 and nothing else.

## Credits

- Bethesda Game Studios for Survival Mode
- colinswrath for Survival Mode Improved - SKSE, whose records three of the four
  overrides are based on

## License

`build.py` is released under the MIT License (see `LICENSE`). The plugin contains
override records derived from Survival Mode and Survival Mode Improved and is
shared as a compatibility patch for people who own and have installed both.
