#!/usr/bin/env python3
"""Hassala concept — insight variants.

H1  Solid classic       — dome + slot + coin edge-on
H2  Installment arc     — three coins arcing down into the slot (ellipsis merge)
H3  Glass hassala       — OUTLINE vessel, coins visible inside (transparency)
H4  Glass + drop        — glass vessel, stack inside, green coin mid-drop (the pick)
"""
import os
import subprocess

BLUE = "#33509C"
GREEN = "#074D31"
WHITE = "#FFFFFF"
HERE = os.path.dirname(os.path.abspath(__file__))


def svg(body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" '
            f'width="512" height="512"><rect width="512" height="512" fill="#ffffff"/>{body}</svg>')


def stroke(sw=44, color=BLUE):
    return f'fill="none" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" stroke-linejoin="round"'


V = {}

V["H1-solid"] = svg(
    f'<path d="M 96 408 A 160 160 0 0 1 416 408 Z" fill="{BLUE}"/>'
    f'<rect x="196" y="256" width="120" height="34" rx="17" fill="{WHITE}"/>'
    f'<rect x="234" y="132" width="44" height="136" rx="22" fill="{GREEN}"/>')

V["H2-installment-arc"] = svg(
    f'<path d="M 96 428 A 160 160 0 0 1 416 428 Z" fill="{BLUE}"/>'
    f'<rect x="196" y="276" width="120" height="34" rx="17" fill="{WHITE}"/>'
    f'<circle cx="256" cy="224" r="34" fill="{GREEN}"/>'
    f'<circle cx="342" cy="152" r="27" fill="{BLUE}"/>'
    f'<circle cx="428" cy="104" r="21" fill="{BLUE}"/>')

# glass vessel: open-top dome outline + base line
GLASS = (f'<g {stroke()}>'
         f'<path d="M 106 408 A 150 150 0 0 1 206 267"/>'
         f'<path d="M 306 267 A 150 150 0 0 1 406 408"/>'
         f'<path d="M 106 408 H 406"/>'
         f'</g>')

V["H3-glass"] = svg(
    GLASS
    + f'<rect x="186" y="346" width="140" height="34" rx="17" fill="{BLUE}"/>'
    + f'<rect x="200" y="300" width="112" height="34" rx="17" fill="{BLUE}"/>'
    + f'<rect x="212" y="254" width="88" height="34" rx="17" fill="{GREEN}"/>')

V["H4-glass-drop"] = svg(
    GLASS
    + f'<rect x="186" y="346" width="140" height="34" rx="17" fill="{BLUE}"/>'
    + f'<rect x="200" y="300" width="112" height="34" rx="17" fill="{BLUE}"/>'
    + f'<rect x="234" y="130" width="44" height="110" rx="22" fill="{GREEN}"/>')

LABELS = {
    "H1-solid": "H1 · Solid classic",
    "H2-installment-arc": "H2 · Installment arc",
    "H3-glass": "H3 · Glass hassala (see inside)",
    "H4-glass-drop": "H4 · Glass + coin dropping",
}

if __name__ == "__main__":
    outd = os.path.join(HERE, "hassala")
    os.makedirs(outd, exist_ok=True)
    labs = []
    for name, doc in V.items():
        p = os.path.join(outd, name + ".svg")
        with open(p, "w") as f:
            f.write(doc)
        subprocess.run(["rsvg-convert", "-w", "512", p, "-o",
                        os.path.join(outd, name + ".png")], check=True)
        lab = os.path.join(outd, "_lab-" + name + ".png")
        subprocess.run(["convert", os.path.join(outd, name + ".png"),
                        "-resize", "340x340", "-gravity", "south", "-background", "white",
                        "-splice", "0x44", "-font", "DejaVu-Sans", "-pointsize", "20",
                        "-fill", "#4B5563", "-annotate", "+0+10", LABELS[name], lab], check=True)
        labs.append(lab)
    subprocess.run(["montage", *labs, "-tile", "4x1", "-geometry", "+10+10",
                    "-background", "#F3F4F6", os.path.join(outd, "sheet-hassala.png")], check=True)
    for l in labs:
        os.remove(l)
    # tiny test for H3/H4
    for n in ("H3-glass", "H4-glass-drop"):
        subprocess.run(["convert", os.path.join(outd, n + ".png"), "-resize", "32x32",
                        "-scale", "160x160", os.path.join(outd, "_t-" + n + ".png")], check=True)
    subprocess.run(["montage", os.path.join(outd, "_t-H3-glass.png"),
                    os.path.join(outd, "_t-H4-glass-drop.png"), "-tile", "2x1",
                    "-geometry", "+10+10", "-background", "white",
                    os.path.join(outd, "sheet-hassala-tiny.png")], check=True)
    for n in ("H3-glass", "H4-glass-drop"):
        os.remove(os.path.join(outd, "_t-" + n + ".png"))
    print("hassala variants done")
