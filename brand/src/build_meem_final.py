#!/usr/bin/env python3
"""Morabh — FINAL Meem kit: mobile + web, light & dark themes, no gradients.

- Typography: Cairo for BOTH scripts (its Latin is designed to pair with the Arabic).
- Light theme: symbol/text #6C8DDF on white. Dark theme: white on #0D1B26.
- Splash A: renders the symbol only.
- Splash B: renders the symbol big -> shrinks & docks inline with مُرابِح ->
  Arabic hides -> English "Morabh" shows inline (symbol slides to lead the line).

Outputs to ../../brand-meem-final/.
"""
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from textpath import shape_glyphs, shape_bounds  # noqa: E402
import build_round_meem as rm  # noqa: E402
from build_round_meem import (S_BBOX, S_W, S_H, RING_C, RING_R, SW,  # noqa: E402
                              TAIL_A, TAIL_B, DROP_C, DROP_R, RING_LEN, TAIL_LEN)

OUT = os.path.abspath(os.path.join(HERE, "..", "..", "brand-meem-final"))
FONTS = os.path.join(HERE, "..", "fonts")
CAIRO = os.path.join(FONTS, "Cairo.ttf")

LIGHT = "#6C8DDF"
DARK_BG = "#0D1B26"
WHITE = "#FFFFFF"
AR_WORD = "\u0645\u064f\u0631\u0627\u0628\u0650\u062d"  # مُرابِح
MARKS = {"uni064F", "uni0650"}

RING_TOP, RING_BOT, SYM_BOT = 96.0, 284.0, 378.0
RING_OUTER = RING_BOT - RING_TOP

ICON_SIZES = [16, 20, 24, 29, 32, 40, 48, 58, 60, 64, 76, 80, 87, 96, 114,
              120, 128, 144, 152, 167, 180, 192, 256, 384, 512, 1024]
FAV_SIZES = [16, 24, 32, 48, 64, 96, 128, 152, 180, 192, 256, 384, 512]
NAV_SIZES = [16, 20, 24, 28, 32, 40, 48, 64, 96, 128]

THEMES = {
    "light": dict(bg=WHITE, fg=LIGHT),
    "dark": dict(bg=DARK_BG, fg=WHITE),
}


def run(cmd):
    subprocess.run(cmd, check=True)


def write_svg(rel, w, h, body):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
                f'width="{w:.0f}" height="{h:.0f}">{body}</svg>')


def render(rel, png_rel, w=None, h=None):
    svg = os.path.join(OUT, rel)
    png = os.path.join(OUT, png_rel)
    os.makedirs(os.path.dirname(png), exist_ok=True)
    cmd = ["rsvg-convert", svg, "-o", png]
    if w:
        cmd += ["-w", str(int(w))]
    if h:
        cmd += ["-h", str(int(h))]
    run(cmd)


def sym_placed(x, y, h, color):
    s = h / S_H
    return (f'<g transform="translate({x - S_BBOX[0]*s:.2f} {y - S_BBOX[1]*s:.2f}) '
            f'scale({s:.5f})">{rm.symbol_frag(color, color)}</g>')


def word_frag(text, size, color, wght):
    glyphs, adv, _, _ = shape_glyphs(CAIRO, text, size, {"wght": wght})
    b = shape_bounds(CAIRO, text, size, {"wght": wght})
    return "".join(f'<path d="{g["d"]}" fill="{color}"/>' for g in glyphs), b


# Cairo Latin cap height (from "M")
_cap = None


def cap_height(size):
    global _cap
    if _cap is None:
        b = shape_bounds(CAIRO, "M", 100, {"wght": 700})
        _cap = -b[1] / 100.0
    return _cap * size


EN_SIZE = 46
AR_SIZE = 48
EN_WGHT = 700
AR_WGHT = 600


def inline_scale():
    return cap_height(EN_SIZE) * 1.06 / RING_OUTER


def geo():
    """Shared geometry for lockups and splash choreography."""
    s = inline_scale()
    sw = S_W * s
    gap = cap_height(EN_SIZE) * 0.24
    _, eb = word_frag("Morabh", EN_SIZE, "#000", EN_WGHT)
    _, ab = word_frag(AR_WORD, AR_SIZE, "#000", AR_WGHT)
    ew = eb[2] - eb[0]
    aw = ab[2] - ab[0]
    # EN pair: [symbol][gap][word]; AR pair: [word][gap][symbol]
    en_W = sw + gap + ew
    ar_W = aw + gap + sw
    return dict(s=s, sw=sw, gap=gap, eb=eb, ab=ab, ew=ew, aw=aw, en_W=en_W, ar_W=ar_W)


