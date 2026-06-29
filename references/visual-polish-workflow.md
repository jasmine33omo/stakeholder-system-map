# Visual Polish Workflow

Use this reference for portfolio-ready system map PNGs that should look less code-generated, more editorial, or closer to a polished design-board reference. This is the default finishing layer for portfolio output, not a replacement for the structured stakeholder model.

## Core Principle

The deterministic map is the source of truth. Image generation can improve visual finish, but it must not decide system logic.

Keep these three artifacts separate:

- `structured-draft.png`: code-rendered map with exact layout, text, stakeholders, relationship labels, legend, and hierarchy.
- `composed-map.png`: deterministic map after generated/curated icons or other visual assets have been placed.
- `visual-polish.png`: image-generation edit of the composed map for visual quality only.
- `final-map.png`: final user-facing image. This may be the polished image, a restored composite, or a repaired polish that keeps the best visual treatment while restoring exact text, icon masks, and critical diagram structure.

## When to Use

Use this workflow by default when:

- The user asks for a finished PNG, portfolio-ready map, polished system diagram, case-study visual, or visual style adaptation.
- The user asks for stronger visual quality, portfolio polish, Pinterest-inspired aesthetics, or a less mechanical diagram.
- The structured map is logically correct but still feels flat, stiff, or too much like boxes and arrows.
- A reference style calls for richer depth, softer card treatment, better texture, more integrated icons, or more coherent color.

Avoid this workflow when:

- The user needs a strictly editable diagram only.
- The map contains dense small text that image generation is likely to distort.
- The diagram is a regulated, legal, scientific, or operational document where exact labels matter more than visual polish.

Do not skip polish merely because the subject is medical, institutional, clinical, or operational. Skip only when exact text risk truly outweighs visual finish, and document that reason. A skipped-polish diagram must still pass text-fit, connector-anchor, density, and structure-semantics checks before it can be called final.

## Required Sequence

1. Render the structured draft first.
   - Use `scripts/render_system_map.py` or project-specific code.
   - Fix collisions, cramped labels, tiny icons, overflow text, clipped labels, unanchored arcs, decorative loops, and unclear relationships before using image generation.
   - If the content is sparse, enlarge the core modules, icons, text, and callouts or choose a more compact structure. Do not leave tiny cards floating across a mostly empty canvas.
   - The draft should already be acceptable as a diagram.

2. Inspect the structured draft.
   - Use `view_image` or an equivalent visual inspection path.
   - Check title, subtitle, node labels, secondary labels, edge labels, legend, footer, and icon placement.
   - Check every major connector endpoint and every large background structure. Curves, loops, rings, and ellipses must connect to a specific node, zone, stage, or semantic boundary.
   - Remove or redraw any arc that misses its endpoint, crosses through a central product icon, cuts through labels, or exists only as decoration.

3. Send the composed map to `imagegen` as an image edit.
   - Use the built-in `image_gen` tool through the `imagegen` skill when available.
   - Ask for visual polish only.
   - Preserve exact text, layout, node names, relationship labels, arrows, rings, legend content, and hierarchy.

4. Save the polished image as `visual-polish.png` and inspect it.
   - Compare it against `composed-map.png`, not only the earlier structured draft.
   - Classify the result as accept, repair, or reject.
   - Accept only if it keeps exact text and system logic while improving the visual finish.
   - Repair if it has the strongest visual direction but introduces local defects such as misspelled labels, warped text, damaged icon corners, broken label pills, softened edge labels, or small unwanted icon/container changes.
   - Reject if it invents stakeholders, changes relationship meaning, moves major nodes, removes required content, or makes the diagram impossible to restore cleanly.

5. Restore or repair deterministically if needed.
   - If the polished image has stronger visual treatment but imperfect text, use Pillow or another deterministic renderer to composite exact text, labels, and legend back from the composed map or JSON spec.
   - If icon corners, icon masks, or icon containers are broken, re-mask/re-place the original composed icons and containers over the polished background.
   - If a polished result adds a visually useful icon to a previously text-only node, keep it only when it does not introduce a new stakeholder, claim, logo, or misleading meaning. Otherwise cover it with the deterministic card area from the composed map.
   - Restore critical arrows, line types, label pills, legends, and group labels when image generation changes their meaning or readability.
   - Preserve the polished background, card depth, global spacing, and overall visual direction when possible.
   - Name the repaired artifact `final-map.png`.

