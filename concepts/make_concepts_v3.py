#!/usr/bin/env python3
"""Morabh symbol v3 — refinement of the strongest v2 insight: Ellipsis Rising."""
import os
import subprocess

BLUE = "#33509C"
TINT = "#A2BCFF"
GREEN = "#074D31"
HERE = os.path.dirname(os.path.abspath(__file__))


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
            f'width="512" height="512"><rect width="512" height="512" fill="#ffffff"/>{body}</svg>')


CONCEPTS = {}

# C1 — pure: three rising, growing dots; the last is the gain
CONCEPTS["v3-C1-ellipsis-pure"] = svg(
    f'<circle cx="112" cy="400" r="44" fill="{BLUE}"/>'
    f'<circle cx="252" cy="304" r="58" fill="{BLUE}"/>'
    f'<circle cx="402" cy="182" r="74" fill="{GREEN}"/>')

# C2 — completion: two paid dots, then the ring (meem head / the plan completed)
#      with the halal gain landing inside it
CONCEPTS["v3-C2-ellipsis-meem"] = svg(
    f'<circle cx="108" cy="404" r="42" fill="{BLUE}"/>'
    f'<circle cx="242" cy="312" r="54" fill="{BLUE}"/>'
    f'<circle cx="396" cy="188" r="78" fill="none" stroke="{BLUE}" stroke-width="44"/>'
    f'<circle cx="396" cy="188" r="34" fill="{GREEN}"/>')

# C3 — journey: paid solid, current ring, next tint — the live payment timeline
CONCEPTS["v3-C3-ellipsis-timeline"] = svg(
    f'<circle cx="108" cy="404" r="42" fill="{BLUE}"/>'
    f'<circle cx="242" cy="312" r="54" fill="{BLUE}"/>'
    f'<circle cx="396" cy="188" r="74" fill="{TINT}"/>'
    f'<circle cx="396" cy="188" r="34" fill="{GREEN}"/>')

# A2 — Pause-Up fixed: damma floats above the rising bar (no exclamation read)
CONCEPTS["v3-A2-pause-up"] = svg(
    f'<rect x="158" y="216" width="76" height="212" rx="38" fill="{BLUE}"/>'
    f'<rect x="292" y="120" width="76" height="212" rx="38" fill="{BLUE}"/>'
    f'<circle cx="330" cy="58" r="28" fill="{GREEN}"/>')

# D2 — Half-Now Coin, clean (no stem)
CONCEPTS["v3-D2-half-now"] = svg(
    f'<path d="M 256 96 A 160 160 0 0 0 256 416 Z" fill="{BLUE}"/>'
    f'<path d="M 256 96 A 160 160 0 0 1 256 416 Z" fill="{TINT}"/>')

LABELS = {
    "v3-C1-ellipsis-pure": "C1 · Ellipsis Rising — pure",
    "v3-C2-ellipsis-meem": "C2 · Ellipsis -> Meem ring + gain",
    "v3-C3-ellipsis-timeline": "C3 · Ellipsis timeline (paid/next)",
    "v3-A2-pause-up": "A2 · Pause-Up + damma",
    "v3-D2-half-now": "D2 · Half-Now Coin",
}

if __name__ == "__main__":
    for name, doc in CONCEPTS.items():
        p = os.path.join(HERE, name + ".svg")
        with open(p, "w") as f:
            f.write(doc)
        subprocess.run(["rsvg-convert", "-w", "512", p, "-o",
                        os.path.join(HERE, name + ".png")], check=True)
    print("v3 rendered:", len(CONCEPTS))
