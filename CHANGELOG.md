# Changelog

## Unreleased – documentation and audit pass (2026-10-20)
No earlier releases exist. The native KiCad design files were **not modified**.

### Added
README.md, docs/ (overview, circuit design, PCB review, BOM, fabrication guide, validation report, hardware checklist, safety, troubleshooting, roadmap, licensing), docs/reports/ (script-generated netlists/statistics), tools/audit_netlist.py, CLAUDE.md, CONTRIBUTING.md, GitHub issue/PR templates.

### Changed
* Screenshots moved/renamed from root `Screenshot 2026-01-2x ….png` to `docs/images/` (descriptive names; content unchanged).
* `.gitignore` rewritten: the old first line was corrupted by a UTF-8 BOM (so `*.bak` never matched); added `fp-info-cache`, `.kicad_prl`, etc. Already-tracked `fp-info-cache` and `.kicad_prl` stay tracked until the owner runs `git rm --cached`.

### Found (not fixed)
Design defects D1–D6 listed in docs/circuit-design.md. ERC/DRC not run (KiCad 8 unavailable).
