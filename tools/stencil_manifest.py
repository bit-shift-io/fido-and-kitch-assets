#!/usr/bin/env python3
"""Emit a text geometry manifest for a level stencil PNG.

The stencil is a grid of CELL x CELL pixel cells coloured:
    pure green  -> solid terrain
    pure blue   -> water / liquid
    pure black  -> empty void

Gemini follows geometry far more reliably when the same layout is supplied as
text alongside the image, so this prints a rectangle list and an ASCII map to
paste into the level-gen prompt.

Usage:
    python3 tools/stencil_manifest.py path/to/stencil.png [--cell 128]
"""

import argparse
import sys

from PIL import Image

TERRAIN, WATER, VOID = "T", "W", "."


def classify(px):
    r, g, b = px[:3]
    if g > 128 and r < 128 and b < 128:
        return TERRAIN
    if b > 128 and r < 128 and g < 128:
        return WATER
    return VOID


def read_grid(path, cell):
    img = Image.open(path).convert("RGB")
    w, h = img.size
    if w % cell or h % cell:
        print(
            f"warning: {w}x{h} is not a whole number of {cell}px cells",
            file=sys.stderr,
        )
    cols, rows = w // cell, h // cell
    px = img.load()
    return [
        [classify(px[c * cell + cell // 2, r * cell + cell // 2]) for c in range(cols)]
        for r in range(rows)
    ], cols, rows


def extract_rects(grid, cols, rows, kind):
    """Greedy maximal-rectangle decomposition of all cells of one kind."""
    used = [[False] * cols for _ in range(rows)]
    rects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] != kind or used[r][c]:
                continue
            # widen
            c1 = c
            while c1 + 1 < cols and grid[r][c1 + 1] == kind and not used[r][c1 + 1]:
                c1 += 1
            # deepen while the full width still matches
            r1 = r
            while r1 + 1 < rows and all(
                grid[r1 + 1][x] == kind and not used[r1 + 1][x] for x in range(c, c1 + 1)
            ):
                r1 += 1
            for y in range(r, r1 + 1):
                for x in range(c, c1 + 1):
                    used[y][x] = True
            rects.append((c, r, c1, r1))
    return rects


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("stencil")
    ap.add_argument("--cell", type=int, default=128)
    args = ap.parse_args()

    grid, cols, rows = read_grid(args.stencil, args.cell)
    cell = args.cell
    terrain = extract_rects(grid, cols, rows, TERRAIN)
    water = extract_rects(grid, cols, rows, WATER)

    voids = extract_rects(grid, cols, rows, VOID)

    def emit(rects, prefix, label):
        if not rects:
            print(f"{label}: none.")
            return
        print(f"{label} — {len(rects)} rectangle(s):")
        for i, (c0, r0, c1, r1) in enumerate(rects, 1):
            w, h = c1 - c0 + 1, r1 - r0 + 1
            print(
                f"  {prefix}{i}: cols {c0}-{c1}, rows {r0}-{r1} "
                f"— EXACTLY {w} wide x {h} tall"
            )

    def at(c, r):
        if 0 <= c < cols and 0 <= r < rows:
            return grid[r][c]
        return None

    def side(c, r, name):
        v = at(c, r)
        if v is None:
            return f"the {name} edge of the image"
        return {TERRAIN: "SOLID TERRAIN", WATER: "LIQUID", VOID: "VOID"}[v]

    total = cols * rows
    void_cells = sum(row.count(VOID) for row in grid)

    print("!! THIS LIST IS A SPECIFICATION FOR YOU TO READ AND OBEY. IT IS NOT A DIAGRAM")
    print("!! TO DRAW. Never render any number, coordinate, label, axis, ruler, grid line,")
    print("!! cell boundary or measurement in the output image. The finished picture")
    print("!! contains no writing of any kind.")
    print()
    print(f"GRID: {cols} columns x {rows} rows of {cell}px cells.")
    print("Origin (col 0, row 0) is the TOP-LEFT cell. Row numbers increase downward.")
    print()
    print("Every row range below is EXACT, not a minimum. A rectangle listed as 1 cell")
    print("tall is one cell tall — no thicker. Rectangles do not extend downward to meet")
    print("whatever is beneath them, and nothing is built on top of them.")
    print()
    emit(terrain, "T", "SOLID TERRAIN")
    print()
    emit(water, "W", "LIQUID")
    print()
    emit(voids, "V", "VOID — pure #000000 empty air, as precisely placed as the terrain")
    print(f"  ({void_cells} of {total} cells — {round(100 * void_cells / total)}% of the "
          f"image — is void. That is correct and finished, not unpainted.)")

    if water:
        print()
        print("LIQUID BOUNDARIES:")
        for i, (c0, r0, c1, r1) in enumerate(water, 1):
            print(
                f"  W{i} occupies columns {c0}-{c1} and nothing else. Its left edge is at "
                f"x {c0 * cell} px and its right edge is at x {(c1 + 1) * cell} px — "
                f"exactly {c1 - c0 + 1} cells apart. Its surface is at y {r0 * cell} px, "
                f"exactly {r1 - r0 + 1} cells above the bottom of the image."
            )
            print(
                f"     Immediately to its LEFT (column {c0 - 1}) is "
                f"{side(c0 - 1, r0, 'left')}. Immediately to its RIGHT (column {c1 + 1}) "
                f"is {side(c1 + 1, r0, 'right')}. Directly ABOVE it (row {r0 - 1}) is "
                f"{side(c0, r0 - 1, 'top')}. Count the columns before you place it — this "
                f"rectangle drifts sideways more often than any other."
            )

    print()
    print(f"BOTTOM EDGE (row {rows - 1}), left to right:")
    r = rows - 1
    c = 0
    names = {TERRAIN: "SOLID TERRAIN", WATER: "LIQUID", VOID: "VOID"}
    while c < cols:
        c1 = c
        while c1 + 1 < cols and grid[r][c1 + 1] == grid[r][c]:
            c1 += 1
        span = f"column {c}" if c == c1 else f"columns {c}-{c1}"
        print(f"  {span}: {names[grid[r][c]]}")
        c = c1 + 1

    print()
    print("ASCII MAP — THE AUTHORITATIVE LAYOUT. If anything above appears to conflict")
    print("with this map, the map wins. One character = one cell. Count characters to")
    print("place every edge. (T = solid terrain, W = liquid, . = void; row 0 is the top.)")
    hdr = "".join(str(c % 10) for c in range(cols))
    print(f"     {hdr}")
    for r, row in enumerate(grid):
        print(f"  {r:2d} |{''.join(row)}|")


if __name__ == "__main__":
    main()
