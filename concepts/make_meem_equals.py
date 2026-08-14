#!/usr/bin/env python3
"""Meem-Equals concept: two Arabic meems (Cairo font), one mirrored,
stacked like an equals sign. Color #6C8DDF on white."""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "brand", "src"))
from textpath import shape_glyphs, shape_bounds  # noqa: E402

CAIRO = os.path.join(HERE, "..", "brand", "fonts", "Cairo.ttf")
MANROPE = os.path.join(HERE, "..", "brand", "fonts", "Manrope.ttf")
LIGHT = "#6C8DDF"
PRIMARY = "#33509C"
GREEN = "#074D31"
WHITE = "#FFFFFF"
AR_WORD = "\u0645\u064f\u0631\u0627\u0628\u0650\u062d"
MARKS = {"uni064F", "uni0650"}

OUTD = os.path.join(HERE, "meem-equals")
os.makedirs(OUTD, exist_ok=True)


def meem_path(size=260, weight=600):
    """Initial-form meem with kashida (مـــ): head + horizontal bar."""
    text = "\u0645\u0640\u0640"  # meem + 2 tatweel for a longer bar
    glyphs, adv, _, _ = shape_glyphs(CAIRO, text, size, {"wght": weight})
    b = shape_bounds(CAIRO, text, size, {"wght": weight})
    return " ".join(g["d"] for g in glyphs), b


def render(svg_path, png_path, w):
    subprocess.run(["rsvg-convert", "-w", str(w), svg_path, "-o", png_path], check=True)


def doc(w, h, body, bg=WHITE):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


def meem_equals_frag(cx, cy, size, gap, color_top, color_bot):
    """Two meems stacked like '=': top normal, bottom mirrored horizontally."""
    d, (x0, y0, x1, y1) = meem_path(size)
    gw, gh = x1 - x0, y1 - y0
    # top meem: centered at (cx, cy - gap/2 - gh/2)
    ty = cy - gap / 2 - gh
    top = (f'<g transform="translate({cx - gw/2 - x0:.2f} {ty - y0:.2f})">'
           f'<path d="{d}" fill="{color_top}"/></g>')
    # bottom meem: mirrored horizontally around its own center
    by = cy + gap / 2
    bot = (f'<g transform="translate({cx + gw/2 + x0:.2f} {by - y0:.2f}) scale(-1 1)">'
           f'<path d="{d}" fill="{color_bot}"/></g>')
    return top + bot, gw, gh


def build_symbols():
    variants = {
        "meem-equals": (LIGHT, LIGHT),
        "meem-equals-duotone": (PRIMARY, LIGHT),
    }
    labels = []
    for name, (c1, c2) in variants.items():
        frag, gw, gh = meem_equals_frag(256, 256, 300, 36, c1, c2)
        p = os.path.join(OUTD, name + ".svg")
        with open(p, "w") as f:
            f.write(doc(512, 512, frag))
        render(p, os.path.join(OUTD, name + ".png"), 512)
        labels.append(name)
    # app-icon style: white meems on light-blue tile
    frag, _, _ = meem_equals_frag(256, 256, 300, 36, WHITE, WHITE)
    p = os.path.join(OUTD, "meem-equals-icon.svg")
    with open(p, "w") as f:
        f.write(doc(512, 512, f'<rect width="512" height="512" rx="114" fill="{LIGHT}"/>' + frag,
                    bg="none"))
    render(p, os.path.join(OUTD, "meem-equals-icon.png"), 512)
    # sheet
    tiles = []
    for name, lab in (("meem-equals", "Meem = Meem  #6C8DDF"),
                      ("meem-equals-duotone", "Duotone variant"),
                      ("meem-equals-icon", "Icon tile")):
        t = os.path.join(OUTD, "_l-" + name + ".png")
        subprocess.run(["convert", os.path.join(OUTD, name + ".png"), "-resize", "340x340",
                        "-gravity", "south", "-background", "white", "-splice", "0x44",
                        "-font", "DejaVu-Sans", "-pointsize", "20", "-fill", "#4B5563",
                        "-annotate", "+0+10", lab, t], check=True)
        tiles.append(t)
    subprocess.run(["montage", *tiles, "-tile", "3x1", "-geometry", "+10+10",
                    "-background", "#F3F4F6", os.path.join(OUTD, "sheet-meem-equals.png")],
                   check=True)
    for t in tiles:
        os.remove(t)
    # tiny size test
    subprocess.run(["convert", os.path.join(OUTD, "meem-equals.png"), "-resize", "32x32",
                    "-scale", "160x160", os.path.join(OUTD, "tiny-32.png")], check=True)


def wm(font, text, size, color, mark_color=None, weight=None):
    w = weight or (800 if font == MANROPE else 600)
    glyphs, adv, _, _ = shape_glyphs(font, text, size, {"wght": w})
    b = shape_bounds(font, text, size, {"wght": w})
    parts = []
    for g in glyphs:
        c = (mark_color or color) if g["name"] in MARKS else color
        parts.append(f'<path d="{g["d"]}" fill="{c}"/>')
    return "".join(parts), b


def build_splash():
    W, H = 390, 844
    parts = []
    # pure white background, whisper tint corners kept out per request
    frag, gw, gh = meem_equals_frag(W / 2, H * 0.40, 150, 20, LIGHT, LIGHT)
    parts.append(frag)
    en_paths, eb = wm(MANROPE, "morabh", 34, LIGHT)
    ew = eb[2] - eb[0]
    by = H * 0.40 + (2 * (gh_est := 0) + 0)  # placeholder, computed below
    # position wordmarks below the mark block (mark block height = 2*gh + gap)
    d, (x0, y0, x1, y1) = meem_path(150)
    mh = (y1 - y0) * 2 + 20
    base_y = H * 0.40 + mh / 2 + 64
    parts.append(f'<g transform="translate({W/2 - ew/2 - eb[0]:.2f} {base_y:.2f})">{en_paths}</g>')
    ar_paths, ab = wm(CAIRO, AR_WORD, 30, LIGHT, GREEN)
    aw = ab[2] - ab[0]
    parts.append(f'<g transform="translate({W/2 - aw/2 - ab[0]:.2f} {base_y + 44:.2f})">{ar_paths}</g>')
    for i, op in enumerate((0.35, 0.6, 1.0)):
        parts.append(f'<circle cx="{W/2 + (i-1)*16:.0f}" cy="{H*0.88:.0f}" r="4" '
                     f'fill="{LIGHT}" opacity="{op}"/>')
    p = os.path.join(OUTD, "splash-meem-equals.svg")
    with open(p, "w") as f:
        f.write(doc(W, H, "".join(parts)))
    render(p, os.path.join(OUTD, "splash-meem-equals.png"), 780)
    # iOS-size export
    render(p, os.path.join(OUTD, "splash-meem-equals-1284x2778.png"), 1284)


if __name__ == "__main__":
    build_symbols()
    build_splash()
    print("meem-equals done")
