# Level Generation Prompt System

Target model: **Nano Banana / Gemini Image** (image-conditioned edit).

> **Never paste this file into Gemini.** It is documentation: it contains `{{PLACEHOLDER}}`
> tokens, five competing theme packs, and troubleshooting prose that the model reads as
> scene description. Always send the built prompt from `tools/build_prompt.py`.

## How to use

1. Build the prompt. This inlines the geometry manifest, splices in one theme pack, and
   errors out if any placeholder is left unsubstituted:

   ```sh
   python3 tools/build_prompt.py maps/sandbox/export_sandbox.png steampunk
   # -> writes maps/sandbox/full_prompt.md, beside the stencil
   python3 tools/build_prompt.py --list        # available themes
   ```

2. Attach the **stencil PNG** (2560×2560, green/blue/black block map) as image slot 1.
3. Optionally attach a **previously approved output** as image slot 2 — the biggest lever
   on style consistency. See [Style anchoring](#style-anchoring).
4. Paste the built prompt. Send nothing else.
5. Score the result rather than eyeballing it. Exits non-zero on any drift:

   ```sh
   python3 tools/check_output.py maps/sandbox/export_sandbox.png generated.png --liquid
   ```

The text geometry is what does the heavy lifting — Gemini follows a coordinate list far
more reliably than it reads shapes out of an image. `tools/stencil_manifest.py` generates
it, and `build_prompt.py` calls that for you.

---

## MASTER PROMPT

```text
TASK: Repaint the attached image in place. This is not a new composition — it is a
paint-by-numbers stencil, and you are colouring inside its existing shapes. Every
coloured rectangle in the stencil already exists at its final position and final size.
Your job is to give each rectangle a material, a texture and lighting. Your job is NOT
to move it, resize it, merge it, split it, or add new ones.

OUTPUT: One image, 2560×2560 pixels, square, no border, no frame, no caption, no UI.

THIS PROMPT DESCRIBES A FINISHED PIECE OF GAME ART, NOT A TECHNICAL DRAWING. It contains
measurements so that you place things accurately. Those measurements are instructions to
follow, never content to depict. The finished image is a painting: it contains no numbers,
no coordinates, no row or column labels, no axes, no rulers, no grid lines, no cell
boundaries, no annotations, no legend, no callouts, and no writing of any kind.

═══════════════════════════════════════════════════════════
1. GEOMETRY CONTRACT — HIGHEST PRIORITY, OVERRIDES ALL ELSE
═══════════════════════════════════════════════════════════
The image is a grid of 128 px cells. Every rectangle is an exact whole number of cells
wide and tall, and sits exactly on cell boundaries. Preserve this precisely.

THE LAYOUT IS ALSO GIVEN TO YOU AS TEXT BELOW. The stencil image and this manifest
describe the SAME layout. Where your instinct about "how a level should look" disagrees
with the manifest, the manifest wins. Work from the manifest first and use the image only
to confirm it.

{{GEOMETRY_MANIFEST}}

COLOUR LEGEND (these stencil colours are instructions, not palette — never render pure
green or pure blue in the output):

  PURE GREEN  #00FF00  →  SOLID TERRAIN. A player stands on its top surface. Render as
                          solid, opaque, physical ground with a clearly readable flat
                          top edge and vertical side walls.
  PURE BLUE   #0000FF  →  WATER / LIQUID VOLUME. A translucent liquid body filling that
                          exact rectangle, with a flat surface line across its top edge.
  PURE BLACK  #000000  →  EMPTY AIR. The player falls through this. Leave it as pure,
                          absolute, featureless #000000 void.

HARD RULES:
- Do not add a platform, ledge, step, pillar, bridge, rock or any standable surface
  anywhere the stencil is black. Not even a small one. Not even in a corner.
- Do not delete, shorten, lengthen, thicken, thin, or shift any green rectangle.
- Do not connect two separate green rectangles that the stencil leaves separated.
- Do not round off, bevel, taper or erode the corners of the collision silhouette.
- Each rectangle's top edge must read as a single straight horizontal line across its
  full width. No slopes, no humps, no stair-stepping, no sagging.
- Left and right ends of a platform are sheer vertical cut faces, not crumbling talus.
- Preserve the exact aspect ratio and framing. Do not crop, zoom, pan, add margins, or
  add vignette.
- Liquid exists ONLY inside the rectangles listed as LIQUID in the manifest. It does not
  spread sideways, does not pool along the bottom of the image, and does not extend under
  or behind terrain. If the manifest lists a 2-cell-wide liquid rectangle, the liquid is
  exactly 2 cells wide. It is a channel of liquid sunk between two solid masses of
  terrain, with no container, tank, frame, glass, border or vessel around it — the terrain
  either side IS the edge of the liquid.
- Terrain rectangles that the manifest lists separately must render as separate, visually
  detached objects, even when their edges are close together or touching. Never fuse two
  listed rectangles into one continuous stepped cliff, staircase or building.
- Every rectangle is a rectangle. Do not reinterpret a listed rectangle as an L-shape, a
  stepped form, a wedge, or a cluster of smaller ledges.
- Nothing is ever built ON TOP of a terrain rectangle. No tower, wall, pillar, chimney,
  raised end, upper tier, battlement, machine housing or second storey rising above its
  top edge. The top edge is the highest point of that rectangle, everywhere along it. This
  is most often broken at the left or right end of a wide, low rectangle — do not do it.

THICKNESS IS EXACT — READ THIS TWICE:
Every row range in the manifest is an exact height, never a minimum. A rectangle listed
as 1 cell tall is 128 px tall and its underside is a hard edge at that height with pure
black immediately below it. Do not thicken a platform downward to give it visual weight.
Do not extend a platform down until it reaches whatever is beneath it. Do not raise the
top of a lower rectangle to meet the bottom of a higher one. Height errors are the most
common failure on this task — a platform that renders 2 cells tall when the manifest says
1 is a rejected image, however good it looks.

THE BOTTOM OF THE IMAGE IS NOT GROUND LEVEL:
Do not treat the lower part of the image as a continuous landscape, ground plane, terrain
line or cross-section. There is no ground level anywhere in this image. The rectangles
that touch the bottom edge are separate islands that happen to be low, and the void
between and above them continues all the way down to the bottom edge of the image and is
just as black there as it is at the top. Void listed at the bottom of the image is void,
not a cave, not a basement, not water, not shadow.

DECORATION ALLOWANCE (the only permitted deviation):
ONLY soft organic growth may break the silhouette, and only by up to 32 px (a quarter
cell): hanging vines, moss fringe, drips, grass tufts, small growths, glow motes. It must
be thin, sparse and wispy — you can see black between the strands — and must read as
clearly non-standable: never a slab, ledge, branch or outcrop a player could mistake for
ground.

HARD OBJECTS NEVER OVERHANG. Gears, cogs, pipes, valves, brackets, panels, plating,
machinery, lanterns, crystals, coral, mushroom caps, roots and any other solid element sit
FLUSH INSIDE the rectangle. Not one of them may extend past the top, bottom, left or right
edge by a single pixel. A gear half-sunk into the front face is correct; a gear hanging
below the underside is a rejected image.

This matters most on the underside. A 1-cell platform with a row of gears slung underneath
reads as a 2-cell platform, and that is a height failure — the most common way this task
goes wrong. Hang nothing solid below anything.

BLACK ZONE ENFORCEMENT:
The black regions are deliberate negative space and must stay pure #000000. No sky, no
stars, no fog, no gradient, no silhouettes, no distant scenery, no glow bleeding out from
the platforms, no atmospheric haze, no god rays, no particles. A separate parallax
background is composited in later. Emptiness here is correct, not unfinished.

═══════════════════════════════════════════════════════════
2. STYLE BIBLE — FROZEN, IDENTICAL ON EVERY RUN
═══════════════════════════════════════════════════════════
Medium: hand-painted 2D game art. Visible painterly brushwork and canvas-level texture
within each shape, contained by crisp, deliberate edges. Painted, not vector-flat; clean,
not sketchy or messy.

Line: every solid form carries a confident dark contour — a deep desaturated version of
its own local colour, never black. Line weight approximately 6–10 px, consistent across
the whole image, slightly heavier where a form meets void.

Colour: vibrant and highly saturated. Deep saturated shadows that stay chromatic (violet,
teal, umber — never grey, never neutral black). Bright saturated midtones. Hot, near-white
highlights on the top-facing surfaces and on light sources.

Lighting: vivid and directional, with one dominant key light plus emissive accents built
into the environment itself. Strong value separation between a platform's lit top surface,
its mid-value front face, and its shadowed underside — this three-value read is what makes
terrain legible at a glance, and it is mandatory on every platform.

Surface detail: a visual feast. Every platform carries layered material storytelling —
texture, wear, growth, small glowing details, tiny points of interest. Rich, but never so
busy that the flat top edge stops reading as a standable surface.

Tone: kid-friendly and joyful. Charming, inviting, wondrous. Zero menace, zero gore, zero
grime, zero horror. Bright and appealing to a six-year-old.

Reference feel: modern hand-painted indie platformer key art (Rayman Legends, Ori,
Trine) crossed with the warmth and colour confidence of a high-end children's picture book.

Camera: dead-flat 2D side-scroller elevation. Orthographic. No perspective convergence,
no vanishing point, no 3D tilt, no camera angle, no foreshortening.

═══════════════════════════════════════════════════════════
3. GAMEPLAY READABILITY LAW — FROZEN, IDENTICAL ON EVERY RUN
═══════════════════════════════════════════════════════════
THERE IS NO BACKGROUND OR MIDGROUND LAYER IN THIS IMAGE. Every painted pixel is a surface
the player physically collides with. Do not paint scenery, architecture, distant
structures, or set dressing that a player could not stand on. If it is painted, it is
solid. If it is not solid, it is not painted.

A player must be able to glance at this image and know instantly where they can stand.
That outranks richness of detail.

WALKABLE CAP BAND (mandatory on every terrain rectangle):
The top 24–40 px of every terrain rectangle is a distinct, unbroken horizontal cap band of
the theme's surface material, running the full width of the rectangle. It is the single
brightest and most saturated element in the image. It is identical in treatment on every
rectangle — a 1-cell platform and a 12-cell platform get the same cap. This band is how
the player reads "I can stand here", so it must never be interrupted, obscured, or matched
in brightness by anything else.

THREE-VALUE READ (mandatory, in strict order):
  1. Cap band       — lightest values in the image.
  2. Front face     — clear mid values.
  3. Underside      — darkest values, a hard shadow line directly beneath the cap.
Every terrain rectangle shows all three. The steps between them are large and obvious, not
subtle gradients.

DETAIL SUBORDINATION:
All surface detail — bricks, gears, panels, coral, roots, machinery, grain — lives on the
front face only, and stays within that face's mid-value range. Detail must be lower in
contrast and lower in saturation than the cap band. Rich texture is welcome; texture that
competes with the cap band for the eye is a failure. Nothing on the front face may read as
a step, ledge, shelf or foothold.

ISLAND SEPARATION:
Each terrain rectangle is a discrete floating island with its own complete silhouette and
its own contour line on all four sides — including its underside, which is always visible
and always in shadow. Where the manifest leaves void between two rectangles, that void
stays pure black at full width and full height, with no bridge, buttress, scaffold, pipe
run, arch, root or vine crossing it. Nothing structural spans a gap.

EMISSIVE DISCIPLINE:
Emissive accents are small, sparse points of light sitting on the front face. They do not
cast light onto the void, do not bloom, and never out-brighten the cap band.

═══════════════════════════════════════════════════════════
4. THEME PACK — THE ONLY BLOCK THAT CHANGES BETWEEN LEVELS
═══════════════════════════════════════════════════════════
THEME NAME: {{THEME_NAME}}

TERRAIN MATERIAL (fills every green rectangle):
{{TERRAIN_MATERIAL}}

TOP SURFACE (the standable top edge — must be the brightest, most legible band):
{{TOP_SURFACE}}

SIDE & UNDERSIDE (cut faces and shadowed bellies):
{{SIDE_UNDERSIDE}}

EDGE DECORATION (within the 32 px allowance):
{{EDGE_DECORATION}}

LIQUID (fills every blue rectangle):
{{LIQUID}}

EMISSIVE ACCENTS (the small self-lit details, on terrain only):
{{EMISSIVE_ACCENTS}}

KEY LIGHT: {{KEY_LIGHT}}

PALETTE: {{PALETTE}}

═══════════════════════════════════════════════════════════
5. DO NOT INCLUDE
═══════════════════════════════════════════════════════════
No numbers, digits, coordinates, row or column labels, axes, tick marks, rulers,
measurements, annotations, legends or callouts anywhere in the image, including along its
edges. This is not a diagram, chart, blueprint, spec sheet, tileset sheet or reference
figure — it is a single finished painting of a level.
No characters, creatures, players, faces or eyes. No text, letters, logos, HUD,
health bars, or watermarks. No coins, chests, keys, doors or pickups. No arrows or
signage. No grid lines, no cell outlines, no visible stencil colours. No photorealism, no
3D render, no depth-of-field blur, no bloom spilling into the black. No pixel art, no flat
vector, no cel-shaded anime, no watercolour bleed, no pastel washing-out. No dark, gritty,
horror, or grimdark treatment. No perspective camera. No background scenery of any kind.

═══════════════════════════════════════════════════════════
6. FINAL CHECK BEFORE YOU OUTPUT
═══════════════════════════════════════════════════════════
Walk the manifest one entry at a time and confirm each of these:
- HEIGHT FIRST: every T rectangle is exactly as many cells tall as listed. Count them.
  Nothing has thickened downward or grown upward.
- Every V rectangle is completely, entirely pure #000000 across its full listed width and
  full listed height — including the V rectangles at the bottom of the image.
- Every listed LIQUID rectangle matches its listed width, height and surface line exactly.
  Liquid appears nowhere else in the image.
- Every listed TERRAIN rectangle exists at exactly its listed columns and rows, as a
  separate island with a visible underside.
- No two listed rectangles have been fused together.
- Every terrain rectangle has the same bright cap band, and nothing else in the image is
  brighter than those bands.
If anything drifted, correct it — geometry and readability outrank beauty.
```

---

## Theme packs

Drop one of these into section 4, replacing the `{{...}}` slots.

### Steampunk overgrowth

```text
THEME NAME: Overgrown steampunk ruins

TERRAIN MATERIAL: Rough-hewn warm grey granite blockwork threaded with riveted brass
plating and etched copper piping. Slabs are chunky and hand-chiselled, with visible mortar
lines and painted stone grain.

TOP SURFACE: A bright band of sunlit moss and short grass over the stone lip, yellow-green
where the light hits, with a thin warm rim-light along the very top edge.

SIDE & UNDERSIDE: Brass gears, cog teeth and copper pipework are sunk flush INTO the front
face, never protruding from it. Cut ends are plain violet-shadowed stone. The underside is
bare stone in deep shadow with verdigris staining — no hardware hangs from it.

EDGE DECORATION: Ivy and hanging vines spilling over the lip, moss fringe. Nothing metal
overhangs.

LIQUID: Clear turquoise pool, translucent, with submerged brass gears and stone masonry
visible through it and pale caustic ripples across the surface line.

EMISSIVE ACCENTS: Warm amber gas lanterns and glowing pressure gauges recessed into the
stone; faint green glow-worms tucked under mossy overhangs.

KEY LIGHT: Warm golden sunlight from the upper left.

PALETTE: Warm grey stone, polished brass gold, verdigris teal, lush yellow-green moss,
turquoise water, violet shadow.
```

### Sunken pirate aquarium

```text
THEME NAME: Sunken pirate treasure reef

TERRAIN MATERIAL: Pale coral limestone and barnacled shipwreck timber, planked and
weather-worn, studded with brass portholes and encrusted cannon barrels.

TOP SURFACE: Bright cyan-lit coral crust and fine white sand catching the light from
above, with a crisp pale rim along the top edge.

SIDE & UNDERSIDE: Deep teal-shadowed timber and stone. Coral clusters and gold doubloons
are set flush into the front face, never protruding. The underside is bare shadowed timber
— nothing hangs from it.

EDGE DECORATION: Swaying kelp fronds and frayed rope ends only, thin and sparse. Coral,
anemones and starfish stay flush inside the rectangle.

LIQUID: Deeper, richer aquamarine than the surrounding water, translucent, with drifting
motes and a bright caustic shimmer across the surface line.

EMISSIVE ACCENTS: Glowing jellyfish nestled in crevices, bioluminescent pink anemone tips,
a soft golden shine off spilled treasure.

KEY LIGHT: Cool cyan god-free light from directly above, as if filtering down from the
surface (light only, no visible rays).

PALETTE: Aquamarine, pale coral pink, sun-bleached driftwood tan, treasure gold, deep teal
shadow, hot magenta accents.
```

### Mushroom caverns

```text
THEME NAME: Cavernous underground mushroom grove

TERRAIN MATERIAL: Damp dark-violet cave rock with mineral striations, capped by dense
clusters of fat, rounded mushroom caps in coral and butter-yellow.

TOP SURFACE: A springy carpet of pale mint moss and tiny mushroom buttons, brightly lit
from the fungal glow, with a clear light band along the top edge.

SIDE & UNDERSIDE: Deep indigo rock face with glinting mineral veins, friendly plump worms
poking cheerfully from burrows in the front face. The underside is bare shadowed rock —
nothing hangs from it.

EDGE DECORATION: Hanging root tendrils and slow glowing drips only, thin and sparse.
Mushroom caps stay flush inside the rectangle and never overhang the edge.

LIQUID: Luminous jade-green pool, translucent, faintly glowing from within, with spore
motes floating on the surface line.

EMISSIVE ACCENTS: Softly pulsing cyan and magenta fungal caps, glowing spore clusters,
tiny lantern-mushrooms in the rock crevices.

KEY LIGHT: Magenta fungal glow from below-left, cool cyan fill from above.

PALETTE: Indigo and violet rock, glowing cyan, hot magenta, coral mushroom caps, mint
moss, jade water.
```

### Space

```text
THEME NAME: Cosmic asteroid outpost

TERRAIN MATERIAL: Chunky slate-blue asteroid rock threaded with glowing crystal seams,
plated with clean white-and-orange sci-fi panelling and chrome trim.

TOP SURFACE: A bright cyan-lit landing deck of white panels with painted safety striping,
crisply lit along the top edge.

SIDE & UNDERSIDE: Deep navy rock shadow. Conduit bundles, thruster nozzles and riveted
hull plating are set flush into the front face, never protruding. The underside is bare
shadowed rock — nothing hangs from it.

EDGE DECORATION: Tiny floating dust motes only, sparse. Antennae, cables, nozzles and
crystal shards stay flush inside the rectangle.

LIQUID: Glowing violet plasma coolant, translucent, with a bright energised surface line
and slow luminous swirls.

EMISSIVE ACCENTS: Cyan panel strip-lights, blinking orange status lamps, glowing crystal
seams pulsing in the rock.

KEY LIGHT: Cold white starlight from the upper right, warm orange bounce from the panels.

PALETTE: Slate blue, chrome white, hot orange, electric cyan, violet plasma, deep navy
shadow.
```

### Mystical forest

```text
THEME NAME: Enchanted ancient forest

TERRAIN MATERIAL: Colossal moss-blanketed tree roots and warm bark-brown timber woven with
lichen-crusted boulders and knotted grain.

TOP SURFACE: Thick emerald grass and clover catching golden light, with a warm yellow rim
along the top edge and small white wildflowers.

SIDE & UNDERSIDE: Rich umber bark shadow shifting to violet, twisting root grain and pale
shelf-fungus rings set flush into the front face. The underside is bare shadowed bark —
nothing hangs from it.

EDGE DECORATION: Trailing ivy, hanging flower vines and dandelion fluff only, thin and
sparse. Ferns and roots stay flush inside the rectangle.

LIQUID: Clear emerald spring water, translucent, with lily pads on the surface line and
smooth river stones visible beneath.

EMISSIVE ACCENTS: Golden fireflies, glowing blue wisps in the hollows, luminous flower
centres, soft glowing runes carved into the bark.

KEY LIGHT: Warm honey-gold shafts from the upper left, cool green-blue fill in the shade.

PALETTE: Emerald green, honey gold, warm umber bark, teal shadow, wildflower white and
lilac, firefly amber.
```

### Writing a new theme pack

Copy an existing pack and swap the materials. Two rules, both learned the hard way:

- **Never name a solid object in the `SIDE & UNDERSIDE` slot without saying "flush into the
  front face".** An early version of the steampunk pack read *"exposed brass gears and cog
  teeth"* there, and the model hung gear clusters below every platform — which reads as
  extra platform thickness and fails the height check. Undersides are bare shadowed
  material, full stop.
- **`EDGE DECORATION` is for soft growth only** — vines, moss, fronds, drips, motes.
  Anything rigid belongs in `TERRAIN MATERIAL` or `SIDE & UNDERSIDE`, flush inside the
  rectangle.

---

## Style anchoring

The Style Bible is frozen wording, but wording alone will not hold a look across five
themes. To lock it:

1. Generate the **steampunk** level first and iterate until it is exactly the look you
   want. That image becomes the *style anchor*.
2. For every subsequent theme, attach the anchor as a second image and prepend one line to
   the master prompt:

   > `Image 1 is the layout stencil. Image 2 is the STYLE ANCHOR — match its brushwork, line
   > weight, saturation, lighting logic and level of detail exactly. Take only the style
   > from image 2 and only the geometry from image 1. Ignore image 2's subject matter,
   > colours and materials entirely; those come from the theme pack below.`

3. Re-anchor whenever you approve a new best-looking output, so the anchor never drifts
   behind the current bar.

## Tuning notes

Change **one variable at a time** between runs. Editing style and theme in the same pass
makes it impossible to tell which change caused the drift.

**Geometry**

Run `check_output.py` first — it tells you which rows failed, and the fix follows from
that. Nearly every failure so far has been *vertical*: rectangles render taller than
listed, then the shapes below them rise to meet the overhang and the gaps close up. Water
spreading is usually a downstream symptom of this, not its own problem, so fix heights
before touching the liquid wording.

- *Platforms too thick / gaps closing?* Name the specific void rectangle from the manifest:
  *"V13 (cols 0-6, rows 13-15) is 3 full cells of pure black. T6 is 1 cell tall and its
  underside is a hard edge with black below it."*
- *Liquid too wide?* Quote the LIQUID CONTAINMENT line back at it and add: *"The liquid is
  a narrow reservoir sunk between two solid masses. There is no sea, lake or river in this
  image."* Also check whether the terrain either side is the real culprit.
- *Rectangles fusing into one cliff?* Add: *"Rectangle Tn and rectangle Tm are separate
  objects with black sky between them"*, naming the specific pair.
- *Bottom band still reading as a landscape?* Add: *"Crop the bottom third mentally: it is
  two separate islands and a narrow tank, floating in black, not a ground plane."*
- *Still drifting after all that?* Split into two passes. Pass 1: sections 1 and 6 only,
  plus "render every terrain rectangle as flat untextured mid-grey, every liquid rectangle
  as flat mid-blue, void as pure black." Score it with `check_output.py` until it is 100%,
  then feed that output back in with only the Style Bible, Readability Law and Theme Pack,
  prefixed with "keep every shape exactly as it is; change only material and lighting."
  Slower, but geometry stops being negotiable.
- *Suspect the prompt itself?* Confirm you sent the built file, not `level-gen.md`.

**When the model draws the spec instead of the level**

A run once came back with row numbers down the left edge and column numbers along the
bottom, five platforms, and the water rendered as a framed glass aquarium. Two lessons,
both now baked into the prompt:

- *There is a ceiling on how much coordinate text helps.* That run added a per-rectangle
  pixel-coordinate block on top of an already number-dense manifest, and the model flipped
  from "satisfy this spec" to "illustrate this spec" — the score fell from 91% to 71%.
  Cell ranges plus the ASCII map are enough; pixel coordinates were pure noise and are
  gone. **If accuracy drops after you add detail, remove it rather than adding more.**
- *Metaphors get rendered literally.* The glass tank came from the phrase *"a narrow tank
  with solid walls"*, meant as a description of proportion. Describe what things are, never
  what they are like — every simile is a request.

**Readability**

- *Can't tell what's standable?* Thicken and brighten the cap band, and add *"reduce the
  contrast of all brick, gear and panel detail by half."* Detail contrast is almost always
  the culprit, not the cap.
- *Platforms reading as buildings?* Strengthen island separation and add *"each platform is
  a slab floating in black, not a wall, tower or facade."*
- *Undersides disappearing?* Add *"the underside of every platform is visible and is the
  darkest value in the image."*

**Style**

- *Drifting toward vector flat?* Strengthen "visible painterly brushwork and canvas-level
  texture" and add *"you can see individual brush strokes"*.
- *Drifting toward mush?* Strengthen the line clause and the three-value read.
- *Theme bleeding into the black?* Add *"the black void is not part of the scene and
  receives no light from it"*.
