#!/usr/bin/env python3
"""Score a generated level image against its stencil, cell by cell.

Primary metric is OCCUPANCY — painted vs void — which is theme-independent and
catches every geometry failure seen so far (platforms thickening downward,
rectangles fusing, liquid spreading). Liquid is scored separately and is only
meaningful for blue-green themes; see --liquid.

Usage:
    python3 tools/check_output.py <stencil.png> <generated.png>
"""

import argparse
import sys

from PIL import Image

from stencil_manifest import TERRAIN, WATER, VOID, read_grid


def sample_grid(path, cols, rows):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    cw, ch = w / cols, h / rows
    px = img.load()
    out = []
    for r in range(rows):
        line = []
        for c in range(cols):
            tot, n = [0, 0, 0], 0
            for dy in range(int(ch * 0.2), int(ch * 0.8), max(1, int(ch / 8))):
                for dx in range(int(cw * 0.2), int(cw * 0.8), max(1, int(cw / 8))):
                    p = px[int(c * cw) + dx, int(r * ch) + dy]
                    for i in range(3):
                        tot[i] += p[i]
                    n += 1
            line.append(tuple(t / n for t in tot))
        out.append(line)
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stencil")
    ap.add_argument("generated")
    ap.add_argument("--cell", type=int, default=128)
    ap.add_argument("--void-threshold", type=float, default=70.0,
                    help="max summed RGB for a cell to count as void")
    ap.add_argument("--liquid", action="store_true",
                    help="also score liquid placement (cyan/blue themes only)")
    args = ap.parse_args()

    target, cols, rows = read_grid(args.stencil, args.cell)
    sampled = sample_grid(args.generated, cols, rows)

    got = []
    for r in range(rows):
        line = ""
        for c in range(cols):
            R, G, B = sampled[r][c]
            if R + G + B < args.void_threshold:
                line += VOID
            elif args.liquid and B > R * 1.4 and G > R * 1.4:
                line += WATER
            else:
                line += TERRAIN
        got.append(line)

    def occ(ch):
        return VOID if ch == VOID else TERRAIN

    wrong_occ, wrong_all, bad_rows = 0, 0, {}
    print("GENERATED                 TARGET                    DIFF")
    for r in range(rows):
        want = "".join(target[r])
        diff = ""
        for c in range(cols):
            g, t = got[r][c], want[c]
            if occ(g) != occ(t):
                diff += "X"
                wrong_occ += 1
                wrong_all += 1
                bad_rows[r] = bad_rows.get(r, 0) + 1
            elif args.liquid and g != t:
                diff += "~"
                wrong_all += 1
            else:
                diff += " "
        print(f"{r:2d} |{got[r]}|  |{want}|  |{diff}|")

    total = cols * rows
    print()
    print(f"OCCUPANCY (painted vs void): {total - wrong_occ}/{total} correct "
          f"({100 * (total - wrong_occ) / total:.1f}%)  X = wrong")
    if args.liquid:
        print(f"WITH LIQUID:                 {total - wrong_all}/{total} correct "
              f"({100 * (total - wrong_all) / total:.1f}%)  ~ = right occupancy, "
              f"wrong material")
    if bad_rows:
        worst = sorted(bad_rows.items(), key=lambda kv: -kv[1])[:5]
        print("Worst rows: " + ", ".join(f"row {r} ({n} cells)" for r, n in worst))
    else:
        print("Geometry matches the stencil exactly.")
    return 1 if wrong_occ else 0


if __name__ == "__main__":
    sys.exit(main())
