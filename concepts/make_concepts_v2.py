#!/usr/bin/env python3
"""Morabh symbol exploration v2 — insight-first, radically simple.

Each mark is built on an idea only a Sharia-compliant BNPL can own,
reduced to 1-3 geometric elements.
"""
import os
import subprocess

BLUE = "#33509C"
TINT = "#A2BCFF"
GREEN = "#074D31"
GOLD = "#E9C25C"
HERE = os.path.dirname(os.path.abspath(__file__))

S = 'fill="none" stroke="#33509C" stroke-width="54" stroke-linecap="round" stroke-linejoin="round"'


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
            f'width="512" height="512"><rect width="512" height="512" fill="#ffffff"/>{body}</svg>')


CONCEPTS = {}

# A — The Pause-Up: pause icon (= pay LATER) whose second bar steps UP (= gain).
#     Also reads as a fair "equals" rotated, and the two stems of M/م reduced to minimum.
CONCEPTS["v2-A-pause-up"] = svg(
    f'<rect x="152" y="212" width="76" height="216" rx="38" fill="{BLUE}"/>'
    f'<rect x="288" y="92" width="76" height="216" rx="38" fill="{BLUE}"/>'
    f'<circle cx="326" cy="418" r="30" fill="{GREEN}"/>')

# B — The Rising Equals: the "=" of fairness tilted upward — equality that grows.
CONCEPTS["v2-B-rising-equals"] = svg(
    f'<g {S}>'
    f'<path d="M 106 330 L 356 216"/>'
    f'<path d="M 156 432 L 406 318"/>'
    f'</g>'
    f'<circle cx="416" cy="128" r="30" fill="{GREEN}"/>')

# C — The Ellipsis Rising: "to be continued..." = later. Each dot an installment,
#     growing in value; the last one is the gain.
CONCEPTS["v2-C-ellipsis-rising"] = svg(
    f'<circle cx="118" cy="392" r="42" fill="{BLUE}"/>'
    f'<circle cx="256" cy="300" r="56" fill="{BLUE}"/>'
    f'<circle cx="404" cy="184" r="72" fill="{GREEN}"/>')

# D — The Half-Now Coin: solid = paid now, tint = later — the plan made visible.
CONCEPTS["v2-D-half-now"] = svg(
    f'<path d="M 256 96 A 160 160 0 0 0 256 416 Z" fill="{BLUE}"/>'
    f'<path d="M 256 96 A 160 160 0 0 1 256 416 Z" fill="{TINT}"/>'
    f'<circle cx="256" cy="52" r="26" fill="{GREEN}"/>')

# E — The Kashida Steps: Arabic-typographic insight — the kashida (ـــ) stretches a
#     word the way Morabh stretches a payment; here the meem's tail extends in steps.
CONCEPTS["v2-E-kashida-steps"] = svg(
    f'<g {S}>'
    f'<circle cx="392" cy="330" r="58"/>'
    f'<path d="M 348 368 H 268 V 290 H 188 V 212 H 108"/>'
    f'</g>'
    f'<circle cx="392" cy="212" r="26" fill="{GREEN}"/>')

# F — The Quarter Coin: down payment made visible — one solid quarter, the rest tint.
CONCEPTS["v2-F-quarter-now"] = svg(
    f'<circle cx="256" cy="256" r="160" fill="{TINT}"/>'
    f'<path d="M 256 256 L 256 96 A 160 160 0 0 1 416 256 Z" fill="{BLUE}"/>'
    f'<circle cx="256" cy="256" r="44" fill="#ffffff"/>')

LABELS = {
    "v2-A-pause-up": "A · Pause-Up (later, rising)",
    "v2-B-rising-equals": "B · Rising Equals (fairness grows)",
    "v2-C-ellipsis-rising": "C · Ellipsis Rising (to be continued)",
    "v2-D-half-now": "D · Half-Now Coin (paid / later)",
    "v2-E-kashida-steps": "E · Kashida Steps (extend the time)",
    "v2-F-quarter-now": "F · Quarter-Now Coin (down payment)",
}

if __name__ == "__main__":
    for name, doc in CONCEPTS.items():
        p = os.path.join(HERE, name + ".svg")
        with open(p, "w") as f:
            f.write(doc)
        subprocess.run(["rsvg-convert", "-w", "512", p, "-o",
                        os.path.join(HERE, name + ".png")], check=True)
    print("v2 rendered:", len(CONCEPTS))
