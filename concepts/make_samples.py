#!/usr/bin/env python3
"""Morabh — sample concept packages (saving / halal-gain theme).

Four directions, each in its own folder under concepts/samples/:
symbol.svg/png, app-icon.png, lockup.png, sizes.png, README.md.
"""
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "brand", "src"))
from textpath import shape_glyphs  # noqa: E402

BLUE = "#33509C"
DEEP = "#1F3B82"
TINT = "#A2BCFF"
TINT25 = "#DEE7FF"
GREEN = "#074D31"
GOLD = "#F1DC84"
WHITE = "#FFFFFF"

MANROPE = os.path.join(HERE, "..", "brand", "fonts", "Manrope.ttf")
CAIRO = os.path.join(HERE, "..", "brand", "fonts", "Cairo.ttf")
AR = "\u0645\u064f\u0631\u0627\u0628\u0650\u062d"
MARKS = {"uni064F", "uni0650"}


def run(cmd):
    subprocess.run(cmd, check=True)


def wm(text_font, text, size, color, mark_color=None):
    glyphs, adv, _, _ = shape_glyphs(text_font, text, size,
                                     {"wght": 800 if text_font == MANROPE else 600})
    parts = []
    for g in glyphs:
        c = (mark_color or color) if g["name"] in MARKS else color
        parts.append(f'<path d="{g["d"]}" fill="{c}"/>')
    return "".join(parts), adv


def svg_doc(w, h, body, bg=WHITE):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
            f'width="{w}" height="{h}"><rect width="{w}" height="{h}" fill="{bg}"/>{body}</svg>')


# ------------------------------------------------------------------ symbols
def sym_hassala(mark=BLUE, coin=GREEN, slot=WHITE):
    """Egyptian hassala (clay money box): dome + slot + coin dropping in edge-on."""
    return (f'<path d="M 96 408 A 160 160 0 0 1 416 408 Z" fill="{mark}"/>'
            f'<rect x="196" y="256" width="120" height="34" rx="17" fill="{slot}"/>'
            f'<rect x="234" y="132" width="44" height="136" rx="22" fill="{coin}"/>')


def sym_meem_coin(mark=BLUE, slot=WHITE):
    """Coin with the Rising Meem carved out, its tail opening through the rim."""
    return (f'<circle cx="256" cy="276" r="170" fill="{mark}"/>'
            f'<circle cx="200" cy="334" r="52" fill="{slot}"/>'
            f'<path d="M 240 296 L 422 114" stroke="{slot}" stroke-width="48" '
            f'stroke-linecap="round" fill="none"/>')


def sym_rising_fill(base=TINT, fill=BLUE, goal=GREEN):
    """Coin filling diagonally upward — savings level rising toward the goal."""
    return (f'<defs><clipPath id="c"><circle cx="256" cy="276" r="166"/></clipPath></defs>'
            f'<circle cx="256" cy="276" r="166" fill="{base}"/>'
            f'<path d="M 70 360 L 442 236 L 442 460 L 70 460 Z" fill="{fill}" clip-path="url(#c)"/>'
            f'<circle cx="352" cy="172" r="30" fill="{goal}"/>')


def sym_ellipsis(a=BLUE, b=BLUE, c=GREEN):
    """Ellipsis rising — installments to be continued, ending in the gain."""
    return (f'<circle cx="112" cy="400" r="44" fill="{a}"/>'
            f'<circle cx="252" cy="304" r="58" fill="{b}"/>'
            f'<circle cx="402" cy="182" r="74" fill="{c}"/>')


