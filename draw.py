#!/usr/bin/env python3
"""Draw "The World - 24 November 2026": an evening-broadcast poster.

One 1024x1024 PNG summing up Tuesday 24 November 2026 in world news.
Layout: a dark-navy "live broadcast" screen — masthead with a red LIVE
bug, a wide lead panel, four story cards in two columns, a slim sixth-story
row, an ALSO TODAY ticker strip, and a sources footer. All art is drawn
from PIL primitives; no external images. Original to this entry and
deliberately different from the 23 November morning broadsheet (crimson,
ivory paper), the 22 November night atlas (dark teal, gold) and the
20 November white wire-desk poster.
"""
from PIL import Image, ImageDraw, ImageFont
import math

W = H = 1024
OUT = "entry.png"

# ---- palette: evening broadcast — deep navy, signal cyan, amber, live red ----
NAVY = (10, 26, 51)
NAVY_DARK = (7, 19, 38)
CARD = (18, 41, 77)
CARD2 = (14, 34, 64)
INK_LINE = (32, 64, 110)
WHITE = (245, 248, 255)
CYAN = (41, 182, 246)
CYAN_DIM = (120, 200, 240)
YELLOW = (255, 196, 0)
RED = (229, 57, 53)
GREEN = (76, 209, 120)
MUTED = (148, 168, 196)
BODY = (205, 218, 235)

SANS = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


F_TITLE = font(SANS_B, 98)
F_DATE = font(SANS_B, 31)
F_LIVE = font(SANS_B, 24)
F_LEAD_HEAD = font(SANS_B, 43)
F_HEAD = font(SANS_B, 27)
F_FACT = font(SANS, 20)
F_LEAD_FACT = font(SANS, 22)
F_TAG = font(SANS_B, 17)
F_ALSO_HEAD = font(SANS_B, 20)
F_ALSO = font(SANS, 18)
F_FOOT = font(SANS, 18)
F_SIXTH_HEAD = font(SANS_B, 27)
F_SIXTH_FACT = font(SANS, 19)


def wrap(draw, text, fnt, width):
    """Greedy word wrap using real glyph widths."""
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = (cur + " " + w).strip()
        if draw.textlength(trial, font=fnt) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def draw_block(draw, xy, lines, fnt, fill, leading):
    x, y = xy
    for ln in lines:
        draw.text((x, y), ln, font=fnt, fill=fill)
        y += leading
    return y


def starburst(d, cx, cy, r_out, r_in, n, fill):
    pts = []
    for i in range(2 * n):
        ang = i * math.pi / n - math.pi / 2
        r = r_out if i % 2 == 0 else r_in
        pts.append((cx + r * math.cos(ang), cy + r * math.sin(ang)))
    d.polygon(pts, fill=fill)


# ---------------------------------------------------------------- pictograms
def pic_satellite(d, x, y, s):
    """Satellite on an orbit ring: the 'Sputnik-S' nuclear-satellite alarm."""
    cx, cy = x + s // 2, y + s // 2 + 6
    # orbit ellipse
    d.ellipse([x + 2, y + 26, x + s - 2, y + s - 6], outline=CYAN_DIM, width=3)
    d.ellipse([x + s - 22, y + s - 22, x + s - 8, y + s - 8], fill=CYAN)
    # solar panels
    d.rectangle([cx - 58, cy - 12, cx - 18, cy + 10], outline=CYAN, width=4,
                fill=(24, 80, 130))
    d.rectangle([cx + 18, cy - 12, cx + 58, cy + 10], outline=CYAN, width=4,
                fill=(24, 80, 130))
    d.line([cx - 58, cy - 1, cx - 18, cy - 1], fill=CYAN, width=2)
    d.line([cx + 18, cy - 1, cx + 58, cy - 1], fill=CYAN, width=2)
    # body
    d.rectangle([cx - 18, cy - 20, cx + 18, cy + 20], outline=WHITE, width=4,
                fill=YELLOW)
    d.rectangle([cx - 8, cy - 8, cx + 8, cy + 8], fill=RED)
    # antenna + red alert star
    d.line([cx, cy - 20, cx + 12, cy - 36], fill=WHITE, width=4)
    starburst(d, cx + 16, cy - 44, 14, 6, 8, RED)


