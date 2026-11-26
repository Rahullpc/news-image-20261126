#!/usr/bin/env python3
"""Draw the front page of THE WORLD for Thursday 26 November 2026.

A code-drawn newspaper poster for the make.fun news-image-20261126 bounty:
one lead story, a 2x3 grid of stories, an ALSO TODAY strip and a footer.
Stdlib + Pillow only. No network, no randomness, no timestamps, so every
run produces byte-identical output.

Usage: python3 draw_poster.py [output-path]   (default: entry.png)
"""
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
MARGIN = 28
CONTENT_W = W - 2 * MARGIN          # 968
GUTTER = 14

PAPER = (247, 242, 231)             # warm newsprint
INK = (22, 21, 19)
RED = (163, 29, 29)
BLUE = (30, 58, 95)
GREEN = (31, 107, 58)
MUTED = (107, 100, 85)
LIGHT_RULE = (190, 180, 160)
PANEL = (238, 231, 214)
SKY = (214, 228, 238)
PITCH = (46, 125, 62)

SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SANS_I = "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf"


def font(path, size):
    return ImageFont.truetype(path, size)


def wrap(draw, text, fnt, max_w):
    """Greedy word wrap; returns a list of lines that fit max_w."""
    words = text.split()
    lines, cur = [], ""
    for word in words:
        trial = (cur + " " + word).strip()
        if draw.textlength(trial, font=fnt) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def para(draw, x, y, text, fnt, max_w, leading, fill=INK):
    """Draw wrapped text; returns the y just below the last line."""
    for line in wrap(draw, text, fnt, max_w):
        draw.text((x, y), line, font=fnt, fill=fill)
        y += leading
    return y


def rule(draw, x0, y, x1, width=2, fill=INK):
    draw.line([(x0, y), (x1, y)], fill=fill, width=width)


def double_rule(draw, x0, y, x1):
    rule(draw, x0, y, x1, width=3)
    rule(draw, x0, y + 5, x1, width=1)


# ---------------------------------------------------------------- masthead
def draw_masthead(d):
    double_rule(d, MARGIN, 26, W - MARGIN)
    f_date = font(SANS_B, 19)
    date = "THURSDAY, 26 NOVEMBER 2026"
    d.text(((W - d.textlength(date, font=f_date)) / 2, 40), date,
           font=f_date, fill=INK)
    f_side = font(SANS, 13)
    d.text((MARGIN, 43), "No. 331", font=f_side, fill=MUTED)
    right = "PRICE: ONE DAY'S NEWS"
    d.text((W - MARGIN - d.textlength(right, font=f_side), 43), right,
           font=f_side, fill=MUTED)

    f_name = font(SERIF_B, 96)
    name = "THE WORLD"
    d.text(((W - d.textlength(name, font=f_name)) / 2, 62), name,
           font=f_name, fill=INK)
    f_sub = font(SANS, 14)
    sub = "THE DAY'S NEWS  •  FROM EVERY CORNER OF THE GLOBE"
    d.text(((W - d.textlength(sub, font=f_sub)) / 2, 158), sub,
           font=f_sub, fill=MUTED)
    double_rule(d, MARGIN, 184, W - MARGIN)


# ---------------------------------------------------------------- ticker
def draw_ticker(d):
    y = 198
    f_lab = font(SANS_B, 14)
    d.text((MARGIN, y), "MARKETS — WEDNESDAY", font=f_lab, fill=RED)
    items = [("Nasdaq", "-0.62%", RED), ("S&P 500", "-0.25%", RED),
             ("Dow", "+0.33%", GREEN), ("KOSPI", "-6.16%", RED),
             ("Nikkei", "-2.78%", RED)]
    f_item = font(SANS_B, 15)
    x = MARGIN + 210
    for name, val, col in items:
        d.text((x, y), name, font=font(SANS, 15), fill=INK)
        x += d.textlength(name + " ", font=font(SANS, 15))
        d.text((x, y), val, font=f_item, fill=col)
        x += d.textlength(val, font=f_item) + 26
    rule(d, MARGIN, 226, W - MARGIN, width=1, fill=LIGHT_RULE)


