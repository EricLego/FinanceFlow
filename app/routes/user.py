from flask import Blueprint, request, jsonify
from app.config.config import get_db_connection
from app.models.user import User
from datetime import datetime

user_bp = Blueprint('user', __name__)

@user_bp.route('/user/create', methods=['POST'])
def create_user():
    db_session = get_db_connection()
    try:
        data = request.get_json()

        # Validate required fields
        required_fields = ["first_name", "last_name", "email", "password", "role"]
        for field in required_fields:
            if not data.get(field):
                return jsonify({"message": f"Missing or empty field: {field}"}), 400

        # Check for duplicate email
        existing_user = db_session.query(User).filter_by(email=data["email"]).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        password = data.get("password")
        if not password:
            return jsonify({"message": "Password is required"}), 400

        hashed_password = User.hash_password(password)

        # Convert string dates to datetime.date
        def parse_date(date_str):
            return datetime.strptime(date_str, "%Y-%m-%d").date() if date_str else None

        new_user = User(
            first_name=data["first_name"],
            last_name=data["last_name"],
            email=data["email"],
            password_hash=hashed_password,
            role=int(data["role"]),
            birth_date=parse_date(data.get("birth_date")),
            hire_date=parse_date(data.get("hire_date")),
            suspend_start=parse_date(data.get("suspend_start")),
            suspend_end=parse_date(data.get("suspend_end")),
            status=True
        )

        db_session.add(new_user)
        db_session.commit()

        return jsonify({"message": "User created successfully"}), 201

    except Exception as e:
        print(f"ERROR: {str(e)}")
        db_session.rollback()
        return jsonify({"message": f"Internal Server Error: {str(e)}"}), 500
    finally:
        db_session.close()
