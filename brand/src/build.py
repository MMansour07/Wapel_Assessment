#!/usr/bin/env python3
"""Morabh brand asset builder.

Generates the complete logo system (SVG masters + PNG exports), favicons,
app icons, splash screens and social media assets from a single source of
truth: the symbol geometry + outlined wordmarks.

Run:  python3 build.py
"""
import os
import subprocess
import math

from textpath import shape_glyphs, shape_bounds

HERE = os.path.dirname(os.path.abspath(__file__))
BRAND = os.path.dirname(HERE)
FONTS = os.path.join(BRAND, "fonts")

MANROPE = os.path.join(FONTS, "Manrope.ttf")
CAIRO = os.path.join(FONTS, "Cairo.ttf")

EN_TEXT = "morabh"
AR_TEXT = "\u0645\u064f\u0631\u0627\u0628\u0650\u062d"  # مُرابِح
ARABIC_MARKS = {"uni064F", "uni0650"}  # damma, kasra

# ---------------------------------------------------------------- palette
GREEN = "#0C7C5F"        # Primary — Morabh Green
GREEN_DEEP = "#095E48"   # Primary 700 (hover / AA text on light)
NILE = "#052E25"         # Dark — Deep Nile
GOLD = "#E9B44C"         # Accent — Prosperity Gold
MINT = "#7CD9B8"         # Secondary — Mint
COTTON = "#F4FAF7"       # Light background — Cotton
WHITE = "#FFFFFF"
BLACK = "#000000"
GRAD_A = "#109070"       # app-icon gradient start
GRAD_B = "#085744"       # app-icon gradient end

# ---------------------------------------------------------------- symbol
# Master geometry lives in a 512x512 box. Ink bbox: (43, 58) .. (469, 454)
SYM_BBOX = (43.0, 58.0, 469.0, 454.0)
SYM_W = SYM_BBOX[2] - SYM_BBOX[0]   # 426
SYM_H = SYM_BBOX[3] - SYM_BBOX[1]   # 396


def symbol_frag(mark, dot, sw=54):
    """The Rising Meem: meem-head ring + ascending M stroke + damma gain-dot."""
    return (
        f'<g fill="none" stroke="{mark}" stroke-width="{sw}" '
        f'stroke-linecap="round" stroke-linejoin="round">'
        f'<circle cx="132" cy="363" r="62"/>'
        f'<path d="M 178 321 L 262 229 L 340 325 L 442 161 L 442 427"/>'
        f'</g>'
        f'<circle cx="442" cy="85" r="27" fill="{dot}"/>'
    )


def symbol_placed(x, y, h, mark, dot):
    """Symbol scaled to ink-height h with ink top-left at (x, y)."""
    s = h / SYM_H
    tx = x - SYM_BBOX[0] * s
    ty = y - SYM_BBOX[1] * s
    return f'<g transform="translate({tx:.3f} {ty:.3f}) scale({s:.5f})">{symbol_frag(mark, dot)}</g>'


# ---------------------------------------------------------------- wordmarks
_cache = {}


def wordmark_en():
    if "en" not in _cache:
        glyphs, adv, _, _ = shape_glyphs(MANROPE, EN_TEXT, 100, {"wght": 800})
        bounds = shape_bounds(MANROPE, EN_TEXT, 100, {"wght": 800})
        _cache["en"] = (glyphs, adv, bounds)
    return _cache["en"]


def wordmark_ar():
    if "ar" not in _cache:
        glyphs, adv, _, _ = shape_glyphs(CAIRO, AR_TEXT, 100, {"wght": 600})
        bounds = shape_bounds(CAIRO, AR_TEXT, 100, {"wght": 600})
        _cache["ar"] = (glyphs, adv, bounds)
    return _cache["ar"]