# ---------------------------------------------------------------- lead art
def draw_lead_art(d, x0, y0, w, h):
    """A market chart: a steep plunge, then a partial recovery."""
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=SKY, outline=INK, width=2)
    # faint grid
    for gx in range(1, 5):
        gx0 = x0 + w * gx // 5
        d.line([(gx0, y0 + 6), (gx0, y0 + h - 6)], fill=(200, 214, 224), width=1)
    for gy in range(1, 4):
        gy0 = y0 + h * gy // 4
        d.line([(x0 + 6, gy0), (x0 + w - 6, gy0)], fill=(200, 214, 224), width=1)
    # plunge then recovery, scaled to the box
    pts = [(x0 + 14, y0 + 52), (x0 + 52, y0 + 44), (x0 + 84, y0 + 60),
           (x0 + 112, y0 + 118), (x0 + 138, y0 + 168), (x0 + 162, y0 + 186),
           (x0 + 186, y0 + 176), (x0 + 214, y0 + 156), (x0 + 244, y0 + 138),
           (x0 + 274, y0 + 122)]
    d.line(pts, fill=RED, width=5, joint="curve")
    # red arrow head at the trough
    d.polygon([(x0 + 162, y0 + 186), (x0 + 150, y0 + 174),
               (x0 + 174, y0 + 176)], fill=RED)
    # green recovery arrow
    d.line([(x0 + 214, y0 + 156), (x0 + 274, y0 + 122)], fill=GREEN, width=4)
    d.polygon([(x0 + 274, y0 + 122), (x0 + 258, y0 + 122),
               (x0 + 270, y0 + 136)], fill=GREEN)
    f_tag = font(SANS_B, 13)
    d.text((x0 + 12, y0 + 10), "NASDAQ: -4.6% INTRADAY", font=f_tag, fill=RED)
    d.text((x0 + 12, y0 + 28), "DIP-BUYERS PARE LOSSES", font=f_tag,
           fill=GREEN)
    # small tariff document in the corner
    px, py = x0 + w - 52, y0 + h - 46
    d.rectangle([px, py, px + 38, py + 34], fill=(255, 255, 255),
                outline=INK, width=2)
    d.text((px + 6, py + 4), "TAX", font=font(SANS_B, 13), fill=RED)
    for i, ly in enumerate((py + 20, py + 26)):
        d.line([(px + 6, ly), (px + 32, ly)], fill=MUTED, width=1)


def draw_lead(d):
    y0 = 240
    draw_lead_art(d, MARGIN, y0, 302, 208)
    x = MARGIN + 322
    w = W - MARGIN - x
    f_kick = font(SANS_B, 15)
    d.text((x, y0 + 2), "LEAD STORY  —  MARKETS & TRADE", font=f_kick, fill=RED)
    y = para(d, x, y0 + 26,
             "TARIFF SHOCK FUELS AI ROUT AS WALL STREET WHIPSAWS",
             font(SERIF_B, 30), w, 35)
    y = para(d, x, y + 6,
             "President Trump's new tariffs on 14 trading partners landed "
             "on top of a deepening AI sell-off. The Nasdaq fell as much "
             "as 4.6% at the open; the Nasdaq 100 briefly fell 20% from "
             "its early-October peak before dip-buyers pared the losses.",
             font(SANS, 15), w, 20)
    y = para(d, x, y + 6,
             "Nvidia fell 3.9%; tariffs of up to 40% after an 8-month "
             "probe. US markets shut today for Thanksgiving.",
             font(SANS_I, 13), w, 17, fill=MUTED)
    rule(d, MARGIN, 462, W - MARGIN, width=1, fill=LIGHT_RULE)


