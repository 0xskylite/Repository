#!/usr/bin/env python3
"""Original soundtrack for "The Tower That Was Saved by Quitting": synthesized SFX + an original score, timed to src/story.ts.

Usage (from the project folder):
    python audio/pisa_audio.py                 # bed only (no voice yet) + events.csv + cues.md
    python audio/pisa_audio.py --voice voice/voice.wav --words voice/words.json

Everything is numpy/scipy only. Picture times come from src/story.ts (LINE_F, hammer and floor beats), so re-run after retiming.
Mix rule (house rule): voice unchanged, music +3 dB, SFX -6 dB relative to their base levels below.
Outputs (48 kHz stereo 24-bit WAV, exact picture length): mix.wav, stem_music.wav, stem_sfx.wav, (stem_voice.wav), events.csv, cues.md"""
import argparse, csv, json, math, os, re, sys, wave
import numpy as np
from scipy import signal

SR, FPS = 48000, 30
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
ap = argparse.ArgumentParser()
ap.add_argument("--story", default=os.path.join(ROOT, "src", "story.ts"))
ap.add_argument("--voice")
ap.add_argument("--words")
ap.add_argument("--out", default=HERE)
ap.add_argument("--seed", type=int, default=7)
args = ap.parse_args()

# ---------------------------------------------------------------- picture timeline (parsed from story.ts)
src = open(args.story, encoding="utf-8").read()
LINE_F = [int(x) for x in re.search(r"export const LINE_F = \[([^\]]*)\]", src).group(1).split(",")]
TOTAL = LINE_F[-1]
DUR = TOTAL / FPS
N = int(round(DUR * SR))
HAMMER_FREEZE = int(re.search(r"HAMMER_FREEZE = (\d+)", src).group(1))
HAMMER_DROP = int(re.search(r"HAMMER_DROP = (\d+)", src).group(1))
FLOOR_BEATS = [float(x) for x in re.search(r"FLOOR_BEATS = \[([^\]]*)\]", src).group(1).split(",")]
Lf = lambda n: LINE_F[n - 1]
Ls = lambda n, off=0: (Lf(n) + off) / FPS            # seconds at an offset (frames) into shot n
Dur = lambda n: (Lf(n + 1) - Lf(n)) / FPS
R = np.random.default_rng(args.seed)

dbg = lambda db: 10.0 ** (db / 20.0)
tt = lambda d: np.arange(int(d * SR)) / SR


# ---------------------------------------------------------------- small DSP kit
def lp(x, f, o=2): return signal.sosfilt(signal.butter(o, min(f, SR * 0.45), "lowpass", fs=SR, output="sos"), x)
def hp(x, f, o=2): return signal.sosfilt(signal.butter(o, f, "highpass", fs=SR, output="sos"), x)
def bp(x, f0, f1, o=2): return signal.sosfilt(signal.butter(o, [f0, min(f1, SR * 0.45)], "bandpass", fs=SR, output="sos"), x)
def noise(d): return R.standard_normal(int(d * SR))
def env(n, a=0.005, d=0.2, curve=3.0):
    t = np.arange(n) / SR
    e = np.minimum(1.0, t / max(a, 1e-4)) * np.exp(-curve * t / max(d, 1e-3))
    return e


def ov(*sigs):
    """overlay signals of different lengths (all start together)"""
    n = max(len(x) for x in sigs)
    out = np.zeros(n)
    for x in sigs:
        out[:len(x)] += x
    return out


def thump(f0=95, f1=45, d=0.35, click=0.25):
    t = tt(d)
    ph = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t * 30)) / SR
    return (np.sin(ph) + click * lp(noise(d), 1800) * np.exp(-t * 60)) * env(len(t), 0.002, d * 0.35, 4)


def stone_hit(d=0.5):
    """marble block set down: low thump + a short stony knock (modal partials) + dust"""
    t = tt(d)
    knock = sum(a * np.sin(2 * np.pi * f * t) * np.exp(-t * k) for f, a, k in [(310, 0.5, 26), (540, 0.35, 34), (910, 0.25, 48), (1480, 0.12, 70)])
    dust = bp(noise(d), 1200, 6000) * np.exp(-t * 11) * 0.25
    return 0.9 * thump(85, 42, d) + 0.5 * knock + dust


