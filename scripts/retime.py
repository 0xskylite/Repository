#!/usr/bin/env python3
"""Rewrite the LINE_F block of src/story.ts from the real voice timings.

Usage:  python scripts/retime.py voice/words.json [--story src/story.ts] [--tail 0.10]

words.json = [{"w": "This", "s": 0.00, "e": 0.21}, ...] (any speech-to-text with word times; hand-fix it first).
Each script line of voice/VOICE.txt starts at the first word the voice says for it. The speech-to-text words are
aligned to the script words (difflib), so small tokenisation differences (numbers, apostrophes) are tolerated.
The end frame is the end of the last word + --tail seconds (the video ends on the last word)."""
import argparse, difflib, json, math, os, re, sys

FPS = 30
ap = argparse.ArgumentParser()
ap.add_argument("words")
ap.add_argument("--story", default="src/story.ts")
ap.add_argument("--script", default="voice/VOICE.txt")
ap.add_argument("--tail", type=float, default=0.10)
ap.add_argument("--dry", action="store_true", help="print only, do not write")
a = ap.parse_args()

norm = lambda w: re.sub(r"[^a-z0-9]", "", w.lower())
lines = [l for l in open(a.script, encoding="utf-8").read().split("\n") if l.strip()]
script_words, line_of_first = [], []
for l in lines:
    line_of_first.append(len(script_words))
    script_words += [norm(w) for w in l.split() if norm(w)]
stt = json.load(open(a.words, encoding="utf-8"))
stt_norm = [norm(w["w"]) for w in stt]
sm = difflib.SequenceMatcher(None, script_words, stt_norm, autojunk=False)
amap = {}
for blk in sm.get_matching_blocks():
    for k in range(blk.size):
        amap[blk.a + k] = blk.b + k
cover = len(amap) / len(script_words)
if cover < 0.85:
    sys.exit(f"only {cover:.0%} of the script words matched the voice words: fix words.json (or VOICE.txt) first")
starts = []
for i, first in enumerate(line_of_first):
    j = first
    while j not in amap and j < len(script_words):  # first word unmatched: use the next matched word of the line
        j += 1
    if j not in amap:
        sys.exit(f"line {i + 1} could not be aligned")
    starts.append(float(stt[amap[j]]["s"]))
if starts[0] > 0.2:
    print(f"note: the voice starts at {starts[0]:.2f} s; the picture starts at frame 0 (reference shorts start the voice at frame 1-4)")
starts[0] = 0.0
end = float(stt[-1]["e"]) + a.tail
frames = [int(round(t * FPS)) for t in starts] + [int(math.ceil(end * FPS))]
for i in range(1, len(frames)):
    if frames[i] <= frames[i - 1]:
        sys.exit(f"line {i} would have no frames; check words.json")
print("LINE_F =", frames)
print("shot lengths (f):", [frames[i + 1] - frames[i] for i in range(len(frames) - 1)])
print(f"total {frames[-1]} f = {frames[-1] / FPS:.2f} s ({cover:.0%} of script words matched)")
if a.dry:
    sys.exit(0)
src = open(a.story, encoding="utf-8").read()
new = re.sub(r"(// LINES:BEGIN[^\n]*\n)export const LINE_F = \[[^\]]*\];\n(// LINES:END)",
             lambda m: f"{m.group(1)}export const LINE_F = [{', '.join(map(str, frames))}];\n{m.group(2)}", src)
if new == src:
    print("LINE_F block already up to date (or markers missing)")
open(a.story, "w", encoding="utf-8").write(new)
print("wrote", a.story, "- now run: npx tsx scripts/check_story.ts   (every camera key must sit inside its shot)")
