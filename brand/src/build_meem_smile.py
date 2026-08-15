#!/usr/bin/env python3
"""Morabh — MEEM SMILE final branding kit (per client brief).

Symbol: the Meem Smile — meem ring + smile swoosh tail + gain dot.
Typography: Cairo (Arabic) + Cairo Latin (English) — one family, one voice.
Themes: light (#6C8DDF on white) and dark (white on #0D1B26). Flat, no gradients.

Splash: Stage 1 symbol fades/scales in centered -> Stage 2 scales down and moves
into inline position, مُرابِح reveals -> Stage 3 Arabic hides, Morabh shows,
symbol NEVER moves during the swap. Smooth easing, no bouncing.

Output: /workspace/branding/  (structure per brief section 12)
"""
import math
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from textpath import shape_glyphs, shape_bounds  # noqa: E402

OUT = os.path.abspath(os.path.join(HERE, "..", "..", "branding"))
FONTS = os.path.join(HERE, "..", "fonts")
CAIRO = os.path.join(FONTS, "Cairo.ttf")

BRAND = "#6C8DDF"
DARK_BG = "#0D1B26"
WHITE = "#FFFFFF"
AR_WORD = "\u0645\u064f\u0631\u0627\u0628\u0650\u062d"  # مُرابِح

THEMES = {
    "light": dict(bg=WHITE, fg=BRAND),
    "dark": dict(bg=DARK_BG, fg=WHITE),
}

# ------------------------------------------------------------- the symbol
# Meem Smile in a 512 design space (approved concept A geometry)
RING_C, RING_R, SW = (196, 192), 68, 48
SMILE = [(166, 254), (130, 360), (220, 420), (310, 408),
         (372, 400), (412, 366), (428, 322)]  # two cubic beziers
DOT_C, DOT_R = (442, 272), 26


def smile_path_d():
    p = SMILE
    return (f"M {p[0][0]} {p[0][1]} C {p[1][0]} {p[1][1]}, {p[2][0]} {p[2][1]}, "
            f"{p[3][0]} {p[3][1]} C {p[4][0]} {p[4][1]}, {p[5][0]} {p[5][1]}, "
            f"{p[6][0]} {p[6][1]}")


def _bezier_points(p0, p1, p2, p3, n=64):
    pts = []
    for i in range(n + 1):
        t = i / n
        mt = 1 - t
        x = mt**3*p0[0] + 3*mt*mt*t*p1[0] + 3*mt*t*t*p2[0] + t**3*p3[0]
        y = mt**3*p0[1] + 3*mt*mt*t*p1[1] + 3*mt*t*t*p2[1] + t**3*p3[1]
        pts.append((x, y))
    return pts


def _symbol_bbox():
    h = SW / 2
    xs, ys = [], []
    xs += [RING_C[0] - RING_R - h, RING_C[0] + RING_R + h]
    ys += [RING_C[1] - RING_R - h, RING_C[1] + RING_R + h]
    pts = (_bezier_points(SMILE[0], SMILE[1], SMILE[2], SMILE[3])
           + _bezier_points(SMILE[3], SMILE[4], SMILE[5], SMILE[6]))
    for x, y in pts:
        xs += [x - h, x + h]
        ys += [y - h, y + h]
    xs += [DOT_C[0] - DOT_R, DOT_C[0] + DOT_R]
    ys += [DOT_C[1] - DOT_R, DOT_C[1] + DOT_R]
    return min(xs), min(ys), max(xs), max(ys)


S_BBOX = _symbol_bbox()
S_W = S_BBOX[2] - S_BBOX[0]
S_H = S_BBOX[3] - S_BBOX[1]
RING_OUTER = 2 * (RING_R + SW / 2)
SMILE_LEN = None


def _polyline_len(pts):
    return sum(math.dist(a, b) for a, b in zip(pts, pts[1:]))


SMILE_LEN = _polyline_len(
    _bezier_points(SMILE[0], SMILE[1], SMILE[2], SMILE[3])
    + _bezier_points(SMILE[3], SMILE[4], SMILE[5], SMILE[6]))
RING_LEN = 2 * math.pi * RING_R


