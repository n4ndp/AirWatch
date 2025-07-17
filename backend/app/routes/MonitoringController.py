from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app.services.MonitoringService import MonitoringService
from app.models.enums.UserRole import UserRole
from app.utils.Decorators import roles_required

monitoring_bp = Blueprint('monitoring', __name__, url_prefix="/api/monitoring")

@monitoring_bp.route('/sensors', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_all_sensors():
    return jsonify(MonitoringService.get_all_sensors())

@monitoring_bp.route('/sensors/<int:sensor_id>', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_sensor(sensor_id):
    return jsonify(MonitoringService.get_sensor(sensor_id))

@monitoring_bp.route('/fans', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_all_fans():
    return jsonify(MonitoringService.get_all_fans())

@monitoring_bp.route('/fans/<int:fan_id>', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_fan(fan_id):
    return jsonify(MonitoringService.get_fan(fan_id))

@monitoring_bp.route('/readings', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_all_readings():
    return jsonify(MonitoringService.get_all_readings())

@monitoring_bp.route('/readings/<int:sensor_id>', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_readings(sensor_id):
    return jsonify(MonitoringService.get_readings(sensor_id))

@monitoring_bp.route('/readings', methods=['POST'])
def create_reading():
    data = request.get_json()
    return jsonify(MonitoringService.create_reading(data)), 201

@monitoring_bp.route('/alerts', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_all_alerts():
    return jsonify(MonitoringService.get_all_alerts())

@monitoring_bp.route('/alerts/<int:zone_id>', methods=['GET'])
@jwt_required()
@roles_required(UserRole.USER, UserRole.ADMIN)
def get_alerts(zone_id):
    return jsonify(MonitoringService.get_alerts(zone_id))

# Simulation
@monitoring_bp.route('/simulate', methods=['POST'])
def simulate_readings():
    data = request.get_json()
    if not data or "sensor_id" not in data or "co2" not in data:
        return jsonify({"error": "Missing 'sensor_id' or 'co2' in request body"}), 400
    return jsonify(MonitoringService.create_reading_simulation(data)), 201
