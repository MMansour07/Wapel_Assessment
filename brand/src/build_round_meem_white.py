#!/usr/bin/env python3
"""Morabh Round Meem — #6C8DDF-on-white product set.

Extends brand-round-meem/ with:
1. app-icon-white/   mobile app icon (symbol only, #6C8DDF on white) — full size matrix
2. splash-white/     white splash: symbol renders, then Morabh with مرابح underneath (animated + static)
3. navbar/           symbol-only navbar icons: #6C8DDF (light) + white (dark), all sizes
4. web/              website symbol logo (#6C8DDF, transparent + white-tile), PNG sizes
5. favicon-white/    favicons #6C8DDF on white — every practical size + .ico + maskable + manifest
6. admin/            admin loading animation (looping) + admin navbar icons
"""
import math
import os
import shutil
import subprocess

import build_round_meem as rm
from build_round_meem import (S_BBOX, S_W, S_H, RING_C, RING_R, SW,
                              TAIL_A, TAIL_B, DROP_C, DROP_R,
                              RING_LEN, TAIL_LEN, symbol_placed, word,
                              CAIRO, MANROPE, AR_WORD)
from textpath import shape_glyphs

OUT = rm.OUT
LIGHT = "#6C8DDF"
WHITE = "#FFFFFF"

ICON_SIZES = [16, 20, 24, 29, 32, 40, 48, 58, 60, 64, 76, 80, 87, 96, 114,
              120, 128, 144, 152, 167, 180, 192, 256, 384, 512, 1024]
FAV_SIZES = [16, 24, 32, 48, 64, 96, 128, 144, 152, 167, 180, 192, 256, 384, 512]
NAV_SIZES = [16, 20, 24, 28, 32, 40, 48, 64, 96, 128]


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


# ------------------------------------------------ 1. mobile app icon (white)
def build_app_icon_white():
    frag = (f'<rect width="1024" height="1024" fill="{WHITE}"/>'
            + symbol_placed((1024 - S_W * (630 / S_H)) / 2, (1024 - 630) / 2, 630,
                            LIGHT, LIGHT))
    write_svg("app-icon-white/icon-master-1024.svg", 1024, 1024, frag)
    for s in ICON_SIZES:
        render("app-icon-white/icon-master-1024.svg",
               f"app-icon-white/icon-{s}x{s}.png", w=s, h=s)
    # rounded preview (how it looks on the home screen)
    frag = (f'<rect width="1024" height="1024" rx="229" fill="{WHITE}" '
            f'stroke="#E7ECF7" stroke-width="4"/>'
            + symbol_placed((1024 - S_W * (630 / S_H)) / 2, (1024 - 630) / 2, 630,
                            LIGHT, LIGHT))
    write_svg("app-icon-white/icon-rounded-preview.svg", 1024, 1024, frag)
    render("app-icon-white/icon-rounded-preview.svg",
           "app-icon-white/icon-rounded-preview.png", w=512, h=512)


# ------------------------------------------------ 3+6. navbar + admin icons
def build_navbar():
    pad = 30
    for name, color in (("navbar-light-6C8DDF", LIGHT), ("navbar-dark-white", WHITE)):
        write_svg(f"navbar/{name}.svg", S_W + 2 * pad, S_H + 2 * pad,
                  symbol_placed(pad, pad, S_H, color, color))
        for s in NAV_SIZES:
            render(f"navbar/{name}.svg", f"navbar/{name}-{s}.png", h=s)
    # dark preview tile (so the white icon is visible in a file browser)
    write_svg("navbar/navbar-dark-preview.svg", 256, 256,
              f'<rect width="256" height="256" rx="32" fill="#0D1B26"/>'
              + symbol_placed((256 - S_W * (150 / S_H)) / 2, 53, 150, WHITE, WHITE))
    render("navbar/navbar-dark-preview.svg", "navbar/navbar-dark-preview.png")