def symbol_frag(color):
    return (f'<g fill="none" stroke="{color}" stroke-width="{SW}" stroke-linecap="round">'
            f'<circle cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
            f'<path d="{smile_path_d()}"/></g>'
            f'<circle cx="{DOT_C[0]}" cy="{DOT_C[1]}" r="{DOT_R}" fill="{color}"/>')


def sym_placed(x, y, h, color):
    s = h / S_H
    return (f'<g transform="translate({x - S_BBOX[0]*s:.2f} {y - S_BBOX[1]*s:.2f}) '
            f'scale({s:.5f})">{symbol_frag(color)}</g>')


# ------------------------------------------------------------- io helpers
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


# ------------------------------------------------------------- typography
EN_SIZE, EN_WGHT = 46, 700
AR_SIZE, AR_WGHT = 48, 600
_cap = None


def cap_height(size):
    global _cap
    if _cap is None:
        b = shape_bounds(CAIRO, "M", 100, {"wght": EN_WGHT})
        _cap = -b[1] / 100.0
    return _cap * size


def word_frag(text, size, color, wght):
    glyphs, _, _, _ = shape_glyphs(CAIRO, text, size, {"wght": wght})
    b = shape_bounds(CAIRO, text, size, {"wght": wght})
    return "".join(f'<path d="{g["d"]}" fill="{color}"/>' for g in glyphs), b


def geo():
    """Inline geometry: symbol left, word right; symbol ring ~ cap height."""
    cap = cap_height(EN_SIZE)
    s = cap * 1.30 / RING_OUTER          # smile mark is compact; ring slightly over cap
    sw = S_W * s
    gap = cap * 0.34
    _, eb = word_frag("Morabh", EN_SIZE, "#000", EN_WGHT)
    _, ab = word_frag(AR_WORD, AR_SIZE, "#000", AR_WGHT)
    ew, aw = eb[2] - eb[0], ab[2] - ab[0]
    return dict(s=s, sw=sw, gap=gap, eb=eb, ab=ab, ew=ew, aw=aw,
                en_W=sw + gap + ew, ar_W=sw + gap + aw)


def sym_inline_at(x_left, baseline, color, s):
    """Ring vertical center aligned to mid-cap; smile dips below baseline."""
    cap = cap_height(EN_SIZE)
    ring_mid_target = baseline - cap * 0.52
    ty = ring_mid_target - RING_C[1] * s
    tx = x_left - S_BBOX[0] * s
    return (f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">'
            f'{symbol_frag(color)}</g>'), (tx, ty, s)


# ------------------------------------------------------------- logos
def build_logos():
    pad = 36
    for theme, T in THEMES.items():
        write_svg(f"logo/{theme}/morabh-symbol.svg", S_W + 2*pad, S_H + 2*pad,
                  sym_placed(pad, pad, S_H, T["fg"]))
        render(f"logo/{theme}/morabh-symbol.svg",
               f"logo/{theme}/morabh-symbol.png", w=1024)
        G = geo()
        for lang, word_txt, size, wght, W in (
                ("en", "Morabh", EN_SIZE, EN_WGHT, G["en_W"]),
                ("ar", AR_WORD, AR_SIZE, AR_WGHT, G["ar_W"])):
            wp, wb = word_frag(word_txt, size, T["fg"], wght)
            cap = cap_height(EN_SIZE)
            pad2 = 40
            sfrag, _ = sym_inline_at(pad2, pad2 + cap, T["fg"], G["s"])
            # vertical extent: symbol top/bottom relative to baseline
            ring_mid = cap * 0.52
            sym_top = -(ring_mid + (RING_C[1] - S_BBOX[1]) * G["s"] * 0 + (RING_C[1] - S_BBOX[1]) * 0)
            # compute properly: symbol top = baseline - ring_mid - (RING_C_y - bbox_top)*s
            sym_top = -(ring_mid + (RING_C[1] - S_BBOX[1]) * G["s"])
            sym_bot = -(ring_mid) + (S_BBOX[3] - RING_C[1]) * G["s"]
            top = min(sym_top, wb[1])
            bot = max(sym_bot, wb[3])
            H = bot - top + 2 * pad2
            baseline = pad2 - top
            sfrag, _ = sym_inline_at(pad2, baseline, T["fg"], G["s"])
            body = (sfrag + f'<g transform="translate('
                    f'{pad2 + G["sw"] + G["gap"] - wb[0]:.2f} {baseline:.2f})">{wp}</g>')
            write_svg(f"logo/{theme}/morabh-{lang}.svg", W + 2*pad2, H, body)
            render(f"logo/{theme}/morabh-{lang}.svg",
                   f"logo/{theme}/morabh-{lang}.png", w=1400)


