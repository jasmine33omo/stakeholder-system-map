# Universal System Map Style Library

Use this library when choosing a map style without user-provided visual references. These styles are organized by communication task, not by industry.

## Selection Rule

1. Pick the style that best matches the argument the diagram must make.
2. Keep the default visual language domain-neutral unless the user asks for a specific field or brand mood.
3. Prefer 8-16 stakeholder nodes for portfolio maps; collapse minor actors into group nodes.
4. Use sparse edge labels and explain detailed relationships in `stakeholder-analysis.md`.
5. Use `concentric-territory-ecosystem` as the first default when the map can be explained by core people, place contexts, external factors, proximity, and a few critical relationships.
6. Do not force this default when the primary argument is a strict sequence, a transaction/value exchange network, or a governance prioritization matrix.

## Presets

### concentric-territory-ecosystem

- Best for: most portfolio-ready stakeholder/system maps where the core argument is "who surrounds the experience, which fields they belong to, and which few relationships matter most."
- Layout: near-square canvas; three concentric fields labeled `People`, `Place`, and `Other factors`; core people in large circles; secondary people as avatar labels; place names as text; pale blue ellipses grouping people with related places.
- Visual language: person/avatar labels, dark blue place labels, light blue sub-place labels, soft translucent circles/ellipses, dashed guide rings, and only 3-6 strong arrows.
- Canvas: square or near-square, normally native `3200x3200` or larger.
- Palette: warm neutral background, pale gray external field, pale blue service/place field, warm pink people/care field, blue place/resource ellipses, purple core relationship arrows.
- Center rule: put the primary beneficiary and 1-2 other key people in the central people field. Do not default to a product/device object as the visual center in this preset.
- Use when the key question is: "How is the experience shaped by people, places, and external forces?"
- Avoid when: the map must show a strict step-by-step flow, a dense exchange network, or a power-interest prioritization matrix.

### radial-ecosystem

- Best for: central product/service, broad ecosystem, direct vs indirect stakeholders.
- Layout: project at center; primary actors near the center; institutions, partners, external forces in outer rings.
- Visual language: soft rings or invisible radial zones, rounded nodes, curved/offset connections.
- Canvas: landscape 3:2 or square.
- Palette: warm off-white background, charcoal text, 4-6 muted group colors.
- Use when the key question is: "Who surrounds this design and how close are they?"

### service-system-flow

- Best for: service journeys, delivery chains, handoffs, operational workflows.
- Layout: left-to-right stages with actor lanes or clustered touchpoints.
- Visual language: compact rounded rectangles, directional arrows, stage labels, thin dividers.
- Canvas: wide landscape.
- Palette: quiet neutral background, one primary accent, one warning/friction accent.
- Use when the key question is: "How does the service move across people, touchpoints, and systems?"

### value-exchange-map

- Best for: resources, value, data, money, material, attention, trust, or capability exchange.
- Layout: network map with clear directional flows; group by actor type or value domain.
- Visual language: line weight for importance, dashed lines for data/information, distinct conflict styling.
- Canvas: landscape or square depending on density.
- Palette: restrained base colors plus semantic edge colors.
- Use when the key question is: "What does each actor give, receive, and depend on?"

### power-interest-map

- Best for: prioritizing stakeholders, governance, adoption strategy, political constraints.
- Layout: four quadrants or concentric priority zones.
- Visual language: axes, soft quadrant backgrounds, compact labels, minimal edge clutter.
- Canvas: square or 4:3.
- Palette: four muted quadrant fields; use contrast carefully so labels remain readable.
- Use when the key question is: "Who has power, who cares, and who must be managed closely?"

### layered-system-map

- Best for: complex sociotechnical systems, platform/service stacks, public systems, policy layers.
- Layout: horizontal layers such as user/community, frontstage, operations, platform/data, governance, external forces.
- Visual language: bands, small node cards, vertical dependencies, few cross-layer arrows.
- Canvas: wide landscape or poster portrait if many layers are needed.
- Palette: neutral bands with subtle tint changes; one accent for critical dependencies.
- Use when the key question is: "Which layer of the system creates or constrains value?"
- Avoid when: the map has few actors, the core argument is a product-centered service moment, or the page would become small cards spread across large empty bands.

### editorial-portfolio-map

- Best for: portfolio pages, presentation boards, concept overviews, final storytelling.
- Layout: asymmetrical but balanced composition; fewer nodes; title and legend integrated elegantly.
- Visual language: generous whitespace, fewer line types, larger labels, strong hierarchy.
- Canvas: 16:10, 3:2, or portfolio page ratio.
- Palette: domain-neutral neutrals plus 2-3 accents.
- Use when the key question is: "How do we make the system legible and visually polished at first glance?"

### object-centered-service-map

- Best for: a product, device, fixture, wearable, or interface that reorganizes one core service moment.
- Layout: large central product/service illustration; 3-5 surrounding service moments, stakeholder roles, or system modules; small callouts for responsibilities and feedback.
- Visual language: larger typography, fewer nodes, icon/label callouts, compact legends, and minimal background structure.
- Canvas: 16:10, 3:2, or square.
- Palette: quiet neutral background plus 2-3 semantic accents.
- Use when the key question is: "How does this product change the service moment around it?"
- Avoid when: the main argument is a long sequential workflow or a many-actor governance ecosystem.

## Domain Adaptation

Only adapt toward a domain mood when the project or reference supports it:

- Technology: sharper geometry, cool accent, data/information lines more prominent.
- Public service: calm contrast, accessible typography, clear authority and feedback lines.
- Education/children: softer shapes, brighter accents, fewer institutional details.
- Sustainability: earthy but not monochrome; highlight material and environmental externalities.
- Luxury/culture: more editorial spacing, fewer colors, refined typography, restrained linework.
- Community/social innovation: emphasize trust, feedback, power imbalance, and excluded groups.

## Visual Defaults

- Background: `#F8F7F2` or another warm neutral.
- Text: near-charcoal, not pure black.
- Type: use a clean system sans; for Chinese, prefer PingFang, Heiti, or Hiragino fallbacks.
- Nodes: choose from icons, avatars, dots, tags, callouts, cards, rings, clusters, or feature cards according to the selected structure. Rounded cards are only one option, not the default.
- Edges: 4-6 semantic types maximum in the legend.
- Labels: short actor names on the PNG; detailed goals/pains in the Markdown analysis.
- Text fit: measure text before export. Increase card size, reduce copy, reflow labels, or change structure instead of allowing overflow or clipped text.
- Density: sparse maps should use larger modules, larger icons, and larger type. Avoid tiny nodes placed far apart just to fill a wide canvas.
- Connectors: every line, arc, loop, or ribbon must have a meaningful endpoint or zone membership. Remove decorative curves, especially ones that miss nodes or cut through product icons and labels.
