"""Regenerates every SVG in /assets. Usage: pip install fonttools && python3 scripts/build_all.py"""
import build_header, scene, build_cards, update_stats, os
O = build_header.OUT
open(os.path.join(O, "header.svg"), "w").write(build_header.header())
open(os.path.join(O, "divider.svg"), "w").write(build_header.divider())
open(os.path.join(O, "pixel-scene.svg"), "w").write(scene.build())
build_cards.build()
d = update_stats.SNAPSHOT
open(os.path.join(O, "stats.svg"), "w").write(update_stats.card(d))
print("all assets rebuilt")