def whoosh(d=0.6, f0=500, f1=5000):
    t = tt(d)
    n = noise(d)
    sweep = np.zeros_like(n)
    for lo in range(0, len(n), 2400):                       # moving band-pass in 50 ms steps
        fc = f0 * (f1 / f0) ** (lo / len(n))
        sweep[lo:lo + 2400] = bp(n[lo:lo + 2400 + 1], fc * 0.7, fc * 1.4)[:len(n[lo:lo + 2400])]
    return sweep * np.sin(np.pi * np.linspace(0, 1, len(n))) ** 2


def ping(f=1800, d=0.35):
    t = tt(d)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 2.4 * t)) * np.exp(-t * 18) * np.minimum(1, t / 0.002)


def drip(f=1500, d=0.25):
    t = tt(d)
    return np.sin(2 * np.pi * (f + 900 * np.exp(-t * 40)) * t) * np.exp(-t * 28) * np.minimum(1, t / 0.002)


def squelch(d=0.6):
    t = tt(d)
    return bp(noise(d), 250, 1600) * (0.6 + 0.4 * np.sin(2 * np.pi * 9 * t)) * np.exp(-t * 3.2) * np.minimum(1, t / 0.02)


def chirp(f0=3400, f1=4600, d=0.12):
    t = tt(d)
    f = f0 + (f1 - f0) * (t / d)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.sin(np.pi * t / d) ** 1.5


def scoop(d=0.5):
    t = tt(d)
    return ov(bp(noise(d), 300, 2500) * np.exp(-t * 6) * 0.7, 0.4 * lp(noise(d), 400) * np.exp(-t * 16))


def creak(d=0.9):
    t = tt(d)
    f = 180 + 70 * np.sin(2 * np.pi * 3.3 * t) + 60 * t
    saw = signal.sawtooth(2 * np.pi * np.cumsum(f) / SR)
    return bp(saw, 300, 1400) * np.sin(np.pi * t / d) * 0.5


def tick(d=0.08):
    t = tt(d)
    return bp(noise(d), 2500, 7000) * np.exp(-t * 70) + 0.4 * np.sin(2 * np.pi * 1900 * t) * np.exp(-t * 90)


def foot(d=0.28):
    return 0.8 * thump(120, 55, d) + 0.25 * bp(noise(d), 1800, 7000) * np.exp(-tt(d) * 45)   # boot on stone + buckle clink


def frame_drum(d=0.5, f=70):
    t = tt(d)
    return (0.9 * thump(f * 1.5, f, d, 0.1) + 0.3 * bp(noise(d), 200, 900) * np.exp(-t * 14))


def pluck(f, d=0.9, bright=1.0):
    t = tt(d)
    out = np.zeros_like(t)
    for k, (m, a, dec) in enumerate([(1, 1.0, 3.2), (2.003, 0.5, 4.5), (3.01, 0.28, 6.0), (4.02, 0.15, 8.0), (5.03, 0.08, 10.0)]):
        out += a * bright ** k * np.sin(2 * np.pi * f * m * t) * np.exp(-t * dec)
    return out * np.minimum(1, t / 0.003)


def pad(freqs, d, level=1.0):
    t = tt(d)
    out = np.zeros_like(t)
    for f in freqs:
        for det in (-0.004, 0.0, 0.004):
            out += np.sin(2 * np.pi * f * (1 + det) * t + R.uniform(0, 6.28)) / 3
    sw = 0.8 + 0.2 * np.sin(2 * np.pi * 0.23 * t)
    a = np.minimum(1, t / 0.6) * np.minimum(1, (d - t) / 0.8)
    return lp(out, 1800) * sw * a * level / max(1, len(freqs)) ** 0.5


# ---------------------------------------------------------------- mixing buffers
def stereo(): return np.zeros((2, N))


def put(buf, sig, t0, db=0.0, pan=0.0):
    i = int(round(t0 * SR))
    if i >= N or i + len(sig) <= 0:
        return
    a, b = max(0, -i), min(len(sig), N - i)
    g = dbg(db)
    l, r = math.cos((pan + 1) * math.pi / 4), math.sin((pan + 1) * math.pi / 4)
    buf[0, i + a:i + b] += sig[a:b] * g * l * math.sqrt(2)
    buf[1, i + a:i + b] += sig[a:b] * g * r * math.sqrt(2)


