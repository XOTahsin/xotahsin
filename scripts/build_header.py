import os
from textpath import text_path, text_width
OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
PF, I6, I5 = "playfair-display-latin-700-normal.woff", "inter-latin-600-normal.woff", "inter-latin-500-normal.woff"

def header():
    hello = text_path(I6, "HELLO, I'M", 13, 500, 62, tracking=9)
    name = text_path(PF, "Md Tahsin Islam", 64, 500, 125, tracking=2)
    roles = ["WEB DEVELOPER", "BASED IN BANGLADESH", "ALWAYS LEARNING · ALWAYS BUILDING"]
    role_svg = ""
    for i, r in enumerate(roles):
        d = text_path(I5, r, 15, 500, 176, tracking=6)
        begin = f' begin="{i*3}s"'
        role_svg += f'<path d="{d}" class="role" opacity="0"><animate attributeName="opacity" values="0;1;1;0;0" keyTimes="0;.05;.28;.33;1" dur="9s"{begin} repeatCount="indefinite"/></path>\n  '
    p = ""
    for cx, cy, r, v, dur in [(90,150,2,"170;40;170",12),(210,60,1.5,"60;170;60",14),(330,170,2,"170;50;170",16),(700,40,1.5,"40;170;40",13),(820,165,2,"165;45;165",15),(920,70,1.5,"70;165;70",11)]:
        p += f'<circle cx="{cx}" cy="{cy}" r="{r}" opacity=".45"><animate attributeName="cy" values="{v}" dur="{dur}s" repeatCount="indefinite"/></circle>'
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1000 210" role="img" aria-label="Md Tahsin Islam, web developer">
  <title>Md Tahsin Islam</title>
  <style>
    :root{{--bg1:#0b1026;--bg2:#161e4a;--accent:#6ee7ff;--t1:#ffffff;--t2:#9fe3ff;--t3:#c9a7ff;--sub:#9fb4e8}}
    @media (prefers-color-scheme: light){{:root{{--bg1:#eef3ff;--bg2:#d9e4ff;--accent:#0b7fa8;--t1:#14204f;--t2:#0b6e99;--t3:#6b3fd0;--sub:#3f5290}}}}
    .role{{fill:var(--sub)}} .hello{{fill:var(--accent)}} .dot{{fill:var(--accent)}}
  </style>
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="var(--bg1)"/>
      <stop offset=".5" stop-color="var(--bg2)"><animate attributeName="offset" values=".3;.7;.3" dur="10s" repeatCount="indefinite"/></stop>
      <stop offset="1" stop-color="var(--bg1)"/>
    </linearGradient>
    <linearGradient id="txt" x1="0" y1="0" x2="1" y2="0">
      <stop offset="0" stop-color="var(--t1)"/><stop offset=".55" stop-color="var(--t2)"/><stop offset="1" stop-color="var(--t3)"/>
    </linearGradient>
  </defs>
  <rect width="1000" height="210" rx="18" fill="url(#bg)"/>
  <rect x=".5" y=".5" width="999" height="209" rx="18" fill="none" stroke="var(--accent)" stroke-opacity=".3"/>
  <g class="dot">{p}</g>
  <path class="hello" d="{hello}" opacity="0"><animate attributeName="opacity" values="0;.9" dur="1s" fill="freeze"/></path>
  <path d="{name}" fill="url(#txt)" opacity="0"><animate attributeName="opacity" values="0;1" dur="1.6s" fill="freeze"/></path>
  <rect class="dot" x="500" y="140" width="0" height="2" opacity=".7"><animate attributeName="x" values="500;380" dur="1.6s" fill="freeze"/><animate attributeName="width" values="0;240" dur="1.6s" fill="freeze"/></rect>
  {role_svg}
</svg>'''

def divider():
    return '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 800 8" role="presentation">
  <style>:root{--a:#6ee7ff;--b:#c9a7ff;--d:#ffffff}@media (prefers-color-scheme: light){:root{--a:#0b7fa8;--b:#6b3fd0;--d:#14204f}}</style>
  <defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0">
    <stop offset="0" stop-color="var(--a)" stop-opacity="0"/><stop offset=".3" stop-color="var(--a)"/><stop offset=".7" stop-color="var(--b)"/><stop offset="1" stop-color="var(--b)" stop-opacity="0"/>
  </linearGradient></defs>
  <rect y="3" width="800" height="2" fill="url(#g)" opacity=".6"/>
  <circle cy="4" r="3" fill="var(--d)"><animate attributeName="cx" values="0;800" dur="6s" repeatCount="indefinite"/><animate attributeName="opacity" values="0;1;1;0" keyTimes="0;.1;.9;1" dur="6s" repeatCount="indefinite"/></circle>
</svg>'''

if __name__ == "__main__":
    open(os.path.join(OUT, "header.svg"), "w").write(header())
    open(os.path.join(OUT, "divider.svg"), "w").write(divider())
    print("ok")