# ------------------------------------------------------------- mobile
IOS_SIZES = [20, 29, 40, 58, 60, 76, 80, 87, 120, 152, 167, 180, 1024]
AND_SIZES = [36, 48, 72, 96, 144, 192, 512]


def build_mobile():
    for theme, T in THEMES.items():
        # app icon: symbol only, generous margins
        frag = (f'<rect width="1024" height="1024" fill="{T["bg"]}"/>'
                + sym_placed((1024 - S_W*(600/S_H))/2, (1024 - 600)/2, 600, T["fg"]))
        write_svg(f"mobile/ios/{theme}/morabh-app-icon.svg", 1024, 1024, frag)
        for s in IOS_SIZES:
            render(f"mobile/ios/{theme}/morabh-app-icon.svg",
                   f"mobile/ios/{theme}/AppIcon-{s}x{s}.png", w=s, h=s)
        write_svg(f"mobile/android/{theme}/morabh-launcher-icon.svg", 1024, 1024, frag)
        for s in AND_SIZES:
            render(f"mobile/android/{theme}/morabh-launcher-icon.svg",
                   f"mobile/android/{theme}/ic_launcher-{s}.png", w=s, h=s)
        write_svg(f"mobile/android/{theme}/adaptive-foreground.svg", 1024, 1024,
                  sym_placed((1024 - S_W*(520/S_H))/2, (1024 - 520)/2, 520, T["fg"]))
        render(f"mobile/android/{theme}/adaptive-foreground.svg",
               f"mobile/android/{theme}/adaptive-foreground-432.png", w=432, h=432)
        write_svg(f"mobile/android/{theme}/adaptive-background.svg", 1024, 1024,
                  f'<rect width="1024" height="1024" fill="{T["bg"]}"/>')
        render(f"mobile/android/{theme}/adaptive-background.svg",
               f"mobile/android/{theme}/adaptive-background-432.png", w=432, h=432)


# ------------------------------------------------------------- web
def build_web():
    # adaptive favicon
    s = 340 / S_H
    tx = (512 - S_W*s)/2 - S_BBOX[0]*s
    ty = 86 - S_BBOX[1]*s
    write_svg("web/favicon/morabh-favicon.svg", 512, 512,
              f'<style>.s{{stroke:{BRAND}}} .f{{fill:{BRAND}}}'
              f'@media (prefers-color-scheme: dark){{.s{{stroke:{WHITE}}} .f{{fill:{WHITE}}}}}'
              f'</style>'
              f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">'
              f'<g class="s" fill="none" stroke-width="{SW}" stroke-linecap="round">'
              f'<circle cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
              f'<path d="{smile_path_d()}"/></g>'
              f'<circle class="f" cx="{DOT_C[0]}" cy="{DOT_C[1]}" r="{DOT_R}"/></g>')
    for theme, T in THEMES.items():
        frag = (f'<rect width="512" height="512" fill="{T["bg"]}"/>'
                + sym_placed((512 - S_W*(340/S_H))/2, 86, 340, T["fg"]))
        write_svg(f"web/favicon/{theme}/favicon-master.svg", 512, 512, frag)
        for s2 in (16, 32, 48, 96, 128, 180, 192, 256, 512):
            render(f"web/favicon/{theme}/favicon-master.svg",
                   f"web/favicon/{theme}/favicon-{s2}x{s2}.png", w=s2, h=s2)
        run(["convert",
             os.path.join(OUT, f"web/favicon/{theme}/favicon-16x16.png"),
             os.path.join(OUT, f"web/favicon/{theme}/favicon-32x32.png"),
             os.path.join(OUT, f"web/favicon/{theme}/favicon-48x48.png"),
             os.path.join(OUT, f"web/favicon/{theme}/favicon.ico")])
        # header logos
        for lang in ("en", "ar"):
            for h in (24, 32, 40, 48, 64, 96, 128):
                render(f"logo/{theme}/morabh-{lang}.svg",
                       f"web/logo/{theme}/header-{lang}-h{h}.png", h=h)
        for h in (20, 24, 32, 40, 48, 64):
            render(f"logo/{theme}/morabh-symbol.svg",
                   f"web/logo/{theme}/header-symbol-h{h}.png", h=h)
    with open(os.path.join(OUT, "web/favicon/snippet.html"), "w") as f:
        f.write('''<!-- Morabh favicon (theme-adaptive SVG first, PNG/ICO fallbacks) -->
<link rel="icon" href="/morabh-favicon.svg" type="image/svg+xml">
<link rel="icon" href="/light/favicon.ico" sizes="48x48">
<link rel="icon" type="image/png" sizes="32x32" href="/light/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="/light/favicon-180x180.png">
<meta name="theme-color" media="(prefers-color-scheme: light)" content="#6C8DDF">
<meta name="theme-color" media="(prefers-color-scheme: dark)" content="#0D1B26">
''')


