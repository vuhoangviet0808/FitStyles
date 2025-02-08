import json
import numpy as np
import cv2
import os
from ai_engine.modules.pose_estimation.process import get_keypoints_from_openpose

STANDARD_HEIGHT = 1.7
IMAGE_DIR = os.path.abspath("./storage/input")
OUTPUT_DIR = os.path.abspath("./storage/output")

def load_keypoints(json_path):
    with open(json_path, 'r') as f:
        data = json.load(f)
    keypoints_2d = np.array(data["people"][0]["pose_keypoints_2d"]).reshape(-1,3)[:,:2]
    return keypoints_2d

def generate_scaled_skeleton(user_height=1.7):
    scale_factor = user_height / STANDARD_HEIGHT  
    base_skeleton = np.array([
        [0.0, 1.7, 0.0],      # 0 - Đỉnh đầu
        [0.0, 1.47, 0.0],     # 1 - Mũi (Nose)
        [0.0, 1.4, 0.0],      # 2 - Cổ (Neck)
        [-0.2, 1.3, 0.0],     # 3 - Vai trái (Shoulder Left)
        [0.2, 1.3, 0.0],      # 4 - Vai phải (Shoulder Right)
        [-0.4, 0.7, 0.0],     # 5 - Khuỷu tay trái (Elbow Left)
        [0.4, 0.7, 0.0],      # 6 - Khuỷu tay phải (Elbow Right)
        [-0.6, 0.4, 0.0],     # 7 - Cổ tay trái (Wrist Left)
        [0.6, 0.4, 0.0],      # 8 - Cổ tay phải (Wrist Right)
        [0.0, 1.0, 0.0],      # 9 - Ngực (Chest)
        [0.0, 0.9, 0.0],      # 10 - Rốn (Belly)
        [-0.175, 0.9, 0.0],   # 11 - Hông trái (Hip Left)
        [0.175, 0.9, 0.0],    # 12 - Hông phải (Hip Right)
        [-0.2, 0.4, 0.0],     # 13 - Đầu gối trái (Knee Left)
        [0.2, 0.4, 0.0],      # 14 - Đầu gối phải (Knee Right)
        [-0.2, 0.1, 0.0],     # 15 - Mắt cá chân trái (Ankle Left)
        [0.2, 0.1, 0.0],      # 16 - Mắt cá chân phải (Ankle Right)
        [-0.05, 1.65, 0.05],  # 17 - Mắt trái
        [0.05, 1.65, 0.05],   # 18 - Mắt phải
        [-0.15, 1.6, 0.1],    # 19 - Tai trái
        [0.15, 1.6, 0.1],     # 20 - Tai phải
        [-0.7, 0.2, 0.0],     # 21 - Ngón tay trái
        [0.7, 0.2, 0.0],      # 22 - Ngón tay phải
        [0.0, 0.85, 0.0],     # 23 - Hông giữa
        [-0.2, 0.55, 0.0],    # 24 - Đùi trái
        [0.2, 0.55, 0.0],     # 25 - Đùi phải
        [-0.2, 0.05, -0.05],  # 26 - Gót chân trái
        [0.2, 0.05, -0.05],   # 27 - Gót chân phải
        [-0.1, 0.0, 0.1],     # 28 - Ngón chân cái trái
        [0.1, 0.0, 0.1],      # 29 - Ngón chân cái phải
        [-0.3, 0.0, 0.0],     # 30 - Mép ngoài chân trái
        [0.3, 0.0, 0.0],      # 31 - Mép ngoài chân phải
        [-0.5, 0.55, 0.0],    # 32 - Cẳng tay trái
        [0.5, 0.55, 0.0],     # 33 - Cẳng tay phải
        [-0.2, 0.0, -0.1],    # 34 - Bàn chân trái
        [0.2, 0.0, -0.1]      # 35 - Bàn chân phải
    ], dtype=np.float32)


    scaled_skeleton = base_skeleton * scale_factor

    return scaled_skeleton


def convert_2D_3D(image_path):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_folder = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    front, back = get_keypoints_from_openpose(image_path)
    front_keypoints = load_keypoints(front)
    back_keypoints = load_keypoints(back)
    distance_between_views = 0.5

    points_2d = np.vstack((front_keypoints, back_keypoints))
    height = 1.7


    real_world_points = generate_scaled_skeleton(height)

    camera_matrix = np.array([
        [1000, 0, 320],
        [0, 1000, 240],
        [0, 0, 1]
    ], dtype=np.float32)

    dist_coeffs = np.zeros((4,1))
    success, rotation_vector, translation_vector = cv2.solvePnP(real_world_points, points_2d, camera_matrix, dist_coeffs)

    points_3d, _ = cv2.projectPoints(real_world_points, rotation_vector, translation_vector, camera_matrix, dist_coeffs)

    output_data = {"keypoints_3d":points_3d.tolist()}
    output =  os.path.join(output_folder, "output_3d.json")
    with open(output, "w") as f:
        json.dump(output_data, f, indent=4)

    print("✅ Create keypoints 3D success, save to output_3d.json")

    return output

if __name__ == "__main__":
    image_path = "../../../storage/input/person2/person2.jpg"  
    convert_2D_3D(os.path.abspath(image_path))
