import os, random
from pix import *
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
W, H, DUR = 192, 108, 32
CYC = [0, .3, .55, .8, 1]          # sunset, night, deep night, dawn, sunset
rng = random.Random(7)

# ---------- palette (shared by every object) ----------
C = dict(ink="#0a0d1f", b1="#0f1538", b2="#1a2252", b3="#27327a", b4="#3a4a9a", rim="#b9ccff",
         cy="#6ee7ff", cy2="#2fa8c9", wh="#ffffff", yl="#ffd86b", yl2="#e8a84b", pk="#ff7ad9", pk2="#b8408f",
         gr="#7dff9a", rd="#ff5c5c")

SKY = [  # 8 bands, 5 phases each
 ["#2b1f4e","#0b1030","#060914","#1a1f4a","#2b1f4e"],
 ["#43296a","#0f173f","#080c1f","#2a2f6a","#43296a"],
 ["#6a3a82","#151f50","#0b102b","#3f4a8a","#6a3a82"],
 ["#94487f","#1b2860","#0e1536","#6a62a0","#94487f"],
 ["#c4577a","#233271","#121a42","#a07aa8","#c4577a"],
 ["#ea6f6b","#2d3d82","#161f4c","#d98fa0","#ea6f6b"],
 ["#f59463","#384a92","#1a2556","#f3a58f","#f59463"],
 ["#fbbf6a","#4558a0","#1f2c60","#fbd08a","#fbbf6a"]]

def sky():
    s = ""; bh = 10
    for i, vals in enumerate(SKY):
        s += R(0, i*bh, W, bh+1, vals[1], A("fill", vals, CYC).join(["><", "></rect>"]).replace("<rect","<rect") ) if False else \
             f'<rect x="0" y="{i*bh}" width="{W}" height="{bh+1}" fill="{vals[1]}">{A("fill", vals, CYC)}</rect>'
    # dithered seams between bands
    for i in range(len(SKY)-1):
        yb = (i+1)*bh
        nxt, cur = SKY[i+1], SKY[i]
        d1 = "".join(f"M{x} {yb-1}h1v1h-1z" for x in range(0, W, 2))
        d2 = "".join(f"M{x} {yb}h1v1h-1z" for x in range(1, W, 2))
        d3 = "".join(f"M{x} {yb-2}h1v1h-1z" for x in range(1, W, 4))
        s += f'<path d="{d1}{d3}" fill="{nxt[1]}">{A("fill", nxt, CYC)}</path>'
        s += f'<path d="{d2}" fill="{cur[1]}">{A("fill", cur, CYC)}</path>'
    return s

def stars():
    out = ""
    for _ in range(46):
        x, y = rng.randrange(2, W-2), rng.randrange(2, 56)
        big = rng.random() < .12
        t = round(rng.uniform(2, 5), 1); b = round(rng.uniform(0, 3), 1)
        c = rng.choice(["#ffffff", "#ffffff", "#cfe0ff", "#fff2c4"])
        out += R(x, y, 1, 1, c, "") .replace("/>", f'>{A("opacity",[1,.25,1],None,t,b)}</rect>')
        if big: out += R(x-1, y, 3, 1, c, 'opacity=".35"') + R(x, y-1, 1, 3, c, 'opacity=".35"')
    return G(out, 'opacity="1"').replace('opacity="1"', 'opacity="1"')[:-4] + A("opacity",[0,1,1,.35,0],CYC) + "</g>"

def moon():
    cx, cy = 166, 17
    pal = {'a':"#f4f1d0", 'b':"#d9d4a8", 'c':"#fffbe6", 'd':"#b8b38a"}
    rows = ["....aaaaaa....","..aaaaaaaaaa..",".aaccaaaaaaaa.","aaaccabbaaaaaa","aaaaaabbbaaaab","aaabbaaaaaaabd","aaabbaaaaaabbd","aaaaaaabbaaaad","aaaaaaabbbaaad","abbaaaaaaaaadd",".abbaaaaaaadd.","..aaaaaaaadd..","....aaaaddd..."]
    glow = f'<circle cx="{cx+7}" cy="{cy+6}" r="13" fill="#f4f1d0" opacity=".06">{A("opacity",[.06,.14,.06],None,6)}</circle>'
    return G(glow + spr(cx, cy, rows, pal)) .replace("<g>", "<g>",1)[:-4] + A("opacity",[0,1,1,.45,0],CYC) + "</g>"

