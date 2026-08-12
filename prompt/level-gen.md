# ABSOLUTE PRIORITY: GAMEPLAY LAYOUT & COLLISION BOUNDARIES
You are a graphic designer creating a high-resolution 2D game concept image for a complete level. Repaint the attached layout reference image in place as a grey-box paint-over.
- DO NOT move, resize, merge, add, shrink, expand, or remove any colored region or block. 
- EVERY platform and liquid volume must retain its exact position, shape, scale, and pixel-bounding-box from the reference image.
- DO NOT allow elements from one colored region to spill over or overwrite adjacent regions.

# FORBIDDEN & NEGATIVE DIRECTIVES (STRICT ENFORCEMENT)
Do NOT render, apply, or include any of the following:
- Spatial/Camera Distortion: NO 3D perspective, NO vanishing points, NO isometric tilt, NO camera tilt, NO foreshortening. The view must remain 100% flat 2D orthographic.
- Layout Bleed & Resizing: NO expanded water bodies, NO sprawling lakes or wide open rivers, NO water bleeding into stone terrain, NO shrinking stone blocks, NO retreating cliff faces, NO sloped hills, NO steep mountains, NO merged grid cells.
- Unwanted Details: NO background scenery, NO midground arches or distant structures, NO atmospheric haze, NO fog filling the void, NO spilled water, NO debris floating outside bounds.
- Edge Quality: NO soft/blurry borders, NO antialiasing artifacts around region edges.

# COLOR-TO-MATERIAL MAPPING:
1. GREEN REGIONS (#00FF00) - SOLID TERRAIN & PLATFORMS:
   - Walkability: The top horizontal edge of EVERY green region defines a player walking surface. You may add subtle organic terrain variance (grass tufts, moss mounds, cobblestone texture), but the top line MUST stay strictly within a ~32-pixel vertical tolerance of the original top edge.
   - Boundaries: The left, right, and bottom edges of green regions must form solid stone/cliff walls that align precisely with the mask. Do not shrink stone masses or retreat cliff edges away from adjacent water or void regions.
   - Detailing: You have full creative freedom along the undersides and faces of green regions to render hanging roots, moss overhangs, copper pipes, arches, and exposed brass gears inside the platform bounds or extending into black negative space.

2. BLUE REGIONS (#0000FF) - LIQUID / WATER VOLUMES:
   - Bounds: Render liquid strictly inside the exact boundaries of the blue regions. Do not widen, expand, shrink, or shift liquid bodies beyond the blue pixels. The liquid must remain tightly contained between adjacent terrain walls.
   - Surface: The top liquid line must align with the top edge of the blue block within a ~32-pixel surface ripple tolerance.

3. BLACK REGIONS (#000000) - VOID / NEGATIVE SPACE:
   - Render as pure, featureless black (#000000) background space. Do not render environmental layers, midground structures, atmospheric haze, background scenery, or distant architecture in black areas.

# ART THEME & MATERIALS:
- Theme: A vibrant hybrid medieval-steampunk level environment. Charming, inviting, wondrous, kid-friendly, and joyful.
- Foreground Materials: Solid medieval stone brickwork with chiseled, rough-hewn textures. Rich moss overgrowth, hanging vines, polished brass gears, and etched copper pipes with green patina.
- Lighting Features: Small, vibrant emissive lighting sources built into the architecture (e.g., glowing green glow-worms or warm brass gas-lamps).
- Water Detail: Crystal-clear, highly saturated turquoise water containing submerged brass gears, stone structures, and thick green seaweed strictly inside the blue volume.

# ART STYLE & TECHNIQUE:
- Medium: Modern hand-painted 2D indie platformer key art (Rayman Legends / Ori style) crossed with a high-end children's picture book. Visible painterly brushwork and canvas texture within each shape, contained by crisp, deliberate edges.
- Lines: Every solid form carries a confident dark contour (a deep desaturated version of its local color, 6–10px weight, never pure black).
- Color: Vibrant and highly saturated. Deep chromatic shadows (violet, teal, umber), bright midtones, and hot highlights on top-facing surfaces.
- Lighting: Vivid three-value read on every platform (lit top surface, mid-tone front face, shadowed underside) driven by a strong key light from above.
- Camera: Dead-flat 2D orthographic side-scroller elevation. Zero perspective convergence, no vanishing point, and no 3D tilt.
