# Decisions and roadmap

## Observed decisions (from the files)
* Single-chip hub (`GL850G-HH` per value) in SSOP-28 on a 4-layer board with GND and `+5V` planes.
* External DC input with a P-MOSFET link to host VBUS instead of a dedicated power-switch IC.
* Passive per-port protection: polyfuse + ferrite + bulk/bypass capacitors; ESD via SRV05-4 arrays shared between two ports.
* Single 0.2 mm track width everywhere; `USD_diff` net class for `USB*`.
* Stock KiCad footprints/3D models used instead of the downloaded custom footprints.

## Suggested improvements (suggestions, not claims)
1. Fix D1–D6; add a correct GL850G symbol/footprint verified against the datasheet.
2. Define current budget; choose polyfuses and justify the P-MOSFET switchover (or use a purpose-built power-path/power-switch IC).
3. Diff-pair rules from the fabricator's stackup; match lengths; widen power; add mounting holes and test points (VCC, +5V, DVDD, AVDD, RESET#, X1).
4. Explicit MPNs and sourcing in the schematic fields; fix `USD_diff` typo; remove the copper logo.
5. Re-position ESD parts near connectors; add a PCB/3D review pass.
6. Bench-test report, board photograph, enclosure documentation.
