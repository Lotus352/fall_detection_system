from flask import Flask
from config import create_app
from routes.history import history_bp
from routes.users import users_bp
from routes.auth import auth_bp  

app, mongo = create_app()

app.register_blueprint(history_bp)
app.register_blueprint(users_bp)
app.register_blueprint(auth_bp)

if __name__ == '__main__':
    app.run(debug=True)
