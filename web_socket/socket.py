from flask_socketio import SocketIO, emit

# Khởi tạo SocketIO
socketio = SocketIO(cors_allowed_origins="*")

# Xử lý khi ESP8266 kết nối tới WebSocket
@socketio.on('connect')
def handle_connect():
    print("ESP8266 đã kết nối!")
    emit('response', {'message': 'Kết nối thành công!'})

# Xử lý khi nhận dữ liệu từ ESP8266
@socketio.on('sensor_data')
def handle_sensor_data(data):
    print(f"Dữ liệu từ ESP8266: {data}")
    # Xử lý dữ liệu từ ESP8266, ví dụ: lưu vào cơ sở dữ liệu
    emit('response', {'message': 'Dữ liệu đã nhận!'})

# Xử lý khi ESP8266 ngắt kết nối
@socketio.on('disconnect')
def handle_disconnect():
    print("ESP8266 đã ngắt kết nối!")
