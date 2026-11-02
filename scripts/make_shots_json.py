#!/usr/bin/env python3
"""Write out/pisa/shots.json for scripts/short_qa.py from src/story.ts (shots, flash, crossfades)."""
import json, re, sys
src = open("src/story.ts", encoding="utf-8").read()
L = [int(x) for x in re.search(r"LINE_F = \[([^\]]*)\]", src).group(1).split(",")]
xf = {int(k): int(v) for k, v in re.findall(r"(\d+):\s*(\d+)", re.search(r"XFADE[^=]*=\s*\{([^}]*)\}", src).group(1))}
shots = [{"id": i + 1, "a": L[i], "b": L[i + 1]} for i in range(len(L) - 1)]
meta = {"shots": shots, "flash": [L[1], L[1] + 4],
        "xfade": [[L[k - 1] - v // 2, L[k - 1] + v // 2 + 1] for k, v in xf.items()]}
out = sys.argv[1] if len(sys.argv) > 1 else "shots.json"
json.dump(meta, open(out, "w"), indent=1)
print("wrote", out, "-", len(shots), "shots,", len(meta["xfade"]), "crossfades")
