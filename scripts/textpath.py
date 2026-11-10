"""Convert text to SVG outline paths so fonts look identical everywhere."""
from fontTools.ttLib import TTFont
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.pens.transformPen import TransformPen
import os
HERE = os.path.dirname(os.path.abspath(__file__))
_cache = {}
def _font(name):
    if name not in _cache:
        _cache[name] = TTFont(os.path.join(HERE, name))
    return _cache[name]

def text_width(font, text, size, tracking=0):
    f = _font(font); cmap = f.getBestCmap(); hmtx = f['hmtx']; upm = f['head'].unitsPerEm
    s = size / upm
    return sum(hmtx[cmap[ord(c)]][0] * s + tracking for c in text) - tracking

def text_path(font, text, size, x, y, anchor="middle", tracking=0):
    f = _font(font); cmap = f.getBestCmap(); gs = f.getGlyphSet(); hmtx = f['hmtx']
    upm = f['head'].unitsPerEm; s = size / upm
    w = text_width(font, text, size, tracking)
    cx = x - (w / 2 if anchor == "middle" else (w if anchor == "end" else 0))
    out = []
    for ch in text:
        gn = cmap[ord(ch)]
        pen = SVGPathPen(gs, ntos=lambda v: ("%.2f" % v).rstrip("0").rstrip("."))
        gs[gn].draw(TransformPen(pen, (s, 0, 0, -s, cx, y)))
        d = pen.getCommands()
        if d: out.append(d)
        cx += hmtx[gn][0] * s + tracking
    return "".join(out)
