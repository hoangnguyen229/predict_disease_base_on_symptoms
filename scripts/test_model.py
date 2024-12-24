import requests
import json

# URL của API (giả sử đang chạy locally)
url = 'http://localhost:5000/predict'

# Tạo mảng symptoms với 132 phần tử (0 là không có triệu chứng, 1 là có triệu chứng)
symptoms = [0] * 132  # Khởi tạo tất cả triệu chứng là 0

# Giả lập một người bệnh có các triệu chứng:
# - sốt cao (high_fever)
# - ho (cough)
# - đau họng (throat_irritation)
# - sổ mũi (runny_nose)

# Mapping một số triệu chứng với vị trí index của chúng
symptom_indices = {
    'high_fever': 25,      # sốt cao
    'cough': 24,          # ho
    'throat_irritation': 51,  # đau họng
    'runny_nose': 54       # sổ mũi
}

# Đặt giá trị 1 cho các triệu chứng có mặt
for symptom in symptom_indices.values():
    symptoms[symptom] = 1

# Tạo payload cho request
payload = {
    "symptoms": symptoms
}

# Gửi POST request
try:
    response = requests.post(url, json=payload)
    
    # In ra status code và response
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
except requests.exceptions.RequestException as e:
    print(f"Error occurred: {e}")