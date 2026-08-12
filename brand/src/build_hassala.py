#!/usr/bin/env python3
"""Morabh brand — GLASS HASSALA symbol, blue app palette. Full asset kit.

The mark: a transparent (outline) Egyptian hassala money box, open at the
top, with saved coins visible inside and the next installment — the green
halal gain — dropping in. Transparency + saving + installments in one shape.

Outputs to ../../brand-hassala/ including an animated splash where the
vessel draws itself and the coins land one by one.
"""
import math
import os
import shutil
import subprocess

import build
import build_blue
from build_blue import (PRIMARY, HOVER, DARKEST, P400, P25, LIGHT_TEXT,
                        MINT_TINT, GOLD, GOLD_TINT, SHARIA, WHITE)
from textpath import shape_glyphs

OUT = os.path.abspath(os.path.join(build.BRAND, "..", "brand-hassala"))

# ------------------------------------------------------------- the symbol
# 512 design box. Ink bbox (with 44 stroke, round caps): (84,130)..(428,430)
H_BBOX = (84.0, 130.0, 428.0, 430.0)
H_W = H_BBOX[2] - H_BBOX[0]   # 344
H_H = H_BBOX[3] - H_BBOX[1]   # 300

ARC_LEN = 150 * math.radians(70.5)   # each shoulder arc ~184.6
BASE_LEN = 300.0


def hassala_frag(mark, dot, sw=44):
    """Glass hassala: open outline vessel + 2 saved coins + dropping gain coin."""
    return (
        f'<g fill="none" stroke="{mark}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round">'
        f'<path d="M 106 408 A 150 150 0 0 1 206 267"/>'
        f'<path d="M 406 408 A 150 150 0 0 0 306 267"/>'
        f'<path d="M 106 408 H 406"/>'
        f'</g>'
        f'<rect x="186" y="346" width="140" height="34" rx="17" fill="{mark}"/>'
        f'<rect x="200" y="300" width="112" height="34" rx="17" fill="{mark}"/>'
        f'<rect x="234" y="130" width="44" height="110" rx="22" fill="{dot}"/>'
    )


def apply():
    build_blue.apply_theme()
    build.OUT = OUT
    build_blue.OUT = OUT
    build.symbol_frag = hassala_frag
    build.SYM_BBOX = H_BBOX
    build.SYM_W = H_W
    build.SYM_H = H_H
    build_blue.SYM_W = H_W
    build_blue.SYM_H = H_H
    build_blue.SYM_BBOX = H_BBOX


# ------------------------------------------------- simplified small favicon
def build_favicons_simplified():
    """At 16-48 px the glass outline mushes, so the favicon uses the solid
    hassala silhouette (white dome, slot cut in bg blue, gold coin)."""
    dome = (f'<path d="M 76 400 A 180 180 0 0 1 436 400 Z" fill="{WHITE}"/>'
            f'<rect x="188" y="230" width="136" height="38" rx="19" fill="{PRIMARY}"/>'
            f'<rect x="231" y="92" width="50" height="152" rx="25" fill="{GOLD}"/>')
    frag = f'<rect width="512" height="512" rx="112" fill="{PRIMARY}"/>' + dome
    build.write_svg("favicon/favicon.svg", 512, 512, frag)
    for s in (16, 32, 48, 180, 192, 512):
        build.render("favicon/favicon.svg", f"favicon/favicon-{s}x{s}.png", w=s, h=s)
    subprocess.run(["convert",
                    os.path.join(OUT, "favicon/favicon-16x16.png"),
                    os.path.join(OUT, "favicon/favicon-32x32.png"),
                    os.path.join(OUT, "favicon/favicon-48x48.png"),
                    os.path.join(OUT, "favicon/favicon.ico")], check=True)
    frag = f'<rect width="512" height="512" fill="{PRIMARY}"/>' + \
        f'<g transform="translate(77 77) scale(0.7)">{dome}</g>'
    build.write_svg("favicon/maskable.svg", 512, 512, frag)
    build.render("favicon/maskable.svg", "favicon/maskable-512x512.png", w=512, h=512)
    build.render("favicon/maskable.svg", "favicon/maskable-192x192.png", w=192, h=192)


# ------------------------------------------------------------- animation
T_BASE, D_BASE = 0.15, 0.45
T_ARC, D_ARC = 0.50, 0.55
T_C1, T_C2, D_COIN = 1.00, 1.28, 0.55
T_DROP, D_DROP = 1.62, 0.55
T_EN, STAG_EN, D_GLYPH = 1.90, 0.07, 0.55
T_AR, STAG_AR = 2.15, 0.08
T_LOADER = 2.65