def reverb_send(buf, amt=0.18, size=0.9):
    ir = noise(size) * np.exp(-tt(size) * 5.2)
    ir = lp(ir, 5200)
    wet = np.stack([signal.fftconvolve(buf[c], ir * (1 if c == 0 else -1))[:N] for c in range(2)])
    return buf + wet * amt / (np.abs(ir).sum() ** 0.5 + 1e-9) * 6


# ---------------------------------------------------------------- SFX event table (also written to events.csv)
EV = []   # (t seconds, name, gain dB, pan, fn)


def ev(t, name, fn, db=0.0, pan=0.0): EV.append((t, name, fn, db, pan))


# shot 1 / 2: today, then the flash whoosh into 1173
ev(Ls(1, 8), "crowd murmur + shutter", lambda: bp(noise(2.4), 300, 3000) * env(int(2.4 * SR), 0.5, 1.4, 1.5) * 0.5, -10)
for k, dt in enumerate([0.5, 1.7, 2.6]):
    ev(Ls(1, 0) + dt, "camera shutter", tick, -12, [-0.5, 0.4, 0.1][k])
ev(Ls(2) - 0.18, "flash whoosh", lambda: whoosh(0.5, 400, 7000), -6)
ev(Ls(2), "flash stinger", lambda: ov(ping(2200, 0.5), 0.4 * ping(3300, 0.5)), -10)
for k in range(6):                                              # shot 2: stones laid
    ev(Ls(2, 90 + k * 11), "first stone", lambda: stone_hit(0.4) * 0.6, -9 - k * 0.5, R.uniform(-0.4, 0.4))
# shot 3: three floors pop up (matches FLOOR_BEATS / KICKS)
for i, b in enumerate(FLOOR_BEATS):
    t0 = (Lf(3) + b * (Lf(4) - Lf(3))) / FPS
    ev(t0 - 0.12, f"floor {i + 1} rise", lambda: whoosh(0.28, 200, 1800) * 0.7, -10)
    ev(t0, f"floor {i + 1} lands", lambda: stone_hit(0.6), -2 - 0 * i)
    ev(t0 + 0.05, f"floor {i + 1} dust", lambda: bp(noise(0.7), 900, 5000) * env(int(0.7 * SR), 0.02, 0.4, 2.5) * 0.4, -12)
# shot 4: the ground gives
for k in range(4):
    ev(Ls(4, 10 + k * 18), "clay squish", lambda: squelch(0.5), -9 - k * 0.8, 0.0)
ev(Ls(4, 30), "foundation groan", lambda: creak(1.2) * 0.9, -9)
# shot 5: plumb bob swings, gasps
for k in range(3):
    ev(Ls(5, 6 + k * 18), "plumb creak", lambda: creak(0.5) * 0.6, -13, 0.2)
ev(Ls(5, 30), "crowd gasp", lambda: bp(noise(0.7), 500, 2800) * env(int(0.7 * SR), 0.1, 0.35, 2.5) * 0.8, -9)
# shot 6: hammer swing -> freeze (silence) -> drop; idle masons sit
ev(Ls(6, 6), "hammer swing up", lambda: whoosh(0.35, 300, 2400), -10)
ev(Ls(6, HAMMER_DROP), "hammer lands", lambda: ov(stone_hit(0.9) * 1.2, 0.5 * tick()), -1)
ev(Ls(6, HAMMER_DROP + 6), "tools clatter", lambda: ov(*[np.pad(tick() * 0.7, (int(d * SR), 0)) for d in (0.0, 0.09, 0.2, 0.31)]), -7)
ev(Ls(6, HAMMER_DROP + 22), "masons sit", lambda: lp(noise(0.5), 700) * env(int(0.5 * SR), 0.02, 0.3, 3) * 0.7, -9)
# shots 7 and 9: soldiers march (footfalls every 0.5 s), banners
def marching(a, b, db):
    k = 0
    t = Ls(a, 0)
    while t < Ls(b + 1, 0):
        ev(t, "march step", foot, db + (0.8 if k % 2 == 0 else 0.0), -0.5 + (k % 2) * 1.0 * 0.4)
        t += 0.5
        k += 1