# ---------------------------------------------------------------- grid art
def draw_refinery(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(250, 232, 200),
                outline=INK, width=1)
    # sky band, ground
    d.rectangle([x0, y0 + h - 22, x0 + w, y0 + h], fill=(120, 96, 70))
    # towers (heights fit the 80 px panel)
    for tx, th in ((x0 + 26, 34), (x0 + 66, 42), (x0 + 112, 30)):
        d.rectangle([tx, y0 + h - 22 - th, tx + 26, y0 + h - 22],
                    fill=(90, 80, 66), outline=INK, width=1)
        d.rectangle([tx + 6, y0 + h - 22 - th - 10, tx + 20,
                     y0 + h - 22 - th], fill=(90, 80, 66), outline=INK, width=1)
    # flame on top of the middle tower
    top = y0 + h - 22 - 42
    d.polygon([(x0 + 76, top), (x0 + 84, top - 14),
               (x0 + 92, top)], fill=(230, 120, 30))
    d.polygon([(x0 + 79, top), (x0 + 84, top - 8),
               (x0 + 89, top)], fill=(250, 200, 60))
    # smoke puffs
    for sx, sy, r in ((x0 + 40, y0 + 12, 9), (x0 + 58, y0 + 6, 7),
                      (x0 + 126, y0 + 14, 8)):
        d.ellipse([sx - r, sy - r, sx + r, sy + r], fill=(160, 150, 135))
    # drones: small crosses with dots
    for dx, dy in ((x0 + 200, y0 + 18), (x0 + 236, y0 + 30), (x0 + 262, y0 + 12)):
        d.line([(dx - 7, dy), (dx + 7, dy)], fill=INK, width=2)
        d.line([(dx, dy - 7), (dx, dy + 7)], fill=INK, width=2)
        d.ellipse([dx - 3, dy - 3, dx + 3, dy + 3], fill=RED)
    d.text((x0 + 168, y0 + h - 19), "4 DRONES DOWNED", font=font(SANS_B, 10),
           fill=(255, 255, 255))


def draw_asteroid(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(18, 28, 48),
                outline=INK, width=1)
    for sx, sy in ((x0 + 18, y0 + 12), (x0 + 60, y0 + 26), (x0 + 120, y0 + 10),
                   (x0 + 200, y0 + 16), (x0 + 260, y0 + 30), (x0 + 290, y0 + 8),
                   (x0 + 150, y0 + 30), (x0 + 230, y0 + 52)):
        d.ellipse([sx - 1, sy - 1, sx + 1, sy + 1], fill=(255, 255, 255))
    # Dimorphos: big grey rock with a stadium-sized crater
    cx, cy, r = x0 + 110, y0 + 52, 40
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(150, 146, 138),
              outline=(90, 86, 80), width=2)
    d.ellipse([cx - 26, cy - 16, cx + 22, cy + 20], fill=(105, 100, 92),
              outline=(70, 66, 60), width=2)
    d.ellipse([cx - 12, cy - 4, cx + 8, cy + 12], fill=(80, 76, 68))
    for bx, by, br in ((cx - 30, cy - 26, 4), (cx + 24, cy - 24, 3),
                       (cx + 28, cy + 18, 4), (cx - 22, cy + 26, 3)):
        d.ellipse([bx - br, by - br, bx + br, by + br], fill=(120, 116, 108))
    # Didymos, the larger companion
    d.ellipse([x0 + 238, y0 + 58, x0 + 268, y0 + 88], fill=(120, 116, 110),
              outline=(80, 76, 70), width=1)
    # Hera probe
    d.rectangle([x0 + 268, y0 + 8, x0 + 282, y0 + 20], fill=(200, 200, 60),
                outline=INK, width=1)
    d.line([(x0 + 268, y0 + 14), (x0 + 252, y0 + 14)], fill=INK, width=2)
    d.line([(x0 + 282, y0 + 14), (x0 + 298, y0 + 14)], fill=INK, width=2)
    d.text((x0 + 10, y0 + h - 18), "DIMORPHOS: 151 m WIDE",
           font=font(SANS_B, 11), fill=(255, 255, 255))


def draw_economy(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(226, 238, 226),
                outline=INK, width=1)
    # rising bars
    base = y0 + h - 14
    for i, bh in enumerate((18, 30, 44, 58)):
        bx = x0 + 18 + i * 30
        d.rectangle([bx, base - bh, bx + 20, base], fill=BLUE, outline=INK,
                    width=1)
    # gauge, needle pointing hot
    gx, gy, gr = x0 + 218, y0 + 58, 34
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 180, 360, fill=RED, width=5)
    d.arc([gx - gr, gy - gr, gx + gr, gy + gr], 180, 270, fill=(200, 200, 200),
          width=5)
    d.line([(gx, gy), (gx + 24, gy - 22)], fill=RED, width=4)
    d.ellipse([gx - 5, gy - 5, gx + 5, gy + 5], fill=INK)
    d.text((gx - 26, gy + 8), "HOT", font=font(SANS_B, 12), fill=RED)
    d.text((x0 + 150, y0 + 8), "PCE 3.8%  •  GDP 4.3%",
           font=font(SANS_B, 12), fill=INK)


