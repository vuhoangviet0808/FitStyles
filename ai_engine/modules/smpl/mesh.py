import json
import numpy as np
import torch
import smplx
import os
import pickle
from scipy.spatial.transform import Rotation as R
from ai_engine.modules.pose_estimation.Convert_2D_to_3D import convert_2D_3D
from ai_engine.modules.pose_estimation.parameter import export_smpl_joints_to_json
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

model_path = os.path.abspath("./ai_engine/modules/smpl/smplify-x/models/smplx/SMPLX_NEUTRAL.pkl")
model_folder = os.path.abspath("./ai_engine/modules/smpl/smplify-x/models/")
IMAGE_DIR = os.path.abspath("./storage/input")
OUTPUT_DIR = os.path.abspath("./storage/output")

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

def adjust_pose_to_vietnamese_standard(keypoints_3d):
    """Điều chỉnh tư thế dựa trên khung người Việt Nam"""
    scale_factor = 1.64 / np.linalg.norm(keypoints_3d[0] - keypoints_3d[8])  # Chuẩn hóa theo chiều cao trung bình
    keypoints_3d *= scale_factor

    # Điều chỉnh tỷ lệ chân, tay theo dữ liệu người Việt
    keypoints_3d[3:5] *= 1.05  # Chân dài hơn một chút
    keypoints_3d[6:8] *= 0.98  # Tay ngắn hơn một chút

    return keypoints_3d


def normalize_keypoints(keypoints_3d):
    center = np.mean(keypoints_3d, axis = 0)
    keypoints_3d -=center
    keypoints_3d[:, [1,2]] = keypoints_3d[:, [2,1]]
    keypoints_3d[:,1] *=-1
    return keypoints_3d

def compute_joint_angles(keypoints_3d):
    """Tính góc quay của khớp từ keypoints 3D để đưa vào SMPLX"""
    num_joints = min(21, len(keypoints_3d))  # Đảm bảo không vượt quá số lượng thật sự
    body_pose = np.zeros((num_joints, 3))  

    for i in range(num_joints - 1):  # Dừng vòng lặp đúng giới hạn
        joint_vec = keypoints_3d[i + 1] - keypoints_3d[i]

        if joint_vec.shape != (3,):
            joint_vec = np.resize(joint_vec, (3,))

        try:
            rotation, _ = R.align_vectors(joint_vec.reshape(1, 3), np.array([[0, 1, 0]]))
            body_pose[i] = rotation.as_euler('xyz', degrees=False)
        except Exception as e:
            print(f"🚨 Lỗi khi tính góc tại khớp {i}: {e}")
            body_pose[i] = np.zeros(3)  # Nếu lỗi, đặt về 0

    print("📌 Góc khớp SMPLX:", body_pose.shape)
    return body_pose.flatten()  # Trả về kích thước (21 * 3 = 63)

def adjust_keypoints_to_smplx(keypoints_3d):
    """ Điều chỉnh keypoints để có đúng 21 điểm """
    target_joints = 21
    current_joints = len(keypoints_3d)

    if current_joints < target_joints:
        print(f"🚨 Số keypoints hiện tại ({current_joints}) nhỏ hơn 21, sẽ nội suy...")
        extra_joints = target_joints - current_joints
        last_joint = keypoints_3d[-1]  # Sao chép khớp cuối cùng
        for _ in range(extra_joints):
            keypoints_3d = np.vstack([keypoints_3d, last_joint])  # Thêm khớp giả định

    elif current_joints > target_joints:
        print(f"🚨 Số keypoints hiện tại ({current_joints}) lớn hơn 21, sẽ cắt bớt...")
        keypoints_3d = keypoints_3d[:target_joints]  # Cắt bớt các điểm dư

    print(f"📌 Keypoints sau khi điều chỉnh: {len(keypoints_3d)}")
    return keypoints_3d

def smpl_mesh(image_path):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    path = os.path.abspath(os.path.dirname(image_path))
    output_path = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    keypoints_3d_path = convert_2D_3D(image_path)

    if not os.path.exists(keypoints_3d_path):
        raise FileNotFoundError(f"🚨 Không tìm thấy file keypoints: {keypoints_3d_path}")
    with open(keypoints_3d_path, "r") as f:
        data = json.load(f)
    keypoints_3d = np.array(data["keypoints_3d"], dtype=np.float32)

    keypoints_3d = adjust_pose_to_vietnamese_standard(keypoints_3d)

    keypoints_3d = normalize_keypoints(keypoints_3d)

    np.savez(f"{path}/keypoints_smpl.npz", keypoints=keypoints_3d)
    with open(model_path, "rb") as f:
        try:
            pickle.load(f, encoding="latin1")
            print("✅ File SMPLX hợp lệ!")
        except Exception as e:
            raise ValueError(f"🚨 File model bị lỗi: {e}")
    

    device = torch.device("cpu")
    model = smplx.create(model_folder, model_type="smplx", gender="neutral", use_pca=False).to(device)

    keypoints_3d = adjust_keypoints_to_smplx(keypoints_3d)


    body_pose_angles = compute_joint_angles(keypoints_3d)

    global_orient_tensor = torch.tensor([[0, 0, np.pi / 8]], dtype=torch.float32, device=device)

    output = model(
        global_orient=global_orient_tensor,
        body_pose=torch.tensor(body_pose_angles, dtype=torch.float32, device=device).unsqueeze(0),
        betas=vietnamese_body_shape.unsqueeze(0),  # Sử dụng hình dạng chuẩn của người Việt
        transl=torch.zeros(1, 3, dtype=torch.float32, device=device)
    )

    vertices = output.vertices.detach().cpu().numpy().squeeze()
    faces = model.faces
    obj_filename = f"{output_path}/smpl_model.obj"
    with open(obj_filename, "w") as f:
        # Ghi vertices (đỉnh)
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")

        # Ghi faces (mặt tam giác)
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    print(f"✅ Đã tạo mô hình SMPL và lưu vào {obj_filename}")

if __name__ =='__main__':
    image_path = os.path.abspath("./storage/input/person2/person2.jpg")
    smpl_mesh(image_path)