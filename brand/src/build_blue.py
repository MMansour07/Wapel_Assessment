#!/usr/bin/env python3
"""Morabh brand — BLUE theme build (app color system).

Re-themes the entire asset pipeline to the product palette:
primary #33509C, light text #6C8DDF, tints #A2BCFF/#DEE7FF,
mint #A3FFED, gold #F1DC84, Sharia green #074D31.

Outputs to ../../brand-blue/. Also generates the static creative
white splash and the animated splash (SVG + HTML preview + GIF).
"""
import math
import os
import shutil
import subprocess

import build
from build import SYM_W, SYM_H, SYM_BBOX, wm_metrics, wordmark_frag, symbol_placed
from textpath import shape_glyphs

# ---------------------------------------------------------------- palette
PRIMARY = "#33509C"      # main / text
HOVER = "#1F3B82"
PRESSED = "#294387"
DARKEST = "#122F78"      # Primary pressed-dark — dark surfaces
P400 = "#5A7CD4"
P200 = "#7798EB"
LIGHT_TEXT = "#6C8DDF"   # Primary light text (display)
P50 = "#A2BCFF"
P25 = "#DEE7FF"          # tint
MINT = "#A3FFED"
MINT_TINT = "#E3FFF9"
GOLD = "#F1DC84"
GOLD_TINT = "#FFEEAA"
SHARIA = "#074D31"       # SA / Sharia green — gain-dot on light bg
WHITE = "#FFFFFF"
BLACK = "#000000"

OUT = os.path.join(os.path.dirname(build.BRAND), "workspace-tmp")  # replaced below
OUT = os.path.abspath(os.path.join(build.BRAND, "..", "brand-blue"))


def apply_theme():
    build.OUT = OUT
    build.GREEN = PRIMARY
    build.GREEN_DEEP = HOVER
    build.NILE = DARKEST
    build.GOLD = GOLD
    build.MINT = MINT
    build.COTTON = "#F7F9FF"
    build.GRAD_A = P400
    build.GRAD_B = HOVER
    build.VARIANTS = {
        # on light: navy mark/text, Sharia-green gain-dot & diacritics
        "color": dict(text=PRIMARY, mark=PRIMARY, dot=SHARIA, ar_mark=SHARIA),
        # on dark/colored: white mark/text, gold gain-dot & diacritics
        "reverse": dict(text=WHITE, mark=WHITE, dot=GOLD, ar_mark=GOLD),
        "black": dict(text=BLACK, mark=BLACK, dot=BLACK, ar_mark=BLACK),
        "white": dict(text=WHITE, mark=WHITE, dot=WHITE, ar_mark=WHITE),
    }


# ---------------------------------------------------------------- splash (static)
def splash_decor(W, H):
    """Creative white-based background: soft tint washes + rising steps."""
    parts = [f'''<defs>
<radialGradient id="w1"><stop offset="0" stop-color="{P25}"/><stop offset="1" stop-color="{P25}" stop-opacity="0"/></radialGradient>
<radialGradient id="w2"><stop offset="0" stop-color="{MINT_TINT}"/><stop offset="1" stop-color="{MINT_TINT}" stop-opacity="0"/></radialGradient>
<radialGradient id="w3"><stop offset="0" stop-color="{GOLD_TINT}"/><stop offset="1" stop-color="{GOLD_TINT}" stop-opacity="0"/></radialGradient>
</defs>''']
    parts.append(f'<rect width="{W}" height="{H}" fill="{WHITE}"/>')
    parts.append(f'<circle cx="{W*0.92:.0f}" cy="{H*0.10:.0f}" r="{W*0.62:.0f}" fill="url(#w1)"/>')
    parts.append(f'<circle cx="{W*0.04:.0f}" cy="{H*0.86:.0f}" r="{W*0.55:.0f}" fill="url(#w2)"/>')
    parts.append(f'<circle cx="{W*0.16:.0f}" cy="{H*0.16:.0f}" r="{W*0.30:.0f}" fill="url(#w3)" opacity="0.7"/>')
    # ascending steps, whisper-quiet, bottom right
    bw = W * 0.045
    for i in range(4):
        bh = H * (0.05 + 0.030 * i)
        x = W * 0.74 + i * bw * 1.55
        parts.append(f'<rect x="{x:.0f}" y="{H*0.965 - bh:.0f}" width="{bw:.0f}" '
                     f'height="{bh + H*0.06:.0f}" rx="{bw/2:.0f}" fill="{P25}" opacity="0.55"/>')
    return "".join(parts)