VW, VH = 390, 844


def animated_splash_svg():
    L = build_blue.splash_layout()
    _, en_glyphs, ar_glyphs, ar_rank = build_blue.glyph_runs()
    me, ma = L["me"], L["ma"]
    css = f'''
    .base {{ stroke-dasharray:{BASE_LEN}; stroke-dashoffset:{BASE_LEN};
             animation: dr-base {D_BASE}s ease-out {T_BASE}s both; }}
    .arc  {{ stroke-dasharray:{ARC_LEN:.1f}; stroke-dashoffset:{ARC_LEN:.1f};
             animation: dr-arc {D_ARC}s cubic-bezier(.55,0,.35,1) {T_ARC}s both; }}
    .coin {{ animation: land {D_COIN}s cubic-bezier(.34,1.56,.64,1) both;
             transform-box: fill-box; transform-origin: center; }}
    .c1 {{ animation-delay: {T_C1}s; }} .c2 {{ animation-delay: {T_C2}s; }}
    .drop {{ animation: fall {D_DROP}s cubic-bezier(.34,1.56,.64,1) {T_DROP}s both;
             transform-box: fill-box; transform-origin: center; }}
    .glyph {{ animation: pop {D_GLYPH}s cubic-bezier(.22,1,.36,1) both;
              transform-box: fill-box; transform-origin: center bottom; }}
    .loader {{ opacity:0; animation: fadein .6s ease-out {T_LOADER}s forwards; }}
    .loader circle {{ animation: pulse 1.2s ease-in-out infinite; }}
    .wash {{ transform-box: fill-box; transform-origin: center;
             animation: floaty 9s ease-in-out infinite alternate; }}
    @keyframes dr-base {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes dr-arc  {{ to {{ stroke-dashoffset: 0; }} }}
    @keyframes land {{ from {{ opacity:0; transform: translateY(-30px); }}
                       to   {{ opacity:1; transform: translateY(0); }} }}
    @keyframes fall {{ from {{ opacity:0; transform: translateY(-56px); }}
                       to   {{ opacity:1; transform: translateY(0); }} }}
    @keyframes pop  {{ from {{ opacity:0; transform: translateY(16px); }}
                       to   {{ opacity:1; transform: translateY(0); }} }}
    @keyframes fadein {{ to {{ opacity:1; }} }}
    @keyframes pulse  {{ 0%,100% {{ opacity:.3; }} 50% {{ opacity:1; }} }}
    @keyframes floaty {{ from {{ transform: translateY(0); }} to {{ transform: translateY(-14px); }} }}
    @media (prefers-reduced-motion: reduce) {{
      .base, .arc {{ animation: none; stroke-dashoffset: 0; }}
      .coin, .drop, .glyph, .loader, .wash, .loader circle {{ animation: none; opacity: 1; }}
    }}'''
    parts = [f'<style>{css}</style>']
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
    # symbol: vessel draws, coins land, gain drops
    parts.append(f'<g transform="translate({L["sym_tx"]:.2f} {L["sym_ty"]:.2f}) scale({L["s"]:.5f})">'
                 f'<g fill="none" stroke="{PRIMARY}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round">'
                 f'<path class="base" d="M 106 408 H 406"/>'
                 f'<path class="arc" d="M 106 408 A 150 150 0 0 1 206 267"/>'
                 f'<path class="arc" d="M 406 408 A 150 150 0 0 0 306 267"/>'
                 f'</g>'
                 f'<rect class="coin c1" x="186" y="346" width="140" height="34" rx="17" fill="{PRIMARY}"/>'
                 f'<rect class="coin c2" x="200" y="300" width="112" height="34" rx="17" fill="{PRIMARY}"/>'
                 f'<rect class="drop" x="234" y="130" width="44" height="110" rx="22" fill="{SHARIA}"/>'
                 f'</g>')
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
    parts.append('<g class="loader">')
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
    with open(os.path.join(OUT, "splash/morabh-splash-animated-preview.html"), "w") as f:
        f.write(f'''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morabh — hassala animated splash</title>
<style>body{{margin:0;background:#DEE7FF;display:flex;align-items:center;justify-content:center;min-height:100vh}}
.phone{{width:min(390px,92vw);aspect-ratio:390/844;border-radius:40px;overflow:hidden;
box-shadow:0 30px 80px rgba(18,47,120,.35);border:10px solid #122F78;background:#fff}}
.phone img{{width:100%;height:100%;display:block}}</style></head>
<body><div class="phone"><img src="morabh-splash-animated.svg" alt="Morabh animated splash"></div>
<script>document.querySelector("img").onclick=e=>{{const s=e.target.src;e.target.src="";e.target.src=s}}</script>
</body></html>''')


