#!/usr/bin/env python3
"""Morabh — Round Meem identity kit (reconstructed from user's reference).

The mark: a rounded م — ring head + hanging tail ending in a drop.
The drop is the accent: white when merged, teal as the "gain" on dark.

Splash matches the reference: light = blue->teal gradient, dark = deep navy
with a soft teal glow. Wordmark: "Morabh" (capitalized) over مرابح.

Outputs to ../../brand-round-meem/.
"""
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from textpath import shape_glyphs, shape_bounds  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, "..", "..", "brand-round-meem"))
FONTS = os.path.join(HERE, "..", "fonts")
CAIRO = os.path.join(FONTS, "Cairo.ttf")
MANROPE = os.path.join(FONTS, "Manrope.ttf")

GRAD_TOP = "#4A90D8"
GRAD_BOT = "#2AB3A6"
DARK_BG = "#0D1B26"
TEAL = "#2BB39F"
WHITE = "#FFFFFF"
NAVY = "#12405E"

AR_WORD = "\u0645\u0631\u0627\u0628\u062d"  # مرابح (plain, as in reference)


def run(cmd):
    subprocess.run(cmd, check=True)


def write_svg(rel, w, h, body):
    path = os.path.join(OUT, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" '
                f'width="{w}" height="{h}">{body}</svg>')


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


# ----------------------------------------------------------- the symbol
# 512 space. Ring head + tail + drop. Ink bbox: (158, 96, 394, 378)
RING_C = (276, 190)
RING_R = 70
SW = 48
TAIL_A = (232, 244)
TAIL_B = (222, 330)
DROP_C = (220, 348)
DROP_R = 30
S_BBOX = (158.0, 96.0, 394.0, 378.0)
S_W = S_BBOX[2] - S_BBOX[0]
S_H = S_BBOX[3] - S_BBOX[1]


def symbol_frag(mark=WHITE, drop=None):
    drop = drop or mark
    return (f'<g fill="none" stroke="{mark}" stroke-width="{SW}" stroke-linecap="round">'
            f'<circle cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
            f'<path d="M {TAIL_A[0]} {TAIL_A[1]} L {TAIL_B[0]} {TAIL_B[1]}"/>'
            f'</g>'
            f'<circle cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R}" fill="{drop}"/>')


def symbol_placed(x, y, h, mark=WHITE, drop=None):
    s = h / S_H
    return (f'<g transform="translate({x - S_BBOX[0]*s:.2f} {y - S_BBOX[1]*s:.2f}) '
            f'scale({s:.5f})">{symbol_frag(mark, drop)}</g>')


GRAD_DEF = (f'<linearGradient id="bg" x1="0" y1="0" x2="0.4" y2="1">'
            f'<stop offset="0" stop-color="{GRAD_TOP}"/>'
            f'<stop offset="1" stop-color="{GRAD_BOT}"/></linearGradient>')


# ----------------------------------------------------------- wordmarks
def word(font, text, size, color, wght):
    glyphs, adv, _, _ = shape_glyphs(font, text, size, {"wght": wght})
    b = shape_bounds(font, text, size, {"wght": wght})
    return "".join(f'<path d="{g["d"]}" fill="{color}"/>' for g in glyphs), b


