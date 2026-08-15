#!/usr/bin/env python3
"""Morabh — Square-Kufic Meem (مربع style) identity kit.

The mark: a custom square-Kufic م in #6C8DDF whose square counter holds a
rising staircase (installments inside the money-letter), crowned by a damma
that is a miniature meem. Lockup: مُرابِح over Morabh beside the letter.

Outputs to ../../brand-meem-square/: logo, lockups, app icons, favicons,
static + animated splash (letter builds itself, then the words appear,
all inside a card rectangle).
"""
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from textpath import shape_glyphs, shape_bounds  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, "..", "..", "brand-meem-square"))
FONTS = os.path.join(HERE, "..", "fonts")
CAIRO = os.path.join(FONTS, "Cairo.ttf")
MANROPE = os.path.join(FONTS, "Manrope.ttf")

LIGHT = "#6C8DDF"     # the letter
PRIMARY = "#33509C"   # Arabic wordmark
TILE = "#DEE7FF"      # background color (Primary 25)
CARD = "#FFFFFF"
GREEN = "#074D31"     # damma
GOLD = "#F1DC84"
WHITE = "#FFFFFF"
P400 = "#5A7CD4"

AR_WORD = "\u0645\u064f\u0631\u0627\u0628\u0650\u062d"
MARKS = {"uni064F", "uni0650"}


def run(cmd):
    subprocess.run(cmd, check=True)


def write_svg(rel, w, h, body, bg=None):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bgr = f'<rect width="{w}" height="{h}" fill="{bg}"/>' if bg else ""
    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
                f'width="{w}" height="{h}">{bgr}{body}</svg>')
    return path


def render(rel, png_rel, w=None, h=None):
    svg = os.path.join(OUT, rel)
    png = os.path.join(OUT, png_rel)
    os.makedirs(os.path.dirname(png), exist_ok=True)
    cmd = ["rsvg-convert", svg, "-o", png]
    if w:
        cmd += ["-w", str(w)]
    if h:
        cmd += ["-h", str(h)]
    run(cmd)


# ----------------------------------------------------------- the letter
# 512 design space. Letter bbox: x 62..350, y 96..390 (damma above: y 20..76)
def letter_pieces(color=LIGHT, damma_color=GREEN, steps=True, simple=False):
    """Return dict of svg fragments: head(ring), steps, tail, damma."""
    ring = (f'<path fill-rule="evenodd" fill="{color}" d="'
            f'M 174 96 H 326 Q 350 96 350 120 V 272 Q 350 296 326 296 H 174 '
            f'Q 150 296 150 272 V 120 Q 150 96 174 96 Z '
            f'M 196 142 V 250 H 304 V 142 Z"/>')
    stair = ""
    if steps and not simple:
        stair = (f'<g fill="{color}">'
                 f'<rect x="196" y="224" width="108" height="26"/>'
                 f'<rect x="232" y="198" width="72" height="26"/>'
                 f'<rect x="268" y="172" width="36" height="26"/>'
                 f'</g>')
    tail = (f'<g fill="{color}">'
            f'<rect x="150" y="272" width="46" height="118" rx="0"/>'
            f'<path d="M 76 344 H 196 V 390 H 76 Q 62 390 62 376 V 358 Q 62 344 76 344 Z"/>'
            f'</g>')
    if simple:
        damma = f'<rect x="296" y="28" width="48" height="48" rx="10" fill="{damma_color}"/>'
    else:
        damma = (f'<path fill-rule="evenodd" fill="{damma_color}" d="'
                 f'M 302 20 H 336 Q 348 20 348 32 V 64 Q 348 76 336 76 H 302 '
                 f'Q 290 76 290 64 V 32 Q 290 20 302 20 Z '
                 f'M 308 38 V 58 H 330 V 38 Z"/>'
                 f'<rect x="266" y="58" width="24" height="18" fill="{damma_color}"/>')
    return {"ring": ring, "steps": stair, "tail": tail, "damma": damma}


def letter_frag(color=LIGHT, damma_color=GREEN, simple=False):
    p = letter_pieces(color, damma_color, simple=simple)
    return p["ring"] + p["steps"] + p["tail"] + p["damma"]