marching(7, 7, -7)
marching(9, 9, -4)
ev(Ls(7, 4), "banner flap", lambda: bp(noise(2.0), 400, 2200) * (0.5 + 0.5 * np.sin(2 * np.pi * 7 * tt(2.0))) * env(int(2.0 * SR), 0.2, 1.4, 1.4) * 0.5, -14)
for k, f0 in enumerate([Ls(7, 40), Ls(7, 70)]):
    ev(f0, "distant clank", lambda: ov(ping(1150, 0.4) * 0.5, tick()), -16, 0.7)
# shot 8: stillness: wind + birds
ev(Ls(8, 0), "quiet wind", lambda: lp(noise(Dur(8) + 0.6), 700, 2) * env(int((Dur(8) + 0.6) * SR), 0.6, 4.0, 0.5) * 0.35, -14)
for k, dt in enumerate([0.4, 0.95, 1.2, 2.1]):
    ev(Ls(8, 0) + dt, "bird", lambda: chirp(3300, 4700, 0.1), -17, -0.6 + 0.4 * k)
# shot 9: "Unluckily" sting
ev(Ls(9, 8), "unlucky sting", lambda: ov(thump(70, 38, 0.8) * 0.9, lp(noise(0.5), 500) * env(int(0.5 * SR), 0.01, 0.2, 4) * 0.3), -5)
# shot 10: wet sponge squeeze
ev(Ls(10, 14), "sponge press", lambda: squelch(0.5), -8)
for k in range(7):
    ev(Ls(10, 28 + k * 5), "sponge drip", lambda: drip(R.uniform(1100, 2000)), -12 + R.uniform(-2, 1), R.uniform(-0.3, 0.3))
# shot 11: wet beach: waves, foot sinks, water squeezes out
ev(Ls(11, 0), "small waves", lambda: lp(noise(Dur(11) + 0.4), 1400, 2) * (0.5 + 0.5 * np.sin(2 * np.pi * 0.28 * tt(Dur(11) + 0.4))) * 0.4, -14)
ev(Ls(11, 24), "foot sinks", lambda: squelch(0.8) * 1.1, -6)
for k in range(8):
    ev(Ls(11, 44 + k * 6), "water squeezes out", lambda: drip(R.uniform(900, 1700)), -13 + R.uniform(-2, 1), R.uniform(-0.4, 0.4))
ev(Ls(11, 112), "print firms", lambda: ov(thump(120, 70, 0.25) * 0.5, tick() * 0.5), -10)
# shot 12: clay squeezes water out and firms
for k in range(18):
    ev(Ls(12, 14 + k * 6.5), "clay drop", lambda: drip(R.uniform(800, 1500)), -14 + R.uniform(-2, 1.5), R.uniform(-0.6, 0.6))
ev(Ls(12, 18), "squeeze creak", lambda: creak(1.4) * 0.5, -12)
ev(Ls(12, 120), "clay firms", lambda: ov(ping(660, 1.0) * 0.3, ping(990, 1.0) * 0.2), -14)
# shot 13: a hundred years: wind, ivy, church bells far away
ev(Ls(13, 0), "wind", lambda: lp(noise(Dur(13) + 0.4), 900, 2) * env(int((Dur(13) + 0.4) * SR), 0.5, 3.0, 0.6) * 0.4, -13)
for k in range(3):
    ev(Ls(13, 20 + k * 36), "far bell", lambda: ov(ping(520, 1.8) * 0.6, ping(1040, 1.8) * 0.2), -17, 0.5)
# shot 14: builders return: lifting, chisels, taller blocks
ev(Ls(14, 0), "workers return", lambda: bp(noise(2.0), 300, 3000) * env(int(2.0 * SR), 0.4, 1.2, 1.5) * 0.4, -14)
for k in range(5):
    ev(Ls(14, 20 + k * 30), "chisel", lambda: ov(tick(), 0.5 * ping(2300, 0.15)), -11, R.uniform(-0.5, 0.5))
for k in range(3):
    ev(Ls(14, 40 + k * 44), "block set", lambda: stone_hit(0.5), -7, R.uniform(-0.3, 0.3))
