#!/usr/bin/env python3
"""Render a stakeholder system map JSON file to a PNG image."""

from __future__ import annotations

import json
import math
import sys
from pathlib import Path
from textwrap import wrap

try:
    from PIL import Image, ImageDraw, ImageFont
except ModuleNotFoundError as exc:
    if exc.name != "PIL":
        raise
    print(
        "Missing dependency: Pillow. Install it with "
        "`python3 -m pip install -r scripts/requirements.txt`, or run this script "
        "with a Python environment that already includes Pillow.",
        file=sys.stderr,
    )
    raise SystemExit(1) from exc


EDGE_STYLES = {
    "service": {"color": "#2F80ED", "dash": None},
    "information": {"color": "#12A594", "dash": (18, 12)},
    "money": {"color": "#B7791F", "dash": None},
    "resource": {"color": "#5B8E7D", "dash": None},
    "authority": {"color": "#6D597A", "dash": None},
    "influence": {"color": "#7C3AED", "dash": (8, 10)},
    "conflict": {"color": "#C1666B", "dash": (24, 10)},
    "dependency": {"color": "#475467", "dash": (10, 8)},
    "feedback": {"color": "#E3B23C", "dash": (6, 8)},
}

STYLE_PRESETS = {
    "concentric-territory-ecosystem": {
        "background": "#F8F7F2",
        "title_color": "#202A36",
        "text_color": "#263238",
        "muted_text": "#667085",
        "node_radius": 58,
        "line_width": 4,
        "show_node_roles": False,
        "node_shape": "avatar-label",
        "structure_grammar": "three-ring-people-place-territory",
        "node_expression": "avatar-label",
        "palette": ["#4EB3D3", "#F2A7A0", "#8C5FA8", "#6A93C8", "#D2D5D8", "#D69C4E"],
    },
    "radial-ecosystem": {
        "background": "#F8F7F2",
        "title_color": "#202124",
        "text_color": "#263238",
        "muted_text": "#667085",
        "node_radius": 62,
        "line_width": 4,
        "show_node_roles": False,
        "node_shape": "circle",
        "palette": ["#466A8F", "#6F9A8D", "#D9A441", "#C36B6B", "#7B6D8D", "#8A9A5B"],
    },
    "service-system-flow": {
        "background": "#F7F8FA",
        "title_color": "#182230",
        "text_color": "#202939",
        "muted_text": "#667085",
        "node_radius": 50,
        "line_width": 4,
        "show_node_roles": False,
        "node_shape": "card",
        "palette": ["#2D5B88", "#4D908E", "#F2B84B", "#B56576", "#5E6472", "#83A95C"],
    },
    "value-exchange-map": {
        "background": "#FAF8F3",
        "title_color": "#1F2933",
        "text_color": "#263238",
        "muted_text": "#687076",
        "node_radius": 58,
        "line_width": 5,
        "show_node_roles": False,
        "node_shape": "circle",
        "palette": ["#2F6F73", "#A66A3F", "#547AA5", "#B24C63", "#7A6C5D", "#6A994E"],
    },
    "power-interest-map": {
        "background": "#F6F4EF",
        "title_color": "#1D2433",
        "text_color": "#263238",
        "muted_text": "#6B7280",
        "node_radius": 52,
        "line_width": 3,
        "show_node_roles": False,
        "node_shape": "tag",
        "palette": ["#3D5A80", "#8A817C", "#BC6C25", "#588157", "#9D4EDD", "#D62828"],
    },
    "layered-system-map": {
        "background": "#F7F6F1",
        "title_color": "#17202A",
        "text_color": "#25313C",
        "muted_text": "#667085",
        "node_radius": 50,
        "line_width": 4,
        "show_node_roles": False,
        "node_shape": "card",
        "palette": ["#355070", "#6D597A", "#B56576", "#E56B6F", "#6A994E", "#577590"],
    },
    "editorial-portfolio-map": {
        "background": "#FBFAF7",
        "title_color": "#191919",
        "text_color": "#272727",
        "muted_text": "#6F6F6F",
        "node_radius": 56,
        "line_width": 3,
        "show_node_roles": False,
        "node_shape": "card",
        "palette": ["#2F4858", "#86BBD8", "#F6AE2D", "#A23E48", "#5C6B73", "#6A994E"],
    },
}


def hex_to_rgb(value: str) -> tuple[int, int, int]:
    value = value.strip().lstrip("#")
    if len(value) == 3:
        value = "".join(ch * 2 for ch in value)
    return tuple(int(value[i : i + 2], 16) for i in (0, 2, 4))


def font(
    size: int,
    bold: bool = False,
    preferred_font: str | None = None,
) -> ImageFont.FreeTypeFont | ImageFont.ImageFont:
    candidates = [
        preferred_font,
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Medium.ttc",
        "/System/Library/Fonts/Hiragino Sans GB.ttc",
        "/System/Library/Fonts/Supplemental/Songti.ttc",
        "/System/Library/Fonts/Supplemental/Arial Bold.ttf" if bold else "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/Library/Fonts/Arial Bold.ttf" if bold else "/Library/Fonts/Arial.ttf",
        "/System/Library/Fonts/Helvetica.ttc",
        "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf",
    ]
    for candidate in candidates:
        if not candidate:
            continue
        try:
            return ImageFont.truetype(candidate, size=size)
        except OSError:
            continue
    return ImageFont.load_default()


def apply_style_preset(style: dict) -> dict:
    preset_name = style.get("preset")
    preset = STYLE_PRESETS.get(preset_name, {})
    merged = {**preset, **style}
    if preset_name and preset_name not in STYLE_PRESETS:
        print(f"Warning: unknown style preset `{preset_name}`; using explicit style values only.", file=sys.stderr)
    return merged


def text_size(draw: ImageDraw.ImageDraw, text: str, font_obj: ImageFont.ImageFont) -> tuple[int, int]:
    box = draw.textbbox((0, 0), text, font=font_obj)
    return box[2] - box[0], box[3] - box[1]


def wrapped_lines(text: str, chars: int) -> list[str]:
    lines: list[str] = []
    for part in text.splitlines() or [""]:
        lines.extend(wrap(part, width=chars) or [""])
    return lines


def draw_multiline_center(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    lines: list[str],
    font_obj: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    spacing: int = 7,
) -> None:
    heights = [text_size(draw, line, font_obj)[1] for line in lines]
    total = sum(heights) + spacing * max(0, len(lines) - 1)
    y = center[1] - total / 2
    for line, height in zip(lines, heights):
        width, _ = text_size(draw, line, font_obj)
        draw.text((center[0] - width / 2, y), line, font=font_obj, fill=fill)
        y += height + spacing


