#!/usr/bin/env python3
"""Morabh brand application mockups (SVG scenes rendered to PNG).

Text uses installed Manrope / Cairo fonts; render via rsvg-convert (Pango
handles Arabic shaping). PNG outputs are the deliverable; SVGs are sources.
"""
from build import (GREEN, GREEN_DEEP, NILE, GOLD, MINT, COTTON, WHITE,
                   GRAD_A, GRAD_B, SYM_W, SYM_H,
                   symbol_placed, wordmark_frag, wm_metrics, write_svg, render)

GRAY_900, GRAY_600, GRAY_400, GRAY_200, GRAY_100 = (
    "#111827", "#4B5563", "#9CA3AF", "#E5E7EB", "#F3F4F6")

DEFS = f'''<defs>
<linearGradient id="grn" x1="0" y1="0" x2="1" y2="1">
  <stop offset="0" stop-color="{GRAD_A}"/><stop offset="1" stop-color="{GRAD_B}"/>
</linearGradient>
<filter id="soft" x="-30%" y="-30%" width="160%" height="160%">
  <feDropShadow dx="0" dy="10" stdDeviation="18" flood-color="#052E25" flood-opacity="0.14"/>
</filter>
<filter id="soft2" x="-30%" y="-30%" width="160%" height="160%">
  <feDropShadow dx="0" dy="4" stdDeviation="8" flood-color="#052E25" flood-opacity="0.10"/>
</filter>
</defs>'''


def ar(x, y, size, text, fill=NILE, weight=600, anchor="start", family="Cairo"):
    # NB: with direction="rtl", text-anchor="start" pins the RIGHT edge at x.
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}" '
            f'direction="rtl">{text}</text>')


def en(x, y, size, text, fill=NILE, weight=600, anchor="start", family="Manrope"):
    return (f'<text x="{x}" y="{y}" font-family="{family}" font-size="{size}" '
            f'font-weight="{weight}" fill="{fill}" text-anchor="{anchor}">{text}</text>')


def rrect(x, y, w, h, r, fill, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}" fill="{fill}" {extra}/>'


def mini_logo_ar(x, y, h_sym, text_color, mark_color, dot_color):
    """Small horizontal AR lockup: wordmark left of symbol (RTL)."""
    m = wm_metrics("ar", h_sym * 0.62 / 1.3)
    size = h_sym * 0.62 / 1.3 * 100 / 100
    return (symbol_placed(x, y, h_sym, mark_color, dot_color))


# ----------------------------------------------------------- phone helpers
PW, PH = 390, 844


def phone_frame(x, y, content, scale=1.0):
    """iPhone-ish frame; content is drawn in a 390x844 local space."""
    return (f'<g transform="translate({x} {y}) scale({scale})">'
            f'<rect x="-14" y="-14" width="{PW+28}" height="{PH+28}" rx="54" '
            f'fill="#0B1512" filter="url(#soft)"/>'
            f'<clipPath id="scr{x}{y}"><rect width="{PW}" height="{PH}" rx="40"/></clipPath>'
            f'<g clip-path="url(#scr{x}{y})">{content}</g>'
            f'<rect x="{PW/2-60}" y="10" width="120" height="26" rx="13" fill="#0B1512"/>'
            f'</g>')


def statusbar(color):
    return (en(28, 36, 15, "9:41", color, 700)
            + f'<g fill="{color}"><rect x="{PW-38}" y="24" width="22" height="12" rx="3" opacity="0.9"/>'
              f'<rect x="{PW-64}" y="24" width="16" height="12" rx="2" opacity="0.7"/>'
              f'<rect x="{PW-86}" y="24" width="16" height="12" rx="2" opacity="0.7"/></g>')


