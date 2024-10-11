from app.db import db
from flask_login import UserMixin

class Role:
    ADMIN = 'admin'
    AUTHOR = 'author'
    READER = 'reader'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    role = db.Column(db.String(10), default=Role.READER, nullable=False)

    def is_admin(self):
        return self.role == Role.ADMIN

    def is_author(self):
        return self.role == Role.AUTHOR
 # This is required by Flask-Login
    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)  # This is necessary for Flask-Login to recognize the user by ID