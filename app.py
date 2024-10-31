from flask import Flask, request, jsonify
from routes.history import history_bp
from routes.predict import model, scaler
from flask_cors import CORS
from flask_sock import Sock
import numpy as np
import torch
import pandas as pd
from datetime import datetime, timezone
from bson import ObjectId
import pymongo
from config import create_app

# Khởi tạo ứng dụng Flask và MongoDB từ create_app
app, mongo = create_app()

# Khởi tạo WebSocket
sock = Sock(app)

# Cho phép CORS cho tất cả các nguồn gốc
CORS(app, resources={r"/*": {"origins": "*"}})

# Đăng ký blueprint cho route lịch sử
app.register_blueprint(history_bp)

# Route WebSocket để nhận dữ liệu và thực hiện dự đoán
@sock.route('/websocket')
def websocket(ws):
    while True:
        data = ws.receive()
        print(f"data: {data}")
        if data:
            try:
                # Tách phần tọa độ GPS và phần dữ liệu cảm biến
                try:
                    gps_data, sensor_data = data.split("|")
                    latitude, longitude = [float(value.strip()) for value in gps_data.split(",")]
                    features = [float(value.strip()) for value in sensor_data.split(",")]
                except ValueError:
                    ws.send("Error: Input data format is incorrect. Expected format: latitude,longitude|accelX,accelY,accelZ,gyroX,gyroY,gyroZ")
                    continue
                
                # Kiểm tra số lượng đặc trưng
                if len(features) != 6:
                    ws.send("Error: Input sensor data must contain 6 features (accelX, accelY, accelZ, gyroX, gyroY, gyroZ)")
                    continue
                
                # Tạo DataFrame từ dữ liệu cảm biến
                features_df = pd.DataFrame([features], columns=['accelX', 'accelY', 'accelZ', 'gyroX', 'gyroY', 'gyroZ'])
                features_scaled = scaler.transform(features_df)
                features_tensor = torch.from_numpy(features_scaled).float()

                # Thực hiện dự đoán
                with torch.no_grad():
                    outputs = model(features_tensor)
                    _, predicted = torch.max(outputs, 1)
               
                # Kết quả dự đoán
                result = "fall" if predicted.item() == 0 else "nofall"
                
                # Lưu lịch sử với tọa độ GPS và trạng thái dự đoán
                history_entry = {
                    "accelX": features[0],
                    "accelY": features[1],
                    "accelZ": features[2],
                    "gyroX": features[3],
                    "gyroY": features[4],
                    "gyroZ": features[5],
                    "latitude": latitude,
                    "longitude": longitude,
                    "timestamp": datetime.now(timezone.utc),  # Sử dụng datetime.now(timezone.utc) thay cho utcnow()
                    "status": result
                }
                mongo.db.history.insert_one(history_entry)
                
                # Gửi dữ liệu trở lại client
                response_data = f"{latitude},{longitude}|{sensor_data}|{result}"
                print(f"response_data: {response_data}")
                ws.send(response_data)
            except Exception as e:
                ws.send(f"Error: {str(e)}")

# Khởi động ứng dụng
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=81, debug=True)
