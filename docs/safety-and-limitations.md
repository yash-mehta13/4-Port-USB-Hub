# Safety and limitations

* **Unvalidated design.** Verified faults (D2 supply/D− merge, D3 swap, D4, D5) mean a built board may not function and could stress a host. Do not connect it to a valuable host before fixing and bench-checking.
* **VBUS short/overcurrent.** Per-port polyfuses are drawn with only a "500mA" label; ratings, trip time and parts are unspecified. No per-port power switch exists. Total current budget is **not defined**, and the current available from the host alone versus four ports has not been analysed (check the USB specification and controller datasheet; do not assume each port can deliver a given current).
* **Backfeed.** `Q1` connects host VBUS and the jack rail; body-diode direction as drawn may feed the host. Analyse before powering both sources.
* **Thermal/copper.** All traces 0.2 mm (see [pcb-layout-review](pcb-layout-review.md)); power paths may overheat before the polyfuse trips.
* **ESD.** SRV05-4 parts are drawn but not verified in function or placement; no ESD test performed.
* **Jack.** Barrel connector voltage/polarity are not specified in the files; use a regulated 5 V supply only after confirming.
* **Limits of EDA checks.** ERC/DRC (not yet run) cannot prove electrical function, signal integrity or USB compliance.
