#!/usr/bin/env python3
"""Morabh — playful round symbol exploration (Souhoola-inspired softness).

Friendly, rounded, continuous shapes built on the م. All #6C8DDF on white.
Samples only.
"""
import os
import subprocess

LIGHT = "#6C8DDF"
WHITE = "#FFFFFF"
HERE = os.path.dirname(os.path.abspath(__file__))
OUTD = os.path.join(HERE, "souhoola-style")

S = f'fill="none" stroke="{LIGHT}" stroke-width="48" stroke-linecap="round" stroke-linejoin="round"'


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
            f'width="512" height="512"><rect width="512" height="512" fill="{WHITE}"/>{body}</svg>')


V = {}

# A — Meem Smile: the meem's tail swings into a smile swoosh
V["A-meem-smile"] = svg(
    f'<g {S}><circle cx="196" cy="192" r="68"/>'
    f'<path d="M 166 254 C 130 360, 220 420, 310 408 C 372 400, 412 366, 428 322"/></g>'
    f'<circle cx="442" cy="272" r="26" fill="{LIGHT}"/>')

# B — Loop Meem: one continuous flourish — ring, underhand loop, rising exit
V["B-loop-meem"] = svg(
    f'<g {S}><circle cx="190" cy="200" r="66"/>'
    f'<path d="M 165 261 C 140 340, 180 392, 250 392 C 310 392, 330 340, 296 322 '
    f'C 262 304, 232 340, 262 372 C 290 402, 360 396, 408 348"/></g>')

# C — Bubble Meem: the م as a chat bubble (we speak your language)
V["C-bubble-meem"] = svg(
    f'<g {S}><circle cx="256" cy="230" r="110"/>'
    f'<path d="M 190 330 L 168 400 L 250 356"/></g>'
    f'<circle cx="256" cy="230" r="34" fill="{LIGHT}"/>')

# D — Coin Smile: happy money — coin with a smile, gain-dot as the dimple
V["D-coin-smile"] = svg(
    f'<circle cx="256" cy="236" r="148" fill="{LIGHT}"/>'
    f'<path d="M 192 262 Q 256 322 320 262" fill="none" stroke="{WHITE}" '
    f'stroke-width="32" stroke-linecap="round"/>'
    f'<circle cx="392" cy="384" r="28" fill="{LIGHT}"/>')

# E — Rising Bubbles: the meem head releasing gain-bubbles upward
V["E-rising-bubbles"] = svg(
    f'<g {S}><circle cx="208" cy="300" r="88"/></g>'
    f'<circle cx="330" cy="196" r="44" fill="{LIGHT}"/>'
    f'<circle cx="404" cy="112" r="24" fill="{LIGHT}"/>')

# F — Spring Meem: the tail bounces — playful drop on its way
V["F-spring-meem"] = svg(
    f'<g {S}><circle cx="196" cy="176" r="62"/>'
    f'<path d="M 170 232 C 140 300, 250 290, 236 352 C 226 398, 300 410, 336 376"/></g>'
    f'<circle cx="376" cy="330" r="26" fill="{LIGHT}"/>')

# G — Soft Square Smile: squircle coin, smile as the counter
V["G-squircle-smile"] = svg(
    f'<rect x="116" y="106" width="280" height="280" rx="96" fill="{LIGHT}"/>'
    f'<path d="M 196 240 Q 256 300 316 240" fill="none" stroke="{WHITE}" '
    f'stroke-width="34" stroke-linecap="round"/>'
    f'<circle cx="256" cy="440" r="24" fill="{LIGHT}"/>')

# H — Wink Meem: the ring looks up-right toward the gain
V["H-wink-meem"] = svg(
    f'<g {S}><circle cx="246" cy="250" r="96"/>'
    f'<path d="M 176 316 L 148 388"/></g>'
    f'<circle cx="286" cy="212" r="34" fill="{LIGHT}"/>')

LABELS = {
    "A-meem-smile": "A · Meem Smile",
    "B-loop-meem": "B · Loop Meem (one flourish)",
    "C-bubble-meem": "C · Bubble Meem (chat)",
    "D-coin-smile": "D · Coin Smile",
    "E-rising-bubbles": "E · Rising Bubbles",
    "F-spring-meem": "F · Spring Meem (bounce)",
    "G-squircle-smile": "G · Squircle Smile",
    "H-wink-meem": "H · Wink Meem",
}

if __name__ == "__main__":
    os.makedirs(OUTD, exist_ok=True)
    labs = []
    for name, doc in V.items():
        p = os.path.join(OUTD, name + ".svg")
        with open(p, "w") as f:
            f.write(doc)
        subprocess.run(["rsvg-convert", "-w", "512", p, "-o",
                        os.path.join(OUTD, name + ".png")], check=True)
        lab = os.path.join(OUTD, "_l" + name + ".png")
        subprocess.run(["convert", os.path.join(OUTD, name + ".png"),
                        "-resize", "300x300", "-gravity", "south", "-background", "white",
                        "-splice", "0x40", "-font", "DejaVu-Sans", "-pointsize", "18",
                        "-fill", "#4B5563", "-annotate", "+0+8", LABELS[name], lab],
                       check=True)
        labs.append(lab)
    subprocess.run(["montage", *labs, "-tile", "4x2", "-geometry", "+10+10",
                    "-background", "#F3F4F6", os.path.join(OUTD, "sheet.png")], check=True)
    for l in labs:
        os.remove(l)
    print("souhoola-style samples done")