L_X0, L_Y0, L_X1, L_Y1 = 62, 20, 350, 390   # incl. damma
L_W, L_H = L_X1 - L_X0, L_Y1 - L_Y0


def letter_placed(x, y, h, color=LIGHT, damma_color=GREEN, simple=False):
    s = h / L_H
    return (f'<g transform="translate({x - L_X0*s:.2f} {y - L_Y0*s:.2f}) scale({s:.5f})">'
            f'{letter_frag(color, damma_color, simple)}</g>')


# ----------------------------------------------------------- wordmarks
def word(font, text, size, color, mark_color=None):
    wght = 800 if font == MANROPE else 600
    glyphs, adv, _, _ = shape_glyphs(font, text, size, {"wght": wght})
    b = shape_bounds(font, text, size, {"wght": wght})
    parts = []
    for g in glyphs:
        c = (mark_color or color) if g["name"] in MARKS else color
        parts.append(f'<path d="{g["d"]}" fill="{c}"/>')
    return "".join(parts), b


# ----------------------------------------------------------- assets
def build_logo():
    # letter alone — transparent + on tile
    pad = 40
    write_svg("logo/meem-square.svg", L_W + 2*pad, L_H + 2*pad,
              letter_placed(pad, pad, L_H))
    render("logo/meem-square.svg", "logo/meem-square.png", w=800)
    write_svg("logo/meem-square-tile.svg", 512, 512,
              f'<rect width="512" height="512" rx="72" fill="{TILE}"/>'
              + letter_placed((512 - L_W*0.72)/2, (512 - L_H*0.72)/2, L_H*0.72))
    render("logo/meem-square-tile.svg", "logo/meem-square-tile.png", w=800)

    # lockup: letter left, مُرابِح over Morabh right, block centered to letter
    ar_paths, ab = word(CAIRO, AR_WORD, 92, PRIMARY, GREEN)
    en_paths, eb = word(MANROPE, "morabh", 76, LIGHT)
    aw, ah = ab[2] - ab[0], ab[3] - ab[1]
    ew, eh = eb[2] - eb[0], eb[3] - eb[1]
    gap_words = 26
    block_h = ah + gap_words + eh
    letter_h = 330
    W = 60 + L_W * (letter_h / L_H) + 70 + max(aw, ew) + 60
    H = letter_h + 120
    cy = H / 2
    parts = [letter_placed(60, cy - letter_h/2, letter_h)]
    bx = 60 + L_W * (letter_h / L_H) + 70
    top = cy - block_h / 2
    parts.append(f'<g transform="translate({bx - ab[0]:.2f} {top - ab[1]:.2f})">{ar_paths}</g>')
    parts.append(f'<g transform="translate({bx - eb[0]:.2f} {top + ah + gap_words - eb[1]:.2f})">{en_paths}</g>')
    write_svg("logo/lockup-horizontal.svg", W, H, "".join(parts))
    render("logo/lockup-horizontal.svg", "logo/lockup-horizontal.png", w=1600)
    write_svg("logo/lockup-horizontal-tile.svg", W, H,
              f'<rect width="{W:.0f}" height="{H:.0f}" rx="40" fill="{TILE}"/>' + "".join(parts))
    render("logo/lockup-horizontal-tile.svg", "logo/lockup-horizontal-tile.png", w=1600)


