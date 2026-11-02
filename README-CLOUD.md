# Pisa Short — Android + Cloud Render Project

This package adds a Remotion + Three.js project, procedural stickman characters, a procedural Leaning Tower scene, synced audio and a GitHub Actions render workflow to the original Pisa short pack.

## Render target
- Composition: `PisaShort`
- Output: 1440 x 2560 (vertical 2K)
- FPS: 30
- Timeline: 1922 frames / 64.07 seconds
- Narration: `public/audio/voice.wav` (time-compressed from the supplied 94.51 s source to fit the 64.07 s shot plan; pitch-preserving FFmpeg atempo)
- Mix: `public/audio/final-mix.wav`

## Android cloud rendering
1. Create a GitHub repository and upload the contents of `pisa-short/` (not the parent folder).
2. Open GitHub → Actions → `Render Pisa Short` → Run workflow.
3. When complete, download `pisa-final-video` from Artifacts.

## Local preview (optional)
Requires Node.js 22+, npm and a browser/WebGL environment:
```bash
npm install
npm run start
```

## Notes / limitations
- This is a procedural first-pass 3D build using Three.js geometry and canvas-drawn stickman sprites. It is not a photoreal asset pack.
- The narration timing scaffold is generated from the approved 17-line script at 3.7 words/sec. It is approximate, not a forced-alignment transcript; check the rendered cut against the narration and adjust `src/story.ts` line frames if needed.
- GitHub Actions is the cloud render host; account minutes, artifact limits and billing depend on your GitHub plan. The workflow has not been executed in this environment, so the MP4 is not yet verified.
- The output code uses only original Pisa story elements and the requested stickman character style.

## Upload from Android with Termux
After extracting the ZIP, move into the `pisa-short` directory and run:
```bash
pkg update -y && pkg install git -y
cd /path/to/pisa-short
# Create an empty GitHub repository first, then use its HTTPS URL below.
git init -b main
git add .
git commit -m "Add Pisa Shorts Remotion project"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPOSITORY.git
git push -u origin main
```
GitHub may ask you to authenticate in a browser or use a Personal Access Token. Do not share that token with anyone. Once pushed, open the repository's Actions tab and run the workflow.
