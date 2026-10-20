# Contributing

## Prerequisites
KiCad 8.x with standard libraries; Python 3 (optional, for `tools/audit_netlist.py`).

## Open and validate
Open `USB Hub Port Extender.kicad_pro`. Run ERC (schematic) and DRC (PCB), update the PCB from the schematic, and record results in `docs/validation-report.md`. Run `python3 -I tools/audit_netlist.py` to refresh `docs/reports/` if connectivity changed.

## Reporting problems
Use the issue templates. For schematic/PCB problems give reference designators, net names, screenshot and KiCad version.

## Proposing changes
* Component/footprint changes: state the datasheet, package and why; update `docs/bill-of-materials.csv` and `docs/circuit-design.md`.
* Include evidence (datasheet page, calculation, ERC/DRC output, measurement) for electrical changes.
* Do not commit generated Gerbers unless asked; attach them to the PR for review, and state the stackup assumed.
* Physical tests: add date, board revision, equipment, measured values and photos to `docs/hardware-validation.md`; never mark a test done without evidence.
* Keep `.kicad_prl`, `fp-info-cache` and lock/backup files out of commits.