def build_icons():
    # mobile app icon — LETTER ONLY on tile background
    frag = (f'<rect width="1024" height="1024" fill="{TILE}"/>'
            + letter_placed((1024 - L_W*1.35)/2, (1024 - L_H*1.35)/2, L_H*1.35))
    write_svg("app-icons/icon-square-1024.svg", 1024, 1024, frag)
    render("app-icons/icon-square-1024.svg", "app-icons/ios/AppIcon-1024.png")
    frag = (f'<rect width="1024" height="1024" rx="229" fill="{TILE}"/>'
            + letter_placed((1024 - L_W*1.35)/2, (1024 - L_H*1.35)/2, L_H*1.35))
    write_svg("app-icons/icon-rounded-1024.svg", 1024, 1024, frag)
    for s in (1024, 512, 192, 180):
        render("app-icons/icon-rounded-1024.svg", f"app-icons/icon-rounded-{s}.png", w=s, h=s)
    # dark alt
    frag = (f'<rect width="1024" height="1024" rx="229" fill="#122F78"/>'
            + letter_placed((1024 - L_W*1.35)/2, (1024 - L_H*1.35)/2, L_H*1.35,
                            color="#A2BCFF", damma_color=GOLD))
    write_svg("app-icons/icon-rounded-dark-1024.svg", 1024, 1024, frag)
    render("app-icons/icon-rounded-dark-1024.svg", "app-icons/icon-rounded-dark-1024.png")
    # android adaptive
    write_svg("app-icons/android/adaptive-foreground.svg", 1024, 1024,
              letter_placed((1024 - L_W*0.95)/2, (1024 - L_H*0.95)/2, L_H*0.95))
    render("app-icons/android/adaptive-foreground.svg",
           "app-icons/android/adaptive-foreground-432.png", w=432, h=432)
    write_svg("app-icons/android/adaptive-background.svg", 1024, 1024,
              f'<rect width="1024" height="1024" fill="{TILE}"/>')
    render("app-icons/android/adaptive-background.svg",
           "app-icons/android/adaptive-background-432.png", w=432, h=432)


def build_favicons():
    # simplified letter (no steps, solid damma) — white on #6C8DDF for punch
    frag = (f'<rect width="512" height="512" rx="112" fill="{LIGHT}"/>'
            + letter_placed((512 - L_W*0.78)/2, (512 - L_H*0.78)/2, L_H*0.78,
                            color=WHITE, damma_color=GOLD, simple=True))
    write_svg("favicon/favicon.svg", 512, 512, frag)
    for s in (16, 32, 48, 180, 192, 512):
        render("favicon/favicon.svg", f"favicon/favicon-{s}x{s}.png", w=s, h=s)
    run(["convert", os.path.join(OUT, "favicon/favicon-16x16.png"),
         os.path.join(OUT, "favicon/favicon-32x32.png"),
         os.path.join(OUT, "favicon/favicon-48x48.png"),
         os.path.join(OUT, "favicon/favicon.ico")])
    frag = (f'<rect width="512" height="512" fill="{LIGHT}"/>'
            + letter_placed((512 - L_W*0.6)/2, (512 - L_H*0.6)/2, L_H*0.6,
                            color=WHITE, damma_color=GOLD, simple=True))
    write_svg("favicon/maskable.svg", 512, 512, frag)
    render("favicon/maskable.svg", "favicon/maskable-512x512.png", w=512, h=512)


# ----------------------------------------------------------- splash
VW, VH = 390, 844
# card rectangle
CX, CY, CW, CH, CR = 45, 168, 300, 470, 30
T_CARD = 0.10
T_RING, T_STEPS, T_TAIL, T_DAMMA = 0.45, 0.85, 1.30, 1.55
T_AR, T_EN, STAG = 1.85, 2.20, 0.07
T_LOADER = 2.70


def splash_layout():
    letter_h = 210
    s = letter_h / L_H
    lx = CX + (CW - L_W * s) / 2
    ly = CY + 52
    ar_size, en_size = 36, 30
    arp, ab = word(CAIRO, AR_WORD, ar_size, PRIMARY, GREEN)
    enp, eb = word(MANROPE, "morabh", en_size, LIGHT)
    ar_y = ly + letter_h + 64
    en_y = ar_y + (ab[3] - ab[1]) + 18
    return dict(letter_h=letter_h, s=s, lx=lx, ly=ly,
                arp=arp, ab=ab, enp=enp, eb=eb, ar_y=ar_y, en_y=en_y)


