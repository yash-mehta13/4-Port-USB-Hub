# PCB layout review

Sources: `USB Hub Port Extender.kicad_pcb`, `.kicad_pro`, and [reports/pcb-statistics.txt](reports/pcb-statistics.txt). KiCad DRC was **not run**; this is a file-level inspection plus screenshots.

## Board facts [from file]
| Property | Value |
|---|---|
| Outline | Edge.Cuts bounding box 55 × 65 mm (x 145–200, y 59–124), 4 lines + 4 arcs (rounded corners) |
| Stackup | `F.Cu` / `In1.Cu` "GND" / `In2.Cu` "PWR" / `B.Cu`; 1.6 mm; Cu 35 µm; prepreg 0.1 mm (εr 4.5) outer, core 1.24 mm. The core entry has `epsilon_r 1`, `loss_tangent 0` – a placeholder, not a real material value. Copper finish "None"; `dielectric_constraints no` |
| Zones | `In1.Cu` GND, `In2.Cu` net `+5V` (upstream VBUS after `L1`) – there is no plane for the downstream `VCC` rail |
| Tracks | 450 segments, **all 0.2 mm** (power, VBUS and data alike) |
| Vias | 45, all 0.6 mm / 0.3 mm drill |
| Footprints | 54, all on `F.Cu`; no mounting holes found |
| Rules in `.kicad_pro` | min clearance 0.2 (netclass), min copper-edge 0.5, min via annular 0.1, min through-hole 0.3, hole clearance 0.25. Not tied to any named fabricator |
| Net classes | `Default` and `USD_diff` (name likely a typo of USB) 0.2 width / 0.15 gap assigned by pattern `USB*` |
| Other | Large "KiCad" logo text (10 mm) on `B.Cu` – copper graphic, almost certainly unintentional |

## USB data routing
Segment-length sums per net (exclude vias/pads) [from file]:

| Pair | N (mm) | P (mm) | Note |
|---|---|---|---|
| USB0 (upstream) | 41.9 | 37.0 | both use B.Cu segments |
| USB1 | 98.4 | 104.5 | long routes |
| USB3 | 51.0 | 46.7 | |
| USB4 | 29.7 | 57.1 | ~27 mm difference; N has 8 B.Cu segments, P is all F.Cu |
| USB2 | n/a | 31.6 | N is merged with VCC (D2), sum meaningless |

* Unmatched pair lengths and layer changes on one side only (USB4) are layout risks for high-speed signalling; whether skew matters depends on the speed mode, which is unconfirmed.
* 0.2 mm width / 0.15 mm gap over 0.1 mm prepreg to the GND plane. A first-order microstrip estimate (IPC-2141-style, [C]) gives roughly 40 Ω single-ended and ~70 Ω differential, below the common 90 Ω USB target. This is an order-of-magnitude check using the stackup values in the file, not a field-solver result or a proof; the fabricator's actual stackup and a proper calculator must decide. Neither compliance nor impedance has been measured.
* Reference-plane continuity, via return paths, stubs and proximity to switching/noisy nets were not analysed beyond the above; do this in KiCad (3D/flat view, DRC, length-tuning tools).
* Differential pair routing (coupled routing) cannot be confirmed from segment lists; check visually in pcbnew.

## Power routing
* VBUS nets and `+5V`/`VCC` use the same 0.2 mm tracks. A rough IPC-2221 external-layer estimate [C] for 0.2 mm × 35 µm at 10 °C rise is ≈0.7 A – comparable to one port's 500 mA label, and well below what a shared `VCC` trunk feeding four ports could draw. Widen/pour power paths and define a current budget [R].
* Bulk and bypass capacitors are placed near each connector (visual); `IC1` has several 0603 bypass caps within ~10 mm.
* GND is the whole `In1.Cu`; ground vias: 10.

## Connectors and mechanics
Three Molex 67643 footprints (J1–J3), a CNC Tech 1001-011-01101 footprint (J4), a Molex 48037-2200 edge footprint (J5, upstream) and a barrel jack. Footprint families differ between ports; confirm real parts, shield connections (D6) and that J5's board-edge position matches the intended enclosure. The IC1 footprint is stock SSOP-28 (not the custom SOP65P780X200-28N).

## Manufacturability (unverified)
Not assessed against any fabricator: via/drill/annular limits, copper-to-edge, solder-mask slivers, silkscreen overlap, courtyard collisions. Run DRC and a fabricator's online checker.

## Proposed improvements [R]
Fix D2–D6 first and re-route affected nets; define a diff-pair class with computed width/gap for the chosen stackup; length-match pairs and keep them on one layer; widen power; add mounting holes/test points; remove the copper logo or move it to silkscreen.