def wordmark_frag(which, x, y, size, color, mark_color=None):
    """Wordmark with baseline at y, left edge of ink at x, at font-size `size`.

    mark_color colors the Arabic diacritics (damma/kasra); defaults to `color`.
    """
    glyphs, adv, (x0, y0, x1, y1) = wordmark_en() if which == "en" else wordmark_ar()
    s = size / 100.0
    tx = x - x0 * s
    parts = [f'<g transform="translate({tx:.3f} {y:.3f}) scale({s:.5f})">']
    for g in glyphs:
        c = (mark_color or color) if g["name"] in ARABIC_MARKS else color
        parts.append(f'<path d="{g["d"]}" fill="{c}"/>')
    parts.append("</g>")
    return "".join(parts)


def wm_metrics(which, size):
    _, adv, (x0, y0, x1, y1) = wordmark_en() if which == "en" else wordmark_ar()
    s = size / 100.0
    return {
        "w": (x1 - x0) * s, "asc": -y0 * s, "desc": y1 * s,
        "x0": x0 * s, "adv": adv * s,
    }


# ---------------------------------------------------------------- io helpers
def write_svg(rel, w, h, content, bg=None):
    path = os.path.join(BRAND, rel)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    bg_rect = f'<rect width="{w:.0f}" height="{h:.0f}" fill="{bg}"/>' if bg else ""
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w:.0f} {h:.0f}" '
           f'width="{w:.0f}" height="{h:.0f}">{bg_rect}{content}</svg>')
    with open(path, "w") as f:
        f.write(svg)
    return path


def render(svg_rel, png_rel, w=None, h=None):
    svg = os.path.join(BRAND, svg_rel)
    png = os.path.join(BRAND, png_rel)
    os.makedirs(os.path.dirname(png), exist_ok=True)
    cmd = ["rsvg-convert", svg, "-o", png]
    if w:
        cmd += ["-w", str(w)]
    if h:
        cmd += ["-h", str(h)]
    subprocess.run(cmd, check=True)


# Variant palettes: (wordmark color, symbol mark, dot, divider)
VARIANTS = {
    "color": dict(text=NILE, mark=GREEN, dot=GOLD, ar_mark=GOLD),
    "reverse": dict(text=WHITE, mark=WHITE, dot=GOLD, ar_mark=GOLD),
    "black": dict(text=BLACK, mark=BLACK, dot=BLACK, ar_mark=BLACK),
    "white": dict(text=WHITE, mark=WHITE, dot=WHITE, ar_mark=WHITE),
}


# ---------------------------------------------------------------- logos
def build_symbol_files():
    pad = 26
    w = SYM_W + pad * 2
    h = SYM_H + pad * 2
    for name, v in VARIANTS.items():
        if name == "reverse":
            continue
        frag = symbol_placed(pad, pad, SYM_H, v["mark"], v["dot"])
        write_svg(f"logos/svg/morabh-symbol-{name}.svg", w, h, frag)
    # default = color
    frag = symbol_placed(pad, pad, SYM_H, GREEN, GOLD)
    write_svg("logos/svg/morabh-symbol.svg", w, h, frag)


def build_horizontal(lang):
    size = 100 if lang == "en" else 92
    m = wm_metrics(lang, size)
    sym_h = m["asc"] * 1.42 if lang == "en" else (m["asc"] + m["desc"]) * 1.06
    gap = sym_h * 0.30
    pad = 18
    text_h_total = m["asc"] + m["desc"]
    H = pad * 2 + max(sym_h, text_h_total)
    baseline = pad + max(sym_h, m["asc"])  # symbol bottom sits on baseline
    W = pad * 2 + SYM_W * (sym_h / SYM_H) + gap + m["w"]
    for name, v in VARIANTS.items():
        sym_x = pad
        sym = symbol_placed(sym_x, baseline - sym_h, sym_h, v["mark"], v["dot"])
        tx = pad + SYM_W * (sym_h / SYM_H) + gap
        wm = wordmark_frag(lang, tx, baseline, size, v["text"], v["ar_mark"])
        if lang == "ar":  # RTL: symbol right, wordmark left
            wm = wordmark_frag(lang, pad, baseline, size, v["text"], v["ar_mark"])
            sym = symbol_placed(pad + m["w"] + gap, baseline - sym_h, sym_h, v["mark"], v["dot"])
        write_svg(f"logos/svg/morabh-logo-horizontal-{lang}-{name}.svg", W, H, sym + wm)
    return W, H


