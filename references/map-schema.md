# Stakeholder System Map JSON Schema

Use this schema to create `stakeholder-system-map.json` for `scripts/render_system_map.py`.

## Top-Level Fields

```json
{
  "title": "System map title",
  "subtitle": "Short project/context subtitle",
  "language": "en",
  "canvas": { "width": 3600, "height": 2400, "margin": 180 },
  "style": {},
  "groups": [],
  "zones": [],
  "external_factors": [],
  "nodes": [],
  "edges": [],
  "legend": []
}
```

`language` is optional and defaults to `en`. Use English labels and analysis unless the user explicitly requests Chinese or another language.

## Style

All fields are optional.

```json
{
  "preset": "radial-ecosystem",
  "structure_grammar": "concentric-orbit",
  "node_expression": "avatar-label",
  "background": "#F7F5EF",
  "title_color": "#1F2933",
  "text_color": "#263238",
  "muted_text": "#667085",
  "font": "Arial",
  "node_radius": 58,
  "line_width": 4,
  "show_node_roles": false,
  "node_shape": "circle",
  "palette": ["#3A6EA5", "#5B8E7D", "#E3B23C", "#C1666B", "#6D597A"]
}
```

`preset` is optional. Supported values:

- `radial-ecosystem`
- `concentric-territory-ecosystem`
- `service-system-flow`
- `value-exchange-map`
- `power-interest-map`
- `layered-system-map`
- `editorial-portfolio-map`

Explicit style fields override preset defaults.

`node_shape` is optional. Supported values: `circle`, `card`, `tag`.

`structure_grammar` and `node_expression` are optional documentation fields used when custom renderers or reference-style adaptations are needed. They help preserve the intended visual logic even when `scripts/render_system_map.py` does not support the full layout. Suggested `structure_grammar` values: `concentric-territory-ecosystem`, `concentric-orbit`, `venn-territory`, `ecosystem-loop`, `service-blueprint`, `radial-segment`, `callout-constellation`, `card-network`. Suggested `node_expression` values: `icon-only`, `avatar-label`, `ring-dot`, `callout`, `tag-strip`, `cluster-bubble`, `mini-card`, `feature-card`, `card`.

The renderer uses system fonts through Pillow. If the specified font is unavailable, it falls back to common macOS and DejaVu fonts, including Chinese-capable PingFang, Heiti, and Hiragino candidates.

## Groups

Groups organize stakeholders visually and semantically.

```json
{
  "id": "public-sector",
  "label": "Public sector",
  "color": "#3A6EA5",
  "description": "Government agencies, regulators, and public service teams"
}
```

## Zones / Semantic Fields

Use `zones` or a project-specific field such as `loop_domains` when large visual areas carry meaning. This is especially important for Venn, concentric, orbit, service-loop, or reference-style maps.

```json
{
  "id": "crew-data",
  "label": "Crew assistance + seat data",
  "kind": "loop",
  "meaning": "In-flight sensing, FAP visualization, haptic reminder control, and crew workflow support",
  "contains": ["sensor-layer", "fap-panel", "cabin-crew"]
}
```

Every zone that appears in the PNG should have a clear `meaning`. Do not include decorative rings or loops in a final portfolio map.

For the default `concentric-territory-ecosystem` preset, use zones to describe translucent fields:

```json
{
  "id": "bedside-care",
  "label": "Bedside care",
  "kind": "blue-territory",
  "meaning": "Physical service context and nearby care touchpoints",
  "x": 0.34,
  "y": 0.55,
  "width": 0.34,
  "height": 0.42,
  "contains": ["patient", "caregiver", "device"]
}
```

Recommended `kind` values for this preset:

- `outer-factors`: pale gray macro context ring.
- `service-context`: pale blue overall place/service field.
- `people-field`: warm pink social, care, trust, collaboration, or emotional-labor field.
- `blue-territory`: place, channel, institution, service touchpoint, or resource container. Use only when multiple nodes or touchpoints share that field.
- `dashed-ring`: distance, interaction frequency, influence strength, or system boundary guide.

`external_factors` is an optional array of short labels placed around the outer field, such as `["Policy", "Culture", "Cost", "Accessibility"]`.

For the default three-ring people/place style, prefer `places` over generic `zones` for blue association fields:

```json
{
  "id": "bedside",
  "label": "Bedside care",
  "x": 0.34,
  "y": 0.40,
  "width": 0.24,
  "height": 0.28,
  "related_people": ["patient", "caregiver"],
  "territory_people": ["patient"],
  "arrow_people": ["patient"],
  "person_overlap": 0.55,
  "max_width_factor": 1.32,
  "max_height_factor": 1.36,
  "alpha": 58,
  "subplaces": ["Water cup", "Cleaning tools", "Waste collection"]
}
```

`places` are rendered as dark blue text labels inside the `Place` ring. Their pale blue ellipse should group a core person with that place. `subplaces` are optional light-blue labels inside the same ellipse. Do not model places as normal icon nodes in this default style.

`related_people` records semantic membership. `territory_people` controls which people the blue ellipse must physically contain. `arrow_people` controls which core person receives the blue person-place arrow. This separation prevents every related actor from stretching the ellipse or creating too many arrows.

Use blue territories for Level 1 and Level 2 core people only. For non-core actors, use `related_people` plus nearby avatar placement, subplace labels, or supplemental relations, but set `"draw_territory": false` or omit the place from `places`.

