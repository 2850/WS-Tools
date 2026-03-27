"""
generate_excalidraw.py
Helper script to programmatically generate valid Excalidraw JSON
and write Obsidian-ready .excalidraw.md files.

Usage:
    Modify the build_elements() function, then run:
    python generate_excalidraw.py --output "MyDiagram.excalidraw.md"

Key advantage: avoids backtick-escaping bugs when writing code fences
inside Python string templates. Uses chr(96)*3 to produce ``` safely.
"""

import json
import argparse
import sys
from pathlib import Path


# ---------------------------------------------------------------------------
# Element factory helpers
# ---------------------------------------------------------------------------

def _seed(id_str: str) -> int:
    return abs(hash(id_str)) % 1_000_000


def make_text(
    id, x, y, w, h, text,
    fontSize=14, color="#374151", containerId=None, align="center",
    fontFamily=1
):
    """Create a standalone text element, or one bound to a container."""
    return {
        "id": id, "type": "text",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": 1, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": None, "seed": _seed(id),
        "version": 1, "versionNonce": _seed(id + "v"),
        "isDeleted": False, "boundElements": [], "updated": 1711123200000,
        "link": None, "locked": False,
        "text": text, "rawText": text,
        "fontSize": fontSize, "fontFamily": fontFamily,
        "textAlign": align, "verticalAlign": "middle",
        "containerId": containerId, "originalText": text,
        "autoResize": True, "lineHeight": 1.25,
    }


def make_rect(id, x, y, w, h, stroke="#1e40af", bg="#dbeafe", bound_text_id=None, roundness=3):
    """Create a rectangle. Optionally bind a text element via bound_text_id."""
    bounds = [{"type": "text", "id": bound_text_id}] if bound_text_id else []
    return {
        "id": id, "type": "rectangle",
        "x": x, "y": y, "width": w, "height": h,
        "angle": 0, "strokeColor": stroke, "backgroundColor": bg,
        "fillStyle": "solid", "strokeWidth": 2, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": {"type": roundness} if roundness else None,
        "seed": _seed(id), "version": 1, "versionNonce": _seed(id + "v"),
        "isDeleted": False, "boundElements": bounds, "updated": 1711123200000,
        "link": None, "locked": False,
    }


def make_line(id, x, y, dx, dy, color="#374151", strokeStyle="solid", strokeWidth=2):
    """
    Create a line element.
    IMPORTANT: Use `points` array, do NOT use x2/y2 (those fields do not exist).
    """
    return {
        "id": id, "type": "line",
        "x": x, "y": y, "width": abs(dx), "height": abs(dy),
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": strokeWidth, "strokeStyle": strokeStyle,
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": None, "seed": _seed(id), "version": 1, "versionNonce": _seed(id + "v"),
        "isDeleted": False, "boundElements": [], "updated": 1711123200000,
        "link": None, "locked": False,
        "points": [[0, 0], [dx, dy]],
        "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": None, "endArrowhead": None,
    }


def make_arrow(id, x, y, dx, dy=0, color="#374151", strokeWidth=2,
               startArrowhead=None, endArrowhead="arrow"):
    """
    Create an arrow element.
    IMPORTANT: Use `points` array, do NOT use x2/y2 (those fields do not exist).
    """
    return {
        "id": id, "type": "arrow",
        "x": x, "y": y, "width": abs(dx), "height": abs(dy),
        "angle": 0, "strokeColor": color, "backgroundColor": "transparent",
        "fillStyle": "solid", "strokeWidth": strokeWidth, "strokeStyle": "solid",
        "roughness": 1, "opacity": 100, "groupIds": [], "frameId": None,
        "roundness": None, "seed": _seed(id), "version": 1, "versionNonce": _seed(id + "v"),
        "isDeleted": False, "boundElements": [], "updated": 1711123200000,
        "link": None, "locked": False,
        "points": [[0, 0], [dx, dy]],
        "lastCommittedPoint": None,
        "startBinding": None, "endBinding": None,
        "startArrowhead": startArrowhead, "endArrowhead": endArrowhead,
    }


# ---------------------------------------------------------------------------
# File writer
# ---------------------------------------------------------------------------

