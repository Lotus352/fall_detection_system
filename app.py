from flask import Flask
from config import create_app
from routes.history import history_bp
from routes.users import users_bp
from routes.auth import auth_bp  
from routes.predict import predict_bp
from web_socket.socket import socketio  # Import SocketIO từ file socket.py

app, mongo = create_app()

app.register_blueprint(history_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(predict_bp)

if __name__ == '__main__':
    socketio.init_app(app)  # Khởi động WebSocket với ứng dụng Flask
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)  # Chạy ứng dụng với WebSocket