def sun():
    pal = {'a':"#ffe8a0",'b':"#ffc15e",'c':"#ff9a4c"}
    rows = ["...aaaa...","..aaaaaa..",".aaaaaaaa.","aaaaaaaaaa","aaaabbbbbb","bbbbbbbbbb",".bbbbbbbb.","..bbcccc..","...cccc..."]
    return G(spr(118, 56, rows, pal), 'opacity="0.001"')[:-4] + AT(["0 0","0 22","0 22","0 22","0 0"], CYC) + A("opacity",[1,0,0,0,1],[0,.14,.5,.86,1]) + "</g>"

def clouds():
    pal = {'a':"#9d94d6", 'b':"#7c74b8"}
    big = ["....aaa.......","..aaaaaaa.aa..",".aaaaaaaaaaaaa","aaaaaaaaaaaaaa",".bbbbbbbbbbbb."]
    sm  = ["..aaa....","aaaaaaaa.","aaaaaaaaa",".bbbbbbb."]
    def layer(sprite, y, dur, delay, op):
        return G(spr(0, y, sprite, pal), f'opacity="{op}"').replace("<g ","<g ",1)[:-4] + AT([f"-30 0", f"{W+10} 0"], None, dur, delay) + "</g>"
    return layer(big, 14, 90, -20, .35) + layer(sm, 30, 70, -50, .3) + layer(big, 40, 60, -5, .28) + layer(sm, 8, 110, -80, .25)

def skyline():
    s = ""
    far = [(0,52,10),(10,46,8),(18,56,12),(30,42,9),(39,54,11),(50,48,8),(58,58,13),(71,44,10),(81,53,9),(91,50,12),(103,57,8),(111,46,11),(122,55,9),(131,49,12),(143,56,8),(151,51,9),(160,47,10),(170,55,9),(179,50,13)]
    base = 83
    s += f'<g fill="{C["b2"]}">' + "".join(f'<rect x="{x}" y="{y+6}" width="{w}" height="{base-y-6}"/>' for x, y, w in far) + "</g>"
    s += R(34, 38+6, 1, 4, C["b2"]) + R(75, 40+6, 1, 4, C["b2"]) + R(165, 41+6, 1, 6, C["b2"])
    s += f'<rect x="35" y="43" width="1" height="1" fill="{C["rd"]}">{A("opacity",[1,0,1],None,1.6)}</rect>'
    # moonlit top edges (rim light, moon is top-right)
    rim = "".join(f'<rect x="{x}" y="{y+6}" width="{w}" height="1"/>' for x, y, w in far if x > 90)
    s += f'<g fill="#5a6cc0" opacity=".9">{rim}</g>'
    near = [(0,64,16),(16,60,10),(26,66,14),(112,62,12),(124,58,16),(140,66,10),(150,61,12),(162,64,14),(176,60,16)]
    s += f'<g fill="{C["b1"]}">' + "".join(f'<rect x="{x}" y="{y}" width="{w}" height="{base-y}"/>' for x, y, w in near) + "</g>"
    rim2 = "".join(f'<rect x="{x}" y="{y}" width="{w}" height="1"/>' for x, y, w in near if x > 100)
    s += f'<g fill="{C["rim"]}" opacity=".55">{rim2}</g>' [:-4] + "</g>"
    # windows
    wins = ""
    for (x, y, w) in far + near:
        top = y + (6 if (x, y, w) in far else 0)
        for wy in range(top+3, 74, 4):
            for wx in range(x+2, x+w-2, 4):
                if rng.random() < .42:
                    col = rng.choice([C["yl"], C["yl"], C["yl2"], C["cy"]])
                    if rng.random() < .15:
                        wins += f'<rect x="{wx}" y="{wy}" width="2" height="1" fill="{col}">{A("opacity",[1,1,0,1],[0,.5,.55,1],round(rng.uniform(5,11),1))}</rect>'
                    else:
                        wins += f'<rect x="{wx}" y="{wy}" width="2" height="1" fill="{col}"/>'
    s += G(wins)[:-4] + A("opacity",[.4,1,.85,.55,.4],CYC) + "</g>"
    return s

def airplane_and_star():
    plane = R(0, 13, 1, 1, C["rd"]).replace("/>", f'>{A("x",[-2,194],None,45)}{A("opacity",[1,0,1],None,1.2)}</rect>')
    star = ('<g opacity="0">' + R(0,0,4,1,"#ffffff") + R(-3,-1,3,1,"#9fb4ff",'opacity=".6"') +
            AT(["172 6","172 6","128 26","128 26"],[0,.02,.14,1],10) + A("opacity",[0,0,1,0,0],[0,.02,.04,.14,1],10) + '</g>')
    return G(plane + star)[:-4] + A("opacity",[0,1,1,.2,0],CYC) + "</g>"

