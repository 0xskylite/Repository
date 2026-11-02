# Soundtrack cue sheet - "The Tower That Was Saved by Quitting"

All sound is original: synthesized with numpy/scipy by `audio/pisa_audio.py`, timed from `src/story.ts`. Re-run after retiming.

## Mix rule
Voice unchanged (gain only, -15 LUFS on its own), music +3 dB, SFX -6 dB from their base levels, music ducked -3 dB while the voice speaks (keyed from words.json).
Test with a stand-in voice: master -14.8 LUFS, true peak -4.1 dBFS, bed about 10 dB under the voice. Bed alone: -24.7 LUFS.

## Score map (original, 100 bpm, D dorian -> D major)
| shots | music |
|---|---|
| 1-2 | light plucked arpeggio, Dm / C, soft pad |
| 3-5 | same tune fuller, bass pluck, frame-drum pulse every 2 beats |
| 6 | **dropout** from the hammer freeze until it lands, then one low pad note |
| 7 | war: Dm / Bb / Gm / Am, frame drum on every beat, low drone |
| 8 | stillness: drum out, two held notes + pad ("Luckily") |
| 9 | drum + drone return heavier ("Unluckily") |
| 10-11 | playful staccato plucks in D / G / Am, rising run on the sponge squeeze |
| 12-13 | slow pad, sparse plucks (time passes) |
| 14-17 | the main tune again in major; last chord blooms on the final word |

## SFX events by shot (from events.csv)

### Shot 1 - hook (today) (frames 0-105)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 0.267 | 8 | crowd murmur + shutter | -10.0 | 0.00 |
| 0.500 | 15 | camera shutter | -12.0 | -0.50 |
| 1.700 | 51 | camera shutter | -12.0 | 0.40 |
| 2.600 | 78 | camera shutter | -12.0 | 0.10 |
| 3.320 | 100 | flash whoosh | -6.0 | 0.00 |

### Shot 2 - 1173 (frames 105-267)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 3.500 | 105 | flash stinger | -10.0 | 0.00 |
| 6.500 | 195 | first stone | -9.0 | 0.10 |
| 6.867 | 206 | first stone | -9.5 | 0.32 |
| 7.233 | 217 | first stone | -10.0 | 0.22 |
| 7.600 | 228 | first stone | -10.5 | -0.22 |
| 7.967 | 239 | first stone | -11.0 | -0.16 |
| 8.333 | 250 | first stone | -11.5 | 0.30 |

### Shot 3 - three floors (frames 267-364)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 9.233 | 277 | floor 1 rise | -10.0 | 0.00 |
| 9.353 | 281 | floor 1 lands | -2.0 | 0.00 |
| 9.403 | 282 | floor 1 dust | -12.0 | 0.00 |
| 10.397 | 312 | floor 2 rise | -10.0 | 0.00 |
| 10.517 | 316 | floor 2 lands | -2.0 | 0.00 |
| 10.567 | 317 | floor 2 dust | -12.0 | 0.00 |
| 11.528 | 346 | floor 3 rise | -10.0 | 0.00 |
| 11.648 | 349 | floor 3 lands | -2.0 | 0.00 |
| 11.698 | 351 | floor 3 dust | -12.0 | 0.00 |

### Shot 4 - the ground gives (frames 364-462)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 12.467 | 374 | clay squish | -9.0 | 0.00 |
| 13.067 | 392 | clay squish | -9.8 | 0.00 |
| 13.133 | 394 | foundation groan | -9.0 | 0.00 |
| 13.667 | 410 | clay squish | -10.6 | 0.00 |
| 14.267 | 428 | clay squish | -11.4 | 0.00 |

### Shot 5 - plumb line (frames 462-527)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 15.600 | 468 | plumb creak | -13.0 | 0.20 |
| 16.200 | 486 | plumb creak | -13.0 | 0.20 |
| 16.400 | 492 | crowd gasp | -9.0 | 0.00 |
| 16.800 | 504 | plumb creak | -13.0 | 0.20 |

### Shot 6 - just stop (frames 527-616)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 17.767 | 533 | hammer swing up | -10.0 | 0.00 |
| 20.167 | 605 | hammer lands | -1.0 | 0.00 |
| 20.367 | 611 | tools clatter | -7.0 | 0.00 |

### Shot 7 - wars (frames 616-729)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 20.533 | 616 | march step | -6.2 | -0.50 |
| 20.667 | 620 | banner flap | -14.0 | 0.00 |
| 20.900 | 627 | masons sit | -9.0 | 0.00 |
| 21.033 | 631 | march step | -7.0 | -0.10 |
| 21.533 | 646 | march step | -6.2 | -0.50 |
| 21.867 | 656 | distant clank | -16.0 | 0.70 |
| 22.033 | 661 | march step | -7.0 | -0.10 |
| 22.533 | 676 | march step | -6.2 | -0.50 |
| 22.867 | 686 | distant clank | -16.0 | 0.70 |
| 23.033 | 691 | march step | -7.0 | -0.10 |
| 23.533 | 706 | march step | -6.2 | -0.50 |
| 24.033 | 721 | march step | -7.0 | -0.10 |

### Shot 8 - Luckily (frames 729-818)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 24.300 | 729 | quiet wind | -14.0 | 0.00 |
| 24.700 | 741 | bird | -17.0 | -0.60 |
| 25.250 | 758 | bird | -17.0 | -0.20 |
| 25.500 | 765 | bird | -17.0 | 0.20 |
| 26.400 | 792 | bird | -17.0 | 0.60 |

