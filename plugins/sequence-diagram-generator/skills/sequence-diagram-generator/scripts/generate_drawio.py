"""
generate_drawio.py
Helper functions to produce valid draw.io mxGraph XML files.

IMPORTANT: Use string-template functions (vertex / edge_pts) — do NOT use
xml.etree or minidom. minidom inserts extra whitespace text-nodes that cause
draw.io to throw "a.push is not a function for mxGeometry".

Usage example:
    from generate_drawio import esc, vertex, edge_pts, drawio_xml
    from pathlib import Path

    cells = []
    cells.append(vertex("box1", "Hello", "rounded=1;", 100, 100, 120, 40))
    cells.append(edge_pts("e1", "label", "endArrow=block;strokeColor=#333;",
                           160, 100, 400, 100))

    Path("output.drawio").write_text(drawio_xml(cells), encoding="utf-8")
"""

from pathlib import Path


# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------

def esc(s: str) -> str:
    """Escape special XML characters for attribute values."""
    return (s.replace("&", "&amp;")
             .replace("<", "&lt;")
             .replace(">", "&gt;")
             .replace('"', "&quot;"))


def vertex(id: str, value: str, style: str,
           x: float, y: float, w: float, h: float) -> str:
    """Return an mxCell string for a vertex (box / shape)."""
    return (
        f'    <mxCell id="{id}" value="{esc(value)}" style="{style}" '
        f'vertex="1" parent="1">'
        f'<mxGeometry x="{x}" y="{y}" width="{w}" height="{h}" as="geometry" />'
        f'</mxCell>'
    )


def edge_pts(id: str, value: str, style: str,
             sx: float, sy: float,
             tx: float, ty: float,
             waypoints: list = None) -> str:
    """
    Return an mxCell string for an edge using explicit sourcePoint/targetPoint.

    Rules:
    - Do NOT add exitX/exitY/entryX/entryY to style — those require
      source/target node IDs and will break floating-point edges.
    - For self-loops, pass waypoints=[(cx+60, y), (cx+60, y+32)] to go around.
    """
    pts = ""
    if waypoints:
        inner = "".join(
            f'\n        <mxPoint x="{px}" y="{py}" />' for px, py in waypoints
        )
        pts = f'\n      <Array as="points">{inner}\n      </Array>'

    return (
        f'    <mxCell id="{id}" value="{esc(value)}" style="{style}" '
        f'edge="1" parent="1">'
        f'\n      <mxGeometry relative="1" as="geometry">'
        f'\n        <mxPoint x="{sx}" y="{sy}" as="sourcePoint" />'
        f'\n        <mxPoint x="{tx}" y="{ty}" as="targetPoint" />'
        f'{pts}'
        f'\n      </mxGeometry>'
        f'\n    </mxCell>'
    )


def drawio_xml(cells: list,
               page_width: int = 1400,
               page_height: int = 1050) -> str:
    """Wrap cell strings in a valid mxGraphModel document."""
    body = "\n".join(cells)
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        f'<mxGraphModel dx="1422" dy="762" grid="0" gridSize="10" guides="1" '
        f'tooltips="1" connect="1" arrows="1" fold="1" page="1" '
        f'pageScale="1" pageWidth="{page_width}" pageHeight="{page_height}" '
        f'math="0" shadow="0">\n'
        '  <root>\n'
        '    <mxCell id="0" />\n'
        '    <mxCell id="1" parent="0" />\n'
        f'{body}\n'
        '  </root>\n'
        '</mxGraphModel>'
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate_drawio(path: str) -> None:
    """
    Validate a .drawio file.
    Raises AssertionError if XML is malformed or any edge lacks mxGeometry.
    """
    import xml.etree.ElementTree as ET

    tree = ET.parse(path)
    cells = tree.findall(".//mxCell")
    edge_cells = [c for c in cells if c.get("edge") == "1"]

    for ec in edge_cells:
        assert ec.find("mxGeometry") is not None, (
            f"Edge '{ec.get('id')}' is missing mxGeometry"
        )

    print(f"[OK] {path}: {len(cells)} cells, {len(edge_cells)} edges — valid")


# ---------------------------------------------------------------------------
# CLI entry-point (optional self-test)
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys

    cells = []
    cells.append(vertex("a", "Actor A", "rounded=1;fillColor=#dae8fc;strokeColor=#6c8ebf;", 100, 60, 120, 40))
    cells.append(vertex("b", "Actor B", "rounded=1;fillColor=#d5e8d4;strokeColor=#82b366;", 400, 60, 120, 40))
    cells.append(edge_pts("e1", "① Hello", "endArrow=block;startArrow=none;strokeColor=#6c8ebf;strokeWidth=1.5;html=1;", 160, 80, 400, 80))
    cells.append(edge_pts("e2", "② Reply", "endArrow=block;startArrow=none;strokeColor=#82b366;strokeWidth=1.5;dashed=1;html=1;", 400, 100, 160, 100))
    # Self-loop
    cells.append(edge_pts("e3", "③ Self", "endArrow=block;startArrow=none;strokeColor=#b85450;strokeWidth=1.5;html=1;",
                           460, 130, 460, 160, waypoints=[(520, 130), (520, 160)]))

    out = "test_output.drawio"
    Path(out).write_text(drawio_xml(cells), encoding="utf-8")
    validate_drawio(out)
    print(f"Written: {out}")
