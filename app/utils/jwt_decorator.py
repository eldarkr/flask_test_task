from flask import request, jsonify
from functools import wraps

from services.user import UserService
from services.auth import AuthService
from db.db_session import get_db

session = next(get_db())


def jwt_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.headers.get("Authorization")
        if not token or not token.startswith("Bearer "):
            return jsonify({"error": "Missing or invalid token"}), 401
        token = token.split("Bearer ")[1]
        user_service = UserService(session)
        current_user = AuthService(user_service).get_current_user_by_token(token)
        if not current_user:
            return jsonify({"error": "Unauthorized"}), 401
        request.current_user = current_user
        return func(*args, **kwargs)
    return wrapper
