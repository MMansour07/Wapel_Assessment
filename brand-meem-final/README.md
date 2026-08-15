# Morabh — مُرابِح · Final Meem Kit (Light + Dark, Mobile + Web)

The round meem symbol (ring + tail + drop) in a clean two-theme system — **no gradients**:

| Theme | Background | Symbol & text |
|---|---|---|
| Light | White `#FFFFFF` | `#6C8DDF` |
| Dark | `#0D1B26` | White |

**Typography: Cairo for both scripts.** مُرابِح is set in Cairo SemiBold and **Morabh in
Cairo Bold (Latin)** — Cairo's Latin was designed to harmonize with its Arabic, so the two
wordmarks share one voice. All text ships as outlined vectors (no font dependency).

Open **`splash/preview.html`** to watch all four splash animations side by side
(click a phone to replay).

---

## The two splash choreographies (per theme)

**A — Symbol only** (`splash-symbol-only-*`): the ring draws itself, the tail extends,
the drop lands. Loader dots. Nothing else.

**B — Full sequence** (`splash-full-*`), exactly as briefed:

1. **0.2 s** — the symbol renders big, centered (ring → tail → drop)
2. **1.95 s** — it **shrinks and glides down**, docking inline to the right of **مُرابِح**
   (correct RTL: the symbol leads the Arabic line) as the word fades in
3. **3.45 s** — مُرابِح hides; the symbol **slides to lead the English line** and
   **Morabh** appears inline beside it
4. **4.15 s** — loader dots pulse until the app is ready

Both are CSS-only SVGs (no JS, no fonts), honor `prefers-reduced-motion`
(reduced motion shows the final English lockup immediately), verified in headless Chrome.
Each also ships as static PNG (1284×2778 iOS, 1080×1920 Android) + GIF preview.

## Folder map

```
brand-meem-final/
├── logo/          symbol-{light,dark}.svg/png (transparent)
│                  lockup-inline-{en,ar}-{light,dark} — Cairo wordmarks
├── app-icons/     light/ + dark/: 26 sizes (16→1024, all iOS slots)
│                  + Android adaptive foreground/background layers
├── favicon/       favicon.svg — ADAPTIVE (follows prefers-color-scheme)
│                  light/ + dark/: 13 sizes + favicon.ico + apple-touch + maskable
│                  snippet.html — paste-ready <head> tags
├── navbar/        symbol-only: navbar-light (#6C8DDF) + navbar-dark (white), 10 sizes
├── web/           header lockups EN/AR × light/dark at h24–h256
└── splash/        light/ + dark/: symbol-only + full choreography
                   (animated SVG, static PNGs, GIF) + preview.html
```

## Usage notes

- **Adaptive favicon**: `favicon/favicon.svg` switches `#6C8DDF` ⇄ white automatically with
  the OS/browser theme; the PNG/ICO fallbacks are in `light/` (use `dark/` variants only if
  you control the surface behind them).
- **Navbar**: use `navbar-light-*.png` on white surfaces, `navbar-dark-*.png` on `#0D1B26`.
- `#6C8DDF` on white is display-level contrast (≈3.2:1) — right for logos and splash;
  keep body text in your darker primaries.

Regenerate: `cd brand/src && python3 build_meem_final.py`