def build_stacked(lang):
    size = 84 if lang == "en" else 78
    m = wm_metrics(lang, size)
    sym_h = 150
    gap = 34
    pad = 24
    sym_w = SYM_W * (sym_h / SYM_H)
    W = pad * 2 + max(sym_w, m["w"])
    H = pad * 2 + sym_h + gap + m["asc"] + m["desc"]
    for name, v in VARIANTS.items():
        sym = symbol_placed((W - sym_w) / 2, pad, sym_h, v["mark"], v["dot"])
        wm = wordmark_frag(lang, (W - m["w"]) / 2, pad + sym_h + gap + m["asc"],
                           size, v["text"], v["ar_mark"])
        write_svg(f"logos/svg/morabh-logo-stacked-{lang}-{name}.svg", W, H, sym + wm)


def build_bilingual_horizontal():
    en_size, ar_size = 96, 108
    me = wm_metrics("en", en_size)
    ma = wm_metrics("ar", ar_size)
    sym_h = me["asc"] * 1.42
    gap = sym_h * 0.30
    div_gap = 34
    pad = 18
    sym_w = SYM_W * (sym_h / SYM_H)
    H = pad * 2 + max(sym_h, ma["asc"] + ma["desc"])
    baseline = pad + max(sym_h, ma["asc"])
    W = pad * 2 + sym_w + gap + me["w"] + div_gap * 2 + ma["w"]
    for name, v in VARIANTS.items():
        sym = symbol_placed(pad, baseline - sym_h, sym_h, v["mark"], v["dot"])
        x = pad + sym_w + gap
        en = wordmark_frag("en", x, baseline, en_size, v["text"])
        x += me["w"] + div_gap
        div_c = v["mark"] if name in ("black", "white") else GREEN
        div = (f'<rect x="{x:.1f}" y="{baseline - me["asc"]:.1f}" width="3" '
               f'height="{me["asc"]:.1f}" rx="1.5" fill="{div_c}" opacity="0.55"/>')
        x += div_gap
        ar = wordmark_frag("ar", x, baseline, ar_size, v["text"], v["ar_mark"])
        write_svg(f"logos/svg/morabh-logo-bilingual-horizontal-{name}.svg",
                  W, H, sym + en + div + ar)


def build_bilingual_stacked():
    en_size, ar_size = 82, 86
    me = wm_metrics("en", en_size)
    ma = wm_metrics("ar", ar_size)
    sym_h = 150
    pad = 26
    sym_w = SYM_W * (sym_h / SYM_H)
    W = pad * 2 + max(sym_w, me["w"], ma["w"])
    gap1, gap2 = 34, 22
    H = pad * 2 + sym_h + gap1 + me["asc"] + gap2 + ma["asc"] + ma["desc"]
    for name, v in VARIANTS.items():
        sym = symbol_placed((W - sym_w) / 2, pad, sym_h, v["mark"], v["dot"])
        by1 = pad + sym_h + gap1 + me["asc"]
        en = wordmark_frag("en", (W - me["w"]) / 2, by1, en_size, v["text"])
        by2 = by1 + gap2 + ma["asc"]
        ar = wordmark_frag("ar", (W - ma["w"]) / 2, by2, ar_size, v["text"], v["ar_mark"])
        write_svg(f"logos/svg/morabh-logo-bilingual-stacked-{name}.svg",
                  W, H, sym + en + ar)


def build_wordmark_files():
    for lang, size in (("en", 100), ("ar", 100)):
        m = wm_metrics(lang, size)
        pad = 16
        W = pad * 2 + m["w"]
        H = pad * 2 + m["asc"] + m["desc"]
        for name, v in VARIANTS.items():
            wm = wordmark_frag(lang, pad, pad + m["asc"], size, v["text"], v["ar_mark"])
            write_svg(f"logos/svg/morabh-wordmark-{lang}-{name}.svg", W, H, wm)


