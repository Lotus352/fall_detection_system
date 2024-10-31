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
        data['timestamp'], data['status'],
        data['latitude'], data['longitude']
    )
    result = mongo.db.history.insert_one(history.__dict__)
    return jsonify({"message": "History entry created successfully", "id": str(result.inserted_id)}), 201

# Lấy tất cả các bản ghi trong collection history với phân trang và lọc theo status
@history_bp.route('/history', methods=['GET'])
def get_all_history():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('per_page', 10))
    status = request.args.get('status')

    query = {}
    if status:
        query['status'] = status

    histories_cursor = mongo.db.history.find(query).sort('timestamp', -1).skip((page - 1) * per_page).limit(per_page)
    histories = list(histories_cursor)
    for history in histories:
        history['_id'] = str(history['_id'])
    return jsonify(histories), 200

# Lấy một bản ghi dựa trên ID
@history_bp.route('/history/<history_id>', methods=['GET'])
def get_history(history_id):
    history = mongo.db.history.find_one({"_id": ObjectId(history_id)})
    if history:
        history['_id'] = str(history['_id'])
        return jsonify(history), 200
    return jsonify({"error": "History not found"}), 404