# ------------------------------------------------ 4. website
def build_web():
    pad = 30
    write_svg("web/website-symbol.svg", S_W + 2 * pad, S_H + 2 * pad,
              symbol_placed(pad, pad, S_H, LIGHT, LIGHT))
    for s in (24, 32, 40, 48, 64, 96, 128, 256, 512):
        render("web/website-symbol.svg", f"web/website-symbol-{s}.png", h=s)
    write_svg("web/website-symbol-white-tile.svg", 512, 512,
              f'<rect width="512" height="512" rx="64" fill="{WHITE}"/>'
              + symbol_placed((512 - S_W * (330 / S_H)) / 2, 91, 330, LIGHT, LIGHT))
    render("web/website-symbol-white-tile.svg", "web/website-symbol-white-tile.png")


# ------------------------------------------------ 5. favicons (white)
def build_favicon_white():
    frag = (f'<rect width="512" height="512" fill="{WHITE}"/>'
            + symbol_placed((512 - S_W * (340 / S_H)) / 2, 86, 340, LIGHT, LIGHT))
    write_svg("favicon-white/favicon.svg", 512, 512, frag)
    for s in FAV_SIZES:
        render("favicon-white/favicon.svg", f"favicon-white/favicon-{s}x{s}.png", w=s, h=s)
    run(["convert",
         os.path.join(OUT, "favicon-white/favicon-16x16.png"),
         os.path.join(OUT, "favicon-white/favicon-32x32.png"),
         os.path.join(OUT, "favicon-white/favicon-48x48.png"),
         os.path.join(OUT, "favicon-white/favicon.ico")])
    # apple touch + maskable
    shutil.copy(os.path.join(OUT, "favicon-white/favicon-180x180.png"),
                os.path.join(OUT, "favicon-white/apple-touch-icon.png"))
    frag = (f'<rect width="512" height="512" fill="{WHITE}"/>'
            + symbol_placed((512 - S_W * (260 / S_H)) / 2, 126, 260, LIGHT, LIGHT))
    write_svg("favicon-white/maskable.svg", 512, 512, frag)
    render("favicon-white/maskable.svg", "favicon-white/maskable-512x512.png", w=512, h=512)
    render("favicon-white/maskable.svg", "favicon-white/maskable-192x192.png", w=192, h=192)
    with open(os.path.join(OUT, "favicon-white/site.webmanifest"), "w") as f:
        f.write('''{
  "name": "Morabh \\u2014 \\u0645\\u0631\\u0627\\u0628\\u062d",
  "short_name": "Morabh",
  "icons": [
    { "src": "/favicon-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/favicon-512x512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/maskable-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "theme_color": "#6C8DDF",
  "background_color": "#FFFFFF",
  "display": "standalone"
}
''')
    with open(os.path.join(OUT, "favicon-white/snippet.html"), "w") as f:
        f.write('''<!-- Morabh favicon set -->
<link rel="icon" href="/favicon.ico" sizes="48x48">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32x32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16x16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/apple-touch-icon.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#6C8DDF">
''')


# ------------------------------------------------ 2. white splash (animated)
VW, VH = 390, 844
T_RING, D_RING = 0.20, 0.75
T_TAIL, D_TAIL = 0.85, 0.40
T_DROP, D_DROP = 1.25, 0.55
T_EN, T_AR, STAG = 1.60, 2.05, 0.06
T_LOADER = 2.55


def layout():
    sym_h = 150
    s = sym_h / S_H
    lx = (VW - S_W * s) / 2
    ly = VH * 0.26
    enp, eb = word(MANROPE, "Morabh", 40, LIGHT, 800)
    arp, ab = word(CAIRO, AR_WORD, 27, LIGHT, 600)
    en_y = ly + sym_h + 62
    ar_y = en_y + (eb[3] - eb[1]) + 26
    return dict(s=s, sym_h=sym_h, lx=lx, ly=ly, enp=enp, eb=eb,
                arp=arp, ab=ab, en_y=en_y, ar_y=ar_y)