def write_excalidraw_md(elements: list, output_path: str, app_state: dict = None):
    """
    Validate JSON and write an Obsidian-ready .excalidraw.md file.

    Uses chr(96)*3 to produce backtick code fences safely,
    avoiding the escaped-backtick bug that writes \\`\\`\\`json instead of ```json.
    """
    data = {
        "type": "excalidraw",
        "version": 2,
        "source": "https://github.com/zsviczian/obsidian-excalidraw-plugin",
        "elements": elements,
        "appState": app_state or {"gridSize": None, "viewBackgroundColor": "#ffffff"},
        "files": {},
    }

    # Validate JSON before writing
    json_str = json.dumps(data, ensure_ascii=False, indent=2)
    try:
        json.loads(json_str)
    except json.JSONDecodeError as e:
        print(f"ERROR: Generated JSON is invalid: {e}", file=sys.stderr)
        sys.exit(1)

    bt = chr(96) * 3  # produces ``` without escaping issues

    content = (
        "---\n"
        "excalidraw-plugin: parsed\n"
        "tags: [excalidraw]\n"
        "---\n"
        "==⚠  Switch to EXCALIDRAW VIEW in the MORE OPTIONS menu of this document. ⚠== "
        "You can decompress Drawing data with the command palette: "
        "'Decompress current Excalidraw file'. "
        "For more info check in plugin settings under 'Saving'\n\n"
        "# Excalidraw Data\n\n"
        "## Text Elements\n"
        "%%\n"
        "## Drawing\n"
        f"{bt}json\n"
        f"{json_str}\n"
        f"{bt}\n"
        "%%"
    )

    Path(output_path).write_text(content, encoding="utf-8")
    print(f"Written: {output_path}  ({len(elements)} elements, {len(content)} chars)")


# ---------------------------------------------------------------------------
# Example: sequence diagram
# ---------------------------------------------------------------------------

def build_sequence_diagram_example():
    """
    Example sequence diagram. Replace with your own element list.
    Actor positions: each actor is centered on its lifeline x-coordinate.
    """
    elements = []
    A1, A2, A3, A4 = 140, 340, 540, 740

    elements.append(make_text("title", 80, 12, 720, 32,
                               "Sequence Diagram Title", fontSize=22, color="#1e40af"))

    for aid, cx, stroke, bg, label in [
        ("a1", A1, "#f59e0b", "#fef3c7", "Actor 1"),
        ("a2", A2, "#059669", "#d1fae5", "Actor 2"),
        ("a3", A3, "#2563eb", "#dbeafe", "Actor 3"),
        ("a4", A4, "#dc2626", "#fee2e2", "Actor 4"),
    ]:
        elements.append(make_rect(aid, cx - 60, 55, 120, 50, stroke, bg, bound_text_id=aid + "t"))
        elements.append(make_text(aid + "t", cx - 60, 55, 120, 50, label,
                                   fontSize=13, color="#1c1917", containerId=aid))

    for lid, cx, color in [
        ("ll1", A1, "#f59e0b"), ("ll2", A2, "#059669"),
        ("ll3", A3, "#2563eb"), ("ll4", A4, "#dc2626"),
    ]:
        elements.append(make_line(lid, cx, 105, 0, 490, color, strokeStyle="dashed"))

    for mid, x1, x2, y, color, label in [
        ("m1", A1, A2, 150, "#f59e0b", "1. Message A to B"),
        ("m2", A2, A3, 210, "#059669", "2. Message B to C"),
        ("m3", A3, A2, 270, "#2563eb", "3. Reply C to B"),
        ("m4", A1, A4, 330, "#f59e0b", "4. Message A to D"),
    ]:
        elements.append(make_arrow(mid, x1, y, x2 - x1, color=color))
        lx = min(x1, x2) + 5
        elements.append(make_text(mid + "l", lx, y - 18, abs(x2 - x1) - 10, 18,
                                   label, fontSize=11, color=color))

    return elements


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate a valid Excalidraw .md file")
    parser.add_argument("--output", default="diagram.excalidraw.md")
    args = parser.parse_args()
    elements = build_sequence_diagram_example()
    write_excalidraw_md(elements, args.output)
