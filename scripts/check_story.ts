// Run after retiming:  npx tsx scripts/check_story.ts
import { TOTAL, LINE_F, SHOTS, camAt, dofAt, checkTimeline } from "../src/story";
const bad = checkTimeline();
let nan = 0;
for (let f = 0; f < TOTAL; f++) {
  const sh = SHOTS.find((s) => f >= s.a && f < s.b)!;
  const c = camAt(sh.id, f), d = dofAt(f);
  if (![...c.pos, ...c.look, c.fov, c.roll, d.cInf].every(Number.isFinite)) nan++;
}
console.log(`TOTAL ${TOTAL} f (${(TOTAL / 30).toFixed(2)} s); shot lengths:`, LINE_F.slice(1).map((v, i) => v - LINE_F[i]).join(" "));
console.log(bad.length ? "PROBLEMS:\n  " + bad.join("\n  ") : "timeline ok", "| NaN frames:", nan);
process.exit(bad.length || nan ? 1 : 0);