def sym_inline_at(x_left, baseline, color, scale):
    tx = x_left - S_BBOX[0] * scale
    ty = baseline - RING_BOT * scale
    return (f'<g transform="translate({tx:.2f} {ty:.2f}) scale({scale:.5f})">'
            f'{rm.symbol_frag(color, color)}</g>')


# ------------------------------------------------------------ logo & lockups
def build_logos():
    pad = 36
    for theme, T in THEMES.items():
        # bare symbol (transparent)
        write_svg(f"logo/symbol-{theme}.svg", S_W + 2 * pad, S_H + 2 * pad,
                  sym_placed(pad, pad, S_H, T["fg"]))
        render(f"logo/symbol-{theme}.svg", f"logo/symbol-{theme}.png", w=800)
        G = geo()
        pad2 = 40
        # EN inline lockup
        top = min((RING_TOP - RING_BOT) * G["s"], G["eb"][1])
        bot = max((SYM_BOT - RING_BOT) * G["s"], G["eb"][3])
        H = bot - top + 2 * pad2
        W = G["en_W"] + 2 * pad2
        enp, eb = word_frag("Morabh", EN_SIZE, T["fg"], EN_WGHT)
        body = (f'<rect width="{W:.0f}" height="{H:.0f}" rx="24" fill="{T["bg"]}"/>'
                + sym_inline_at(pad2, pad2 - top, T["fg"], G["s"])
                + f'<g transform="translate({pad2 + G["sw"] + G["gap"] - eb[0]:.2f} '
                  f'{pad2 - top:.2f})">{enp}</g>')
        write_svg(f"logo/lockup-inline-en-{theme}.svg", W, H, body)
        render(f"logo/lockup-inline-en-{theme}.svg",
               f"logo/lockup-inline-en-{theme}.png", w=1400)
        # AR inline lockup (symbol right)
        top = min((RING_TOP - RING_BOT) * G["s"], G["ab"][1])
        bot = max((SYM_BOT - RING_BOT) * G["s"], G["ab"][3])
        H = bot - top + 2 * pad2
        W = G["ar_W"] + 2 * pad2
        arp, ab = word_frag(AR_WORD, AR_SIZE, T["fg"], AR_WGHT)
        body = (f'<rect width="{W:.0f}" height="{H:.0f}" rx="24" fill="{T["bg"]}"/>'
                + f'<g transform="translate({pad2 - ab[0]:.2f} {pad2 - top:.2f})">{arp}</g>'
                + sym_inline_at(pad2 + G["aw"] + G["gap"], pad2 - top, T["fg"], G["s"]))
        write_svg(f"logo/lockup-inline-ar-{theme}.svg", W, H, body)
        render(f"logo/lockup-inline-ar-{theme}.svg",
               f"logo/lockup-inline-ar-{theme}.png", w=1400)


# ------------------------------------------------------------ icons & favicons
def build_icons():
    for theme, T in THEMES.items():
        frag = (f'<rect width="1024" height="1024" fill="{T["bg"]}"/>'
                + sym_placed((1024 - S_W * (630 / S_H)) / 2, (1024 - 630) / 2, 630, T["fg"]))
        write_svg(f"app-icons/{theme}/icon-master-1024.svg", 1024, 1024, frag)
        for s in ICON_SIZES:
            render(f"app-icons/{theme}/icon-master-1024.svg",
                   f"app-icons/{theme}/icon-{s}x{s}.png", w=s, h=s)
        # android adaptive
        write_svg(f"app-icons/{theme}/adaptive-foreground.svg", 1024, 1024,
                  sym_placed((1024 - S_W * (560 / S_H)) / 2, (1024 - 560) / 2, 560, T["fg"]))
        render(f"app-icons/{theme}/adaptive-foreground.svg",
               f"app-icons/{theme}/adaptive-foreground-432.png", w=432, h=432)
        write_svg(f"app-icons/{theme}/adaptive-background.svg", 1024, 1024,
                  f'<rect width="1024" height="1024" fill="{T["bg"]}"/>')
        render(f"app-icons/{theme}/adaptive-background.svg",
               f"app-icons/{theme}/adaptive-background-432.png", w=432, h=432)