def screen_splash():
    parts = [rrect(0, 0, PW, PH, 0, NILE)]
    sym_h = 96
    sym_w = SYM_W * (sym_h / SYM_H)
    me = wm_metrics("en", 34)
    ma = wm_metrics("ar", 30)
    top = PH * 0.36
    parts.append(symbol_placed((PW - sym_w) / 2, top, sym_h, WHITE, GOLD))
    by = top + sym_h + 30 + me["asc"]
    parts.append(wordmark_frag("en", (PW - me["w"]) / 2, by, 34, WHITE))
    by2 = by + 12 + ma["asc"]
    parts.append(wordmark_frag("ar", (PW - ma["w"]) / 2, by2, 30, WHITE, GOLD))
    for i, op in enumerate((0.3, 0.55, 1.0)):
        parts.append(f'<circle cx="{PW/2 + (i-1)*20}" cy="{PH*0.88}" r="4.5" fill="{MINT}" opacity="{op}"/>')
    return "".join(parts) + statusbar(WHITE)


def screen_home():
    parts = [rrect(0, 0, PW, PH, 0, COTTON)]
    # header
    parts.append(f'<path d="M0 0 H{PW} V148 Q{PW/2} 178 0 148 Z" fill="url(#grn)"/>')
    sym_h = 30
    parts.append(symbol_placed(PW - 28 - SYM_W * (sym_h / SYM_H), 58, sym_h, WHITE, GOLD))
    parts.append(ar(PW - 28, 122, 21, "أهلاً بيك، أحمد", WHITE, 700))
    parts.append(en(28, 122, 13, "morabh", "#CDEDE0", 800))
    # balance / plan card
    parts.append(rrect(24, 168, PW - 48, 128, 20, WHITE, 'filter="url(#soft2)"'))
    parts.append(ar(PW - 44, 202, 14, "المتبقي من خطتك", GRAY_600, 600))
    parts.append(ar(PW - 44, 240, 26, "4,250 ج.م", NILE, 700))
    parts.append(en(44, 240, 12, "of 12,000 EGP", GRAY_400, 600))
    # progress steps (brand motif)
    for i in range(6):
        c = GREEN if i < 4 else GRAY_200
        parts.append(rrect(44 + i * 52, 262, 44, 8, 4, c))
    parts.append(ar(PW - 44, 288, 12, "٤ من ٦ أقساط مدفوعة", GREEN_DEEP, 600))
    # CTA
    parts.append(rrect(24, 316, PW - 48, 56, 16, GOLD))
    parts.append(ar(PW / 2, 352, 17, "اطلب شراء جديد", NILE, 700, "middle"))
    # section title
    parts.append(ar(PW - 28, 412, 17, "القسط الجاي", NILE, 700))
    parts.append(rrect(24, 428, PW - 48, 84, 18, WHITE, 'filter="url(#soft2)"'))
    parts.append(f'<circle cx="{PW-64}" cy="470" r="20" fill="{COTTON}"/>')
    sym_h2 = 22
    parts.append(symbol_placed(PW - 64 - SYM_W * (sym_h2 / SYM_H) / 2, 470 - sym_h2 / 2, sym_h2, GREEN, GOLD))
    parts.append(ar(PW - 100, 462, 15, "قسط شهر سبتمبر", NILE, 700))
    parts.append(ar(PW - 100, 488, 13, "الاستحقاق 5 سبتمبر 2026", GRAY_600, 500))
    parts.append(en(44, 480, 17, "2,125 EGP", GREEN_DEEP, 800))
    # orders
    parts.append(ar(PW - 28, 556, 17, "طلباتك", NILE, 700))
    rows = [("موبايل سامسونج A56", "في انتظار موافقة المتجر", GOLD),
            ("ثلاجة توشيبا 16 قدم", "تم التسليم", GREEN)]
    for i, (t, s, c) in enumerate(rows):
        y0 = 572 + i * 92
        parts.append(rrect(24, y0, PW - 48, 80, 18, WHITE, 'filter="url(#soft2)"'))
        parts.append(f'<circle cx="{PW-60}" cy="{y0+40}" r="6" fill="{c}"/>')
        parts.append(ar(PW - 84, y0 + 34, 15, t, NILE, 700))
        parts.append(ar(PW - 84, y0 + 60, 13, s, GRAY_600, 500))
    # tab bar
    parts.append(rrect(0, PH - 84, PW, 84, 0, WHITE))
    labels = ["حسابي", "المدفوعات", "طلباتي", "الرئيسية"]
    for i, l in enumerate(labels):
        xx = PW / 8 * (2 * i + 1)
        c = GREEN if i == 3 else GRAY_400
        parts.append(f'<circle cx="{xx}" cy="{PH-52}" r="10" fill="{c}" opacity="0.9"/>')
        parts.append(ar(xx, PH - 22, 11, l, c, 600, "middle"))
    return "".join(parts) + statusbar(WHITE)