def draw_dashed_line(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill: tuple[int, int, int],
    width: int,
    dash: tuple[int, int] | None,
) -> None:
    if not dash:
        draw.line([start, end], fill=fill, width=width)
        return

    x1, y1 = start
    x2, y2 = end
    dx = x2 - x1
    dy = y2 - y1
    distance = math.hypot(dx, dy)
    if distance == 0:
        return
    ux, uy = dx / distance, dy / distance
    drawn = 0.0
    dash_len, gap_len = dash
    while drawn < distance:
        seg_end = min(drawn + dash_len, distance)
        p1 = (x1 + ux * drawn, y1 + uy * drawn)
        p2 = (x1 + ux * seg_end, y1 + uy * seg_end)
        draw.line([p1, p2], fill=fill, width=width)
        drawn += dash_len + gap_len


def draw_arrowhead(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill: tuple[int, int, int],
    size: int,
) -> None:
    angle = math.atan2(end[1] - start[1], end[0] - start[0])
    left = (end[0] - size * math.cos(angle - math.pi / 6), end[1] - size * math.sin(angle - math.pi / 6))
    right = (end[0] - size * math.cos(angle + math.pi / 6), end[1] - size * math.sin(angle + math.pi / 6))
    draw.polygon([end, left, right], fill=fill)


