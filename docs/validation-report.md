# Validation report

Date: 2026-10-20. Environment: Ubuntu 24.04 container, Python 3.13. Project files saved by KiCad 8.0 (schematic format 20231120, PCB format 20240108).

## Tooling
| Item | Result |
|---|---|
| `kicad-cli` / KiCad | **Not installed.** `apt` only offers KiCad 7.0.11, which cannot open KiCad 8 files; the KiCad 8 PPA was unreachable (HTTP 403 from the network proxy). Not installed to avoid a misleading result. |
| Internet datasheet access | GL850G datasheet **not retrieved** (one web search returned only a secondary source; direct fetch failed) |

## Checks actually executed
| Check | How | Result |
|---|---|---|
| Schematic connectivity | `tools/audit_netlist.py` (wires, junctions, labels, power symbols, pin geometry) → [reports/schematic-netlist.txt](reports/schematic-netlist.txt) | 47 nets; defects D2–D5 found |
| PCB nets/pads | same script → [reports/pcb-pad-nets.txt](reports/pcb-pad-nets.txt), [reports/pcb-statistics.txt](reports/pcb-statistics.txt) | 54 footprints, 450 segments, 45 vias, 2 zones |
| Schematic ↔ PCB consistency | compared pad-net partitions | identical except `J1` pin 5 (D6) |
| BOM ↔ PCB | reference set compared | 54/54 references agree |
| Screenshot review | viewed all 8 PNGs | mapped in README |

The script is an independent reimplementation and may mis-trace unusual geometry; KiCad's own netlist is authoritative.

## Checks NOT run (blocked: no KiCad 8)
ERC, DRC, footprint-assignment check, unconnected-pad/ratsnest check, library-resolution check, KiCad BOM/netlist export, Gerber, drill, position, STEP export. **No ERC/DRC result exists; do not assume clean.** Expected ERC findings based on the audit: pin-type/mislabeled-pin errors on `IC1`, multiple net names on the VCC/`USB2_N` net, label mismatches.

## Outstanding checks
Run ERC/DRC in KiCad 8; verify GL850G pinout/straps/package against the official datasheet; fabricator DRC; impedance with a field solver and fabricator stackup; all items in [hardware-validation](hardware-validation.md). Unverified-by-anyone: USB compliance, signal integrity, ESD, current limits, thermal.