def draw_capitol(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(232, 226, 214),
                outline=INK, width=1)
    cx = x0 + w // 2
    base = y0 + h - 10
    # dome
    d.pieslice([cx - 34, y0 + 6, cx + 34, y0 + 58], 180, 360, fill=(200, 192, 170),
               outline=INK, width=1)
    d.rectangle([cx - 40, y0 + 48, cx + 40, y0 + 56], fill=(200, 192, 170),
                outline=INK, width=1)
    # columns
    for i in range(5):
        colx = cx - 44 + i * 20
        d.rectangle([colx, y0 + 56, colx + 8, base], fill=(220, 212, 190),
                    outline=INK, width=1)
    d.rectangle([cx - 50, base - 4, cx + 50, base], fill=(200, 192, 170),
                outline=INK, width=1)
    # chip at the side
    d.rectangle([x0 + 12, y0 + 52, x0 + 44, y0 + 76], fill=(40, 60, 40),
                outline=INK, width=1)
    for px in (x0 + 18, x0 + 28, x0 + 38):
        d.line([(px, y0 + 46), (px, y0 + 52)], fill=INK, width=2)
        d.line([(px, y0 + 76), (px, y0 + 82)], fill=INK, width=2)
    d.text((x0 + 196, y0 + 8), "HEARING 3 DEC", font=font(SANS_B, 11),
           fill=RED)