def shorten_line(
    start: tuple[float, float],
    end: tuple[float, float],
    start_pad: float,
    end_pad: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.hypot(dx, dy)
    if distance <= start_pad + end_pad:
        return start, end
    ux, uy = dx / distance, dy / distance
    return (
        (start[0] + ux * start_pad, start[1] + uy * start_pad),
        (end[0] - ux * end_pad, end[1] - uy * end_pad),
    )


def offset_points(
    start: tuple[float, float],
    end: tuple[float, float],
    offset: float,
) -> tuple[tuple[float, float], tuple[float, float]]:
    if offset == 0:
        return start, end
    dx = end[0] - start[0]
    dy = end[1] - start[1]
    distance = math.hypot(dx, dy)
    if distance == 0:
        return start, end
    nx, ny = -dy / distance, dx / distance
    return (
        (start[0] + nx * offset, start[1] + ny * offset),
        (end[0] + nx * offset, end[1] + ny * offset),
    )


def edge_offsets(edges: list[dict]) -> dict[int, float]:
    grouped: dict[tuple[str, str], list[int]] = {}
    for index, edge in enumerate(edges):
        pair = tuple(sorted([edge.get("from", ""), edge.get("to", "")]))
        grouped.setdefault(pair, []).append(index)

    offsets: dict[int, float] = {}
    for indexes in grouped.values():
        count = len(indexes)
        if count == 1:
            offsets[indexes[0]] = 0
            continue
        step = 34
        start_offset = -step * (count - 1) / 2
        for order, index in enumerate(indexes):
            offsets[index] = start_offset + step * order
    return offsets


def auto_layout(nodes: list[dict], width: int, height: int, margin: int) -> dict[str, tuple[float, float]]:
    center = (width / 2, height / 2 + 20)
    radius = min(width, height) * 0.32
    positions: dict[str, tuple[float, float]] = {}
    central = [node for node in nodes if node.get("type") == "project"]
    outer = [node for node in nodes if node not in central]
    for node in central:
        positions[node["id"]] = center
    for idx, node in enumerate(outer):
        angle = -math.pi / 2 + idx * (2 * math.pi / max(1, len(outer)))
        positions[node["id"]] = (
            max(margin, min(width - margin, center[0] + math.cos(angle) * radius)),
            max(margin, min(height - margin, center[1] + math.sin(angle) * radius)),
        )
    return positions


def resolve_positions(data: dict, width: int, height: int, margin: int) -> dict[str, tuple[float, float]]:
    nodes = data.get("nodes", [])
    positions = auto_layout(nodes, width, height, margin)
    for node in nodes:
        if "x" in node and "y" in node:
            positions[node["id"]] = (
                margin + float(node["x"]) * (width - margin * 2),
                margin + float(node["y"]) * (height - margin * 2),
            )
    return positions


def draw_label_box(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    text: str,
    font_obj: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    outline: tuple[int, int, int],
    text_fill: tuple[int, int, int],
) -> None:
    lines = wrapped_lines(text, 22)
    widths = [text_size(draw, line, font_obj)[0] for line in lines]
    heights = [text_size(draw, line, font_obj)[1] for line in lines]
    box_w = max(widths or [80]) + 28
    box_h = sum(heights) + 6 * max(0, len(lines) - 1) + 18
    x0, y0 = center[0] - box_w / 2, center[1] - box_h / 2
    x1, y1 = center[0] + box_w / 2, center[1] + box_h / 2
    draw.rounded_rectangle([x0, y0, x1, y1], radius=18, fill=fill, outline=outline, width=3)
    draw_multiline_center(draw, center, lines, font_obj, text_fill, spacing=6)


def rgba(value: str, alpha: int) -> tuple[int, int, int, int]:
    return (*hex_to_rgb(value), alpha)


def blend(bg: tuple[int, int, int], fg: tuple[int, int, int], amount: float) -> tuple[int, int, int]:
    return tuple(int(b * (1 - amount) + f * amount) for b, f in zip(bg, fg))


def default_concentric_canvas(data: dict) -> dict:
    canvas = dict(data.get("canvas", {}))
    if not canvas:
        canvas = {"width": 3200, "height": 3200, "margin": 170}
    canvas.setdefault("width", 3200)
    canvas.setdefault("height", 3200)
    canvas.setdefault("margin", 170)
    return canvas


def node_level(node: dict) -> int:
    explicit = node.get("level")
    if explicit is not None:
        return int(explicit)
    node_type = node.get("type", "secondary")
    if node_type in {"project", "primary"}:
        return 1
    if node_type in {"operator", "institution", "partner"}:
        return 2
    if node_type == "external":
        return 4
    return 3


def draw_translucent_ellipse(
    image: Image.Image,
    box: list[float],
    fill: str,
    alpha: int,
    outline: str | None = None,
    width: int = 3,
) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.ellipse(box, fill=rgba(fill, alpha), outline=rgba(outline, min(180, alpha + 70)) if outline else None, width=width)
    image.alpha_composite(overlay)


def draw_translucent_polygon(
    image: Image.Image,
    points: list[tuple[float, float]],
    fill: str,
    alpha: int,
    outline: str | None = None,
    width: int = 3,
) -> None:
    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    od = ImageDraw.Draw(overlay)
    od.polygon(points, fill=rgba(fill, alpha), outline=rgba(outline, min(180, alpha + 70)) if outline else None)
    if outline:
        od.line(points + [points[0]], fill=rgba(outline, min(180, alpha + 70)), width=width)
    image.alpha_composite(overlay)


def draw_dashed_ellipse(
    draw: ImageDraw.ImageDraw,
    box: list[float],
    fill: tuple[int, int, int],
    width: int = 3,
    dash_degrees: int = 7,
    gap_degrees: int = 7,
) -> None:
    start = 0
    while start < 360:
        draw.arc(box, start=start, end=min(360, start + dash_degrees), fill=fill, width=width)
        start += dash_degrees + gap_degrees


def draw_centered_text(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    text_value: str,
    font_obj: ImageFont.ImageFont,
    fill: tuple[int, int, int],
    chars: int,
    spacing: int = 6,
) -> None:
    draw_multiline_center(draw, center, wrapped_lines(text_value, chars), font_obj, fill, spacing=spacing)


def paste_asset(
    image: Image.Image,
    node: dict,
    center: tuple[float, float],
    size: int,
    fallback_color: tuple[int, int, int],
) -> bool:
    asset = node.get("asset")
    if not asset:
        return False
    asset_path = Path(asset)
    if not asset_path.is_absolute():
        asset_path = Path.cwd() / asset_path
    try:
        icon = Image.open(asset_path).convert("RGBA")
    except OSError:
        return False
    icon = prepare_icon_asset(icon)
    icon.thumbnail((size, size), Image.Resampling.LANCZOS)
    x = int(center[0] - icon.width / 2)
    y = int(center[1] - icon.height / 2)
    image.alpha_composite(icon, (x, y))
    return True


def color_distance(a: tuple[int, int, int], b: tuple[int, int, int]) -> float:
    return math.sqrt(sum((a[i] - b[i]) ** 2 for i in range(3)))


def transparent_edge_background(icon: Image.Image, threshold: int = 42) -> Image.Image:
    """Remove only edge-connected white/off-white backgrounds from generated icons."""
    icon = icon.convert("RGBA")
    w, h = icon.size
    if w == 0 or h == 0:
        return icon
    alpha = icon.getchannel("A")
    if alpha.getextrema()[0] < 250:
        return trim_transparent_icon(icon)

    corner_points = [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]
    corners = [icon.getpixel(point)[:3] for point in corner_points]
    bg = tuple(sum(color[i] for color in corners) // len(corners) for i in range(3))
    if min(bg) < 210:
        return trim_transparent_icon(icon)

    pixels = icon.load()
    visited = set()
    stack = []
    for x in range(w):
        stack.append((x, 0))
        stack.append((x, h - 1))
    for y in range(h):
        stack.append((0, y))
        stack.append((w - 1, y))

    while stack:
        x, y = stack.pop()
        if (x, y) in visited or x < 0 or y < 0 or x >= w or y >= h:
            continue
        visited.add((x, y))
        r, g, b, a = pixels[x, y]
        if a == 0:
            continue
        if color_distance((r, g, b), bg) > threshold or min(r, g, b) < 205:
            continue
        pixels[x, y] = (r, g, b, 0)
        stack.extend([(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)])
    return trim_transparent_icon(icon)


def trim_transparent_icon(icon: Image.Image, padding: int = 12) -> Image.Image:
    alpha = icon.getchannel("A")
    bbox = alpha.getbbox()
    if not bbox:
        return icon
    x0, y0, x1, y1 = bbox
    x0 = max(0, x0 - padding)
    y0 = max(0, y0 - padding)
    x1 = min(icon.width, x1 + padding)
    y1 = min(icon.height, y1 + padding)
    return icon.crop((x0, y0, x1, y1))


def prepare_icon_asset(icon: Image.Image) -> Image.Image:
    return transparent_edge_background(icon)


def draw_simple_icon(
    draw: ImageDraw.ImageDraw,
    center: tuple[float, float],
    size: int,
    fill: tuple[int, int, int],
    kind: str = "person",
) -> None:
    cx, cy = center
    kind = kind.lower()
    if kind in {"place", "institution", "partner"}:
        w = size * 0.58
        h = size * 0.52
        draw.rounded_rectangle([cx - w / 2, cy - h / 2, cx + w / 2, cy + h / 2], radius=size * 0.08, fill=fill)
        draw.rectangle([cx - w * 0.36, cy - h * 0.15, cx - w * 0.18, cy + h * 0.12], fill=(255, 255, 255))
        draw.rectangle([cx + w * 0.08, cy - h * 0.15, cx + w * 0.26, cy + h * 0.12], fill=(255, 255, 255))
        draw.rectangle([cx - w * 0.12, cy + h * 0.08, cx + w * 0.12, cy + h * 0.5], fill=(255, 255, 255))
        return
    if kind in {"system", "product", "project"}:
        draw.rounded_rectangle([cx - size * 0.32, cy - size * 0.28, cx + size * 0.32, cy + size * 0.28], radius=size * 0.08, fill=fill)
        draw.ellipse([cx - size * 0.18, cy - size * 0.13, cx - size * 0.08, cy - size * 0.03], fill=(255, 255, 255))
        draw.ellipse([cx + size * 0.08, cy - size * 0.13, cx + size * 0.18, cy - size * 0.03], fill=(255, 255, 255))
        draw.arc([cx - size * 0.14, cy - size * 0.08, cx + size * 0.14, cy + size * 0.16], 20, 160, fill=(255, 255, 255), width=max(2, int(size * 0.04)))
        return
    if kind in {"family", "parents", "care-team"}:
        for offset, scale in [(-0.14, 0.9), (0.16, 0.75)]:
            ox = cx + size * offset
            draw.ellipse([ox - size * 0.12 * scale, cy - size * 0.32, ox + size * 0.12 * scale, cy - size * 0.08], fill=fill)
            draw.rounded_rectangle([ox - size * 0.16 * scale, cy - size * 0.04, ox + size * 0.16 * scale, cy + size * 0.28], radius=size * 0.07, fill=fill)
        return
    if kind in {"nurse", "doctor", "dentist", "clinician"}:
        draw.ellipse([cx - size * 0.15, cy - size * 0.36, cx + size * 0.15, cy - size * 0.06], fill=fill)
        if kind == "nurse":
            draw.rounded_rectangle([cx - size * 0.2, cy - size * 0.45, cx + size * 0.2, cy - size * 0.3], radius=size * 0.04, fill=fill)
            draw.rectangle([cx - size * 0.035, cy - size * 0.43, cx + size * 0.035, cy - size * 0.32], fill=(255, 255, 255))
            draw.rectangle([cx - size * 0.09, cy - size * 0.395, cx + size * 0.09, cy - size * 0.355], fill=(255, 255, 255))
        draw.rounded_rectangle([cx - size * 0.22, cy - size * 0.01, cx + size * 0.22, cy + size * 0.36], radius=size * 0.08, fill=fill)
        if kind in {"doctor", "dentist", "clinician"}:
            draw.arc([cx - size * 0.16, cy + size * 0.03, cx + size * 0.16, cy + size * 0.32], 20, 160, fill=(255, 255, 255), width=max(2, int(size * 0.035)))
        return
    if kind in {"patient", "resident", "passenger"}:
        draw.ellipse([cx - size * 0.14, cy - size * 0.38, cx + size * 0.14, cy - size * 0.1], fill=fill)
        draw.rounded_rectangle([cx - size * 0.2, cy - size * 0.04, cx + size * 0.2, cy + size * 0.34], radius=size * 0.08, fill=fill)
        draw.line([cx - size * 0.3, cy + size * 0.38, cx + size * 0.3, cy + size * 0.38], fill=fill, width=max(2, int(size * 0.06)))
        return
    draw.ellipse([cx - size * 0.16, cy - size * 0.34, cx + size * 0.16, cy - size * 0.02], fill=fill)
    draw.rounded_rectangle([cx - size * 0.22, cy + size * 0.02, cx + size * 0.22, cy + size * 0.36], radius=size * 0.08, fill=fill)


def infer_person_icon_kind(node: dict) -> str:
    text_value = " ".join(str(node.get(key, "")) for key in ("icon", "role_key", "label", "role")).lower()
    for key in ("nurse", "dentist", "doctor", "clinician", "family", "parent", "patient", "resident", "passenger", "caregiver"):
        if key in text_value:
            if key == "parent":
                return "family"
            if key == "caregiver":
                return "person"
            return key
    return "person"


def draw_territory_node(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    node: dict,
    position: tuple[float, float],
    level: int,
    group_color: tuple[int, int, int],
    text: tuple[int, int, int],
    muted: tuple[int, int, int],
    fonts: dict[str, ImageFont.ImageFont],
) -> None:
    label = node.get("label", node.get("id", ""))
    icon_kind = node.get("icon", node.get("type", "person"))
    x, y = position
    if level == 1:
        scale = float(node.get("_render_scale", 1.0))
        radius = int(float(node.get("radius", 170)) * scale)
        fill = hex_to_rgb(node.get("fill", "#E95345"))
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill)
        icon_center = (x, y - radius * 0.18)
        if not paste_asset(image, node, icon_center, int(radius * 0.92), fill):
            draw_simple_icon(draw, icon_center, int(radius * 0.7), (255, 246, 235), icon_kind)
        draw_centered_text(draw, (x, y + radius * 0.52), label, fonts["small_bold"], (255, 255, 255), 12, spacing=5)
        return
    if level == 2:
        scale = float(node.get("_render_scale", 1.0))
        radius = int(float(node.get("radius", 132)) * scale)
        draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=(255, 255, 255), outline=blend((255, 255, 255), group_color, 0.35), width=3)
        if not paste_asset(image, node, (x, y - 28), int(radius * 0.96), group_color):
            draw_simple_icon(draw, (x, y - 22), int(radius * 0.78), group_color, icon_kind)
        draw_centered_text(draw, (x, y + radius * 0.48), label, fonts["small_bold"], group_color, 12, spacing=4)
        return
    if level == 4:
        draw_centered_text(draw, position, label, fonts["tiny"], muted, 16, spacing=3)
        return
    scale = float(node.get("_render_scale", 1.0))
    size = int(float(node.get("icon_size", 96)) * scale)
    if not paste_asset(image, node, (x, y), size, group_color):
        draw_simple_icon(draw, (x, y), int(size * 0.72), group_color, icon_kind)
    label_y = y + size * 0.55
    draw_centered_text(draw, (x, label_y), label, fonts["tiny"], text, 14, spacing=3)


