# How to edit
- Project cards, skills and levels: edit `PROJECTS` / `SKILLS` in `scripts/build_cards.py`.
- "Currently" block: edit the `cols` list in `currently()` in the same file.
- Pixel scene: `scripts/scene.py` (sprites are ASCII grids, 1 character = 1 pixel).
- Rebuild everything: `pip install fonttools` then `python3 scripts/build_all.py` (run from the repo root).
- The stats card and snake refresh through `.github/workflows/update-profile.yml`.
  One-time setup: Settings > Actions > General > Workflow permissions > Read and write.
