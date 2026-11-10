import os
from textpath import text_path, text_width
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "..", "assets")
I5, I6, PF = "inter-latin-500-normal.woff", "inter-latin-600-normal.woff", "playfair-display-latin-700-normal.woff"

STYLE = """<style>
  :root{--card:#0f1538;--card2:#161e4a;--bd:#2a3678;--tx:#eef2ff;--mu:#9fb4e8;--ac:#6ee7ff;--ac2:#c9a7ff;--bar:#1c2557;--ok:#7dff9a}
  @media (prefers-color-scheme: light){:root{--card:#f6f8ff;--card2:#e6edff;--bd:#c3d0f5;--tx:#14204f;--mu:#4a5a92;--ac:#0b7fa8;--ac2:#6b3fd0;--bar:#dbe4ff;--ok:#1a9a52}}
  .t{fill:var(--tx)} .m{fill:var(--mu)} .a{fill:var(--ac)} .a2{fill:var(--ac2)}
</style>"""

def T(font, s, size, x, y, cls="t", anchor="start", tracking=0):
    return f'<path class="{cls}" d="{text_path(font, s, size, x, y, anchor, tracking)}"/>'

def wrap(font, s, size, maxw, tracking=0):
    words, lines, cur = s.split(), [], ""
    for w in words:
        t = (cur + " " + w).strip()
        if text_width(font, t, size, tracking) <= maxw: cur = t
        else: lines.append(cur); cur = w
    if cur: lines.append(cur)
    return lines

def svg(w, h, body, label):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="{label}">'
            f'<title>{label}</title>{STYLE}<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="var(--ac)"/><stop offset="1" stop-color="var(--ac2)"/></linearGradient></defs>{body}</svg>')

def card_bg(w, h, r=14):
    return (f'<rect x=".5" y=".5" width="{w-1}" height="{h-1}" rx="{r}" fill="var(--card)" stroke="var(--bd)"/>')
