from flask import Blueprint, request, jsonify

from schemas.user import UserCreate
from services.user import UserService, UserUpdate
from db.db_session import get_db
from utils.jwt_decorator import jwt_required

user_bp = Blueprint("user", __name__, url_prefix="/user")
session = next(get_db())


@user_bp.route('/<uuid:user_id>')
def get_user(user_id):
    user = UserService(session).get_user(user_id)
    
    return jsonify({
        "id": user.id,
        "email": user.email, 
        "role": user.role.value
    })
    
    
@user_bp.route('/all')
def get_all_users():
    users = UserService(session).get_all_users()
    users = [
        {
            "id": user.id,
            "email": user.email,
            "role": user.role.value
        } for user in users
    ]
    
    return jsonify(users)


@user_bp.route('/', methods=['POST'])
@jwt_required
def create_user():
    user_service = UserService(session)
    current_user = request.current_user
    user = user_service.create_user(
        UserCreate(**request.json), current_user
    )
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role.value
    })


@user_bp.route('/manager', methods=['POST'])
@jwt_required
def create_editor():
    user_service = UserService(session)
    current_user = request.current_user
    user = user_service.create_user_with_role_editor(
        UserCreate(**request.json), current_user
    )
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role.value
    })


@user_bp.route('/<uuid:user_id>', methods=['DELETE'])
@jwt_required
def delete_user(user_id):
    user_service = UserService(session)
    current_user = request.current_user
    user = user_service.delete_user(user_id, current_user)
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role.value
    })


@user_bp.route('/<uuid:user_id>', methods=['PUT'])
@jwt_required
def update_user(user_id):
    user_service = UserService(session)
    current_user = request.current_user
    user = user_service.update_user(user_id, UserUpdate(**request.json), current_user)
    
    return jsonify({
        "id": user.id,
        "email": user.email,
        "role": user.role.value
    })


@user_bp.route('/search')
def search_user():
    text = request.json.get('text')
    users = UserService(session).find_user_by_text(text)
    
    return jsonify([
        {
            "id": user.id,
            "email": user.email,
            "role": user.role.value
        } for user in users
    ])
