#!/usr/bin/env python3
"""Read-only audit helper for the native KiCad 8 files (no KiCad install needed).

Parses the .kicad_sch / .kicad_pcb s-expressions, rebuilds the schematic
connectivity from wires/labels/pin positions, and writes:
  docs/reports/schematic-netlist.txt   nets derived from the schematic
  docs/reports/pcb-pad-nets.txt        nets as stored in the PCB
  docs/reports/pcb-statistics.txt      track/via/zone statistics
  docs/bill-of-materials.csv is NOT written here (hand-maintained).
It is NOT a replacement for KiCad ERC/DRC. Usage: python3 -I tools/audit_netlist.py
"""
import math, re, sys
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
NAME = "USB Hub Port Extender"


def parse(text):
    tok = re.findall(r'"(?:\\.|[^"\\])*"|\(|\)|[^\s()]+', text)
    i = 0
    def rd():
        nonlocal i
        if tok[i] == "(":
            i += 1; out = []
            while tok[i] != ")": out.append(rd())
            i += 1; return out
        v = tok[i]; i += 1
        return v[1:-1] if v.startswith('"') else v
    return rd()


def find(n, k):
    return [x for x in n if isinstance(x, list) and x and x[0] == k]


def xy(node):
    a = find(node, "at")[0]
    return float(a[1]), float(a[2])


def rnd(p):
    return (round(p[0], 2), round(p[1], 2))


def schematic_nets(t):
    libs = {}
    for s in find(find(t, "lib_symbols")[0], "symbol"):
        pins = {}
        def walk(n):
            for c in n:
                if isinstance(c, list):
                    if c[0] == "pin":
                        pins[find(c, "number")[0][1]] = (*xy(c), find(c, "name")[0][1])
                    elif c[0] == "symbol":
                        walk(c)
        walk(s); libs[s[1]] = pins
    par = {}
    def f(a):
        par.setdefault(a, a)
        while par[a] != a:
            par[a] = par[par[a]]; a = par[a]
        return a
    def u(a, b): par[f(a)] = f(b)
    segs = []
    for w in find(t, "wire"):
        p = find(find(w, "pts")[0], "xy")
        a = rnd((float(p[0][1]), float(p[0][2]))); b = rnd((float(p[1][1]), float(p[1][2])))
        u(a, b); segs.append((a, b))
    def onseg(p, a, b):
        if abs((b[0]-a[0])*(p[1]-a[1]) - (b[1]-a[1])*(p[0]-a[0])) > 0.02: return False
        return min(a[0], b[0])-.01 <= p[0] <= max(a[0], b[0])+.01 and min(a[1], b[1])-.01 <= p[1] <= max(a[1], b[1])+.01
    pinpts, power = [], defaultdict(list)
    for s in find(t, "symbol"):
        p = {q[1]: q[2] for q in find(s, "property")}
        at = find(s, "at")[0]; x0, y0 = float(at[1]), float(at[2]); rot = float(at[3]) if len(at) > 3 else 0
        mir = find(s, "mirror"); mir = mir[0][1] if mir else ""
        for num, (px, py, nm) in libs[find(s, "lib_id")[0][1]].items():
            x, y = px, -py
            if mir == "x": y = -y
            if mir == "y": x = -x
            for _ in range(int(round(rot / 90)) % 4): x, y = y, -x
            pt = rnd((x0 + x, y0 + y)); f(pt)
            pinpts.append((p["Reference"], num, nm, pt))
            if p["Reference"].startswith("#PWR"): power[p["Value"]].append(pt)
    for j in find(t, "junction"): f(rnd(xy(j)))
    for p in list(par):
        for a, b in segs:
            if p != a and p != b and onseg(p, a, b): u(p, a)
    labels = defaultdict(list)
    for k in ("label", "global_label"):
        for l in find(t, k):
            pt = rnd(xy(l)); f(pt)
            for a, b in segs:
                if onseg(pt, a, b): u(pt, a)
            labels[l[1]].append(pt)
    for pts in list(labels.values()) + list(power.values()):
        for p in pts[1:]: u(pts[0], p)
    names = defaultdict(set)
    for n, pts in labels.items(): names[f(pts[0])].add(n)
    for n, pts in power.items(): names[f(pts[0])].add(n)
    nc = {f(rnd(xy(x))) for x in find(t, "no_connect")}
    nets = defaultdict(list)
    for ref, num, nm, pt in pinpts:
        if not ref.startswith("#"): nets[f(pt)].append((ref, num, nm))
    return [(",".join(sorted(names.get(r, []))) or "(unnamed)", sorted(pl), r in nc) for r, pl in nets.items()]


def main():
    sch = parse((ROOT / f"{NAME}.kicad_sch").read_text())
    pcb = parse((ROOT / f"{NAME}.kicad_pcb").read_text())
    out = ROOT / "docs" / "reports"; out.mkdir(parents=True, exist_ok=True)
    lines = []
    for nm, pl, nc in sorted(schematic_nets(sch)):
        lines.append(f"{nm}{' [no-connect marker]' if nc else ''}: " + " ".join(f"{a}.{b}({c})" for a, b, c in pl))
    (out / "schematic-netlist.txt").write_text("\n".join(lines) + "\n")
    nets = {n[1]: n[2] for n in find(pcb, "net")}
    pads = defaultdict(list)
    for fp in find(pcb, "footprint"):
        ref = {q[1]: q[2] for q in find(fp, "property")}["Reference"]
        for pad in find(fp, "pad"):
            n = find(pad, "net")
            if n: pads[nets[n[0][1]]].append(f"{ref}.{pad[1]}")
    (out / "pcb-pad-nets.txt").write_text("\n".join(f"{n}: {' '.join(sorted(v))}" for n, v in sorted(pads.items())) + "\n")
    st = []
    ln, wd, ly = defaultdict(float), defaultdict(Counter), defaultdict(Counter)
    for s in find(pcb, "segment"):
        n = nets[find(s, "net")[0][1]]; a = find(s, "start")[0]; b = find(s, "end")[0]
        ln[n] += math.dist((float(a[1]), float(a[2])), (float(b[1]), float(b[2])))
        wd[n][find(s, "width")[0][1]] += 1; ly[n][find(s, "layer")[0][1]] += 1
    st.append("net, summed track-segment length mm (excludes vias/pads), widths mm, segments per layer")
    for n in sorted(ln): st.append(f"{n}, {ln[n]:.1f}, {dict(wd[n])}, {dict(ly[n])}")
    st.append("vias (size,drill): " + str(Counter((find(v, 'size')[0][1], find(v, 'drill')[0][1]) for v in find(pcb, 'via'))))
    (out / "pcb-statistics.txt").write_text("\n".join(st) + "\n")
    print("wrote", [p.name for p in out.iterdir()])

if __name__ == "__main__":
    main()