SAMPLES = {
    "01-hassala": dict(
        title="The Hassala — الحصّالة",
        sym=sym_hassala,
        icon=lambda: sym_hassala(mark=WHITE, coin=GOLD, slot=BLUE),
        readme="""# Sample 01 — The Hassala (الحصّالة)

**Perspective: the user saving.**

The Egyptian clay money box — the answer every Egyptian home already has to the
(haram) piggy bank. Reduced to three shapes: a dome, a slot, and a coin about to drop.

- **Saving story:** money going in, kept safe — the most universal saving image in Egypt.
- **Sharia by nature:** it *is* the halal alternative to the piggy bank; no religious symbols needed.
- **The coin doubles as the damma dot** over the dome (مُ).
- **Unique vs Takka:** Takka's identity is speed ("a click"); this owns *keeping and growing*.
- Risk: dome silhouette must stay geometric so it never reads as architecture.
""",
    ),
    "02-meem-coin": dict(
        title="The Meem Coin — negative space",
        sym=sym_meem_coin,
        icon=lambda: sym_meem_coin(mark=WHITE, slot=BLUE),
        readme="""# Sample 02 — The Meem Coin

**Perspective: the owner's identity — مُرابِح, the one who gains.**

A solid coin with the Rising Meem carved out of it in negative space: the meem head
and a tail that climbs out toward the rim.

- **The gain lives inside the money** — the brand's name is literally cut into the coin
  (FedEx-arrow style hidden detail: people who spot the م never unsee it).
- **One solid shape** — the boldest, most app-icon-native option; unbeatable at 16 px.
- **Sharia positioning** through the Arabic letterform itself, not ornament.
- **Unique vs Takka:** Takka uses a wordmark-led identity; a negative-space coin-monogram
  is instantly differentiated on a store shelf of fintech icons.
- Risk: needs careful curve tuning so the cutout reads as م and not a keyhole.
""",
    ),
    "03-rising-fill": dict(
        title="The Rising Fill — saving level",
        sym=sym_rising_fill,
        icon=lambda: sym_rising_fill(base="#4A66B0", fill=WHITE, goal=GOLD),
        readme="""# Sample 03 — The Rising Fill

**Perspective: the user watching savings grow.**

A coin filling up — but diagonally, like a level rising toward a goal-dot near the rim.

- **Saving made visible:** the fill *is* your progress; the green dot is the goal (the gain).
- **Product-true:** the same graphic can be the app's live progress element — the logo
  literally fills as the user completes installments.
- **Dynamic, not static:** the diagonal makes it growth, not a 50/50 split.
- **Unique vs Takka:** nothing in their system shows *state*; this mark is alive.
- Risk: must keep the chord angle fixed brand-wide so it stays a mark, not a chart.
""",
    ),
    "04-ellipsis-rising": dict(
        title="The Ellipsis Rising — to be continued",
        sym=sym_ellipsis,
        icon=lambda: sym_ellipsis(a=WHITE, b=WHITE, c=GOLD),
        readme="""# Sample 04 — The Ellipsis Rising

**Perspective: both — pay later (user) and growing gain (owner).**

Three dots, rising and growing; the last one is the gain in Sharia green.

- **"…" is the universal sign for *later*** — the product in one glyph.
- **Each dot an installment**, growing in value as they rise.
- **Arabic-native:** Arabic script is defined by dots (إعجام), and the damma in مُرابِح
  is already a dot — no calligraphy needed.
- **Built-in motion:** dot… dot… dot — splash animation and loading indicator for free.
- **Unique vs Takka:** they own a static bold wordmark; this owns a *rhythm*.
- Risk: typing-indicator association — countered by the fixed diagonal + size + color signature.
""",
    ),
}


# ------------------------------------------------------------------ builders
def build_sample(key, spec):
    d = os.path.join(HERE, "samples", key)
    os.makedirs(d, exist_ok=True)
    # symbol
    sym_svg = svg_doc(512, 512, spec["sym"]())
    with open(os.path.join(d, "symbol.svg"), "w") as f:
        f.write(sym_svg)
    run(["rsvg-convert", "-w", "512", os.path.join(d, "symbol.svg"),
         "-o", os.path.join(d, "symbol.png")])
    # app icon (flat primary bg so cut-outs match)
    icon_svg = svg_doc(512, 512,
                       f'<rect width="512" height="512" rx="114" fill="{BLUE}"/>'
                       f'<g transform="translate(51 51) scale(0.8)">{spec["icon"]()}</g>',
                       bg="none")
    p = os.path.join(d, "app-icon.svg")
    with open(p, "w") as f:
        f.write(icon_svg)
    run(["rsvg-convert", "-w", "512", p, "-o", os.path.join(d, "app-icon.png")])
    # lockup: symbol + EN + AR
    en_paths, en_adv = wm(MANROPE, "morabh", 120, BLUE)
    ar_paths, ar_adv = wm(CAIRO, AR, 82, "#5A7CD4", GREEN)
    lock = (f'<g transform="translate(40 60) scale(0.55)">{spec["sym"]()}</g>'
            f'<g transform="translate(360 218)">{en_paths}</g>'
            f'<g transform="translate(364 320)">{ar_paths}</g>')
    W = int(360 + en_adv + 60)
    p = os.path.join(d, "lockup.svg")
    with open(p, "w") as f:
        f.write(svg_doc(W, 400, lock))
    run(["rsvg-convert", "-w", str(W * 2), p, "-o", os.path.join(d, "lockup.png")])
    # sizes strip: 512 / 48 / 16
    sp = os.path.join(d, "symbol.png")
    t48 = os.path.join(d, "_48.png")
    t16 = os.path.join(d, "_16.png")
    run(["convert", sp, "-resize", "48x48", t48])
    run(["convert", sp, "-resize", "16x16", t16])
    run(["convert", t48, "-scale", "512x512", t48])
    run(["convert", t16, "-scale", "512x512", t16])
    run(["montage", sp, t48, t16, "-tile", "3x1", "-geometry", "+8+8",
         "-background", "#F3F4F6", os.path.join(d, "sizes.png")])
    os.remove(t48)
    os.remove(t16)
    with open(os.path.join(d, "README.md"), "w") as f:
        f.write(spec["readme"])
    print("built", key)


if __name__ == "__main__":
    for key, spec in SAMPLES.items():
        build_sample(key, spec)
    # overview sheet
    tiles = []
    for key in SAMPLES:
        src = os.path.join(HERE, "samples", key, "symbol.png")
        lab = os.path.join(HERE, "samples", key, "_lab.png")
        run(["convert", src, "-resize", "340x340", "-gravity", "south",
             "-background", "white", "-splice", "0x44", "-font", "DejaVu-Sans",
             "-pointsize", "20", "-fill", "#4B5563",
             "-annotate", "+0+10", SAMPLES[key]["title"], lab])
        tiles.append(lab)
    run(["montage", *tiles, "-tile", "4x1", "-geometry", "+10+10",
         "-background", "#F3F4F6", os.path.join(HERE, "samples", "overview.png")])
    for t in tiles:
        os.remove(t)
    print("samples done")
