#!/usr/bin/env python3
"""Morabh Round Meem — inDrive-style INLINE lockups + splash update.

The symbol sits inline with the wordmark like a letterform: ring aligned to
cap height, tail + drop hanging below the baseline like a descender.

- logo/lockup-inline-en-*  : [symbol] Morabh
- logo/lockup-inline-ar-*  : مُرابِح [symbol]   (RTL: symbol leads on the right)
- splash-white/, splash/   : all splash compositions updated to the inline
  arrangement (animated SVG + GIF + statics regenerated in place)
"""
import math
import os
import shutil
import subprocess

import build_round_meem as rm
from build_round_meem import (S_BBOX, S_W, S_H, RING_C, RING_R, SW,
                              TAIL_A, TAIL_B, DROP_C, DROP_R,
                              RING_LEN, TAIL_LEN, word,
                              CAIRO, MANROPE,
                              GRAD_TOP, GRAD_BOT, DARK_BG, TEAL, WHITE)
from textpath import shape_glyphs, shape_bounds

OUT = rm.OUT
LIGHT = "#6C8DDF"
BLACK = "#000000"
AR_WORD = "\u0645\u064f\u0631\u0627\u0628\u0650\u062d"  # مُرابِح (with diacritics)
MARKS = {"uni064F", "uni0650"}

# symbol vertical anatomy (512 units): ring outer 96..284, descender to 378
RING_TOP, RING_BOT, SYM_BOT = 96.0, 284.0, 378.0
RING_OUTER = RING_BOT - RING_TOP  # 188


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


def sym_inline(x_left, baseline, en_size, mark, drop=None):
    """Symbol scaled so ring = ~1.06 cap height, ring-bottom on the baseline."""
    cap = 0.715 * en_size
    s = cap * 1.06 / RING_OUTER
    tx = x_left - S_BBOX[0] * s
    ty = baseline - RING_BOT * s
    return (f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">'
            f'{rm.symbol_frag(mark, drop or mark)}</g>'), S_W * s, s


def word_frag(font, text, size, color, mark_color=None):
    wght = 800 if font == MANROPE else 600
    glyphs, adv, _, _ = shape_glyphs(font, text, size, {"wght": wght})
    b = shape_bounds(font, text, size, {"wght": wght})
    parts = []
    for g in glyphs:
        c = (mark_color or color) if g["name"] in MARKS else color
        parts.append(f'<path d="{g["d"]}" fill="{c}"/>')
    return "".join(parts), b


def inline_lockup_en(size, mark, text_c, drop=None):
    """Returns (frag, W, H, baseline). Content starts at x=0 (plus pad by caller)."""
    enp, eb = word_frag(MANROPE, "Morabh", size, text_c)
    cap = 0.715 * size
    gap = cap * 0.22
    sfrag, sw, s = sym_inline(0, 0, size, mark, drop)
    tx = sw + gap
    frag = sfrag + f'<g transform="translate({tx - eb[0]:.2f} 0)">{enp}</g>'
    W = tx + (eb[2] - eb[0])
    top = min((RING_TOP - RING_BOT) * s, eb[1])
    bot = max((SYM_BOT - RING_BOT) * s, eb[3])
    return frag, W, top, bot


def inline_lockup_ar(size, mark, text_c, drop=None, mark_c=None):
    """RTL: symbol on the right, word to its left."""
    arp, ab = word_frag(CAIRO, AR_WORD, size, text_c, mark_c or drop or text_c)
    cap = 0.715 * size
    gap = cap * 0.24
    aw = ab[2] - ab[0]
    frag_w = f'<g transform="translate({-ab[0]:.2f} 0)">{arp}</g>'
    sfrag, sw, s = sym_inline(aw + gap, 0, size, mark, drop)
    W = aw + gap + sw
    top = min((RING_TOP - RING_BOT) * s, ab[1])
    bot = max((SYM_BOT - RING_BOT) * s, ab[3])
    return frag_w + sfrag, W, top, bot


