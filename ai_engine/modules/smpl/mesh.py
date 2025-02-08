import json
import numpy as np
import torch
import smplx
import os
import pickle
from scipy.spatial.transform import Rotation as R
from ai_engine.modules.pose_estimation.Conver_2D_to_3D import convert_2D_3D


model_path = os.path.abspath("./ai_engine/modules/smpl/smplify-x/models/smplx/SMPLX_NEUTRAL.pkl")
model_folder = os.path.abspath("./ai_engine/modules/smpl/smplify-x/models/")
IMAGE_DIR = os.path.abspath("./storage/input")
OUTPUT_DIR = os.path.abspath("./storage/output")

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
    np.savez(f"{path}/keypoints_smpl.npz", keypoints=keypoints_3d)
    with open(model_path, "rb") as f:
        try:
            pickle.load(f, encoding="latin1")
            print("✅ File SMPLX hợp lệ!")
        except Exception as e:
            raise ValueError(f"🚨 File model bị lỗi: {e}")
    device = torch.device("cpu")
    model = smplx.create(model_folder, model_type="smplx", gender="neutral", use_pca=False).to(device)
    openpose_to_smplx = [
        0,  # MidHip
        1,  # Rhip
        2,  # RKnee
        3,  # RAnkle
        4,  # Lhip
        5,  # LKnee
        6,  # LAnkle
        7,  # Spine
        8,  # Neck
        9,  # Head
        10, # LShoulder
        11, # LElbow
        12, # LWrist
        13, # RShoulder
        14, # RElbow
        15, # RWrist
        16, # LHand
        17, # RHand
        18, # LBigToe
        19, # LSmallToe
        20, # LHeel
        21, # RBigToe
        22, # RSmallToe
        23  # RHeel
    ]

    smplx_keypoints_3d = keypoints_3d[openpose_to_smplx]
    def compute_joint_angles(keypoints_3d):
        """ Chuyển keypoints 3D thành các góc quay tương ứng với SMPLX """
        body_pose = np.zeros((23, 3))  
        for i in range(1, len(keypoints_3d) - 1):
            joint_vec = keypoints_3d[i + 1] - keypoints_3d[i]
            if joint_vec.shape != (3,):
                joint_vec = np.resize(joint_vec, (3,))  
            try:
                rotation, _ = R.align_vectors(joint_vec.reshape(1, 3), np.array([[0, 1, 0]]))
                body_pose[i - 1] = rotation.as_euler('xyz', degrees=False)  
            except Exception as e:
                print(f"🚨 Lỗi khi tính góc tại khớp {i}: {e}")
                body_pose[i - 1] = np.zeros(3) 

        return body_pose.flatten()

    body_pose_angles = compute_joint_angles(smplx_keypoints_3d)
    num_body_joints = model.NUM_BODY_JOINTS  
    expected_body_pose_size = num_body_joints * 3  

    body_pose_tensor = torch.tensor(body_pose_angles, dtype=torch.float32, device=device).unsqueeze(0)

    if body_pose_tensor.shape[1] > expected_body_pose_size:
        body_pose_tensor = body_pose_tensor[:, :expected_body_pose_size]  
    elif body_pose_tensor.shape[1] < expected_body_pose_size:
        padding = torch.zeros((1, expected_body_pose_size - body_pose_tensor.shape[1]), device=device)
        body_pose_tensor = torch.cat((body_pose_tensor, padding), dim=1)  

    print(f"📌 Final body_pose shape: {body_pose_tensor.shape}")
    transl_tensor = torch.zeros((1, 3), dtype=torch.float32, device=device)
    transl_tensor = torch.zeros(( 1, 3), dtype=torch.float32, device=device)
    output = model(
        global_orient=torch.zeros(1, 3, device=device),  
        body_pose=body_pose_tensor,  
        betas=torch.zeros(1, 10, device=device),  
        transl=transl_tensor 
    )

    vertices = output.vertices.detach().cpu().numpy().squeeze()
    faces = model.faces
    obj_filename = f"{output_path}/smpl_model.obj"
    with open(obj_filename, "w") as f:
        for v in vertices:
            f.write(f"v {v[0]} {v[1]} {v[2]}\n")
        for face in faces:
            f.write(f"f {face[0]+1} {face[1]+1} {face[2]+1}\n")

    print(f"✅ Đã tạo mô hình SMPL và lưu vào {obj_filename}")

if __name__ =='__main__':
    image_path = os.path.abspath("./storage/input/person2/person2.jpg")
    smpl_mesh(image_path)