def build_favicons():
    # adaptive SVG favicon: follows the browser's color scheme
    s = 340 / S_H
    tx = (512 - S_W * s) / 2 - S_BBOX[0] * s
    ty = 86 - S_BBOX[1] * s
    adaptive = (f'<style>.m{{stroke:{LIGHT}}} .d{{fill:{LIGHT}}}'
                f'@media (prefers-color-scheme: dark){{.m{{stroke:{WHITE}}} .d{{fill:{WHITE}}}}}'
                f'</style>'
                f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">'
                f'<g class="m" fill="none" stroke-width="{SW}" stroke-linecap="round">'
                f'<circle cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
                f'<path d="M {TAIL_A[0]} {TAIL_A[1]} L {TAIL_B[0]} {TAIL_B[1]}"/></g>'
                f'<circle class="d" cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R}"/></g>')
    write_svg("favicon/favicon.svg", 512, 512, adaptive)
    for theme, T in THEMES.items():
        frag = (f'<rect width="512" height="512" fill="{T["bg"]}"/>'
                + sym_placed((512 - S_W * (340 / S_H)) / 2, 86, 340, T["fg"]))
        write_svg(f"favicon/{theme}/favicon-master.svg", 512, 512, frag)
        for s2 in FAV_SIZES:
            render(f"favicon/{theme}/favicon-master.svg",
                   f"favicon/{theme}/favicon-{s2}x{s2}.png", w=s2, h=s2)
        run(["convert",
             os.path.join(OUT, f"favicon/{theme}/favicon-16x16.png"),
             os.path.join(OUT, f"favicon/{theme}/favicon-32x32.png"),
             os.path.join(OUT, f"favicon/{theme}/favicon-48x48.png"),
             os.path.join(OUT, f"favicon/{theme}/favicon.ico")])
        shutil.copy(os.path.join(OUT, f"favicon/{theme}/favicon-180x180.png"),
                    os.path.join(OUT, f"favicon/{theme}/apple-touch-icon.png"))
        frag = (f'<rect width="512" height="512" fill="{T["bg"]}"/>'
                + sym_placed((512 - S_W * (260 / S_H)) / 2, 126, 260, T["fg"]))
        write_svg(f"favicon/{theme}/maskable.svg", 512, 512, frag)
        render(f"favicon/{theme}/maskable.svg",
               f"favicon/{theme}/maskable-512x512.png", w=512, h=512)
    with open(os.path.join(OUT, "favicon/snippet.html"), "w") as f:
        f.write('''<!-- Morabh favicon set (theme-adaptive SVG first) -->
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" href="/light/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/light/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/light/apple-touch-icon.png">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#6C8DDF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0D1B26">
''')


def build_navbar_web():
    pad = 30
    for theme, T in THEMES.items():
        write_svg(f"navbar/navbar-{theme}.svg", S_W + 2 * pad, S_H + 2 * pad,
                  sym_placed(pad, pad, S_H, T["fg"]))
        for s in NAV_SIZES:
            render(f"navbar/navbar-{theme}.svg", f"navbar/navbar-{theme}-{s}.png", h=s)
        for s in (24, 32, 40, 48, 64, 96, 128, 256):
            render(f"logo/lockup-inline-en-{theme}.svg",
                   f"web/header-lockup-en-{theme}-h{s}.png", h=s)
            render(f"logo/lockup-inline-ar-{theme}.svg",
                   f"web/header-lockup-ar-{theme}-h{s}.png", h=s)


# ------------------------------------------------------------ splash
VW, VH = 390, 844
# big symbol phase
BIG_H = 150
BIG_Y = VH * 0.36
# choreography times
T_RING, D_RING = 0.20, 0.70
T_TAIL, D_TAIL = 0.80, 0.35
T_DROP, D_DROP = 1.15, 0.50
T_DOCK, D_DOCK = 1.95, 0.65   # shrink + move inline with AR
T_ARIN = 2.30                  # مُرابِح fades in
T_SWAP, D_SWAP = 3.45, 0.45   # AR out, symbol slides, EN in
T_LOADER = 4.15
BASELINE = VH * 0.47


def splash_transforms():
    """Big placement B, AR dock D_a, EN dock D_e (translate+scale pairs)."""
    G = geo()
    sb = BIG_H / S_H
    bx = (VW - S_W * sb) / 2
    B = (bx - S_BBOX[0] * sb, BIG_Y - S_BBOX[1] * sb, sb)
    si = G["s"]
    ar_x0 = (VW - G["ar_W"]) / 2
    en_x0 = (VW - G["en_W"]) / 2
    # AR: symbol after word; EN: symbol first
    Da = (ar_x0 + G["aw"] + G["gap"] - S_BBOX[0] * si, BASELINE - RING_BOT * si, si)
    De = (en_x0 - S_BBOX[0] * si, BASELINE - RING_BOT * si, si)
    return G, B, Da, De, ar_x0, en_x0


