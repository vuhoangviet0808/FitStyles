import json
import numpy as np
import cv2
import os
from ai_engine.modules.pose_estimation.process import get_keypoints_from_openpose

STANDARD_HEIGHT = 1.7  
OUTPUT_DIR = os.path.abspath("./storage/output")

def load_keypoints(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    if len(data["people"]) == 0:
        raise ValueError(f"No people detected in {json_path}")
    keypoints_2d = np.array(data["people"][0]["pose_keypoints_2d"]).reshape(-1, 3)[:, :2]
    return keypoints_2d

def normalize_keypoints(keypoints):
    """ Dịch keypoints về tâm và chuẩn hóa tọa độ """
    center_x = np.mean([keypoints[11][0], keypoints[12][0]])  # Trung bình hông trái & phải
    center_y = np.mean([keypoints[11][1], keypoints[12][1]])
    
    keypoints[:, 0] -= center_x
    keypoints[:, 1] -= center_y
    
    return keypoints

def estimate_camera_distance(front_keypoints, back_keypoints):
    """ Ước lượng khoảng cách camera dựa trên hông """
    hip_left_front, hip_right_front = front_keypoints[11], front_keypoints[12]
    hip_left_back, hip_right_back = back_keypoints[11], back_keypoints[12]

    avg_hip_front = (hip_left_front + hip_right_front) / 2
    avg_hip_back = (hip_left_back + hip_right_back) / 2

    distance = np.abs(avg_hip_front[0] - avg_hip_back[0]) / 100  
    return max(distance, 0.3)  

def get_camera_matrices(distance):
    """ Tạo ma trận chiếu """
    focal_length = 1000
    cx, cy = 320, 240  
    camera_matrix = np.array([
        [focal_length, 0, cx],
        [0, focal_length, cy],
        [0, 0, 1]
    ], dtype=np.float32)

    R_front = np.eye(3)
    T_front = np.array([[0], [0], [0]])

    R_back = cv2.Rodrigues(np.array([0, np.pi, 0]))[0]
    T_back = np.array([[0], [0], [-distance]])

    proj_matrix_front = camera_matrix @ np.hstack((R_front, T_front))
    proj_matrix_back = camera_matrix @ np.hstack((R_back, T_back))

    return proj_matrix_front, proj_matrix_back

def triangulate_points(front_keypoints, back_keypoints, proj_matrix_front, proj_matrix_back):
    """ Triangulation 3D """
    front_keypoints = front_keypoints.T
    back_keypoints = back_keypoints.T

    points_3d_homogeneous = cv2.triangulatePoints(proj_matrix_front, proj_matrix_back, front_keypoints, back_keypoints)
    points_3d = points_3d_homogeneous[:3] / points_3d_homogeneous[3] 

    return points_3d.T  

def convert_2D_3D(image_path):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_folder = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    os.makedirs(output_folder, exist_ok=True)

    front_json, back_json = get_keypoints_from_openpose(image_path)

    front_keypoints = load_keypoints(front_json)
    back_keypoints = load_keypoints(back_json)

    # Chuẩn hóa keypoints để căn chỉnh
    front_keypoints = normalize_keypoints(front_keypoints)
    back_keypoints = normalize_keypoints(back_keypoints)

    # Ước lượng khoảng cách camera
    camera_distance = estimate_camera_distance(front_keypoints, back_keypoints)

    # Lấy ma trận chiếu
    proj_matrix_front, proj_matrix_back = get_camera_matrices(camera_distance)

    # Triangulation
    points_3d = triangulate_points(front_keypoints, back_keypoints, proj_matrix_front, proj_matrix_back)

    # Lưu kết quả
    output_data = {"keypoints_3d": points_3d.tolist()}
    output_path = os.path.join(output_folder, "output_3d.json")
    with open(output_path, "w") as f:
        json.dump(output_data, f, indent=4)

    print("✅ Keypoints 3D created successfully and saved to:", output_path)
    return output_path

if __name__ == "__main__":
    front_json = "/mnt/data/front.json"
    back_json = "/mnt/data/back.json"
    convert_2D_3D(front_json, back_json)
