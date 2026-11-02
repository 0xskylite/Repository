# The Tower That Was Saved by Quitting — Pisa Short

This is the completed first-pass production project for the 17-shot vertical short. It includes the original story/timeline/audio design, a Remotion + Three.js scene implementation, the requested white-head stickman character style, a synced voice/music/SFX mix, and a GitHub Actions cloud-render workflow.

**Start here:** read `README-CLOUD.md`.

## Included
- `src/story.ts`: 17-shot timeline and story physics (1922 frames, 30 fps).
- `src/scene/World.tsx`: procedural 3D Pisa tower, piazza, cutaway, beach/sponge stages and 2D stickman sprite characters.
- `src/Root.tsx`, `src/index.tsx`, `src/PisaShort.tsx`: Remotion entry/composition.
- `public/audio/voice.wav`: pitch-preserved, time-compressed narration matched to the planned 64.07-second cut.
- `public/audio/bed.wav`, `public/audio/final-mix.wav`: soundtrack and final audio mix.
- `.github/workflows/render.yml`: manual cloud rendering workflow.

## Important
The source project and audio mix are prepared. The GitHub Actions workflow has not yet been run, so a final MP4 render and visual QA are still pending. The 3D build is a procedural first pass; tune the scene after reviewing the cloud-rendered result.
