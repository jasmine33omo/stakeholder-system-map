---
name: stakeholder-system-map
description: Research, analyze, and visualize stakeholder systems for design projects. Use when a user gives a design idea, service concept, product proposal, social innovation project, urban/community intervention, UX case study, or portfolio project and wants AI to identify stakeholders, map relationships, explain interests/conflicts/power/resource flows, create a portfolio-ready stakeholder or system map as PNG, and optionally adapt the visual language from user-provided reference style templates.
---

# Stakeholder System Map

## Overview

Use this skill to turn a design concept or project description from any design domain into a researched stakeholder system analysis and a finished PNG system map suitable for a design portfolio. Always produce both a visual artifact and a text-only analysis unless the user asks for only one.

Default language: English. Write the PNG labels, title, legend, JSON labels, and Markdown analysis in English unless the user explicitly asks for Chinese or another language. If the user's project description is in Chinese but they do not specify an output language, translate the analysis and diagram labels into polished English.

## Core Workflow

1. Define the system boundary.
   - Restate the design concept, geography, industry, service moment, and intended audience.
   - If the user gives little context, make practical assumptions and label them in the analysis.
   - Separate the project owner, primary users, secondary users, operators, regulators, funders, partners, affected non-users, and external forces.

2. Research missing stakeholder context.
   - Browse when current facts, local institutions, regulations, market actors, public programs, or real organizations could change or are uncertain.
   - Prefer primary or authoritative sources for government, policy, institutional, and company facts.
   - Cite sources in the text analysis. Mark uncited reasoning as "inferred" rather than factual.
   - Do not invent named organizations when generic stakeholder categories are more honest.

3. Build the stakeholder model.
   - Identify each stakeholder's role, goals, needs, pain points, influence level, dependency level, resources contributed, value received, risks, and likely attitude toward the design.
   - Classify relationships as one or more of: service flow, information flow, money flow, material/resource flow, authority/regulation, influence/trust, conflict/friction, dependency, feedback loop.
   - Note direction, strength, certainty, and whether each relationship is factual, sourced, user-provided, or inferred.
   - For visual maps, also identify secondary tasks, minor actors, hidden handoffs, preparation/storage/cleaning/maintenance contexts, records, training, procurement, safety, privacy, exception handling, and external constraints before deciding what appears on the PNG.

4. Find design implications.
   - Surface leverage points, blockers, hidden beneficiaries, excluded groups, conflicting incentives, consent/privacy risks, maintenance responsibilities, and adoption constraints.
   - Translate the map into opportunities the designer can act on.

5. Choose the map structure.
   - Choose by the communication task, not by industry.
   - Default to `concentric-territory-ecosystem` for most portfolio-ready maps when the user provides no reference and the system can be explained through centrality, stakeholder distance, shared territories, and a few critical relationships.
   - Use `radial-ecosystem` for central product/service ecosystems and broad external forces.
   - Use `service-system-flow` for service chains with stages, touchpoints, and operators.
   - Use `value-exchange-map` when value, resource, data, or money flows are the argument.
   - Use `power-interest-map` when governance, decision power, adoption, or stakeholder priority is the argument.
   - Use `layered-system-map` when user, organization, platform, policy, and external forces must be separated.
   - Use `editorial-portfolio-map` when the portfolio page needs a quieter, more polished summary rather than a dense research board.
   - Read `references/style-library.md` when selecting a visual direction.
   - Read `references/concentric-territory-default.md` before using or adapting the default concentric-territory style.
   - If the user provides a reference image, first read `references/reference-style-deconstruction.md` and extract the reference's structure grammar before choosing a renderer or node form.
   - Do not repeatedly fall back to horizontal layer bands or rounded card workflows. Use `layered-system-map` only when layers are the clearest argument; otherwise prefer radial, ecosystem, value-exchange, orbit/constellation, editorial, or a user-reference-derived structure.

6. Decide whether visual assets are needed.
   - For polished portfolio maps, do not rely on tiny primitive icons or text-only node boxes.
   - For final portfolio PNGs, use either a curated professional icon family or an `imagegen`-generated icon/avatar sheet for all primary actors and product/system modules.
   - Use hand-drawn Pillow primitives only for rough drafts, layout tests, or explicit sketch styles. Do not present them as final portfolio icons.
   - Use the `imagegen` skill when the map needs custom role avatars, device illustrations, institutional badges, a coherent illustrative icon family, or no suitable curated icon set exists.
   - Read `references/icon-asset-workflow.md` before generating or placing custom icon/avatar assets.
   - Do not default to rounded icon cards. Match the reference's node expression system, such as icon-only nodes, avatar labels, ring dots, leader-line callouts, tag strips, cluster bubbles, mini-cards, or feature cards.