def screen_schedule():
    parts = [rrect(0, 0, PW, PH, 0, COTTON)]
    parts.append(rrect(0, 0, PW, 120, 0, WHITE))
    parts.append(ar(PW / 2, 92, 19, "جدول الأقساط", NILE, 700, "middle"))
    parts.append(en(28, 92, 18, "←", GRAY_600, 600))
    # summary card
    parts.append(rrect(24, 140, PW - 48, 110, 20, NILE, 'filter="url(#soft2)"'))
    parts.append(ar(PW - 44, 176, 13, "إجمالي التكلفة — شفاف من غير مفاجآت", MINT, 600))
    parts.append(ar(PW - 44, 214, 24, "12,000 ج.م", WHITE, 700))
    parts.append(en(44, 214, 13, "0% hidden fees", GOLD, 700))
    parts.append(ar(PW - 44, 238, 12, "دفعة مقدمة 3,000 ج.م + 6 أقساط شهرية", "#BFE8D8", 500))
    rows = [("يونيو 2026", "2,125 ج.م", "paid"), ("يوليو 2026", "2,125 ج.م", "paid"),
            ("أغسطس 2026", "2,125 ج.م", "paid"), ("سبتمبر 2026", "2,125 ج.م", "due"),
            ("أكتوبر 2026", "2,125 ج.م", "next"), ("نوفمبر 2026", "2,125 ج.م", "next")]
    for i, (mth, amt, st) in enumerate(rows):
        y0 = 274 + i * 74
        parts.append(rrect(24, y0, PW - 48, 62, 16, WHITE, 'filter="url(#soft2)"'))
        if st == "paid":
            parts.append(f'<circle cx="{PW-58}" cy="{y0+31}" r="13" fill="{GREEN}"/>')
            parts.append(f'<path d="M{PW-64} {y0+31} l4 5 l8 -10" stroke="{WHITE}" stroke-width="2.6" fill="none" stroke-linecap="round" stroke-linejoin="round"/>')
        elif st == "due":
            parts.append(f'<circle cx="{PW-58}" cy="{y0+31}" r="13" fill="{GOLD}"/>')
        else:
            parts.append(f'<circle cx="{PW-58}" cy="{y0+31}" r="12" fill="none" stroke="{GRAY_200}" stroke-width="3"/>')
        parts.append(ar(PW - 86, y0 + 30, 14, mth, NILE, 700))
        lab = "مدفوع" if st == "paid" else ("مستحق دلوقتي" if st == "due" else "قادم")
        col = GREEN_DEEP if st == "paid" else (GOLD if st == "due" else GRAY_400)
        parts.append(ar(PW - 86, y0 + 50, 11, lab, col, 600))
        parts.append(en(44, y0 + 38, 15, amt.replace(" ج.م", " EGP"), GRAY_900, 700))
    # CTA
    parts.append(rrect(24, PH - 96, PW - 48, 56, 16, GREEN))
    parts.append(ar(PW / 2, PH - 60, 17, "ادفع قسط سبتمبر — إنستاباي", WHITE, 700, "middle"))
    return "".join(parts) + statusbar(NILE)