6. If polish is skipped or rejected, do not silently deliver the code render as the final portfolio map.
   - Use a name such as `structured-draft.png` or `code-rendered-map.png`.
   - Explain the reason: user requested editability/code-only output, dense text, image generation unavailable, exact regulated content, or polish defects could not be repaired cleanly.
   - If the user accepts the tradeoff, then a code-rendered `final-map.png` is allowed.

## Imagegen Prompt Pattern

Use a prompt like this for whole-map polish:

```text
Edit the provided system map image. Keep the exact layout, all text, node names, relationship labels, arrows, rings, and legend content unchanged. Do not add, remove, rename, or move any stakeholders. Do not rewrite text.

Visual polish only: make the map look more portfolio-ready and professionally designed. Improve subtle background texture, card depth, shadows, rounded card treatment, icon integration, line anti-aliasing, spacing feel, and overall color harmony.

Preserve legibility: all text must remain sharp and readable. Preserve the structured diagram feel, not a realistic scene. Avoid heavy gradients, glossy 3D effects, photorealism, extra decorative objects, watermarks, logos, or any new text.
```

Adapt the color and style sentence to the selected preset or user reference. Keep the preservation instructions strict.

## Text Restoration Rules

If text restoration is needed:

- Use the structured JSON or deterministic draft as the label source, never OCR from the polished image.
- Restore all critical text: title, subtitle, node names, secondary node descriptions, relationship labels, legend labels, group labels, and source/footer notes.
- Keep a readable minimum line-height. Do not place restored text directly on icons or complex textures.
- If the polished card area became too small for exact text, prioritize exactness and readability over preserving that polished area.

## Repair Decision Rules

Use this decision rule after inspecting `visual-polish.png`:

- Accept polish: visual quality improves and all text, icons, relationships, and hierarchy remain correct.
- Repair polish: visual quality is best, but defects are local and deterministic overlays can fix them. Typical repairs include exact text replacement, icon corner/mask restoration, label pill cleanup, legend replacement, and arrow replacement.
- Reject polish: defects change the system meaning, add/remove stakeholders, rewrite substantial labels, or require so many overlays that the polished image no longer contributes useful value.

When repairing, keep a copy of the unmodified polished candidate as `visual-polish.png`, then write the repaired result to `final-map.png`.

## Quality Checklist

Before delivering `final-map.png`, confirm:

- No stakeholder was added, removed, renamed, or moved into a misleading group.
- No relationship direction, type, strength, or label changed.
- All title, node, legend, and key edge text is readable at portfolio viewing size.
- No text overflows its card, pill, callout, label area, or boundary.
- Icons remain fully inside their intended containers unless the chosen style intentionally uses a consistent break-frame treatment.
- Icon containers preserve their intended rounded corners or masks; generated icon sheet cell backgrounds must not cover container corners.
- Cards have enough internal padding around text and icons.
- Every line, arrow, arc, loop, ring, or ribbon has an intended semantic anchor and does not accidentally cut through central icons or labels.
- The composition uses the canvas proportionally: sparse diagrams should have larger cards, icons, and type, not small objects scattered across long distances.
- The color system still reads as one coherent palette, not random category colors.
- The final image still looks like a system map, not a generic illustration.

## Deliverables

When this workflow is used, provide:

- `final-map.png`: the image to show the user.
- `structured-draft.png`: exact diagram source image for future edits.
- `composed-map.png`: deterministic map with generated/curated assets placed, when separate from the structured draft.
- `visual-polish.png`: unmodified image-generation polish candidate, useful for comparison and repair audit.
- `stakeholder-system-map.json`: editable map data.
- `stakeholder-analysis.md`: text-only analysis.
- `style-notes.md`: when a user reference, researched style, or named preset influenced the visual direction.
