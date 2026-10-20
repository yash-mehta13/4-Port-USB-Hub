# Troubleshooting

| Symptom | Design-relevant causes to check |
|---|---|
| Hub does not enumerate | `RESET#` unconnected/floating (D4); crystal not oscillating (`Y1`, `C9/C10`); wrong controller pin map (D1); upstream D+/D− (`J5`, `IC4`); supply rails |
| Port 1 not working / device resets | D+/D− swapped at `J1` (D3) |
| Port 2 dead or 5 V on data pin | `USB2_N` merged with VCC (D2) – measure D− to GND with power off |
| Overcurrent never reported / odd behaviour | label mismatch `OVCURR1#`/`OVCURR#1` (D5) |
| Unstable or disconnecting devices | insufficient power budget, polyfuse tripped (let cool), skewed/unmatched pair routing, unwanted plane crossings |
| Hot components / shorts | polyfuse/ferrite undersized, VBUS short, 0.2 mm tracks |
| Host powers up/back-fed | `Q1` body-diode path with jack connected |
| KiCad can't open file | need KiCad 8.x |
| Missing footprint/model warnings | standard KiCad 8 libraries not installed; `${KICAD8_3DMODEL_DIR}` unset; custom files aren't registered in any lib table |
| Schematic symbol mismatch | `IC1` uses the MCP23017 symbol (D1) |