def build_app_mockup():
    W, H = 1560, 1100
    s = 1.02
    content = (f'<rect width="{W}" height="{H}" fill="#E9F2EE"/>'
               + f'<rect width="{W}" height="{H}" fill="url(#grn)" opacity="0.06"/>'
               + phone_frame(80, 100, screen_splash(), s)
               + phone_frame(575, 100, screen_home(), s)
               + phone_frame(1070, 100, screen_schedule(), s))
    write_svg("mockups/mockup-app-screens.svg", W, H, DEFS + content)
    render("mockups/mockup-app-screens.svg", "mockups/mockup-app-screens.png", w=2340)


# ----------------------------------------------------------- website
def build_web_mockup():
    W, H = 1600, 1000
    parts = [f'<rect width="{W}" height="{H}" fill="#DDE9E4"/>', DEFS]
    # browser window
    bx, by, bw, bh = 100, 80, 1400, 840
    parts.append(rrect(bx, by, bw, bh, 18, WHITE, 'filter="url(#soft)"'))
    parts.append(rrect(bx, by, bw, 52, 18, GRAY_100))
    parts.append(f'<rect x="{bx}" y="{by+34}" width="{bw}" height="18" fill="{GRAY_100}"/>')
    for i, c in enumerate(("#F87171", "#FBBF24", "#34D399")):
        parts.append(f'<circle cx="{bx+28+i*24}" cy="{by+26}" r="7" fill="{c}"/>')
    parts.append(rrect(bx + 420, by + 12, 560, 28, 14, WHITE))
    parts.append(en(bx + 700, by + 31, 13, "morabh.com.eg", GRAY_600, 600, "middle"))
    # site header with logo
    hy = by + 52
    parts.append(rrect(bx, hy, bw, 76, 0, WHITE))
    sym_h = 34
    parts.append(symbol_placed(bx + 48, hy + 20, sym_h, GREEN, GOLD))
    me = wm_metrics("en", 30)
    parts.append(wordmark_frag("en", bx + 48 + SYM_W * (sym_h / SYM_H) + 14, hy + 50, 30, NILE))
    for i, item in enumerate(["كيف يعمل", "المتاجر", "الأسعار", "الدعم"]):
        parts.append(ar(bx + bw - 340 - i * 110, hy + 47, 15, item, GRAY_600, 600, "middle"))
    parts.append(rrect(bx + bw - 190, hy + 18, 140, 40, 12, GREEN))
    parts.append(ar(bx + bw - 120, hy + 44, 14, "ابدأ دلوقتي", WHITE, 700, "middle"))
    # hero
    hero_y = hy + 76
    parts.append(f'<rect x="{bx}" y="{hero_y}" width="{bw}" height="{bh-128}" fill="{COTTON}"/>')
    parts.append(ar(bx + bw - 70, hero_y + 130, 44, "اشتري دلوقتي.", NILE, 700))
    parts.append(ar(bx + bw - 70, hero_y + 196, 44, "وقسّط بوضوح.", GREEN, 700))
    parts.append(ar(bx + bw - 70, hero_y + 252, 18, "تقسيط متوافق مع الشريعة — من غير رسوم مخفية ولا مفاجآت.", GRAY_600, 500))
    parts.append(rrect(bx + bw - 300, hero_y + 300, 230, 54, 14, GOLD))
    parts.append(ar(bx + bw - 185, hero_y + 335, 17, "اعمل طلب شراء", NILE, 700, "middle"))
    parts.append(rrect(bx + bw - 560, hero_y + 300, 230, 54, 14, "none",
                       f'stroke="{GREEN}" stroke-width="2"'))
    parts.append(ar(bx + bw - 445, hero_y + 335, 17, "لمتاجر الشركاء", GREEN_DEEP, 700, "middle"))
    # hero phone visual
    parts.append(phone_frame(bx + 130, hero_y + 90, screen_home(), 0.62))
    # trust badges
    ty = hero_y + 470
    for i, t in enumerate(["متوافق مع الشريعة", "بدون رسوم مخفية", "موافقة سريعة"]):
        xx = bx + bw - 70 - i * 280
        parts.append(f'<circle cx="{xx+18}" cy="{ty-6}" r="6" fill="{GOLD}"/>')
        parts.append(ar(xx, ty, 16, t, GREEN_DEEP, 700))
    write_svg("mockups/mockup-website.svg", W, H, "".join(parts))
    render("mockups/mockup-website.svg", "mockups/mockup-website.png", w=2400)