7. Produce deliverables.
   - `stakeholder-analysis.md`: text-only analysis.
   - `stakeholder-system-map.json`: structured map spec for rendering and future edits.
   - `structured-draft.png`: deterministic code-rendered map used as the source of truth.
   - `final-map.png`: portfolio-ready user-facing PNG at high resolution.
   - `preview-map.png`: optional smaller preview when useful for quick inspection.
   - For normal portfolio-ready output, use the structured draft -> generated/curated assets -> code composition -> imagegen visual polish -> QA -> deterministic text/icon repair workflow in `references/visual-polish-workflow.md`.
   - If the final user-facing PNG is only code-rendered, explicitly state why imagegen polish was skipped, such as user requested fully editable output, dense text made polish unsuitable, image generation was unavailable, or the user asked for code-only output.
   - Optional `style-notes.md` when the user provides visual references or asks for a named style preset.

## Output Requirements

### Text Analysis

Include these sections:

- Project framing: scope, assumptions, and system boundary.
- Stakeholder inventory: grouped table with role, goals, pains, influence, dependency, contribution, and value received.
- Relationship analysis: explain the most important connections and whether they are service, information, money, authority, resource, influence, conflict, or feedback relationships.
- Tensions and leverage points: conflicts, bottlenecks, missing actors, risks, and design opportunities.
- Source notes: citations for researched facts and a short list of inferred assumptions.

### PNG System Map

Create a polished map with:

- Clear title and subtitle.
- Portfolio-ready resolution: `final-map.png` should normally be at least 3200 px on the long edge, and preferably 2x the intended display size. Use native high-resolution rendering, such as a high-resolution canvas/SVG/vector export or Pillow renderer with scaled coordinates and fonts. Do not simply upscale a low-resolution preview and deliver it as final.
- Grouped stakeholders with readable labels.
- Professional typography: no overlapping text, cramped line-height, clipped labels, or text colliding with icons, arrows, rings, or legends.
- Hard text-fit rule: every visible text block must be measured against its container before export. If a label, title, subtitle, legend item, or stage caption exceeds its container, enlarge the container, shorten the label, reflow text, or switch layout. Do not deliver overflow or clipped text.
- Minimum text spacing: keep at least 1.25 line-height for multi-line labels, reserve a separate icon area and text area inside every node, and shorten labels before shrinking text below portfolio-readable size.
- Directional lines with a legend.
- Visual hierarchy for primary, secondary, institutional, and external-force actors.
- Meaningful large structures: rings, circles, loops, lanes, and segments must encode system domains, closeness, stage, power, responsibility, or value flow. Do not use them as decoration.
- Anchored connector rule: every visible line, arrow, arc, ribbon, or loop must have a clear semantic role and anchor to the intended node, zone, stage, or boundary. Remove unanchored decorative arcs and lines that pass through icons or labels without meaning.
- Relationship strength shown with line weight or opacity.
- Conflict/friction shown differently from cooperative flows.
- Adequate whitespace and no overlapping labels.
- Proportional density: if the map has few nodes or short labels, enlarge nodes, icons, font sizes, and spacing so the diagram intentionally uses the canvas. Avoid tiny cards floating far apart in a mostly empty frame.
- For the default three-ring concentric style, visible typography and node sizes must respond to content density. Sparse maps should grow in scale; dense maps should aggregate minor actors before shrinking text.
- If a layout produces text collisions, rerender with fewer visible edge labels, larger node cards, shorter labels, or a different map structure before final delivery.
- A neutral, domain-agnostic fallback style if no reference template is provided.
- Sparse edge labels. Label only the relationships that must be understood from the PNG alone; put detailed relationship explanations in `stakeholder-analysis.md`.

Use `scripts/render_system_map.py` for deterministic draft rendering when the user's request can be represented with the JSON schema in `references/map-schema.md`.

For the default `concentric-territory-ecosystem` preset, the renderer creates a near-square three-ring map: `People` at the center, `Place` in the middle, and `Other factors` in the outer field. It uses person/avatar icons for stakeholders, text labels for places and factors, pale blue person-place territories, and a small number of critical bidirectional arrows.

