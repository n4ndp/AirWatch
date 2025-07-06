from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.UserService import UserService
from app.models.enums.UserRole import UserRole
from app.utils.Decorators import roles_required

user_bp = Blueprint("user_bp", __name__, url_prefix="/api/users")


@user_bp.route("/me", methods=["GET"])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_current_user():
    username = get_jwt_identity()
    profile = UserService.get_user_profile(username)
    return jsonify(profile), 200


@user_bp.route("/me", methods=["PUT"])
@jwt_required()
@roles_required(UserRole.USER)
def update_current_user():
    username = get_jwt_identity()
    data = request.get_json()
    updated_profile = UserService.update_profile(username, data)
    return jsonify(updated_profile), 200


@user_bp.route("", methods=["GET"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def get_all_users():
    users = UserService.get_all_users()
    return jsonify(users), 200


@user_bp.route("", methods=["POST"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def create_user():
    data = request.get_json()
    created_user = UserService.create_user(data)
    return jsonify(created_user), 201


@user_bp.route("/<string:username>", methods=["PUT"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def update_user(username):
    data = request.get_json()
    updated_user = UserService.update_user_by_admin(username, data)
    return jsonify(updated_user), 200


@user_bp.route("/delete/<string:username>", methods=["DELETE"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def delete_user(username):
    result = UserService.delete_user(username)
    return jsonify(result), 200
