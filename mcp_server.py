# -*- coding: utf-8 -*-
"""
OpenClaw GenPark AR Tryon MCP Server
FastMCP standard interface for 3D bounding-box IoU and anthropometric sizing fit.
"""

import json
from typing import Dict, Any, List, Tuple
from client import OpenClawGenParkArTryon

try:
    from mcp.server.fastmcp import FastMCP
    mcp = FastMCP("openclaw-genpark-ar-tryon")
except ImportError:
    class MockFastMCP:
        def __init__(self, name):
            self.name = name
        def tool(self):
            def decorator(f):
                return f
            return decorator
    mcp = MockFastMCP("openclaw-genpark-ar-tryon")

tryon = OpenClawGenParkArTryon()

@mcp.tool()
def calculate_3d_bounding_box_iou(
    box_a_min: List[float],
    box_a_max: List[float],
    box_b_min: List[float],
    box_b_max: List[float]
) -> str:
    """
    Calculates exact Intersection over Union (IoU 3D) for two axis-aligned 3D bounding boxes.
    """
    res = tryon.calculate_3d_bounding_box_iou(box_a_min, box_a_max, box_b_min, box_b_max)
    return json.dumps(res, indent=2)

@mcp.tool()
def evaluate_anthropometric_fit_index(
    user_measurements_cm: Dict[str, float],
    garment_measurements_cm: Dict[str, float],
    desired_ease_cm: float = 4.0
) -> str:
    """
    Evaluates multi-point sizing fit index comparing actual ease allowance against target ease allowance.
    """
    res = tryon.evaluate_anthropometric_fit_index(user_measurements_cm, garment_measurements_cm, desired_ease_cm)
    return json.dumps(res, indent=2)

@mcp.tool()
def project_3d_point_to_camera_surface(
    point_3d: List[float],
    focal_length_px: float = 800.0
) -> str:
    """
    Projects a 3D coordinate (X, Y, Z) to 2D pixel coordinates (u, v) using pinhole camera model.
    """
    res = tryon.project_3d_point_to_camera_surface(point_3d, focal_length_px)
    return json.dumps(res, indent=2)

def main():
    print("Testing AR Tryon:")
    print(calculate_3d_bounding_box_iou([0,0,0], [1,1,1], [0.5,0.5,0.5], [1.5,1.5,1.5]))

if __name__ == "__main__":
    main()