def splash_frag_blue(W, H, dark=False):
    if dark:
        parts = [f'<rect width="{W}" height="{H}" fill="{DARKEST}"/>',
                 f'<circle cx="{W*0.9:.0f}" cy="{H*0.08:.0f}" r="{W*0.6:.0f}" fill="{PRIMARY}" opacity="0.35"/>',
                 f'<circle cx="{W*0.05:.0f}" cy="{H*0.9:.0f}" r="{W*0.5:.0f}" fill="{PRESSED}" opacity="0.45"/>']
        mark, dot, text_en, text_ar, marks, sub = WHITE, GOLD, WHITE, WHITE, GOLD, MINT
    else:
        parts = [splash_decor(W, H)]
        mark, dot, text_en, text_ar, marks, sub = PRIMARY, SHARIA, LIGHT_TEXT, LIGHT_TEXT, SHARIA, P400
    sym_h = H * 0.115
    sym_w = SYM_W * (sym_h / SYM_H)
    en_size = H * 0.040
    ar_size = H * 0.036
    me = wm_metrics("en", en_size)
    ma = wm_metrics("ar", ar_size)
    cy = H * 0.42
    top = cy - (sym_h + H * 0.02 + me["asc"] + H * 0.012 + ma["asc"] + ma["desc"]) / 2
    parts.append(symbol_placed((W - sym_w) / 2, top, sym_h, mark, dot))
    by = top + sym_h + H * 0.02 + me["asc"]
    parts.append(wordmark_frag("en", (W - me["w"]) / 2, by, en_size, text_en))
    by2 = by + H * 0.012 + ma["asc"]
    parts.append(wordmark_frag("ar", (W - ma["w"]) / 2, by2, ar_size, text_ar, marks))
    dot_y = H * 0.88
    for i, op in enumerate((0.35, 0.6, 1.0)):
        parts.append(f'<circle cx="{W/2 + (i-1)*28:.0f}" cy="{dot_y:.0f}" r="7" fill="{sub}" opacity="{op}"/>')
    return "".join(parts)


def build_splash_blue():
    for tag, dark in (("light", False), ("dark", True)):
        for W, H, label in ((1284, 2778, "ios"), (1080, 1920, "android")):
            rel = f"splash/morabh-splash-{tag}-{label}-{W}x{H}"
            build.write_svg(rel + ".svg", W, H, splash_frag_blue(W, H, dark))
            build.render(rel + ".svg", rel + ".png")


# ---------------------------------------------------------------- animated splash
# Timeline (seconds)
T_RING, D_RING = 0.15, 0.80
T_LINE, D_LINE = 0.55, 1.00
T_DOT, D_DOT = 1.35, 0.55
T_EN, STAG_EN, D_GLYPH = 1.55, 0.07, 0.55
T_AR, STAG_AR = 1.80, 0.08
T_LOADER = 2.30

RING_LEN = 2 * math.pi * 62          # 389.6 (symbol local units)
LINE_PTS = [(178, 321), (262, 229), (340, 325), (442, 161), (442, 427)]
LINE_LEN = sum(math.dist(a, b) for a, b in zip(LINE_PTS, LINE_PTS[1:]))

VW, VH = 390, 844                     # design viewport


def splash_layout():
    """Positions shared by the animated SVG and the GIF frame renderer."""
    sym_h = VH * 0.115
    s = sym_h / SYM_H
    sym_w = SYM_W * s
    en_size = VH * 0.040
    ar_size = VH * 0.036
    me = wm_metrics("en", en_size)
    ma = wm_metrics("ar", ar_size)
    cy = VH * 0.42
    top = cy - (sym_h + VH * 0.02 + me["asc"] + VH * 0.012 + ma["asc"] + ma["desc"]) / 2
    sym_tx = (VW - sym_w) / 2 - SYM_BBOX[0] * s
    sym_ty = top - SYM_BBOX[1] * s
    by_en = top + sym_h + VH * 0.02 + me["asc"]
    by_ar = by_en + VH * 0.012 + ma["asc"]
    return dict(s=s, sym_tx=sym_tx, sym_ty=sym_ty,
                en_size=en_size, ar_size=ar_size, me=me, ma=ma,
                x_en=(VW - me["w"]) / 2, by_en=by_en,
                x_ar=(VW - ma["w"]) / 2, by_ar=by_ar)


