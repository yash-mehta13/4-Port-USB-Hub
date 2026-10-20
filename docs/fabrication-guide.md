# Fabrication guide

**Status: not ready to order.** Resolve the defects in [circuit-design](circuit-design.md#defect-register) first. This guide lists the process; no outputs have been generated.

## Before generating outputs
1. Open the project in KiCad 8.x. Review schematic and PCB.
2. Fix D1–D6, update PCB from schematic (F8), re-route affected nets.
3. Run ERC and DRC; resolve or document each item.
4. Check Edge.Cuts is a closed outline; check each footprint against its real datasheet (especially `IC1` package, USB connectors, polyfuse and MOSFET once chosen).
5. Replace placeholder stackup values (core `epsilon_r 1`) with the fabricator's.

## Outputs (KiCad GUI, version-dependent)
* **Gerbers:** File → Fabrication Outputs → Gerbers. Copper layers `F.Cu`, `In1.Cu`, `In2.Cu`, `B.Cu`, mask, paste, silkscreen, `Edge.Cuts`.
* **Drill:** Generate Drill Files (Excellon, PTH and NPTH).
* **Position file:** Fabrication Outputs → Component Placement (if assembly is ordered).
* **BOM:** Schematic Editor → Tools → Generate BOM, then merge with [bill-of-materials.csv](bill-of-materials.csv) and resolve every "unresolved" MPN.
* Preview the result in a Gerber viewer. `kicad-cli` equivalents (`kicad-cli sch erc`, `pcb drc`, `pcb export gerbers/drill/pos`) exist in KiCad 8 but were **not run here**; check `kicad-cli <cmd> --help` for your version.

## What to give a fabricator
Gerbers, drill files, board thickness (1.6 mm in file), layer count (4), stackup and controlled-impedance requirement (if any), copper weight, mask/silkscreen colour, surface finish and tolerances. **These are not defined in the design** (finish is "None" in the file) and must be chosen by the owner. Ask the fabricator for the stackup they will build and use it for the USB pair geometry.

## Reproducing the review
1. Install KiCad 8.x with standard libraries.
2. Clone the repo; open `USB Hub Port Extender.kicad_pro`. (`${KICAD8_3DMODEL_DIR}` is resolved by KiCad.)
3. Inspect schematic and PCB; run ERC and DRC.
4. `python3 -I tools/audit_netlist.py` regenerates [reports/](reports/) without KiCad.
5. Export netlist/BOM/Gerbers/drill as above; preview.
6. After fabrication, follow [hardware-validation](hardware-validation.md).
The project depends only on KiCad's stock libraries plus the embedded symbols; the custom library files are not required by the current PCB.
