import json
import numpy as np
import torch
import smplx
import os
from scipy.spatial.transform import Rotation as R

# Đường dẫn đến mô hình SMPLX
model_folder = os.path.abspath("./ai_engine/modules/smpl/smplify-x/models/")

# 📌 Thông số hình dạng chuẩn của người Việt Nam
vietnamese_body_shape = torch.tensor([
    0.0,  # Body width (x)
    -0.02, # Body depth (y)
    -0.05, # Body height (z)
    0.01,  # Leg length
    -0.02, # Arm length
    0.0,   # Shoulder width
    -0.01, # Hip width
    0.02,  # Neck size
    -0.02, # Head size
    0.0    # Additional small tweaks
], dtype=torch.float32)

def convert_openpose_to_smplx_coords(keypoints_3d):
    """ Chuyển đổi hệ tọa độ từ OpenPose sang SMPLX """
    keypoints_3d[:, [1, 2]] = keypoints_3d[:, [2, 1]]  # Hoán đổi Y & Z
    keypoints_3d[:, 1] *= -1  # Đảo ngược trục Y
    return keypoints_3d

def adjust_pose_to_vietnamese_standard(keypoints_3d):
    """ Điều chỉnh tỷ lệ cơ thể theo hình dạng người Việt """
    scale_factor = 1.64 / np.linalg.norm(keypoints_3d[0] - keypoints_3d[8])  # Chuẩn hóa theo chiều cao trung bình
    keypoints_3d *= scale_factor

    keypoints_3d[3:5] *= 1.05  # Chân dài hơn một chút
    keypoints_3d[6:8] *= 0.98  # Tay ngắn hơn một chút

    return keypoints_3d

def compute_joint_angles(keypoints_3d):
    """Tính toán góc quay của các khớp từ keypoints 3D để đưa vào SMPLX"""
    num_joints = min(21, len(keypoints_3d))
    body_pose = np.zeros((num_joints, 3))

    for i in range(num_joints - 1):
        joint_vec = keypoints_3d[i + 1] - keypoints_3d[i]

        if np.linalg.norm(joint_vec) == 0:
            continue  # Nếu vector bị lỗi (trùng điểm), bỏ qua

        try:
            rotation, _ = R.align_vectors(joint_vec.reshape(1, 3), np.array([[0, 1, 0]]))
            body_pose[i] = rotation.as_euler('xyz', degrees=False)
        except Exception as e:
            print(f"🚨 Lỗi khi tính góc tại khớp {i}: {e}")
            body_pose[i] = np.zeros(3)

    return body_pose.flatten()

