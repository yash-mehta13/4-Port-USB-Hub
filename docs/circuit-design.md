# Circuit design

Evidence legend: **[F]** read from the KiCad files (schematic connectivity rebuilt by `tools/audit_netlist.py`, cross-checked against pad nets stored in the PCB), **[L]** read from a library/symbol property, **[C]** simple engineering calculation, **[R]** recommendation. Nothing here is a measurement. KiCad ERC was **not** run ([validation-report](validation-report.md)). Full derived netlist: [reports/schematic-netlist.txt](reports/schematic-netlist.txt).

## Defect register
| ID | Severity | Finding | Evidence |
|---|---|---|---|
| D1 | High | `IC1` (value `GL850G-HH`) uses library symbol `MCP23017-E_SS:MCP23017-E_SS`; pin names (`GPB0…`, `SCL`, `SDA`, `A0–A2`, `INTA/B`) and properties (Microchip MCP23017-E/SS, DigiKey/Mouser data) belong to an I²C I/O expander. Hub pin functions are therefore mislabeled and ERC cannot be meaningful. | [F] schematic `lib_symbols`, PCB net names `Net-(IC1-GPB0)` etc. |
| D2 | **Critical** | Net `USB2_N,VCC`: a `USB2_N` global label sits on the VCC wire. One net joins `J2.2` (D−), `IC1.2`, `IC1.23`, `IC2.3/5`, `IC3.5`, `Q1.3`, `CN1.1`, `R1–R4.1`, `R13.1`, `R6.2`, `C16/17/21/22.1`. PCB names the same net `USB2_N`. Port 2 D− is shorted to the supply rail. | [F] netlist + PCB pads |
| D3 | High | Port 1 data swapped: `J1.2` (D− contact) = `USB1_P`, `J1.3` (D+) = `USB1_N`; `J2–J5` are D−→`_N`, D+→`_P`. | [F] |
| D4 | High | `RESET#` label touches only `IC1.13`; the reset network node (`R8.2`,`R9.1`,`C15.1`) has no label and is an isolated net. | [F] |
| D5 | Medium | Overcurrent divider output is labeled `OVCURR1#`; `IC1.21` is labeled `OVCURR#1`. Different nets, so pin 21 has no bias. | [F] |
| D6 | Low | `J1` pin 5 (shield) unconnected in the schematic but `GND` in the PCB (the only schematic↔PCB net difference found). Verify in KiCad. | [F] |

Items needing verification against the official GL850G datasheet (not retrieved; a secondary web source listed pins 25/26 = DM0/DP0 and 21 = OVCUR1#, consistent with this design, but the rest is unconfirmed): function of pins 1, 4, 5, 10 (each carries only a capacitor or resistor to ground), 23, 17, 18, 13, supply pin mapping, and package outline.

## Section walkthrough
### Hub controller (`IC1`)
Footprint `Package_SO:SSOP-28_5.3x10.2mm_P0.65mm` [F]. Pin-to-net map (PCB, [reports/pcb-pad-nets.txt](reports/pcb-pad-nets.txt)): upstream `USB0_N/P` pins 25/26; `USB1` 27/28; `USB2` 2/3; `USB3` 8/9; `USB4` 11/12; `X1`/`X2` pins 6/7; `RESET#` 13; `PSELF` 17; `PGANG` 18; `OVCURR#1` 21; `DVDD` pins 16 and 24; `GND` pin 15; pins 14, 19, 20, 22 carry no-connect markers. Pins 1 (`C12`), 5 (`C11`,`C14`), 10 (`C13`) and 4 (`R5` 680 Ω) connect only to passives to GND [F] – plausibly regulator-bypass/bias pins, to be confirmed. The hub IC's 5 V supply pin is presumed to be pin 23 (on the VCC net); unverified.

### Clock (`Y1`, `C9`, `C10`)
12 MHz, 18 pF CL crystal [L]; two 33 pF to GND. First-order load: 33 pF ‖ 33 pF series = 16.5 pF + stray [C], reasonable for 18 pF – layout stray not assessed. Nets `X1`/`X2` ↔ `IC1` pins 6/7.

### Configuration
`PSELF` (pin 17): `R13` 470 kΩ to VCC, `R12` 470 Ω to the `Q1` gate, `CN1` pin 3. `PGANG` (pin 18): `R11` 100 kΩ to `AVDD`; `LED1` (red) with `R10` 470 Ω forms the "gang indicator". Whether these are the correct strap polarities is **unverified** pending the datasheet. Unused pins 14/19/20/22 are marked no-connect.

### Reset (`R8` 10 k to `+5V`, `R9` 47 k to GND, `C15` 0.1 µF across R9)
Divider midpoint ≈ 4.1 V from 5 V [C] but not connected to `RESET#` (D4).

### Upstream (`J5`, `L1`, `IC4`)
`J5` Type-A, D−=`USB0_N`, D+=`USB0_P`; VBUS → `L1` (FB-0603-2A) → `+5V`; `IC4` SRV05-4 channels IO1/IO2 on D+/D−, pin 5 on `+5V`, IO3/IO4 unused. `+5V` also feeds `R8`, `Q1` source.

### Downstream (`J1`–`J4`)
Per port: VCC → polyfuse (`R1`..`R4`, value "500mA") → ferrite (`L2`..`L5`) → VBUS, with `C1..C4` 100 µF and `C5..C8` 0.1 µF at the connector. Mapping: J1→R1/L2/C1/C5, J2→R3/L3/C2/C6, J3→R2/L4/C3/C7, J4→R4/L5/C4/C8 (`R3` feeds J2 and `R2` feeds J3 per the pad nets). ESD: `IC2` serves ports 1–2, `IC3` ports 3–4 (IC3.5 supply pin on the merged net D2). Polyfuses are drawn but their trip/hold ratings are undefined; there is no per-port power switch, so the hub's overcurrent input cannot see a switch fault flag.

### Power distribution
`CN1` (barrel, switch contact → `PSELF`) → `VCC`, `C21` 0.1 µF, `C22` 100 µF. `Q1` (generic P-MOSFET, source `+5V`, drain `VCC`, gate via `R12` to `PSELF`, `R13` pulls `PSELF` to `VCC`). Behaviour is not simulated. **Risk [R]:** with source on host VBUS and drain on VCC the intrinsic body diode points from VCC toward `+5V`, which can feed the host when the jack is powered; the intended switchover and backfeed behaviour must be analysed. `AVDD` = `DVDD` via `L6`, with `C18/C16` and `C19/C17/C20` decoupling.

### Protection summary
ESD arrays are present and wired to data lines (`IC2`–`IC4`), but their effectiveness is not verified, and with D2 their supply pin is on a net shorted to a data line. Do not describe ports as ESD-protected until fixed and tested.

## Library usage
| File | Used by current design? |
|---|---|
| `MCP23017-E_SS.kicad_sym` | symbol embedded and used by `IC1` (**wrongly**, D1) |
| `SOP65P780X200-28N.kicad_mod` | no – `IC1` uses stock SSOP-28 5.3×10.2 mm; compare outlines before choosing |
| `ECS-120-18-4X-CKM.kicad_sym` | symbol used by `Y1` |
| `XTAL_ECS-120-18-4X-CKM.kicad_mod` | no – `Y1` uses stock `Crystal_SMD_HC49-SD`; custom one is through-hole |
| `PMV20EN.kicad_sym`, `SOT23-BEC.kicad_mod` | no – N-channel MOSFET, `Q1` is a generic P-MOSFET |
| `*.step`, `*.zip` | not referenced by the PCB (all footprints use `${KICAD8_3DMODEL_DIR}` stock models) |
