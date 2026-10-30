# -*- coding: utf-8 -*-
from client import OpenClawGenParkArTryon

tryon = OpenClawGenParkArTryon()

# 1. 3D Bounding-Box IoU
iou = tryon.calculate_3d_bounding_box_iou([0, 0, 0], [1.0, 1.0, 1.0], [0.2, 0.2, 0.2], [1.2, 1.2, 1.2])
print(f"3D Bounding-Box IoU: {iou['iou_3d']} (Collision: {iou['collision_detected']}, InterVol: {iou['intersection_volume']})")

# 2. Anthropometric Fit Index
user = {"chest": 96.0, "waist": 82.0, "hip": 100.0, "shoulder": 44.0}
garment = {"chest": 102.0, "waist": 86.0, "hip": 104.0, "shoulder": 46.0}
fit = tryon.evaluate_anthropometric_fit_index(user, garment, desired_ease_cm=4.0)
print()
print(f"Sizing Fit: RMSE={fit['fit_rmse_cm']}cm ({fit['fit_classification']}, Action: {fit['recommended_action']})")

# 3. Pinhole Projection
proj = tryon.project_3d_point_to_camera_surface([0.15, 0.45, 1.8], focal_length_px=800.0)
print()
print(f"Pinhole Projection: u={proj['pixel_coordinates']['u']}, v={proj['pixel_coordinates']['v']} (Depth={proj['depth_z_meters']}m)")