If `territory_people` is omitted, the renderer may fall back to `related_people`. If `arrow_people` is omitted, no blue arrow is inferred unless the place has `"core_touchpoint": true`. Set `"show_arrow": false` to explicitly suppress an inferred arrow.

Use `person_overlap`, `max_width_factor`, `max_height_factor`, and `alpha` only when a territory needs manual correction. The default territory should be a local translucent petal, not a giant field that merges with all other places.

## Nodes

```json
{
  "id": "resident",
  "label": "Residents",
  "group": "community",
  "type": "primary",
  "icon": "person",
  "asset": "assets/icons/resident.png",
  "visual": "avatar-label",
  "role": "Primary affected users",
  "influence": "medium",
  "dependency": "high",
  "x": 0.5,
  "y": 0.52
}
```

Coordinates are normalized from `0` to `1`. Omit `x` and `y` for automatic circular layout.

Recommended `type` values:

- `project`: central project, service, intervention, or designed system.
- `primary`: primary users or directly served stakeholders.
- `secondary`: indirect users, caregivers, neighbors, support roles.
- `operator`: staff, maintainers, service providers.
- `institution`: government, schools, hospitals, regulators, funders.
- `partner`: NGOs, vendors, community groups, data/platform partners.
- `external`: social, economic, cultural, environmental, or technological forces.

Recommended `influence` and `dependency` values: `low`, `medium`, `high`.

`icon` and `asset` are optional. Use `icon` for semantic icon keys when the renderer has built-in icons. Use `asset` for generated or curated bitmap/SVG assets. If `asset` is present, render it large enough to be legible; primary icons should not appear as tiny decorative marks.

`visual` is optional and can override the map-level `style.node_expression` for a single node. Use it to mix a central product illustration, small stakeholder avatars, ring dots, leader-line callouts, and tag strips without forcing every actor into the same rounded card.

## Edges

```json
{
  "from": "resident",
  "to": "service-team",
  "label": "Feedback and service requests",
  "type": "feedback",
  "strength": 0.8,
  "show_label": true,
  "certainty": "inferred"
}
```

Recommended edge `type` values:

- `service`
- `information`
- `money`
- `resource`
- `authority`
- `influence`
- `conflict`
- `dependency`
- `feedback`

`strength` should be between `0.1` and `1.0`. Use stronger lines for critical relationships. Use `certainty` values: `user-provided`, `sourced`, `inferred`, or `uncertain`.

`show_label` is optional and defaults to `false`. Set `show_label: true` only for relationships that must be legible on the PNG itself; leave most relationship details for `stakeholder-analysis.md`.

For `concentric-territory-ecosystem`, edges can use an optional `connector_style`:

- `core-person`: purple thick bidirectional arrow between core people.
- `person-place`: blue thick bidirectional arrow between a person node and a `places` item.
- `supplemental-dashed`: purple thin dashed relation with a short label.

Set `"bidirectional": true` when the connector should show arrowheads at both ends. For place endpoints, `from` or `to` may reference a `places[].id`.

When explicit `person-place` edges are omitted, the renderer may infer blue arrows from `places[].arrow_people` or from `related_people` only when `"core_touchpoint": true`. This is deterministic, not random. Disable with `"auto_person_place_edges": false` in `style` when every arrow must be hand-authored.

You may also provide a separate `supplemental_relations` array for dashed purple place/person annotations:

```json
{
  "from": "bedside",
  "to": "nurse_station",
  "label": "Care record"
}
```

Supplemental relations are routed as soft arcs around the people field in the default renderer. Use them sparingly for secondary place/person relationships; do not use them as a substitute for full relationship analysis.

## Legend

The renderer can auto-create a legend from edge types. Provide a custom legend only when the map needs special terminology.

```json
[
  { "type": "service", "label": "Service flow" },
  { "type": "authority", "label": "Authority / regulation" },
  { "type": "conflict", "label": "Conflict or friction" }
]
```

## Portfolio Drafting Guidance

- Use high-resolution output for final PNGs. The final long edge should usually be at least 3200 px; 3600-4800 px is appropriate for portfolio spreads, decks, and print-ish exports.
- Render high-resolution output natively. For Pillow/canvas renderers, scale coordinates, font sizes, line widths, icon sizes, shadows, and radii before drawing; do not render a small image and resize it into `final-map.png`.
- Do not use sharpening filters to make low-resolution diagrams look high-resolution. Use sharpening only for photo/scan cleanup or explicitly image-like assets.
- If a smaller file is needed for inspection, downsample the native high-resolution output and save it separately as `preview-map.png`; keep `final-map.png` high resolution.
- Keep final maps to 8-16 stakeholder nodes when possible.
- Group less important actors into category nodes instead of making every organization its own node.
- Use labels that are specific enough for critique, but short enough to read at portfolio scale.
- For most presets, put the designed product/service near the visual center unless the analysis calls for another focus. For `concentric-territory-ecosystem`, put the primary person or core person-to-person relationship in the central people field instead, and represent the product/service through place context, labels, and analysis.
- Choose `style.preset` by communication task rather than by industry. See `style-library.md`.
- Use edge labels sparingly. Too many edge labels make the diagram look like research notes rather than a finished system map.
- Keep node role captions out of dense maps unless they improve scanning; the text analysis should carry the detailed role descriptions.
