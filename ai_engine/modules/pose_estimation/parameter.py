import numpy as np
from ai_engine.modules.pose_estimation.Convert_2D_to_3D import get_keypoints_from_openpose, load_keypoints
from ai_engine.config import OUTPUT_DIR, MODEL_SMPLX_PATH, MODEL_SMPLX_DIR
import os
import json
import smplx
import torch
import numpy as np
import trimesh
import os
import json

#smpl
#import torch
from scipy.optimize import minimize
#import numpy as np

model_path = MODEL_SMPLX_PATH
model_folder = MODEL_SMPLX_DIR

def euclidean_dist(a, b):
    return np.linalg.norm(np.array(a) - np.array(b))


def calculate_body_length(image_path, height):
    front = get_keypoints_from_openpose(image_path)
    front_keypoints = load_keypoints(front)

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

    leg_length = max(leg_length_L, leg_length_R)
    arm_length = max(arm_length_L, arm_length_R)


    torso_length = neck_to_hip + head_length
    # length = {
    #     "neck_to_height": neck_to_hip/height_estimate*height,
    #     "shoulder_width": shoulder_width/height_estimate*height,
    #     "arm_length_R": arm_length_R/height_estimate*height,
    #     "arm_length_L": arm_length_L/height_estimate*height,
    #     "hand_span_estimated": hand_span_estimated/height_estimate*height,
    #     "leg_length_R": (leg_length_R)/height_estimate*height,
    #     "leg_length_L": (leg_length_L)/height_estimate*height,
    #     "neck_length": neck_length / height_estimate * height,
    #     "head_length": head_length / height_estimate * height,
    #     "torso_length": torso_length / height_estimate * height
    # }

    length = {
        "height": height,
        "head": head_length/height_estimate * height,
        "neck": neck_length/height_estimate * height,
        "torso": torso_length/height_estimate * height,
        "leg": leg_length/height_estimate * height,
        "arm": arm_length/height_estimate * height,
        "hand": hand_span_estimated/height_estimate * height,
        "shoulder": shoulder_width/height_estimate*height,
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
        
# def export_to_json_with_measurements(image_path,height, weight, sex='Male'):
#     base_name = os.path.splitext(os.path.basename(image_path))[0]
#     output_folder = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
#     body_length = calculate_body_length(image_path, height)
#     measurements = calculate_bode_weight(height, weight, sex)
#     body_data = {
#         "height": height,
#         "weight": weight,
#         "sex": sex,
#         "measurements": measurements,  # Thêm số đo 3 vòng
#         "body_ratios": body_length  # Thêm các tỷ lệ chiều dài cơ thể
#     }

#     output_path = os.path.join(output_folder,"body_data_with_ratios.json") 
#     with open(output_path, "w") as json_file:
#         json.dump(body_data, json_file, indent=4)

# if __name__ == "__main__":
#     height = 1.75
#     weight = 70
#     sex = "Male"
#     image_path = os.path.abspath("./storage/input/person2/person2.jpg")
#     export_to_json_with_measurements(image_path,height, weight, sex)

#SMPL

def estimate_body_depth_width(measurements):
    body_dimensions = {}

    # Tính chiều sâu và chiều rộng cho các bộ phận cơ thể
    body_dimensions['chest'] = {
        'depth': measurements['chest'] * 0.3,  # 30% của vòng ngực
        'width': measurements['chest'] * 0.5  # 50% của vòng ngực (giả định)
    }
    body_dimensions['waist'] = {
        'depth': measurements['waist'] * 0.25,  # 25% của vòng eo
        'width': measurements['waist'] * 0.5  # 50% của vòng eo (giả định)
    }
    body_dimensions['hip'] = {
        'depth': measurements['hip'] * 0.3,  # 30% của vòng hông
        'width': measurements['hip'] * 0.5  # 50% của vòng hông (giả định)
    }

    return body_dimensions

def loss_function(model ,betas, body_length, body_weight):
    betas = torch.tensor(betas).float().unsqueeze(0)
    output = model(betas=betas)
    joints = output.joints[0]

    predicted_height = joints[0,1].item()
    predicted_arm_length = (joints[16, 1] - joints[17, 1]).abs().item()
    predicted_leg_length = (joints[1,1] - joints[4,1]).abs().item()
    predicted_shoulder_width = (joints[12, 0] - joints[11, 0]).abs().item()

    predicted_chest_width = (joints[12, 0] - joints[11, 0]).abs().item()
    predicted_waist_width = (joints[9, 0] - joints[8, 0]).abs().item()
    predicted_hips_width = (joints[7, 0] - joints[6, 0]).abs().item()
    loss = (
        (predicted_height - body_length["height"])**2
        + (predicted_arm_length - body_length["arm"])**2
        + (predicted_shoulder_width - body_length['shoulder'])**2
        + (predicted_leg_length - body_length["arm"])**2
        + (predicted_chest_width - body_weight['chest'])**2
        + (predicted_waist_width - body_weight['waist'])**2
        + (predicted_hips_width - body_weight['hip'])**2
    )
    return loss


def smpl_joints_to_parameters(model ,body_length, body_weight):
    # initial_betas = torch.tensor([0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0], dtype=torch.float32)
    initial_betas = np.zeros(10, dtype = np.float32)
    loss_func_with_params = lambda betas: loss_function(model, betas, body_length, body_weight) 
    bounds = [(-1, 1)]*10
    result = minimize(loss_func_with_params, initial_betas, method = "Powell", bounds = bounds)

    optimal_betas = torch.tensor(result.x, dtype=torch.float32)

    pose = torch.zeros(1, 63)  # Body pose (21 khớp, mỗi khớp có 3 tham số góc xoay)

    # betas[0] = body_measurements['chest'] * 0.01  # Ứớc tính shape từ vòng ngực
    # betas[1] = body_measurements['waist'] * 0.01  # Ứớc tính shape từ vòng eo
    # betas[2] = body_measurements['hip'] * 0.01  # Ứớc tính shape từ vòng hông

    pose = torch.zeros(1, 63, dtype=torch.float32)

    return optimal_betas, pose
import torch.nn as nn
import torch.optim as optim 
def train_betas_nn(model, smplx_model, body_length, body_measurements, num_epochs=500, learning_rate=1e-4):
    """
    Huấn luyện mạng Neural Network để tối ưu `betas` trong SMPL-X.
    """
    # Chuyển input thành tensor
    input_features = torch.tensor([
        body_length["height"], body_length["arm"], body_length["shoulder"], body_length["leg"],
        body_measurements["chest"], body_measurements["waist"], body_measurements["hip"]
    ], dtype=torch.float32).unsqueeze(0)  # (1, 7)

    # Optimizer & Loss
    optimizer = optim.Adam(model.parameters(), lr=learning_rate)

    loss_fn = nn.MSELoss()
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=50, gamma=0.7)

    # Train loop
    for epoch in range(num_epochs):
        optimizer.zero_grad()  # Xóa gradient cũ
        
        # Dự đoán `betas` từ mạng neural network
        betas_pred = model(input_features)  # betas_pred có requires_grad=True

        # Tính loss với SMPL-X
        loss = loss_function(betas_pred, smplx_model, body_length, body_measurements)
        
        # Backpropagation
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
        # 🔥 Kiểm tra Gradient của Model
        # for name, param in model.named_parameters():
        #     if param.grad is not None:
        #         print(f"🔥 Gradient của {name}: {param.grad.norm().item()}")
        
        optimizer.step()
        scheduler.step()
        
        if (epoch + 1) % 50 == 0:
            # print(f"🔥 Epoch {epoch+1}/{num_epochs}, Loss: {loss.item()}")
            print(f"{betas_pred}")

    return betas_pred.detach()