Example:

```bash
python3 scripts/render_system_map.py stakeholder-system-map.json stakeholder-system-map.png
```

If the local system Python lacks Pillow, use the bundled Codex runtime Python when available.

For portfolio-ready maps, keep the deterministic render as the source of truth and then apply the image-generation polish workflow in `references/visual-polish-workflow.md` by default. Deliver `final-map.png` as the user-facing PNG, and keep `structured-draft.png`, `composed-map.png`, and any `visual-polish.png` candidate available for auditability and future edits.

If the renderer creates a smaller inspection image, save it as `preview-map.png` and create a high-resolution `final-map.png`. Do not make the preview the final deliverable.

For diagrams, text-heavy maps, line art, and UI-like system maps, avoid sharpening filters as a substitute for true resolution. Sharpening is appropriate only for photo/scan cleanup or a deliberate raster-image finishing step after the map is already rendered at native final size.

Only skip whole-map image-generation polish when the user explicitly wants fully editable/code-only output, when the diagram is too text-dense for reliable image editing, when image generation is unavailable, or when exact operational/legal/scientific text accuracy is more important than visual finish. If skipped, say so clearly and name the output `structured-draft.png` or `code-rendered-map.png`, not `final-map.png`, unless the user has accepted that tradeoff.

Do not treat whole-map polish as a binary accept/reject step. If the polished image has the best visual direction but corrupts text, icon masks, or local structure, use it as the visual base and deterministically restore exact text, icon containers, and critical edges from the composed map or JSON. Prefer a repaired polished image over reverting to a flatter composed map when the repair can preserve both accuracy and visual quality.

Do not use image-generation polish to rescue a structurally weak draft. Fix text fit, connector anchors, layout density, and visual hierarchy deterministically first; then polish. If the deterministic map has overflow text, unanchored arcs, or decorative structures, it is not ready for polish or final delivery.

## Style Template Adaptation

Use style as a communication layer, not as an industry costume. The default map should not look medical, civic, educational, financial, or technology-specific unless the project or user reference calls for that.

When the user provides a reference image, deck page, poster, portfolio screenshot, or template:

1. Extract style rules rather than copying content.
2. Extract the reference's structural grammar: whether it uses concentric rings, overlapping territories, loop paths, service lanes, radial segments, callout constellations, or card networks.
3. Extract the reference's node expression grammar: icon-only, avatar+label, ring-dot, callout, tag strip, cluster bubble, mini-card, feature-card, or card.
4. Describe what every large visual field means in `style-notes.md`; if a ring/circle/loop cannot be assigned meaning, remove it.
5. Adapt color palette, typography feel, node geometry, line style, spacing, density, label treatment, legend placement, and title treatment.
6. Preserve the user's actual stakeholder content and relationship logic.
7. Avoid copying distinctive proprietary graphics, logos, or exact layouts unless the user owns the template or explicitly asks to use their own file.

Read `references/style-adaptation.md` and `references/reference-style-deconstruction.md` before applying a reference style.

When the user asks for the AI to research visual references:

1. Search broadly across service design, systems thinking, stakeholder mapping, platform ecosystems, public service, social innovation, product strategy, urban systems, and portfolio diagrams.
2. Prefer Pinterest/image search discovery when requested, but use public design articles, templates, and portfolio pages as backups when Pinterest is blocked by login or crawling limits.
3. Record sources, reusable style rules, and non-copyable parts in `style-notes.md` or a project-specific research note.
4. Read `references/pinterest-style-study.md` when the user wants Pinterest-inspired visual improvement, especially icon/avatar, Venn, ring, blueprint, or poster-style maps.
5. Use the style families in `references/style-library.md` as the canonical presets.
6. Do not let a test project's domain become the default style for future projects.

## Structured Map Spec

Use `references/map-schema.md` for the JSON fields accepted by the renderer. Prefer explicit `x` and `y` coordinates for final portfolio maps. Use automatic layout only for first drafts.

Keep the JSON as an editable intermediate artifact so the user can ask for changes like "make government less central", "show conflict more strongly", or "use the template colors".

For dense maps, set `style.show_node_roles` to `false` and use `show_label: true` only on the most important edges.

## Icon and Illustration Quality

