from flask import Blueprint, request, jsonify

from services.auth import AuthService
from services.user import UserService
from db.db_session import get_db

login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("/", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    if not email or not password:
        return jsonify({"message": "Email and password are required"}), 400
    user_service = UserService(next(get_db()))
    auth_service = AuthService(user_service)
    access_token = auth_service.login(email=email, password=password)
    if not access_token:
        return jsonify({"message": "Invalid credentials"}), 401
    return jsonify(access_token=access_token), 200