def build_logo():
    pad = 36
    # white on gradient tile
    write_svg("logo/symbol-gradient-tile.svg", 512, 512,
              f'<defs>{GRAD_DEF}</defs><rect width="512" height="512" rx="96" fill="url(#bg)"/>'
              + symbol_placed((512 - S_W*0.9)/2, (512 - S_H*0.9)/2, S_H*0.9))
    render("logo/symbol-gradient-tile.svg", "logo/symbol-gradient-tile.png", w=800)
    # dark tile with teal drop
    write_svg("logo/symbol-dark-tile.svg", 512, 512,
              f'<rect width="512" height="512" rx="96" fill="{DARK_BG}"/>'
              f'<circle cx="256" cy="256" r="220" fill="{TEAL}" opacity="0.08"/>'
              + symbol_placed((512 - S_W*0.9)/2, (512 - S_H*0.9)/2, S_H*0.9, WHITE, TEAL))
    render("logo/symbol-dark-tile.svg", "logo/symbol-dark-tile.png", w=800)
    # teal-on-white and mono black (transparent bg)
    write_svg("logo/symbol-color.svg", S_W + 2*pad, S_H + 2*pad,
              symbol_placed(pad, pad, S_H, GRAD_BOT, TEAL))
    render("logo/symbol-color.svg", "logo/symbol-color.png", w=800)
    write_svg("logo/symbol-black.svg", S_W + 2*pad, S_H + 2*pad,
              symbol_placed(pad, pad, S_H, "#000000"))
    render("logo/symbol-black.svg", "logo/symbol-black.png", w=800)
    # stacked lockup on gradient (like the reference)
    W, H = 900, 900
    enp, eb = word(MANROPE, "Morabh", 96, WHITE, 800)
    arp, ab = word(CAIRO, AR_WORD, 64, WHITE, 600)
    ew, aw = eb[2] - eb[0], ab[2] - ab[0]
    parts = [f'<defs>{GRAD_DEF}</defs><rect width="{W}" height="{H}" rx="0" fill="url(#bg)"/>']
    parts.append(symbol_placed((W - S_W*1.05)/2, 150, S_H*1.05))
    parts.append(f'<g transform="translate({(W-ew)/2 - eb[0]:.1f} {560 - eb[1]:.1f})">{enp}</g>')
    parts.append(f'<g opacity="0.78" transform="translate({(W-aw)/2 - ab[0]:.1f} {680 - ab[1]:.1f})">{arp}</g>')
    write_svg("logo/lockup-stacked-gradient.svg", W, H, "".join(parts))
    render("logo/lockup-stacked-gradient.svg", "logo/lockup-stacked-gradient.png", w=1080)


def build_icons():
    frag = (f'<defs>{GRAD_DEF}</defs><rect width="1024" height="1024" fill="url(#bg)"/>'
            + symbol_placed((1024 - S_W*1.75)/2, (1024 - S_H*1.75)/2, S_H*1.75))
    write_svg("app-icons/icon-square-1024.svg", 1024, 1024, frag)
    render("app-icons/icon-square-1024.svg", "app-icons/ios/AppIcon-1024.png")
    frag = (f'<defs>{GRAD_DEF}</defs><rect width="1024" height="1024" rx="229" fill="url(#bg)"/>'
            + symbol_placed((1024 - S_W*1.75)/2, (1024 - S_H*1.75)/2, S_H*1.75))
    write_svg("app-icons/icon-rounded-1024.svg", 1024, 1024, frag)
    for s in (1024, 512, 192, 180):
        render("app-icons/icon-rounded-1024.svg", f"app-icons/icon-rounded-{s}.png", w=s, h=s)
    frag = (f'<rect width="1024" height="1024" rx="229" fill="{DARK_BG}"/>'
            f'<circle cx="512" cy="512" r="430" fill="{TEAL}" opacity="0.08"/>'
            + symbol_placed((1024 - S_W*1.75)/2, (1024 - S_H*1.75)/2, S_H*1.75, WHITE, TEAL))
    write_svg("app-icons/icon-rounded-dark-1024.svg", 1024, 1024, frag)
    render("app-icons/icon-rounded-dark-1024.svg", "app-icons/icon-rounded-dark-1024.png")
    write_svg("app-icons/android/adaptive-foreground.svg", 1024, 1024,
              symbol_placed((1024 - S_W*1.1)/2, (1024 - S_H*1.1)/2, S_H*1.1))
    render("app-icons/android/adaptive-foreground.svg",
           "app-icons/android/adaptive-foreground-432.png", w=432, h=432)
    write_svg("app-icons/android/adaptive-background.svg", 1024, 1024,
              f'<defs>{GRAD_DEF}</defs><rect width="1024" height="1024" fill="url(#bg)"/>')
    render("app-icons/android/adaptive-background.svg",
           "app-icons/android/adaptive-background-432.png", w=432, h=432)


