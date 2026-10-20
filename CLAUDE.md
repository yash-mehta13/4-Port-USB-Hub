# CLAUDE.md – instructions for AI assistants

* Inspect the native KiCad project (`USB Hub Port Extender.kicad_sch/.kicad_pcb/.kicad_pro`) before any edit. Files are KiCad 8.0 format; never save them with an older KiCad.
* Preserve the schematic, PCB, settings, libraries, STEP/ZIP files, screenshots and `USB Hub Port Extender-backups/`. No destructive git commands; do not commit/push without the owner's request.
* Verify hardware facts from the files or authoritative datasheets. Never invent part numbers, ratings, test results, USB compliance, ESD protection or fabrication readiness. Label statements as file-derived, datasheet-derived, calculated, recommended or measured.
* Treat electrical changes (nets, pin maps, values, footprints, routing) as engineering changes with evidence and a changelog entry, not cosmetic edits. The known defect list is in `docs/circuit-design.md`; do not silently "fix" items without owner review.
* Use `kicad-cli` only after checking `kicad-cli <command> --help` for the installed version. If KiCad 8 is unavailable, say so; `tools/audit_netlist.py` is a helper, not ERC/DRC.
* Keep custom libraries; use project-relative paths, no absolute machine paths. Don't break `${KICAD8_3DMODEL_DIR}` model references.
* Keep docs consistent with `docs/bill-of-materials.csv` and `docs/images/` paths.
