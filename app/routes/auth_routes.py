from flask import Blueprint, request, jsonify

from core.security import SecurityService

login_bp = Blueprint("login", __name__, url_prefix="/login")


@login_bp.route("/", methods=["POST"])
def login():
    email = request.json.get("email")
    password = request.json.get("password")
    
    access_token = SecurityService.create_access_token(email)
    return jsonify(access_token=access_token), 200
