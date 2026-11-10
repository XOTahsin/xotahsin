import os, math
from theme import *

LANGCOL = {"HTML": "#e34c26", "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "CSS": "#9a6cf0", "Dart": "#00b4ab"}

PROJECTS = [  # edit freely, then run: python3 scripts/build_all.py
 dict(slug="regnar", name="Regnar", lang="HTML", url="https://github.com/XOTahsin/Regnar", live="regnar.vercel.app",
      desc="Premium framed wall-art storefront with a private admin dashboard. Enquiry-based ordering over WhatsApp, in English and Arabic.",
      tags=["HTML", "CSS", "JavaScript", "Supabase"]),
 dict(slug="area-dna-bangladesh", name="AREA DNA Bangladesh", lang="TypeScript", url="https://github.com/XOTahsin/area-dna-bangladesh", live="",
      desc="A platform that shows the real picture of your local area in one place, built stage by stage with typed, linted code.",
      tags=["TypeScript", "Next.js", "Node 20"]),
 dict(slug="studyflow-v2", name="StudyFlow V2", lang="HTML", url="https://github.com/XOTahsin/StudyFlow-V2", live="",
      desc="Second version of my study-planning web app, built to keep study sessions organised and consistent.",
      tags=["HTML", "CSS", "JavaScript"]),
 dict(slug="studymate", name="StudyMate", lang="HTML", url="https://github.com/XOTahsin/StudyMate", live="",
      desc="A study companion web app for students, part of my self-improvement and study-systems work.",
      tags=["HTML", "CSS", "JavaScript"]),
 dict(slug="vaultx-v2", name="Vaultx V2", lang="HTML", url="https://github.com/XOTahsin/Vaultx-v2", live="",
      desc="Second iteration of Vaultx, a lightweight web app built with plain HTML, CSS and JavaScript.",
      tags=["HTML", "CSS", "JavaScript"]),
 dict(slug="bup-mark-calculator", name="BUP Mark Calculator", lang="HTML", url="https://github.com/XOTahsin/Bup-Mark-Calculator", live="",
      desc="A quick marks and grade calculator for BUP students, built as a simple, fast web tool.",
      tags=["HTML", "CSS", "JavaScript"]),
]

def project_card(p):
    w, h = 420, 168
    b = card_bg(w, h)
    b += f'<rect x="1" y="1" width="{w-2}" height="4" rx="2" fill="url(#g)" opacity=".9"><animate attributeName="opacity" values=".55;1;.55" dur="5s" repeatCount="indefinite"/></rect>'
    b += T(I6, p["name"], 19, 22, 38, "t")
    b += f'<circle cx="{w-30}" cy="32" r="3.5" fill="{LANGCOL.get(p["lang"], "#9fb4e8")}"/>'
    b += T(I5, p["lang"], 11, w-38, 36, "m", "end")
    y = 62
    for ln in wrap(I5, p["desc"], 12.5, w-44)[:3]:
        b += T(I5, ln, 12.5, 22, y, "m"); y += 18
    x = 22
    for tag in p["tags"]:
        tw = text_width(I5, tag, 10.5) + 16
        b += f'<rect x="{x}" y="{h-36}" width="{tw:.1f}" height="21" rx="10.5" fill="var(--card2)" stroke="var(--bd)"/>' + T(I5, tag, 10.5, x+tw/2, h-21.5, "a", "middle")
        x += tw + 6
    label = "LIVE ↗" if p["live"] else "VIEW ↗"
    return svg(w, h, b, f'{p["name"]} project card')

def currently():
    w, h = 880, 150
    b = card_bg(w, h, 16)
    cols = [("BUILDING", "Study & productivity apps", "Habit trackers, study planners and self-improvement tools."),
            ("LEARNING", "Full-stack architecture", "Next.js, TypeScript, Supabase and clean app structure."),
            ("OPEN TO", "Freelance & collabs", "Web apps, landing pages and thoughtful UI work.")]
    cw = (w - 40) / 3
    for i, (k, t, d) in enumerate(cols):
        x = 24 + i * cw
        if i: b += f'<rect x="{x-14:.1f}" y="26" width="1" height="{h-52}" fill="var(--bd)"/>'
        b += f'<circle cx="{x+4:.1f}" cy="38" r="4" fill="url(#g)"><animate attributeName="r" values="3;5;3" dur="{3+i*.7}s" repeatCount="indefinite"/></circle>'
        b += T(I6, k, 11, x+16, 42, "a", "start", 3)
        b += T(PF, t, 19, x, 76, "t")
        for j, ln in enumerate(wrap(I5, d, 12.5, cw-32)[:3]):
            b += T(I5, ln, 12.5, x, 100 + j*17, "m")
    return svg(w, h, b, "Currently: building, learning, open to")

SKILLS = [("HTML & CSS", 92), ("JavaScript", 82), ("TypeScript", 68), ("Next.js / React", 62), ("Supabase & Postgres", 60), ("Flutter", 50), ("Git & GitHub", 76)]
def skills():
    w, rh = 880, 38
    h = 36 + len(SKILLS) * rh + 14
    b = card_bg(w, h, 16)
    b += T(I6, "SKILLS", 11, 28, 30, "a", "start", 3)
    bw = 520
    for i, (n, v) in enumerate(SKILLS):
        y = 56 + i * rh
        b += T(I6, n, 13.5, 28, y+14, "t")
        b += f'<rect x="250" y="{y+4}" width="{bw}" height="10" rx="5" fill="var(--bar)"/>'
        b += f'<rect x="250" y="{y+4}" width="0" height="10" rx="5" fill="url(#g)"><animate attributeName="width" values="0;{bw*v/100:.0f}" dur="1.2s" begin="{.15*i:.2f}s" fill="freeze" calcMode="spline" keyTimes="0;1" keySplines=".2 .8 .2 1"/></rect>'
        b += T(I6, f"{v}%", 12.5, 250+bw+16, y+14, "m")
    return svg(w, h, b, "Skills with proficiency bars")

def wave_path(amp, period, phase, base, width):
    pts = []
    for x in range(0, width+1, 10):
        pts.append(f"{x},{base + amp*math.sin(2*math.pi*(x+phase)/period):.1f}")
    return "M" + " L".join(pts) + f" L{width},120 L0,120 Z"

def footer():
    w, h = 1000, 120
    body = ""
    for i, (amp, per, op, dur, col) in enumerate([(9, 250, .35, 14, "var(--ac)"), (7, 333, .28, 20, "var(--ac2)"), (5, 200, .5, 10, "var(--ac)")]):
        d = wave_path(amp, per, i*70, 60 + i*14, w*2 + per)
        body += f'<g opacity="{op}"><path d="{d}" fill="{col}"><animateTransform attributeName="transform" type="translate" values="0 0;-{per} 0" dur="{dur}s" repeatCount="indefinite"/></path></g>'
    body += T(I5, "© 2026 Md Tahsin Islam · built with HTML, CSS, SVG and curiosity", 12, 500, 104, "m", "middle")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Animated footer wave"><title>Footer</title>{STYLE}{body}</svg>')

def cta():
    w, h = 340, 64
    b = f'<defs><clipPath id="c"><rect x="2" y="2" width="{w-4}" height="{h-4}" rx="30"/></clipPath></defs>'
    b += f'<rect x="2" y="2" width="{w-4}" height="{h-4}" rx="30" fill="url(#g)"/>'
    b += f'<g clip-path="url(#c)"><rect x="-80" y="0" width="50" height="{h}" fill="#fff" opacity=".28" transform="skewX(-20)"><animate attributeName="x" values="-90;{w+60}" dur="3.4s" repeatCount="indefinite"/></rect></g>'
    tw = text_width(I6, "Let’s build something", 17, .5)
    x0 = w/2 - (tw+30)/2
    b += f'<path fill="#0b1026" d="{text_path(I6, "Let’s build something", 17, x0+tw/2, 38.5, "middle", 0.5)}"/>'
    ax = x0 + tw + 12
    b += f'<path d="M{ax:.1f} 32h14M{ax+8:.1f} 26l6 6-6 6" fill="none" stroke="#0b1026" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><animateTransform attributeName="transform" type="translate" values="0 0;3 0;0 0" dur="1.6s" repeatCount="indefinite"/></path>'
    return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" role="img" aria-label="Let’s build something"><title>Let’s build something</title>{STYLE}<defs><linearGradient id="g" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#6ee7ff"/><stop offset="1" stop-color="#c9a7ff"/></linearGradient></defs>{b}</svg>')

def build():
    for p in PROJECTS:
        open(os.path.join(OUT, f"project-{p['slug']}.svg"), "w").write(project_card(p))
    for n, f in [("currently", currently), ("skills", skills), ("footer", footer), ("cta", cta)]:
        open(os.path.join(OUT, f"{n}.svg"), "w").write(f())

if __name__ == "__main__":
    build(); print("cards ok")
