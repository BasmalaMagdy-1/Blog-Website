import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from the .env file

class Config:
    FLASK_DEBUG = os.getenv("FLASK_DEBUG", default=True)
    SQLALCHEMY_DATABASE_URI = os.getenv("SQLALCHEMY_DATABASE_URI", default='sqlite:///database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Avoid warning from SQLAlchemy
    LOGIN_MANAGER_LOGIN_VIEW = 'auth.login'
    CREATE_DATABASE_IF_NOT_FOUND = os.getenv("CREATE_DATABASE_IF_NOT_FOUND", default=True)
    SECRET_KEY = os.getenv("SECRET_KEY", "a_very_secret_key")  # Change to something secure
    MONGO_URI = "mongodb://localhost:27017/myDatabase"