# ------------------------------------------------------------- splash
# timings (s) — per brief: fast, smooth, no bounce
T_IN, D_IN = 0.10, 0.45
T_MV, D_MV = 1.00, 0.45
T_ARI, D_ARI = 1.42, 0.28
T_ARO, D_ARO = 2.45, 0.25
T_ENI, D_ENI = 2.72, 0.28
TOTAL = 3.60
EASE = "cubic-bezier(.4,0,.2,1)"


def splash_transforms(VW, VH, big_h):
    G = geo()
    big_y = VH * 0.40 - big_h / 2
    sb = big_h / S_H
    B = ((VW - S_W*sb)/2 - S_BBOX[0]*sb, big_y - S_BBOX[1]*sb, sb)
    baseline = VH * 0.46
    x0 = (VW - G["en_W"]) / 2   # symbol fixed at EN-lockup position for BOTH stages
    _, (tx, ty, s) = sym_inline_at(x0, baseline, "#000", G["s"])
    D = (tx, ty, s)
    return G, B, D, x0, baseline


def rel(frm, to):
    k = to[2] / frm[2]
    return (to[0] - k*frm[0], to[1] - k*frm[1], k)


def splash_static(theme, stage, VW, VH, big_h):
    """stage: 'symbol' | 'arabic' | 'english'"""
    T = THEMES[theme]
    G, B, D, x0, baseline = splash_transforms(VW, VH, big_h)
    parts = [f'<rect width="{VW}" height="{VH}" fill="{T["bg"]}"/>']
    if stage == "symbol":
        parts.append(f'<g transform="translate({B[0]:.2f} {B[1]:.2f}) scale({B[2]:.5f})">'
                     f'{symbol_frag(T["fg"])}</g>')
    else:
        parts.append(f'<g transform="translate({D[0]:.2f} {D[1]:.2f}) scale({D[2]:.5f})">'
                     f'{symbol_frag(T["fg"])}</g>')
        txt, size, wght = (("Morabh", EN_SIZE, EN_WGHT) if stage == "english"
                           else (AR_WORD, AR_SIZE, AR_WGHT))
        wp, wb = word_frag(txt, size, T["fg"], wght)
        parts.append(f'<g transform="translate({x0 + G["sw"] + G["gap"] - wb[0]:.2f} '
                     f'{baseline:.2f})">{wp}</g>')
    return "".join(parts)