def splash_static_frag():
    L = splash_layout()
    parts = [f'<rect width="{VW}" height="{VH}" fill="{TILE}"/>',
             f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{CR}" fill="{CARD}"/>']
    parts.append(letter_placed(L["lx"], L["ly"], L["letter_h"]))
    aw = L["ab"][2] - L["ab"][0]
    parts.append(f'<g transform="translate({CX + (CW-aw)/2 - L["ab"][0]:.2f} '
                 f'{L["ar_y"] - L["ab"][1]:.2f})">{L["arp"]}</g>')
    ew = L["eb"][2] - L["eb"][0]
    parts.append(f'<g transform="translate({CX + (CW-ew)/2 - L["eb"][0]:.2f} '
                 f'{L["en_y"] - L["eb"][1]:.2f})">{L["enp"]}</g>')
    for i, op in enumerate((0.35, 0.6, 1.0)):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.86:.0f}" r="4" '
                     f'fill="{P400}" opacity="{op}"/>')
    return "".join(parts)


def build_splash_static():
    write_svg("splash/splash-static.svg", VW, VH, splash_static_frag())
    render("splash/splash-static.svg", "splash/splash-1284x2778.png", w=1284, h=2778)
    render("splash/splash-static.svg", "splash/splash-1080x1920.png", w=1080, h=1920)
    render("splash/splash-static.svg", "splash/splash-preview.png", w=780)