# shot 15: engineers: plumb still; a single beep
ev(Ls(15, 4), "plumb stops", lambda: ping(880, 0.8) * 0.4, -13)
ev(Ls(15, 40), "radio beep", lambda: ov(ping(1500, 0.12), np.pad(ping(1500, 0.12), (int(0.2 * SR), 0))), -15, 0.3)
# shot 16: soil extraction tubes + shovel
for k in range(5):
    ev(Ls(16, 6 + k * 14), "soil pulled up", lambda: scoop(0.6), -9 - 0.5 * k, -0.4)
ev(Ls(16, 44), "shovel", lambda: ov(scoop(0.5), tick() * 0.4), -7, 0.2)
ev(Ls(16, 60), "tower nudges", lambda: ov(creak(1.0) * 0.5, thump(60, 35, 0.6) * 0.3), -12)
# shot 17: tourists, the hole, final stinger
ev(Ls(17, 0), "tourist chatter", lambda: bp(noise(2.0), 300, 3200) * env(int(2.0 * SR), 0.4, 1.2, 1.5) * 0.5, -13)
for k, dt in enumerate([0.9, 1.6]):
    ev(Ls(17, 0) + dt, "camera shutter", tick, -13, [0.3, -0.3][k])
ev((TOTAL - 14) / FPS, "final thump", lambda: ov(thump(80, 40, 0.8), 0.3 * ping(2000, 0.3)), -4)

sfx = stereo()
for t, name, fn, db, pan in EV:
    s = np.asarray(fn(), float)
    put(sfx, s / (np.max(np.abs(s)) + 1e-9) * 0.5, t, db, pan)      # every event normalised to 0.5 FS, then its own dB
sfx = reverb_send(sfx, 0.14)

# ---------------------------------------------------------------- music (original, D dorian -> D major at the end)
mus = stereo()
BPM = 100.0
BEAT = 60.0 / BPM
midi = lambda m: 440.0 * 2 ** ((m - 69) / 12)
CH = {"Dm": [50, 53, 57, 62], "C": [48, 52, 55, 60], "Gm": [43, 50, 55, 58], "Am": [45, 52, 57, 60], "Bb": [46, 50, 53, 58],
      "D": [50, 54, 57, 62], "G": [43, 50, 55, 59], "A": [45, 52, 57, 61]}


def arp(t0, t1, prog, step=0.5, vel=-14, bright=1.0, bass=True):
    """eighth-note arpeggio over a progression (a chord per bar of 4 beats)"""
    t, i, bar = t0, 0, 0
    pat = [0, 1, 2, 3, 2, 1, 2, 1]
    while t < t1 - 1e-6:
        ch = CH[prog[int(((t - t0) / (4 * BEAT)) % len(prog))]]
        k = int(round((t - t0) / (step * BEAT)))
        n = ch[pat[k % 8] % 4] + 12
        put(mus, pluck(midi(n), 0.8, bright), t, vel + (2 if k % 4 == 0 else 0), -0.2 + 0.4 * ((k % 8) / 8))
        if bass and k % 4 == 0:
            put(mus, pluck(midi(ch[0] - 12), 1.1, 0.5), t, vel + 3, 0.0)
        t += step * BEAT


def padchord(t0, t1, prog, db=-26):
    bar = 4 * BEAT
    t, i = t0, 0
    while t < t1 - 0.01:
        ch = CH[prog[i % len(prog)]]
        d = min(bar, t1 - t) + 0.4
        put(mus, pad([midi(n) for n in ch], d), t, db)
        t += bar
        i += 1


S = {n: (Ls(n), Ls(n + 1)) for n in range(1, 18)}
# intro: bright and light
arp(S[1][0], S[3][0], ["Dm", "C"], vel=-17, bright=1.1)
padchord(S[1][0], S[3][0], ["Dm", "C"], -29)
# building: the same tune, fuller, with a soft pulse
arp(S[3][0], Ls(6, HAMMER_FREEZE), ["Dm", "C", "Gm", "Am"], vel=-15)
padchord(S[3][0], Ls(6, HAMMER_FREEZE), ["Dm", "C", "Gm", "Am"], -28)
for b in np.arange(S[3][0], S[5][0], BEAT * 2):
    put(mus, frame_drum(0.3, 90) * 0.4, b, -17, 0)