def splash_static_frag():
    L = layout()
    parts = [f'<rect width="{VW}" height="{VH}" fill="{WHITE}"/>']
    parts.append(symbol_placed(L["lx"], L["ly"], L["sym_h"], LIGHT, LIGHT))
    ew = L["eb"][2] - L["eb"][0]
    parts.append(f'<g transform="translate({(VW-ew)/2 - L["eb"][0]:.1f} '
                 f'{L["en_y"] - L["eb"][1]:.1f})">{L["enp"]}</g>')
    aw = L["ab"][2] - L["ab"][0]
    parts.append(f'<g opacity="0.85" transform="translate({(VW-aw)/2 - L["ab"][0]:.1f} '
                 f'{L["ar_y"] - L["ab"][1]:.1f})">{L["arp"]}</g>')
    for i, op in enumerate((0.35, 0.6, 1.0)):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{LIGHT}" opacity="{op}"/>')
    return "".join(parts)


def build_splash_white():
    write_svg("splash-white/splash-white.svg", VW, VH, splash_static_frag())
    render("splash-white/splash-white.svg", "splash-white/splash-white-1284x2778.png",
           w=1284, h=2778)
    render("splash-white/splash-white.svg", "splash-white/splash-white-1080x1920.png",
           w=1080, h=1920)
    render("splash-white/splash-white.svg", "splash-white/splash-white-preview.png", w=780)
    # animated
    L = layout()
    s = L["s"]
    css = f'''
    .ring {{ stroke-dasharray:{RING_LEN:.1f}; stroke-dashoffset:{RING_LEN:.1f};
             animation: dr {D_RING}s cubic-bezier(.55,0,.35,1) {T_RING}s both; }}
    .tail {{ stroke-dasharray:{TAIL_LEN:.1f}; stroke-dashoffset:{TAIL_LEN:.1f};
             animation: dt {D_TAIL}s ease-out {T_TAIL}s both; }}
    .drop {{ animation: fall {D_DROP}s cubic-bezier(.34,1.56,.64,1) {T_DROP}s both;
             transform-box: fill-box; transform-origin: center; }}
    .glyph {{ animation: pop .5s cubic-bezier(.22,1,.36,1) both;
              transform-box: fill-box; transform-origin: center bottom; }}
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
    parts = [f'<style>{css}</style>', f'<rect width="{VW}" height="{VH}" fill="{WHITE}"/>']
    parts.append(f'<g transform="translate({L["lx"] - S_BBOX[0]*s:.2f} '
                 f'{L["ly"] - S_BBOX[1]*s:.2f}) scale({s:.5f})">'
                 f'<g fill="none" stroke="{LIGHT}" stroke-width="{SW}" stroke-linecap="round">'
                 f'<circle class="ring" cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
                 f'<path class="tail" d="M {TAIL_A[0]} {TAIL_A[1]} L {TAIL_B[0]} {TAIL_B[1]}"/>'
                 f'</g>'
                 f'<circle class="drop" cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R}" fill="{LIGHT}"/>'
                 f'</g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "Morabh", 40, {"wght": 800})
    eb = L["eb"]
    ew = eb[2] - eb[0]
    parts.append(f'<g transform="translate({(VW-ew)/2 - eb[0]:.1f} {L["en_y"] - eb[1]:.1f})">')
    for i, g in enumerate(eg):
        parts.append(f'<g class="glyph" style="animation-delay:{T_EN + i*STAG:.2f}s">'
                     f'<path d="{g["d"]}" fill="{LIGHT}"/></g>')
    parts.append('</g>')
    ag, _, _, _ = shape_glyphs(CAIRO, AR_WORD, 27, {"wght": 600})
    order = sorted(range(len(ag)), key=lambda i: ag[i]["cluster"])
    rank = {idx: r for r, idx in enumerate(order)}
    ab = L["ab"]
    aw = ab[2] - ab[0]
    parts.append(f'<g opacity="0.85" transform="translate({(VW-aw)/2 - ab[0]:.1f} '
                 f'{L["ar_y"] - ab[1]:.1f})">')
    for i, g in enumerate(ag):
        parts.append(f'<g class="glyph" style="animation-delay:{T_AR + rank[i]*STAG:.2f}s">'
                     f'<path d="{g["d"]}" fill="{LIGHT}"/></g>')
    parts.append('</g>')
    parts.append('<g class="loader">')
    for i in range(3):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{LIGHT}" style="animation-delay:{i*0.2:.1f}s"/>')
    parts.append('</g>')
    write_svg("splash-white/splash-white-animated.svg", VW, VH, "".join(parts))
    with open(os.path.join(OUT, "splash-white/splash-white-preview.html"), "w") as f:
        f.write('''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morabh — white splash</title>