def railing_floor():
    s = ""
    s += R(0, 74, W, 1, C["b4"]) + R(0, 75, W, 1, C["b3"])
    s += "".join(R(x, 76, 1, 7, "#1f2a5e") for x in range(2, W, 10))
    s += R(0, 82, W, 1, C["b3"]) + R(0, 81, W, 1, "#141b46")
    s += R(0, 83, W, 25, C["ink"])
    # floor seams (perspective)
    for y, c in [(89,"#141b3d"),(96,"#141b3d"),(104,"#181f47")]:
        s += R(0, y, W, 1, c)
    for y0, y1, step in [(83,89,14),(89,96,18),(96,104,24),(104,108,32)]:
        off = (y0 * 3) % step
        s += "".join(R(x, y0, 1, y1-y0, "#121835") for x in range(-off, W, step) if x >= 0)
    # shadow dither under railing
    s += "".join(R(x, 83, 1, 1, "#05070f") for x in range(0, W, 2)) + "".join(R(x, 84, 1, 1, "#05070f") for x in range(1, W, 4))
    # puddles
    for x, y, w in [(18, 98, 20), (94, 100, 26), (146, 96, 18)]:
        s += R(x, y, w, 2, "#16204f") + R(x+2, y, w-6, 1, "#26337f")
    return s

def hut():
    s = ""
    s += R(0, 54, 42, 38, "#1b2354") + R(0, 54, 42, 1, "#2a3678")
    for y in range(58, 92, 4): s += R(0, y, 42, 1, "#141b46")
    for y in range(56, 92, 8): s += "".join(R(x, y, 1, 4, "#141b46") for x in range(3, 42, 9))
    for y in range(60, 92, 8): s += "".join(R(x, y, 1, 4, "#141b46") for x in range(7, 42, 9))
    s += R(-1, 50, 44, 4, "#2d3a80") + R(-1, 50, 44, 1, "#4a5cb8") + R(-1, 54, 44, 1, "#0f1538")
    # door with warm light
    s += R(27, 62, 11, 30, "#0f1538") + R(28, 63, 9, 29, "#e8a84b") + R(28, 63, 9, 6, "#ffd86b") + R(30, 63, 7, 29, "#ffe08a", 'opacity=".35"')
    s += R(26, 61, 13, 1, "#3a4a9a") + R(31, 76, 1, 1, "#0f1538") + R(35, 78, 2, 14, "#8a5a1c", 'opacity=".5"')
    # light spill on floor
    s += "".join(R(x, y, 1, 1, "#ffd86b", 'opacity=".22"') for y in range(92, 100) for x in range(27+(y-92), 38+(y-92)*2) if (x+y) % 2 == 0)
    # sticky board
    s += R(3, 61, 21, 19, "#6b4a33") + R(4, 62, 19, 17, "#8a6445") + R(4, 62, 19, 1, "#a07a52")
    notes = [(5,63,"#ffd86b"),(11,64,"#ff7ad9"),(17,63,"#6ee7ff"),(6,70,"#7dff9a"),(12,71,"#ffd86b"),(18,70,"#ff7ad9")]
    for x, y, c in notes:
        s += R(x, y, 4, 4, c) + R(x+1, y+1, 2, 1, "#00000055") + R(x, y+3, 4, 1, "#00000033")
        s += R(x+1, y-1 if False else y, 1, 1, C["rd"])
    # fluttering note (2 frames)
    f1 = R(18, 70, 4, 4, "#ff7ad9") + R(19, 71, 2, 1, "#00000055")
    f2 = R(18, 70, 4, 3, "#ff7ad9") + R(21, 73, 1, 1, "#ff7ad9") + R(19, 71, 2, 1, "#00000055")
    s += R(18, 70, 4, 4, "#8a6445")  # cover original
    s += frames([f1, f2], {0: [(0, .6)], 1: [(.6, 1)]}, 3.2)
    return s

