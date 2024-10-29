from flask import Blueprint, request, jsonify
import torch
import numpy as np
from model.models import load_model, load_scaler

# Định nghĩa blueprint cho API dự đoán
predict_bp = Blueprint('predict', __name__)

# Tải mô hình và scaler
model = load_model("model/mlp_model.pth")
scaler = load_scaler("model/scaler.pkl")

@predict_bp.route('/predict', methods=['POST'])
def predict():
    data = request.json.get('features', [])
    
    if len(data) != 6:
        return jsonify({"error": "Input data must contain 6 features (ax, ay, az, gx, gy, gz)"}), 400

    # Chuẩn hóa dữ liệu đầu vào
    data = np.array(data).reshape(1, -1)
    data = scaler.transform(data)
    data = torch.tensor(data, dtype=torch.float32)

    # Dự đoán
    with torch.no_grad():
        outputs = model(data)
        _, predicted = torch.max(outputs, 1)

    # Trả về kết quả dự đoán
    result = "Fall" if predicted.item() == 0 else "No Fall"
    return jsonify({"prediction": result})
