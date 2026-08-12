TASK: Repaint the attached image in place. 

The image is a grid of 128 px cells. Every rectangle is an exact whole number of cells
wide and tall, and sits exactly on cell boundaries. Preserve this precisely.


COLOUR LEGEND (these stencil colours are instructions, not palette — never render pure
green or pure blue in the output):

  PURE GREEN  #00FF00  →  SOLID TERRAIN. A player stands on its top surface. Render as
                          solid, opaque, physical ground with a clearly readable flat
                          top edge and vertical side walls.
  PURE BLUE   #0000FF  →  WATER / LIQUID VOLUME. A translucent liquid body filling that
                          exact rectangle, with a flat surface line across its top edge.
  PURE BLACK  #000000  →  EMPTY AIR. The player falls through this. Leave it as pure,
                          absolute, featureless #000000 void.

ASCII MAP — THE AUTHORITATIVE LAYOUT. If anything above appears to conflict
with this map, the map wins. One character = one cell. Count characters to
place every edge. (T = solid terrain, W = liquid, . = void; row 0 is the top.)
     01234567890123456789
   0 |....................|
   1 |....................|
   2 |....................|
   3 |....................|
   4 |....................|
   5 |....................|
   6 |.T.TTTTTTTT.TTT.....|
   7 |....................|
   8 |..............TTTTTT|
   9 |....................|
  10 |....................|
  11 |...........TTTTT....|
  12 |TTTTTTT.............|
  13 |....................|
  14 |....................|
  15 |....................|
  16 |TTTTTTT.............|
  17 |TTTTTTT...TTTTTTTTTT|
  18 |TTTTTTTWWWTTTTTTTTTT|
  19 |TTTTTTTWWWTTTTTTTTTT|

Follow the exact structural layout grid from the uploaded png:
* Green regions: Solid medieval stone platforms with moss overhangs and copper steampunk accents.
* Blue region: Crystal clear turquoise water pool at the bottom-center with submerged brass gears, stone structures and sea weed growth.
* Black region: Environmental background layers.


# THEME:

Carved stone architecture, steampunk copper pipes, brass gears. Add lush overgrowth and vivid lighting.

# ART STYLE & HYBRID DIRECTIVE:

## Foreground Gameplay Layer:
Style: Ultra-crisp 2D vector style with thick, clean dark outlines and vibrant fills (Bluey cartoon aesthetic). Then apply hand painted details with rough brush strokes for finer texture detail.
Details: Carved stone architecture, steampunk copper pipes, brass gears. Add lush overgrowth and vivid lighting.

## Background Layer:
Style: Keep it black. The user will add their own background.


