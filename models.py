from flask_bcrypt import Bcrypt
from bson import ObjectId 

bcrypt = Bcrypt()

class History:
    def __init__(self, accelX, accelY, accelZ, gyroX, gyroY, gyroZ, timestamp, status, user_id):
        self.accelX = accelX
        self.accelY = accelY
        self.accelZ = accelZ
        self.gyroX = gyroX
        self.gyroY = gyroY
        self.gyroZ = gyroZ
        self.timestamp = timestamp
        self.status = status
        self.user_id = ObjectId(user_id)

class User:
    def __init__(self, name, email, age, username, password, role="user"):
        self.name = name
        self.email = email
        self.age = age
        self.username = username
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.role = role