def build_splash_animated():
    L = splash_layout()
    pieces = letter_pieces()
    css = f'''
    .card {{ animation: card .55s cubic-bezier(.22,1,.36,1) {T_CARD}s both;
             transform-box: fill-box; transform-origin: center; }}
    .ring {{ animation: rise .6s cubic-bezier(.22,1,.36,1) {T_RING}s both;
             transform-box: fill-box; transform-origin: center; }}
    .st rect {{ animation: slide .45s cubic-bezier(.22,1,.36,1) both; }}
    .st rect:nth-child(1) {{ animation-delay: {T_STEPS}s; }}
    .st rect:nth-child(2) {{ animation-delay: {T_STEPS+0.13}s; }}
    .st rect:nth-child(3) {{ animation-delay: {T_STEPS+0.26}s; }}
    .tail {{ animation: drop .5s cubic-bezier(.22,1,.36,1) {T_TAIL}s both;
             transform-box: fill-box; transform-origin: top center; }}
    .damma {{ animation: spring .55s cubic-bezier(.34,1.56,.64,1) {T_DAMMA}s both;
              transform-box: fill-box; transform-origin: center; }}
    .glyph {{ animation: pop .5s cubic-bezier(.22,1,.36,1) both;
              transform-box: fill-box; transform-origin: center bottom; }}
    .loader {{ opacity:0; animation: fadein .5s ease-out {T_LOADER}s forwards; }}
    .loader circle {{ animation: pulse 1.2s ease-in-out infinite; }}
    @keyframes card   {{ from {{ opacity:0; transform: scale(.94) translateY(14px); }}
                         to   {{ opacity:1; transform: none; }} }}
    @keyframes rise   {{ from {{ opacity:0; transform: translateY(18px) scale(.96); }}
                         to   {{ opacity:1; transform: none; }} }}
    @keyframes slide  {{ from {{ opacity:0; transform: translateX(26px); }}
                         to   {{ opacity:1; transform: none; }} }}
    @keyframes drop   {{ from {{ opacity:0; transform: scaleY(0); }}
                         to   {{ opacity:1; transform: scaleY(1); }} }}
    @keyframes spring {{ from {{ opacity:0; transform: translateY(-30px); }}
                         to   {{ opacity:1; transform: none; }} }}
    @keyframes pop    {{ from {{ opacity:0; transform: translateY(12px); }}
                         to   {{ opacity:1; transform: none; }} }}
    @keyframes fadein {{ to {{ opacity:1; }} }}
    @keyframes pulse  {{ 0%,100% {{ opacity:.3; }} 50% {{ opacity:1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .card,.ring,.st rect,.tail,.damma,.glyph,.loader,.loader circle
      {{ animation: none; opacity: 1; transform: none; }}
    }}'''
    s = L["s"]
    parts = [f'<style>{css}</style>',
             f'<rect width="{VW}" height="{VH}" fill="{TILE}"/>',
             f'<g class="card"><rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" '
             f'rx="{CR}" fill="{CARD}"/></g>']
    steps_rects = (f'<rect x="196" y="224" width="108" height="26" fill="{LIGHT}"/>'
                   f'<rect x="232" y="198" width="72" height="26" fill="{LIGHT}"/>'
                   f'<rect x="268" y="172" width="36" height="26" fill="{LIGHT}"/>')
    parts.append(f'<g transform="translate({L["lx"] - L_X0*s:.2f} {L["ly"] - L_Y0*s:.2f}) scale({s:.5f})">'
                 f'<g class="ring">{pieces["ring"]}</g>'
                 f'<g class="st">{steps_rects}</g>'
                 f'<g class="tail">{pieces["tail"]}</g>'
                 f'<g class="damma">{pieces["damma"]}</g>'
                 f'</g>')
    # Arabic word glyphs (reading order = cluster ascending)
    glyphs, _, _, _ = shape_glyphs(CAIRO, AR_WORD, 36, {"wght": 600})
    order = sorted(range(len(glyphs)), key=lambda i: (glyphs[i]["cluster"],
                   glyphs[i]["name"] in MARKS))
    rank = {idx: r for r, idx in enumerate(order)}
    ab = L["ab"]
    aw = ab[2] - ab[0]
    parts.append(f'<g transform="translate({CX + (CW-aw)/2 - ab[0]:.2f} {L["ar_y"] - ab[1]:.2f})">')
    for i, g in enumerate(glyphs):
        is_mark = g["name"] in MARKS
        c = GREEN if is_mark else PRIMARY
        d = T_AR + rank[i] * STAG + (0.1 if is_mark else 0)
        parts.append(f'<g class="glyph" style="animation-delay:{d:.2f}s">'
                     f'<path d="{g["d"]}" fill="{c}"/></g>')
    parts.append('</g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "morabh", 30, {"wght": 800})
    eb = L["eb"]
    ew = eb[2] - eb[0]
    parts.append(f'<g transform="translate({CX + (CW-ew)/2 - eb[0]:.2f} {L["en_y"] - eb[1]:.2f})">')
    for i, g in enumerate(eg):
        parts.append(f'<g class="glyph" style="animation-delay:{T_EN + i*STAG:.2f}s">'
                     f'<path d="{g["d"]}" fill="{LIGHT}"/></g>')
    parts.append('</g>')
    parts.append('<g class="loader">')
    for i in range(3):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.86:.0f}" r="4" '
                     f'fill="{P400}" style="animation-delay:{i*0.2:.1f}s"/>')
    parts.append('</g>')
    write_svg("splash/splash-animated.svg", VW, VH, "".join(parts))
    with open(os.path.join(OUT, "splash/splash-animated-preview.html"), "w") as f:
        f.write(f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morabh — square meem splash</title>
<style>body{{margin:0;background:#c9d8f8;display:flex;align-items:center;justify-content:center;min-height:100vh}}
.phone{{width:min(390px,92vw);aspect-ratio:390/844;border-radius:40px;overflow:hidden;
box-shadow:0 30px 80px rgba(18,47,120,.35);border:10px solid #122F78;background:#fff}}
.phone img{{width:100%;height:100%;display:block}}</style></head>
<body><div class="phone"><img src="splash-animated.svg" alt="Morabh splash"></div>
<script>document.querySelector("img").onclick=e=>{{const s=e.target.src;e.target.src="";e.target.src=s}}</script>
</body></html>''')


# ----------------------------------------------------------- GIF preview
def _cl(v):
    return max(0.0, min(1.0, v))


def _eo(p):
    return 1 - (1 - p) ** 3


def _eb(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def frame_svg(t):
    L = splash_layout()
    s = L["s"]
    parts = [f'<rect width="{VW}" height="{VH}" fill="{TILE}"/>']
    pc = _eo(_cl((t - T_CARD) / 0.55))
    if pc > 0:
        dy = 14 * (1 - pc)
        parts.append(f'<g transform="translate(0 {dy:.1f})" opacity="{pc:.2f}">'
                     f'<rect x="{CX}" y="{CY}" width="{CW}" height="{CH}" rx="{CR}" fill="{CARD}"/></g>')
    lp = []
    pr = _eo(_cl((t - T_RING) / 0.6))
    pieces = letter_pieces()
    if pr > 0:
        lp.append(f'<g transform="translate(0 {18*(1-pr):.1f})" opacity="{pr:.2f}">{pieces["ring"]}</g>')
    steps_geo = [(196, 224, 108), (232, 198, 72), (268, 172, 36)]
    for i, (x, y, w) in enumerate(steps_geo):
        p = _eo(_cl((t - (T_STEPS + i * 0.13)) / 0.45))
        if p > 0:
            lp.append(f'<rect x="{x + 26*(1-p):.1f}" y="{y}" width="{w}" height="26" '
                      f'fill="{LIGHT}" opacity="{p:.2f}"/>')
    pt = _eo(_cl((t - T_TAIL) / 0.5))
    if pt > 0:
        lp.append(f'<g transform="translate(0 {296*(1-pt):.3f}) scale(1 {pt:.3f}) '
                  f'translate(0 {-296*(1-pt) if False else 0:.3f})" opacity="{pt:.2f}">'
                  f'{pieces["tail"]}</g>' if False else
                  f'<g opacity="{pt:.2f}">{pieces["tail"]}</g>')
    pd = _cl((t - T_DAMMA) / 0.55)
    if pd > 0:
        f = _eb(pd)
        lp.append(f'<g transform="translate(0 {-30*(1-f):.1f})" opacity="{min(1,pd*3):.2f}">'
                  f'{pieces["damma"]}</g>')
    parts.append(f'<g transform="translate({L["lx"] - L_X0*s:.2f} {L["ly"] - L_Y0*s:.2f}) '
                 f'scale({s:.5f})">{"".join(lp)}</g>')
    # words
    glyphs, _, _, _ = shape_glyphs(CAIRO, AR_WORD, 36, {"wght": 600})
    order = sorted(range(len(glyphs)), key=lambda i: (glyphs[i]["cluster"],
                   glyphs[i]["name"] in MARKS))
    rank = {idx: r for r, idx in enumerate(order)}
    ab = L["ab"]
    aw = ab[2] - ab[0]
    parts.append(f'<g transform="translate({CX + (CW-aw)/2 - ab[0]:.2f} {L["ar_y"] - ab[1]:.2f})">')
    for i, g in enumerate(glyphs):
        is_mark = g["name"] in MARKS
        d = T_AR + rank[i] * STAG + (0.1 if is_mark else 0)
        p = _eo(_cl((t - d) / 0.5))
        if p > 0:
            c = GREEN if is_mark else PRIMARY
            parts.append(f'<path d="{g["d"]}" fill="{c}" opacity="{p:.2f}" '
                         f'transform="translate(0 {12*(1-p):.1f})"/>')
    parts.append('</g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "morabh", 30, {"wght": 800})
    eb2 = L["eb"]
    ew = eb2[2] - eb2[0]
    parts.append(f'<g transform="translate({CX + (CW-ew)/2 - eb2[0]:.2f} {L["en_y"] - eb2[1]:.2f})">')
    for i, g in enumerate(eg):
        p = _eo(_cl((t - (T_EN + i * STAG)) / 0.5))
        if p > 0:
            parts.append(f'<path d="{g["d"]}" fill="{LIGHT}" opacity="{p:.2f}" '
                         f'transform="translate(0 {12*(1-p):.1f})"/>')
    parts.append('</g>')
    pl = _cl((t - T_LOADER) / 0.5)
    if pl > 0:
        for i in range(3):
            pulse = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t - T_LOADER) / 1.2) - i * 1.1))
            parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.86:.0f}" r="4" '
                         f'fill="{P400}" opacity="{pl*pulse:.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
            f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')


def build_gif(fps=15, dur=3.8):
    tmp = "/tmp/msq-frames"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    for k in range(int(dur * fps)):
        p = os.path.join(tmp, f"f{k:03d}.svg")
        with open(p, "w") as f:
            f.write(frame_svg(k / fps))
        run(["rsvg-convert", "-w", "300", p, "-o", os.path.join(tmp, f"f{k:03d}.png")])
    run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
         os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame",
         os.path.join(OUT, "splash/splash-animated-preview.gif")])


if __name__ == "__main__":
    build_logo()
    build_icons()
    build_favicons()
    build_splash_static()
    build_splash_animated()
    build_gif()
    print("meem-square kit ->", OUT)
