from flask import jsonify
from flask_sqlalchemy import SQLAlchemy
from app.models.user import User,Role
from app import create_app
from app.db import db
app = create_app()

@app.route('/createdb', methods=['GET', 'POST'])
def create_db():
    with app.app_context():
        db.create_all()  # Creates all tables
    return jsonify({"message": "Database tables created!"}), 200
if __name__ == "__main__":
    app.run(debug=True)
