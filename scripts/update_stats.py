"""Builds assets/stats.svg from live GitHub data (falls back to a snapshot offline).
Run by the GitHub Action daily. Needs GITHUB_TOKEN for contribution counts."""
import os, json, sys, urllib.request
from datetime import datetime, timezone
from theme import *

USER = os.environ.get("GH_USER", "XOTahsin")
TOKEN = os.environ.get("GITHUB_TOKEN", "")
LANGCOL = {"HTML": "#e34c26", "JavaScript": "#f1e05a", "TypeScript": "#3178c6", "CSS": "#9a6cf0", "Dart": "#00b4ab", "Python": "#3572a5", "Shell": "#89e051"}
SNAPSHOT = dict(repos=10, stars=0, followers=0, contrib=None, since=2025, langs={"HTML": 7, "TypeScript": 1, "JavaScript": 1})

def get(url, data=None):
    req = urllib.request.Request(url, data=data, headers={"User-Agent": "stats-card", **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    return json.load(urllib.request.urlopen(req, timeout=20))

def fetch():
    u = get(f"https://api.github.com/users/{USER}")
    repos = get(f"https://api.github.com/users/{USER}/repos?per_page=100&type=owner")
    langs = {}
    for r in repos:
        if r.get("fork"): continue
        try:
            for k, v in get(r["languages_url"]).items(): langs[k] = langs.get(k, 0) + v
        except Exception: pass
    contrib = None
    if TOKEN:
        q = json.dumps({"query": 'query($l:String!){user(login:$l){contributionsCollection{contributionCalendar{totalContributions}}}}', "variables": {"l": USER}}).encode()
        try: contrib = get("https://api.github.com/graphql", q)["data"]["user"]["contributionsCollection"]["contributionCalendar"]["totalContributions"]
        except Exception: pass
    return dict(repos=u["public_repos"], stars=sum(r["stargazers_count"] for r in repos), followers=u["followers"],
                contrib=contrib, since=int(u["created_at"][:4]), langs=langs)

def card(d):
    w, h = 880, 230
    b = card_bg(w, h, 16)
    b += T(I6, "GITHUB AT A GLANCE", 11, 28, 32, "a", "start", 3)
    stats = [("Public repos", d["repos"]), ("Stars earned", d["stars"]), ("Followers", d["followers"]),
             ("Contributions · 1 yr", d["contrib"] if d["contrib"] is not None else "–"), ("Building since", d["since"])]
    cw = (w - 56) / len(stats)
    for i, (k, v) in enumerate(stats):
        x = 28 + i * cw
        b += T(PF, str(v), 34, x, 84, "t")
        b += T(I5, k, 12, x, 106, "m")
    tot = sum(d["langs"].values()) or 1
    items = sorted(d["langs"].items(), key=lambda kv: -kv[1])[:6]
    b += T(I6, "TOP LANGUAGES", 11, 28, 148, "a", "start", 3)
    bx, bw = 28, w - 56
    b += f'<clipPath id="lc"><rect x="{bx}" y="160" width="{bw}" height="10" rx="5"/></clipPath><g clip-path="url(#lc)"><rect x="{bx}" y="160" width="{bw}" height="10" fill="var(--bar)"/>'
    x = bx
    for n, v in items:
        sw = bw * v / sum(v2 for _, v2 in items)
        b += f'<rect x="{x:.1f}" y="160" width="{sw:.1f}" height="10" fill="{LANGCOL.get(n, "#9fb4e8")}"/>'; x += sw
    b += '</g>'
    x = bx
    for n, v in items:
        pct = 100 * v / sum(v2 for _, v2 in items)
        lab = f"{n}  {pct:.0f}%"
        b += f'<circle cx="{x+4}" cy="196" r="4" fill="{LANGCOL.get(n, "#9fb4e8")}"/>' + T(I5, lab, 12, x+14, 200, "m")
        x += text_width(I5, lab, 12) + 40
    b += T(I5, "Updated " + datetime.now(timezone.utc).strftime("%d %b %Y"), 10.5, w-28, 32, "m", "end")
    return svg(w, h, b, "GitHub stats card")

if __name__ == "__main__":
    try: d = fetch()
    except Exception as e:
        print("live fetch failed, using snapshot:", e, file=sys.stderr); d = SNAPSHOT
    open(os.path.join(OUT, "stats.svg"), "w").write(card(d)); print("stats ok", d)
