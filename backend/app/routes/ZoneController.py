from flask import Blueprint, jsonify, request
from flask_jwt_extended import jwt_required
from app.services.ZoneService import ZoneService
from app.models.enums.UserRole import UserRole
from app.utils.Decorators import roles_required

zone_bp = Blueprint("zone_bp", __name__, url_prefix="/api/zones")

@zone_bp.route("/", methods=["GET"])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_all_zones():
    zones = ZoneService.get_all_zones()
    return jsonify(zones), 200

@zone_bp.route("/<int:zone_id>", methods=["GET"])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_zone(zone_id):
    zone = ZoneService.get_zone(zone_id)
    return jsonify(zone), 200

@zone_bp.route("/", methods=["POST"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def create_zone():
    data = request.get_json()
    try:
        zone = ZoneService.create_zone(data)
        return jsonify(zone), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
    
@zone_bp.route("/<int:zone_id>", methods=["PUT"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def update_zone(zone_id):
    data = request.get_json()
    try:
        zone = ZoneService.update_zone(zone_id, data)
        return jsonify(zone), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@zone_bp.route("/<int:zone_id>/status", methods=["PUT"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def update_zone_status(zone_id):
    data = request.get_json()
    try:
        zone = ZoneService.update_zone(zone_id, data)
        return jsonify(zone), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@zone_bp.route("/<int:zone_id>", methods=["DELETE"])
@jwt_required()
@roles_required(UserRole.ADMIN)
def delete_zone(zone_id):
    try:
        ZoneService.delete_zone(zone_id)
        return jsonify({"message": "Zone deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400