<style>body{margin:0;background:#E8EBF2;display:flex;align-items:center;justify-content:center;min-height:100vh}
.phone{width:min(390px,92vw);aspect-ratio:390/844;border-radius:40px;overflow:hidden;
box-shadow:0 30px 80px rgba(13,27,38,.35);border:10px solid #122F78;background:#fff}
.phone img{width:100%;height:100%;display:block}</style></head>
<body><div class="phone"><img src="splash-white-animated.svg" alt="Morabh splash"></div>
<script>document.querySelector("img").onclick=e=>{const s=e.target.src;e.target.src="";e.target.src=s}</script>
</body></html>''')


def _cl(v):
    return max(0.0, min(1.0, v))


def _eo(p):
    return 1 - (1 - p) ** 3


def _ebk(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def frame_svg(t):
    L = layout()
    s = L["s"]
    parts = [f'<rect width="{VW}" height="{VH}" fill="{WHITE}"/>']
    inner = [f'<g fill="none" stroke="{LIGHT}" stroke-width="{SW}" stroke-linecap="round">']
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
                     f'fill="{LIGHT}" opacity="{min(1, pd*3):.2f}"/>')
    parts.append(f'<g transform="translate({L["lx"] - S_BBOX[0]*s:.2f} '
                 f'{L["ly"] - S_BBOX[1]*s:.2f}) scale({s:.5f})">{"".join(inner)}</g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "Morabh", 40, {"wght": 800})
    eb = L["eb"]
    ew = eb[2] - eb[0]
    parts.append(f'<g transform="translate({(VW-ew)/2 - eb[0]:.1f} {L["en_y"] - eb[1]:.1f})">')
    for i, g in enumerate(eg):
        p = _eo(_cl((t - (T_EN + i * STAG)) / 0.5))
        if p > 0:
            parts.append(f'<path d="{g["d"]}" fill="{LIGHT}" opacity="{p:.2f}" '
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
            parts.append(f'<path d="{g["d"]}" fill="{LIGHT}" opacity="{p*0.85:.2f}" '
                         f'transform="translate(0 {12*(1-p):.1f})"/>')
    parts.append('</g>')
    pl = _cl((t - T_LOADER) / 0.5)
    if pl > 0:
        for i in range(3):
            pulse = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t - T_LOADER) / 1.2) - i * 1.1))
            parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                         f'fill="{LIGHT}" opacity="{pl*pulse:.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
            f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')


def build_gif(fps=15, dur=3.6):
    tmp = "/tmp/rmw-frames"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    for k in range(int(dur * fps)):
        p = os.path.join(tmp, f"f{k:03d}.svg")
        with open(p, "w") as f:
            f.write(frame_svg(k / fps))
        run(["rsvg-convert", "-w", "300", p, "-o", os.path.join(tmp, f"f{k:03d}.png")])
    run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
         os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame",
         os.path.join(OUT, "splash-white/splash-white-animated-preview.gif")])


# ------------------------------------------------ 6. admin loader
def build_admin():
    # navbar icons for admin (same as app navbar)
    pad = 30
    write_svg("admin/admin-navbar-6C8DDF.svg", S_W + 2 * pad, S_H + 2 * pad,
              symbol_placed(pad, pad, S_H, LIGHT, LIGHT))
    for s in (20, 24, 32, 40, 48, 64):
        render("admin/admin-navbar-6C8DDF.svg", f"admin/admin-navbar-{s}.png", h=s)
    # looping loader: ghost symbol + orbiting arc on the ring + pulsing drop
    arc = RING_LEN * 0.28
    css = f'''
    .spin {{ stroke-dasharray:{arc:.1f} {RING_LEN - arc:.1f};
             animation: orbit 1.4s linear infinite;
             transform-origin: {RING_C[0]}px {RING_C[1]}px; }}
    .pulse {{ animation: beat 1.4s ease-in-out infinite;
              transform-box: fill-box; transform-origin: center; }}
    @keyframes orbit {{ to {{ transform: rotate(360deg); }} }}
    @keyframes beat {{ 0%,100% {{ transform: scale(1); opacity:.9; }}
                       50% {{ transform: scale(1.25); opacity:1; }} }}
    @media (prefers-reduced-motion: reduce) {{ .spin,.pulse {{ animation:none; }} }}'''
    body = (f'<style>{css}</style>'
            f'<g opacity="0.22">{rm.symbol_frag(LIGHT, LIGHT)}</g>'
            f'<circle class="spin" cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}" '
            f'fill="none" stroke="{LIGHT}" stroke-width="{SW}" stroke-linecap="round"/>'
            f'<circle class="pulse" cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R}" fill="{LIGHT}"/>')
    write_svg("admin/admin-loader.svg", 512, 512,
              f'<rect width="512" height="512" fill="{WHITE}"/>'
              f'<g transform="translate({(512 - S_W*(300/S_H))/2 - S_BBOX[0]*(300/S_H):.2f} '
              f'{(512-300)/2 - S_BBOX[1]*(300/S_H):.2f}) scale({300/S_H:.5f})">{body}</g>')
    # loader GIF preview
    tmp = "/tmp/adm-frames"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    fps, dur = 20, 1.4
    for k in range(int(fps * dur)):
        t = k / fps
        ang = 360 * (t / 1.4)
        beat = 1 + 0.25 * math.sin(math.pi * (t / 1.4) * 2 - math.pi / 2) * 0.5 + 0.125
        sc = 1 + 0.25 * (0.5 - 0.5 * math.cos(2 * math.pi * t / 1.4))
        frame = (f'<rect width="512" height="512" fill="{WHITE}"/>'
                 f'<g transform="translate({(512 - S_W*(300/S_H))/2 - S_BBOX[0]*(300/S_H):.2f} '
                 f'{(512-300)/2 - S_BBOX[1]*(300/S_H):.2f}) scale({300/S_H:.5f})">'
                 f'<g opacity="0.22">{rm.symbol_frag(LIGHT, LIGHT)}</g>'
                 f'<g transform="rotate({ang:.1f} {RING_C[0]} {RING_C[1]})">'
                 f'<circle cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}" fill="none" '
                 f'stroke="{LIGHT}" stroke-width="{SW}" stroke-linecap="round" '
                 f'stroke-dasharray="{arc:.1f} {RING_LEN - arc:.1f}"/></g>'
                 f'<circle cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R*sc:.1f}" fill="{LIGHT}"/>'
                 f'</g>')
        p = os.path.join(tmp, f"f{k:03d}.svg")
        with open(p, "w") as f:
            f.write(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
                    f'width="512" height="512">{frame}</svg>')
        run(["rsvg-convert", "-w", "220", p, "-o", os.path.join(tmp, f"f{k:03d}.png")])
    run(["convert", "-delay", "5", "-loop", "0", os.path.join(tmp, "f*.png"),
         "-layers", "OptimizeFrame", os.path.join(OUT, "admin/admin-loader-preview.gif")])


if __name__ == "__main__":
    build_app_icon_white()
    build_navbar()
    build_web()
    build_favicon_white()
    build_splash_white()
    build_gif()
    build_admin()
    print("white set ->", OUT)