### Shot 9 - Unluckily (frames 818-883)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 27.267 | 818 | march step | -3.2 | -0.50 |
| 27.533 | 826 | unlucky sting | -5.0 | 0.00 |
| 27.767 | 833 | march step | -4.0 | -0.10 |
| 28.267 | 848 | march step | -3.2 | -0.50 |
| 28.767 | 863 | march step | -4.0 | -0.10 |
| 29.267 | 878 | march step | -3.2 | -0.50 |

### Shot 10 - wet sponge (frames 883-956)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 29.900 | 897 | sponge press | -8.0 | 0.00 |
| 30.367 | 911 | sponge drip | -14.0 | 0.19 |
| 30.533 | 916 | sponge drip | -11.6 | -0.02 |
| 30.700 | 921 | sponge drip | -13.1 | -0.13 |
| 30.867 | 926 | sponge drip | -13.2 | -0.03 |
| 31.033 | 931 | sponge drip | -12.5 | 0.03 |
| 31.200 | 936 | sponge drip | -11.0 | 0.18 |
| 31.367 | 941 | sponge drip | -12.1 | 0.29 |

### Shot 11 - wet beach (frames 956-1127)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 31.867 | 956 | small waves | -14.0 | 0.00 |
| 32.667 | 980 | foot sinks | -6.0 | 0.00 |
| 33.333 | 1000 | water squeezes out | -14.4 | -0.27 |
| 33.533 | 1006 | water squeezes out | -13.2 | -0.36 |
| 33.733 | 1012 | water squeezes out | -14.9 | 0.01 |
| 33.933 | 1018 | water squeezes out | -13.6 | 0.33 |
| 34.133 | 1024 | water squeezes out | -13.1 | 0.01 |
| 34.333 | 1030 | water squeezes out | -13.5 | -0.20 |
| 34.533 | 1036 | water squeezes out | -15.0 | -0.25 |
| 34.733 | 1042 | water squeezes out | -12.9 | -0.24 |
| 35.600 | 1068 | print firms | -10.0 | 0.00 |

### Shot 12 - clay firms (frames 1127-1289)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 38.033 | 1141 | clay drop | -14.7 | -0.60 |
| 38.167 | 1145 | squeeze creak | -12.0 | 0.00 |
| 38.250 | 1148 | clay drop | -13.1 | -0.41 |
| 38.467 | 1154 | clay drop | -15.1 | 0.46 |
| 38.683 | 1160 | clay drop | -14.2 | 0.42 |
| 38.900 | 1167 | clay drop | -13.8 | 0.29 |
| 39.117 | 1174 | clay drop | -15.7 | 0.05 |
| 39.333 | 1180 | clay drop | -14.2 | 0.45 |
| 39.550 | 1186 | clay drop | -14.7 | 0.12 |
| 39.767 | 1193 | clay drop | -15.8 | -0.13 |
| 39.983 | 1200 | clay drop | -14.9 | -0.42 |
| 40.200 | 1206 | clay drop | -13.1 | -0.14 |
| 40.417 | 1212 | clay drop | -12.6 | 0.11 |
| 40.633 | 1219 | clay drop | -13.9 | 0.17 |
| 40.850 | 1226 | clay drop | -13.6 | -0.42 |
| 41.067 | 1232 | clay drop | -14.5 | -0.31 |
| 41.283 | 1238 | clay drop | -14.6 | -0.48 |
| 41.500 | 1245 | clay drop | -12.6 | -0.34 |
| 41.567 | 1247 | clay firms | -14.0 | 0.00 |
| 41.717 | 1252 | clay drop | -13.6 | -0.24 |

### Shot 13 - a hundred years later (frames 1289-1410)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 42.967 | 1289 | wind | -13.0 | 0.00 |
| 43.633 | 1309 | far bell | -17.0 | 0.50 |
| 44.833 | 1345 | far bell | -17.0 | 0.50 |
| 46.033 | 1381 | far bell | -17.0 | 0.50 |

### Shot 14 - builders return (frames 1410-1597)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 47.000 | 1410 | workers return | -14.0 | 0.00 |
| 47.667 | 1430 | chisel | -11.0 | 0.37 |
| 48.333 | 1450 | block set | -7.0 | 0.24 |
| 48.667 | 1460 | chisel | -11.0 | 0.16 |
| 49.667 | 1490 | chisel | -11.0 | -0.37 |
| 49.800 | 1494 | block set | -7.0 | 0.04 |
| 50.667 | 1520 | chisel | -11.0 | 0.35 |
| 51.267 | 1538 | block set | -7.0 | -0.21 |
| 51.667 | 1550 | chisel | -11.0 | 0.44 |

### Shot 15 - 2008, stopped (frames 1597-1710)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 53.367 | 1601 | plumb stops | -13.0 | 0.00 |
| 54.567 | 1637 | radio beep | -15.0 | 0.30 |

### Shot 16 - digging (frames 1710-1799)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 57.200 | 1716 | soil pulled up | -9.0 | -0.40 |
| 57.667 | 1730 | soil pulled up | -9.5 | -0.40 |
| 58.133 | 1744 | soil pulled up | -10.0 | -0.40 |
| 58.467 | 1754 | shovel | -7.0 | 0.20 |
| 58.600 | 1758 | soil pulled up | -10.5 | -0.40 |
| 59.000 | 1770 | tower nudges | -12.0 | 0.00 |
| 59.067 | 1772 | soil pulled up | -11.0 | -0.40 |

### Shot 17 - saved by a hole (frames 1799-1922)
| time s | frame | event | dB | pan |
|---|---|---|---|---|
| 59.967 | 1799 | tourist chatter | -13.0 | 0.00 |
| 60.867 | 1826 | camera shutter | -13.0 | 0.30 |
| 61.567 | 1847 | camera shutter | -13.0 | -0.30 |
| 63.600 | 1908 | final thump | -4.0 | 0.00 |