def pic_chart(d, x, y, s):
    """Rising market chart: Nvidia +31%."""
    ox, oy = x + 10, y + s - 18
    d.line([ox, y + 12, ox, oy], fill=MUTED, width=4)
    d.line([ox, oy, x + s - 8, oy], fill=MUTED, width=4)
    pts = [(ox + 6, oy - 26), (ox + 34, oy - 40), (ox + 52, oy - 30),
           (ox + 78, oy - 62), (ox + 102, oy - 88)]
    d.line(pts, fill=GREEN, width=6, joint="curve")
    # arrowhead
    d.polygon([(ox + 102, oy - 88), (ox + 84, oy - 88), (ox + 102, oy - 70)],
              fill=GREEN)
    d.text((ox + 8, y + 2), "+31%", font=font(SANS_B, 30), fill=YELLOW)


def pic_football(d, x, y, s):
    """Football: FIFA Women's World Cup hosts."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 8
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=WHITE, width=5,
              fill=(24, 80, 130))
    # pentagon
    pent = []
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        pent.append((cx + 20 * math.cos(ang), cy + 20 * math.sin(ang)))
    d.polygon(pent, fill=WHITE)
    for i in range(5):
        ang = -math.pi / 2 + i * 2 * math.pi / 5
        d.line([pent[i], (cx + (r - 2) * math.cos(ang),
                          cy + (r - 2) * math.sin(ang))], fill=WHITE, width=3)


def pic_rook(d, x, y, s):
    """Chess rook: World Championship Game 1 in Geneva."""
    rx, ry = x + 18, y + 12
    # top with three crenellations
    d.rectangle([rx, ry, rx + 76, ry + 16], outline=WHITE, width=4,
                fill=CYAN)
    for i in range(3):
        d.rectangle([rx + 4 + i * 26, ry - 12, rx + 22 + i * 26, ry],
                    outline=WHITE, width=4, fill=CYAN)
    # body: wide trapezoid tapering down, then flaring base
    d.polygon([(rx + 6, ry + 16), (rx + 70, ry + 16), (rx + 58, ry + 66),
               (rx + 18, ry + 66)], outline=WHITE, width=4, fill=CARD2)
    d.rectangle([rx - 4, ry + 66, rx + 80, ry + 88], outline=WHITE, width=4,
                fill=YELLOW)
    d.text((x + s - 42, y + s - 36), "1", font=font(SANS_B, 30), fill=YELLOW)


def pic_coin(d, x, y, s):
    """Coin with a B: US seizes $1.1bn in crypto from N. Korean hackers."""
    cx, cy, r = x + s // 2, y + s // 2, s // 2 - 10
    d.ellipse([cx - r, cy - r, cx + r, cy + r], outline=YELLOW, width=5,
              fill=(24, 80, 130))
    d.ellipse([cx - r + 10, cy - r + 10, cx + r - 10, cy + r - 10],
              outline=YELLOW, width=2)
    d.text((cx - 16, cy - 30), "B", font=font(SANS_B, 56), fill=YELLOW)


def pic_flags(d, x, y, s):
    """Two small flags: India hosts Nepal's PM."""
    # India: saffron / white / green with wheel dot
    fx, fy = x + 6, y + 22
    d.rectangle([fx, fy, fx + 56, fy + 12], fill=(255, 153, 51))
    d.rectangle([fx, fy + 12, fx + 56, fy + 24], fill=WHITE)
    d.rectangle([fx, fy + 24, fx + 56, fy + 36], fill=(19, 136, 8))
    d.ellipse([fx + 24, fy + 14, fx + 32, fy + 22], outline=(0, 0, 128),
              width=2)
    d.line([fx, fy + 36, fx, fy + 62], fill=WHITE, width=3)
    # Nepal: simplified crimson double pennon
    nx, ny = x + s - 62, y + 22
    d.polygon([(nx, ny), (nx + 44, ny + 12), (nx, ny + 24)], fill=RED,
              outline=WHITE)
    d.polygon([(nx, ny + 24), (nx + 36, ny + 34), (nx, ny + 44)], fill=RED,
              outline=WHITE)
    d.line([nx, ny, nx, ny + 62], fill=WHITE, width=3)