def billboard():
    s = ""
    s += R(8, 41, 2, 10, "#0f1538") + R(38, 41, 2, 10, "#0f1538")
    s += R(5, 28, 40, 13, "#0a0d1f") + R(5, 28, 40, 1, "#2d3a80") + R(5, 40, 40, 1, "#070914") + R(5, 28, 1, 13, "#2d3a80")
    s += R(5, 28, 40, 13, "none", 'stroke="none"')
    word = "XOTAHSIN"
    halo = "".join(text_px(9 + dx, 31 + dy, word, "#ff7ad9").replace('fill="#ff7ad9"', 'fill="#ff7ad9" opacity=".22"') for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)])
    letters = text_px(9, 31, word, "#ffd1f3")
    core = text_px(9, 31, word, "#ff7ad9")
    s += G(halo + core + letters.replace('fill="#ffd1f3"', 'fill="#ffd1f3" opacity=".55"'))[:-4] + A("opacity",[.75,1,1,.5,.75],CYC) + "</g>"
    # one flickering letter (S)
    s += G(text_px(9+4*5, 31, "S", "#0a0d1f"), 'opacity="0.001"')[:-4] + A("opacity",[0,0,1,0,0,0,0.8,0],[0,.3,.31,.33,.6,.61,.62,1],5) + "</g>"
    s += R(8, 38, 34, 1, "#6ee7ff", 'opacity=".5"')
    return s

def plant():
    pot = spr(44, 84, ["aaaaaaa",".bbbbb.",".bbbbb.",".bcccb.","..ccc.."], {'a':"#c4703f",'b':"#8f4a2a",'c':"#6b3a22"})
    pal = {'a':"#3fbf6b",'b':"#2a8f55",'c':"#7dff9a",'d':"#1d6a40"}
    l1 = spr(42, 76, ["..c...c..",".cac.cac.","caaac.aaac","aabaabaab.",".dbaabab..","..dbbbd...","...dbd...","....d...."], pal)
    l2 = spr(43, 76, ["...c.c...",".cacacac.","aaaaaaaac","abaabaab.","..dbaab...","...dbbd...","....bd...","....d...."], pal)
    return pot + frames([l1, l2], {0: [(0, .5)], 1: [(.5, 1)]}, 3.4)

def desk_props():
    s = ""
    wood = {'a':"#8a6445",'b':"#6b4a33",'c':"#4a3222"}
    s += R(80, 72, 72, 1, "#a07a52") + R(80, 73, 72, 2, "#8a6445") + R(80, 75, 72, 1, "#4a3222")
    s += R(82, 76, 3, 14, "#6b4a33") + R(82, 76, 1, 14, "#8a6445") + R(147, 76, 3, 14, "#6b4a33") + R(147, 76, 1, 14, "#8a6445")
    s += R(85, 84, 62, 1, "#4a3222")
    return s

def laptop():
    pal = {'a':"#b9c2e8",'b':"#7f89b8",'c':"#4f5a8f",'d':"#2d3560"}
    base = spr(84, 70, ["aaaaaaaaaaaaaaaa","bbbbbbbbbbbbbbbb","cccccccccccccccc"], pal)
    screen = spr(98, 56, ["..dd","..cb","..cb",".dcb",".dcb",".dcb","dccb","dccb","dcbb","dcbb","dcbb","dcbb","aaaa"][:13], pal)
    return base + screen

