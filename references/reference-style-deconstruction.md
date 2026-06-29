# Reference Style Deconstruction

Use this when the user supplies a visual reference and asks the system map to follow that style. The goal is to extract the reference's diagram grammar, not to paste surface decoration onto the default renderer.

## Required Order

1. Identify the reference's structural grammar before choosing colors or node styling.
2. Identify what the large shapes mean: territories, rings, stages, flows, influence fields, service loops, or decorative atmosphere.
3. Identify the node expression system: icon-only, avatar+label, small badge, dot on a ring, callout label, tag strip, table cell, card, or hybrid.
4. Identify the connector grammar: radial guide lines, leader lines, arc arrows, thick journey ribbons, dashed data traces, dotted association lines, or no explicit connectors.
5. Translate the user's project into that grammar. Place nodes by meaning, not by visual convenience.
6. Only then adapt palette, typography, line weight, shadows, spacing, and labels.

## Structure Grammar Types

- `concentric-territory-ecosystem`: central experience plus rings, translucent people/place/resource territories, external factors, small icon/avatar labels, and only a few critical arrows. Use as the default when centrality, field membership, overlap, and stakeholder distance communicate more than a dense edge network.
- `concentric-orbit`: central product/user with rings for closeness, priority, lifecycle stage, or stakeholder distance. Nodes sit on rings or between rings. Use few arrows.
- `venn-territory`: overlapping translucent areas encode system domains. Nodes inside overlaps belong to multiple domains. Use the overlap as the argument.
- `ecosystem-loop`: thick loop paths encode service stages or value loops. Nodes sit on or near the loop they participate in.
- `service-blueprint`: horizontal or vertical lanes encode actors, frontstage/backstage, technology, operations, and policy. Use aligned handoffs.
- `radial-segment`: wedge sectors encode categories; nodes sit inside sectors. Useful when classification matters more than relationships.
- `callout-constellation`: central system with leader lines to small icons and labels. The icon/leader-line grammar is primary; cards are minimal or absent.
- `card-network`: rounded cards linked by arrows. Use only when the reference itself uses card-like nodes.

## Node Expression Options

Do not default to rounded-rectangle cards. Choose the node form that matches the reference:

- `icon-only`: icon plus tiny label, good for dense ecosystem maps.
- `avatar-label`: person/avatar icon with label underneath or beside it, no enclosing card.
- `ring-dot`: colored dot or small badge located on a ring with a leader label.
- `callout`: icon or dot connected to a compact text label by a thin line.
- `tag-strip`: short horizontal label strip for external factors, policies, platforms, channels, or market inputs.
- `cluster-bubble`: soft filled circle containing several small nodes.
- `mini-card`: small rounded rectangle used sparingly for dense labels, not as every node.
- `feature-card`: larger card for one or two key modules when the reference clearly has object tiles.

If more than half the nodes become `mini-card` or `feature-card`, verify that the reference actually uses cards. Otherwise, switch to icon/callout/ring-dot nodes and move detail text to the Markdown analysis.

## Large Shape Semantics

Every large background shape must have a stated meaning in `style-notes.md` and, when useful, in `stakeholder-system-map.json`.

Good examples:

- A large left circle means "patient home context"; a right circle means "clinical service context"; their overlap means "shared care coordination."
- An inner ring means "direct users"; middle ring means "operators and systems"; outer ring means "governance and external constraints."
- A thick arrow loop means "awareness -> consideration -> conversion -> support."

Bad examples:

- Blue rings because the reference has blue rings.
- Random loops around white space.
- Background circles that do not correspond to stakeholder groups, stages, power, distance, or flows.

## Reference Adaptation Checklist

Before rendering, write or mentally validate:

- What does each ring, circle, loop, lane, or segment mean?
- Which nodes belong inside each area, and why?
- What does overlap mean in this project?
- Which elements are relationship connectors and which are only spatial guides?
- What node forms does the reference actually use?
- Which labels can be tiny because icons carry meaning?
- Which detailed explanations should move to `stakeholder-analysis.md` instead of crowding the PNG?

## Special Case: Concentric Icon Ecosystems

For references that use concentric circles plus icons and leader lines:

- Use a central product/service illustration.
- Use 2-4 rings with explicit labels, such as `core use`, `service support`, `business system`, `external constraints`.
- Place stakeholders as icons or avatars on the relevant ring, not in large text cards.
- Use thin gray leader lines from center or ring nodes to labels.
- Use thick arrows only for major lifecycle or conversion stages.
- Keep explanatory text terse: actor name plus 1-3 words. Put longer rationale in the text analysis.

## Special Case: Three-Ring People/Place Territory Ecosystems

For references like the patient/doctor/specialist example with three concentric fields:

- Read the rings from center outward as `People`, `Place`, and `Other factors`.
- Put the 2-3 most important people inside the central people circle. The primary beneficiary can use a filled warm circle; other key people use large white circles.
- Put secondary people inside the people field as transparent-background avatar icons plus short labels. Do not put them in cards or small circled containers.
- Use person/avatar icons only. Places, products, devices, dashboards, rooms, and institutions are written as text labels in this style unless the user explicitly requests another grammar.
- Place names sit in the middle `Place` circle as dark blue text. Position each place close to the people who use, operate, or depend on it.
- Use pale blue translucent circles/ellipses to group a person with a nearby place label and optional light-blue sub-place labels. These ellipses must encode person-place association, not decoration.
- Size pale blue ellipses from their related people and place labels. They should not accidentally cut through a core person's circular node.
- Place macro factors inside the outer gray circle as text only. They are not nodes and do not need icons.
- Use purple thick bidirectional arrows between the core people for care, coordination, trust, judgment, referral, or responsibility.
- Use blue thick bidirectional arrows between a core person and their associated place/territory.
- Use purple thin dashed lines, with short purple labels, for supplementary relations between places, people, or territories. Route these as gentle arcs around the people field unless the relationship is very short.
- Do not add extra dashed concentric guide rings unless the reference visibly contains them and their meaning is explicit.
- Express most relationships through proximity, circle membership, ellipse grouping, and overlap. Draw only a few explicit connectors.

## Anti-Patterns

- Do not force every stakeholder into a rounded card with icon+title+subtitle.
- Do not use reference colors while retaining an unrelated layout.
- Do not use large circles, rings, or loops as decoration.
- Do not add arrows merely because the system has relationships; use spatial membership when the reference is area-based.
- Do not draw blue ellipses unless they encode a shared place, channel, institution, touchpoint, or resource container.
- For the three-ring people/place style, do not draw product, room, dashboard, or device icons as default nodes; use person avatars and text place labels.
- Do not put `Other factors` outside the outer circle when the reference clearly places them inside the gray field.
- Do not turn every secondary person into a tiny circled node; the reference uses icon+label without a container for minor people.
- Do not use primitive fallback person icons in final portfolio output; use distinct generated or curated role avatars.
- Do not let generated image polish invent the reference grammar. Establish grammar deterministically first.