# ---------------------------------------------------------------- stories
LEAD = {
    "tag": "SPACE  •  SECURITY  —  WDR / NDR / SZ VIA REUTERS",
    "head": "'Sputnik-S': nuclear satellite alarm",
    "fact": ("Western intelligence says Russia could put a nuclear-armed "
             "satellite in orbit by December. The Kremlin dismisses the "
             "reports."),
    "pic": pic_satellite,
}

CARDS = [
    {
        "tag": "MARKETS  •  WALL STREET  —  AP / REUTERS",
        "head": "Nvidia +31% as Huang returns",
        "fact": ("Shares jump 31.5% — about $950bn in a day — as Jensen "
                 "Huang returns as CEO. Nasdaq +6.5%, S&P +4.7%."),
        "pic": pic_chart,
    },
    {
        "tag": "SPORT  •  FOOTBALL  —  FIFA / AP",
        "head": "FIFA picks 2031 & 2035 hosts",
        "fact": ("USA, Mexico, Costa Rica and Jamaica host the first "
                 "48-team Women's World Cup in 2031; the UK hosts 2035."),
        "pic": pic_football,
    },
    {
        "tag": "SPORT  •  CHESS  —  FIDE",
        "head": "Chess title: Game 1 today",
        "fact": ("Gukesh defends against Sindarov in Geneva — the youngest "
                 "world title match ever. Both 20; 14 games, $2.5m prize."),
        "pic": pic_rook,
    },
    {
        "tag": "CYBER  •  CRIME  —  US AUTHORITIES",
        "head": "US seizes $1.1bn in crypto",
        "fact": ("US authorities move to reclaim over $1.1bn in crypto "
                 "taken by North Korean hackers."),
        "pic": pic_coin,
    },
]

EXTRA = {
    "tag": "DIPLOMACY  •  NEW DELHI  —  INDIA / NEPAL",
    "head": "Modi hosts Nepal PM; $1.62bn package",
    "fact": "India announces a $1.62bn development package for Nepal.",
    "pic": pic_flags,
}

ALSO = ("SEOUL: N. Korean jets 'violate' airspace"
        "  •  TONIGHT: Supermoon meets Pleiades"
        "  •  GERMANY: 450 schools get bomb threats"
        "  •  GAZA: UNRWA worker killed in strike")


