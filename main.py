#!/usr/bin/env python3
"""Draw a newspaper-style front page summing up Tuesday 17 November 2026
world news. Deterministic: same bytes every run, no network, no time,
no randomness. Writes /output/entry.png (1024x1024)."""

import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
PAPER = (250, 247, 240)          # #faf7f0 warm off-white
INK = (17, 17, 17)               # near-black
NAVY = (26, 42, 74)              # #1a2a4a
RED = (163, 29, 29)              # #a31d1d
GREEN = (30, 107, 74)            # #1e6b4a
OCHRE = (122, 74, 18)            # #7a4a12
GREY = (90, 90, 90)

FONT_DIR = "/usr/share/fonts/truetype/liberation"


def font(name, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, name), size)


SERIF_B = "LiberationSerif-Bold.ttf"
SERIF_R = "LiberationSerif-Regular.ttf"
SANS_B = "LiberationSans-Bold.ttf"
SANS_R = "LiberationSans-Regular.ttf"


def wrap(text, fnt, max_w):
    """Greedy word wrap by measured width. Returns a list of lines."""
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        trial = (cur + " " + w).strip()
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines


def main():
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)

    margin = 40
    x0 = margin
    x1 = W - margin
    cw = x1 - x0  # 944

    # ---- Masthead -------------------------------------------------------
    y = 20
    d.line([(x0, y), (x1, y)], fill=INK, width=2)
    y += 12
    mast = font(SERIF_B, 88)
    d.text((W // 2, y), "WORLD NEWS", font=mast, fill=NAVY, anchor="mt")
    y += 96
    date_f = font(SERIF_R, 34)
    d.text((W // 2, y), "Tuesday, 17 November 2026", font=date_f,
           fill=RED, anchor="mt")
    y += 44
    d.line([(x0, y), (x1, y)], fill=INK, width=5)
    y += 18

    # ---- Lead story -----------------------------------------------------
    kicker_f = font(SANS_B, 18)
    d.text((x0, y), "MIDDLE EAST", font=kicker_f, fill=RED, anchor="lt")
    y += 26
    head_f = font(SERIF_B, 48)
    head_lines = wrap("US strikes Iran after Hormuz tanker attacks",
                      head_f, cw)
    for ln in head_lines:
        d.text((x0, y), ln, font=head_f, fill=INK, anchor="lt")
        y += 56
    y += 6
    sum_f = font(SANS_R, 23)
    sum_lines = wrap(
        "Warplanes hit missile sites on Qeshm Island; a tanker ablaze, "
        "24 seafarers rescued; Trump weighs an unverified "
        "'dirty bomb' report.",
        sum_f, cw)
    for ln in sum_lines:
        d.text((x0, y), ln, font=sum_f, fill=INK, anchor="lt")
        y += 29

    # ---- Grid of 6 cards ------------------------------------------------
    cards = [
        ("EUROPE", NAVY,
         "Ukraine hits Crimean Bridge again",
         "A road span collapses into the sea; Russia answers with "
         "strikes on Kyiv bridges."),
        ("ASIA", RED,
         "Trump in Asia for Xi\u2013Putin summit",
         "Quad talks in Manila; a rare trilateral looms in Beijing as "
         "the Nvidia spy row simmers."),
        ("HEALTH", GREEN,
         "US loses measles elimination status",
         "First time since 2000, after a year of uninterrupted spread, "
         "officials confirm."),
        ("ASIA-PACIFIC", OCHRE,
         "Japan scrambles jets at Russian planes",
         "Two suspected Russian aircraft enter airspace near "
         "Okinoshima; Tokyo protests."),
        ("MIDDLE EAST", RED,
         "Gaza: winter rains deepen shelter crisis",
         "UN warns floods wreck tents and food; Britain, Australia, "
         "Canada and Italy urge aid access."),
        ("MARKETS", NAVY,
         "Wall Street falls as Nvidia in focus",
         "AI and tech shares drag indexes lower; Apple services hit by "
         "outages."),
    ]

    tag_f = font(SANS_B, 18)
    card_head_f = font(SERIF_B, 30)
    card_sum_f = font(SANS_R, 19)

    gutter = 28
    col_w = (cw - gutter) // 2
    col_x = [x0, x0 + col_w + gutter]

    grid_top = y + 16
    footer_rule_y = 966
    grid_bottom = footer_rule_y - 14
    row_gap = 14
    row_h = (grid_bottom - grid_top - 2 * row_gap) // 3

    for row in range(3):
        top = grid_top + row * (row_h + row_gap)
        for col in range(2):
            tag, color, headline, summary = cards[row * 2 + col]
            cx = col_x[col]
            # thin top rule
            d.line([(cx, top), (cx + col_w, top)], fill=INK, width=2)
            cy = top + 10
            d.text((cx, cy), tag, font=tag_f, fill=color, anchor="lt")
            cy += 26
            for ln in wrap(headline, card_head_f, col_w):
                d.text((cx, cy), ln, font=card_head_f, fill=INK,
                       anchor="lt")
                cy += 36
            cy += 4
            for ln in wrap(summary, card_sum_f, col_w):
                d.text((cx, cy), ln, font=card_sum_f, fill=GREY,
                       anchor="lt")
                cy += 24

    # ---- Footer ---------------------------------------------------------
    d.line([(x0, footer_rule_y), (x1, footer_rule_y)], fill=INK, width=2)
    foot_f = font(SANS_R, 17)
    d.text((W // 2, footer_rule_y + 10),
           "Tuesday, 17 November 2026 \u00b7 Sources: Reuters, AP, AFP",
           font=foot_f, fill=GREY, anchor="mt")

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG")


if __name__ == "__main__":
    main()