def smpl_mesh(image_path):
    """Tạo mô hình SMPL từ keypoints 3D OpenPose + điều chỉnh theo dữ liệu người Việt"""
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    keypoints_3d_path = os.path.abspath(f"./storage/output/{base_name}/output_3d.json")

    # 📌 Đọc keypoints từ file JSON
    with open(keypoints_3d_path, "r") as f:
        data = json.load(f)
    keypoints_3d = np.array(data["keypoints_3d"], dtype=np.float32)

    # 📌 Chuyển hệ tọa độ OpenPose → SMPLX
    keypoints_3d = convert_openpose_to_smplx_coords(keypoints_3d)

    # 📌 Điều chỉnh theo tỷ lệ cơ thể người Việt
    keypoints_3d = adjust_pose_to_vietnamese_standard(keypoints_3d)

    # 📌 Khởi tạo mô hình SMPLX
    device = torch.device("cpu")
    model = smplx.create(model_folder, model_type="smplx", gender="neutral", use_pca=False).to(device)

    # 📌 Tính toán góc quay của khớp (body_pose)
    body_pose_angles = compute_joint_angles(keypoints_3d)

    # 📌 Điều chỉnh Global Orientation để tránh mô hình bị nghiêng
    global_orient_tensor = torch.tensor([[0, 0, np.pi / 12]], dtype=torch.float32, device=device)  # Xoay nhẹ 15 độ

    # 📌 Tạo mô hình với các tham số chuẩn của người Việt
    output = model(
        global_orient=global_orient_tensor,
        body_pose=torch.tensor(body_pose_angles, dtype=torch.float32, device=device).unsqueeze(0),
        betas=vietnamese_body_shape.unsqueeze(0),  # Áp dụng hình dạng chuẩn người Việt
        transl=torch.zeros(1, 3, dtype=torch.float32, device=device)
    )

    # 📌 Lấy vertices và faces để xuất file OBJ
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    faces = model.faces

    obj_filename = f"./storage/output/{base_name}/smpl_model.obj"

    with open(obj_filename, "w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    print(f"✅ Đã tạo mô hình SMPL và lưu vào {obj_filename}")

if __name__ == "__main__":
    image_path = os.path.abspath("./storage/input/person2/person2.jpg")
    smpl_mesh(image_path)


import json
import numpy as np
import torch
import smplx
import os
from scipy.spatial.transform import Rotation as R

# Đường dẫn đến mô hình SMPLX
model_folder = os.path.abspath("./ai_engine/modules/smpl/smplify-x/models/")

# 📌 Thông số chuẩn của người Việt Nam
vietnamese_body_shape = torch.tensor([
    0.0,  # Body width (x)
    -0.02, # Body depth (y)
    -0.05, # Body height (z)
    0.01,  # Leg length
    -0.02, # Arm length
    0.0,   # Shoulder width
    -0.01, # Hip width
    0.02,  # Neck size
    -0.02, # Head size
    0.0    # Additional small tweaks
], dtype=torch.float32)

def convert_openpose_to_smplx_coords(keypoints_3d):
    """Chuyển đổi hệ tọa độ từ OpenPose sang SMPLX"""
    keypoints_3d[:, [1, 2]] = keypoints_3d[:, [2, 1]]  # Hoán đổi Y & Z
    keypoints_3d[:, 1] *= -1  # Đảo ngược trục Y
    return keypoints_3d

def compute_relative_ratios(keypoints_3d):
    """Tính toán tỷ lệ cơ thể từ OpenPose"""
    total_height = np.linalg.norm(keypoints_3d[0] - keypoints_3d[8])  # Tổng chiều cao dựa trên đầu & hông

    neck_length = np.linalg.norm(keypoints_3d[1] - keypoints_3d[2]) / total_height  # Tỷ lệ cổ
    leg_length = np.linalg.norm(keypoints_3d[3] - keypoints_3d[5]) / total_height  # Tỷ lệ chân
    arm_length = np.linalg.norm(keypoints_3d[6] - keypoints_3d[8]) / total_height  # Tỷ lệ tay

    return neck_length, leg_length, arm_length

def adjust_smpl_betas(neck_ratio, leg_ratio, arm_ratio):
    """Điều chỉnh thông số hình dạng SMPLX theo tỷ lệ từ OpenPose"""
    new_betas = vietnamese_body_shape.clone()
    
    new_betas[2] += (neck_ratio - 0.13) * 0.2  # Cổ
    new_betas[3] += (leg_ratio - 0.45) * 0.2  # Chân
    new_betas[4] += (arm_ratio - 0.32) * 0.2  # Tay
    
    return new_betas

def compute_joint_angles(keypoints_3d):
    """Tính toán góc quay của các khớp từ keypoints 3D để đưa vào SMPLX"""
    num_joints = min(21, len(keypoints_3d))
    body_pose = np.zeros((num_joints, 3))

    for i in range(num_joints - 1):
        joint_vec = keypoints_3d[i + 1] - keypoints_3d[i]

        if np.linalg.norm(joint_vec) == 0:
            continue  # Nếu vector bị lỗi (trùng điểm), bỏ qua

        try:
            rotation, _ = R.align_vectors(joint_vec.reshape(1, 3), np.array([[0, 1, 0]]))
            body_pose[i] = rotation.as_euler('xyz', degrees=False)
        except Exception as e:
            print(f"🚨 Lỗi khi tính góc tại khớp {i}: {e}")
            body_pose[i] = np.zeros(3)

    return body_pose.flatten()

def smpl_mesh(image_path):
    """Tạo mô hình SMPL từ keypoints 3D OpenPose + điều chỉnh theo dữ liệu người Việt"""
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    keypoints_3d_path = os.path.abspath(f"./storage/output/{base_name}/output_3d.json")

    # 📌 Đọc keypoints từ file JSON
    with open(keypoints_3d_path, "r") as f:
        data = json.load(f)
    keypoints_3d = np.array(data["keypoints_3d"], dtype=np.float32)

    # 📌 Chuyển hệ tọa độ OpenPose → SMPLX
    keypoints_3d = convert_openpose_to_smplx_coords(keypoints_3d)

    # 📌 Tính toán tỷ lệ tương đối từ OpenPose
    neck_ratio, leg_ratio, arm_ratio = compute_relative_ratios(keypoints_3d)

    # 📌 Điều chỉnh betas dựa trên tỷ lệ thực tế
    new_betas = adjust_smpl_betas(neck_ratio, leg_ratio, arm_ratio)

    # 📌 Khởi tạo mô hình SMPLX
    device = torch.device("cpu")
    model = smplx.create(model_folder, model_type="smplx", gender="neutral", use_pca=False).to(device)

    # 📌 Tính toán góc quay của khớp (body_pose)
    body_pose_angles = compute_joint_angles(keypoints_3d)

    # 📌 Điều chỉnh Global Orientation để tránh mô hình bị nghiêng
    global_orient_tensor = torch.tensor([[0, 0, np.pi / 12]], dtype=torch.float32, device=device)  # Xoay nhẹ 15 độ

    # 📌 Tạo mô hình với các thông số tinh chỉnh
    output = model(
        global_orient=global_orient_tensor,
        body_pose=torch.tensor(body_pose_angles, dtype=torch.float32, device=device).unsqueeze(0),
        betas=new_betas.unsqueeze(0),  # Áp dụng betas mới
        transl=torch.zeros(1, 3, dtype=torch.float32, device=device)
    )

    # 📌 Lấy vertices và faces để xuất file OBJ
    vertices = output.vertices.detach().cpu().numpy().squeeze()
    faces = model.faces

    obj_filename = f"./storage/output/{base_name}/smpl_model.obj"

    with open(obj_filename, "w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    print(f"✅ Đã tạo mô hình SMPL và lưu vào {obj_filename}")

if __name__ == "__main__":
    image_path = os.path.abspath("./storage/input/person2/person2.jpg")
    smpl_mesh(image_path)