def main():
    img = Image.new("RGB", (W, H), NAVY)
    d = ImageDraw.Draw(img)

    # faint broadcast grid
    for xx in range(0, W, 64):
        d.line([(xx, 0), (xx, H)], fill=(13, 32, 62), width=1)
    for yy in range(0, H, 64):
        d.line([(0, yy), (W, yy)], fill=(13, 32, 62), width=1)

    # ---- masthead: title + LIVE bug + date bar ----
    d.rectangle([0, 0, W, 150], fill=NAVY_DARK)
    d.rectangle([0, 150, W, 156], fill=CYAN)
    title = "THE WORLD"
    tw = d.textlength(title, font=F_TITLE)
    d.text(((W - tw) / 2, 4), title, font=F_TITLE, fill=WHITE)
    # LIVE bug, top right
    bug = "● LIVE"
    bw = d.textlength(bug, font=F_LIVE) + 28
    d.rounded_rectangle([W - 36 - bw, 22, W - 36, 22 + 44], radius=8,
                        fill=RED)
    d.text((W - 36 - bw + 14, 30), bug, font=F_LIVE, fill=WHITE)
    d.text((36, 108), "TUESDAY, 24 NOVEMBER 2026", font=F_DATE,
           fill=YELLOW)
    right = "6 STORIES  •  ONE DAY"
    d.text((W - 36 - d.textlength(right, font=F_DATE), 108), right,
           font=F_DATE, fill=CYAN_DIM)

    # ---- lead story: full-width panel, 172-362 ----
    lx, ly, lw, lh = 36, 172, W - 72, 190
    d.rectangle([lx, ly, lx + lw, ly + lh], fill=CARD, outline=INK_LINE,
                width=2)
    d.rectangle([lx, ly, lx + 10, ly + lh], fill=YELLOW)
    d.text((lx + 28, ly + 12), LEAD["tag"], font=F_TAG, fill=CYAN)
    head_lines = wrap(d, LEAD["head"], F_LEAD_HEAD, lw - 250)
    draw_block(d, (lx + 28, ly + 40), head_lines, F_LEAD_HEAD, WHITE, 50)
    fact_lines = wrap(d, LEAD["fact"], F_LEAD_FACT, lw - 250)
    draw_block(d, (lx + 28, ly + 40 + len(head_lines) * 50 + 8),
               fact_lines, F_LEAD_FACT, BODY, 29)
    LEAD["pic"](d, lx + lw - 172, ly + 22, 144)

    # ---- four story cards: 2 columns x 2 rows, 378-806 ----
    cw, ch, gap = 466, 208, 20
    for i, c in enumerate(CARDS):
        col, row = i % 2, i // 2
        x = 36 + col * (cw + gap)
        y = 378 + row * (ch + 12)
        d.rectangle([x, y, x + cw, y + ch], fill=CARD, outline=INK_LINE,
                    width=2)
        d.rectangle([x, y, x + cw, y + 5], fill=CYAN if col == 0 else YELLOW)
        d.text((x + 18, y + 16), c["tag"], font=F_TAG, fill=CYAN)
        head_lines = wrap(d, c["head"], F_HEAD, cw - 150)
        end = draw_block(d, (x + 18, y + 44), head_lines, F_HEAD, WHITE, 33)
        fact_lines = wrap(d, c["fact"], F_FACT, cw - 150)
        draw_block(d, (x + 18, end + 4), fact_lines, F_FACT, BODY, 25)
        c["pic"](d, x + cw - 130, y + 58, 112)

    # ---- sixth story: slim full-width row, 822-910 ----
    ex, ey, ew, eh = 36, 822, W - 72, 88
    d.rectangle([ex, ey, ex + ew, ey + eh], fill=CARD2, outline=INK_LINE,
                width=2)
    d.rectangle([ex, ey, ex + 10, ey + eh], fill=RED)
    d.text((ex + 28, ey + 8), EXTRA["tag"], font=F_TAG, fill=CYAN)
    d.text((ex + 28, ey + 30), EXTRA["head"], font=F_SIXTH_HEAD,
           fill=WHITE)
    d.text((ex + 28, ey + 62), EXTRA["fact"], font=F_SIXTH_FACT,
           fill=BODY)
    EXTRA["pic"](d, ex + ew - 104, ey + 10, 66)

    # ---- also today ticker, 922-978 ----
    ax, ay, aw, ah = 36, 922, W - 72, 56
    d.rectangle([ax, ay, ax + aw, ay + ah], fill=(0, 0, 0))
    d.rectangle([ax, ay, ax + aw, ay + ah], outline=YELLOW, width=2)
    d.text((ax + 16, ay + 17), "ALSO TODAY", font=F_ALSO_HEAD, fill=YELLOW)
    ax0 = ax + 16 + d.textlength("ALSO TODAY", font=F_ALSO_HEAD) + 18
    items = wrap(d, ALSO, F_ALSO, aw - (ax0 - ax) - 16)
    draw_block(d, (ax0, ay + 6), items[:2], F_ALSO, WHITE, 22)

    # ---- footer ----
    d.text((36, 986), "Sources: Reuters • AP • AFP • FIFA • FIDE — drawn for "
           "make.fun news-image-20261124", font=F_FOOT, fill=MUTED)
    d.text((W - 36 - d.textlength("24 NOV 2026", font=F_FOOT), 986),
           "24 NOV 2026", font=F_FOOT, fill=MUTED)

    img.save(OUT, "PNG", optimize=True)
    print(f"wrote {OUT} {img.size}")


if __name__ == "__main__":
    main()
