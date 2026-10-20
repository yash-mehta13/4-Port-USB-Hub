# Hardware validation checklist

For the first assembled board **after** the defects in [circuit-design](circuit-design.md#defect-register) are fixed. **No item below has been performed; all boxes are intentionally unchecked.** Record date, board revision, equipment and measured values for every step.

## 0. Before power
- [ ] Visual inspection (polarity of C1–C4/C19/C22/LED1, SSOP-28 orientation, connector solder joints).
- [ ] Continuity: no short between `VCC`, `+5V`, `GND`; no short between any D+/D− and a supply rail (this specifically catches the D2 class of fault).
- [ ] Connector pin check: pin 1 VBUS, 2 D−, 3 D+, 4 GND on every port (catches D3 class).

## 1. Power
- [ ] Current-limited bench supply on `CN1`; record start-up current.
- [ ] Measure `VCC`, `DVDD`, `AVDD`, `+5V`, and the hub's internal-regulator pins (per datasheet).
- [ ] Confirm that the host VBUS is **not** back-fed when `CN1` is powered (measure with the host side open / a protected test host).
- [ ] Confirm behaviour with host only (no jack).

## 2. Controller
- [ ] 12 MHz at `X1/X2` (use a high-impedance probe; record amplitude).
- [ ] `RESET#` level/timing at power-up.
- [ ] `PSELF`, `PGANG` levels against datasheet strap requirements; LED1 state.

## 3. Enumeration and function
- [ ] Host enumerates the hub (record speed and descriptors).
- [ ] Each downstream port individually: low-/full-/high-speed device if supported.
- [ ] All ports populated simultaneously; data transfer test; connector orientation.
- [ ] Hot-plug / unplug repeatedly.

## 4. Power and protection
- [ ] VBUS at each port under load; record droop and ferrite/polyfuse drop.
- [ ] Polyfuse behaviour with a controlled overload (use a current-limited supply).
- [ ] Overcurrent reporting through `OVCURR#1` if applicable.
- [ ] Thermal inspection (IR camera/thermocouple) at max load.

## 5. Qualification (separate effort)
- [ ] ESD testing (IEC 61000-4-2 or equivalent), USB-IF compliance/eye-diagram, impedance coupon measurement, EMC. Not planned or performed.