def rel_transform(frm, to):
    """CSS transform E with E∘frm = to for translate+scale pairs."""
    k = to[2] / frm[2]
    return (to[0] - k * frm[0], to[1] - k * frm[1], k)


def splash_animated(theme, full=True):
    T = THEMES[theme]
    G, B, Da, De, ar_x0, en_x0 = splash_transforms()
    e1 = rel_transform(B, Da)
    e2 = rel_transform(B, De)
    css = f'''
    .ring {{ stroke-dasharray:{RING_LEN:.1f}; stroke-dashoffset:{RING_LEN:.1f};
             animation: dr {D_RING}s cubic-bezier(.55,0,.35,1) {T_RING}s both; }}
    .tail {{ stroke-dasharray:{TAIL_LEN:.1f}; stroke-dashoffset:{TAIL_LEN:.1f};
             animation: dt {D_TAIL}s ease-out {T_TAIL}s both; }}
    .drop {{ animation: fall {D_DROP}s cubic-bezier(.34,1.56,.64,1) {T_DROP}s both;
             transform-box: fill-box; transform-origin: center; }}
    @keyframes dr {{ to {{ stroke-dashoffset:0; }} }}
    @keyframes dt {{ to {{ stroke-dashoffset:0; }} }}
    @keyframes fall {{ from {{ opacity:0; transform: translateY(-30px) scale(.5); }}
                       to {{ opacity:1; transform:none; }} }}
    .loader {{ opacity:0; animation: fadein .5s ease-out {T_LOADER if full else 2.0}s forwards; }}
    .loader circle {{ animation: pulse 1.2s ease-in-out infinite; }}
    @keyframes fadein {{ to {{ opacity:1; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:.3; }} 50% {{ opacity:1; }} }}'''
    if full:
        css += f'''
    .move {{ animation: mv {D_DOCK}s cubic-bezier(.45,0,.2,1) {T_DOCK}s both,
                        mv2 {D_SWAP}s cubic-bezier(.45,0,.2,1) {T_SWAP}s forwards; }}
    @keyframes mv  {{ from {{ transform: none; }}
                      to {{ transform: translate({e1[0]:.2f}px, {e1[1]:.2f}px) scale({e1[2]:.5f}); }} }}
    @keyframes mv2 {{ from {{ transform: translate({e1[0]:.2f}px, {e1[1]:.2f}px) scale({e1[2]:.5f}); }}
                      to {{ transform: translate({e2[0]:.2f}px, {e2[1]:.2f}px) scale({e2[2]:.5f}); }} }}
    .arw {{ opacity:0; animation: arin .45s cubic-bezier(.22,1,.36,1) {T_ARIN}s forwards,
                        arout .35s ease-in {T_SWAP}s forwards; }}
    @keyframes arin  {{ from {{ opacity:0; transform: translateY(8px); }}
                        to {{ opacity:1; transform:none; }} }}
    @keyframes arout {{ from {{ opacity:1; }} to {{ opacity:0; }} }}
    .enw {{ opacity:0; animation: enin .5s cubic-bezier(.22,1,.36,1) {T_SWAP + 0.25}s forwards; }}
    @keyframes enin {{ from {{ opacity:0; transform: translateX(12px); }}
                       to {{ opacity:1; transform:none; }} }}'''
    css += f'''
    @media (prefers-reduced-motion: reduce) {{
      .ring,.tail {{ animation:none; stroke-dashoffset:0; }}
      .drop,.loader,.loader circle {{ animation:none; opacity:1; }}
      {".move { animation: none; transform: translate(%.2fpx, %.2fpx) scale(%.5f); } .arw { animation: none; opacity: 0; } .enw { animation: none; opacity: 1; }" % e2 if full else ""}
    }}'''
    parts = [f'<style>{css}</style>',
             f'<rect width="{VW}" height="{VH}" fill="{T["bg"]}"/>']
    move_open = '<g class="move">' if full else '<g>'
    parts.append(move_open
                 + f'<g transform="translate({B[0]:.2f} {B[1]:.2f}) scale({B[2]:.5f})">'
                 f'<g fill="none" stroke="{T["fg"]}" stroke-width="{SW}" stroke-linecap="round">'
                 f'<circle class="ring" cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
                 f'<path class="tail" d="M {TAIL_A[0]} {TAIL_A[1]} L {TAIL_B[0]} {TAIL_B[1]}"/>'
                 f'</g>'
                 f'<circle class="drop" cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R}" '
                 f'fill="{T["fg"]}"/></g></g>')
    if full:
        arp, ab = word_frag(AR_WORD, AR_SIZE, T["fg"], AR_WGHT)
        parts.append(f'<g transform="translate({(VW - G["ar_W"])/2 - ab[0]:.2f} '
                     f'{BASELINE:.2f})"><g class="arw">{arp}</g></g>')
        enp, eb = word_frag("Morabh", EN_SIZE, T["fg"], EN_WGHT)
        parts.append(f'<g transform="translate({(VW - G["en_W"])/2 + G["sw"] + G["gap"] - eb[0]:.2f} '
                     f'{BASELINE:.2f})"><g class="enw">{enp}</g></g>')
    parts.append('<g class="loader">')
    for i in range(3):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{T["fg"]}" style="animation-delay:{i*0.2:.1f}s" opacity="0.85"/>')
    parts.append('</g>')
    return "".join(parts)