# dropout on "stop": silence from the freeze until the hammer drops, then a single low pad note
put(mus, pad([midi(38)], 3.0), Ls(6, HAMMER_DROP + 4), -26)
# wars: minor, frame drum on every beat, low drone
arp(S[7][0], S[8][0], ["Dm", "Bb", "Gm", "Am"], step=1.0, vel=-17, bright=0.7, bass=False)
padchord(S[7][0], S[8][0], ["Dm", "Bb"], -25)
for b in np.arange(S[7][0], S[8][0], BEAT):
    put(mus, frame_drum(0.4, 70) * 0.8, b, -9 + (3 if round((b - S[7][0]) / BEAT) % 2 == 0 else 0), 0)
# "Luckily": drum out, two held notes + pad (stillness)
padchord(S[8][0], S[9][0], ["Dm"], -27)
put(mus, pluck(midi(62), 2.5, 0.6), S[8][0] + 0.4, -22, -0.3)
put(mus, pluck(midi(57), 2.5, 0.6), S[8][0] + 1.6, -23, 0.3)
# "Unluckily": drum + drone return heavier
for b in np.arange(S[9][0], S[10][0], BEAT):
    put(mus, frame_drum(0.4, 62) * 1.0, b, -12, 0)
padchord(S[9][0], S[10][0], ["Dm"], -23)
# explanation: playful staccato plucks, major-ish colour (D, G, A)
arp(S[10][0], S[12][0] + 0.001, ["D", "G", "Am", "D"], step=0.5, vel=-17, bright=1.2, bass=True)
padchord(S[10][0], S[13][0], ["D", "G"], -29)
# squeeze rising run on "wet sponge"
for k, n in enumerate([62, 64, 66, 69, 71, 74]):
    put(mus, pluck(midi(n), 0.5, 1.2), Ls(10, 20) + k * 0.1, -18, -0.5 + 0.2 * k)
# a hundred years: slow pad + sparse plucks, golden
padchord(S[12][0] + 0.001, S[14][0], ["Dm", "Bb", "Gm", "Am"], -17)
for k, (dt, n) in enumerate([(0.3, 69), (1.9, 65), (3.3, 62)]):
    put(mus, pluck(midi(n), 2.2, 0.7), S[13][0] + dt, -17, 0.3 * (k - 1))
# builders return: the main tune again in major, building to the resolve
arp(S[14][0], S[15][0], ["D", "G", "A", "D"], vel=-15, bright=1.2)
padchord(S[14][0], S[15][0], ["D", "G", "A", "D"], -27)
# engineers + dig: warm and steady
arp(S[15][0], S[17][0], ["D", "G", "A", "D"], vel=-16, bright=1.0)
padchord(S[15][0], S[17][0], ["D", "G", "A", "D"], -26)
for b in np.arange(S[16][0], S[17][0], BEAT * 2):
    put(mus, frame_drum(0.3, 90) * 0.3, b, -19, 0)
# last shot: the tune again, resolves on the last word with a long D major chord
arp(S[17][0], (TOTAL - 20) / FPS, ["D", "G"], vel=-15, bright=1.2)
padchord(S[17][0], DUR, ["D"], -22)
for k, n in enumerate([50, 57, 62, 66, 69]):
    put(mus, pluck(midi(n), 3.0, 0.9), (TOTAL - 14) / FPS + 0.02 * k, -16, -0.4 + 0.2 * k)
mus = reverb_send(mus, 0.22, 1.2)

# ---------------------------------------------------------------- voice, ducking, levels, mix
def read_wav(p):
    with wave.open(p, "rb") as w:
        n, ch, sw, sr = w.getnframes(), w.getnchannels(), w.getsampwidth(), w.getframerate()
        raw = w.readframes(n)
    a = np.frombuffer(raw, np.int16 if sw == 2 else np.int32 if sw == 4 else np.uint8).astype(np.float64)
    a = a.reshape(-1, ch).mean(1) / (2 ** (8 * sw - 1))
    if sr != SR:
        a = signal.resample_poly(a, SR, sr)
    return a


def write_wav(p, x):
    y = np.clip(x, -1, 1)
    pcm = (y.T * 8388607).astype(np.int32)
    b = bytearray()
    for v in pcm.reshape(-1):
        b += int(v).to_bytes(4, "little", signed=True)[:3]
    with wave.open(p, "wb") as w:
        w.setnchannels(2); w.setsampwidth(3); w.setframerate(SR)
        w.writeframes(bytes(b))


