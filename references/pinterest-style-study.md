# Pinterest Style Study

Use this when the user asks Codex to learn visual language from Pinterest or similar image references before rendering a stakeholder/system map. These notes are based on public Pinterest image results and should guide style extraction, not copying.

## Access Note

Codex can read the front Chrome tab URL, but cannot read the logged-in Pinterest page DOM unless Chrome enables `View > Developer > Allow JavaScript from Apple Events`. When direct page access is blocked, use public Pinterest image search results and cite the pins used.

## Studied Visual Patterns

### 1. Venn stakeholder territories

Representative pin: `https://www.pinterest.com/brucehanington/stakeholder-maps/`

- Large overlapping translucent circles define stakeholder territories.
- Individual actors sit inside meaningful regions rather than being connected only by arrows.
- Small white people/building icons make actor types readable before text is read.
- Best use: projects with multiple stakeholder domains that overlap, such as hospital/pharmacy/nursing/logistics/building infrastructure.

Design rule: use area membership and overlap as the primary structure; use very few arrows.

### 2. Concentric ecosystem with core/direct/indirect rings

Representative pin: `https://ca.pinterest.com/pin/ecosystem-map-design--844493672467261/`

- Central user/system is surrounded by rings such as core, direct, indirect.
- Dots vary by size and color; larger dark nodes mark high-importance actors.
- The palette is coherent: one dominant family, soft ring fills, small contrasting accents.
- Best use: early ecosystem mapping and portfolio overview pages.

Design rule: hierarchy comes from distance, size, and ring location; lines should be sparse and secondary.

### 3. Circular service ecosystem with journey clusters

Representative pin: `https://www.pinterest.com/pin/906982812452121805/`

- A large circle contains several colored clusters representing stages or activity areas.
- Small icons around clusters indicate channels, touchpoints, tools, or systems.
- Labels are embedded in bubbles; arrows are almost absent.
- Best use: service systems where activities and touchpoints matter more than point-to-point dependencies.

Design rule: organize by stage/activity cluster, then place stakeholders and touchpoints inside each cluster.

### 4. Service blueprint / swimlane system

Representative pin: `https://www.pinterest.com/pin/814377545099890286/`

- Horizontal lanes separate evidence, customer actions, onstage actions, technology, backstage actions, and support processes.
- Arrows are mostly vertical handoffs between lanes, reducing visual chaos.
- Small blocks keep text aligned and scannable.
- Best use: operational services, delivery workflows, institutional processes.

Design rule: use lanes and stage columns before using network arrows.

### 5. Icon-centered relationship map

Representative pin: `https://www.pinterest.com/pin/334321972309475430/`

- Actor nodes use simple people, group, building, and institution icons.
- Pale circular zones create a soft system boundary.
- Dotted lines are lightweight, so icons and spatial grouping stay dominant.
- Best use: portfolio-friendly stakeholder maps where actor identity should be understood quickly.

Design rule: every stakeholder node should include a role icon; relationship lines should be light and curved/dotted.

### 6. Stakeholder onion diagram with avatars

Representative pin: `https://www.pinterest.com/pin/stakeholder-onion-diagram--863002347317503695/`

- Rings encode closeness to the product.
- Human avatars make stakeholder types feel concrete.
- A few dashed arrows show selected dependencies without turning the map into a network tangle.
- Best use: prioritizing direct users, support roles, organizational roles, regulators, and external beneficiaries.

Design rule: combine concentric priority with actor illustrations; use selected lines only.

### 7. Radial category wheel

Representative pin: `https://www.pinterest.com/pin/stakeholder-maps-the-design-thinking-salon--668573507174148629/`

- Large radial segments encode categories such as internal, external, regulatory, capabilities.
- Stakeholders are placed inside segments instead of free-floating.
- The map reads from macro zones first, details second.
- Best use: stakeholder classification and portfolio explanation.

Design rule: categories should become visible spaces, not just legend colors.

### 8. Value network / dark infographic style

Representative pin: `https://www.pinterest.com/pin/que-es-y-como-hacer-un-value-network-mapping-mapa-de-red-de-valor--331085010111123365/`

- Dark background, white icons, thin curved links, and red accent create a strong poster style.
- Nodes are icon containers rather than text boxes.
- Best use: value network maps when the output should feel more graphic/editorial.

Design rule: if using dark editorial style, keep node text very short and let icons carry meaning.

### 9. Minimal concentric value focus

Representative pin: `https://fr.pinterest.com/pin/concentric-circles-of-stakeholders-in-design-value-targeting--108438303514007828/`

- Almost no arrows, just nested arcs and labels.
- The diagram is about focus and distance, not detailed relationships.
- Best use: explaining design value audiences or stakeholder priority at a high level.

Design rule: sometimes the best system map has no arrows; use distance and labels to encode priority.

## Renderer Implications

The current renderer is too network-centric. To make portfolio-grade maps, add:

- `node.icon`: semantic icon keys such as `person`, `group`, `nurse`, `courier`, `pharmacy`, `vehicle`, `database`, `building`, `elevator`, `maintenance`, `policy`.
- `node.visual`: avatar, icon badge, device illustration, organization badge.
- `layout.mode`: `venn-territory`, `concentric-rings`, `service-blueprint`, `cluster-ecosystem`, `radial-segments`, `value-network-poster`.
- `zones`: named translucent areas or rings that carry meaning beyond color legend.
- `edge.visibility`: `primary`, `secondary`, `hidden` so dense relations can move to text analysis.
- `edge.route`: curved/orthogonal/arc options and collision avoidance.
- A constrained palette system: background, primary, secondary, accent, neutral, danger only.
- Text layout constraints: separate icon and text zones inside each node, use 1.25-1.45 line-height for multi-line labels, avoid labels on top of rings or arrows, and hide relationship labels when they compete with actor labels.
- Icon quality constraints: use a coherent icon/avatar family for final output. Hand-drawn primitive icons are acceptable only as a draft renderer fallback.
- Icon scale constraints: primary icons must be large enough to read as illustrations, not tiny decorations. If icons become small and crowded, reduce node count, enlarge cards, use a larger canvas, or move secondary actors into a legend/list.

## Practical Rule For Next Hospital Map

Do not redraw the hospital project as text boxes plus arrows. Use an icon-centered concentric or Venn-territory map:

- Center: smart delivery vehicle as a device/vehicle illustration.
- Inner ring: courier, nurse, pharmacy staff with human role icons.
- Middle ring: logistics, identity record, medication tray/data system with system icons.
- Outer ring: elevator, stairs/ward space, maintenance, hospital governance with infrastructure icons.
- Use one teal/blue primary palette with coral for clinical handoff and amber for digital authorization.
- Keep only 3-5 visible relationship lines; use proximity, rings, and icons for the rest.