def splash_static(theme, full=True):
    T = THEMES[theme]
    G, B, Da, De, ar_x0, en_x0 = splash_transforms()
    parts = [f'<rect width="{VW}" height="{VH}" fill="{T["bg"]}"/>']
    if full:
        parts.append(sym_inline_at(en_x0, BASELINE, T["fg"], G["s"]))
        enp, eb = word_frag("Morabh", EN_SIZE, T["fg"], EN_WGHT)
        parts.append(f'<g transform="translate({en_x0 + G["sw"] + G["gap"] - eb[0]:.2f} '
                     f'{BASELINE:.2f})">{enp}</g>')
    else:
        parts.append(f'<g transform="translate({B[0]:.2f} {B[1]:.2f}) scale({B[2]:.5f})">'
                     f'{rm.symbol_frag(T["fg"], T["fg"])}</g>')
    for i, op in enumerate((0.35, 0.6, 1.0)):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{T["fg"]}" opacity="{op*0.85:.2f}"/>')
    return "".join(parts)


def _cl(v):
    return max(0.0, min(1.0, v))


def _eo(p):
    return 1 - (1 - p) ** 3


def _eio(p):
    return 3 * p * p - 2 * p * p * p


def _ebk(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def frame_svg(t, theme, full=True):
    T = THEMES[theme]
    G, B, Da, De, ar_x0, en_x0 = splash_transforms()
    parts = [f'<rect width="{VW}" height="{VH}" fill="{T["bg"]}"/>']
    # current symbol transform
    if not full or t < T_DOCK:
        cur = B
    elif t < T_DOCK + D_DOCK:
        p = _eio(_cl((t - T_DOCK) / D_DOCK))
        cur = tuple(B[i] + (Da[i] - B[i]) * p for i in range(3))
    elif t < T_SWAP:
        cur = Da
    elif t < T_SWAP + D_SWAP:
        p = _eio(_cl((t - T_SWAP) / D_SWAP))
        cur = tuple(Da[i] + (De[i] - Da[i]) * p for i in range(3))
    else:
        cur = De
    inner = [f'<g fill="none" stroke="{T["fg"]}" stroke-width="{SW}" stroke-linecap="round">']
    pr = _eo(_cl((t - T_RING) / D_RING))
    if pr > 0.001:
        inner.append(f'<circle cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}" '
                     f'stroke-dasharray="{RING_LEN:.1f}" stroke-dashoffset="{RING_LEN*(1-pr):.1f}"/>')
    pt = _eo(_cl((t - T_TAIL) / D_TAIL))
    if pt > 0.001:
        inner.append(f'<path d="M {TAIL_A[0]} {TAIL_A[1]} L {TAIL_B[0]} {TAIL_B[1]}" '
                     f'stroke-dasharray="{TAIL_LEN:.1f}" stroke-dashoffset="{TAIL_LEN*(1-pt):.1f}"/>')
    inner.append('</g>')
    pd = _cl((t - T_DROP) / D_DROP)
    if pd > 0:
        f = _ebk(pd)
        dy = -30 * (1 - f) / cur[2]
        sc = 0.5 + 0.5 * f
        inner.append(f'<circle cx="{DROP_C[0]}" cy="{DROP_C[1] + dy:.1f}" r="{DROP_R*sc:.1f}" '
                     f'fill="{T["fg"]}" opacity="{min(1, pd*3):.2f}"/>')
    parts.append(f'<g transform="translate({cur[0]:.2f} {cur[1]:.2f}) scale({cur[2]:.5f})">'
                 f'{"".join(inner)}</g>')
    if full:
        # Arabic word: in after T_ARIN, out at T_SWAP
        pa_in = _eo(_cl((t - T_ARIN) / 0.45))
        pa_out = _cl((t - T_SWAP) / 0.35)
        ar_op = pa_in * (1 - pa_out)
        if ar_op > 0.01:
            arp, ab = word_frag(AR_WORD, AR_SIZE, T["fg"], AR_WGHT)
            parts.append(f'<g opacity="{ar_op:.2f}" transform="translate('
                         f'{(VW - G["ar_W"])/2 - ab[0]:.2f} '
                         f'{BASELINE + 8*(1-pa_in):.2f})">{arp}</g>')
        pe = _eo(_cl((t - (T_SWAP + 0.25)) / 0.5))
        if pe > 0.01:
            enp, eb = word_frag("Morabh", EN_SIZE, T["fg"], EN_WGHT)
            parts.append(f'<g opacity="{pe:.2f}" transform="translate('
                         f'{(VW - G["en_W"])/2 + G["sw"] + G["gap"] - eb[0] + 12*(1-pe):.2f} '
                         f'{BASELINE:.2f})">{enp}</g>')
    t_loader = T_LOADER if full else 2.0
    pl = _cl((t - t_loader) / 0.5)
    if pl > 0:
        for i in range(3):
            pulse = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t - t_loader) / 1.2) - i * 1.1))
            parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                         f'fill="{T["fg"]}" opacity="{pl*pulse*0.85:.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
            f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')


