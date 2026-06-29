# Concentric Territory Ecosystem Default

Use this reference when no user style reference is provided and the system can be explained through people, places, external factors, proximity, and a small number of critical relationships.

## Core Grammar

The default grammar is a three-ring people-and-place ecosystem map:

- Inner circle: `People`.
- Middle circle: `Place`.
- Outer circle: `Other factors`.

This style is not a card network and not a generic product-module diagram. It uses people icons, place text, translucent place territories, and sparse arrows.

## Ring Semantics

- `People`: central stakeholder layer. Put the 2-3 most important people in large circular nodes. Put secondary people as transparent-background avatar icons plus short labels, without circle or card backgrounds.
- `Place`: service locations, channels, institutional contexts, and touchpoint settings. Render place names as dark blue text, not as object icons.
- `Other factors`: macro conditions such as language, age, economics, culture, policy, regulation, education, infrastructure, diagnosis, or environment. Place these labels inside the outer gray circle, not outside it.

The map should feel like three nested fields. Do not draw unrelated layers, decorative loops, or background bands.

## Core People Rules

- Use person/avatar icons only in this default style. Do not use product, device, scene, building, tray, dashboard, or infrastructure icons unless the user explicitly asks for a different style.
- The central beneficiary or primary user usually receives the strongest filled circle, commonly red or warm coral.
- Other key people receive large white circles.
- Secondary people receive no enclosing circle: avatar plus 1-3 word label only.
- Detailed role descriptions belong in `stakeholder-analysis.md`, not on the PNG.

For product design projects, express the product through the relationship around the user, the place context, and the text analysis. Do not make the product object the default center of this style.

## Place Territory Rules

Use pale blue translucent circles or ellipses only when they group a core person with a core place.

Each blue territory should contain:

- A dark blue place label, such as `Home`, `Ward`, `Cabin seat`, or `Bedside care`.
- One core person positioned near that place.
- Optional light blue sub-place labels, such as `waiting room`, `storage`, `crew panel`, `sink`, or `charging area`.

Blue territories are semantic grouping devices, not decoration. If an ellipse does not connect a person to a place, remove it.

Only Level 1 and Level 2 people should normally receive blue territories. Secondary people, maintainers, partners, reviewers, and supporting roles should appear as avatar labels near a relevant place, or be mentioned as sub-place/context text, without their own blue ellipse.

The ellipse should behave like a local petal around a person-place relationship, not like a full background wash. It may partially overlap a core person circle, but it should not swallow multiple unrelated nodes or merge with every other blue territory into one large blob.

For large core people, prefer intentional clean overlap over fully containing the entire person circle. Fully containing every related person often makes the blue territories too large and destroys the reference grammar.

If several places begin to merge visually, keep only the core person-place territories, lower their opacity, cap their size, or demote minor places into light-blue sub-place labels.

## Connector Rules

Draw only a few connectors:

- Purple thick bidirectional arrows: core person-to-person relationships such as care, trust, coordination, clinical judgment, referral, responsibility, or decision-making.
- Blue thick bidirectional arrows: key person-to-place relationships. These connect a core person to a nearby place label or place territory.
- Purple thin dashed lines: supplementary relationships between places, people, or place-person areas. Label them with short purple words such as `Transportation`, `Scheduling`, `Time`, `Handoff`, or `Consent`.

Connectors must land on the intended person, place label, or territory edge. Do not draw long decorative curves that pass through icons, text, or empty space.

For this reference grammar, purple supplementary dashed lines must route outside the `People` field as gentle arcs. They should not cross the red/pink people circle or pass between core people unless the reference explicitly shows that behavior.

Do not add extra dashed guide rings by default. The three main fields already communicate the structure. Add guide rings only if the chosen reference explicitly contains them and their meaning is named.

## Density Rules

- Fill the square canvas intentionally. The three key people, place territories, and labels should be large enough to read at portfolio scale.
- Do not shrink nodes because the output is high resolution.
- If content is sparse, enlarge people circles, avatar icons, place labels, and territory ellipses rather than leaving a tiny diagram in the center.
- Typography, node size, and territory size must respond to content density. Sparse maps should automatically use larger fonts and icons; dense maps should aggregate minor actors before shrinking text.
- Keep PNG labels short and let `stakeholder-analysis.md` carry nuance.

## Content Depth Rules

Before rendering, build a real system model. Do not create a minimal demo JSON directly from the first few nouns in the project description.

For each project, identify:

- Core people, secondary people, operators, decision makers, maintainers, payers, affected non-users, and responsible institutions.
- Primary places plus secondary places, touchpoints, preparation/storage/cleaning/maintenance locations, records, handoff moments, training contexts, and exception scenarios.
- External factors such as policy, safety, procurement, staffing, privacy, culture, accessibility, cost, certification, standards, and environmental constraints.
- Which person-place associations deserve blue arrows and which should be shown only through proximity or territory membership.

Only after this analysis should the renderer choose which items are visible on the PNG and which move to `stakeholder-analysis.md`.

## Asset Rules

- Generate or curate transparent-background person/avatar icons.
- Final maps must use distinct role avatars, not generic primitive fallback people. The fallback icon is only for layout tests and cannot be delivered as `final-map.png`.
- Distinct avatars should communicate role differences through clothing, posture, hair, accessories, or professional cues while staying in one cohesive illustrated style.
- If an image sheet arrives on white or off-white, remove the edge-connected background before placement.
- Do not rely on circular clipping to hide square icon backgrounds. Icons should already be transparent.

## QA Rules

- The three rings must be visible and labeled `People`, `Place`, and `Other factors` unless the user requests another language.
- Other-factor labels must sit inside the outer gray circle.
- Blue territories must group a person with a place and optional sub-places.
- Blue territories should be reserved for Level 1/2 core people; non-core actors should not create their own blue territory.
- Secondary people must not appear as tiny circled nodes.
- Every arrow must have a clear semantic role and a correct endpoint.
- The final PNG must be rendered natively at high resolution; do not upscale a preview or apply sharpening as fake clarity.
