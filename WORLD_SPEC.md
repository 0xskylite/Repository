# World, characters and effects to build (what the template files must change)
Every number below is already used by `src/story.ts`; build the world to these values and the cameras land correctly.
Start by copying `templates/bridge/` to `src/videos/pisa/` and the audio/scripts folders (see README). Ownership follows the skill's sandbox split.

## Layout (metres, +y up, piazza floor y = 0, tower base centre at the origin)
| thing | value |
|---|---|
| tower | radius R = 7.2, floor height FH = 5.4, 8 floors (43 m). Floors 1-3 = 1173, 4-7 = 1272, 8 = belfry (modern only). Round white marble, arcaded galleries (cartoon arcades: 14 arches per floor), ink on arches and columns |
| lean | rotate the stacked floors about the base toward **+x** by `tilt` (rad). `sink` lowers the +x edge of the foundation into the ground (m). `curve` bends the floors above 3: add about (curve x 0.012 rad) extra straightening per floor (a starting value, tune by eye), i.e. the upper floors straighten up, giving the banana curve |
| tilt values | hook / modern 0.10 rad; 1173 era 0.06 rad (exaggerated on purpose); shot 4 grows 0.006 -> 0.05 |
| cathedral | a big white-and-grey cathedral behind the tower at about (-26, 0, -10), long axis along x; baptistery optional |
| piazza | huge flat lawn (storybook green) with paving strip around the cathedral; low stone wall far back; a few cypress trees (kit `tree_cone`) |
| scaffold | wooden scaffold + a treadwheel crane on the +z side of floors 1-3; hammer point at (-6.5, 7.5, 6.5) |
| plumb | cord from (9.5, 12, 4) hanging to a bob at (9.5, 6, 4) on a tall wooden post; swings in shot 5, hangs dead still in shot 15 |
| foreman | stands at about (5, 0, 11) in 1173 (shot 2), plumb foreman at (11, 0, 5) |
| DIG | soil-extraction tubes under the HIGH (-x) side, surface point (-5, 0, 6) |
| CUT stage | at (-150, 0, 90): soil slab x -12..12, z -5..5, y -14..0, painted layers (silt top, clay below, sand at the bottom), tower on top; clay colour = `firm` (0 light tan, soft -> 1 dark firm brown); droplets rise and ripple at `drain` |
| BEACH stage | at (150, 0, -80): wet dark sand (z < -80) -> dry light sand; thin sea to -z, small waves; one footprint that deepens with `footSink` then half-recovers |
| SPONGE stage | at (150, 1, 80): wooden table, big yellow sponge, water drips |

## States to read from story.ts per frame (world.ts per-frame posing)
`towerState(id, f)` -> floors (fractional: the top floor scales up from the ground with an overshoot), tilt, sink, firm, moss (weeds + ivy on the stump), curve, drain.
`warFront(tau)`, `marchPhase(tau)` for the column; `squeeze(f)` for the sponge; `footSink(f)` for the beach; `HAMMER_FREEZE` / `HAMMER_DROP` for the mason's hammer.

## Light
- `day` and `golden` presets from lights.ts are reused unchanged (day: shots 1-6, 10-12, 14-17; golden: 7-9, 13).
- Cut-away and sponge stages use the day preset with the sun camera-relative; no fog on the cut-away (it is a model slab).

## Cast (character cards, `cast.ts` / `toon.ts`, all on the NOINK layer, plum ink)
| role | look |
|---|---|
| tourists (shots 1, 17) | modern clothes, one with a camera, one with sunglasses; "hold the tower up" pose: arms up, palms toward the tower |
| 1173 foreman | beard, long tunic, scroll plan under the arm |
| masons (6-8 cards) | wool caps in different colours, leather aprons; hammer, chisel, rope |
| 1272 foreman | clean-shaven, red cap (so viewers see it is a new person) |
| soldiers | light mail, red-and-white pennons, spears; peaceful cartoon marching |
| engineers 2008 | white hard hats, orange vests, tablet; one on a radio |
| beach kid | one bean character barefoot on wet sand |
| digger (shot 17) | in a small hole, waving, hard hat |
Faces: reuse the 14-expression library; add "surprised, mouth O" and "deadpan" if missing.

## Effect cards (flat 2D sprites in the scene)
dust puff (floor landings), water drops and ripples, exclamation mark / question mark (shot 5 gasps), sweat drop, sparkle on the final chord, squelch rings on the sand, speed lines on the hammer swing.

## Props from the Kenney kit (names that already exist in build.ts)
`cart`, `plant_bushDetailed`, `lantern`, `stall-bench`, `banner-red`, `tree_cone` / `tree_oak` / `tree_default`, `canoe` (unused here). New hand-built: tower floors, cathedral, scaffold, plumb post, sponge, extraction tubes, shovel, hole.

## Readability traps for THIS short (check in every sandbox round)
- Pisa (red field, white cross) and Genoa (white field, red cross) flags must never be in the same frame at small size; use plain coloured pennons for the extras.
- Keep the plumb cord crossing nobody's torso (it reads as a hanging): bob and post to the side of the masons in shots 5 and 15.
- The lean must read at a glance on a phone: if the 0.06 rad tilt looks weak in the stills, raise OLD_TILT to 0.07 (story.ts) and nothing else changes.
- No text in the cut-aways (no labels, no arrows): colour and drops tell the story.
- Cut-away slabs need a clean ink outline on the cut face only, not on every layer line.
- Props closer than 2 m to a lens become blobs: shots 5 and 15 put the lens 2.9 m from the bob (ok); check shot 6 (hammer, 5.4 m) and shot 11 (feet CU 2.5 m).

## Sandbox ownership (from the skill)
cam: story.ts | world: world.ts, lights.ts, shade.ts, grade.ts | mat: paint.ts, build.ts | char: toon.ts, cast.ts, cardshade.ts | post: ink.ts, Bridge.tsx, lensblur.ts