def build_gif(theme, full, out_rel, fps=15):
    dur = 5.2 if full else 3.0
    tmp = f"/tmp/mf-{theme}-{int(full)}"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    for k in range(int(dur * fps)):
        p = os.path.join(tmp, f"f{k:03d}.svg")
        with open(p, "w") as f:
            f.write(frame_svg(k / fps, theme, full))
        run(["rsvg-convert", "-w", "300", p, "-o", os.path.join(tmp, f"f{k:03d}.png")])
    run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
         os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame",
         os.path.join(OUT, out_rel)])


def build_splashes():
    for theme in THEMES:
        for full, tag in ((False, "symbol-only"), (True, "full")):
            base = f"splash/{theme}/splash-{tag}"
            write_svg(base + "-animated.svg", VW, VH, splash_animated(theme, full))
            write_svg(base + "-static.svg", VW, VH, splash_static(theme, full))
            render(base + "-static.svg", base + "-1284x2778.png", w=1284, h=2778)
            render(base + "-static.svg", base + "-1080x1920.png", w=1080, h=1920)
            build_gif(theme, full, base + "-preview.gif")
    with open(os.path.join(OUT, "splash/preview.html"), "w") as f:
        f.write('''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morabh — splash previews</title>
<style>body{margin:0;background:#E8EBF2;display:flex;gap:24px;align-items:center;
justify-content:center;min-height:100vh;flex-wrap:wrap;padding:24px}
.phone{width:min(300px,80vw);aspect-ratio:390/844;border-radius:36px;overflow:hidden;
box-shadow:0 24px 60px rgba(13,27,38,.35);border:9px solid #0D1B26;background:#fff}
.phone img{width:100%;height:100%;display:block}
p{width:100%;text-align:center;font:600 14px system-ui;color:#4B5563;margin:0}</style></head>
<body>
<p>Click any phone to replay</p>
<div class="phone"><img src="light/splash-symbol-only-animated.svg" alt="light symbol"></div>
<div class="phone"><img src="light/splash-full-animated.svg" alt="light full"></div>
<div class="phone"><img src="dark/splash-symbol-only-animated.svg" alt="dark symbol"></div>
<div class="phone"><img src="dark/splash-full-animated.svg" alt="dark full"></div>
<script>document.querySelectorAll("img").forEach(m=>m.onclick=e=>{const s=e.target.src;e.target.src="";e.target.src=s})</script>
</body></html>''')


if __name__ == "__main__":
    build_logos()
    build_icons()
    build_favicons()
    build_navbar_web()
    build_splashes()
    print("meem-final kit ->", OUT)
