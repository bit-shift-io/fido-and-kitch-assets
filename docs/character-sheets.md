# Character Sheet Reference & Terminology Guide

When creating or working with character reference sheets for game development, 2D animation, or 3D modeling, standardized artwork and terminology ensure consistent asset creation across the production pipeline.

---

## 1. Sheet Types & Layouts

* **Model Sheet / Turnaround Sheet:** The foundational document showing the character from multiple standardized angles to display exact proportions, silhouette, and details across 360 degrees.
* **Expression Sheet:** A collection of close-ups on the character's face demonstrating their range of emotion, facial deformation, and key micro-expressions.
* **Action / Dynamic Sheet:** Key drawings showing the character in iconic poses, extreme movements, or using signature abilities to convey personality, weight, and center of gravity.
* **Breakout / Detail Sheet:** Close-up views of intricate elements that are easy to miss on full-body drawings, such as costume patterns, weapons, mechanical props, or hidden layers.

---

## 2. Orthographic Projections (Standard Angles)

Orthographic views are drawn with zero perspective distortion (parallel projection) so artists and 3D modelers can measure proportions directly off the sheet.

* **Front View:** Straight-on view facing the viewer.
* **Side View (Profile):** Exactly 90 degrees to the side, critical for defining depth (nose, chest, backpack alignment).
* **Back View:** Directly from behind to show rear details, tail, hair, or cape attachments.
* **Three-Quarter View (3/4 View):** Rotated approximately 45 degrees between front and profile. This is the most natural view for showing form and depth, but is non-orthographic if perspective is applied.

---

## 3. Poses & Posture Terminology

* **T-Pose:** The character stands upright with arms extended straight out horizontally to the sides, palms facing down or forward. Standard baseline for 3D rigging and automatic skinning.
* **A-Pose:** The character stands with arms relaxed downward at roughly a 45-degree angle. This reduces shoulder texture distortion during rigging compared to a T-Pose.
* **Bind Pose / Rest Pose:** The default neutral pose in which a digital model is built and bound to its underlying skeleton before any animation is applied.
* **Contrapposto:** A natural standing pose where weight is shifted onto one foot, causing the shoulders and hips to tilt in opposite directions to show life and organic balance.

---

## 4. Scale, Guidelines & Proportions

* **Head-Count (Proportions):** Measuring character height using head lengths as the unit (e.g., standard realistic human = 7 to 7.5 heads high; heroic fantasy = 8 heads; chibi/stylized = 2 to 3 heads).
* **Construction Lines / Alignment Guides:** Horizontal lines running across front, side, and back views to ensure features like the nose, elbows, waist, and knees align across every angle.
* **Silhouette:** The solid black shape of the character when lighting and internal details are removed. A strong character design should remain identifiable purely by its silhouette.

---

## 5. Technical Animation Prep

* **Rig-Ready Breakdown / Sliced View:** The character sheet layout where every modular component (forearm, bicep, head, torso, individual hair strands, floating accessories) is offset and arranged neatly across the canvas with visible overlap padding.
* **Parts Sheet / Component Layout:** A dedicated texture atlas layout where each separate limb and layer is spread out, allowing standard pivot points and joint anchors to be clearly defined before being imported into software like Spine, DragonBones, or Unity/Godot 2D Animation.
* **Exploded View:** A breakdown drawing where layered outfit elements, armor plates, or hair strands are drawn floating away from the main body to show what lies underneath.
* **Turnaround Lineup:** Aligning all characters in the cast side-by-side on a single grid to establish exact relative heights.
* **Joint Centers / Pivot Anchors:** Marked points on a modular character sheet showing where limbs attach and pivot (shoulders, elbows, hips).
