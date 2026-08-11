# Morabh — مُرابِح · Brand Identity (Blue / App Color System)

The complete Morabh identity re-themed onto the product's blue color system, plus an
**animated splash** that "renders" the brand while the app opens.

Open **`splash/morabh-splash-animated-preview.html`** in any browser to watch the splash animation
(click the phone to replay). A GIF preview is at `splash/morabh-splash-animated-preview.gif`.

---

## The idea

The symbol is unchanged — **"The Rising Meem"**: one continuous stroke that starts as the head of
**م** (first letter of مُرابِح), rises as an ascending Latin **M** whose second peak ends higher than
the first (installments as steps toward ownership), crowned by the floating dot — the *damma* of
**مُ** and the moment of gain.

What changes in this theme is the color story:

| Element | On white / light | On blue / dark |
|---|---|---|
| Mark stroke | Primary `#33509C` | White |
| Gain-dot + Arabic diacritics | **Sharia green `#074D31`** | **Gold `#F1DC84`** |
| Wordmark (logos) | Primary `#33509C` | White |
| Wordmark (splash / display) | **Primary light `#6C8DDF`** | White |

**Why the dot flips color:** your gold `#F1DC84` is a pastel — on white it is nearly invisible
(≈1.4:1 contrast), but on blue surfaces it glows. On light backgrounds the dot instead takes the
SA/Sharia green `#074D31` — a quiet, deliberate signal that *the gain is halal*. One mark, two
moods: **green gain on light, golden gain on dark.**

**The splash background** stays white-based as requested, made "creative" with three soft radial
washes drawn from the palette tints — `#DEE7FF` (primary 25), `#E3FFF9` (mint tint), `#FFEEAA`
(gold tint) — plus a whisper of the ascending-steps motif in the bottom corner. It reads premium
and airy while keeping the logo as the only focal point.

## The splash animation (how it "renders")

Timeline (~2.8 s, then the loader loops):

1. **0.15 s — the meem head draws itself** (ring stroke, dash-offset animation)
2. **0.55 s — the line rises** through both peaks up to the final stem
3. **1.35 s — the damma dot drops in** with a spring overshoot — the "gain" lands
4. **1.55 s — "morabh" renders letter by letter** (rise + fade, left to right) in `#6C8DDF`
5. **1.80 s — مُرابِح renders glyph by glyph in reading order** (م first, right to left),
   with the green diacritics popping in last
6. **2.30 s — three loader dots pulse** until the app is ready

Files:

- `splash/morabh-splash-animated.svg` — self-contained animated SVG (CSS animations, no JS,
  no font dependency — all text is outlined vector). Respects `prefers-reduced-motion`
  (shows the finished lockup instantly).
- `splash/morabh-splash-animated-preview.html` — phone-frame preview, click to replay
- `splash/morabh-splash-animated-preview.gif` — video preview of the sequence
- `splash/morabh-splash-{light,dark}-*.png/svg` — static splash (iOS 1284×2778, Android 1080×1920)

## Palette reference

| Role | Hex |
|---|---|
| Primary / main text | `#33509C` |
| Hover | `#1F3B82` · Pressed `#294387` |
| Dark surface | `#122F78` |
| Primary 400 / 200 | `#5A7CD4` / `#7798EB` |
| Primary light text | `#6C8DDF` |
| Primary 50 / 25 | `#A2BCFF` / `#DEE7FF` |
| Secondary (mint) | `#A3FFED` · tint `#E3FFF9` |
| Tertiary (gold) | `#F1DC84` · tint `#FFEEAA` |
| SA / Sharia green | `#074D31` |
| Success / Info / Warning / Error | `#079455` / `#1570EF` / `#DC6803` / `#D92D20` |

## Insights & recommendations

1. **`#6C8DDF` is a display color, not a body color.** On white it measures ≈3.2:1 — passes WCAG AA
   only for large text (≥24 px, or ≥19 px bold). Use it for the wordmark, hero headlines and big
   numbers; keep body copy and small UI labels in `#33509C` (≈7.6:1, AAA) or `#122F78`.
2. **Never place `#F1DC84` or `#A3FFED` on white** for anything meaningful — both are tints
   (≈1.3–1.4:1). Use them on `#33509C`/`#122F78` surfaces, or use their `-tint` values as
   *backgrounds* with dark text on top.
3. **The dual-color gain-dot is a feature, not a compromise** — it gives the brand a light-mode and
   dark-mode personality while both stay on-palette. Keep it consistent: green dot ⇢ light surface,
   gold dot ⇢ dark/colored surface. (Mono black/white logos are unaffected.)
4. **Native splash screens can't animate.** iOS launch screens and Android 12+ splash are static by
   OS design. The pattern that feels animated: show the **static** splash (provided) natively, then
   render the **animated SVG** as the first in-app frame — the transition is seamless because both
   share the same layout and background. In Flutter use `flutter_svg`+Rive/Lottie or a WebView;
   in React Native use `react-native-svg` (the CSS animations also run as-is in any WebView).
5. **The animated SVG needs no fonts and no JS** — wordmarks are outlined paths, so it renders
   identically everywhere, including airplane-mode first launches.
6. **Semantic colors stay reserved**: success `#079455`, info `#1570EF`, warning `#DC6803`, error
   `#D92D20` should never be used decoratively, so payment states stay instantly readable.
7. If you later want a Lottie/`.json` version for Android's animated vector splash, the same
   timeline (draw ring → rise → dot → letters) ports 1:1 — the SVG structure was built with that
   in mind (each glyph is a separate node).

## Folder map

```
brand-blue/
├── logos/svg + png     symbol, EN/AR wordmarks, horizontal / stacked / bilingual
│                       lockups × color / reverse / black / white
├── favicon/            favicon.svg, 16–512 px PNG, favicon.ico, maskable, webmanifest
├── app-icons/          iOS 1024, Android adaptive layers, Play Store 512, rounded previews
├── splash/             static light/dark (iOS + Android) + ANIMATED svg/html/gif
├── social/             profile 1080 (circle-safe), covers X/FB/LinkedIn/YouTube, OG image
└── fonts/              Manrope, Cairo, IBM Plex Sans Arabic (OFL)
```

Regenerate everything: `cd brand/src && python3 build_blue.py`
