from flask import Blueprint, request, jsonify
from config import create_app
from models import User
from bson import ObjectId

app, mongo = create_app()
users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['POST'])
def create_user():
    data = request.json
    # Kiểm tra trùng username hoặc email
    if mongo.db.users.find_one({"username": data['username']}):
        return jsonify({"error": "Username already exists"}), 400
    if mongo.db.users.find_one({"email": data['email']}):
        return jsonify({"error": "Email already exists"}), 400
    
    # Tạo người dùng mới
    user = User(
        name=data['name'],
        email=data['email'],
        age=data['age'],
        username=data['username'],
        password=data['password'],
        role=data.get('role', 'user')
    )
    result = mongo.db.users.insert_one(user.__dict__)
    return jsonify({"message": "User created successfully", "id": str(result.inserted_id)}), 201

# Lấy tất cả người dùng (không bao gồm password và role)
@users_bp.route('/users', methods=['GET'])
def get_all_users():
    users = list(mongo.db.users.find())
    for user in users:
        user['_id'] = str(user['_id'])
        user.pop('password', None)  # Loại bỏ password khỏi kết quả trả về
        user.pop('role', None)      # Loại bỏ role khỏi kết quả trả về
    return jsonify(users), 200

# Lấy thông tin người dùng theo ID (không bao gồm password và role)
@users_bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    if user:
        user['_id'] = str(user['_id'])
        user.pop('password', None)  # Loại bỏ password khỏi kết quả trả về
        user.pop('role', None)      # Loại bỏ role khỏi kết quả trả về
        return jsonify(user), 200
    return jsonify({"error": "User not found"}), 404

# Cập nhật thông tin người dùng theo ID, kiểm tra trùng lặp email và username
@users_bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.json
    
    # Kiểm tra nếu username hoặc email đã được sử dụng bởi người dùng khác
    if "username" in data:
        existing_user = mongo.db.users.find_one({"username": data['username'], "_id": {"$ne": ObjectId(user_id)}})
        if existing_user:
            return jsonify({"error": "Username already exists"}), 400
    if "email" in data:
        existing_user = mongo.db.users.find_one({"email": data['email'], "_id": {"$ne": ObjectId(user_id)}})
        if existing_user:
            return jsonify({"error": "Email already exists"}), 400
    
    # Cập nhật thông tin người dùng
    update_data = {
        "name": data.get('name'),
        "email": data.get('email'),
        "age": data.get('age'),
        "username": data.get('username')
    }
    update_data = {k: v for k, v in update_data.items() if v is not None}
    result = mongo.db.users.update_one({"_id": ObjectId(user_id)}, {"$set": update_data})
    
    # Trả về thành công ngay cả khi không có sự thay đổi
    if result.matched_count:
        return jsonify({"message": "User updated successfully"}), 200
    return jsonify({"error": "User not found"}), 404

# Xóa người dùng theo ID
@users_bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    result = mongo.db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count:
        return jsonify({"message": "User deleted successfully"}), 200
    return jsonify({"error": "User not found"}), 404
