from ..models.user import User
from app.db import db

def get_all_users():
    return User.query.all()

def promote_user_service(user_id):
    user = User.query.get(user_id)
    if user:
        user.role = 'Author'  # Change to Admin if necessary
        db.session.commit()
        return True
    return False

def delete_user_service(user_id):
    user = User.query.get(user_id)
    if user:
        db.session.delete(user)
        db.session.commit()
        return True
    return False
