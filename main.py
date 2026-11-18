#!/usr/bin/env python3
"""Newspaper front page for Tuesday 17 November 2026 world news.

Draws a 1024x1024 PNG front page: masthead, red date line, one lead
story and a 2x3 grid of story cards, then a footer. Fully deterministic
(same bytes on every run): no network, no clock, no randomness.
Writes /output/entry.png.
"""

import os
from PIL import Image, ImageDraw, ImageFont

PAGE_W, PAGE_H = 1024, 1024
PAPER = (250, 247, 240)   # #faf7f0 warm off-white
INK = (17, 17, 17)        # near-black
NAVY = (26, 42, 74)       # #1a2a4a
RED = (163, 29, 29)       # #a31d1d
GREEN = (30, 107, 74)     # #1e6b4a
OCHRE = (122, 74, 18)     # #7a4a12
GREY = (90, 90, 90)

FONTS = "/usr/share/fonts/truetype/liberation"

SERIF_BOLD = "LiberationSerif-Bold.ttf"
SERIF = "LiberationSerif-Regular.ttf"
SANS_BOLD = "LiberationSans-Bold.ttf"
SANS = "LiberationSans-Regular.ttf"


def load_font(name, size):
    return ImageFont.truetype(os.path.join(FONTS, name), size)


def wrap_text(text, font, max_width):
    """Greedy word wrap by measured pixel width."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if font.getlength(trial) <= max_width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def draw_masthead(d, left, right):
    y = 20
    d.line([(left, y), (right, y)], fill=INK, width=2)
    y += 12
    d.text((PAGE_W // 2, y), "WORLD NEWS",
           font=load_font(SERIF_BOLD, 88), fill=NAVY, anchor="mt")
    y += 96
    d.text((PAGE_W // 2, y), "Tuesday, 17 November 2026",
           font=load_font(SERIF, 34), fill=RED, anchor="mt")
    y += 44
    d.line([(left, y), (right, y)], fill=INK, width=5)
    return y + 18


def draw_lead(d, left, width, y):
    d.text((left, y), "MIDDLE EAST",
           font=load_font(SANS_BOLD, 18), fill=RED, anchor="lt")
    y += 26
    head_font = load_font(SERIF_BOLD, 48)
    for line in wrap_text("US strikes Iran after Hormuz tanker attacks",
                          head_font, width):
        d.text((left, y), line, font=head_font, fill=INK, anchor="lt")
        y += 56
    y += 6
    sum_font = load_font(SANS, 23)
    lead_sum = (
        "Warplanes hit missile sites on Qeshm Island; a tanker ablaze, "
        "24 seafarers rescued; Trump weighs an unverified "
        "'dirty bomb' report."
    )
    for line in wrap_text(lead_sum, sum_font, width):
        d.text((left, y), line, font=sum_font, fill=INK, anchor="lt")
        y += 29
    return y


def draw_grid(d, left, width, top, bottom):
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
    tag_font = load_font(SANS_BOLD, 18)
    # 27px: every card headline fits on one line (no orphaned word on a
    # second line — the two longest are 447.7 and 454.1px vs 458px wide).
    head_font = load_font(SERIF_BOLD, 27)
    sum_font = load_font(SANS, 19)

    gutter = 28
    col_w = (width - gutter) // 2
    col_x = [left, left + col_w + gutter]
    row_gap = 14
    row_h = (bottom - top - 2 * row_gap) // 3

    for row in range(3):
        row_top = top + row * (row_h + row_gap)
        for col in range(2):
            tag, color, headline, summary = cards[row * 2 + col]
            cx = col_x[col]
            d.line([(cx, row_top), (cx + col_w, row_top)], fill=INK, width=2)
            cy = row_top + 10
            d.text((cx, cy), tag, font=tag_font, fill=color, anchor="lt")
            cy += 26
            for line in wrap_text(headline, head_font, col_w):
                d.text((cx, cy), line, font=head_font, fill=INK, anchor="lt")
                cy += 33
            cy += 4
            for line in wrap_text(summary, sum_font, col_w):
                d.text((cx, cy), line, font=sum_font, fill=GREY, anchor="lt")
                cy += 24


def draw_footer(d, left, right, rule_y):
    d.line([(left, rule_y), (right, rule_y)], fill=INK, width=2)
    d.text((PAGE_W // 2, rule_y + 10),
           "Tuesday, 17 November 2026 \u00b7 Sources: Reuters, AP, AFP",
           font=load_font(SANS, 17), fill=GREY, anchor="mt")


def main():
    img = Image.new("RGB", (PAGE_W, PAGE_H), PAPER)
    d = ImageDraw.Draw(img)

    margin = 40
    left = margin
    right = PAGE_W - margin
    content_w = right - left

    y = draw_masthead(d, left, right)
    y = draw_lead(d, left, content_w, y)

    footer_rule_y = 966
    grid_top = y + 16
    grid_bottom = footer_rule_y - 14
    draw_grid(d, left, content_w, grid_top, grid_bottom)
    draw_footer(d, left, right, footer_rule_y)

    os.makedirs("/output", exist_ok=True)
    img.save("/output/entry.png", format="PNG")


if __name__ == "__main__":
    main()
