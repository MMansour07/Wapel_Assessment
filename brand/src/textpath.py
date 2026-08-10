"""Shape a text string with HarfBuzz and emit combined SVG path data.

Used to convert the Morabh wordmarks (Latin + Arabic) into standalone
vector outlines so the final brand SVGs have no font dependencies.
"""
import uharfbuzz as hb
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
from fontTools.misc.transform import Transform


def shape_glyphs(font_path, text, size=100.0, variations=None, features=None):
    """Shape `text`; return (glyphs, advance, ascender, descender).

    glyphs is a list of dicts: {name, cluster, d} where d is SVG path data
    positioned in a y-down coordinate space with baseline at y=0.
    """
    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    font = hb.Font(face)
    if variations:
        font.set_variations(variations)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {})

    upem = face.upem
    scale = size / upem

    tt = TTFont(font_path)
    if variations and "fvar" in tt:
        from fontTools.varLib.instancer import instantiateVariableFont
        instantiateVariableFont(tt, variations, inplace=True)
    glyph_set = tt.getGlyphSet()
    glyph_order = tt.getGlyphOrder()

    x_cursor, y_cursor = 0.0, 0.0
    glyphs = []
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyph_name = glyph_order[info.codepoint]
        t = Transform(scale, 0, 0, -scale,
                      (x_cursor + pos.x_offset) * scale,
                      -(y_cursor + pos.y_offset) * scale)
        spen = SVGPathPen(glyph_set)
        pen = TransformPen(spen, t)
        glyph_set[glyph_name].draw(pen)
        d = spen.getCommands()
        if d:
            glyphs.append({"name": glyph_name, "cluster": info.cluster, "d": d})
        x_cursor += pos.x_advance
        y_cursor += pos.y_advance

    hhea = tt["hhea"]
    return glyphs, x_cursor * scale, hhea.ascender * scale, hhea.descender * scale


def text_to_svg_path(font_path, text, size=100.0, variations=None, features=None):
    """Return (path_data, advance_width, ascender, descender) scaled to `size` px per em."""
    glyphs, adv, asc, desc = shape_glyphs(font_path, text, size, variations, features)
    return " ".join(g["d"] for g in glyphs), adv, asc, desc


def shape_bounds(font_path, text, size=100.0, variations=None, features=None):
    """True ink bounding box (xmin, ymin, xmax, ymax) of the shaped run, y-down, baseline at 0."""
    from fontTools.pens.boundsPen import BoundsPen

    blob = hb.Blob.from_file_path(font_path)
    face = hb.Face(blob)
    font = hb.Font(face)
    if variations:
        font.set_variations(variations)

    buf = hb.Buffer()
    buf.add_str(text)
    buf.guess_segment_properties()
    hb.shape(font, buf, features or {})

    upem = face.upem
    scale = size / upem

    tt = TTFont(font_path)
    if variations and "fvar" in tt:
        from fontTools.varLib.instancer import instantiateVariableFont
        instantiateVariableFont(tt, variations, inplace=True)
    glyph_set = tt.getGlyphSet()
    glyph_order = tt.getGlyphOrder()

    xmin = ymin = float("inf")
    xmax = ymax = float("-inf")
    x_cursor, y_cursor = 0.0, 0.0
    for info, pos in zip(buf.glyph_infos, buf.glyph_positions):
        glyph_name = glyph_order[info.codepoint]
        bpen = BoundsPen(glyph_set)
        glyph_set[glyph_name].draw(bpen)
        if bpen.bounds:
            gx0, gy0, gx1, gy1 = bpen.bounds
            # font coords y-up -> svg y-down
            x0 = (x_cursor + pos.x_offset + gx0) * scale
            x1 = (x_cursor + pos.x_offset + gx1) * scale
            y0 = -((y_cursor + pos.y_offset + gy1)) * scale
            y1 = -((y_cursor + pos.y_offset + gy0)) * scale
            xmin, ymin = min(xmin, x0), min(ymin, y0)
            xmax, ymax = max(xmax, x1), max(ymax, y1)
        x_cursor += pos.x_advance
        y_cursor += pos.y_advance
    return xmin, ymin, xmax, ymax


if __name__ == "__main__":
    import sys, json
    font_path, text, size = sys.argv[1], sys.argv[2], float(sys.argv[3])
    variations = json.loads(sys.argv[4]) if len(sys.argv) > 4 else None
    d, adv, asc, desc = text_to_svg_path(font_path, text, size, variations)
    print(json.dumps({"d": d, "advance": adv, "ascender": asc, "descender": desc}))
