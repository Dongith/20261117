#!/usr/bin/env python3
"""World News front page for Tuesday 17 November 2026.

Renders a deterministic 1024x1024 newspaper front page with Pillow.
No network, no randomness, no clock: the same input always yields
the same bytes. Run: python3 main.py  ->  writes /output/entry.png
"""

from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
PAPER = (250, 247, 240)
NAVY = (26, 42, 74)
RED = (163, 29, 29)
INK = (34, 34, 34)
MUTED = (90, 90, 90)
RULE = (26, 42, 74)

TAG_HUES = {
    "EUROPE": (31, 78, 121),
    "ASIA": (15, 118, 110),
    "HEALTH": (45, 106, 46),
    "ASIA-PACIFIC": (107, 63, 160),
    "MIDDLE EAST": (154, 107, 0),
    "MARKETS": (127, 29, 29),
}

SERIF_B = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"
SERIF_R = "/usr/share/fonts/truetype/liberation/LiberationSerif-Regular.ttf"
SANS_B = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SANS_R = "/usr/share/fonts/truetype/liberation/LiberationSans-Regular.ttf"

W, H = 1024, 1024
MARGIN = 46
OUT = "/output/entry.png"

DATE_LINE = "Tuesday, 17 November 2026"

# ---------------------------------------------------------------- content
LEAD = {
    "tag": "US / IRAN",
    "head": "US strikes Iran after Hormuz tanker attacks",
    "body": (
        "US warplanes hit missile sites on Qeshm Island after a tanker was "
        "set ablaze in the Strait of Hormuz; 24 seafarers were rescued. "
        "Trump is weighing an unverified report of a \u2018dirty bomb\u2019."
    ),
}

CARDS = [
    {
        "tag": "EUROPE",
        "head": "Ukraine hits Crimean Bridge again",
        "body": "A road span collapsed after a Ukrainian strike; Russia "
                "answered by hitting bridges in Kyiv.",
    },
    {
        "tag": "ASIA",
        "head": "Trump in Asia for Xi\u2013Putin summit",
        "body": "Quad talks in Manila come first; a trilateral summit "
                "looms in Beijing as a Nvidia chips row shadows the trip.",
    },
    {
        "tag": "HEALTH",
        "head": "US loses measles elimination status",
        "body": "The US loses its measles elimination status for the "
                "first time since 2000 as cases climb.",
    },
    {
        "tag": "ASIA-PACIFIC",
        "head": "Japan scrambles jets at Russian planes",
        "body": "Japanese fighters scrambled to Russian aircraft near "
                "Okinoshima; Tokyo lodged a formal protest.",
    },
    {
        "tag": "MIDDLE EAST",
        "head": "Gaza: winter rains deepen shelter crisis",
        "body": "The UN warns winter rains are worsening the shelter "
                "crisis; Britain, Australia, Canada and Italy urge more aid.",
    },
    {
        "tag": "MARKETS",
        "head": "Wall Street falls as Nvidia in focus",
        "body": "US shares fell as investors awaited Nvidia results and "
                "weighed the outlook for AI spending.",
    },
]


# ---------------------------------------------------------------- helpers
class Sheet:
    """A thin wrapper around the drawing surface and its typefaces."""

    def __init__(self):
        self.img = Image.new("RGB", (W, H), PAPER)
        self.d = ImageDraw.Draw(self.img)

    def font(self, path, size):
        return ImageFont.truetype(path, size)

    def centre(self, y, text, font, fill):
        """Draw text centred on the page; return how far down it reaches.

        textbbox reports the glyph box relative to the draw origin, so
        the advance must be the box BOTTOM (box[3]), not its height:
        the top inset is blank font leading that the next line would
        otherwise overlap.
        """
        box = self.d.textbbox((0, 0), text, font=font)
        tw = box[2] - box[0]
        self.d.text(((W - tw) / 2, y), text, font=font, fill=fill)
        return box[3]

    def wrap(self, text, font, width):
        """Greedy word wrap; returns a list of lines that fit width."""
        lines = []
        for paragraph in text.split("\n"):
            words = paragraph.split()
            if not words:
                lines.append("")
                continue
            cur = words[0]
            for word in words[1:]:
                trial = cur + " " + word
                if self.d.textlength(trial, font=font) <= width:
                    cur = trial
                else:
                    lines.append(cur)
                    cur = word
            lines.append(cur)
        return lines

    def para(self, x, y, text, font, width, fill, leading):
        """Draw a wrapped paragraph; return the y just below it."""
        for line in self.wrap(text, font, width):
            self.d.text((x, y), line, font=font, fill=fill)
            y += leading
        return y


def hline(draw, y, thick, x0=MARGIN, x1=W - MARGIN, fill=RULE):
    draw.rectangle([x0, y, x1, y + thick - 1], fill=fill)


# ---------------------------------------------------------------- sections
def masthead(sheet):
    y = 26
    y += sheet.centre(y, "WORLD NEWS", sheet.font(SERIF_B, 92), NAVY)
    y += 6
    y += sheet.centre(y, DATE_LINE, sheet.font(SERIF_B, 33), RED)
    y += 14
    hline(sheet.d, y, 5)
    hline(sheet.d, y + 10, 1)
    return y + 26


def lead_block(sheet, y):
    f_tag = sheet.font(SANS_B, 22)
    f_head = sheet.font(SERIF_B, 48)
    f_body = sheet.font(SERIF_R, 26)
    sheet.d.text((MARGIN, y), LEAD["tag"], font=f_tag, fill=RED)
    y += 34
    y = sheet.para(MARGIN, y, LEAD["head"], f_head, W - 2 * MARGIN, NAVY, 56)
    y += 10
    y = sheet.para(MARGIN, y, LEAD["body"], f_body, W - 2 * MARGIN, INK, 34)
    return y


def card(sheet, x, y, w, h, story):
    f_tag = sheet.font(SANS_B, 18)
    f_head = sheet.font(SERIF_B, 29)
    f_body = sheet.font(SERIF_R, 20)
    hue = TAG_HUES[story["tag"]]
    sheet.d.text((x, y), story["tag"], font=f_tag, fill=hue)
    cy = y + 28
    cy = sheet.para(x, cy, story["head"], f_head, w, NAVY, 35)
    cy = sheet.para(x, cy + 4, story["body"], f_body, w, INK, 26)
    return y + h


def grid(sheet, y):
    col_w = (W - 2 * MARGIN - 24) // 2
    row_h = 150
    gap = 16
    for i, story in enumerate(CARDS):
        col = i % 2
        row = i // 2
        x = MARGIN + col * (col_w + 24)
        card(sheet, x, y + row * (row_h + gap), col_w, row_h, story)
    return y + 3 * row_h + 2 * gap


def footer(sheet):
    f = sheet.font(SANS_R, 18)
    text = DATE_LINE + " \u00b7 Sources: Reuters, AP, AFP"
    box = sheet.d.textbbox((0, 0), text, font=f)
    tw = box[2] - box[0]
    sheet.d.text(((W - tw) / 2, H - 34), text, font=f, fill=MUTED)


# ---------------------------------------------------------------- main
def main():
    sheet = Sheet()
    y = masthead(sheet)
    y = lead_block(sheet, y)
    y += 18
    hline(sheet.d, y, 1)
    y = grid(sheet, y + 18)
    footer(sheet)
    sheet.img.save(OUT, format="PNG")


if __name__ == "__main__":
    main()
