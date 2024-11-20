from flask import Flask, request, jsonify
import pickle
import numpy as np
import pandas as pd
import json
import os

# Tạo ứng dụng Flask
app = Flask(__name__)

# Đọc danh sách symptom features từ file JSON
def load_symptom_features():
    try:
        # Lấy đường dẫn của thư mục hiện tại
        current_dir = os.path.dirname(os.path.abspath(__file__))
        # Đường dẫn đến file symptom_features.json
        json_path = os.path.join(current_dir, "symptom_features.json")
        
        with open(json_path, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        print("Không tìm thấy file symptom_features.json")
        return None
    except json.JSONDecodeError:
        print("Lỗi khi đọc file JSON. Kiểm tra lại định dạng của file.")
        return None

# Nạp danh sách symptom features
symptom_features = load_symptom_features()
if symptom_features is None:
    raise Exception("Không thể khởi động ứng dụng do không đọc được danh sách symptom features")

# Nạp mô hình
try:
    model_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "decision_tree_model.pkl")
    with open(model_path, "rb") as file:
        model = pickle.load(file)
except FileNotFoundError:
    print("Không tìm thấy file mô hình. Hãy kiểm tra lại đường dẫn đến file.")
    raise

@app.route('/predict', methods=['POST'])
def predict():
    # Nhận dữ liệu JSON từ yêu cầu POST
    data = request.get_json()
    symptoms = data.get("symptoms")

    # Kiểm tra độ dài của symptoms có khớp với số features không
    if len(symptoms) != len(symptom_features):
        return jsonify({
            "error": f"Số lượng features không khớp. Cần {len(symptom_features)} features nhưng nhận được {len(symptoms)} features"
        }), 400

    # Tạo DataFrame với tên các feature
    symptoms_df = pd.DataFrame([symptoms], columns=symptom_features)

    # Dự đoán bệnh
    prediction = model.predict(symptoms_df)

    # Trả về kết quả dự đoán dưới dạng số nguyên
    return jsonify({"predicted_disease": int(prediction[0])})

if __name__ == '__main__':
    app.run(debug=True)