def splash_animated(theme, VW, VH, big_h):
    T = THEMES[theme]
    G, B, D, x0, baseline = splash_transforms(VW, VH, big_h)
    e = rel(B, D)
    sym_cx = B[0] + (S_BBOX[0] + S_W/2) * B[2]
    sym_cy = B[1] + (S_BBOX[1] + S_H/2) * B[2]
    css = f'''
    .in {{ opacity:0; transform-origin: {sym_cx:.1f}px {sym_cy:.1f}px;
           animation: ain {D_IN}s {EASE} {T_IN}s forwards; }}
    @keyframes ain {{ from {{ opacity:0; transform: scale(.92); }}
                      to {{ opacity:1; transform: scale(1); }} }}
    .mv {{ animation: amv {D_MV}s {EASE} {T_MV}s forwards; }}
    @keyframes amv {{ from {{ transform: none; }}
                      to {{ transform: translate({e[0]:.2f}px, {e[1]:.2f}px) scale({e[2]:.5f}); }} }}
    .arw {{ opacity:0;
            animation: win {D_ARI}s {EASE} {T_ARI}s forwards,
                       wout {D_ARO}s {EASE} {T_ARO}s forwards; }}
    .enw {{ opacity:0; animation: win {D_ENI}s {EASE} {T_ENI}s forwards; }}
    @keyframes win  {{ from {{ opacity:0; transform: translateY(6px); }}
                       to {{ opacity:1; transform: none; }} }}
    @keyframes wout {{ from {{ opacity:1; }} to {{ opacity:0; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .in {{ animation:none; opacity:1; }}
      .mv {{ animation:none; transform: translate({e[0]:.2f}px, {e[1]:.2f}px) scale({e[2]:.5f}); }}
      .arw {{ animation:none; opacity:0; }}
      .enw {{ animation:none; opacity:1; }}
    }}'''
    parts = [f'<style>{css}</style>',
             f'<rect width="{VW}" height="{VH}" fill="{T["bg"]}"/>',
             f'<g class="mv"><g class="in">'
             f'<g transform="translate({B[0]:.2f} {B[1]:.2f}) scale({B[2]:.5f})">'
             f'{symbol_frag(T["fg"])}</g></g></g>']
    arp, ab = word_frag(AR_WORD, AR_SIZE, T["fg"], AR_WGHT)
    parts.append(f'<g transform="translate({x0 + G["sw"] + G["gap"] - ab[0]:.2f} '
                 f'{baseline:.2f})"><g class="arw">{arp}</g></g>')
    enp, eb = word_frag("Morabh", EN_SIZE, T["fg"], EN_WGHT)
    parts.append(f'<g transform="translate({x0 + G["sw"] + G["gap"] - eb[0]:.2f} '
                 f'{baseline:.2f})"><g class="enw">{enp}</g></g>')
    return "".join(parts)


def _cl(v):
    return max(0.0, min(1.0, v))


def _eio(p):
    return 3*p*p - 2*p*p*p


def frame_svg(t, theme, VW, VH, big_h):
    T = THEMES[theme]
    G, B, D, x0, baseline = splash_transforms(VW, VH, big_h)
    parts = [f'<rect width="{VW}" height="{VH}" fill="{T["bg"]}"/>']
    p_in = _eio(_cl((t - T_IN) / D_IN))
    p_mv = _eio(_cl((t - T_MV) / D_MV))
    cur = tuple(B[i] + (D[i] - B[i]) * p_mv for i in range(3))
    if p_in > 0.01:
        sc = 0.92 + 0.08 * p_in
        cx = cur[0] + (S_BBOX[0] + S_W/2) * cur[2]
        cy = cur[1] + (S_BBOX[1] + S_H/2) * cur[2]
        parts.append(f'<g opacity="{p_in:.2f}" transform="translate({cx:.2f} {cy:.2f}) '
                     f'scale({sc:.4f}) translate({-cx:.2f} {-cy:.2f})">'
                     f'<g transform="translate({cur[0]:.2f} {cur[1]:.2f}) scale({cur[2]:.5f})">'
                     f'{symbol_frag(T["fg"])}</g></g>')
    ar_op = _eio(_cl((t - T_ARI) / D_ARI)) * (1 - _eio(_cl((t - T_ARO) / D_ARO)))
    if ar_op > 0.01:
        arp, ab = word_frag(AR_WORD, AR_SIZE, T["fg"], AR_WGHT)
        dy = 6 * (1 - _eio(_cl((t - T_ARI) / D_ARI)))
        parts.append(f'<g opacity="{ar_op:.2f}" transform="translate('
                     f'{x0 + G["sw"] + G["gap"] - ab[0]:.2f} {baseline + dy:.2f})">{arp}</g>')
    en_op = _eio(_cl((t - T_ENI) / D_ENI))
    if en_op > 0.01:
        enp, eb = word_frag("Morabh", EN_SIZE, T["fg"], EN_WGHT)
        dy = 6 * (1 - en_op)
        parts.append(f'<g opacity="{en_op:.2f}" transform="translate('
                     f'{x0 + G["sw"] + G["gap"] - eb[0]:.2f} {baseline + dy:.2f})">{enp}</g>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
            f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')


def build_gif(theme, VW, VH, big_h, out_rel, fps=20):
    tmp = f"/tmp/ms-{theme}-{VW}"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    for k in range(int(TOTAL * fps)):
        p = os.path.join(tmp, f"f{k:03d}.svg")
        with open(p, "w") as f:
            f.write(frame_svg(k / fps, theme, VW, VH, big_h))
        run(["rsvg-convert", "-w", "300" if VW < VH else "480", p,
             "-o", os.path.join(tmp, f"f{k:03d}.png")])
    run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
         os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame",
         os.path.join(OUT, out_rel)])


