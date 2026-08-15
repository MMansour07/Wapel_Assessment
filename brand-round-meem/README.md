# Morabh — مرابح · The Round Meem (from your reference)

Vector reconstruction of the uploaded symbol: a rounded **م** — ring head, hanging tail,
and a **drop** at the tip. The drop is the brand accent: merged white in the light
gradient version, **teal (`#2BB39F`) as "the gain"** on dark surfaces.

Open **`splash/splash-animated-preview.html`** to watch both splash versions
(click a phone to replay). GIFs: `splash/splash-animated-{light,dark}-preview.gif`.

---

## Colors (sampled from the reference)

| Role | Value |
|---|---|
| Gradient (light splash / icons) | `#4A90D8` → `#2AB3A6` |
| Dark background | `#0D1B26` + teal glow at 10% |
| Symbol / wordmark | White |
| Gain drop (dark + color-on-white versions) | `#2BB39F` |
| Arabic wordmark | White at 75% (as in reference) |

## The splash animation

1. **0.20 s** — the ring draws itself (the meem head)
2. **0.85 s** — the tail extends downward
3. **1.25 s** — the drop falls in with a spring — the gain lands
4. **1.60 s** — **Morabh** renders letter by letter
5. **2.05 s** — **مرابح** renders glyph by glyph (م first)
6. **2.55 s** — loader dots pulse until the app is ready

CSS-only SVG (no JS, no font files — all outlines), honors `prefers-reduced-motion`,
verified in headless Chrome. Light and dark versions included.

## Folder map

```
brand-round-meem/
├── logo/          symbol (gradient tile, dark tile, teal-on-white, black)
│                  + stacked gradient lockup (symbol / Morabh / مرابح)
├── app-icons/     iOS 1024, rounded 180/192/512/1024, dark alt,
│                  Android adaptive layers (gradient background)
├── favicon/       gradient favicons 16–512 + favicon.ico + maskable
└── splash/        static light/dark (1284×2778, 1080×1920)
                   + animated SVG light/dark + HTML preview + GIFs
```

Regenerate: `cd brand/src && python3 build_round_meem.py`
