from flask import Blueprint, request, jsonify
from config import create_app
from models import History
from bson import ObjectId

app, mongo = create_app()
history_bp = Blueprint('history', __name__)

# Tạo bản ghi mới trong collection history
@history_bp.route('/history', methods=['POST'])
def create_history():
    data = request.json
    history = History(
        data['accelX'], data['accelY'], data['accelZ'],
        data['gyroX'], data['gyroY'], data['gyroZ'],
        data['timestamp'], data['status'], data['user_id'] 
    )
    result = mongo.db.history.insert_one(history.__dict__)
    return jsonify({"message": "History entry created successfully", "id": str(result.inserted_id)}), 201

# Lấy tất cả các bản ghi trong collection history
@history_bp.route('/history', methods=['GET'])
def get_all_history():
    histories = list(mongo.db.history.find())
    for history in histories:
        history['_id'] = str(history['_id'])
        history['user_id'] = str(history['user_id'])  # Chuyển user_id thành chuỗi
    return jsonify(histories), 200

# Lấy một bản ghi dựa trên ID
@history_bp.route('/history/<history_id>', methods=['GET'])
def get_history(history_id):
    history = mongo.db.history.find_one({"_id": ObjectId(history_id)})
    if history:
        history['_id'] = str(history['_id'])
        history['user_id'] = str(history['user_id'])  # Chuyển user_id thành chuỗi
        return jsonify(history), 200
    return jsonify({"error": "History not found"}), 404

# Lấy tất cả các bản ghi dựa trên user_id và sắp xếp theo thời gian sớm nhất lên trước
@history_bp.route('/history/user/<user_id>', methods=['GET'])
def get_history_by_user_id(user_id):
    # Truy vấn và sắp xếp theo `timestamp` tăng dần
    histories = list(mongo.db.history.find({"user_id": ObjectId(user_id)}).sort("timestamp", 1))
    for history in histories:
        history['_id'] = str(history['_id'])
        history['user_id'] = str(history['user_id'])  # Chuyển user_id thành chuỗi
    return jsonify(histories), 200