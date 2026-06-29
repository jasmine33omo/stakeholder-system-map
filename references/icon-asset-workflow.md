# Icon and Avatar Asset Workflow

Use this when a stakeholder/system map needs portfolio-grade icon, avatar, device, or infrastructure visuals.

## Default Asset Strategy

1. First decide whether icons should be curated vector assets or generated bitmap illustrations.
2. Use a curated vector icon family when the map needs neutral, clean, deterministic symbols.
3. Use the `imagegen` skill when the map needs custom role avatars, product/device illustrations, or a more editorial visual language.
4. Keep all assets in one coherent style: same stroke weight, perspective, line detail, shadow treatment, and color palette.

For portfolio-ready output, primary actor icons, product illustrations, device/system icons, and role avatars must come from a curated professional icon set or an `imagegen`-generated icon sheet. Hand-coded Pillow primitives are acceptable only for draft layout, fallback debugging, or an explicitly requested sketch style. Do not deliver a code-drawn placeholder icon set as the final portfolio image.

For the default `concentric-territory-ecosystem` style, generate person/avatar icons only. The default visual grammar represents places, rooms, products, devices, data systems, and institutions as text labels or territories, not as object icons. Use non-person icons only when the selected style preset or user reference explicitly calls for them.

## Image Model Path

The available image-generation path is the `imagegen` skill:

- Default: built-in `image_gen` tool for normal bitmap generation and editing.
- Fallback: imagegen CLI only if the user explicitly asks for API/model control, or when true transparent output is required and the user confirms the fallback.

Do not present hand-coded Pillow primitives as final-quality icons unless the user asks for a sketch/prototype style. If image generation is unavailable and no curated icon set is used, label the output as a draft or explain the limitation before delivery.

## Recommended Prompt Pattern

Generate an icon sheet rather than unrelated one-off icons whenever possible:

```text
Use case: infographic-diagram
Asset type: system map icon sheet
Primary request: Create a cohesive set of flat editorial icons for a stakeholder system map.
Subjects: <list of actors and systems>
Style: clean vector-like editorial illustration, consistent stroke weight, rounded geometry, no text, no logos, no watermark.
Palette: <map palette>
Composition: each icon centered in its own evenly spaced cell on a flat chroma-key background, generous padding, front-facing or simple three-quarter view.
Avoid: photorealism, 3D effects, busy backgrounds, shadows that complicate cutout, tiny details, inconsistent perspectives.
```

For a hospital medication delivery vehicle map, the icon sheet might include:

- courier standing on a compact delivery vehicle
- ward nurse
- pharmacy / medication tray
- smart delivery vehicle
- logistics database
- identity scan card
- elevator
- stairs / ward corridor
- maintenance / charging

For an economy seat cushion system map, the icon sheet might include:

- seated economy passenger on a cushion
- sliding cushion rail mechanism
- airline commercial / preferred-seat value
- cabin crew member
- maintenance technician with replacement cushion
- FAP or crew panel with seat states
- pressure sensor pad
- vibration motor reminder module
- safety / certification shield

## Required Portfolio Asset Sequence

For normal portfolio-ready system maps:

1. Render a structured draft with empty icon slots or draft placeholders.
2. Generate or select the icon family.
3. Save the icon source sheet in the project assets folder.
4. Convert generated icons to transparent-background PNGs before placement. For built-in image generation, use a flat chroma-key background plus local removal when possible; if the generated sheet has a white/off-white background, remove only the edge-connected background so white details inside the icon are preserved.
5. Crop/place icons into the deterministic layout.
6. Inspect the composed map before whole-map polish.
7. Continue to `visual-polish-workflow.md` for final image-generation polish unless the user explicitly wants code-only output.

If step 2 is skipped, record why in `style-notes.md` and do not imply that the icons were image-generated.

## Transparency and Cropping

Built-in image generation does not need to be the final transparent asset. For project-bound assets:

1. Generate on a flat chroma-key background if transparency is needed.
2. Remove the background locally with the imagegen chroma-key helper.
3. If a sheet arrives on white/off-white instead, remove only the edge-connected background, not all white pixels.
4. Crop each icon to its content bounding box plus consistent padding.
5. Place the icons at consistent optical sizes in the map.

For circular avatar styles, verify transparency before composition. A square white or off-white icon cell inside a circle is a failed asset, even if the circle mask hides some corners.

## Sizing Rules

- Central product/service illustration: 120-180 px tall in the final PNG.
- Primary stakeholder avatar/icon: 64-96 px tall.
- Secondary system/infrastructure icon: 56-80 px tall.
- Micro markers: 24-40 px, only for decoration or small status hints.

Never make a primary icon so small that it becomes an unreadable pictogram. If space is tight, reduce the number of visible actors, enlarge the canvas, or switch to a layout with more room.

## Text and Icon Layout

- Use separate icon and text zones inside each node.
- Icons must sit fully inside their card or container unless the user explicitly requests a deliberate break-frame style. Accidental half-inside/half-outside icons are not acceptable.
- For circular icon-label styles, icons should be transparent PNGs; do not place square white-background image cells inside small circles.
- If icons are cropped from an image-generated sheet, place them through a deterministic rounded mask or alpha mask so the sheet cell background cannot cover rounded icon-container corners.
- Keep at least 16 px between icon and primary label.
- Keep at least 10-16 px between primary and secondary label baselines; use more spacing for portfolio maps than for dense dashboards.
- Keep label and sublabel line-height at 1.25-1.45.
- If a node contains an icon, label, and sublabel, the card must be tall enough for all three without overlap.
- Relationship label pills must have generous padding around text: at least 22-28 px horizontal and 12-16 px vertical in the final PNG.
- If a generated icon has too much internal detail, simplify the prompt or use a curated vector symbol instead.