def export_logo_pngs():
    svg_dir = os.path.join(BRAND, "logos", "svg")
    for f in sorted(os.listdir(svg_dir)):
        if not f.endswith(".svg"):
            continue
        base = f[:-4]
        render(f"logos/svg/{f}", f"logos/png/{base}.png", h=480)
        render(f"logos/svg/{f}", f"logos/png/{base}@2x.png", h=960)


# ---------------------------------------------------------------- app icons
def icon_frag(size, radius_ratio=0.0, symbol_scale=0.62, bg=True):
    """Rounded-square gradient icon with white symbol."""
    r = size * radius_ratio
    grad = (f'<defs><linearGradient id="ig" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{GRAD_A}"/>'
            f'<stop offset="1" stop-color="{GRAD_B}"/></linearGradient></defs>')
    parts = [grad]
    if bg:
        parts.append(f'<rect width="{size}" height="{size}" rx="{r:.1f}" fill="url(#ig)"/>')
    sh = size * symbol_scale * (SYM_H / SYM_W)  # scale by width for optical fit
    sw = size * symbol_scale
    s = sw / SYM_W
    sh = SYM_H * s
    x = (size - sw) / 2
    y = (size - sh) / 2 + size * 0.015
    parts.append(symbol_placed(x, y, sh, WHITE, GOLD))
    return "".join(parts)


def build_app_icons():
    # master square (no rounding — iOS masks it itself)
    write_svg("app-icons/morabh-app-icon-square.svg", 1024, 1024, icon_frag(1024))
    render("app-icons/morabh-app-icon-square.svg", "app-icons/ios/AppIcon-1024.png")
    # rounded preview / android legacy
    write_svg("app-icons/morabh-app-icon-rounded.svg", 1024, 1024,
              icon_frag(1024, radius_ratio=0.2237))
    render("app-icons/morabh-app-icon-rounded.svg", "app-icons/morabh-app-icon-rounded-1024.png")
    for s in (512, 192, 180):
        render("app-icons/morabh-app-icon-rounded.svg",
               f"app-icons/morabh-app-icon-rounded-{s}.png", w=s, h=s)
    # android adaptive: foreground symbol inside 66/108 safe zone, on transparent
    fg = symbol_placed((1024 - SYM_W * 0.95) / 2, (1024 - SYM_H * 0.95) / 2,
                       SYM_H * 0.95, WHITE, GOLD)
    write_svg("app-icons/android/adaptive-foreground.svg", 1024, 1024, fg)
    render("app-icons/android/adaptive-foreground.svg",
           "app-icons/android/adaptive-foreground-432.png", w=432, h=432)
    bg = (f'<defs><linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">'
          f'<stop offset="0" stop-color="{GRAD_A}"/>'
          f'<stop offset="1" stop-color="{GRAD_B}"/></linearGradient></defs>'
          f'<rect width="1024" height="1024" fill="url(#bg)"/>')
    write_svg("app-icons/android/adaptive-background.svg", 1024, 1024, bg)
    render("app-icons/android/adaptive-background.svg",
           "app-icons/android/adaptive-background-432.png", w=432, h=432)
    render("app-icons/morabh-app-icon-square.svg",
           "app-icons/android/play-store-512.png", w=512, h=512)