def build_favicons():
    frag = (f'<defs>{GRAD_DEF}</defs><rect width="512" height="512" rx="112" fill="url(#bg)"/>'
            + symbol_placed((512 - S_W*0.95)/2, (512 - S_H*0.95)/2, S_H*0.95))
    write_svg("favicon/favicon.svg", 512, 512, frag)
    for s in (16, 32, 48, 180, 192, 512):
        render("favicon/favicon.svg", f"favicon/favicon-{s}x{s}.png", w=s, h=s)
    run(["convert", os.path.join(OUT, "favicon/favicon-16x16.png"),
         os.path.join(OUT, "favicon/favicon-32x32.png"),
         os.path.join(OUT, "favicon/favicon-48x48.png"),
         os.path.join(OUT, "favicon/favicon.ico")])
    frag = (f'<defs>{GRAD_DEF}</defs><rect width="512" height="512" fill="url(#bg)"/>'
            + symbol_placed((512 - S_W*0.7)/2, (512 - S_H*0.7)/2, S_H*0.7))
    write_svg("favicon/maskable.svg", 512, 512, frag)
    render("favicon/maskable.svg", "favicon/maskable-512x512.png", w=512, h=512)


# ----------------------------------------------------------- splash
VW, VH = 390, 844
T_RING, D_RING = 0.20, 0.75
T_TAIL, D_TAIL = 0.85, 0.40
T_DROP, D_DROP = 1.25, 0.55
T_EN, T_AR, STAG = 1.60, 2.05, 0.06
T_LOADER = 2.55
RING_LEN = 2 * math.pi * RING_R
TAIL_LEN = math.dist(TAIL_A, TAIL_B)


def splash_layout():
    sym_h = 150
    s = sym_h / S_H
    lx = (VW - S_W * s) / 2
    ly = VH * 0.26
    enp, eb = word(MANROPE, "Morabh", 40, WHITE, 800)
    arp, ab = word(CAIRO, AR_WORD, 27, WHITE, 600)
    en_y = ly + sym_h + 62
    ar_y = en_y + (eb[3] - eb[1]) + 26
    return dict(s=s, sym_h=sym_h, lx=lx, ly=ly, enp=enp, eb=eb,
                arp=arp, ab=ab, en_y=en_y, ar_y=ar_y)


def splash_bg(dark):
    if dark:
        return (f'<rect width="{VW}" height="{VH}" fill="{DARK_BG}"/>'
                f'<circle cx="{VW/2}" cy="{VH*0.36:.0f}" r="{VW*0.55:.0f}" fill="{TEAL}" opacity="0.10"/>')
    return f'<defs>{GRAD_DEF}</defs><rect width="{VW}" height="{VH}" fill="url(#bg)"/>'


def splash_static_frag(dark):
    L = splash_layout()
    drop = TEAL if dark else WHITE
    parts = [splash_bg(dark)]
    parts.append(symbol_placed(L["lx"], L["ly"], L["sym_h"], WHITE, drop))
    ew = L["eb"][2] - L["eb"][0]
    parts.append(f'<g transform="translate({(VW-ew)/2 - L["eb"][0]:.1f} '
                 f'{L["en_y"] - L["eb"][1]:.1f})">{L["enp"]}</g>')
    aw = L["ab"][2] - L["ab"][0]
    parts.append(f'<g opacity="0.75" transform="translate({(VW-aw)/2 - L["ab"][0]:.1f} '
                 f'{L["ar_y"] - L["ab"][1]:.1f})">{L["arp"]}</g>')
    for i, op in enumerate((0.35, 0.6, 1.0)):
        c = TEAL if dark else WHITE
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{c}" opacity="{op*0.8:.2f}"/>')
    return "".join(parts)


def build_splash_static():
    for tag, dark in (("light", False), ("dark", True)):
        write_svg(f"splash/splash-{tag}.svg", VW, VH, splash_static_frag(dark))
        render(f"splash/splash-{tag}.svg", f"splash/splash-{tag}-1284x2778.png", w=1284, h=2778)
        render(f"splash/splash-{tag}.svg", f"splash/splash-{tag}-1080x1920.png", w=1080, h=1920)
        render(f"splash/splash-{tag}.svg", f"splash/splash-{tag}-preview.png", w=780)