def holo():
    s = ""
    # projector puck + beam
    s += R(117, 71, 14, 1, "#5a6390") + R(119, 70, 10, 1, "#9fb4e8") + R(121, 69, 6, 1, C["cy"])
    beam = f'<polygon points="120,69 128,69 154,57 94,57" fill="#6ee7ff" opacity=".08">{A("opacity",[.05,.12,.05],None,3)}</polygon>'
    s += beam
    px, py, pw, ph = 95, 26, 58, 31
    panel = R(px, py, pw, ph, "#6ee7ff", 'opacity=".10"')
    border = R(px, py, pw, 1, C["cy"]) + R(px, py+ph-1, pw, 1, C["cy"]) + R(px, py, 1, ph, C["cy"]) + R(px+pw-1, py, 1, ph, C["cy"])
    border = G(border, 'opacity=".7"')
    corners = "".join(R(x, y, 2, 2, "#ffffff") for x, y in [(px-1, py-1), (px+pw-1, py-1), (px-1, py+ph-1), (px+pw-1, py+ph-1)])
    title = R(px, py, pw, 4, C["cy"], 'opacity=".22"') + R(px+2, py+1, 1, 1, "#ff5c8a") + R(px+4, py+1, 1, 1, C["yl"]) + R(px+6, py+1, 1, 1, C["gr"])
    lines = [("const", "#ff7ad9", " me = {", "#9fb4e8"), ("  role", "#6ee7ff", ": dev,", "#ffd86b"), ("  ship", "#6ee7ff", ": true", "#7dff9a"), ("};", "#9fb4e8", "", "")]
    code = ""; defs = ""
    for k, (a, ca, b, cb) in enumerate(lines):
        n = len(a) + len(b); y = py + 6 + k*6
        cid = f"clip{k}"
        step = 0.13; start = 0.6 + k*2.5; CH = 14
        vals = [0]; kts = [0]
        for i in range(1, n+1):
            vals.append(i*4); kts.append((start + i*step)/CH)
        vals += [0]; kts += [0.93]
        kts[0] = 0
        # discrete needs values==keytimes; clip starts at 0 (hidden) until start
        vals.insert(1, 0); kts.insert(1, start/CH)
        defs += f'<clipPath id="{cid}"><rect x="{px+2}" y="{y-1}" width="{n*4+2}" height="7">{A("width", vals, kts, CH, None, True)}</rect></clipPath>'
        code += f'<g clip-path="url(#{cid})">{text_px(px+3, y, a, ca)}{text_px(px+3+len(a)*4, y, b, cb) if b else ""}</g>'
    cursor = R(px+3+2*4+2, py+6+3*6, 2, 5, "#ffffff", f'>{A("opacity",[1,0,1],None,1)}</rect><rect x="0" y="0" width="0" height="0"').replace('/><rect x="0" y="0" width="0" height="0"', '', 0)
    cursor = f'<rect x="{px+3+3*4}" y="{py+6+3*6}" width="2" height="5" fill="#ffffff">{A("opacity",[1,0,1],None,1)}</rect>'
    bob = AT(["0 0","0 -1","0 0"], None, 4)
    panel_g = f'<g>{bob}{panel}{border}{corners}{title}{code}{cursor}</g>'
    s += f'<defs>{defs}</defs>' + G(panel_g)[:-4] + A("opacity",[.7,1,1,.85,.7],CYC) + "</g>"
    # dust motes
    for x, y, d in [(103,50,5),(114,44,7),(124,52,6),(136,46,8),(145,52,5),(108,36,9)]:
        s += f'<rect x="{x}" y="{y}" width="1" height="1" fill="#bff6ff">{A("opacity",[0,.9,0],None,d)}{A("y",[y,y-2,y-5],None,d)}</rect>'
    return s

def mug_radio():
    mug = spr(105, 67, ["aaaa.","abbac","abbac","aaaac",".ddd."], {'a':"#e8e8ff",'b':"#3a2418",'c':"#aab3e0",'d':"#7f89b8"})
    steam = ""
    for x, d, b in [(106, 2.4, 0), (108, 3.0, 1.1)]:
        steps = ["0 0","0 -1","1 -2","0 -3","0 -4"]
        steam += G(R(x, 64, 1, 2, "#e6ecff", 'opacity=".5"'))[:-4] + AT(steps, None, d, b) + A("opacity",[.0,.6,.5,.2,0],None,d,b) + "</g>"
    # radio
    rp = {'a':"#2b3560",'b':"#3f4aa8",'c':"#0a0d1f",'d':"#ffd86b",'e':"#6ee7ff",'f':"#161d45"}
    radio = spr(139, 63, ["..........b","...........","aaaaaaaaaaa","abbbbbbbbba","abccccbeeba","abccccbbbba","abccccbdbba","abccccbbbba","affffffffff"], rp)
    # antenna
    radio += R(148, 58, 1, 1, "#9fb4e8") + R(149, 57, 1, 1, "#9fb4e8") + R(150, 56, 1, 1, "#9fb4e8") + R(145, 62, 1, 1, "#9fb4e8")
    # eq bars (3 frames)
    eq = [R(143,66,1,1,C["cy"])+R(144,65,1,2,C["cy"])+R(145,67,1,0,C["cy"]),
          R(143,64,1,3,C["cy"])+R(144,66,1,1,C["cy"]),
          R(143,65,1,2,C["cy"])+R(144,64,1,3,C["cy"])]
    eq_g = frames(eq, {0:[(0,.33)],1:[(.33,.66)],2:[(.66,1)]}, 0.9)
    # music notes
    note = ["..##",".#.#","...#","##..","##.."] if False else [".##",".#.",".#.","##.","##."]
    notes = ""
    for i, (col, d, b) in enumerate([("#ff7ad9", 4.0, 0), ("#6ee7ff", 4.0, 1.4), ("#ffd86b", 4.0, 2.7)]):
        sway = [0,1,1,0,-1,-1,0,1,1,0,-1,-1]
        steps = [f"{sway[k]} {-k*2}" for k in range(12)]
        notes += G(spr(143, 56, note, {'#': col}) if False else spr(143, 56, [r.replace('#','a') for r in note], {'a': col}))[:-4] + AT(steps, None, d, b, True) + A("opacity",[0,1,1,0],[0,.1,.7,1],d,b) + "</g>"
    return G(mug + steam)[:-4] + vis([(0, 6/12), (8/12, 1)], 12) + "</g>" + radio + eq_g + notes