Prefer a consistent icon system over ad hoc hand-drawn shapes. For deterministic renderers, use a single coherent icon family or carefully designed simple vector symbols. Use hand-drawn Pillow primitives only for rough drafts, not final portfolio output, unless the user explicitly wants a sketch style.

When the map requires a polished illustrative look, use generated bitmap assets or a curated icon set for role avatars, devices, buildings, data systems, and infrastructure. Keep icon style consistent across all nodes: same stroke weight, perspective, level of detail, and color treatment.

Use `imagegen` for custom bitmap assets. The normal path is the built-in `image_gen` tool through the `imagegen` skill. CLI/API fallback is only for explicit model/API control or true transparent-background workflows and requires the user's confirmation when applicable.

Use image generation for two different jobs with different constraints:

- Asset generation: create icon sheets, avatars, product illustrations, or badges before deterministic composition.
- Whole-map visual polish: lightly improve the already-rendered composed map without changing layout, text, stakeholders, or relationship logic. Read `references/visual-polish-workflow.md` before using this step.

For normal portfolio-ready outputs, both jobs should be considered part of the default production path. If either job is skipped, document the reason in `style-notes.md` or in the final response.

Icon placement rules:

- Primary stakeholder icons or avatars should be visually significant, not decorative specks.
- In the default `concentric-territory-ecosystem` style, use person/avatar icons only; represent places, products, devices, systems, and external factors through labels, territories, and the text analysis unless the user reference calls for object icons.
- Reserve at least 56-80 px of final PNG height for ordinary node icons and 120-180 px for the central product/service illustration.
- Keep icon and text in separate zones inside a node. Do not place labels directly on top of icons.
- Keep generated icons fully inside their node container unless a deliberate, consistent break-frame style is requested.
- Give relationship label pills enough padding around text; the border should not hug the words.
- Use comfortable spacing between primary and secondary node labels; do not stack them tightly.
- If an icon must be smaller than 40 px in the final PNG, treat it as a secondary marker and do not rely on it for recognition.
- Prefer generating an icon sheet with all required assets in one coherent style, then crop/place each icon consistently.

Node expression rules:

- Cards are not the default answer. Use card nodes only when the selected preset or reference style needs them.
- For concentric, Venn, orbit, or constellation references, prefer icons, avatars, dots, leader labels, and tags over full cards.
- If using a reference with small icons and leader lines, keep PNG labels short and move secondary descriptions to `stakeholder-analysis.md`.
- Use spatial membership as a relationship when the reference is area-based; avoid adding arrows for every relationship.

## Quality Check

Before final delivery:

- Re-read the text analysis and ensure every major claim is either sourced, user-provided, or marked as inferred.
- Check the pixel dimensions and render method of `final-map.png`; the long edge should usually be 3200 px or larger and should be produced by native high-resolution rendering, not low-resolution upscale.
- Open or inspect the PNG and confirm all labels fit inside their containers, labels are readable, nodes do not collide, and the legend matches the rendered edge types.
- Confirm each major connector starts and ends at an intended node, stage, zone, or boundary. Remove any large arc or loop that is not anchored and explained.
- Confirm large loops, ellipses, bands, and zones do not pass through central product icons or text unless they intentionally encode an overlap and remain visually clean.
- Confirm the layout density matches the content volume: a sparse map should have larger typography and modules, not tiny labels in a wide empty canvas.
- For `concentric-territory-ecosystem`, confirm blue territories contain their intended `territory_people` and place labels, purple dashed supplementary relations route outside the core people field, no extra guide rings appear unless named, and every blue person-place arrow follows from explicit edges, `places[].arrow_people`, or a marked core touchpoint.
- For `concentric-territory-ecosystem`, do not name the output `final-map.png` if it still uses generic fallback person icons. Generate or curate distinct transparent-background role avatars first, then compose and polish.
- Confirm `final-map.png` is the polished final artifact for portfolio-ready requests. If the delivered image is only the deterministic code render, confirm the user explicitly requested or accepted that limitation.
- If image-generation polish was used, compare the polished image against the composed map and confirm no text, node, edge, legend item, icon mask, or hierarchy was added, removed, renamed, or made unreadable. If the polish is visually strongest but imperfect, repair it deterministically before naming it `final-map.png`.
- Ensure the diagram can stand alone in a portfolio without the chat history.
- Mention any limitations, such as uncertain stakeholders, missing local context, or unverified assumptions.
