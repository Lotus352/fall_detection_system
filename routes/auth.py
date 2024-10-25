from flask import Blueprint, request, jsonify
from config import create_app
from models import User
from flask_bcrypt import Bcrypt
from bson import ObjectId

app, mongo = create_app()
bcrypt = Bcrypt(app)
auth_bp = Blueprint('auth', __name__)

# Đăng ký người dùng mới
@auth_bp.route('/register', methods=['POST'])
def register():
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
    return jsonify({"message": "User registered successfully", "id": str(result.inserted_id)}), 201

# Đăng nhập người dùng
@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = mongo.db.users.find_one({"username": data['username']})
    if user and bcrypt.check_password_hash(user['password'], data['password']):
        return jsonify({
            "message": "Login successful",
            "user_id": str(user['_id']),
            "role": user['role']  # Trả về role khi đăng nhập thành công
        }), 200
    return jsonify({"error": "Invalid username or password"}), 401
