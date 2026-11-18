# ENDGAME — news-image-20261117 v3c ("The Daily Meridian")

## Artifact
- Repo: https://github.com/FadliAR/news-image-20261117-v3c-meridian
- Repo birth: kit `init` ran FIRST in the empty workspace. ROOT commit `588c1f1a238e6f463e47f12a3bfb46ec78d58b4f` is the makefun beacon root holding only `.makefun/freshness.json` (drand round 34070258); the second commit adds the LICENSE. Every later commit builds on that root — history was never rewritten.
- LICENSE: first line `SPDX-License-Identifier: MIT` (committed by init itself; verified by grep).
- entry.png: 1024×1024, **603,255 bytes**
- entry.png sha256: `3d8e1fc38fd991701f4056305e138581bd67ac9bac63168e8906c09399b0d2fe`
- Determinism: generator run twice into separate dirs → `cmp` byte-identical (verified after the final edits, and again before the final commit).
- Final commit: see the git log / the report that accompanies this build (HEAD is pushed; `git ls-remote origin HEAD` == local HEAD).

## Story count
- Illustrated features: **13** (3 large leads + 10 features), each with its own drawn scene, kicker, headline and summary.
- One-liners ("ALSO ON TUESDAY 17 NOVEMBER", numbered 14–46): **33**
- **Total: 46 stories**

## Checklist vs the winners' formula
- [x] Top strip: "THE WORLD'S NEWS IN ONE PICTURE" left / "45+ STORIES · 6 CONTINENTS · ALL FROM TUESDAY" right; paper name "THE DAILY MERIDIAN".
- [x] Giant masthead: "Tuesday 17 November 2026" full width on a dark band.
- [x] Lead trio, each a drawn scene with labels + caption bar: 1 Kerch/Crimea Bridge broken span + explosion + CRIMEA/RUSSIA; 2 Iran–Gulf map scene (IRAN/QESHM/BAHRAIN/ARABIA/HORMUZ, dashed arcs, drones, "DRONES DOWNED", radar burst at Bahrain); 3 Quad Manila (US/India/Japan/Australia flags, banner, table + seated leaders).
- [x] Features 4–13 all illustrated: Ebola virus+clinic+bars; COP31 globe+torn draft; measles cracked shield; Nvidia bars/chip vs Dow −849; Gaza tents+held aid truck in rain; Mongolia parliament+ger+resigning president; Serbia parliament+student crowd+140–103 bar; Dhaka factory+"Tk 30,000 NOW" crowd+gas cloud; An-12 wreck in snow (wing/stripe/propeller); Mondlane courthouse+scales+green ribbon.
- [x] World map: continent polygons, numbered pins 1–13 matching story numbers, 7-region legend (Americas/Europe/Middle East/Asia/Africa/Oceania/Global).
- [x] Stat strip exactly: "2 days — strikes on the Crimean Bridge" · "11,000+ — Ebola cases in DR Congo" · "$115.8BN — Nvidia quarterly sales, up 103%" · "-849 — Dow fall (-1.6%)".
- [x] Footer: "Every story here happened or was first reported on Tuesday 17 November 2026. Contested claims are marked as claims." + "Sources: Reuters, AP, AFP, BBC, Al Jazeera, WHO, UN. Original drawings."
- [x] Density: filled edge to edge; PNG 603,255 bytes — inside the 250–650 KB target band and under the 1 MiB gate.
- [x] Tech: Python stdlib only (os, sys, zlib, struct, math), own rasteriser + own stroke font, no PIL, no assets, no network; main.py revised in several edit rounds after visual QA.

## Visual QA iterations
1. First render (667,783 bytes): headlines collided with summaries, one-liners wrapped into each other, Gulf "DRONES DOWNED"/"QESHM"/"ARABIA" labels collided, COP31/An-12 bottom labels touched headlines. Fixes: shortened headlines + summaries, dynamic summary offset, one-liners shortened to single lines, scene labels moved, grain reduced (size fell into band).
2. Zoomed crops: Gulf badge text was wider than its red box; Serbia vote bar spilled into the headline; Ebola cross/clinic/bars overlapped; Mongolia "RESIGNS" sat on the ger. Fixes: badge widened + moved, vote bar raised inside the scene, Ebola scene re-laid out, RESIGNS moved to the corner, QESHM moved onto clear water.
3. Stat strip crop: sub-labels too faint at 6.8px → enlarged to 7.5px, big numbers 13px; CLINIC and BAHRAIN labels nudged clear. Final read: no collisions, all text legible.

## Honest limits
- Stroke font is a hand-built condensed sans, not a true serif; the masthead reads as a heavy newspaper title but is not classical serif type.
- World map is simplified polygon geography; the Mediterranean/Black Sea are not carved from Eurasia at this scale, but continents and pin placements are recognisable and geographically sensible (the Europe/Middle-East pin cluster is dense, as in the winners' pages).
- A few in-scene micro-labels (CLINIC, DOW -849 chip) are small at thumbnail size, though legible at full size.
