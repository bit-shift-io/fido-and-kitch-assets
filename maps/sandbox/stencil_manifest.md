GRID: 20 columns x 20 rows of 128px cells (2560 x 2560 px).
Origin (col 0, row 0) is the TOP-LEFT cell.

SOLID TERRAIN — 8 rectangle(s):
  T1: cols 1-1, rows 6-6  (1 x 1 cells)  = x 128-256, y 768-896 px
  T2: cols 3-10, rows 6-6  (8 x 1 cells)  = x 384-1408, y 768-896 px
  T3: cols 12-14, rows 6-6  (3 x 1 cells)  = x 1536-1920, y 768-896 px
  T4: cols 14-19, rows 8-8  (6 x 1 cells)  = x 1792-2560, y 1024-1152 px
  T5: cols 11-15, rows 11-11  (5 x 1 cells)  = x 1408-2048, y 1408-1536 px
  T6: cols 0-6, rows 12-12  (7 x 1 cells)  = x 0-896, y 1536-1664 px
  T7: cols 0-6, rows 16-19  (7 x 4 cells)  = x 0-896, y 2048-2560 px
  T8: cols 10-19, rows 17-19  (10 x 3 cells)  = x 1280-2560, y 2176-2560 px

LIQUID — 1 rectangle(s):
  W1: cols 7-9, rows 18-19  (3 x 2 cells)  = x 896-1280, y 2304-2560 px

VOID: every remaining cell — 306 of 400 cells (76% of the image) is pure #000000 empty air.

ASCII MAP (T = solid terrain, W = liquid, . = void). Row 0 is the top row:
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