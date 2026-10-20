# Project overview

**Name:** 4-Port USB Hub / USB Hub Port Extender. **Author:** yash-mehta13. **EDA:** KiCad 8.0 (native files).

## Objective
Design a compact board that expands one upstream USB-A port into four downstream USB-A ports using a single hub controller (`IC1`, value `GL850G-HH`), with an external barrel-jack supply, per-port polyfuses/ferrites/bulk capacitors and SRV05-4 ESD arrays.

## Artifacts
| Artifact | File(s) |
|---|---|
| Schematic (1 sheet, A4, dated 2026-01-12) | `USB Hub Port Extender.kicad_sch` |
| PCB (4 layers, 55 × 65 mm, 54 footprints) | `USB Hub Port Extender.kicad_pcb` |
| Project / local settings | `.kicad_pro`, `.kicad_prl` |
| Library downloads (symbols, footprints, STEP) | root `ECS-…`, `MCP23017-E_SS…`, `PMV20EN…`, `SOP65P780X200-28N.kicad_mod`, `SOT23-BEC.kicad_mod`, `XTAL_…kicad_mod` |
| KiCad auto-backups (25 zip snapshots, 2026-01-13 → 01-22) | `USB Hub Port Extender-backups/` |
| Screenshots (8) | `docs/images/` |
| Footprint cache | `fp-info-cache` (machine-generated, tracked) |

## Intended use
Learning/portfolio hardware design for a self-powered USB 2.0-class hub. Intended speed, current budget and compliance targets are **not documented in the design** and are not claimed here.

## Current status
Design in progress. Audit found critical connectivity defects (see [circuit-design](circuit-design.md#defect-register)); ERC/DRC not run; never fabricated or tested. Treat the design as **not fabrication-ready**.

## Principal features (as drawn)
Upstream + 4 downstream Type-A ports; per-port PTC fuse, ferrite and bulk/bypass capacitance; three SRV05-4 ESD arrays; external DC input with a P-MOSFET link to host VBUS; gang-mode LED; 12 MHz crystal; 4-layer stackup with GND and +5V planes.