def create_smplx_model(model, betas, pose):
    # device = torch.device("cpu")
    # smplx_model = smplx.create(model_folder, model_type='smplx', gender='male', use_pca=False).to(device)
    
    output = model.forward(betas=betas.unsqueeze(0), body_pose=pose)
    
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    return vertices, model.faces


def display_3d_model(vertices, faces):
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.show()

class BetasPredictor(nn.Module):
    def __init__(self, input_dim=7, output_dim=100):  # 7 input features (chiều cao, vòng eo, vòng mông, v.v.)
        super(BetasPredictor, self).__init__()
        self.model = nn.Sequential(
            nn.Linear(input_dim, 64),
            nn.ReLU(),
            nn.Linear(64, 128),
            nn.Sigmoid(),
            nn.Linear(128, 256),
            nn.ReLU(),
            nn.Linear(256, output_dim),
        )

    def forward(self, x):
        return self.model(x)


# Ví dụ chạy thử
if __name__ == "__main__":
    height = 1.65
    weight = 70
    sex = "Male"
    image_path = os.path.abspath("./storage/input/person2/person2.jpg")
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    path = os.path.abspath(os.path.dirname(image_path))
    output_path = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    body_length = calculate_body_length(image_path, height)
    body_measurements = calculate_bode_weight(height, weight, sex)
    device = torch.device("cpu")
    smplx_model = smplx.create(model_folder, model_type='smplx', gender=sex, use_pca=False).to(device)
    # num_betas =200
    # smplx_model = smplx.create(MODEL_SMPLX_DIR, model_type='smplx', gender="male", num_betas = num_betas, use_pca=False)
    
    betas, pose = smpl_joints_to_parameters(smplx_model, body_length, body_measurements)
    print(betas)
    # Tạo mô hình SMPL-X và hiển thị mô hình 3D
    vertices, faces = create_smplx_model(smplx_model,betas, pose)
    obj_filename = f"{output_path}/smpl_model.obj"
    with open(obj_filename, "w") as f:
        # Ghi vertices (đỉnh)
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # Ghi faces (mặt tam giác)
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    print(f"✅ Đã tạo mô hình SMPL và lưu vào {obj_filename}")
    display_3d_model(vertices, faces)

    # betas_model = BetasPredictor(input_dim=7, output_dim=num_betas)

    # # Train NN để tìm `betas`
    # betas_opt = train_betas_nn(betas_model, smplx_model, body_length, body_measurements)

    # print("🔥 Betas tối ưu sau khi học bằng Neural Network:", betas_opt)

    # # Chạy SMPL-X với betas mới
    # pose = torch.zeros(1, 63, dtype=torch.float32)  # Pose mặc định
    # expression = torch.zeros(1, 10, dtype=torch.float32)  # Biểu cảm khuôn mặt

    # output = smplx_model.forward(betas=betas_opt, body_pose=pose)

    # # Hiển thị mô hình 3D sau khi tối ưu
    # vertices = output.vertices.detach().cpu().numpy().squeeze()
    # display_3d_model(vertices, smplx_model.faces)