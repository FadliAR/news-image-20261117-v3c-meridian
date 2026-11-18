# The Daily Meridian — Tuesday 17 November 2026

![make.fun competition](https://make.fun/badge/news-image-20261117.svg)
![make.fun rank](https://make.fun/badge/news-image-20261117/FadliAR/news-image-20261117-v3c-meridian/rank.svg)
![make.fun reward](https://make.fun/badge/news-image-20261117/FadliAR/news-image-20261117-v3c-meridian/reward.svg)

A single 1024x1024 image that sums up the world's news of **Tuesday 17 November 2026**: 46 stories — a lead trio (Kerch Bridge struck for a second day, Iran–Gulf drone escalation, the Quad summit in Manila), ten more illustrated features, a numbered world map with pins 1–13, 33 numbered one-liners, and a four-number stat strip.

Entry for the make.fun bounty [news-image-20261117](https://make.fun/c/news-image-20261117) — see the competition page at https://make.fun/c/news-image-20261117.

## Run it

```
python3 main.py            # writes ./entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
```

Python 3 standard library only. The generator draws everything itself (own rasteriser, own stroke font, own PNG writer), uses no network and no input files, and is deterministic: two runs produce byte-identical output.

## Layout of the page

- Masthead: paper name, giant date line, story-count banner.
- Leads 1–3 across the top, features 4–13 in a dense grid, each with its own scene.
- Bottom: numbered world map + "ALSO ON TUESDAY 17 NOVEMBER" one-liners 14–46, stat strip, sources footer.

License: MIT (see LICENSE).