# ----------------------------------------------------------- print & retail
def build_business_cards():
    W, H = 1500, 950
    parts = [f'<rect width="{W}" height="{H}" fill="#E5E1D8"/>', DEFS]
    cw, ch, r = 630, 372, 22   # 85x55mm ratio
    # front (dark)
    x1, y1 = 90, 160
    parts.append(rrect(x1, y1, cw, ch, r, NILE, 'filter="url(#soft)"'))
    sym_h = 96
    sym_w = SYM_W * (sym_h / SYM_H)
    parts.append(symbol_placed(x1 + (cw - sym_w) / 2, y1 + 86, sym_h, WHITE, GOLD))
    me = wm_metrics("en", 34)
    parts.append(wordmark_frag("en", x1 + (cw - me["w"]) / 2, y1 + 240, 34, WHITE))
    ma = wm_metrics("ar", 26)
    parts.append(wordmark_frag("ar", x1 + (cw - ma["w"]) / 2, y1 + 288, 26, MINT, GOLD))
    # back (light)
    x2, y2 = 780, 420
    parts.append(rrect(x2, y2, cw, ch, r, WHITE, 'filter="url(#soft)"'))
    parts.append(f'<path d="M{x2} {y2+ch-84} h{cw} v84 a{r} {r} 0 0 1 -{r} {r} h-{cw-2*r} a{r} {r} 0 0 1 -{r} -{r} z" fill="{GREEN}" opacity="0.08"/>')
    sym_h2 = 44
    parts.append(symbol_placed(x2 + 44, y2 + 44, sym_h2, GREEN, GOLD))
    parts.append(ar(x2 + cw - 44, y2 + 80, 22, "أحمد مصطفى", NILE, 700))
    parts.append(ar(x2 + cw - 44, y2 + 112, 14, "مدير شراكات المتاجر", GRAY_600, 500))
    parts.append(en(x2 + 44, y2 + 190, 14, "ahmed@morabh.com.eg", GRAY_900, 600))
    parts.append(en(x2 + 44, y2 + 222, 14, "+20 100 234 5678", GRAY_900, 600))
    parts.append(en(x2 + 44, y2 + 254, 14, "morabh.com.eg", GREEN_DEEP, 700))
    parts.append(ar(x2 + cw - 44, y2 + 330, 13, "اشتري دلوقتي. وقسّط بوضوح.", GREEN_DEEP, 600))
    write_svg("mockups/mockup-business-cards.svg", W, H, "".join(parts))
    render("mockups/mockup-business-cards.svg", "mockups/mockup-business-cards.png", w=2250)


