# Sprite Slicing & Modularization Guide

This process is most commonly called **Sprite Slicing**, **Sprite Separation**, or **Sprite Modularization**, depending on which phase of production you are in:

## Core Terms

* **Sprite Slicing / Slicing:** The immediate graphic editing action of cropping, cutting out, and separating a single composite character drawing into individual image files (head, torso, upper arm, lower arm, etc.). Game engines like Unity use a built-in tool specifically called the "Sprite Slicer" for this.
* **Modularization (or Modular Sprite Creation):** The design strategy of breaking a character into distinct parts so they can be swapped dynamically (e.g., swapping armor, weapons, or expressions without re-animating the whole character).
* **Asset Decomposition / Dissection:** A broader technical artist term for taking a finished piece of artwork and breaking it down into raw functional layers or components.

---

## What Comes Next (The Animation Stage)

Once you have sliced the sprite sheet into distinct body parts, the downstream animation technique is called:

1. **Cutout Animation (or Modular 2D Animation):** Arranging the flat sprite pieces into hierarchy layers and transforming them (rotating, translating) frame-by-frame or via keyframes.
2. **Skeletal Animation (or 2D Rigging):** Binding the sliced sprite parts to a 2D digital bone structure (using software like Spine 2D, DragonBones, or Godot/Unity's 2D Animation packages) so moving a bone drives the attached sprite component automatically.

---

## Quick Workflow Checklist for Slicing

* **Overdraw / Padding:** Ensure joint areas (like elbows, shoulders, and knees) have extra circular artwork hidden behind neighboring parts so gaps don't appear when limbs rotate.
* **Pivot Points:** Set the rotation origin (pivot) for each slice directly on its joint axis rather than the center of the image crop box.
