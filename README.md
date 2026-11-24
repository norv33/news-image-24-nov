[![make.fun](https://make.fun/badge/news-image-20261124.svg)](https://make.fun/c/news-image-20261124)
[![rank](https://make.fun/badge/news-image-20261124/norv33/news-image-24-nov/rank.svg)](https://make.fun/c/news-image-20261124)
[![reward](https://make.fun/badge/news-image-20261124/norv33/news-image-24-nov/reward.svg)](https://make.fun/c/news-image-20261124)

# The World — 24 November 2026

A single image that sums up Tuesday 24 November 2026 in world news: an
"evening broadcast" poster — deep navy screen, signal cyan, amber highlights
and a red LIVE bug — with the day's six most consequential stories, an
also-today ticker, and the date in large amber type.

Entry for the make.fun bounty
[Sum up 24 November's world news in one image](https://make.fun/c/news-image-20261124).

## Run it

```
mkdir -p out && MAKEFUN_OUTPUT_DIR=out node main.ts
# writes out/entry.png — run it twice and compare sha256: identical.
```

To redraw the image from scratch (needs Python 3 + Pillow):

```
python3 draw.py   # writes entry.png (1024x1024, < 1 MiB)
```

## The six stories

1. **'Sputnik-S': nuclear satellite alarm** — Western intelligence says
   Russia could put a nuclear-armed satellite in orbit by December; the
   Kremlin dismisses the reports.
   (WDR / NDR / Süddeutsche Zeitung via Reuters)
2. **Nvidia +31% as Huang returns** — shares jump 31.5%, about $950bn in a
   day, as Jensen Huang returns as CEO. Nasdaq +6.5%, S&P +4.7%.
   (AP; Reuters)
3. **FIFA picks 2031 & 2035 hosts** — USA, Mexico, Costa Rica and Jamaica
   host the first 48-team Women's World Cup in 2031; the UK's home nations
   host 2035.
   (FIFA; AP)
4. **Chess title: Game 1 today** — Gukesh defends against Sindarov in
   Geneva, the youngest world title match ever. Both 20; 14 games, $2.5m
   prize.
   (FIDE)
5. **US seizes $1.1bn in crypto** — US authorities move to reclaim over
   $1.1bn in crypto taken by North Korean hackers.
   (US authorities)
6. **Modi hosts Nepal PM; $1.62bn package** — India announces a $1.62bn
   development package for Nepal.
   (India / Nepal)

Also today: suspected N. Korean jets 'violate' South Korean airspace;
tonight a supermoon meets the Pleiades; 450 German schools get bomb
threats; an UNRWA worker is killed in a strike in Gaza.

## Design

An "evening broadcast" poster: "THE WORLD" in huge white bold type on a
dark-navy screen with a red LIVE bug, the date "TUESDAY, 24 NOVEMBER 2026"
in large amber type, then one wide lead panel for the Sputnik-S satellite
alarm and four story cards in two columns — each with a hand-drawn
pictogram (satellite on an orbit ring, rising market chart, football,
chess rook, crypto coin), a coloured region tag, a headline and one fact
line — followed by a slim sixth-story row, an "ALSO TODAY" ticker strip
and a sources footer. This design is original to this entry and
deliberately different from the 23 November entry (crimson morning
broadsheet on ivory paper), the 22 November entry (dark-teal evening atlas
with gold) and the 20 November entry (white wire-desk poster, 2×3 grid).

## How it works

`entry.png` (1024×1024, drawn with Python PIL and Liberation fonts by
`draw.py`) is the image. `main.ts` (Node 22, stdlib only) validates it first —
the first 8 bytes must match the PNG signature, the file must be at most 1 MiB,
and the IHDR dimensions must be exactly 1024×1024 — then writes it atomically
to `$MAKEFUN_OUTPUT_DIR` (or `/output`) as `entry.png`: the bytes go to a
temporary file in the output directory, then rename over `entry.png`, so a
failed run never leaves a truncated image behind.

Running it twice produces byte-identical output.

Every story above happened on, or was reported on, 24 November 2026.
