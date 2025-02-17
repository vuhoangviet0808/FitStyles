import os
import json
import subprocess
import shutil
from ai_engine.config import OUTPUT_DIR, IMAGE_DIR, MODEL_OPENPOSE_DIR

MODEL_DIR = MODEL_OPENPOSE_DIR

#Ham chay openpose len tat ca file anh trong 1 folder
def run_openpose(image_path):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    image_folder = os.path.abspath(os.path.dirname(image_path))
    output_folder = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    
    command = [
        "docker", "run", "--rm",
        "-v", f"{image_folder}:/workspace/input",
        "-v", f"{output_folder}:/workspace/output",
        "-v", f"{MODEL_DIR}:/workspace/models",
        "mvdoc/openpose-cpu",
        "/openpose/build/examples/openpose/openpose.bin",
        "--image_dir", "/workspace/input",
        "--write_json", "/workspace/output/",
        "--write_images", "/workspace/output/",
        "--display", "0",
        "--net_resolution", "656x368",
        "--model_folder", "/workspace/models/"
    ]

    try:
        subprocess.run(command, check=True)
        print("✅ OpenPose đã xử lý xong!")
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi chạy OpenPose: {e}")

#Ham tim keypoints cua 1 anh
def get_keypoints_from_openpose(image_path, take_keypoints=False):
    base_name = os.path.splitext(os.path.basename(image_path))[0]
    image_folder = os.path.abspath(os.path.join(IMAGE_DIR, base_name))
    output_folder = os.path.abspath(os.path.join(OUTPUT_DIR, base_name))
    
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)


    old_keypoints_1 = os.path.join(output_folder, f"{base_name}_keypoints.json")
    # old_keypoints_2 = os.path.join(output_folder, f"{base_name}back_keypoints.json")
    
    new_keypoints_1 = os.path.join(output_folder, "front.json")
    # new_keypoints_2 = os.path.join(output_folder, "back.json")

    if not os.path.exists(new_keypoints_1): #or not os.path.exists(new_keypoints_2):
        run_openpose(image_path)

    if os.path.exists(old_keypoints_1):
        shutil.move(old_keypoints_1, new_keypoints_1)
    # if os.path.exists(old_keypoints_2):
    #     shutil.move(old_keypoints_2, new_keypoints_2)


    if not os.path.exists(new_keypoints_1): #or not os.path.exists(new_keypoints_2):
        print(f"❌ Không tìm thấy file keypoints cho ảnh {image_path}.")
        return None

    with open(new_keypoints_1, 'r') as f1: #, open(new_keypoints_2, 'r') as f2:
        keypoints_2d = json.load(f1)#, json.load(f2)]

    if take_keypoints:
        return keypoints_2d
    return new_keypoints_1#, new_keypoints_2





if __name__ == "__main__":
    image_path = "./storage/input/person2/person2.jpg"  
    keypoints = get_keypoints_from_openpose(image_path, False)
    if keypoints:
        print("✅ Keypoints 2D đã được lấy thành công!")
    else:
        print("❌ Không thể lấy keypoints từ ảnh!")