def build_splash_animated(dark=False):
    L = splash_layout()
    tag = "dark" if dark else "light"
    drop = TEAL if dark else WHITE
    loader_c = TEAL if dark else WHITE
    css = f'''
    .ring {{ stroke-dasharray:{RING_LEN:.1f}; stroke-dashoffset:{RING_LEN:.1f};
             animation: dr {D_RING}s cubic-bezier(.55,0,.35,1) {T_RING}s both; }}
    .tail {{ stroke-dasharray:{TAIL_LEN:.1f}; stroke-dashoffset:{TAIL_LEN:.1f};
             animation: dt {D_TAIL}s ease-out {T_TAIL}s both; }}
    .drop {{ animation: fall {D_DROP}s cubic-bezier(.34,1.56,.64,1) {T_DROP}s both;
             transform-box: fill-box; transform-origin: center; }}
    .glyph {{ animation: pop .5s cubic-bezier(.22,1,.36,1) both;
              transform-box: fill-box; transform-origin: center bottom; }}
    .ar {{ opacity: 0.75; }}
    .loader {{ opacity:0; animation: fadein .5s ease-out {T_LOADER}s forwards; }}
    .loader circle {{ animation: pulse 1.2s ease-in-out infinite; }}
    @keyframes dr {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes dt {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes fall {{ from {{ opacity:0; transform: translateY(-34px) scale(.5); }}
                       to   {{ opacity:1; transform: none; }} }}
    @keyframes pop  {{ from {{ opacity:0; transform: translateY(12px); }}
                       to   {{ opacity:1; transform: none; }} }}
    @keyframes fadein {{ to {{ opacity:1; }} }}
    @keyframes pulse  {{ 0%,100% {{ opacity:.3; }} 50% {{ opacity:1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .ring,.tail {{ animation:none; stroke-dashoffset:0; }}
      .drop,.glyph,.loader,.loader circle {{ animation:none; opacity:1; }}
    }}'''
    s = L["s"]
    parts = [f'<style>{css}</style>', splash_bg(dark)]
    parts.append(f'<g transform="translate({L["lx"] - S_BBOX[0]*s:.2f} '
                 f'{L["ly"] - S_BBOX[1]*s:.2f}) scale({s:.5f})">'
                 f'<g fill="none" stroke="{WHITE}" stroke-width="{SW}" stroke-linecap="round">'
                 f'<circle class="ring" cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
                 f'<path class="tail" d="M {TAIL_A[0]} {TAIL_A[1]} L {TAIL_B[0]} {TAIL_B[1]}"/>'
                 f'</g>'
                 f'<circle class="drop" cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R}" fill="{drop}"/>'
                 f'</g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "Morabh", 40, {"wght": 800})
    eb = L["eb"]
    ew = eb[2] - eb[0]
    parts.append(f'<g transform="translate({(VW-ew)/2 - eb[0]:.1f} {L["en_y"] - eb[1]:.1f})">')
    for i, g in enumerate(eg):
        parts.append(f'<g class="glyph" style="animation-delay:{T_EN + i*STAG:.2f}s">'
                     f'<path d="{g["d"]}" fill="{WHITE}"/></g>')
    parts.append('</g>')
    ag, _, _, _ = shape_glyphs(CAIRO, AR_WORD, 27, {"wght": 600})
    order = sorted(range(len(ag)), key=lambda i: ag[i]["cluster"])
    rank = {idx: r for r, idx in enumerate(order)}
    ab = L["ab"]
    aw = ab[2] - ab[0]
    parts.append(f'<g class="ar" transform="translate({(VW-aw)/2 - ab[0]:.1f} '
                 f'{L["ar_y"] - ab[1]:.1f})">')
    for i, g in enumerate(ag):
        parts.append(f'<g class="glyph" style="animation-delay:{T_AR + rank[i]*STAG:.2f}s">'
                     f'<path d="{g["d"]}" fill="{WHITE}"/></g>')
    parts.append('</g>')
    parts.append('<g class="loader">')
    for i in range(3):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{loader_c}" style="animation-delay:{i*0.2:.1f}s"/>')
    parts.append('</g>')
    write_svg(f"splash/splash-animated-{tag}.svg", VW, VH, "".join(parts))


def write_preview_html():
    with open(os.path.join(OUT, "splash/splash-animated-preview.html"), "w") as f:
        f.write('''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morabh — round meem splash</title>
<style>body{margin:0;background:#E8EBF2;display:flex;gap:32px;align-items:center;
justify-content:center;min-height:100vh;flex-wrap:wrap}
.phone{width:min(340px,88vw);aspect-ratio:390/844;border-radius:40px;overflow:hidden;
box-shadow:0 30px 80px rgba(13,27,38,.4);border:10px solid #0D1B26;background:#fff}
.phone img{width:100%;height:100%;display:block}</style></head>
<body><div class="phone"><img src="splash-animated-light.svg" alt="light"></div>
<div class="phone"><img src="splash-animated-dark.svg" alt="dark"></div>
<script>document.querySelectorAll("img").forEach(m=>m.onclick=e=>{const s=e.target.src;e.target.src="";e.target.src=s})</script>
</body></html>''')


# ----------------------------------------------------------- GIF
def _cl(v):
    return max(0.0, min(1.0, v))


def _eo(p):
    return 1 - (1 - p) ** 3


def _ebk(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def frame_svg(t, dark=False):
    L = splash_layout()
    s = L["s"]
    drop = TEAL if dark else WHITE
    parts = [splash_bg(dark)]
    inner = [f'<g fill="none" stroke="{WHITE}" stroke-width="{SW}" stroke-linecap="round">']
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
        dy = -34 * (1 - f) / s
        sc = 0.5 + 0.5 * f
        inner.append(f'<circle cx="{DROP_C[0]}" cy="{DROP_C[1] + dy:.1f}" r="{DROP_R*sc:.1f}" '
                     f'fill="{drop}" opacity="{min(1, pd*3):.2f}"/>')
    parts.append(f'<g transform="translate({L["lx"] - S_BBOX[0]*s:.2f} '
                 f'{L["ly"] - S_BBOX[1]*s:.2f}) scale({s:.5f})">{"".join(inner)}</g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "Morabh", 40, {"wght": 800})
    eb = L["eb"]
    ew = eb[2] - eb[0]
    parts.append(f'<g transform="translate({(VW-ew)/2 - eb[0]:.1f} {L["en_y"] - eb[1]:.1f})">')
    for i, g in enumerate(eg):
        p = _eo(_cl((t - (T_EN + i * STAG)) / 0.5))
        if p > 0:
            parts.append(f'<path d="{g["d"]}" fill="{WHITE}" opacity="{p:.2f}" '
                         f'transform="translate(0 {12*(1-p):.1f})"/>')
    parts.append('</g>')
    ag, _, _, _ = shape_glyphs(CAIRO, AR_WORD, 27, {"wght": 600})
    order = sorted(range(len(ag)), key=lambda i: ag[i]["cluster"])
    rank = {idx: r for r, idx in enumerate(order)}
    ab = L["ab"]
    aw = ab[2] - ab[0]
    parts.append(f'<g transform="translate({(VW-aw)/2 - ab[0]:.1f} {L["ar_y"] - ab[1]:.1f})">')
    for i, g in enumerate(ag):
        p = _eo(_cl((t - (T_AR + rank[i] * STAG)) / 0.5))
        if p > 0:
            parts.append(f'<path d="{g["d"]}" fill="{WHITE}" opacity="{p*0.75:.2f}" '
                         f'transform="translate(0 {12*(1-p):.1f})"/>')
    parts.append('</g>')
    pl = _cl((t - T_LOADER) / 0.5)
    if pl > 0:
        c = TEAL if dark else WHITE
        for i in range(3):
            pulse = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t - T_LOADER) / 1.2) - i * 1.1))
            parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                         f'fill="{c}" opacity="{pl*pulse*0.8:.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
            f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')


def build_gif(dark=False, fps=15, dur=3.6):
    tag = "dark" if dark else "light"
    tmp = f"/tmp/rm-frames-{tag}"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    for k in range(int(dur * fps)):
        p = os.path.join(tmp, f"f{k:03d}.svg")
        with open(p, "w") as f:
            f.write(frame_svg(k / fps, dark))
        run(["rsvg-convert", "-w", "300", p, "-o", os.path.join(tmp, f"f{k:03d}.png")])
    run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
         os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame",
         os.path.join(OUT, f"splash/splash-animated-{tag}-preview.gif")])


if __name__ == "__main__":
    build_logo()
    build_icons()
    build_favicons()
    build_splash_static()
    build_splash_animated(False)
    build_splash_animated(True)
    write_preview_html()
    build_gif(False)
    build_gif(True)
    print("round-meem kit ->", OUT)