def build_lockups():
    variants = {
        "6C8DDF-white": dict(bg=WHITE, mark=LIGHT, text=LIGHT, drop=None),
        "white-gradient": dict(bg="grad", mark=WHITE, text=WHITE, drop=None),
        "white-dark": dict(bg=DARK_BG, mark=WHITE, text=WHITE, drop=TEAL),
        "black": dict(bg=None, mark=BLACK, text=BLACK, drop=None),
    }
    for lang in ("en", "ar"):
        for name, v in variants.items():
            size = 120
            if lang == "en":
                frag, W, top, bot = inline_lockup_en(size, v["mark"], v["text"], v["drop"])
            else:
                frag, W, top, bot = inline_lockup_ar(size, v["mark"], v["text"], v["drop"],
                                                     mark_c=v["drop"] or v["text"])
            pad = 44
            H = (bot - top) + 2 * pad
            bg = ""
            if v["bg"] == "grad":
                bg = (f'<defs>{rm.GRAD_DEF}</defs>'
                      f'<rect width="{W + 2*pad:.0f}" height="{H:.0f}" rx="28" fill="url(#bg)"/>')
            elif v["bg"]:
                bg = f'<rect width="{W + 2*pad:.0f}" height="{H:.0f}" rx="28" fill="{v["bg"]}"/>'
            body = bg + f'<g transform="translate({pad:.1f} {pad - top:.1f})">{frag}</g>'
            rel = f"logo/lockup-inline-{lang}-{name}.svg"
            write_svg(rel, W + 2 * pad, H, body)
            render(rel, f"logo/lockup-inline-{lang}-{name}.png", w=1400)
    # remove superseded stacked lockup
    for f in ("logo/lockup-stacked-gradient.svg", "logo/lockup-stacked-gradient.png"):
        p = os.path.join(OUT, f)
        if os.path.exists(p):
            os.remove(p)


# ------------------------------------------------------------- splash inline
VW, VH = 390, 844
T_RING, D_RING = 0.20, 0.75
T_TAIL, D_TAIL = 0.85, 0.40
T_DROP, D_DROP = 1.25, 0.55
T_EN, STAG = 1.60, 0.06
T_AR = 2.15
T_LOADER = 2.65

EN_SIZE = 44
AR_SIZE = 26


def theme(kind):
    if kind == "white":
        return dict(bg=f'<rect width="{VW}" height="{VH}" fill="{WHITE}"/>',
                    mark=LIGHT, text=LIGHT, drop=LIGHT, ar=LIGHT, loader=LIGHT, ar_op=0.85)
    if kind == "light":
        return dict(bg=(f'<defs>{rm.GRAD_DEF}</defs>'
                        f'<rect width="{VW}" height="{VH}" fill="url(#bg)"/>'),
                    mark=WHITE, text=WHITE, drop=WHITE, ar=WHITE, loader=WHITE, ar_op=0.75)
    return dict(bg=(f'<rect width="{VW}" height="{VH}" fill="{DARK_BG}"/>'
                    f'<circle cx="{VW/2}" cy="{VH*0.40:.0f}" r="{VW*0.55:.0f}" '
                    f'fill="{TEAL}" opacity="0.10"/>'),
                mark=WHITE, text=WHITE, drop=TEAL, ar=WHITE, loader=TEAL, ar_op=0.75)


def splash_geo():
    enp, eb = word_frag(MANROPE, "Morabh", EN_SIZE, "#000")
    cap = 0.715 * EN_SIZE
    gap = cap * 0.22
    s = cap * 1.06 / RING_OUTER
    sw = S_W * s
    W = sw + gap + (eb[2] - eb[0])
    x0 = (VW - W) / 2
    baseline = VH * 0.435
    arp, ab = word_frag(CAIRO, AR_WORD, AR_SIZE, "#000")
    ar_y = baseline + (SYM_BOT - RING_BOT) * s + 58
    return dict(x0=x0, baseline=baseline, s=s, sw=sw, gap=gap, eb=eb, ab=ab, ar_y=ar_y)


def splash_static(kind):
    G = splash_geo()
    T = theme(kind)
    parts = [T["bg"]]
    sfrag, _, _ = sym_inline(G["x0"], G["baseline"], EN_SIZE, T["mark"], T["drop"])
    parts.append(sfrag)
    enp, eb = word_frag(MANROPE, "Morabh", EN_SIZE, T["text"])
    parts.append(f'<g transform="translate({G["x0"] + G["sw"] + G["gap"] - eb[0]:.2f} '
                 f'{G["baseline"]:.2f})">{enp}</g>')
    arp, ab = word_frag(CAIRO, AR_WORD, AR_SIZE, T["ar"], T["drop"] if kind == "dark" else None)
    aw = ab[2] - ab[0]
    parts.append(f'<g opacity="{T["ar_op"]}" transform="translate({(VW-aw)/2 - ab[0]:.2f} '
                 f'{G["ar_y"] - ab[1]:.2f})">{arp}</g>')
    for i, op in enumerate((0.35, 0.6, 1.0)):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{T["loader"]}" opacity="{op*0.85:.2f}"/>')
    return "".join(parts)