def territory_node_pad(node: dict) -> float:
    level = node_level(node)
    scale = float(node.get("_render_scale", 1.0))
    if level == 1:
        return float(node.get("radius", 170)) * scale + 12
    if level == 2:
        return float(node.get("radius", 132)) * scale + 12
    if level == 3:
        return float(node.get("icon_size", 96)) * scale * 0.52 + 12
    return 36


def draw_curved_or_straight_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill: tuple[int, int, int],
    width: int,
    dash: tuple[int, int] | None = None,
) -> None:
    draw_dashed_line(draw, start, end, fill, width, dash)
    draw_arrowhead(draw, start, end, fill, max(16, width * 4))


def draw_double_arrow(
    draw: ImageDraw.ImageDraw,
    start: tuple[float, float],
    end: tuple[float, float],
    fill: tuple[int, int, int],
    width: int,
    dash: tuple[int, int] | None = None,
) -> None:
    draw_dashed_line(draw, start, end, fill, width, dash)
    size = max(18, width * 4)
    draw_arrowhead(draw, start, end, fill, size)
    draw_arrowhead(draw, end, start, fill, size)


def interpolate_quadratic(
    start: tuple[float, float],
    control: tuple[float, float],
    end: tuple[float, float],
    steps: int = 80,
) -> list[tuple[float, float]]:
    points: list[tuple[float, float]] = []
    for idx in range(steps + 1):
        t = idx / steps
        x = (1 - t) ** 2 * start[0] + 2 * (1 - t) * t * control[0] + t**2 * end[0]
        y = (1 - t) ** 2 * start[1] + 2 * (1 - t) * t * control[1] + t**2 * end[1]
        points.append((x, y))
    return points


def draw_dashed_polyline(
    draw: ImageDraw.ImageDraw,
    points: list[tuple[float, float]],
    fill: tuple[int, int, int],
    width: int,
    dash: tuple[int, int],
) -> None:
    if len(points) < 2:
        return
    dash_len, gap_len = dash
    draw_remaining = dash_len
    gap_remaining = 0
    drawing = True
    for start, end in zip(points, points[1:]):
        x1, y1 = start
        x2, y2 = end
        dx = x2 - x1
        dy = y2 - y1
        distance = math.hypot(dx, dy)
        if distance == 0:
            continue
        ux, uy = dx / distance, dy / distance
        walked = 0.0
        while walked < distance:
            remaining = distance - walked
            step = min(remaining, draw_remaining if drawing else gap_remaining)
            p1 = (x1 + ux * walked, y1 + uy * walked)
            p2 = (x1 + ux * (walked + step), y1 + uy * (walked + step))
            if drawing:
                draw.line([p1, p2], fill=fill, width=width)
                draw_remaining -= step
                if draw_remaining <= 0:
                    drawing = False
                    gap_remaining = gap_len
            else:
                gap_remaining -= step
                if gap_remaining <= 0:
                    drawing = True
                    draw_remaining = dash_len
            walked += step