def steam_g(s): return s

def cat_ac():
    s = ""
    ac = {'a':"#2d3a80",'b':"#1f2a5e",'c':"#141b46",'d':"#3a4a9a"}
    s += R(162, 71, 28, 19, "#1f2a5e") + R(162, 70, 28, 2, "#3a4a9a") + R(162, 89, 28, 1, "#0f1538") + R(162, 71, 1, 18, "#2d3a80") + R(189, 71, 1, 19, "#141b46")
    s += "".join(R(165, y, 22, 1, "#141b46") for y in (75, 78, 81, 84, 87))
    # fan
    fan1 = spr(170, 74, ["...#...",".#.#.#.","..###..","#######","..###..",".#.#.#.","...#..."], {'#': "#4a5cb8"}) 
    fan2 = spr(170, 74, ["#.....#",".#...#.","..#.#..","...#...","..#.#..",".#...#.","#.....#"], {'#': "#4a5cb8"})
    s += R(169, 73, 9, 9, "#0f1538") + frames([fan1, fan2], {0: [(0,.5)], 1: [(.5,1)]}, .3)
    s += R(163, 70, 27, 1, C["rim"], 'opacity=".6"') + R(189, 71, 1, 6, C["rim"], 'opacity=".5"')
    # cat loaf (2 breathing frames)
    cp = {'o':"#e8955c",'p':"#c4703f",'d':"#8f4a2a",'w':"#fff1dc",'k':"#2a1f2d"}
    c1 = ["..d.d..........","..oooo.........","oooooooooooo...","ooopoooopoooop.","woooooooooooopd",".dddddddddddd.."]
    c2 = ["..d.d..........","..oooo.........","oooooooooooo...","oooooopooooopop","woooooooooooopd",".dddddddddddd.."]
    c1[1] = "..oook........."; c2[1] = "..oook........."
    cat = frames([spr(168, 64, c1, cp), spr(168, 63, c2, cp)], {0: [(0,.5)], 1: [(.5,1)]}, 2.8)
    s += cat + R(171, 66, 1, 1, "#2a1f2d")  # closed eye
    # ear rim
    s += R(172, 63, 1, 1, C["rim"], 'opacity=".6"')
    # zzz
    for k, (dx, d, b) in enumerate([(0, 4.5, 0), (3, 4.5, 1.5), (6, 4.5, 3.0)]):
        z = spr(163+dx, 58, ["###","..#",".#.","#..","###"] if False else ["aaa",".a.","aaa"] , {'a': "#cfe0ff"})
        steps = [f"{(i//3)} {-i}" for i in range(9)]
        s += G(z)[:-4] + AT(steps, None, d, b, True) + A("opacity",[0,1,1,0],[0,.15,.7,1],d,b) + "</g>"
    return s

def character():
    s = ""
    # stool
    s += R(60, 78, 15, 2, "#6b4a33") + R(60, 78, 15, 1, "#8a6445") + R(62, 80, 2, 10, "#4a3222") + R(71, 80, 2, 10, "#4a3222") + R(62, 86, 11, 1, "#4a3222")
    # legs
    jp = {'k':"#4a5aa0",'J':"#34427f",'j':"#262f61"}
    s += spr(65, 75, ["kkkkkkkkkkkkkkk","JJJJJJJJJJJJJJJ","jjjjjjjjjjjjjjj"], jp)
    s += spr(77, 78, ["kJJJ","kJJj","kJJj","kJJj","kJJj","kJJj","kJJj","kJJj","kJJj","kJJj","kJjj","kJjj"], jp)
    s += spr(75, 90, ["wwwwwwww","wwwwwwwp","pppppppp"], {'w':"#e8e8ff",'p':"#ff7ad9"})
    # far arm group is drawn per frame; torso
    tp = {'F':"#8fa0ff",'B':"#5b6ee1",'b':"#3f4aa8",'d':"#2c3380",'w':"#ffffff"}
    torso = ["..bbBBBBB...","...bBBBBBBb.","..bBBBBBBFBb","bbBBBBBBBFBb","bBBBBBBBwBBb","bbBBBBBBwBbd","bbBBBBBBBbbd","bbbBBBBBbbdd","bbbBBBBbbbdd","bbbbBBbbbddd","bbbbbbbbbddd","dbbbbbbbdddd"]
    s += spr(62, 63, torso, tp)
    return s

