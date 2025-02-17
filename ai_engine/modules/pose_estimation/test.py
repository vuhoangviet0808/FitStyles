import torch
import numpy as np
import smplx
import trimesh
from ai_engine.config import MODEL_SMPLX_DIR

# Khởi tạo mô hình SMPL-X
smplx_model = smplx.create(MODEL_SMPLX_DIR, model_type='smplx', gender="male", use_pca=False)

def loss_function(betas, model, body_length, body_measurements):
    """
    Tính toán loss dựa trên số đo thực tế và số đo từ mô hình SMPL-X.
    """
    output = model(betas=betas)
    joints = output.joints[0]  # Lấy tọa độ khớp từ mô hình

    # Dự đoán số đo từ mô hình SMPL-X
    predicted_height = joints[0, 1]
    predicted_arm_length = (joints[16, 1] - joints[17, 1]).abs()
    predicted_leg_length = (joints[1, 1] - joints[4, 1]).abs()
    predicted_shoulder_width = (joints[12, 0] - joints[11, 0]).abs()

    predicted_chest_width = (joints[12, 0] - joints[11, 0]).abs()
    predicted_waist_width = (joints[9, 0] - joints[8, 0]).abs()
    predicted_hips_width = (joints[7, 0] - joints[6, 0]).abs()

    # Tính loss
    loss = (
        (predicted_height - body_length["height"])**2 +
        (predicted_arm_length - body_length["arm"])**2 +
        (predicted_leg_length - body_length["leg"])**2 +
        (predicted_shoulder_width - body_length["shoulder"])**2 +
        (predicted_chest_width - body_measurements["chest"])**2 +
        (predicted_waist_width - body_measurements["waist"])**2 +
        (predicted_hips_width - body_measurements["hip"])**2
    )

    return loss

def smpl_joints_to_parameters(model, body_length, body_measurements, num_iterations=200, learning_rate=0.01):
    """
    Tối ưu `betas` bằng Adam để khớp với số đo thực tế.
    """
    # Khởi tạo `betas` có requires_grad=True
    betas = torch.zeros(1, 10, dtype=torch.float32, requires_grad=True)

    # Khởi tạo optimizer Adam
    optimizer = torch.optim.Adam([betas], lr=learning_rate)

    # Tối ưu hóa Adam
    for i in range(num_iterations):
        optimizer.zero_grad()  # Xóa gradient cũ
        loss = loss_function(betas, model, body_length, body_measurements)  # Tính loss
        loss.backward()  # Tính gradient
        optimizer.step()  # Cập nhật betas

        if (i + 1) % 20 == 0:  # In loss sau mỗi 20 vòng lặp
            print(f"🔥 Iter {i+1}/{num_iterations}, Loss: {loss.item()}, Betas: {betas.detach().numpy()}")

    # Đảm bảo `betas` có đúng shape (1, 10)
    betas = betas.detach()  # Loại bỏ requires_grad

    # Pose mặc định (người đứng thẳng, không cử động)
    pose = torch.zeros(1, 63, dtype=torch.float32)

    return betas, pose

def display_3d_model(vertices, faces):
    """
    Hiển thị mô hình 3D từ tọa độ đỉnh (`vertices`) và mặt (`faces`).
    """
    mesh = trimesh.Trimesh(vertices=vertices, faces=faces)
    mesh.show()

# Ví dụ số đo thực tế
body_length = {
    "height": 160,  # Chiều cao tổng thể (cm)
    "arm": 65,  # Chiều dài tay (cm)
    "shoulder": 45,  # Chiều rộng vai (cm)
    "leg": 90  # Chiều dài chân (cm)
}

body_measurements = {
    "chest": 75,  # Vòng ngực (cm)
    "waist": 95,  # Vòng eo (cm)
    "hip": 100  # Vòng mông (cm)
}

# Gọi hàm tối ưu bằng Adam
betas, pose = smpl_joints_to_parameters(smplx_model, body_length, body_measurements)

print("🔥 Betas tối ưu:", betas)

# Sửa lỗi `RuntimeError`: Đảm bảo betas có đúng số chiều (1, 10)
if betas.dim() == 2 and betas.shape[0] == 1:
    betas = betas.squeeze(0)  # Chuyển từ (1, 10) thành (10,)

# Kiểm tra nếu mô hình yêu cầu `expression`
expression = torch.zeros(1, 10, dtype=torch.float32)  # Biểu cảm khuôn mặt (SMPL-X cần điều này)

# Chạy mô hình với `betas`, `pose`, và `expression`
output = smplx_model.forward(betas=betas.unsqueeze(0), body_pose=pose, expression=expression)

# Hiển thị mô hình 3D sau khi tối ưu
vertices = output.vertices.detach().cpu().numpy().squeeze()
display_3d_model(vertices, smplx_model.faces)
