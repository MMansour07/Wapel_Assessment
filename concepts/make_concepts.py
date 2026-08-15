#!/usr/bin/env python3
"""Morabh symbol exploration — 10 concept drafts on one sheet.

Consistent construction: 512x512 box, primary #33509C strokes (54 w, round
caps/joins), Sharia-green #074D31 gain-dot, gold only where noted.
"""
import os
import subprocess

BLUE = "#33509C"
GREEN = "#074D31"
GOLD = "#E9C25C"
HERE = os.path.dirname(os.path.abspath(__file__))

S = 'fill="none" stroke="#33509C" stroke-width="54" stroke-linecap="round" stroke-linejoin="round"'


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
            f'width="512" height="512"><rect width="512" height="512" fill="#ffffff"/>{body}</svg>')


CONCEPTS = {}

# 1 — The Rising Meem (current)
CONCEPTS["01-rising-meem"] = svg(
    f'<g {S}><circle cx="132" cy="363" r="62"/>'
    f'<path d="M 178 321 L 262 229 L 340 325 L 442 161 L 442 427"/></g>'
    f'<circle cx="442" cy="85" r="27" fill="{GREEN}"/>')

# 2 — The Step Path: one folded ribbon staircase + damma at the summit
CONCEPTS["02-step-path"] = svg(
    f'<g {S}><path d="M 70 424 H 190 V 306 H 310 V 188 H 430"/></g>'
    f'<circle cx="430" cy="112" r="27" fill="{GREEN}"/>')

# 3 — The Meem Key: meem head as bow, rising shaft, two installment teeth
CONCEPTS["03-meem-key"] = svg(
    f'<g {S}><circle cx="148" cy="364" r="62"/>'
    f'<path d="M 194 318 L 408 104"/>'
    f'<path d="M 300 212 L 344 256"/>'
    f'<path d="M 366 146 L 410 190"/></g>')

# 4 — The Transparent Coin: total split into equal visible parts, one part = the gain
CONCEPTS["04-transparent-coin"] = svg(
    f'<g fill="none" stroke-width="58" stroke-linecap="round">'
    f'<path d="M 256 106 A 150 150 0 0 1 385 180" stroke="{GREEN}"/>'
    f'<path d="M 402 218 A 150 150 0 0 1 366 372" stroke="#33509C"/>'
    f'<path d="M 334 398 A 150 150 0 0 1 178 398" stroke="#33509C"/>'
    f'<path d="M 146 372 A 150 150 0 0 1 110 218" stroke="#33509C"/>'
    f'<path d="M 127 180 A 150 150 0 0 1 218 111" stroke="#33509C"/>'
    f'</g>')

# 5 — The Scale Dot: two ledger lines balanced under the gain
CONCEPTS["05-scale-dot"] = svg(
    f'<g {S}><path d="M 116 306 H 396"/><path d="M 166 396 H 346"/></g>'
    f'<circle cx="256" cy="196" r="34" fill="{GREEN}"/>')

# 6 — The Handshake Loop: two hooks interlocking (negative space hints at meem)
CONCEPTS["06-handshake-loop"] = svg(
    f'<g {S}>'
    f'<path d="M 96 200 H 236 A 62 62 0 0 1 298 262 V 312"/>'
    f'<path d="M 416 312 H 276 A 62 62 0 0 1 214 250 V 200"/>'
    f'</g>')

# 7 — The Growing Seed: meem seed, rising stem, gain as fruit
CONCEPTS["07-growing-seed"] = svg(
    f'<g {S}><circle cx="256" cy="380" r="58"/>'
    f'<path d="M 256 322 C 256 250 300 226 316 170"/>'
    f'<path d="M 268 260 C 214 250 196 216 196 174"/></g>'
    f'<circle cx="330" cy="106" r="27" fill="{GREEN}"/>')

# 8 — The Open Door: geometric threshold with the path rising through it
CONCEPTS["08-open-door"] = svg(
    f'<g {S}>'
    f'<path d="M 128 434 V 176 A 60 60 0 0 1 188 116 H 324 A 60 60 0 0 1 384 176 V 236"/>'
    f'<path d="M 60 388 L 256 306 L 384 342"/>'
    f'</g>'
    f'<circle cx="448" cy="300" r="27" fill="{GREEN}"/>')

# 9 — The Progress Ring + Damma: the dot completes the plan (reads as م)
CONCEPTS["09-progress-ring"] = svg(
    f'<g fill="none" stroke="#33509C" stroke-width="60" stroke-linecap="round">'
    f'<path d="M 348 130 A 156 156 0 1 0 398 208"/></g>'
    f'<circle cx="404" cy="130" r="34" fill="{GREEN}"/>')

# 10 — The Ascending Tick: approval that keeps rising
CONCEPTS["10-ascending-tick"] = svg(
    f'<g {S}><path d="M 96 296 L 208 408 L 420 130"/></g>'
    f'<circle cx="446" cy="66" r="27" fill="{GREEN}"/>')

LABELS = {
    "01-rising-meem": "1 · Rising Meem (current)",
    "02-step-path": "2 · Step Path",
    "03-meem-key": "3 · Meem Key",
    "04-transparent-coin": "4 · Transparent Coin",
    "05-scale-dot": "5 · Scale Dot",
    "06-handshake-loop": "6 · Handshake Loop",
    "07-growing-seed": "7 · Growing Seed",
    "08-open-door": "8 · Open Door",
    "09-progress-ring": "9 · Progress Ring + Damma",
    "10-ascending-tick": "10 · Ascending Tick",
}

if __name__ == "__main__":
    for name, doc in CONCEPTS.items():
        p = os.path.join(HERE, name + ".svg")
        with open(p, "w") as f:
            f.write(doc)
        subprocess.run(["rsvg-convert", "-w", "512", p, "-o",
                        os.path.join(HERE, name + ".png")], check=True)
    print("concepts rendered:", len(CONCEPTS))
