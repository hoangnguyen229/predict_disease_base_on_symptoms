import pandas as pd
from sklearn import preprocessing

# Đọc dữ liệu training
training = pd.read_csv('./Data/Training.csv')

# Lấy danh sách các bệnh duy nhất từ cột 'prognosis'
diseases = training['prognosis'].unique()

# Tạo LabelEncoder để chuyển đổi tên bệnh thành ID
le = preprocessing.LabelEncoder()
le.fit(diseases)

# Tạo dictionary map giữa ID và tên bệnh
disease_mapping = {}
for disease in diseases:
    disease_id = le.transform([disease])[0]
    disease_mapping[disease_id] = disease

# Sắp xếp theo ID và in ra kết quả
print("Danh sách bệnh và ID tương ứng:")
print("-" * 50)
print("ID  | Tên bệnh")
print("-" * 50)
for disease_id in sorted(disease_mapping.keys()):
    print(f"{disease_id:<4}| {disease_mapping[disease_id]}")

# Lưu mapping vào file JSON để sử dụng sau này
import json
with open('disease_mapping.json', 'w') as f:
    json.dump(disease_mapping, f, indent=2)

print("\nĐã lưu mapping vào file 'disease_mapping.json'")