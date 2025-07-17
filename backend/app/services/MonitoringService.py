from flask import abort
from app import db
from app.models.Sensor import Sensor
from app.models.Fan import Fan
from app.models.Alert import Alert
from app.models.Reading import Reading
from app.models.Zone import Zone
from app.models.enums.ZoneStatus import ZoneStatus
from app.models.enums.SensorStatus import SensorStatus
from app.models.enums.FanStatus import FanStatus
from datetime import datetime, timezone
import random

UMBRAL_CO2 = 1000

def to_reading_dict(reading):
    return {
        "id": reading.id,
        "timestamp": reading.timestamp.isoformat() if reading.timestamp else None,
        "co2": reading.co2,
        "sensor_id": reading.sensor_id,
        "sensor_serial_number": reading.sensor.serial_number,
        "sensor_status": reading.sensor.status.value,
        "alert": {
            "id": reading.alert.id if reading.alert else None,
            "message": reading.alert.message if reading.alert else None,
            "co2": reading.alert.co2 if reading.alert else None,
            "created_at": reading.alert.created_at.isoformat() if reading.alert else None,
            "zone_id": reading.alert.zone_id if reading.alert else None
        } if reading.alert else None
    }
    
def to_alert_dict(alert):
    return {
        "id": alert.id,
        "message": alert.message,
        "co2": alert.co2,
        "created_at": alert.created_at.isoformat() if alert.created_at else None,
        "reading_id": alert.reading_id,
        "zone_id": alert.zone_id
    }

class MonitoringService:
    
    @staticmethod
    def get_all_sensors():
        sensors = Sensor.query.all()
        if not sensors:
            abort(404, description="No sensors found")
        return [sensor.to_dict() for sensor in sensors]
    
    @staticmethod
    def get_sensor(sensor_id):
        sensor = Sensor.query.get_or_404(sensor_id)
        return sensor.to_dict()
    
    @staticmethod
    def get_all_fans():
        fans = Fan.query.all()
        if not fans:
            abort(404, description="No fans found")
        return [fan.to_dict() for fan in fans]
    
    @staticmethod
    def get_fan(fan_id):
        fan = Fan.query.get_or_404(fan_id)
        return fan.to_dict()
    
    @staticmethod
    def get_all_readings():
        readings = Reading.query.all()
        if not readings:
            abort(404, description="No readings found")
        return [to_reading_dict(reading) for reading in readings]
    
    @staticmethod
    def get_readings(sensor_id):
        return [to_reading_dict(reading) for reading in Reading.query.filter_by(sensor_id=sensor_id).all()]
    
    @staticmethod
    def create_reading(data):
        sensor = Sensor.query.get_or_404(data["sensor_id"])

        reading = Reading(
            co2=data["co2"],
            sensor=sensor,
            timestamp=datetime.now(timezone.utc)
        )
        db.session.add(reading)
        db.session.flush()

        zone = Zone.query.filter_by(sensor_id=sensor.id).first()
        alert = None

        if zone and zone.fan:
            if reading.co2 > UMBRAL_CO2:
                zone.fan.status = FanStatus.ON
                alert = Alert(
                    message="Nivel de CO₂ elevado, activando ventilación",
                    co2=reading.co2,
                    reading=reading,
                    zone=zone
                )
                db.session.add(alert)
            else:
                zone.fan.status = FanStatus.OFF

        db.session.commit()

        return to_reading_dict(reading)

    @staticmethod
    def get_all_alerts():
        alerts = Alert.query.all()
        if not alerts:
            abort(404, description="No alerts found")
        return [to_alert_dict(alert) for alert in alerts]
    
    @staticmethod
    def get_alerts(zone_id):
        alert = Alert.query.filter_by(zone_id=zone_id).all()
        if not alert:
            abort(404, description="No alerts found for this zone")
        return [to_alert_dict(alert) for alert in alert]
    
    # Simulation
    @staticmethod
    def create_reading_simulation(data):
        base_sensor = Sensor.query.get_or_404(data["sensor_id"])

        if base_sensor.status != SensorStatus.ACTIVE:
            abort(400, description="Base sensor is not active")

        base_co2 = data["co2"]
        active_sensors = Sensor.query.filter(
            Sensor.status == SensorStatus.ACTIVE,
            Sensor.id != base_sensor.id
        ).all()

        created_readings = []

        base_reading = MonitoringService.create_reading({
            "sensor_id": base_sensor.id,
            "co2": base_co2
        })
        created_readings.append(base_reading)

        for sensor in active_sensors:
            simulated_co2 = round(base_co2 + random.uniform(-30, 30), 2)
            simulated_data = {
                "sensor_id": sensor.id,
                "co2": simulated_co2
            }
            reading = MonitoringService.create_reading(simulated_data)
            created_readings.append(reading)

        return {
            "message": "Simulated readings created successfully",
            "simulated_readings": created_readings
        }