def build_favicons():
    # favicon: white mark on green rounded square, slightly bolder for tiny sizes
    fav_w = 512 * 0.80
    fav_h = fav_w * (SYM_H / SYM_W)
    frag = (f'<rect width="512" height="512" rx="112" fill="{GREEN}"/>'
            + symbol_placed((512 - fav_w) / 2, (512 - fav_h) / 2 + 8, fav_h, WHITE, GOLD))
    write_svg("favicon/favicon.svg", 512, 512, frag)
    for s in (16, 32, 48, 180, 192, 512):
        render("favicon/favicon.svg", f"favicon/favicon-{s}x{s}.png", w=s, h=s)
    subprocess.run(["convert",
                    os.path.join(BRAND, "favicon/favicon-16x16.png"),
                    os.path.join(BRAND, "favicon/favicon-32x32.png"),
                    os.path.join(BRAND, "favicon/favicon-48x48.png"),
                    os.path.join(BRAND, "favicon/favicon.ico")], check=True)
    # maskable PWA icon: symbol within 80% safe-zone circle, full-bleed bg
    mw = 512 * 0.56
    mh = mw * (SYM_H / SYM_W)
    frag = (f'<rect width="512" height="512" fill="{GREEN}"/>'
            + symbol_placed((512 - mw) / 2, (512 - mh) / 2 + 8, mh, WHITE, GOLD))
    write_svg("favicon/maskable.svg", 512, 512, frag)
    render("favicon/maskable.svg", "favicon/maskable-512x512.png", w=512, h=512)
    render("favicon/maskable.svg", "favicon/maskable-192x192.png", w=192, h=192)
    with open(os.path.join(BRAND, "favicon/site.webmanifest"), "w") as f:
        f.write('''{
  "name": "Morabh \\u2014 \\u0645\\u064f\\u0631\\u0627\\u0628\\u0650\\u062d",
  "short_name": "Morabh",
  "icons": [
    { "src": "/favicon-192x192.png", "sizes": "192x192", "type": "image/png" },
    { "src": "/favicon-512x512.png", "sizes": "512x512", "type": "image/png" },
    { "src": "/maskable-512x512.png", "sizes": "512x512", "type": "image/png", "purpose": "maskable" }
  ],
  "theme_color": "#0C7C5F",
  "background_color": "#F4FAF7",
  "display": "standalone"
}
''')


# ---------------------------------------------------------------- splash
def splash_frag(W, H, dark=False):
    bg = NILE if dark else COTTON
    text = WHITE if dark else NILE
    mark = WHITE if dark else GREEN
    sub = MINT if dark else GREEN_DEEP
    # stacked lockup centered slightly above optical middle
    sym_h = H * 0.115
    sym_w = SYM_W * (sym_h / SYM_H)
    en_size = H * 0.040
    ar_size = H * 0.036
    me = wm_metrics("en", en_size)
    ma = wm_metrics("ar", ar_size)
    cy = H * 0.42
    parts = [f'<rect width="{W}" height="{H}" fill="{bg}"/>']
    top = cy - (sym_h + H * 0.02 + me["asc"] + H * 0.012 + ma["asc"] + ma["desc"]) / 2
    parts.append(symbol_placed((W - sym_w) / 2, top, sym_h, mark, GOLD))
    by = top + sym_h + H * 0.02 + me["asc"]
    parts.append(wordmark_frag("en", (W - me["w"]) / 2, by, en_size, text))
    by2 = by + H * 0.012 + ma["asc"]
    parts.append(wordmark_frag("ar", (W - ma["w"]) / 2, by2, ar_size, text, GOLD))
    # footer wordarea: small tagline dots (progress) at bottom safe area
    dot_y = H * 0.88
    for i, op in enumerate((0.35, 0.6, 1.0)):
        parts.append(f'<circle cx="{W/2 + (i-1)*28:.0f}" cy="{dot_y:.0f}" r="7" '
                     f'fill="{sub}" opacity="{op}"/>')
    return "".join(parts)


def build_splash():
    for tag, dark in (("light", False), ("dark", True)):
        for W, H, label in ((1284, 2778, "ios"), (1080, 1920, "android")):
            rel = f"splash/morabh-splash-{tag}-{label}-{W}x{H}"
            write_svg(rel + ".svg", W, H, splash_frag(W, H, dark))
            render(rel + ".svg", rel + ".png")