def glyph_runs():
    """(glyphs, transform-scale) for both wordmarks at layout sizes."""
    L = splash_layout()
    en_glyphs, _, _, _ = shape_glyphs(build.MANROPE, build.EN_TEXT, 100, {"wght": 800})
    ar_glyphs, _, _, _ = shape_glyphs(build.CAIRO, build.AR_TEXT, 100, {"wght": 600})
    # Arabic reading order = cluster ascending (meem first); marks pop after bases
    order = sorted(range(len(ar_glyphs)), key=lambda i: (ar_glyphs[i]["cluster"],
                   ar_glyphs[i]["name"] in build.ARABIC_MARKS))
    ar_rank = {idx: r for r, idx in enumerate(order)}
    return L, en_glyphs, ar_glyphs, ar_rank


def animated_splash_svg():
    L, en_glyphs, ar_glyphs, ar_rank = glyph_runs()
    me, ma = L["me"], L["ma"]
    sw = 54
    css = f'''
    .ring {{ stroke-dasharray:{RING_LEN:.1f}; stroke-dashoffset:{RING_LEN:.1f};
            animation: draw-ring {D_RING}s cubic-bezier(.55,0,.35,1) {T_RING}s both; }}
    .rise {{ stroke-dasharray:{LINE_LEN:.1f}; stroke-dashoffset:{LINE_LEN:.1f};
            animation: draw-rise {D_LINE}s cubic-bezier(.55,0,.3,1) {T_LINE}s both; }}
    .gain {{ animation: drop {D_DOT}s cubic-bezier(.34,1.56,.64,1) {T_DOT}s both;
            transform-box: fill-box; transform-origin: center; }}
    .glyph {{ animation: pop {D_GLYPH}s cubic-bezier(.22,1,.36,1) both;
             transform-box: fill-box; transform-origin: center bottom; }}
    .loader {{ opacity:0; animation: fadein .6s ease-out {T_LOADER}s forwards; }}
    .loader circle {{ animation: pulse 1.2s ease-in-out infinite; }}
    .wash {{ transform-box: fill-box; transform-origin: center;
            animation: floaty 9s ease-in-out infinite alternate; }}
    @keyframes draw-ring {{ from {{ stroke-dashoffset: {RING_LEN:.1f}; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes draw-rise {{ from {{ stroke-dashoffset: {LINE_LEN:.1f}; }} to {{ stroke-dashoffset: 0; }} }}
    @keyframes drop   {{ from {{ opacity:0; transform: translateY(-64px) scale(.4); }}
                         to   {{ opacity:1; transform: translateY(0) scale(1); }} }}
    @keyframes pop    {{ from {{ opacity:0; transform: translateY(16px); }}
                         to   {{ opacity:1; transform: translateY(0); }} }}
    @keyframes fadein {{ to {{ opacity:1; }} }}
    @keyframes pulse  {{ 0%,100% {{ opacity:.3; }} 50% {{ opacity:1; }} }}
    @keyframes floaty {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-14px); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .ring, .rise {{ animation: none; stroke-dashoffset: 0; }}
      .gain, .glyph, .loader, .wash, .loader circle {{ animation: none; opacity: 1; }}
    }}'''
    parts = [f'<style>{css}</style>']
    # -- creative white background
    parts.append(f'''<defs>
<radialGradient id="w1"><stop offset="0" stop-color="{P25}"/><stop offset="1" stop-color="{P25}" stop-opacity="0"/></radialGradient>
<radialGradient id="w2"><stop offset="0" stop-color="{MINT_TINT}"/><stop offset="1" stop-color="{MINT_TINT}" stop-opacity="0"/></radialGradient>
<radialGradient id="w3"><stop offset="0" stop-color="{GOLD_TINT}"/><stop offset="1" stop-color="{GOLD_TINT}" stop-opacity="0"/></radialGradient>
</defs>
<rect width="{VW}" height="{VH}" fill="{WHITE}"/>
<circle class="wash" cx="{VW*0.92:.0f}" cy="{VH*0.10:.0f}" r="{VW*0.62:.0f}" fill="url(#w1)"/>
<circle class="wash" style="animation-delay:-4s" cx="{VW*0.04:.0f}" cy="{VH*0.86:.0f}" r="{VW*0.55:.0f}" fill="url(#w2)"/>
<circle class="wash" style="animation-delay:-7s" cx="{VW*0.16:.0f}" cy="{VH*0.16:.0f}" r="{VW*0.30:.0f}" fill="url(#w3)" opacity="0.7"/>''')
    for i in range(4):
        bh = VH * (0.05 + 0.030 * i)
        x = VW * 0.74 + i * VW * 0.045 * 1.55
        parts.append(f'<rect x="{x:.0f}" y="{VH*0.965 - bh:.0f}" width="{VW*0.045:.0f}" '
                     f'height="{bh + VH*0.06:.0f}" rx="{VW*0.0225:.0f}" fill="{P25}" opacity="0.55"/>')
    # -- symbol: ring draws, line rises, damma-dot drops in
    parts.append(f'<g transform="translate({L["sym_tx"]:.2f} {L["sym_ty"]:.2f}) scale({L["s"]:.5f})">'
                 f'<g fill="none" stroke="{PRIMARY}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round">'
                 f'<circle class="ring" cx="132" cy="363" r="62"/>'
                 f'<path class="rise" d="M 178 321 L 262 229 L 340 325 L 442 161 L 442 427"/>'
                 f'</g><circle class="gain" cx="442" cy="85" r="27" fill="{SHARIA}"/></g>')
    # -- wordmarks render in glyph by glyph
    s_en = L["en_size"] / 100.0
    parts.append(f'<g transform="translate({L["x_en"] - me["x0"]:.2f} {L["by_en"]:.2f}) scale({s_en:.5f})">')
    for i, g in enumerate(en_glyphs):
        parts.append(f'<g class="glyph" style="animation-delay:{T_EN + i*STAG_EN:.2f}s">'
                     f'<path d="{g["d"]}" fill="{LIGHT_TEXT}"/></g>')
    parts.append('</g>')
    s_ar = L["ar_size"] / 100.0
    parts.append(f'<g transform="translate({L["x_ar"] - ma["x0"]:.2f} {L["by_ar"]:.2f}) scale({s_ar:.5f})">')
    for i, g in enumerate(ar_glyphs):
        is_mark = g["name"] in build.ARABIC_MARKS
        fill = SHARIA if is_mark else LIGHT_TEXT
        delay = T_AR + ar_rank[i] * STAG_AR + (0.12 if is_mark else 0.0)
        parts.append(f'<g class="glyph" style="animation-delay:{delay:.2f}s">'
                     f'<path d="{g["d"]}" fill="{fill}"/></g>')
    parts.append('</g>')
    # -- loader dots
    parts.append(f'<g class="loader">')
    for i in range(3):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.88:.0f}" r="4" '
                     f'fill="{P400}" style="animation-delay:{i*0.2:.1f}s"/>')
    parts.append('</g>')
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
           f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')
    path = os.path.join(OUT, "splash/morabh-splash-animated.svg")
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(svg)
    # HTML preview wrapper
    with open(os.path.join(OUT, "splash/morabh-splash-animated-preview.html"), "w") as f:
        f.write(f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morabh — animated splash preview</title>
<style>body{{margin:0;background:#DEE7FF;display:flex;align-items:center;justify-content:center;min-height:100vh}}
.phone{{width:min(390px,92vw);aspect-ratio:390/844;border-radius:40px;overflow:hidden;
box-shadow:0 30px 80px rgba(18,47,120,.35);border:10px solid #122F78;background:#fff}}
.phone img{{width:100%;height:100%;display:block}}</style></head>
<body><div class="phone"><img src="morabh-splash-animated.svg" alt="Morabh animated splash"></div>
<script>/* click to replay */document.querySelector("img").onclick=e=>{{const s=e.target.src;e.target.src="";e.target.src=s}}</script>
</body></html>''')


# ---------------------------------------------------------------- GIF preview
def _clamp(v):
    return max(0.0, min(1.0, v))


def _ease_out_cubic(p):
    return 1 - (1 - p) ** 3


def _ease_out_back(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def frame_svg(t):
    L, en_glyphs, ar_glyphs, ar_rank = glyph_runs()
    me, ma = L["me"], L["ma"]
    parts = [splash_decor(VW, VH)]
    p_ring = _ease_out_cubic(_clamp((t - T_RING) / D_RING))
    p_line = _ease_out_cubic(_clamp((t - T_LINE) / D_LINE))
    parts.append(f'<g transform="translate({L["sym_tx"]:.2f} {L["sym_ty"]:.2f}) scale({L["s"]:.5f})">'
                 f'<g fill="none" stroke="{PRIMARY}" stroke-width="54" stroke-linecap="round" stroke-linejoin="round">')
    if p_ring > 0.001:
        parts.append(f'<circle cx="132" cy="363" r="62" stroke-dasharray="{RING_LEN:.1f}" '
                     f'stroke-dashoffset="{RING_LEN*(1-p_ring):.1f}"/>')
    if p_line > 0.001:
        parts.append(f'<path d="M 178 321 L 262 229 L 340 325 L 442 161 L 442 427" '
                     f'stroke-dasharray="{LINE_LEN:.1f}" stroke-dashoffset="{LINE_LEN*(1-p_line):.1f}"/>')
    parts.append('</g>')
    pd = _clamp((t - T_DOT) / D_DOT)
    if pd > 0:
        f = _ease_out_back(pd)
        dy = -64 * (1 - f) / L["s"]
        sc = 0.4 + 0.6 * f
        op = min(1.0, pd * 3)
        parts.append(f'<g transform="translate(442 {85 + dy:.1f})">'
                     f'<circle r="{27*sc:.1f}" fill="{SHARIA}" opacity="{op:.2f}"/></g>')
    parts.append('</g>')

    def glyph_state(delay):
        p = _ease_out_cubic(_clamp((t - delay) / D_GLYPH))
        return p, 16 * (1 - p)

    s_en = L["en_size"] / 100.0
    parts.append(f'<g transform="translate({L["x_en"] - me["x0"]:.2f} {L["by_en"]:.2f}) scale({s_en:.5f})">')
    for i, g in enumerate(en_glyphs):
        p, dy = glyph_state(T_EN + i * STAG_EN)
        if p > 0:
            parts.append(f'<path d="{g["d"]}" fill="{LIGHT_TEXT}" opacity="{p:.2f}" '
                         f'transform="translate(0 {dy / s_en:.1f})"/>')
    parts.append('</g>')
    s_ar = L["ar_size"] / 100.0
    parts.append(f'<g transform="translate({L["x_ar"] - ma["x0"]:.2f} {L["by_ar"]:.2f}) scale({s_ar:.5f})">')
    for i, g in enumerate(ar_glyphs):
        is_mark = g["name"] in build.ARABIC_MARKS
        delay = T_AR + ar_rank[i] * STAG_AR + (0.12 if is_mark else 0.0)
        p, dy = glyph_state(delay)
        if p > 0:
            fill = SHARIA if is_mark else LIGHT_TEXT
            parts.append(f'<path d="{g["d"]}" fill="{fill}" opacity="{p:.2f}" '
                         f'transform="translate(0 {dy / s_ar:.1f})"/>')
    parts.append('</g>')
    pl = _clamp((t - T_LOADER) / 0.6)
    if pl > 0:
        for i in range(3):
            pulse = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t - T_LOADER) / 1.2) - i * 1.1))
            parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.88:.0f}" r="4" '
                         f'fill="{P400}" opacity="{pl * pulse:.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
            f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')


def build_gif(fps=15, dur=3.4):
    tmp = "/tmp/splash-frames"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    n = int(dur * fps)
    for k in range(n):
        t = k / fps
        svg_path = os.path.join(tmp, f"f{k:03d}.svg")
        with open(svg_path, "w") as f:
            f.write(frame_svg(t))
        subprocess.run(["rsvg-convert", "-w", "300", svg_path, "-o",
                        os.path.join(tmp, f"f{k:03d}.png")], check=True)
    out_gif = os.path.join(OUT, "splash/morabh-splash-animated-preview.gif")
    subprocess.run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
                    os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame", out_gif], check=True)
    print("gif:", out_gif)


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    apply_theme()
    build.build_symbol_files()
    build.build_horizontal("en")
    build.build_horizontal("ar")
    build.build_stacked("en")
    build.build_stacked("ar")
    build.build_bilingual_horizontal()
    build.build_bilingual_stacked()
    build.build_wordmark_files()
    build.export_logo_pngs()
    build.build_app_icons()
    build.build_favicons()
    build.build_social()
    build_splash_blue()
    animated_splash_svg()
    build_gif()
    print("blue theme done ->", OUT)
