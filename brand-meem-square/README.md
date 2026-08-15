# Morabh — مُرابِح · The Square Meem (مربع) Identity

A custom **square-Kufic (مربع-style) م** drawn from scratch — letter in `#6C8DDF` on the
`#DEE7FF` tint background.

Open **`splash/splash-animated-preview.html`** to watch the splash build itself
(click the phone to replay). GIF preview: `splash/splash-animated-preview.gif`.

---

## The two creative touches

1. **The staircase inside the square.** The meem's square counter isn't empty — it holds
   three steps rising toward the top-right corner: *the installments live inside the
   money-letter*. It's a hidden-detail mark (FedEx-arrow style): once seen, never unseen.
2. **The damma is a miniature meem.** Instead of a generic accent, the damma above the
   letter is the letter itself, shrunk — *a small gain that grows into a big one* — in
   Sharia green `#074D31` (gold on dark surfaces).

## Structure

| Piece | Meaning |
|---|---|
| Square head (مربع) | Stability, structure, fairness |
| Steps in the counter | Installments — the journey inside the money |
| L-tail | The letter grounded — trust |
| Mini-meem damma | The gain (green = halal) |

## The splash (per the brief: letter renders, then the words, all inside a rectangle)

1. **0.10 s** — the card rectangle rises
2. **0.45 s** — the square head appears
3. **0.85 s** — the three steps slide in, one per installment
4. **1.30 s** — the tail drops and grounds the letter
5. **1.55 s** — the mini-meem damma springs in from above
6. **1.85 s** — **مُرابِح** renders glyph by glyph (م first), green diacritics last
7. **2.20 s** — **morabh** renders letter by letter in `#6C8DDF`
8. **2.70 s** — loader dots pulse until the app is ready

`splash-animated.svg` is CSS-only (no JS, no font files — all outlines),
honors `prefers-reduced-motion`, and was verified in headless Chrome.

## Folder map

```
brand-meem-square/
├── logo/          meem-square (transparent + tile), lockup-horizontal:
│                  the letter beside مُرابِح over Morabh, inline-centered
├── app-icons/     LETTER-ONLY icons: iOS 1024, rounded 180/192/512/1024,
│                  dark alt, Android adaptive layers
├── favicon/       letter-only favicons 16–512 + favicon.ico + maskable
│                  (simplified: no steps below 48 px, white on #6C8DDF for contrast)
└── splash/        static (1284×2778, 1080×1920) + animated SVG/HTML/GIF
```

## Color notes

- Letter `#6C8DDF` on `#DEE7FF` is a soft, airy pairing (≈2.6:1) — perfect for splash
  and brand moments; the favicon flips to **white letter on `#6C8DDF`** so it stays
  crisp at 16 px.
- Arabic wordmark `#33509C` (strong), English `#6C8DDF` (light) — hierarchy with
  the Arabic leading, as an Egyptian brand should.

Regenerate: `cd brand/src && python3 build_meem_square.py`