def build_storefront():
    W, H = 1600, 1000
    parts = [f'<rect width="{W}" height="{H}" fill="#CFD6D2"/>', DEFS]
    # wall
    parts.append(f'<rect width="{W}" height="620" fill="#E8E4DC"/>')
    parts.append(f'<rect y="620" width="{W}" height="380" fill="#B9BDb8"/>')
    # fascia sign
    parts.append(rrect(180, 90, 1240, 220, 10, NILE, 'filter="url(#soft)"'))
    sym_h = 120
    sym_w = SYM_W * (sym_h / SYM_H)
    me = wm_metrics("en", 84)
    ma = wm_metrics("ar", 92)
    total = sym_w + 40 + me["w"] + 90 + ma["w"]
    x = 180 + (1240 - total) / 2
    parts.append(symbol_placed(x, 200 - sym_h / 2 - 8, sym_h, WHITE, GOLD))
    x += sym_w + 40
    parts.append(wordmark_frag("en", x, 200 + me["asc"] * 0.38, 84, WHITE))
    x += me["w"] + 90
    parts.append(wordmark_frag("ar", x, 200 + me["asc"] * 0.38, 92, WHITE, GOLD))
    # glass door + partner sticker
    parts.append(rrect(240, 360, 420, 560, 8, "#9FB4AC", 'opacity="0.85"'))
    parts.append(rrect(250, 370, 400, 540, 6, "#C4D4CD", 'opacity="0.7"'))
    parts.append(f'<circle cx="450" cy="640" r="96" fill="{WHITE}" filter="url(#soft2)"/>')
    sh = 62
    parts.append(symbol_placed(450 - SYM_W * (sh / SYM_H) / 2, 585, sh, GREEN, GOLD))
    parts.append(ar(450, 692, 20, "قسّط هنا مع مُرابِح", NILE, 700, "middle"))
    # window poster
    parts.append(rrect(760, 380, 620, 420, 10, GREEN, 'filter="url(#soft2)"'))
    parts.append(f'<rect x="760" y="380" width="620" height="420" rx="10" fill="url(#grn)"/>')
    parts.append(ar(1330, 480, 42, "اشتري دلوقتي.", WHITE, 700))
    parts.append(ar(1330, 545, 42, "وقسّط بوضوح.", GOLD, 700))
    parts.append(ar(1330, 600, 19, "تقسيط حلال وواضح على مشترياتك", "#D3EFE3", 500))
    sh2 = 74
    parts.append(symbol_placed(816, 690, sh2, WHITE, GOLD))
    parts.append(ar(1330, 745, 22, "متجر شريك", WHITE, 700))
    write_svg("mockups/mockup-storefront.svg", W, H, "".join(parts))
    render("mockups/mockup-storefront.svg", "mockups/mockup-storefront.png", w=2400)


def build_bag():
    W, H = 1200, 1000
    parts = [f'<rect width="{W}" height="{H}" fill="#DCD8CF"/>', DEFS]
    # bag body
    bx, by, bw, bh = 400, 260, 400, 520
    parts.append(f'<path d="M{bx} {by} h{bw} l26 {bh} h-{bw+52} z" fill="{COTTON}" filter="url(#soft)"/>')
    # handles
    parts.append(f'<path d="M{bx+110} {by} q90 -130 180 0" stroke="{GREEN_DEEP}" stroke-width="14" fill="none" stroke-linecap="round"/>')
    # stacked logo on bag
    sym_h = 130
    sym_w = SYM_W * (sym_h / SYM_H)
    cx = bx + bw / 2 + 6
    parts.append(symbol_placed(cx - sym_w / 2, by + 120, sym_h, GREEN, GOLD))
    me = wm_metrics("en", 52)
    parts.append(wordmark_frag("en", cx - me["w"] / 2, by + 330, 52, NILE))
    ma = wm_metrics("ar", 42)
    parts.append(wordmark_frag("ar", cx - ma["w"] / 2, by + 395, 42, NILE, GOLD))
    parts.append(ar(cx, by + 460, 17, "اشتري دلوقتي. وقسّط بوضوح.", GREEN_DEEP, 600, "middle"))
    write_svg("mockups/mockup-shopping-bag.svg", W, H, "".join(parts))
    render("mockups/mockup-shopping-bag.svg", "mockups/mockup-shopping-bag.png", w=1800)