def build_splash():
    MOB = (390, 844, 170)
    WEB = (1440, 900, 220)
    for theme in THEMES:
        # static stage frames (per brief structure)
        for stage, fname in (("symbol", "symbol"), ("arabic", "arabic"),
                             ("english", "english")):
            write_svg(f"splash/{theme}/{fname}.svg", *MOB[:2],
                      splash_static(theme, stage, *MOB))
        render(f"splash/{theme}/symbol.svg",
               f"splash/{theme}/morabh-splash-symbol-{theme}-1284x2778.png",
               w=1284, h=2778)
        render(f"splash/{theme}/symbol.svg",
               f"splash/{theme}/morabh-splash-symbol-{theme}-1080x1920.png",
               w=1080, h=1920)
        # animated: mobile + web
        write_svg(f"splash/{theme}/morabh-splash-animated-mobile.svg", *MOB[:2],
                  splash_animated(theme, *MOB))
        write_svg(f"splash/{theme}/morabh-splash-animated-web.svg", *WEB[:2],
                  splash_animated(theme, *WEB))
        build_gif(theme, *MOB, f"splash/{theme}/morabh-splash-preview.gif")
    with open(os.path.join(OUT, "splash/preview.html"), "w") as f:
        f.write('''<!DOCTYPE html><html><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Morabh — Meem Smile splash</title>
<style>body{margin:0;background:#E8EBF2;display:flex;gap:28px;align-items:center;
justify-content:center;min-height:100vh;flex-wrap:wrap;padding:24px}
.phone{width:min(320px,86vw);aspect-ratio:390/844;border-radius:38px;overflow:hidden;
box-shadow:0 24px 60px rgba(13,27,38,.35);border:9px solid #0D1B26;background:#fff}
.web{width:min(720px,94vw);aspect-ratio:1440/900;border-radius:14px;overflow:hidden;
box-shadow:0 24px 60px rgba(13,27,38,.3);border:1px solid #c8d0dc;background:#fff}
img{width:100%;height:100%;display:block}
p{width:100%;text-align:center;font:600 14px system-ui;color:#4B5563;margin:0}</style></head>
<body>
<p>Click any preview to replay — Symbol → مُرابِح → Morabh</p>
<div class="phone"><img src="light/morabh-splash-animated-mobile.svg"></div>
<div class="phone"><img src="dark/morabh-splash-animated-mobile.svg"></div>
<div class="web"><img src="light/morabh-splash-animated-web.svg"></div>
<div class="web"><img src="dark/morabh-splash-animated-web.svg"></div>
<script>document.querySelectorAll("img").forEach(m=>m.onclick=e=>{const s=e.target.src;e.target.src="";e.target.src=s})</script>
</body></html>''')


if __name__ == "__main__":
    build_logos()
    build_mobile()
    build_web()
    build_splash()
    print("meem-smile branding ->", OUT)
