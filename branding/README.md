# Morabh — مُرابِح · Meem Smile Branding (Final)

Primary brand mark: **the Meem Smile** — the meem ring, a smile swoosh tail, and the
gain dot. Flat, modern, no gradients.

**Typography:** Arabic — **Cairo** (SemiBold). English — **Cairo's companion Latin**
(Bold): same family, identical weight logic and geometric proportions, available on web
and mobile, so مُرابِح and Morabh speak with one voice. All wordmarks are outlined
vectors — no font files needed at runtime.

**Themes** (no gradients, ever):

| Theme | Background | Symbol & text |
|---|---|---|
| Light | White | `#6C8DDF` |
| Dark | `#0D1B26` | White |

Open **`splash/preview.html`** to watch the mobile + web splash animations in both
themes (click to replay).

---

## Splash choreography — Symbol → Symbol + مُرابِح → Symbol + Morabh

| Time | Stage |
|---|---|
| 0.10 s | **Stage 1** — Meem Smile fades/scales in (0.92→1.0), centered |
| 1.00 s | **Stage 2** — symbol scales down and glides into its inline position |
| 1.42 s | مُرابِح reveals beside it (soft fade + 6 px rise) |
| 2.45 s | **Stage 3** — Arabic fades out; the symbol does not move |
| 2.72 s | Morabh fades in at the same spot |
| ~3.6 s | Hand off to the application |

Smooth `cubic-bezier(.4,0,.2,1)` easing throughout — no bounce, no particles, no
effects. CSS-only SVG (no JS, no fonts), honors `prefers-reduced-motion` (renders the
final English lockup instantly). Verified in headless Chrome.

## Structure

```
branding/
├── logo/
│   ├── light/  morabh-symbol.svg/png · morabh-ar.svg/png · morabh-en.svg/png
│   └── dark/   (same, white marks — transparent backgrounds)
├── splash/
│   ├── light/  symbol.svg · arabic.svg · english.svg   (stage frames)
│   │           morabh-splash-animated-mobile.svg · -web.svg
│   │           static PNGs 1284×2778 + 1080×1920 · preview GIF
│   ├── dark/   (same)
│   └── preview.html
├── mobile/
│   ├── ios/{light,dark}/      AppIcon 20→1024 (13 sizes) + master SVG
│   └── android/{light,dark}/  ic_launcher 36→512 + adaptive fg/bg layers
└── web/
    ├── favicon/  morabh-favicon.svg (THEME-ADAPTIVE via prefers-color-scheme)
    │             {light,dark}/ 9 PNG sizes + favicon.ico · snippet.html
    └── logo/{light,dark}/  header EN/AR h24–h128 + responsive symbol h20–h64
```

## Usage notes

- **App icon = symbol only** (per brief) — the wordmark never appears in launcher icons.
- **Native splash**: ship the static `symbol` stage as the OS launch screen, then play
  the animated SVG as the app's first frame — the transition is seamless.
- `web/favicon/morabh-favicon.svg` switches `#6C8DDF` ⇄ white automatically with the
  browser theme; `snippet.html` has paste-ready `<head>` tags.
- At sizes below 20 px prefer the symbol-only PNGs (the smile stays readable; the dot
  is preserved down to 16 px).

Regenerate everything: `cd brand/src && python3 build_meem_smile.py`
