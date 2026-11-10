"""Tiny pixel-art toolkit: sprites -> merged SVG paths, animation helpers, 3x5 font."""
import random
def esc(c): return c
def R(x, y, w, h, c, extra=""):
    return f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{c}"{(" "+extra) if extra else ""}/>'
def spr(x, y, rows, pal, extra=""):
    runs = {}
    for j, row in enumerate(rows):
        i = 0
        while i < len(row):
            ch = row[i]
            if ch == '.' or ch == ' ' or ch not in pal: i += 1; continue
            k = i
            while k < len(row) and row[k] == ch: k += 1
            runs.setdefault(ch, []).append(f"M{x+i} {y+j}h{k-i}v1h-{k-i}z")
            i = k
    return "".join(f'<path fill="{pal[ch]}" d="{"".join(d)}"/>' for ch, d in runs.items())
def G(inner, extra=""): return f'<g{(" "+extra) if extra else ""}>{inner}</g>'
def fmt(v):
    return ("%g" % v)
def A(attr, vals, kts=None, dur=32, begin=None, discrete=False, extra=""):
    v = ";".join(str(x) for x in vals)
    s = f'<animate attributeName="{attr}" values="{v}" dur="{dur}s" repeatCount="indefinite"'
    if kts: s += f' keyTimes="{";".join(fmt(k) for k in kts)}"'
    if discrete: s += ' calcMode="discrete"'
    if begin is not None: s += f' begin="{begin}s"'
    return s + (" " + extra if extra else "") + "/>"
def AT(vals, kts=None, dur=32, begin=None, discrete=False, typ="translate"):
    v = ";".join(str(x) for x in vals)
    s = f'<animateTransform attributeName="transform" type="{typ}" values="{v}" dur="{dur}s" repeatCount="indefinite"'
    if kts: s += f' keyTimes="{";".join(fmt(k) for k in kts)}"'
    if discrete: s += ' calcMode="discrete"'
    if begin is not None: s += f' begin="{begin}s"'
    return s + "/>"
def vis(intervals, dur, begin=None):
    pts = sorted({0.0} | {a for a, b in intervals} | {b for a, b in intervals if b < 1})
    vals = ["visible" if any(a <= p < b for a, b in intervals) else "hidden" for p in pts]
    return A("visibility", vals, pts, dur, begin, True)
def frames(frame_list, schedule, dur, begin=None):
    """frame_list: list of svg strings; schedule: {idx: [(a,b)...]} in 0..1. First frame visible in static preview."""
    out = ""
    for i, f in enumerate(frame_list):
        base = "visible" if i == 0 else "hidden"
        out += f'<g visibility="{base}">{f}{vis(schedule[i], dur, begin)}</g>'
    return out
def stepseq(n, kt_from=0.0, kt_to=1.0):
    return [kt_from + (kt_to - kt_from) * i / n for i in range(n)]

# 3x5 pixel font
F = {
 'X':["#.#","#.#",".#.","#.#","#.#"], 'O':["###","#.#","#.#","#.#","###"], 'T':["###",".#.",".#.",".#.",".#."],
 'A':[".#.","#.#","###","#.#","#.#"], 'H':["#.#","#.#","###","#.#","#.#"], 'S':["###","#..","###","..#","###"],
 'I':["###",".#.",".#.",".#.","###"], 'N':["#.#","###","###","###","#.#"],
 'c':["###","#..","#..","#..","###"], 'o':["###","#.#","#.#","#.#","###"], 'n':["##.","#.#","#.#","#.#","#.#"],
 's':["###","#..","###","..#","###"], 't':["###",".#.",".#.",".#.",".#."], 'm':["#.#","###","###","#.#","#.#"],
 'e':["###","#..","###","#..","###"], 'r':["##.","#.#","#..","#..","#.."], 'l':["#..","#..","#..","#..","###"],
 'd':["##.","#.#","#.#","#.#","##."], 'v':["#.#","#.#","#.#","#.#",".#."], 'h':["#..","#..","###","#.#","#.#"],
 'i':[".#.","...",".#.",".#.",".#."], 'p':["###","#.#","###","#..","#.."], 'u':["#.#","#.#","#.#","#.#","###"],
 '=':["...","###","...","###","..."], '{':[".##",".#.","#..",".#.",".##"], '}':["##.",".#.","..#",".#.","##."],
 ':':["...",".#.","...",".#.","..."], ',':["...","...","...",".#.","#.."], ';':["...",".#.","...",".#.","#.."],
 ' ':["...","...","...","...","..."],
}
def text_px(x, y, s, color, adv=4):
    """Return merged path of text using 3x5 font; color is a fill value."""
    d = []
    for k, ch in enumerate(s):
        g = F[ch]
        for j, row in enumerate(g):
            i = 0
            while i < 3:
                if row[i] == '#':
                    e = i
                    while e < 3 and row[e] == '#': e += 1
                    d.append(f"M{x+k*adv+i} {y+j}h{e-i}v1h-{e-i}z"); i = e
                else: i += 1
    return f'<path fill="{color}" d="{"".join(d)}"/>'
