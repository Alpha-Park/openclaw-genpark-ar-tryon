# -*- coding: utf-8 -*-
"""
OpenClaw GenPark AR Tryon Client
Pure Python Standard Library (Zero External Dependencies)
Implements 3D bounding-box spatial intersection-over-union (IoU 3D),
anthropometric sizing fit index, and perspective camera pinhole projection.
"""

import math
from typing import Dict, Any, List, Optional, Tuple

class OpenClawGenParkArTryon:
    """
    Spatial geometry and anthropometric sizing engine for virtual try-on agents.
    """

    def __init__(self):
        pass

    def calculate_3d_bounding_box_iou(
        self,
        box_a_min: List[float],
        box_a_max: List[float],
        box_b_min: List[float],
        box_b_max: List[float]
    ) -> Dict[str, Any]:
        """
        Calculates exact Intersection over Union (IoU 3D) for two axis-aligned 3D bounding boxes:
          IoU = Volume(A n B) / (Volume(A) + Volume(B) - Volume(A n B))
        """
        # Volume A
        dx_a = max(0.0, box_a_max[0] - box_a_min[0])
        dy_a = max(0.0, box_a_max[1] - box_a_min[1])
        dz_a = max(0.0, box_a_max[2] - box_a_min[2])
        vol_a = dx_a * dy_a * dz_a

        # Volume B
        dx_b = max(0.0, box_b_max[0] - box_b_min[0])
        dy_b = max(0.0, box_b_max[1] - box_b_min[1])
        dz_b = max(0.0, box_b_max[2] - box_b_min[2])
        vol_b = dx_b * dy_b * dz_b

        # Intersection
        inter_min = [max(box_a_min[i], box_b_min[i]) for i in range(3)]
        inter_max = [min(box_a_max[i], box_b_max[i]) for i in range(3)]

        inter_dx = max(0.0, inter_max[0] - inter_min[0])
        inter_dy = max(0.0, inter_max[1] - inter_min[1])
        inter_dz = max(0.0, inter_max[2] - inter_min[2])
        inter_vol = inter_dx * inter_dy * inter_dz

        union_vol = vol_a + vol_b - inter_vol
        iou = round(inter_vol / union_vol, 4) if union_vol > 0 else 0.0

        return {
            "volume_box_a": round(vol_a, 4),
            "volume_box_b": round(vol_b, 4),
            "intersection_volume": round(inter_vol, 4),
            "union_volume": round(union_vol, 4),
            "iou_3d": iou,
            "collision_detected": inter_vol > 0.0
        }

    def evaluate_anthropometric_fit_index(
        self,
        user_measurements_cm: Dict[str, float],
        garment_measurements_cm: Dict[str, float],
        desired_ease_cm: float = 4.0
    ) -> Dict[str, Any]:
        """
        Evaluates multi-point sizing fit index (chest, waist, hip, shoulder) comparing
        actual ease allowance against target ease allowance.
        """
        deltas = {}
        total_sq_error = 0.0
        points_count = 0

        for dimension in ["chest", "waist", "hip", "shoulder"]:
            if dimension in user_measurements_cm and dimension in garment_measurements_cm:
                user_m = float(user_measurements_cm[dimension])
                garm_m = float(garment_measurements_cm[dimension])
                actual_ease = garm_m - user_m
                diff = actual_ease - desired_ease_cm
                
                deltas[dimension] = {
                    "user_cm": user_m,
                    "garment_cm": garm_m,
                    "actual_ease_cm": round(actual_ease, 1),
                    "ease_delta_cm": round(diff, 1)
                }
                total_sq_error += diff ** 2
                points_count += 1

        rmse = round(math.sqrt(total_sq_error / max(1, points_count)), 2)

        # Fit classification
        if rmse <= 2.0:
            classification = "PERFECT_TAILORED_FIT"
        elif rmse <= 5.0:
            classification = "COMFORTABLE_RELAXED_FIT"
        elif rmse <= 8.0:
            classification = "SLIGHTLY_LOOSE_OR_SNUG"
        else:
            classification = "INCOMPATIBLE_SIZE_MISMATCH"

        return {
            "dimension_evaluations": deltas,
            "fit_rmse_cm": rmse,
            "fit_classification": classification,
            "recommended_action": "PURCHASE" if rmse <= 5.0 else "TRY_ALTERNATIVE_SIZE"
        }

    def project_3d_point_to_camera_surface(
        self,
        point_3d: List[float],
        focal_length_px: float = 800.0,
        optical_center_xy: Tuple[float, float] = (400.0, 300.0),
        camera_translation: Tuple[float, float, float] = (0.0, 0.0, 0.0)
    ) -> Dict[str, Any]:
        """
        Projects a 3D coordinate (X, Y, Z) to 2D pixel coordinates (u, v) using pinhole camera model:
          u = fx * (X + tx) / (Z + tz) + cx
          v = fy * (Y + ty) / (Z + tz) + cy
        """
        x = point_3d[0] + camera_translation[0]
        y = point_3d[1] + camera_translation[1]
        z = point_3d[2] + camera_translation[2]

        if z <= 0.01:
            return {"visible": False, "error": "Point behind camera focal plane"}

        cx, cy = optical_center_xy
        u = round((focal_length_px * x / z) + cx, 2)
        v = round((focal_length_px * y / z) + cy, 2)

        return {
            "visible": True,
            "pixel_coordinates": {"u": u, "v": v},
            "depth_z_meters": round(z, 3),
            "normalized_scale_factor": round(focal_length_px / z, 3)
        }