def curved_relation_points(
    start: tuple[float, float],
    end: tuple[float, float],
    center: tuple[float, float],
    outward: float,
) -> list[tuple[float, float]]:
    mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
    vx, vy = mid[0] - center[0], mid[1] - center[1]
    length = math.hypot(vx, vy)
    if length < 1:
        dx, dy = end[0] - start[0], end[1] - start[1]
        length = math.hypot(dx, dy) or 1
        vx, vy = -dy / length, dx / length
    else:
        vx, vy = vx / length, vy / length
    control = (mid[0] + vx * outward, mid[1] + vy * outward)
    return interpolate_quadratic(start, control, end, steps=100)


def normalize_angle_delta(delta: float) -> float:
    while delta > math.pi:
        delta -= math.tau
    while delta < -math.pi:
        delta += math.tau
    return delta


def safe_outer_arc_points(
    start: tuple[float, float],
    end: tuple[float, float],
    center: tuple[float, float],
    safe_radius: float,
    steps: int = 96,
) -> list[tuple[float, float]]:
    """Route a supplementary relation around, not through, the central people field."""
    cx, cy = center

    def polar(point: tuple[float, float]) -> tuple[float, float]:
        dx, dy = point[0] - cx, point[1] - cy
        return math.atan2(dy, dx), math.hypot(dx, dy)

    start_angle, start_dist = polar(start)
    end_angle, end_dist = polar(end)
    start_anchor = (cx + math.cos(start_angle) * safe_radius, cy + math.sin(start_angle) * safe_radius)
    end_anchor = (cx + math.cos(end_angle) * safe_radius, cy + math.sin(end_angle) * safe_radius)
    delta = normalize_angle_delta(end_angle - start_angle)
    if abs(delta) < math.radians(18):
        delta = math.copysign(math.radians(18), delta or 1)

    points: list[tuple[float, float]] = []
    if start_dist > safe_radius:
        points.append(start)
    points.append(start_anchor)
    for idx in range(1, steps):
        theta = start_angle + delta * (idx / steps)
        points.append((cx + math.cos(theta) * safe_radius, cy + math.sin(theta) * safe_radius))
    points.append(end_anchor)
    if end_dist > safe_radius:
        points.append(end)
    return points


def concentric_edge_style(edge_type: str) -> dict:
    if edge_type in {"service", "resource", "money"}:
        return {"color": "#4FB5D7", "dash": None}
    if edge_type in {"information", "feedback"}:
        return {"color": "#5278B6", "dash": (20, 14)}
    if edge_type in {"authority", "influence", "dependency"}:
        return {"color": "#8A4CA0", "dash": None}
    if edge_type == "conflict":
        return {"color": "#D95D50", "dash": (22, 12)}
    return {"color": "#8A4CA0", "dash": None}


def concentric_connector_style(edge: dict) -> dict:
    connector = edge.get("connector_style")
    if connector == "person-place":
        return {"color": "#4FB5D7", "dash": None, "width": 12, "bidirectional": True}
    if connector == "supplemental-dashed":
        return {"color": "#8A4CA0", "dash": (22, 14), "width": 4, "bidirectional": False}
    if connector == "core-person":
        return {"color": "#8A4CA0", "dash": None, "width": 12, "bidirectional": True}
    style = concentric_edge_style(edge.get("type", "influence"))
    if edge.get("type") in {"service", "resource"}:
        return {**style, "width": 10, "bidirectional": bool(edge.get("bidirectional", True))}
    if edge.get("type") in {"information", "feedback"}:
        return {**style, "width": 5, "bidirectional": bool(edge.get("bidirectional", False))}
    return {**style, "width": 10, "bidirectional": bool(edge.get("bidirectional", True))}


def resolved_item_position(item: dict, width: int, height: int, margin: int) -> tuple[float, float]:
    return (
        margin + float(item.get("x", 0.5)) * (width - margin * 2),
        margin + float(item.get("y", 0.5)) * (height - margin * 2),
    )


def place_dimensions(place: dict, width: int, height: int, margin: int) -> tuple[float, float]:
    return (
        float(place.get("width", 0.22)) * (width - margin * 2),
        float(place.get("height", 0.24)) * (height - margin * 2),
    )


def expanded_place_box(
    place: dict,
    center: tuple[float, float],
    size: tuple[float, float],
    positions: dict[str, tuple[float, float]],
    nodes: dict[str, dict],
) -> list[float]:
    px, py = center
    pw, ph = size
    x0, y0, x1, y1 = px - pw / 2, py - ph / 2, px + pw / 2, py + ph / 2
    related_people = place.get("territory_people") or place.get("related_people") or place.get("related_nodes") or []
    for node_id in related_people:
        if node_id not in positions or node_id not in nodes:
            continue
        nx, ny = positions[node_id]
        pad = territory_node_pad(nodes[node_id]) * float(place.get("person_overlap", 0.55)) + float(place.get("person_padding", 70))
        x0 = min(x0, nx - pad)
        y0 = min(y0, ny - pad)
        x1 = max(x1, nx + pad)
        y1 = max(y1, ny + pad)

    max_w = float(place.get("max_width_px", pw * float(place.get("max_width_factor", 1.32))))
    max_h = float(place.get("max_height_px", ph * float(place.get("max_height_factor", 1.36))))
    current_w = x1 - x0
    current_h = y1 - y0
    if current_w > max_w:
        mid_x = (x0 + x1) / 2
        x0, x1 = mid_x - max_w / 2, mid_x + max_w / 2
    if current_h > max_h:
        mid_y = (y0 + y1) / 2
        y0, y1 = mid_y - max_h / 2, mid_y + max_h / 2
    return [x0, y0, x1, y1]


def draw_place_territory(
    image: Image.Image,
    draw: ImageDraw.ImageDraw,
    place: dict,
    center: tuple[float, float],
    size: tuple[float, float],
    box: list[float],
    fonts: dict[str, ImageFont.ImageFont],
) -> None:
    px, py = center
    pw, ph = size
    draw_translucent_ellipse(image, box, "#86D9EF", int(place.get("alpha", 58)), "#67C8E0", width=3)
    label_pos = (
        px + float(place.get("label_dx", 0)) * pw,
        py + float(place.get("label_dy", -0.28)) * ph,
    )
    draw_centered_text(draw, label_pos, place.get("label", place.get("id", "")), fonts["small_bold"], hex_to_rgb("#245C88"), 16, spacing=4)
    subplaces = place.get("subplaces") or place.get("sub_scenes") or []
    if not subplaces:
        return
    sub_color = hex_to_rgb("#6AAEC4")
    radius_x = pw * 0.27
    radius_y = ph * 0.22
    for idx, sub in enumerate(subplaces[:6]):
        angle = -math.pi * 0.15 + idx * (math.pi * 1.3 / max(1, min(len(subplaces), 6) - 1))
        sx = px + math.cos(angle) * radius_x
        sy = py + math.sin(angle) * radius_y + ph * 0.08
        draw_centered_text(draw, (sx, sy), str(sub), fonts["tiny"], sub_color, 13, spacing=2)