def splash_animated(kind):
    G = splash_geo()
    T = theme(kind)
    s = G["s"]
    css = f'''
    .ring {{ stroke-dasharray:{RING_LEN:.1f}; stroke-dashoffset:{RING_LEN:.1f};
             animation: dr {D_RING}s cubic-bezier(.55,0,.35,1) {T_RING}s both; }}
    .tail {{ stroke-dasharray:{TAIL_LEN:.1f}; stroke-dashoffset:{TAIL_LEN:.1f};
             animation: dt {D_TAIL}s ease-out {T_TAIL}s both; }}
    .drop {{ animation: fall {D_DROP}s cubic-bezier(.34,1.56,.64,1) {T_DROP}s both;
             transform-box: fill-box; transform-origin: center; }}
    .glyph {{ animation: pop .5s cubic-bezier(.22,1,.36,1) both;
              transform-box: fill-box; transform-origin: center bottom; }}
    .arw {{ opacity:0; animation: rise .6s cubic-bezier(.22,1,.36,1) {T_AR}s forwards; }}
    .loader {{ opacity:0; animation: fadein .5s ease-out {T_LOADER}s forwards; }}
    .loader circle {{ animation: pulse 1.2s ease-in-out infinite; }}
    @keyframes dr {{ to {{ stroke-dashoffset:0; }} }}
    @keyframes dt {{ to {{ stroke-dashoffset:0; }} }}
    @keyframes fall {{ from {{ opacity:0; transform: translateY(-30px) scale(.5); }}
                       to {{ opacity:1; transform:none; }} }}
    @keyframes pop {{ from {{ opacity:0; transform: translateX(14px); }}
                      to {{ opacity:1; transform:none; }} }}
    @keyframes rise {{ from {{ opacity:0; transform: translateY(10px); }}
                       to {{ opacity:{T["ar_op"]}; transform:none; }} }}
    @keyframes fadein {{ to {{ opacity:1; }} }}
    @keyframes pulse {{ 0%,100% {{ opacity:.3; }} 50% {{ opacity:1; }} }}
    @media (prefers-reduced-motion: reduce) {{
      .ring,.tail {{ animation:none; stroke-dashoffset:0; }}
      .drop,.glyph,.loader,.loader circle {{ animation:none; opacity:1; }}
      .arw {{ animation:none; opacity:{T["ar_op"]}; }}
    }}'''
    parts = [f'<style>{css}</style>', T["bg"]]
    tx = G["x0"] - S_BBOX[0] * s
    ty = G["baseline"] - RING_BOT * s
    parts.append(f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">'
                 f'<g fill="none" stroke="{T["mark"]}" stroke-width="{SW}" stroke-linecap="round">'
                 f'<circle class="ring" cx="{RING_C[0]}" cy="{RING_C[1]}" r="{RING_R}"/>'
                 f'<path class="tail" d="M {TAIL_A[0]} {TAIL_A[1]} L {TAIL_B[0]} {TAIL_B[1]}"/>'
                 f'</g>'
                 f'<circle class="drop" cx="{DROP_C[0]}" cy="{DROP_C[1]}" r="{DROP_R}" '
                 f'fill="{T["drop"]}"/></g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "Morabh", EN_SIZE, {"wght": 800})
    eb = G["eb"]
    parts.append(f'<g transform="translate({G["x0"] + G["sw"] + G["gap"] - eb[0]:.2f} '
                 f'{G["baseline"]:.2f})">')
    for i, g in enumerate(eg):
        parts.append(f'<g class="glyph" style="animation-delay:{T_EN + i*STAG:.2f}s">'
                     f'<path d="{g["d"]}" fill="{T["text"]}"/></g>')
    parts.append('</g>')
    arp, ab = word_frag(CAIRO, AR_WORD, AR_SIZE, T["ar"],
                        T["drop"] if kind == "dark" else None)
    aw = ab[2] - ab[0]
    parts.append(f'<g transform="translate({(VW-aw)/2 - ab[0]:.2f} '
                 f'{G["ar_y"] - ab[1]:.2f})"><g class="arw">{arp}</g></g>')
    parts.append('<g class="loader">')
    for i in range(3):
        parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                     f'fill="{T["loader"]}" style="animation-delay:{i*0.2:.1f}s"/>')
    parts.append('</g>')
    return "".join(parts)


def _cl(v):
    return max(0.0, min(1.0, v))


def _eo(p):
    return 1 - (1 - p) ** 3


