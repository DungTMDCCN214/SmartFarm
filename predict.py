

import cv2
import numpy as np
import tensorflow as tf
import os

# Cấu hình Class Names và Model cho từng loại cây


PLANT_CONFIG = {
    "cam": {
        "model_path": r"F:/TTCS/APP/models/Cay_cam_model.keras",
        "class_names": [
            "Vang_la_gan_xanh",
            "benh_loet", 
            "la_khoe", 
            "thieu_dinh_duong"
            
        ]
    },
    "chanh": {
        "model_path": r"F:/TTCS/APP/models/Cay_chanh_model.keras",
        "class_names": [
            "La_khoe", 
            "La_vang_thoi_re", 
            "Lo_loet", 
            "dom_den"
        ]
    },
    "dua_hau": {
        "model_path": r"F:/TTCS/APP/models/Cay_dua_hau_model.keras",
        "class_names": [
            "Benh_suong_mai", 
            "Benh_than_thu", 
            "La_khoe_manh", 
            "virus_kham"
        ]
    },
    "le": {
        "model_path": r"F:/TTCS/APP/models/Cay_le_model.keras",
        "class_names": [
            "Chay_la", 
            "Dom_la", 
            "La_khoe", 
            "Sen_tran"
        ]
    },
    "oi": {
        "model_path": r"F:/TTCS/APP/models/Cay_oi_model.keras",
        "class_names": [
            "La_khoe", 
            "Loet", 
            "Than_thu", 
            "ri_sat"
        ]
    },
    "xoai": {
        "model_path": r"F:/TTCS/APP/models/Cay_xoai_model.keras",
        "class_names": [
            "Benh_loet_do_vi_khuan", 
            "Benh_phan_trang", 
            "Benh_than_thu", 
            "Bo_canh_cung_cat", 
            "Chet_dan", 
            "La_khoe", 
            "Nam_bo_hong", 
            "Ruoi_gay_u"
        ]
    },
    "thanh_long": {
        "model_path": r"F:/TTCS/APP/models/dragonfruit_model.keras",
        "class_names": [
            "benh_dom_den",
            "benh_dom_nau",
            "benh_thoi_re",
            "la_khoe_manh"
        ]
    },
    "buoi": {
        "model_path": r"F:/TTCS/APP/models/citrus_model.keras",
        "class_names": [
            "benh_dom_den",
            "benh_loet_vikhuan",
            "benh_vang_la_gan_xanh",
            "la_khoe_manh"
        ]
    },
    "vai": {
        "model_path": r"D:\DATASET\app phan loai\Keras_Models_Final\Lychee\lychee_model.keras",
        "class_names": [
            "benh_phan_trang",
            "benh_suong_mai",
            "benh_than_thu",
            "la_khoe_manh"
        ]
    }
}


# Biến toàn cục để lưu cache model
loaded_models = {}

def get_model(plant_type):
    """Load và cache model theo loại cây"""
    if plant_type not in PLANT_CONFIG:
        raise ValueError(f"Không hỗ trợ loại cây: {plant_type}")
        
    if plant_type not in loaded_models:
        path = PLANT_CONFIG[plant_type]["model_path"]
        if not os.path.exists(path):
            raise FileNotFoundError(f"Không tìm thấy model tại {path}")
            
        print(f"Loading model cho {plant_type}...")
        loaded_models[plant_type] = tf.keras.models.load_model(path, compile=False)        
    return loaded_models[plant_type]

def preprocess_image(image_path, target_size=(224, 224)):
    """Sử dụng OpenCV để đọc và tiền xử lý ảnh"""
    # Đọc ảnh bằng OpenCV
    img = cv2.imread(image_path)
    if img is None:
        raise ValueError("Không thể đọc ảnh. Kiểm tra lại đường dẫn.")
        
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    img = cv2.resize(img, target_size)
    
    img = img.astype('float32') / 255.0

    img = np.expand_dims(img, axis=0)
    
    return img

def predict_disease(image_path, plant_type):
    """Hàm chính để dự đoán bệnh"""
    try:
        # 1. Đọc và tiền xử lý ảnh
        processed_img = preprocess_image(image_path)
        
        # 2. Load model
        model = get_model(plant_type)
        class_names = PLANT_CONFIG[plant_type]["class_names"]
        
        # --- BẮT ĐẦU ĐOẠN IN DEBUG ---
        print("\n--- DEBUG INFO ---")
        print("1. Hình dáng ảnh:", processed_img.shape) 
        print("2. Vài pixel đầu tiên:", processed_img[0][0][0]) 
        # --- KẾT THÚC ĐOẠN IN DEBUG ---

        # 3. Dự đoán
        predictions = model.predict(processed_img)
        
        # In nốt tỉ lệ % để xem AI đang thiên vị bệnh nào
        print("3. Tỉ lệ % AI phán đoán:", predictions[0]) 
        print("------------------\n")
        
        # 4. Trích xuất kết quả
        predicted_class_index = np.argmax(predictions[0])
        confidence = float(predictions[0][predicted_class_index])
        disease_name = class_names[predicted_class_index]
        
        return {
            "status": "success",
            "plant_type": plant_type,
            "disease": disease_name,
            "confidence": confidence
        }
        
    except Exception as e:
        return {
            "status": "error",
            "message": str(e)
        }
# if __name__ == "__main__":
#     # Giả sử bạn có một tấm ảnh test
#     test_image = r"F:\Benh_loai_cay\Cay_cam\la_khoe_manh\flipped_horizontal_IMG_20230630_192958.jpg"

#     kq = predict_disease(test_image, "cam")
#     print(kq)