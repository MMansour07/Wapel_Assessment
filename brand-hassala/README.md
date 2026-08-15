# Morabh — مُرابِح · The Glass Hassala Identity

**The mark:** a transparent Egyptian hassala (حصّالة) money box — drawn as an open outline
vessel with the saved coins **visible inside**, and the next coin — the halal gain, in
Sharia green — dropping in through the open slot.

Open **`splash/morabh-splash-animated-preview.html`** to watch the animated splash
(click the phone to replay). GIF preview: `splash/morabh-splash-animated-preview.gif`.

---

## Why this shape

1. **Saving, from the user's side.** The hassala is the saving object every Egyptian
   home already owns — instantly clear, warm, and local. No explanation needed.
2. **The "glass" is the insight.** A clay hassala hides your money until you break it.
   Morabh's hassala is transparent — *you always see what's inside*: your plan, your
   paid installments, your remaining balance. Transparency is drawn into the logo itself.
3. **Halal by nature.** It's the culture's own alternative to the (haram) piggy bank,
   and the green dropping coin is the gain that stays Sharia-compliant — values shown
   through form, not religious symbols.
4. **It's openable.** The vessel is open at the top — your money isn't locked away or
   hidden behind procedures.
5. **Born animated.** Every element is an animation step: the vessel draws itself,
   the saved coins land, the green gain drops in. Logo, loading state and payment-success
   moment are all the same shape.
6. **Unique next to Takka.** Takka (the direct Sharia-compliant competitor) owns *speed*
   ("a click") with a bold wordmark; Morabh owns *keeping, seeing and growing* with a
   pictorial mark no other regional fintech uses.

## The animation (≈2.8 s + looping loader)

1. **0.15 s** — the base line draws
2. **0.50 s** — the two shoulders rise (the vessel builds itself, dash-offset)
3. **1.00 / 1.28 s** — the two saved coins land inside with a soft spring
4. **1.62 s** — the green gain-coin drops through the slot
5. **1.90 s** — "morabh" renders letter by letter in `#6C8DDF`
6. **2.15 s** — مُرابِح renders glyph by glyph in reading order, green diacritics last
7. **2.65 s** — three loader dots pulse until the app is ready

`morabh-splash-animated.svg` is self-contained: CSS-only, no JavaScript, no font files
(all text outlined), and `prefers-reduced-motion` shows the finished lockup instantly.

## Color system (app palette)

| Element | Light surface | Dark / blue surface |
|---|---|---|
| Vessel + saved coins | Primary `#33509C` | White |
| Dropping gain-coin | Sharia green `#074D31` | Gold `#F1DC84` |
| Wordmark (logos) | `#33509C` | White |
| Wordmark (splash/display) | `#6C8DDF` | White |

**Small-size note:** below ~48 px the glass outline closes up, so the favicon set uses the
**solid** hassala silhouette (white dome, slot, gold coin on primary blue) — same object,
simplified. This is intentional and standard practice (icon simplification).

## Folder map

```
brand-hassala/
├── logos/svg + png     symbol, EN/AR wordmarks, horizontal / stacked / bilingual
│                       lockups × color / reverse / black / white
├── favicon/            simplified solid mark — favicon.svg, 16–512 px, .ico, maskable
├── app-icons/          iOS 1024, Android adaptive layers, Play Store 512
├── splash/             static light/dark (iOS 1284×2778, Android 1080×1920)
│                       + morabh-splash-animated.svg / -preview.html / -preview.gif
└── social/             profile 1080 (circle-safe), covers X/FB/LinkedIn/YouTube, OG image
```

Fonts (Manrope, Cairo, IBM Plex Sans Arabic — OFL) are in `../brand/fonts/`.

Regenerate everything: `cd brand/src && python3 build_hassala.py`

## Concept exploration trail

- `concepts/hassala/` — the four hassala variants (solid, installment-arc, glass, glass+drop)
- `concepts/samples/` — the earlier saving/halal-gain directions in separated folders
