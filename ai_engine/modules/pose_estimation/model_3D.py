import smplx
import torch
from scipy.optimize import minimize
import numpy as np
import os
from ai_engine.config import OUTPUT_DIR, MODEL_SMPLX_DIR
from ai_engine.modules.pose_estimation.parameter import calculate_bode_weight, calculate_body_length
import trimesh

def loss_funtion(model ,betas, body_length, body_weight):
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
    loss_func_with_params = lambda betas: loss_funtion(model, betas, body_length, body_weight) 
    result = minimize(loss_func_with_params, initial_betas, method = "L-BFGS-B")

    optimal_betas = torch.tensor(result.x, dtype=torch.float32)

    pose = torch.zeros(1, 63)  
    pose = torch.zeros(1, 63, dtype=torch.float32)

    return optimal_betas, pose


def create_smplx_model(model, betas, pose):
    # device = torch.device("cpu")
    # smplx_model = smplx.create(model_folder, model_type='smplx', gender='male', use_pca=False).to(device)
    
    output = model.forward(betas=betas.unsqueeze(0), body_pose=pose)
    
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    return vertices, model.faces


def display_3d_model(vertices, faces):
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.show()


# Ví dụ chạy thử
if __name__ == "__main__":
    height = 1.75
    weight = 70
    sex = "Male"
    image_path = os.path.abspath("./storage/input/person2/person2.jpg")
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    path = os.path.abspath(os.path.dirname(image_path))
    output_path = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    body_length = calculate_body_length(image_path, height)
    body_measurements = calculate_bode_weight(height, weight, sex)
    device = torch.device("cpu")
    smplx_model = smplx.create(MODEL_SMPLX_DIR, model_type='smplx', gender=sex, use_pca=False).to(device)
    
    betas, pose = smpl_joints_to_parameters(smplx_model, body_length, body_measurements)

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