def build_social_post():
    S = 1080
    parts = [DEFS, f'<rect width="{S}" height="{S}" fill="url(#grn)"/>']
    # motif
    for i in range(5):
        bh = S * (0.16 + 0.1 * i)
        parts.append(f'<rect x="{S*0.76 + i*46}" y="{S - bh + 40}" width="34" height="{bh+100}" rx="17" fill="{WHITE}" opacity="0.08"/>')
    sym_h = 150
    parts.append(symbol_placed(80, 90, sym_h, WHITE, GOLD))
    parts.append(ar(S - 90, 430, 84, "اشتري دلوقتي.", WHITE, 700))
    parts.append(ar(S - 90, 560, 84, "وقسّط بوضوح.", GOLD, 700))
    parts.append(ar(S - 90, 660, 30, "تقسيط متوافق مع الشريعة — بدون رسوم مخفية", "#D3EFE3", 500))
    # CTA pill
    parts.append(rrect(S - 90 - 360, 730, 360, 92, 46, WHITE))
    parts.append(ar(S - 90 - 180, 790, 32, "حمّل التطبيق", GREEN_DEEP, 700, "middle"))
    me = wm_metrics("en", 44)
    parts.append(wordmark_frag("en", 80, S - 80, 44, WHITE))
    ma = wm_metrics("ar", 40)
    parts.append(wordmark_frag("ar", 80 + me["w"] + 50, S - 80, 40, WHITE, GOLD))
    write_svg("mockups/mockup-social-post.svg", S, S, "".join(parts))
    render("mockups/mockup-social-post.svg", "mockups/mockup-social-post.png", w=1080)


def build_notification():
    W, H = 1200, 700
    parts = [f'<rect width="{W}" height="{H}" fill="#0E2B23"/>', DEFS,
             f'<rect width="{W}" height="{H}" fill="url(#grn)" opacity="0.25"/>']
    parts.append(en(W / 2, 150, 96, "9:41", WHITE, 300, "middle"))
    parts.append(en(W / 2, 200, 22, "Tuesday, September 1", "#BFE8D8", 500, "middle"))
    # notification card
    nx, ny, nw, nh = 150, 260, 900, 150
    parts.append(rrect(nx, ny, nw, nh, 28, "rgba(255,255,255,0.96)", 'filter="url(#soft)"'))
    # app icon
    parts.append(rrect(nx + nw - 118, ny + 26, 88, 88, 22, "url(#grn)"))
    sh = 46
    parts.append(symbol_placed(nx + nw - 118 + (88 - SYM_W * (sh / SYM_H)) / 2, ny + 26 + 20, sh, WHITE, GOLD))
    parts.append(ar(nx + nw - 140, ny + 60, 24, "مُرابِح", NILE, 700))
    parts.append(en(nx + 30, ny + 58, 16, "now", GRAY_400, 500))
    parts.append(ar(nx + nw - 140, ny + 100, 20, "فاضل ٣ أيام على قسط سبتمبر — 2,125 ج.م. جاهز؟", GRAY_900, 500))
    # second notification
    ny2 = ny + 170
    parts.append(rrect(nx, ny2, nw, 120, 28, "rgba(255,255,255,0.85)"))
    parts.append(rrect(nx + nw - 106, ny2 + 22, 76, 76, 19, "url(#grn)"))
    sh2 = 40
    parts.append(symbol_placed(nx + nw - 106 + (76 - SYM_W * (sh2 / SYM_H)) / 2, ny2 + 22 + 18, sh2, WHITE, GOLD))
    parts.append(ar(nx + nw - 130, ny2 + 52, 22, "مُرابِح", NILE, 700))
    parts.append(ar(nx + nw - 130, ny2 + 90, 19, "تمت الموافقة على طلبك — راجع خطة التقسيط", GRAY_900, 500))
    write_svg("mockups/mockup-notification.svg", W, H, "".join(parts))
    render("mockups/mockup-notification.svg", "mockups/mockup-notification.png", w=1800)


if __name__ == "__main__":
    build_app_mockup()
    build_web_mockup()
    build_business_cards()
    build_storefront()
    build_bag()
    build_social_post()
    build_notification()
    print("mockups done")