def concentric_density_scale(data: dict, style: dict) -> float:
    if "density_scale" in style:
        return float(style["density_scale"])
    visible_nodes = [node for node in data.get("nodes", []) if node.get("type") != "external"]
    places = data.get("places") or [zone for zone in data.get("zones", []) if zone.get("kind") == "blue-territory"]
    factors = data.get("external_factors") or []
    content_units = len(visible_nodes) + len(places) + min(len(factors), 14) * 0.25
    if content_units <= 10:
        return 1.58
    if content_units <= 16:
        return 1.42
    if content_units <= 24:
        return 1.25
    if content_units <= 32:
        return 1.1
    return 1.0


def auto_person_place_edges(
    places: list[dict],
    nodes: dict[str, dict],
    existing_edges: list[dict],
) -> list[dict]:
    existing_pairs = {
        tuple(sorted([edge.get("from", ""), edge.get("to", "")]))
        for edge in existing_edges
        if edge.get("connector_style") == "person-place"
    }
    generated: list[dict] = []
    for place in places:
        place_id = place.get("id", place.get("label", ""))
        related = place.get("related_people") or place.get("related_nodes") or []
        core_related = [
            node_id
            for node_id in related
            if node_id in nodes and node_level(nodes[node_id]) in {1, 2}
        ]
        if place.get("show_arrow") is False:
            continue
        if "arrow_people" in place:
            arrow_people = place.get("arrow_people") or []
        elif place.get("core_touchpoint", False):
            arrow_people = core_related[:1]
        else:
            arrow_people = []
        for node_id in arrow_people[:1]:
            if node_id not in core_related:
                continue
            pair = tuple(sorted([node_id, place_id]))
            if pair in existing_pairs:
                continue
            existing_pairs.add(pair)
            generated.append(
                {
                    "from": node_id,
                    "to": place_id,
                    "connector_style": "person-place",
                    "strength": 0.72,
                    "certainty": "inferred-from-place-membership",
                    "auto_generated": True,
                }
            )
    return generated