def draw_football(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=PITCH, outline=INK, width=1)
    # pitch lines
    d.line([(x0 + w // 2, y0), (x0 + w // 2, y0 + h)], fill=(255, 255, 255),
           width=2)
    d.ellipse([x0 + w // 2 - 22, y0 + h // 2 - 22, x0 + w // 2 + 22,
               y0 + h // 2 + 22], outline=(255, 255, 255), width=2)
    # goal
    d.rectangle([x0 + w - 34, y0 + 18, x0 + w - 6, y0 + 62],
                outline=(255, 255, 255), width=2)
    for gy in range(y0 + 22, y0 + 60, 8):
        d.line([(x0 + w - 34, gy), (x0 + w - 6, gy)], fill=(255, 255, 255),
               width=1)
    # ball
    bx, by = x0 + 70, y0 + h - 30
    d.ellipse([bx - 12, by - 12, bx + 12, by + 12], fill=(255, 255, 255),
              outline=INK, width=1)
    d.polygon([(bx, by - 6), (bx + 6, by - 2), (bx + 4, by + 5),
               (bx - 4, by + 5), (bx - 6, by - 2)], fill=INK)
    # scoreboard
    d.rectangle([x0 + 8, y0 + 8, x0 + 168, y0 + 30], fill=(20, 20, 20))
    d.text((x0 + 14, y0 + 11), "LILLE 2–1 BAYERN", font=font(SANS_B, 13),
           fill=(255, 220, 60))


def draw_climate(d, x0, y0, w, h):
    d.rectangle([x0, y0, x0 + w, y0 + h], fill=(222, 232, 226),
                outline=INK, width=1)
    # globe with a crack
    cx, cy, r = x0 + 80, y0 + 46, 34
    d.ellipse([cx - r, cy - r, cx + r, cy + r], fill=(90, 140, 190),
              outline=INK, width=2)
    d.ellipse([cx - 18, cy - 20, cx + 2, cy + 4], fill=(80, 150, 90))
    d.ellipse([cx - 2, cy + 8, cx + 22, cy + 28], fill=(80, 150, 90))
    d.line([(cx - 6, cy - 32), (cx + 4, cy - 10), (cx - 4, cy + 6),
            (cx + 8, cy + 30)], fill=RED, width=3)
    # EU stars ring
    for i in range(8):
        import math
        ang = math.pi * 2 * i / 8 - math.pi / 2
        sx = x0 + 218 + int(30 * math.cos(ang))
        sy = y0 + 46 + int(30 * math.sin(ang))
        d.ellipse([sx - 2, sy - 2, sx + 2, sy + 2], fill=(220, 180, 40))
    d.text((x0 + 196, y0 + h - 18), "NO DEAL", font=font(SANS_B, 12),
           fill=RED)
    # factory smoke
    for sx, sy, rr in ((x0 + 250, y0 + 12, 6), (x0 + 262, y0 + 6, 5)):
        d.ellipse([sx - rr, sy - rr, sx + rr, sy + rr], fill=(150, 150, 150))


GRID = [
    ("MIDDLE EAST", "HOUTHIS CLAIM STRIKE ON SAUDI'S BIGGEST REFINERY",
     "Yemen's Houthis say they hit the Ras Tanura refinery, the kingdom's "
     "largest. The coalition says it shot down four drones over the site.",
     draw_refinery),
    ("SPACE", "ASTEROID LEFT FLATTENED BY A GIANT CRATER",
     "ESA's Hera mission shows Dimorphos, struck by NASA's DART in 2022, "
     "flattened by a crater nearly as wide as the 151 m moonlet itself.",
     draw_asteroid),
    ("ECONOMY", "US ECONOMY TOO HOT: PRICES UP 3.8%",
     "October prices rose 3.8% on the year and third-quarter growth was "
     "revised up to 4.3%. Traders price a ~95–97% chance of a Fed hike.",
     draw_economy),
    ("WASHINGTON", "SENATOR DEMANDS ANSWERS ON HUANG'S RETURN",
     "Top Senate antitrust Democrat Cory Booker presses Nvidia on CEO "
     "Jensen Huang's reinstatement. A public hearing is set for 3 Dec.",
     draw_capitol),
    ("SPORT", "LILLE STUN BAYERN IN EUROPE",
     "Champions League, Matchday 5: Lille beat Bayern 2–1, Liverpool won "
     "3–0 at Club Brugge and PSG were held 2–2 by Roma.",
     draw_football),
    ("CLIMATE", "COP31 BLAME GAME: OPEC POINTS AT EU",
     "A day after the Antalya talks collapsed, OPEC's chief blamed the EU "
     "for the failure while Pope Leo XIV urged firm action on Earth.",
     draw_climate),
]


def draw_grid(d):
    cell_w = (CONTENT_W - 2 * GUTTER) // 3          # 313
    cell_h = 196
    y_rows = (476, 678)
    for i, (kick, head, body, art) in enumerate(GRID):
        col, row = i % 3, i // 3
        x = MARGIN + col * (cell_w + GUTTER)
        y = y_rows[row]
        art(d, x, y, cell_w, 80)
        d.text((x, y + 88), kick, font=font(SANS_B, 12), fill=RED)
        yy = para(d, x, y + 106, head, font(SERIF_B, 18), cell_w, 21)
        para(d, x, yy + 2, body, font(SANS, 13), cell_w, 16)


# ---------------------------------------------------------------- strip
def draw_strip(d):
    y0 = 896
    rule(d, MARGIN, y0, W - MARGIN, width=2)
    d.text((MARGIN, y0 + 10), "ALSO TODAY", font=font(SANS_B, 15), fill=RED)
    col_w = (CONTENT_W - 160) // 3
    items = [
        ("THANKSGIVING", "US stock and bond markets shut all day; trading "
         "resumes Friday, early close 1 p.m. ET."),
        ("EUROPE", "ECB holds its deposit rate steady at 2.50%; the next "
         "decision comes on 17 December."),
        ("BRAZIL", "Government targets a primary surplus of up to 2% of "
         "GDP by 2031; Congress caps spending growth at 2%."),
    ]
    x = MARGIN + 160
    for kick, text in items:
        para(d, x, y0 + 10, kick + " — " + text, font(SANS, 12), col_w - 12,
             15)
        x += col_w
    rule(d, MARGIN, 956, W - MARGIN, width=1, fill=LIGHT_RULE)


# ---------------------------------------------------------------- footer
def draw_footer(d):
    f = font(SANS, 12)
    line = ("THE WORLD  •  Thursday 26 November 2026  •  Sources: Reuters, "
            "AP, CNN, ESA, Xinhua  •  Drawn in code; no photographs.")
    d.text(((W - d.textlength(line, font=f)) / 2, 968), line, font=f,
           fill=MUTED)
    f2 = font(SANS, 11)
    line2 = "All events reported on 25–26 November 2026."
    d.text(((W - d.textlength(line2, font=f2)) / 2, 986), line2, font=f2,
           fill=MUTED)


def main():
    out = sys.argv[1] if len(sys.argv) > 1 else "entry.png"
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    draw_masthead(d)
    draw_ticker(d)
    draw_lead(d)
    draw_grid(d)
    draw_strip(d)
    draw_footer(d)
    img.save(out, "PNG", optimize=True)
    print(f"wrote {out}")


if __name__ == "__main__":
    main()
