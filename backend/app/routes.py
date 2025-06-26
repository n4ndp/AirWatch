from time import timezone
from flask import Blueprint, request, jsonify
from . import db
from .models import Sensor, Ventilator, Reading, Alert, Zone, Account, User
from datetime import datetime, timezone

bp = Blueprint('main', __name__)

# ===========================
# 1. Gestión de Sensores
# ===========================

# Obtener todos los sensores
@bp.route('/sensors', methods=['GET'])
def get_sensors():
    sensors = Sensor.query.all()
    return jsonify([{
        'id': sensor.id,
        'model': sensor.model,
        'purchase_date': sensor.purchase_date
    } for sensor in sensors])

# Obtener un sensor específico
@bp.route('/sensors/<sensor_id>', methods=['GET'])
def get_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    return jsonify({
        'id': sensor.id,
        'model': sensor.model,
        'purchase_date': sensor.purchase_date
    })

# Registrar un nuevo sensor
@bp.route('/sensors', methods=['POST'])
def add_sensor():
    data = request.json
    new_sensor = Sensor(
        model=data['model'],
        purchase_date=datetime.now(timezone.utc)
    )
    db.session.add(new_sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor added', 'sensor_id': new_sensor.id}), 201

# Actualizar un sensor
@bp.route('/sensors/<sensor_id>', methods=['PUT'])
def update_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    data = request.json
    sensor.model = data['model']
    db.session.commit()
    return jsonify({'message': 'Sensor updated'})

# Eliminar un sensor
@bp.route('/sensors/<sensor_id>', methods=['DELETE'])
def delete_sensor(sensor_id):
    sensor = Sensor.query.get_or_404(sensor_id)
    db.session.delete(sensor)
    db.session.commit()
    return jsonify({'message': 'Sensor deleted'})

# ===========================
# 2. Gestión de Ventiladores
# ===========================

# Obtener todos los ventiladores
@bp.route('/ventilators', methods=['GET'])
def get_ventilators():
    ventilators = Ventilator.query.all()
    return jsonify([{
        'id': ventilator.id,
        'model': ventilator.model,
        'purchase_date': ventilator.purchase_date
    } for ventilator in ventilators])

# Registrar un nuevo ventilador
@bp.route('/ventilators', methods=['POST'])
def add_ventilator():
    data = request.json
    new_ventilator = Ventilator(
        model=data['model'],
        purchase_date=datetime.now(timezone.utc)
    )
    db.session.add(new_ventilator)
    db.session.commit()
    return jsonify({'message': 'Ventilator added', 'ventilator_id': new_ventilator.id}), 201

# Obtener un ventilador específico
@bp.route('/ventilators/<ventilator_id>', methods=['GET'])
def get_ventilator(ventilator_id):
    ventilator = Ventilator.query.get_or_404(ventilator_id)
    return jsonify({
        'id': ventilator.id,
        'model': ventilator.model,
        'purchase_date': ventilator.purchase_date
    })

# Actualizar un ventilador
@bp.route('/ventilators/<ventilator_id>', methods=['PUT'])
def update_ventilator(ventilator_id):
    ventilator = Ventilator.query.get_or_404(ventilator_id)
    data = request.json
    ventilator.model = data['model']
    db.session.commit()
    return jsonify({'message': 'Ventilator updated'})

# Eliminar un ventilador
@bp.route('/ventilators/<ventilator_id>', methods=['DELETE'])
def delete_ventilator(ventilator_id):
    ventilator = Ventilator.query.get_or_404(ventilator_id)
    db.session.delete(ventilator)
    db.session.commit()
    return jsonify({'message': 'Ventilator deleted'})

# ===========================
# 3. Gestión de Zonas
# ===========================

# Obtener todas las zonas
@bp.route('/zones', methods=['GET'])
def get_zones():
    zones = Zone.query.all()
    return jsonify([{
        'id': zone.id,
        'sensor_id': zone.sensor_id,
        'ventilator_id': zone.ventilator_id,
        'x_coordinate': zone.x_coordinate,
        'y_coordinate': zone.y_coordinate,
        'floor': zone.floor,
        'operation_date': zone.operation_date,
        'description': zone.description
    } for zone in zones])

# Crear una zona
@bp.route('/zones', methods=['POST'])
def add_zone():
    data = request.json
    new_zone = Zone(
        sensor_id=data['sensor_id'],
        ventilator_id=data['ventilator_id'],
        x_coordinate=data['x_coordinate'],
        y_coordinate=data['y_coordinate'],
        floor=data['floor'],
        description=data['description'],
        operation_date=datetime.now(timezone.utc)
    )
    db.session.add(new_zone)
    db.session.commit()
    return jsonify({'message': 'Zone added', 'zone_id': new_zone.id}), 201

# Obtener una zona específica
@bp.route('/zones/<zone_id>', methods=['GET'])
def get_zone(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    return jsonify({
        'id': zone.id,
        'sensor_id': zone.sensor_id,
        'ventilator_id': zone.ventilator_id,
        'x_coordinate': zone.x_coordinate,
        'y_coordinate': zone.y_coordinate,
        'floor': zone.floor,
        'operation_date': zone.operation_date,
        'description': zone.description
    })

# Actualizar una zona
@bp.route('/zones/<zone_id>', methods=['PUT'])
def update_zone(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    data = request.json
    zone.x_coordinate = data['x_coordinate']
    zone.y_coordinate = data['y_coordinate']
    zone.floor = data['floor']
    zone.description = data['description']
    db.session.commit()
    return jsonify({'message': 'Zone updated'})

# Eliminar una zona
@bp.route('/zones/<zone_id>', methods=['DELETE'])
def delete_zone(zone_id):
    zone = Zone.query.get_or_404(zone_id)
    db.session.delete(zone)
    db.session.commit()
    return jsonify({'message': 'Zone deleted'})

# ===========================
# 4. Lecturas de Sensores
# ===========================

# Registrar una lectura
@bp.route('/readings', methods=['POST'])
def add_reading():
    data = request.json
    new_reading = Reading(
        sensor_id=data['sensor_id'],
        co2=data['co2'],
        temperature=data['temperature'],
        humidity=data['humidity'],
        timestamp=datetime.now(timezone.utc)
    )
    db.session.add(new_reading)
    db.session.commit()
    
    # Verificar alertas
    if data['co2'] > 1000:
        alert = Alert(
            reading_id=new_reading.id,
            sensor_id=data['sensor_id'],
            alert_type='highCO2',
            severity='critical',
            message='High CO2 level detected, activating ventilator.'
        )
        db.session.add(alert)
        db.session.commit()

        # Activar ventilador
        return jsonify({'message': 'Reading added and ventilator activated'}), 201
    
    return jsonify({'message': 'Reading added, no alert created'}), 201

# Obtener todas las lecturas
@bp.route('/readings', methods=['GET'])
def get_readings():
    readings = Reading.query.all()
    return jsonify([{
        'id': reading.id,
        'sensor_id': reading.sensor_id,
        'timestamp': reading.timestamp,
        'co2': reading.co2,
        'temperature': reading.temperature,
        'humidity': reading.humidity
    } for reading in readings])

# ===========================
# 5. Alertas
# ===========================

# Obtener todas las alertas
@bp.route('/alerts', methods=['GET'])
def get_alerts():
    alerts = Alert.query.all()
    return jsonify([{
        'id': alert.id,
        'sensor_id': alert.sensor_id,
        'alert_type': alert.alert_type,
        'severity': alert.severity,
        'message': alert.message,
        'created_at': alert.created_at
    } for alert in alerts])

# Crear una alerta manualmente
@bp.route('/alerts', methods=['POST'])
def create_alert():
    data = request.json
    new_alert = Alert(
        reading_id=data['reading_id'],
        sensor_id=data['sensor_id'],
        alert_type=data['alert_type'],
        severity=data['severity'],
        message=data['message']
    )
    db.session.add(new_alert)
    db.session.commit()
    return jsonify({'message': 'Alert created', 'alert_id': new_alert.id}), 201

# ===========================
# 6. Control de Ventiladores
# ===========================

# # Activar un ventilador
# @bp.route('/ventilators/<ventilator_id>/activate', methods=['POST'])
# def activate_ventilator(ventilator_id):
#     ventilator = Ventilator.query.get_or_404(ventilator_id)
#     # Aquí, en un caso real, enviarías una señal para activar el ventilador.
#     return jsonify({'message': f'Ventilator {ventilator_id} activated'}), 200

# # Desactivar un ventilador
# @bp.route('/ventilators/<ventilator_id>/deactivate', methods=['POST'])
# def deactivate_ventilator(ventilator_id):
#     ventilator = Ventilator.query.get_or_404(ventilator_id)
#     # Aquí, en un caso real, enviarías una señal para desactivar el ventilador.
#     return jsonify({'message': f'Ventilator {ventilator_id} deactivated'}), 200

# # Obtener el estado de todos los ventiladores
# @bp.route('/ventilators/status', methods=['GET'])
# def get_ventilator_status():
#     ventilators = Ventilator.query.all()
#     # Aquí deberías devolver el estado real de cada ventilador (encendido/apagado)
#     return jsonify([{'id': ventilator.id, 'model': ventilator.model, 'status': 'on/off'} for ventilator in ventilators])

# ===========================
# 1. Registrar un nuevo usuario
# ===========================

# @bp.route('/users/register', methods=['POST'])
# def register_user():
#     data = request.json
#     # Crear una cuenta (simple, sin encriptación de contraseñas)
#     new_account = Account(
#         full_name=data['full_name'],
#         email=data['email'],
#         role='viewer',  # Asignar un rol por defecto
#         registered_at=datetime.now(timezone.utc)
#     )
#     db.session.add(new_account)
#     db.session.commit()

#     # Crear el usuario asociado a la cuenta
#     new_user = User(
#         username=data['username'],
#         password=data['password'],
#         account_id=new_account.id
#     )
#     db.session.add(new_user)
#     db.session.commit()

#     return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201

@bp.route('/users/register', methods=['POST'])
def register_user():
    try:
        data = request.json
        new_account = Account(
            full_name=data['fullName'],
            email=data['email'],
            role='viewer',
            registered_at=datetime.now(timezone.utc)
        )
        db.session.add(new_account)
        db.session.commit()

        new_user = User(
            username=data['username'],
            password=data['password'],
            account_id=new_account.id
        )
        db.session.add(new_user)
        db.session.commit()

        return jsonify({'message': 'User registered successfully', 'user_id': new_user.id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ===========================
# 2. Iniciar sesión (Login básico)
# ===========================

# @bp.route('/users/login', methods=['POST'])
# def login_user():
#     data = request.json
#     user = User.query.filter_by(username=data['username'], password=data['password']).first()
    
#     if user:
#         return jsonify({'message': f'User {user.username} logged in successfully'}), 200
#     else:
#         return jsonify({'message': 'Invalid username or password'}), 401
@bp.route('/users/login', methods=['POST'])
def login_user():
    data = request.json
    user = User.query.filter_by(username=data['username'], password=data['password']).first()
    
    if user:
        # Obtener el rol de la cuenta asociada al usuario
        account = Account.query.get(user.account_id)
        
        # Retornar el mensaje con el rol
        return jsonify({
            'message': f'User {user.username} logged in successfully',
            'role': account.role  # Agregar el rol
        }), 200
    else:
        return jsonify({'message': 'Invalid username or password'}), 401

# ===========================
# 3. Obtener todos los usuarios
# ===========================

@bp.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': user.id,
        'username': user.username,
        'account_id': user.account_id
    } for user in users])

# ===========================
# 4. Obtener un usuario específico
# ===========================

@bp.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify({
        'id': user.id,
        'username': user.username,
        'account_id': user.account_id
    })

# ===========================
# 5. Actualizar usuario
# ===========================

@bp.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.json

    # Solo puedes actualizar algunos campos
    user.username = data['username']
    user.password = data['password']

    db.session.commit()
    return jsonify({'message': 'User updated successfully'})

# ===========================
# 6. Eliminar un usuario
# ===========================

@bp.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