def _ebk(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def frame_svg(t, kind):
    G = splash_geo()
    T = theme(kind)
    s = G["s"]
    parts = [T["bg"]]
    inner = [f'<g fill="none" stroke="{T["mark"]}" stroke-width="{SW}" stroke-linecap="round">']
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
        dy = -30 * (1 - f) / s
        sc = 0.5 + 0.5 * f
        inner.append(f'<circle cx="{DROP_C[0]}" cy="{DROP_C[1] + dy:.1f}" r="{DROP_R*sc:.1f}" '
                     f'fill="{T["drop"]}" opacity="{min(1, pd*3):.2f}"/>')
    tx = G["x0"] - S_BBOX[0] * s
    ty = G["baseline"] - RING_BOT * s
    parts.append(f'<g transform="translate({tx:.2f} {ty:.2f}) scale({s:.5f})">{"".join(inner)}</g>')
    eg, _, _, _ = shape_glyphs(MANROPE, "Morabh", EN_SIZE, {"wght": 800})
    eb = G["eb"]
    parts.append(f'<g transform="translate({G["x0"] + G["sw"] + G["gap"] - eb[0]:.2f} '
                 f'{G["baseline"]:.2f})">')
    for i, g in enumerate(eg):
        p = _eo(_cl((t - (T_EN + i * STAG)) / 0.5))
        if p > 0:
            parts.append(f'<path d="{g["d"]}" fill="{T["text"]}" opacity="{p:.2f}" '
                         f'transform="translate({14*(1-p):.1f} 0)"/>')
    parts.append('</g>')
    pa = _eo(_cl((t - T_AR) / 0.6))
    if pa > 0:
        arp, ab = word_frag(CAIRO, AR_WORD, AR_SIZE, T["ar"],
                            T["drop"] if kind == "dark" else None)
        aw = ab[2] - ab[0]
        parts.append(f'<g opacity="{pa * T["ar_op"]:.2f}" transform="translate('
                     f'{(VW-aw)/2 - ab[0]:.2f} {G["ar_y"] - ab[1] + 10*(1-pa):.2f})">{arp}</g>')
    pl = _cl((t - T_LOADER) / 0.5)
    if pl > 0:
        for i in range(3):
            pulse = 0.3 + 0.7 * (0.5 + 0.5 * math.sin(2 * math.pi * ((t - T_LOADER) / 1.2) - i * 1.1))
            parts.append(f'<circle cx="{VW/2 + (i-1)*16:.0f}" cy="{VH*0.885:.0f}" r="4" '
                         f'fill="{T["loader"]}" opacity="{pl*pulse*0.85:.2f}"/>')
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {VW} {VH}" '
            f'width="{VW}" height="{VH}">{"".join(parts)}</svg>')


def build_gif(kind, out_rel, fps=15, dur=3.7):
    tmp = f"/tmp/inl-{kind}"
    shutil.rmtree(tmp, ignore_errors=True)
    os.makedirs(tmp)
    for k in range(int(dur * fps)):
        p = os.path.join(tmp, f"f{k:03d}.svg")
        with open(p, "w") as f:
            f.write(frame_svg(k / fps, kind))
        run(["rsvg-convert", "-w", "300", p, "-o", os.path.join(tmp, f"f{k:03d}.png")])
    run(["convert", "-delay", str(round(100 / fps)), "-loop", "0",
         os.path.join(tmp, "f*.png"), "-layers", "OptimizeFrame",
         os.path.join(OUT, out_rel)])


def build_splashes():
    jobs = {
        "white": ("splash-white/splash-white", "splash-white/splash-white-animated",
                  "splash-white/splash-white-animated-preview.gif"),
        "light": ("splash/splash-light", "splash/splash-animated-light",
                  "splash/splash-animated-light-preview.gif"),
        "dark": ("splash/splash-dark", "splash/splash-animated-dark",
                 "splash/splash-animated-dark-preview.gif"),
    }
    for kind, (static_base, anim_base, gif_rel) in jobs.items():
        write_svg(static_base + ".svg", VW, VH, splash_static(kind))
        render(static_base + ".svg", static_base + "-1284x2778.png", w=1284, h=2778)
        render(static_base + ".svg", static_base + "-1080x1920.png", w=1080, h=1920)
        render(static_base + ".svg", static_base + "-preview.png", w=780)
        write_svg(anim_base + ".svg", VW, VH, splash_animated(kind))
        build_gif(kind, gif_rel)


if __name__ == "__main__":
    build_lockups()
    build_splashes()
    print("inline update ->", OUT)
