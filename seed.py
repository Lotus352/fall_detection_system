import random
from datetime import datetime, timedelta
from config import create_app
from models import User, History
from flask_bcrypt import Bcrypt
from bson import ObjectId

app, mongo = create_app()
bcrypt = Bcrypt()

def create_sample_users():
    print("Creating sample users...")
    sample_users = [
        {"name": "Alice Nguyen", "email": "alice@example.com", "age": 70, "username": "alice", "password": "password123", "role": "user"},
        {"name": "Bob Tran", "email": "bob@example.com", "age": 65, "username": "bob", "password": "password123", "role": "user"},
        {"name": "Charlie Pham", "email": "charlie@example.com", "age": 75, "username": "charlie", "password": "password123", "role": "admin"},
    ]

    user_ids = []  # Danh sách lưu trữ user_id

    for user_data in sample_users:
        user_data["password"] = bcrypt.generate_password_hash(user_data["password"]).decode('utf-8')
        result = mongo.db.users.insert_one(user_data)
        user_ids.append(result.inserted_id)  # Lưu user_id sau khi tạo người dùng
    print("Sample users created.")
    return user_ids

def create_sample_histories(user_ids):
    print("Creating sample histories...")
    statuses = ["ngã", "không ngã"]
    
    for _ in range(30):  # Tạo 30 bản ghi lịch sử mẫu
        history_data = {
            "accelX": round(random.uniform(-2.0, 2.0), 2),
            "accelY": round(random.uniform(-2.0, 2.0), 2),
            "accelZ": round(random.uniform(9.5, 10.5), 2),
            "gyroX": round(random.uniform(-0.5, 0.5), 2),
            "gyroY": round(random.uniform(-0.5, 0.5), 2),
            "gyroZ": round(random.uniform(-0.5, 0.5), 2),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 10))).isoformat(),
            "status": random.choice(statuses),
            "user_id": random.choice(user_ids)  # Sử dụng user_id ngẫu nhiên
        }
        mongo.db.history.insert_one(history_data)
    print("Sample histories created.")

if __name__ == "__main__":
    with app.app_context():
        user_ids = create_sample_users()
        create_sample_histories(user_ids)