def _clamp(v):
    return max(0.0, min(1.0, v))


def _eoc(p):
    return 1 - (1 - p) ** 3


def _eob(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def frame_svg(t):
    L = build_blue.splash_layout()
    _, en_glyphs, ar_glyphs, ar_rank = build_blue.glyph_runs()
    me, ma = L["me"], L["ma"]
    parts = [build_blue.splash_decor(VW, VH)]
    parts.append(f'<g transform="translate({L["sym_tx"]:.2f} {L["sym_ty"]:.2f}) scale({L["s"]:.5f})">'
                 f'<g fill="none" stroke="{PRIMARY}" stroke-width="44" stroke-linecap="round" stroke-linejoin="round">')
    pb = _eoc(_clamp((t - T_BASE) / D_BASE))
    pa = _eoc(_clamp((t - T_ARC) / D_ARC))
    if pb > 0.001:
        parts.append(f'<path d="M 106 408 H 406" stroke-dasharray="{BASE_LEN}" '
                     f'stroke-dashoffset="{BASE_LEN*(1-pb):.1f}"/>')
    if pa > 0.001:
        parts.append(f'<path d="M 106 408 A 150 150 0 0 1 206 267" stroke-dasharray="{ARC_LEN:.1f}" '
                     f'stroke-dashoffset="{ARC_LEN*(1-pa):.1f}"/>'
                     f'<path d="M 406 408 A 150 150 0 0 0 306 267" stroke-dasharray="{ARC_LEN:.1f}" '
                     f'stroke-dashoffset="{ARC_LEN*(1-pa):.1f}"/>')
    parts.append('</g>')
    for (x, y, w, delay) in ((186, 346, 140, T_C1), (200, 300, 112, T_C2)):
        p = _clamp((t - delay) / D_COIN)
        if p > 0:
            f = _eob(p)
            dy = -30 * (1 - f) / L["s"]
            parts.append(f'<rect x="{x}" y="{y + dy:.1f}" width="{w}" height="34" rx="17" '
                         f'fill="{PRIMARY}" opacity="{min(1, p*3):.2f}"/>')
    p = _clamp((t - T_DROP) / D_DROP)
    if p > 0:
        f = _eob(p)
        dy = -56 * (1 - f) / L["s"]
        parts.append(f'<rect x="234" y="{130 + dy:.1f}" width="44" height="110" rx="22" '
                     f'fill="{SHARIA}" opacity="{min(1, p*3):.2f}"/>')
    parts.append('</g>')

    def gstate(delay):
        p = _eoc(_clamp((t - delay) / D_GLYPH))
        return p, 16 * (1 - p)

    s_en = L["en_size"] / 100.0
    parts.append(f'<g transform="translate({L["x_en"] - me["x0"]:.2f} {L["by_en"]:.2f}) scale({s_en:.5f})">')
    for i, g in enumerate(en_glyphs):
        p, dy = gstate(T_EN + i * STAG_EN)
        if p > 0:
            parts.append(f'<path d="{g["d"]}" fill="{LIGHT_TEXT}" opacity="{p:.2f}" '
                         f'transform="translate(0 {dy / s_en:.1f})"/>')
    parts.append('</g>')
    s_ar = L["ar_size"] / 100.0
    parts.append(f'<g transform="translate({L["x_ar"] - ma["x0"]:.2f} {L["by_ar"]:.2f}) scale({s_ar:.5f})">')
    for i, g in enumerate(ar_glyphs):
        is_mark = g["name"] in build.ARABIC_MARKS
        delay = T_AR + ar_rank[i] * STAG_AR + (0.12 if is_mark else 0.0)
        p, dy = gstate(delay)
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


def build_gif(fps=15, dur=3.8):
    tmp = "/tmp/hassala-frames"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    n = int(dur * fps)
    for k in range(n):
        svg_path = os.path.join(tmp, f"f{k:03d}.svg")
        with open(svg_path, "w") as f:
            f.write(frame_svg(k / fps))
        subprocess.run(["rsvg-convert", "-w", "300", svg_path, "-o",
                        os.path.join(tmp, f"f{k:03d}.png")], check=True)
    subprocess.run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
                    os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame",
                    os.path.join(OUT, "splash/morabh-splash-animated-preview.gif")], check=True)


if __name__ == "__main__":
    apply()
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
    build_favicons_simplified()
    build.build_social()
    build_blue.build_splash_blue()
    animated_splash_svg()
    build_gif()
    print("hassala kit done ->", OUT)
