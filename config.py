# config.py
from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app = Flask(__name__)
    mongo_uri = (
        f"mongodb+srv://{os.getenv('MONGO_USER')}:{os.getenv('MONGO_PASSWORD')}"
        f"@{os.getenv('MONGO_HOST')}/{os.getenv('MONGO_DB')}?retryWrites=true&w=majority"
    )
    app.config["MONGO_URI"] = mongo_uri
    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
    
    mongo = PyMongo(app)
    return app, mongo