HEAD = ["...hhHHHH....","..hPPPPPPH...",".hhHHHHHHHH..",".hHHHHHHLLLH.",".HHPPHHSLLLLs",".HPpPHHSLELLs",".HPpPHHSLLLLs",".HHPPHSLLLmLs","..HHHSSLLLLs.","...HHsSSSSss.","....ssSSss..."]
HP = {'H':"#2a1f2d",'h':"#5a4668",'S':"#e8a87c",'L':"#f5c9a0",'s':"#c47f5c",'E':"#140c1c",'P':"#ff7ad9",'p':"#b8408f",'m':"#a8574a"}

def line_px(x0, y0, x1, y1, c, th=2):
    pts = []; dx, dy = abs(x1-x0), abs(y1-y0); sx = 1 if x0 < x1 else -1; sy = 1 if y0 < y1 else -1
    err = dx - dy; x, y = x0, y0
    while True:
        pts.append((x, y))
        if x == x1 and y == y1: break
        e2 = 2*err
        if e2 > -dy: err -= dy; x += sx
        if e2 < dx: err += dx; y += sy
    return "".join(R(px_, py_, 1, th, c) for px_, py_ in pts)

def arm(sh, el, ha, base, shade, far=False):
    out = line_px(*sh, *el, shade if far else base, 2) + line_px(*el, *ha, shade if far else base, 2)
    # highlight/shadow
    if not far:
        out += line_px(sh[0], sh[1], el[0], el[1], "#8fa0ff", 1) .replace('fill="#8fa0ff"', 'fill="#8fa0ff" opacity=".55"')
    hand = R(ha[0], ha[1]-1, 3, 3, "#e8a87c") + R(ha[0], ha[1]-1, 3, 1, "#f5c9a0")
    return out + hand

def arm_frames():
    sh = (69, 66)
    base, shade = "#5b6ee1", "#3f4aa8"
    fa = arm((70, 66), (77, 66), (88, 69), "#3f4aa8", "#2c3380", True) + arm(sh, (76, 73), (86, 68), base, shade)
    fb = arm((70, 66), (77, 66), (88, 67), "#3f4aa8", "#2c3380", True) + arm(sh, (76, 73), (87, 70), base, shade)
    mug = spr(79, 54, ["aaaa.","abbac","abbac","aaaac",".ddd."], {'a':"#e8e8ff",'b':"#3a2418",'c':"#aab3e0",'d':"#7f89b8"})
    fs = arm((70, 66), (77, 66), (88, 69), "#3f4aa8", "#2c3380", True) + arm(sh, (77, 67), (79, 58), base, shade) + mug
    fst = arm((70, 66), (73, 58), (78, 45), "#3f4aa8", "#2c3380", True) + arm(sh, (72, 58), (73, 44), base, shade)
    return [fa, fb, fs, fst]

def char_anim():
    CH = 12
    A_iv, B_iv = [], []
    for a, b in [(0, 6), (8, 10)]:
        t = a
        while t < b - 1e-9:
            A_iv.append((t/CH, (t+.25)/CH)); B_iv.append(((t+.25)/CH, (t+.5)/CH)); t += .5
    sched = {0: A_iv, 1: B_iv, 2: [(6/CH, 8/CH)], 3: [(10/CH, 1)]}
    arms = frames(arm_frames(), sched, CH)
    # head: nod to the beat; tilts back while stretching
    ev = []
    t = 0; k = 0
    while t < 10 - 1e-9:
        ev.append((t/CH, "0 0" if k % 2 == 0 else "0 1")); t += .5; k += 1
    ev.append((10/CH, "0 -1"))
    kts = [e[0] for e in ev]; vals = [e[1] for e in ev]
    head_glow = ""
    # cyan light from laptop/hologram on the face, ear and hand side
    head_glow += R(73, 54, 2, 7, C["cy"], 'opacity=".22"') + R(74, 55, 1, 5, C["cy"], 'opacity=".25"') + R(72, 61, 3, 1, C["cy"], 'opacity=".25"')
    head = spr(62, 51, HEAD, HP)
    # blink
    blink = R(72, 56, 1, 1, "#c47f5c") 
    head_g = f'<g>{AT(vals, kts, CH, None, True)}{head}<g>{head_glow}</g>{blink.replace("/>", ">" + A("opacity",[0,0,1,0,0],[0,.7,.72,.76,1],4) + "</rect>")}</g>'
    neck = R(66, 62, 5, 1, "#c47f5c")
    return neck + head_g + arms

