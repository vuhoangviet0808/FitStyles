import numpy as np
from ai_engine.modules.pose_estimation.Convert_2D_to_3D import get_keypoints_from_openpose, load_keypoints
import os
import json
OUTPUT_DIR = os.path.abspath("./storage/output")

def euclidean_dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def calculate_body_legnth(image_path, height):
    front, back = get_keypoints_from_openpose(image_path)
    front_keypoints = load_keypoints(front)
    back_keypoints = load_keypoints(back)

    keypoints = np.array(front_keypoints)

    points = {
        "Nose": keypoints[0, :2],
        "Neck": keypoints[1, :2],
        "R_Shoulder": keypoints[2, :2],
        "L_Shoulder": keypoints[5, :2],
        "R_Elbow": keypoints[3, :2],
        "L_Elbow": keypoints[6, :2],
        "R_Wrist": keypoints[4, :2],
        "L_Wrist": keypoints[7, :2],
        "R_Hip": keypoints[8, :2],
        "L_Hip": keypoints[11, :2],
        "R_Knee": keypoints[9, :2],
        "L_Knee": keypoints[12, :2],
        "R_Ankle": keypoints[10, :2],
        "L_Ankle": keypoints[13, :2],
    }
    
    neck_to_hip = euclidean_dist(points["Neck"], points["R_Hip"]) 
    shoulder_width = euclidean_dist(points["R_Shoulder"], points["L_Shoulder"])
    upper_arm_R = euclidean_dist(points["R_Shoulder"], points["R_Elbow"])
    lower_arm_R = euclidean_dist(points["R_Elbow"], points["R_Wrist"])
    upper_arm_L = euclidean_dist(points["L_Elbow"], points["L_Wrist"])
    lower_arm_L = euclidean_dist(points["L_Elbow"], points["L_Wrist"])
    upper_leg_R = euclidean_dist(points["R_Hip"], points["R_Knee"])
    lower_leg_R = euclidean_dist(points["R_Knee"], points["R_Ankle"])
    upper_leg_L = euclidean_dist(points["L_Hip"], points["L_Knee"])
    lower_leg_L = euclidean_dist(points["L_Knee"], points["L_Ankle"])

    arm_length_R =  upper_arm_R + lower_arm_R
    arm_length_L = upper_arm_L + lower_arm_L
    
    #Uoc tinh chieu dai ban tay (tu le giua ban tay va cach tay)
    hand_length_R = arm_length_R*0.14
    hand_length_L = arm_length_L*0.14
    hand_span_estimated = hand_length_R + hand_length_L

    leg_length_R = upper_leg_R + lower_leg_R
    leg_length_L = upper_leg_L + lower_leg_L
    height_estimate = arm_length_R + arm_length_L + hand_span_estimated
    neck_length = euclidean_dist(points["Neck"], points["Nose"])  # Cổ
    head_length = neck_length * 1.5  # Giả định chiều dài đầu = 1.5 lần chiều dài cổ

    torso_length = neck_to_hip + head_length
    length = {
        "neck_to_height": neck_to_hip/height_estimate*height,
        "shoulder_width": shoulder_width/height_estimate*height,
        "arm_length_R": arm_length_R/height_estimate*height,
        "arm_length_L": arm_length_L/height_estimate*height,
        "hand_span_estimated": hand_span_estimated/height_estimate*height,
        "leg_length_R": (leg_length_R)/height_estimate*height,
        "leg_length_L": (leg_length_L)/height_estimate*height,
        "neck_length": neck_length / height_estimate * height,
        "head_length": head_length / height_estimate * height,
        "torso_length": torso_length / height_estimate * height
    }

    return length

def calculate_bode_weight(height, weight, sex='Male'):
    BMI_user = weight/(height**2)
    BMI_avg = 62/((168/100)**2)

    scale_factor_weight = BMI_user/BMI_avg
    chest_real = 0 #vong nguc
    waist_real = 0 #vong eo
    hip_real = 0 #vong hong
    if sex == 'Male':
        chest_real = 94*scale_factor_weight
        waist_real = 83*scale_factor_weight
        hip_real = 94*scale_factor_weight

    elif sex == 'Female':
        chest_real = 89*scale_factor_weight
        waist_real = 70*scale_factor_weight
        hip_real = 94*scale_factor_weight

    return {
        'chest': chest_real,
        'waist': waist_real,
        'hip': hip_real,
    }
        

def calculate_body_parameter( image_path ,height, weight, sex='Male'):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_folder = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))


def export_to_json_with_measurements(image_path,height, weight, sex='Male'):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    output_folder = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    body_length = calculate_body_legnth(image_path, height)
    measurements = calculate_bode_weight(height, weight, sex)
    body_data = {
        "height": height,
        "weight": weight,
        "sex": sex,
        "measurements": measurements,  # Thêm số đo 3 vòng
        "body_ratios": body_length  # Thêm các tỷ lệ chiều dài cơ thể
    }

    output_path = os.path.join(output_folder,"body_data_with_ratios.json") 
    with open(output_path, "w") as json_file:
        json.dump(body_data, json_file, indent=4)

if __name__ == "__main__":
    height = 1.75
    weight = 70
    sex = "Male"
    image_path = os.path.abspath("./storage/input/person2/person2.jpg")
    export_to_json_with_measurements(image_path,height, weight, sex)