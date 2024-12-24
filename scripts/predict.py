from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import json
import os
from datetime import datetime
from sklearn import preprocessing

# Tạo ứng dụng Flask
app = Flask(__name__)

# Đọc danh sách symptom features từ file JSON
def load_symptom_features():
    try:
        current_dir = os.path.dirname(os.path.abspath(__file__))
        json_path = os.path.join(current_dir, "../Data/symptom_features.json")
        
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Không tìm thấy file symptom_features.json")
        return None
    except json.JSONDecodeError:
        print("Lỗi khi đọc file JSON. Kiểm tra lại định dạng của file.")
        return None

# Tạo mapping disease ID to name
def create_disease_mapping():
    try:
        # Đọc dữ liệu training
        training = pd.read_csv('./Data/Training.csv')
        
        # Lấy danh sách các bệnh duy nhất
        diseases = training['prognosis'].unique()
        
        # Tạo LabelEncoder
        le = preprocessing.LabelEncoder()
        le.fit(diseases)
        
        # Tạo mapping
        disease_mapping = {}
        for disease in diseases:
            disease_id = le.transform([disease])[0]
            disease_mapping[int(disease_id)] = disease
            
        return disease_mapping
    except Exception as e:
        print(f"Lỗi khi tạo disease mapping: {str(e)}")
        return None

# Nạp danh sách symptom features
symptom_features = load_symptom_features()
if symptom_features is None:
    raise Exception("Không thể khởi động ứng dụng do không đọc được danh sách symptom features")

# Nạp disease mapping
disease_mapping = create_disease_mapping()
if disease_mapping is None:
    raise Exception("Không thể tạo được disease mapping")

# Nạp mô hình
try:
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../notebooks/decision_tree_model.pkl")
    with open(model_path, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("Không tìm thấy file mô hình. Hãy kiểm tra lại đường dẫn đến file.")
    raise

def log_request(request_data):
    """Ghi log request với timestamp"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print("\n" + "="*50)
    print(f"[{timestamp}] Nhận request mới")
    print("\nHeaders:")
    for header, value in request.headers:
        print(f"{header}: {value}")
    
    print("\nRequest Body:")
    print(json.dumps(request_data, indent=2))
    
    # Log các triệu chứng có giá trị 1 (các triệu chứng được chọn)
    if "symptoms" in request_data:
        active_symptoms = []
        for idx, value in enumerate(request_data["symptoms"]):
            if value == 1:
                active_symptoms.append(symptom_features[idx])
        
        print("\nCác triệu chứng được chọn:")
        for symptom in active_symptoms:
            print(f"- {symptom}")
    
    print("="*50 + "\n")

@app.route('/predict', methods=['POST'])
def predict():
    # Nhận dữ liệu JSON từ yêu cầu POST
    data = request.get_json()
    
    # Log request
    log_request(data)
    
    symptoms = data.get("symptoms")

    # Kiểm tra độ dài của symptoms
    if len(symptoms) != len(symptom_features):
        error_message = f"Số lượng features không khớp. Cần {len(symptom_features)} features nhưng nhận được {len(symptoms)} features"
        print(f"[ERROR] {error_message}")
        return jsonify({
            "error": error_message
        }), 400

    # Tạo DataFrame với tên các feature
    symptoms_df = pd.DataFrame([symptoms], columns=symptom_features)

    # Dự đoán bệnh
    predicted_disease = int(model.predict(symptoms_df)[0])
    
    # Lấy tên bệnh từ ID
    predicted_disease_name = disease_mapping.get(predicted_disease, "Unknown Disease")
    
    # Log kết quả dự đoán
    print(f"Kết quả dự đoán:")
    print(f"Disease ID: {predicted_disease}")
    print(f"Disease Name: {predicted_disease_name}")

    # Trả về kết quả dự đoán
    return jsonify({
        "predicted_disease": predicted_disease,
    })

if __name__ == '__main__':
    print("Starting Flask server...")
    print(f"Loaded {len(symptom_features)} symptom features")
    print(f"Loaded {len(disease_mapping)} diseases")
    print("\nDisease Mapping:")
    for disease_id, disease_name in sorted(disease_mapping.items()):
        print(f"ID {disease_id}: {disease_name}")
    app.run(debug=True)