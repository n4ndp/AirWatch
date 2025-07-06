from flask import Blueprint, request, jsonify
from app.services.AuthService import AuthService
import traceback

auth_bp = Blueprint("auth_bp", __name__, url_prefix="/api/auth")


@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        data = request.get_json(force=True)
        result = AuthService.register(data)
        return jsonify({"success": True, "message": "User registered successfully", "data": result}), 201
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), getattr(e, 'code', 500)


@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        data = request.get_json(force=True)
        result = AuthService.login(data)
        return jsonify({"success": True, "message": "Login successful", "data": result}), 200
    except Exception as e:
        traceback.print_exc()
        return jsonify({"success": False, "error": str(e)}), getattr(e, 'code', 500)