# ---------------------------------------------------------------- social
def social_profile():
    # green gradient bg, white symbol centered inside circle-safe zone
    S = 1080
    pw = S * 0.52
    ph = pw * (SYM_H / SYM_W)
    frag = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{GRAD_A}"/>'
            f'<stop offset="1" stop-color="{GRAD_B}"/></linearGradient></defs>'
            f'<rect width="{S}" height="{S}" fill="url(#g)"/>'
            + symbol_placed((S - pw) / 2, (S - ph) / 2 + 12, ph, WHITE, GOLD))
    write_svg("social/morabh-profile-1080.svg", S, S, frag)
    render("social/morabh-profile-1080.svg", "social/morabh-profile-1080.png")
    render("social/morabh-profile-1080.svg", "social/morabh-profile-400.png", w=400, h=400)
    # light square logo tile
    sym_h = 150
    en_size, ar_size = 82, 76
    me = wm_metrics("en", en_size)
    ma = wm_metrics("ar", ar_size)
    sym_w = SYM_W * (sym_h / SYM_H)
    inner_h = sym_h + 34 + me["asc"] + 22 + ma["asc"] + ma["desc"]
    top = (512 - inner_h) / 2
    parts = [f'<rect width="512" height="512" fill="{COTTON}"/>']
    parts.append(symbol_placed((512 - sym_w) / 2, top, sym_h, GREEN, GOLD))
    by = top + sym_h + 34 + me["asc"]
    parts.append(wordmark_frag("en", (512 - me["w"]) / 2, by, en_size, NILE))
    by2 = by + 22 + ma["asc"]
    parts.append(wordmark_frag("ar", (512 - ma["w"]) / 2, by2, ar_size, NILE, GOLD))
    write_svg("social/morabh-square-light-512.svg", 512, 512, "".join(parts))
    render("social/morabh-square-light-512.svg", "social/morabh-square-light-1080.png",
           w=1080, h=1080)


def steps_motif(W, H, color, opacity=0.10):
    """Ascending rounded steps — background motif drawn from the symbol."""
    parts = [f'<g fill="{color}" opacity="{opacity}">']
    n = 5
    bw = W * 0.052
    gap = bw * 0.66
    x0 = W * 0.795
    for i in range(n):
        bh = H * (0.24 + 0.14 * i)
        x = x0 + i * (bw + gap) * 0.62
        y = H - bh + H * 0.06
        parts.append(f'<rect x="{x:.0f}" y="{y:.0f}" width="{bw:.0f}" height="{bh + H*0.2:.0f}" rx="{bw/2:.0f}"/>')
    parts.append("</g>")
    return "".join(parts)


def social_cover(W, H, name):
    en_size = H * 0.30
    ar_size = H * 0.24
    me = wm_metrics("en", en_size)
    ma = wm_metrics("ar", ar_size)
    sym_h = H * 0.44
    sym_w = SYM_W * (sym_h / SYM_H)
    grad = (f'<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="1">'
            f'<stop offset="0" stop-color="{GRAD_B}"/>'
            f'<stop offset="1" stop-color="{GRAD_A}"/></linearGradient></defs>')
    parts = [grad, f'<rect width="{W}" height="{H}" fill="url(#g)"/>',
             steps_motif(W, H, WHITE)]
    total_w = sym_w + sym_h * 0.32 + me["w"] + H * 0.14 + ma["w"]
    x = (W - total_w) / 2
    mid = H * 0.52
    parts.append(symbol_placed(x, mid - sym_h / 2, sym_h, WHITE, GOLD))
    x += sym_w + sym_h * 0.32
    baseline = mid + me["asc"] * 0.38
    parts.append(wordmark_frag("en", x, baseline, en_size, WHITE))
    x += me["w"] + H * 0.14
    parts.append(wordmark_frag("ar", x, baseline, ar_size, WHITE, GOLD))
    rel = f"social/morabh-cover-{name}-{W}x{H}"
    write_svg(rel + ".svg", W, H, "".join(parts))
    render(rel + ".svg", rel + ".png")


def build_social():
    social_profile()
    social_cover(1500, 500, "x")
    social_cover(820, 312, "facebook")
    social_cover(1584, 396, "linkedin")
    social_cover(2560, 1440, "youtube")
    social_cover(1200, 630, "og-image")


# ---------------------------------------------------------------- main
if __name__ == "__main__":
    build_symbol_files()
    build_horizontal("en")
    build_horizontal("ar")
    build_stacked("en")
    build_stacked("ar")
    build_bilingual_horizontal()
    build_bilingual_stacked()
    build_wordmark_files()
    export_logo_pngs()
    build_app_icons()
    build_favicons()
    build_splash()
    build_social()
    print("done")