def character_glow():
    # cyan light on the desk, mug rim, hands & laptop base
    d = "".join(f"M{x} 72h1v1h-1z" for x in range(84, 122, 2)) + "".join(f"M{x} 73h1v1h-1z" for x in range(85, 108, 4))
    s = f'<path fill="{C["cy"]}" opacity=".4" d="{d}">{A("opacity",[.25,.45,.35,.45,.25],CYC)}</path>'
    s += R(98, 56, 1, 13, C["cy"], 'opacity=".55"') + R(105, 67, 1, 4, C["cy"], 'opacity=".35"')
    return s

def rain():
    drops = ""
    for layer, (dur, op, n) in enumerate([(0.75, .75, 16), (1.0, .55, 14), (1.35, .35, 12)]):
        pts = [(rng.randrange(0, W), rng.randrange(0, H)) for _ in range(n)]
        d = "".join(f"M{x} {y}h1v2h-1z" for x, y in pts) + "".join(f"M{x} {y-H}h1v2h-1z" for x, y in pts)
        drops += f'<g opacity="{op}"><path fill="#a9bcff" d="{d}">{AT(["0 0", f"0 {H}"], None, dur, None)}</path></g>'
    # ripples on puddles
    rip = ""
    for k, (x, y, w) in enumerate([(18, 98, 20), (94, 100, 26), (146, 96, 18)]):
        for j in range(3):
            cx = x + 3 + (j * 6 + k * 2) % (w - 6)
            fr = [R(cx+2, y, 1, 1, "#b9ccff"), R(cx+1, y, 3, 1, "#b9ccff") , R(cx, y, 5, 1, "#8ea3ee", 'opacity=".7"')]
            rip += frames(fr, {0: [(0,.33)], 1: [(.33,.66)], 2: [(.66,1)]}, 1.2, round(j*.4+k*.17, 2))
    return G(drops + rip, 'opacity="0.001"')[:-4] + A("opacity",[0,0,0,1,1,0,0],[0,.42,.46,.5,.66,.71,1]) + "</g>"

def fireflies():
    out = ""
    for x, y in [(52,72),(58,80),(40,94),(130,88),(176,80),(150,64),(30,88)]:
        xs = [x, x+1, x+1, x, x-1, x-1, x]; ys = [y, y, y-1, y-1, y-1, y, y]
        d = round(rng.uniform(5, 9), 1)
        out += f'<rect width="1" height="1" fill="#d8ff7a" x="{x}" y="{y}">{A("x", xs, None, d, None, True)}{A("y", ys, None, d, None, True)}{A("opacity",[0,1,1,.2,1,0],None,d)}</rect>'
    return G(out)[:-4] + A("opacity",[0,1,1,.5,0],CYC) + "</g>"

def overlay():
    return (f'<rect width="{W}" height="{H}" fill="#ff8a4c" opacity="0.001">{A("opacity",[.14,0,0,.1,.14],CYC)}</rect>'
            f'<rect width="{W}" height="{H}" fill="#000" opacity=".06">{A("opacity",[0,.06,.14,.04,0],CYC)}</rect>')

def build():
    parts = [sky(), sun(), stars(), moon(), airplane_and_star(), clouds(), skyline(), railing_floor(),
             billboard(), hut(), plant(), desk_props(), holo(), laptop(), mug_radio(), cat_ac(), character(),
             character_glow(), char_anim(), fireflies(), rain(), overlay()]
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" shape-rendering="crispEdges" role="img" '
           f'aria-label="Animated pixel art: a developer coding on a rooftop while the sky cycles from sunset to night to dawn, with rain, a sleeping cat, a lo-fi radio and a neon sign">'
           f'<title>Developer on a rooftop, day and night loop</title>' + "".join(parts) + '</svg>')
    return svg

if __name__ == "__main__":
    svg = build()
    open(os.path.join(OUT, "pixel-scene.svg"), "w").write(svg)
    print(len(svg)//1024, "KB")
