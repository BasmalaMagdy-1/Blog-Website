from werkzeug.security import generate_password_hash, check_password_hash
from app.db import db


def register_user_service(username, password):
    existing_user = User.query.filter_by(username=username).first()
    if existing_user:
        return {'success': False, 'message': 'Username already exists.'}

    hashed_password = generate_password_hash(password)
    new_user = User(username=username, password=hashed_password, role='Reader')  # Default role
    db.session.add(new_user)
    db.session.commit()

    return {'success': True}



from app.models.user import User

# def login_user_service(username, password):
#     user = User.query.filter_by(username=username).first()
#
#     if user and check_password_hash(user.password, password):
#         return user
#     return None
from werkzeug.security import check_password_hash

def login_user_service(username, password):
    user = User.query.filter_by(username=username).first()
    if user:
        # Debugging output to help trace the logic without exposing passwords
        print(f"Found user: {user.username}, comparing passwords.{user.password},{password}")
        if check_password_hash(user.password, password):  # Correct usage of password check
            return user
        else:
            print("Password does not match.")
    else:
        print("User not found.")
    return None




def create_user(username, email, password):
    hashed_password = generate_password_hash(password)
    new_user = User(username=username, email=email, password=hashed_password)

    try:
        db.session.add(new_user)
        db.session.commit()
        return new_user
    except Exception as e:
        db.session.rollback()  # Roll back in case of any error
        print(f"Error creating user: {e}")
        return None