def render_concentric_territory(data: dict, output_path: Path) -> None:
    canvas = default_concentric_canvas(data)
    style = apply_style_preset(data.get("style", {}))
    width = int(canvas.get("width", 3200))
    height = int(canvas.get("height", 3200))
    margin = int(canvas.get("margin", 170))
    bg = hex_to_rgb(style.get("background", "#F8F7F2"))
    text = hex_to_rgb(style.get("text_color", "#263238"))
    title_color = hex_to_rgb(style.get("title_color", "#202A36"))
    muted = hex_to_rgb(style.get("muted_text", "#667085"))
    preferred_font = style.get("font")
    density_scale = concentric_density_scale(data, style)

    def scaled_font_size(value: int) -> int:
        return max(14, int(value * density_scale))

    image = Image.new("RGBA", (width, height), (*bg, 255))
    draw = ImageDraw.Draw(image)

    fonts = {
        "title": font(max(46, width // 52), bold=True, preferred_font=preferred_font),
        "subtitle": font(max(24, width // 105), preferred_font=preferred_font),
        "field": font(scaled_font_size(max(42, width // 66)), bold=True, preferred_font=preferred_font),
        "label": font(scaled_font_size(max(30, width // 88)), bold=True, preferred_font=preferred_font),
        "small_bold": font(scaled_font_size(max(27, width // 100)), bold=True, preferred_font=preferred_font),
        "small": font(scaled_font_size(max(25, width // 112)), preferred_font=preferred_font),
        "tiny": font(scaled_font_size(max(23, width // 120)), preferred_font=preferred_font),
    }

    title = data.get("title", "Stakeholder System Map")
    subtitle = data.get("subtitle", "")
    draw.text((margin, 58), title, font=fonts["title"], fill=title_color)
    if subtitle:
        draw.text((margin, 122), subtitle, font=fonts["subtitle"], fill=muted)

    cx = width / 2
    cy = height / 2 + height * 0.055
    base_radius = min(width, height) * 0.43
    place_radius = base_radius * 0.78
    people_radius = base_radius * 0.48

    draw_translucent_ellipse(
        image,
        [cx - base_radius, cy - base_radius, cx + base_radius, cy + base_radius],
        "#D9DBDD",
        90,
    )
    draw_translucent_ellipse(
        image,
        [cx - place_radius, cy - place_radius, cx + place_radius, cy + place_radius],
        "#DDF3F7",
        120,
    )
    draw_translucent_ellipse(
        image,
        [cx - people_radius, cy - people_radius, cx + people_radius, cy + people_radius],
        "#F6B2AE",
        100,
        "#EBA19F",
        width=3,
    )
    if style.get("show_guide_rings", False):
        ring_color = hex_to_rgb("#AA879F")
        draw_dashed_ellipse(draw, [cx - people_radius * 1.08, cy - people_radius * 1.08, cx + people_radius * 1.08, cy + people_radius * 1.08], ring_color, width=2)
        draw_dashed_ellipse(draw, [cx - place_radius * 0.76, cy - place_radius * 0.76, cx + place_radius * 0.76, cy + place_radius * 0.76], ring_color, width=2)

    draw_centered_text(draw, (cx, cy - base_radius + 78), style.get("outer_label", "Other factors"), fonts["field"], (173, 176, 180), 24)
    draw_centered_text(draw, (cx, cy - place_radius + 84), style.get("place_label", "Place"), fonts["field"], hex_to_rgb("#86CFE1"), 18)
    draw_centered_text(draw, (cx, cy - people_radius + 86), style.get("people_label", "People"), fonts["field"], hex_to_rgb("#CF8C8B"), 18)

    zones = data.get("zones", [])
    places = list(data.get("places", []))
    if not places:
        places = [
            {
                "id": zone.get("id", f"place-{index}"),
                "label": zone.get("label", ""),
                "x": zone.get("x", 0.5),
                "y": zone.get("y", 0.5),
                "width": zone.get("width", 0.24),
                "height": zone.get("height", 0.24),
                "subplaces": zone.get("subplaces") or zone.get("sub_scenes") or [],
            }
            for index, zone in enumerate(zones)
            if zone.get("kind") == "blue-territory"
        ]

    positions = resolve_positions(data, width, height, margin)
    nodes = {node["id"]: {**node, "_render_scale": density_scale} for node in data.get("nodes", [])}

    place_positions: dict[str, tuple[float, float]] = {}
    for place in places:
        center = resolved_item_position(place, width, height, margin)
        size = place_dimensions(place, width, height, margin)
        place_positions[place.get("id", place.get("label", ""))] = (
            center[0] + float(place.get("label_dx", 0)) * size[0],
            center[1] + float(place.get("label_dy", -0.28)) * size[1],
        )
        if place.get("draw_territory", True):
            box = expanded_place_box(place, center, size, positions, nodes)
            draw_place_territory(image, draw, place, center, size, box, fonts)
        else:
            draw_centered_text(
                draw,
                place_positions[place.get("id", place.get("label", ""))],
                place.get("label", place.get("id", "")),
                fonts["small_bold"],
                hex_to_rgb("#245C88"),
                16,
                spacing=4,
            )

    factors = data.get("external_factors") or style.get("external_factors") or []
    if not factors:
        factors = [node.get("label", node.get("id", "")) for node in data.get("nodes", []) if node.get("type") == "external"]
    if factors:
        factor_radius = base_radius * 0.9
        start_angle = -150
        span = 300
        for idx, factor_label in enumerate(factors[:18]):
            angle = math.radians(start_angle + span * (idx / max(1, len(factors[:18]) - 1)))
            x = cx + math.cos(angle) * factor_radius
            y = cy + math.sin(angle) * factor_radius
            draw_centered_text(draw, (x, y), str(factor_label), fonts["tiny"], muted, 16, spacing=3)

    groups = {group["id"]: dict(group) for group in data.get("groups", [])}
    palette = style.get("palette", ["#4EB3D3", "#F2A7A0", "#8C5FA8", "#6A93C8", "#D2D5D8", "#D69C4E"])
    for idx, group in enumerate(groups.values()):
        group.setdefault("color", palette[idx % len(palette)])

    positions.update(place_positions)
    all_edges = list(data.get("edges", []))
    if style.get("auto_person_place_edges", True):
        all_edges.extend(auto_person_place_edges(places, nodes, all_edges))

    critical_edges = [
        edge
        for edge in all_edges
        if edge.get("connector_style")
        or edge.get("show_label")
        or float(edge.get("strength", 0.6)) >= 0.72
    ]
    if len(critical_edges) < 3:
        critical_edges = all_edges[:6]
    critical_edges = critical_edges[:8]
    for edge in critical_edges:
        if edge.get("from") not in positions or edge.get("to") not in positions:
            continue
        start_raw = positions[edge["from"]]
        end_raw = positions[edge["to"]]
        start_pad = territory_node_pad(nodes[edge["from"]]) if edge.get("from") in nodes else 30
        end_pad = territory_node_pad(nodes[edge["to"]]) if edge.get("to") in nodes else 30
        start, end = shorten_line(start_raw, end_raw, start_pad, end_pad)
        edge_style = concentric_connector_style(edge)
        color = hex_to_rgb(edge_style["color"])
        strength = max(0.1, min(1.0, float(edge.get("strength", 0.75))))
        width_px = max(edge_style["width"], int(edge_style["width"] * strength))
        if edge.get("connector_style") == "supplemental-dashed":
            points = safe_outer_arc_points(start, end, (cx, cy), safe_radius=people_radius * 1.14)
            draw_dashed_polyline(draw, points, color, width_px, edge_style["dash"] or (22, 14))
        elif edge_style.get("bidirectional"):
            draw_double_arrow(draw, start, end, color, width_px, edge_style["dash"])
        else:
            draw_dashed_line(draw, start, end, color, width_px, edge_style["dash"])
        if edge.get("label") and edge.get("show_label"):
            mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            draw_centered_text(draw, (mid[0], mid[1] - 20), edge["label"], fonts["tiny"], color, 18, spacing=3)

    for relation in data.get("supplemental_relations", []):
        if relation.get("from") not in positions or relation.get("to") not in positions:
            continue
        start_raw = positions[relation["from"]]
        end_raw = positions[relation["to"]]
        start_pad = territory_node_pad(nodes[relation["from"]]) if relation.get("from") in nodes else 30
        end_pad = territory_node_pad(nodes[relation["to"]]) if relation.get("to") in nodes else 30
        start, end = shorten_line(start_raw, end_raw, start_pad, end_pad)
        purple = hex_to_rgb("#8A4CA0")
        points = safe_outer_arc_points(start, end, (cx, cy), safe_radius=people_radius * 1.16)
        draw_dashed_polyline(draw, points, purple, 4, (22, 14))
        if relation.get("label"):
            mid = points[len(points) // 2]
            draw_centered_text(draw, (mid[0], mid[1] - 24), relation["label"], fonts["tiny"], purple, 16, spacing=3)

    for node_id, node in nodes.items():
        if node.get("type") == "external":
            continue
        position = positions[node_id]
        group = groups.get(node.get("group", ""), {})
        group_color = hex_to_rgb(group.get("color", "#4EB3D3"))
        node_to_draw = dict(node)
        if not style.get("allow_non_person_icons", False):
            node_to_draw["icon"] = infer_person_icon_kind(node_to_draw)
        draw_territory_node(image, draw, node_to_draw, position, node_level(node_to_draw), group_color, text, muted, fonts)

    legend_items = data.get("legend") or [
        {"connector_style": "core-person", "label": "core people relationship"},
        {"connector_style": "person-place", "label": "person-place association"},
        {"connector_style": "supplemental-dashed", "label": "supplementary relation"},
    ]
    legend_x = width - margin - 560
    legend_y = height - margin - 180
    for idx, item in enumerate(legend_items[:4]):
        y = legend_y + idx * 46
        style_item = concentric_connector_style(item)
        color = hex_to_rgb(style_item["color"])
        if style_item.get("bidirectional"):
            draw_double_arrow(draw, (legend_x, y), (legend_x + 95, y), color, 5, style_item["dash"])
        else:
            draw_dashed_line(draw, (legend_x, y), (legend_x + 95, y), color, 5, style_item["dash"])
        draw.text((legend_x + 122, y - 16), item.get("label", item.get("type", "")), font=fonts["tiny"], fill=muted)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.convert("RGB").save(output_path)


def render(data: dict, output_path: Path) -> None:
    canvas = data.get("canvas", {})
    style = apply_style_preset(data.get("style", {}))
    if style.get("preset") == "concentric-territory-ecosystem":
        render_concentric_territory(data, output_path)
        return
    width = int(canvas.get("width", 2400))
    height = int(canvas.get("height", 1600))
    margin = int(canvas.get("margin", 120))
    bg = hex_to_rgb(style.get("background", "#F8F7F2"))
    text = hex_to_rgb(style.get("text_color", "#263238"))
    title_color = hex_to_rgb(style.get("title_color", "#1F2933"))
    muted = hex_to_rgb(style.get("muted_text", "#667085"))
    node_radius = int(style.get("node_radius", 58))
    base_line = int(style.get("line_width", 4))
    show_node_roles = bool(style.get("show_node_roles", False))
    preferred_font = style.get("font")
    node_shape = style.get("node_shape", "circle")

    image = Image.new("RGB", (width, height), bg)
    draw = ImageDraw.Draw(image)

    title_font = font(54, bold=True, preferred_font=preferred_font)
    subtitle_font = font(27, preferred_font=preferred_font)
    label_font = font(24, bold=True, preferred_font=preferred_font)
    small_font = font(20, preferred_font=preferred_font)
    tiny_font = font(18, preferred_font=preferred_font)

    title = data.get("title", "Stakeholder System Map")
    subtitle = data.get("subtitle", "")
    draw.text((margin, 58), title, font=title_font, fill=title_color)
    if subtitle:
        draw.text((margin, 126), subtitle, font=subtitle_font, fill=muted)

    groups = {group["id"]: group for group in data.get("groups", [])}
    palette = style.get("palette", ["#3A6EA5", "#5B8E7D", "#E3B23C", "#C1666B", "#6D597A"])
    for idx, group in enumerate(groups.values()):
        group.setdefault("color", palette[idx % len(palette)])

    positions = resolve_positions(data, width, height, margin)
    nodes = {node["id"]: node for node in data.get("nodes", [])}

    edges = data.get("edges", [])
    offsets = edge_offsets(edges)
    for edge_index, edge in enumerate(edges):
        if edge.get("from") not in positions or edge.get("to") not in positions:
            continue
        start_raw = positions[edge["from"]]
        end_raw = positions[edge["to"]]
        start, end = shorten_line(start_raw, end_raw, node_radius + 8, node_radius + 12)
        start, end = offset_points(start, end, offsets.get(edge_index, 0))
        edge_type = edge.get("type", "influence")
        edge_style = EDGE_STYLES.get(edge_type, EDGE_STYLES["influence"])
        color = hex_to_rgb(edge_style["color"])
        strength = max(0.1, min(1.0, float(edge.get("strength", 0.6))))
        width_px = max(2, int(base_line * (0.7 + strength)))
        draw_dashed_line(draw, start, end, color, width_px, edge_style["dash"])
        draw_arrowhead(draw, start, end, color, max(14, width_px * 5))
        show_edge_label = bool(edge.get("show_label", False))
        if edge.get("label") and show_edge_label:
            mid = ((start[0] + end[0]) / 2, (start[1] + end[1]) / 2)
            draw_label_box(draw, mid, edge["label"], tiny_font, bg, color, text)

    for node_id, node in nodes.items():
        x, y = positions[node_id]
        group = groups.get(node.get("group", ""), {})
        color = hex_to_rgb(group.get("color", "#3A6EA5"))
        node_type = node.get("type", "secondary")
        radius = node_radius + (18 if node_type == "project" else 0)
        outline_width = 8 if node_type == "project" else 4
        fill = tuple(int(bg_channel * 0.72 + color_channel * 0.28) for bg_channel, color_channel in zip(bg, color))
        if node_shape in {"card", "tag"}:
            box_w = radius * (3.1 if node_shape == "card" else 2.7)
            box_h = radius * (1.62 if node_shape == "card" else 1.35)
            corner = 26 if node_shape == "card" else 18
            draw.rounded_rectangle(
                [x - box_w / 2, y - box_h / 2, x + box_w / 2, y + box_h / 2],
                radius=corner,
                fill=fill,
                outline=color,
                width=outline_width,
            )
        else:
            draw.ellipse([x - radius, y - radius, x + radius, y + radius], fill=fill, outline=color, width=outline_width)
        lines = wrapped_lines(node.get("label", node_id), 14 if node_type == "project" else 13)
        draw_multiline_center(draw, (x, y), lines, label_font if node_type == "project" else small_font, text)
        if show_node_roles and node.get("role"):
            role_lines = wrapped_lines(node["role"], 22)
            draw_multiline_center(draw, (x, y + radius + 34), role_lines[:2], tiny_font, muted, spacing=4)

    legend_items = data.get("legend") or [{"type": key, "label": key.replace("-", " ").title()} for key in used_edge_types(data)]
    legend_title = data.get("legend_title", "Relationship key")
    draw_legend(draw, legend_items, width, height, margin, small_font, tiny_font, text, muted, bg, legend_title)
    draw_group_key(draw, list(groups.values()), margin, height, small_font, text)

    output_path.parent.mkdir(parents=True, exist_ok=True)
    image.save(output_path)


def used_edge_types(data: dict) -> list[str]:
    seen = []
    for edge in data.get("edges", []):
        edge_type = edge.get("type", "influence")
        if edge_type not in seen:
            seen.append(edge_type)
    return seen


def draw_legend(
    draw: ImageDraw.ImageDraw,
    items: list[dict],
    width: int,
    height: int,
    margin: int,
    label_font: ImageFont.ImageFont,
    tiny_font: ImageFont.ImageFont,
    text: tuple[int, int, int],
    muted: tuple[int, int, int],
    bg: tuple[int, int, int],
    title: str,
) -> None:
    box_w = 520
    row_h = 42
    box_h = 82 + row_h * len(items)
    x0 = width - margin - box_w
    y0 = height - margin - box_h
    draw.rounded_rectangle([x0, y0, x0 + box_w, y0 + box_h], radius=24, fill=bg, outline=(210, 210, 205), width=2)
    draw.text((x0 + 28, y0 + 24), title, font=label_font, fill=text)
    y = y0 + 72
    for item in items:
        edge_type = item.get("type", "influence")
        edge_style = EDGE_STYLES.get(edge_type, EDGE_STYLES["influence"])
        color = hex_to_rgb(edge_style["color"])
        draw_dashed_line(draw, (x0 + 30, y + 14), (x0 + 120, y + 14), color, 5, edge_style["dash"])
        draw_arrowhead(draw, (x0 + 30, y + 14), (x0 + 120, y + 14), color, 16)
        draw.text((x0 + 142, y), item.get("label", edge_type), font=tiny_font, fill=muted)
        y += row_h


def draw_group_key(
    draw: ImageDraw.ImageDraw,
    groups: list[dict],
    margin: int,
    height: int,
    font_obj: ImageFont.ImageFont,
    text: tuple[int, int, int],
) -> None:
    x = margin
    y = height - margin - 34
    for group in groups[:7]:
        color = hex_to_rgb(group.get("color", "#3A6EA5"))
        draw.ellipse([x, y, x + 22, y + 22], fill=color)
        draw.text((x + 32, y - 3), group.get("label", group.get("id", "")), font=font_obj, fill=text)
        label_w, _ = text_size(draw, group.get("label", group.get("id", "")), font_obj)
        x += label_w + 78


def main(argv: list[str]) -> int:
    if len(argv) != 3:
        print("Usage: render_system_map.py input.json output.png", file=sys.stderr)
        return 2
    input_path = Path(argv[1])
    output_path = Path(argv[2])
    with input_path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    render(data, output_path)
    print(f"Wrote {output_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv))
