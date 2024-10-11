from ..models.user import User
from app.db import db

def get_user_profile(user_id):
    return User.query.get(user_id)

def update_user_profile_service(username, email):
    user = User.query.filter_by(username=username).first()
    if user:
        user.email = email  # Assuming email is part of User model
        db.session.commit()
        return True
    return False
def get_all_users():

    return User.query.all()