# Morabh — مُرابِح · Brand Identity

**Shop now. Pay clearly.** · **اشتري دلوقتي. وقسّط بوضوح.**

Complete visual identity for Morabh, Egypt's Sharia-compliant Buy Now, Pay Later platform.
Open **[`guidelines/index.html`](guidelines/index.html)** for the full brand presentation.

---

## The concept — "The Rising Meem"

The symbol fuses three ideas into one continuous rounded stroke:

1. **The meem head** — the circular head of **م**, first letter of **مُرابِح**, anchors the mark in Arabic.
2. **An ascending M** — the Latin monogram for **Morabh**, drawn as two rising peaks where the second
   peak is higher than the first: each installment is a step, and the journey ends higher than it began
   (from wanting → owning).
3. **The gold damma dot** — the damma (**ُ**) that crowns **مُ**, floating above the final stem as the
   moment of *gain* — the fair, transparent benefit at the heart of مُرابِح ("the one who gains").

No mosques, crescents, carts or currency signs — the brand expresses Sharia compliance through its
values: clarity, fairness and transparency.

## Color palette

| Color | HEX | RGB | CMYK | Role |
|---|---|---|---|---|
| **Morabh Green** | `#0C7C5F` | 12 124 95 | 90 0 23 51 | Primary brand color |
| **Deep Green** | `#095E48` | 9 94 72 | 90 0 23 63 | Primary 700 — AA/AAA text, hover |
| **Deep Nile** | `#052E25` | 5 46 37 | 89 0 20 82 | Dark — headlines, dark mode |
| **Prosperity Gold** | `#E9B44C` | 233 180 76 | 0 23 67 9 | Accent — damma dot, key CTAs |
| **Mint** | `#7CD9B8` | 124 217 184 | 43 0 15 15 | Secondary — highlights on dark |
| **Cotton** | `#F4FAF7` | 244 250 247 | 2 0 1 2 | Light background |
| Neutral grays | `#111827` `#4B5563` `#9CA3AF` `#E5E7EB` `#F3F4F6` `#F9FAFB` | — | — | Text & surfaces |

Key contrast pairs: Deep Nile on white **13.9:1** (AAA) · Deep Green on white **7:1** (AAA) ·
Morabh Green on white **4.6:1** (AA) · Deep Nile on Gold **7.6:1** (AAA).

## Typography

| Role | Typeface | Weights |
|---|---|---|
| English UI & headings | **Manrope** | 800 / 700 / 600 / 500 |
| Arabic display & headings | **Cairo** | 700 / 600 (matches the wordmark) |
| Arabic body & UI | **IBM Plex Sans Arabic** | 600 / 400 |
| Numbers & amounts | Manrope, tabular figures | 700–800 |

Both wordmarks ship as **outlined vectors** (no font dependency): English in customized Manrope
ExtraBold lowercase; Arabic drawn from Cairo SemiBold with the gold damma/kasra as part of the mark.

## Repository map

```
brand/
├── logos/
│   ├── svg/        Master vectors — symbol, wordmarks (EN/AR), horizontal,
│   │               stacked & bilingual lockups × color / reverse / black / white
│   └── png/        PNG exports (1x + @2x) of every logo
├── favicon/        favicon.svg + 16/32/48/180/192/512 PNG + favicon.ico
│                   + maskable PWA icons + site.webmanifest
├── app-icons/      iOS 1024 icon, Android adaptive layers, Play Store 512,
│                   rounded previews (180/192/512/1024)
├── splash/         Light & dark splash screens — iOS 1284×2778, Android 1080×1920
├── social/         Profile tiles (circle-safe), covers for X / Facebook /
│                   LinkedIn / YouTube, OG image 1200×630
├── mockups/        App screens, website, business cards, storefront,
│                   shopping bag, social post, notifications
├── guidelines/     index.html — full brand presentation & usage rules
├── fonts/          Manrope, Cairo, IBM Plex Sans Arabic (OFL licensed)
└── src/            build.py / mockups.py / textpath.py — regenerate everything
```

## Asset → channel mapping

| Need | Use |
|---|---|
| Website header (LTR / RTL) | `logos/svg/morabh-logo-horizontal-en-color.svg` / `...-ar-color.svg` |
| Compact header / footer | `logos/svg/morabh-symbol-color.svg` / `...-white.svg` |
| Browser favicon | `favicon/favicon.ico` + `favicon/favicon.svg` |
| PWA | `favicon/maskable-512x512.png` + `favicon/site.webmanifest` |
| iOS App Store | `app-icons/ios/AppIcon-1024.png` |
| Android adaptive | `app-icons/android/adaptive-foreground-432.png` + `adaptive-background-432.png` |
| Splash / launch | `splash/morabh-splash-{light,dark}-{ios,android}-*.png` |
| Social profile (all channels) | `social/morabh-profile-1080.png` |
| Social covers | `social/morabh-cover-{x,facebook,linkedin,youtube}-*.png` |
| Link previews (OG) | `social/morabh-cover-og-image-1200x630.png` |
| Documents / print | `logos/svg/morabh-logo-bilingual-horizontal-color.svg`, mono `-black` |

## Rebuilding assets

```bash
sudo apt-get install librsvg2-bin imagemagick
pip3 install uharfbuzz fonttools
cd brand/src
python3 build.py     # logos, icons, favicons, splash, social
python3 mockups.py   # application mockups (needs fonts installed: cp ../fonts/*.ttf ~/.fonts && fc-cache)
```
