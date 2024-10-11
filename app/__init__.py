from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

from .routes.auth import auth_bp
from .routes.user import user_bp
from .routes.blog import blog_bp  # Import the blog blueprint
from .routes.admin import admin_bp  # Import the blog blueprint
from app.models.user import User,Role  # Import User model from your models file

from app.db import db
# Initialize the database

login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('app.config.Config')

    db.init_app(app)  # Initialize the database with the app
    login_manager.init_app(app)

    @app.before_request
    def create_default_admin():
        with app.app_context():
            # Check if the admin user already exists
            admin_user = User.query.filter_by(username='admin').first()
            if admin_user:
                # If the admin user exists, delete it
                db.session.delete(admin_user)
                db.session.commit()
                print("Existing admin user deleted.")

            # Create a new admin user
            hashed_password = generate_password_hash('Admin123')
            admin_user = User(username='admin', email='admin@example.com', password=hashed_password, role=Role.ADMIN)
            db.session.add(admin_user)
            db.session.commit()
            print("Default admin user created.")

    # Register the blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp, url_prefix='/user')
    app.register_blueprint(blog_bp, url_prefix='/blog')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    # Register the blog blueprint

    return app

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))