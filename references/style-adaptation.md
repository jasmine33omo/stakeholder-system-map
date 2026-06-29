# Style Adaptation Guide

Use this guide when the user provides a reference style template, portfolio page, diagram screenshot, slide, or visual example.

For default styles and AI-researched visual directions, read `style-library.md` first. For online research starting points, read `online-style-research.md`. For Pinterest-inspired improvements with icons, avatars, rings, Venn territories, blueprint lanes, or poster-style maps, read `pinterest-style-study.md`.

When the user provides a concrete reference image, also read `reference-style-deconstruction.md`. Do not start from the default rounded-card renderer and skin it with the reference colors. First identify the reference's structure grammar and node expression grammar.

## Extract These Style Rules

Create `style-notes.md` with:

- Overall mood: academic, editorial, service-design, speculative, technical, playful, minimal, dense, etc.
- Canvas ratio and composition: landscape, portrait, square, central radial, left-to-right process, rings, columns, layered bands.
- Expression structure: radial ecosystem, service flow, value exchange, power-interest, layered system, or editorial portfolio.
- Structure grammar: concentric orbit, Venn territory, ecosystem loop, service blueprint, radial segment, callout constellation, or card network.
- Large-shape semantics: what each circle, ring, loop, lane, segment, or field means. If a large shape has no meaning, do not use it.
- Overlap semantics: what it means when nodes or zones overlap, such as shared responsibility, multi-sided value, cross-channel handoff, or governance constraint.
- Color system: background, primary accents, secondary accents, neutral text, warning/conflict color.
- Typography feel: geometric, humanist, condensed, serif, mono, handwritten; include practical system-font substitutes.
- Node language: icon-only, avatar+label, ring-dot, callout, tag strip, cluster bubble, mini-card, feature-card, or full card.
- Edge language: leader lines, radial guide lines, straight, curved, orthogonal, dashed, dotted, thick journey ribbons, faint association lines, arrowheads, no arrowheads.
- Label density: terse labels only, explanatory captions, numbered callouts, annotated research map.
- Legend and metadata treatment: prominent legend, small corner key, caption block, source note.

## Structure Before Surface

Use this decision sequence:

1. What is the reference's primary organizing device?
   - Rings/distance, overlapping territories, loop stages, lanes, segments, or cards.
2. What information does that organizing device encode?
   - Stakeholder closeness, system domain, journey stage, value flow, operational responsibility, power, or external constraint.
3. How are nodes expressed?
   - Small icons, dots, avatars, tags, callouts, clusters, or cards.
4. How are relationships expressed?
   - Spatial membership, overlap, leader line, loop order, arrow, or line type.
5. Which details should be removed from the PNG and moved to the text analysis?

Only after answering these should you render.

## Adapt Without Copying

Borrow transferable rules, not unique artwork. Do not reproduce logos, proprietary templates, exact illustrations, or highly distinctive compositions unless the user owns them.

Good adaptation:

- "Use a warm off-white background, thin charcoal lines, muted red conflict links, and small uppercase group labels."
- "Use a dense service-design board style with grouped columns and compact node tags."

Bad adaptation:

- "Copy the exact poster layout and illustration."
- "Trace the reference icons."

## Convert Style Notes to Renderer Settings

Map the extracted rules into `stakeholder-system-map.json`:

- Structure family -> `style.preset`
- Background -> `style.background`
- Main text -> `style.text_color`
- Title -> `style.title_color`
- Group colors -> `groups[].color`
- Node size -> `style.node_radius`
- Node shape -> `style.node_shape`
- Edge weight -> `style.line_width`
- Canvas ratio -> `canvas.width` and `canvas.height`
- Structure grammar -> `style.structure_grammar`
- Node expression -> `style.node_expression`
- Large semantic fields -> `zones[]` or project-specific `loop_domains[]`

If the reference uses a layout the renderer cannot reproduce well, create a custom SVG/HTML/canvas workflow and export PNG from that instead. Still keep a JSON or Markdown intermediate that documents nodes and relationships.

## Card Overuse Check

Before final rendering, count visible nodes. If most nodes are rounded cards but the reference mainly uses icons, dots, callouts, tags, or rings, the adaptation has failed. Redesign the node system to match the reference and shorten labels.

## Avoid Domain Lock-In

Do not let the user's test example define the skill's default look. A hospital, mobility, education, civic, luxury, sustainability, or platform project may need a different mood, but the style preset should first follow the diagram's purpose: ecosystem, flow, exchange, power, layer, or portfolio summary.