def lufs(x):
    """simple BS.1770 integrated loudness (K-weighting, gated), stereo"""
    b1 = [1.53512485958697, -2.69169618940638, 1.19839281085285]; a1 = [1.0, -1.69065929318241, 0.73248077421585]
    b2 = [1.0, -2.0, 1.0]; a2 = [1.0, -1.99004745483398, 0.99007225036621]
    k = np.stack([signal.lfilter(b2, a2, signal.lfilter(b1, a1, c)) for c in x])
    blk, hop = int(0.4 * SR), int(0.1 * SR)
    z = [np.sum(np.mean(k[:, i:i + blk] ** 2, axis=1)) for i in range(0, k.shape[1] - blk + 1, hop)]
    z = np.array(z)
    l = -0.691 + 10 * np.log10(z + 1e-12)
    g = z[l > -70]
    if not len(g): return -70.0
    th = -0.691 + 10 * np.log10(g.mean()) - 10
    g2 = z[l > th]
    return -0.691 + 10 * np.log10(g2.mean() + 1e-12) if len(g2) else -70.0


# base levels (before the house offsets): music -23 LUFS, SFX -23 LUFS, then music +3 dB and SFX -6 dB
mus *= dbg(-23 - lufs(mus)) if np.any(mus) else 1
sfx *= dbg(-23 - lufs(sfx)) if np.any(sfx) else 1
mus *= dbg(+3 - 3 - 0)       # +3 dB house offset, then -3 dB so the bed leaves room for the voice at -15 LUFS
sfx *= dbg(-6)

words = json.load(open(args.words)) if args.words else json.load(open(os.path.join(ROOT, "voice", "words_estimated.json")))
spans = []
for w in words:
    s, e = float(w["s"]), float(w["e"])
    if spans and s - spans[-1][1] < 0.3: spans[-1][1] = max(spans[-1][1], e)
    else: spans.append([s, e])
ctrl = np.zeros(N)
for s, e in spans:
    ctrl[max(0, int((s - 0.08) * SR)): int((e + 0.12) * SR)] = 1.0
kern = signal.windows.hann(int(0.35 * SR)); kern /= kern.sum()
duck = 1 - (1 - dbg(-3.0)) * np.convolve(ctrl, kern, "same")      # -3 dB music dip while the voice speaks
mus *= duck

voice = None
if args.voice:
    v = read_wav(args.voice)
    voice = np.zeros(N); voice[: min(N, len(v))] = v[:N]
    voice = np.stack([voice, voice])
    voice *= dbg(-15 - lufs(voice))                                 # voice unchanged except gain to -15 LUFS on its own
mix = mus + sfx + (voice if voice is not None else 0)
# master: gentle peak control (soft clip above -1.2 dBFS), then a loudness check
ceil = dbg(-1.2)
mix = np.tanh(mix / ceil) * ceil
os.makedirs(args.out, exist_ok=True)
write_wav(os.path.join(args.out, "mix.wav"), mix)
write_wav(os.path.join(args.out, "stem_music.wav"), mus)
write_wav(os.path.join(args.out, "stem_sfx.wav"), sfx)
if voice is not None: write_wav(os.path.join(args.out, "stem_voice.wav"), voice)
with open(os.path.join(args.out, "events.csv"), "w", newline="") as fh:
    w = csv.writer(fh); w.writerow(["time_s", "frame", "shot", "event", "gain_db", "pan"])
    for t, name, fn, db, pan in sorted(EV, key=lambda e: e[0]):
        shot = next((n for n in range(1, 18) if Lf(n) <= t * FPS < Lf(n + 1)), 17)
        w.writerow([f"{t:.3f}", int(round(t * FPS)), shot, name, f"{db:.1f}", f"{pan:.2f}"])
print(f"duration {N / SR:.3f} s ({TOTAL} f); {len(EV)} SFX events; mix {lufs(mix):.1f} LUFS (bed only: {lufs(mus + sfx):.1f}), "
      f"peak {20 * np.log10(np.max(np.abs(mix)) + 1e-12):.1f} dBFS; voice: {'yes' if voice is not None else 'NO (bed only)'}")
