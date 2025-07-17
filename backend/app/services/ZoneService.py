from flask import abort
from app import db
from app.models.Zone import Zone
from app.models.Sensor import Sensor
from app.models.Fan import Fan
from app.models.enums.SensorStatus import SensorStatus
from app.models.enums.ZoneStatus import ZoneStatus
from app.models.enums.FanStatus import FanStatus
import random

def to_zone_full_info(zone):
    return {
        "id": zone.id,
        "name": zone.name,
        "location": zone.location,
        "area": zone.area,
        "status": zone.status.value,
        "sensor": {
            "id": zone.sensor.id,
            "serial_number": zone.sensor.serial_number,
            "status": zone.sensor.status.value
        },
        "fan": {
            "id": zone.fan.id,
            "serial_number": zone.fan.serial_number,
            "status": zone.fan.status.value
        }
    }

class ZoneService:
    
    @staticmethod
    def get_all_zones():
        zones = Zone.query.all()
        if not zones:
            abort(404, description="No zones found")

        return [to_zone_full_info(zone) for zone in zones]
    
    @staticmethod
    def get_zone(zone_id):
        zone = Zone.query.get_or_404(zone_id)
        if not zone:
            abort(404, message="Zone not found")
        
        return to_zone_full_info(zone)
    
    @staticmethod
    def create_zone(data):
        existing_sensor_zone = Zone.query.filter_by(sensor_id=data["sensor_id"]).first()
        if existing_sensor_zone:
            abort(400, description="Este sensor ya está asignado a otra zona")
            
        existing_fan_zone = Zone.query.filter_by(fan_id=data["fan_id"]).first()
        if existing_fan_zone:
            abort(400, description="Este ventilador ya está asignado a otra zona")
        
        sensor = Sensor.query.get_or_404(data["sensor_id"])
        fan = Fan.query.get_or_404(data["fan_id"])
        
        sensor.status = SensorStatus.ACTIVE
        
        location = f'{data["x"]} {data["y"]}'
        area = round(random.uniform(20.0, 100.0), 2)
        
        zone = Zone(
            name=data["name"],
            location=location,
            area=area,
            sensor=sensor,
            fan=fan,
        )
        
        db.session.add(zone)
        db.session.commit()
        
        return to_zone_full_info(zone)

    @staticmethod
    def update_zone(zone_id, data):
        zone = Zone.query.get_or_404(zone_id)
        if not zone:
            abort(404, message="Zone not found")
        
        if "name" in data:
            zone.name = data["name"]
        if "x" in data and "y" in data:
            zone.location = f'{data["x"]} {data["y"]}'
        if "sensor_id" in data:
            existing_sensor_zone = Zone.query.filter(
                Zone.sensor_id == data["sensor_id"],
                Zone.id != zone_id
            ).first()
            if existing_sensor_zone:
                abort(400, description="Este sensor ya está asignado a otra zona")

            sensor = Sensor.query.get_or_404(data["sensor_id"])
            sensor.status = SensorStatus.ACTIVE
            zone.sensor = sensor
        if "fan_id" in data:
            existing_fan_zone = Zone.query.filter(
                Zone.fan_id == data["fan_id"],
                Zone.id != zone_id
            ).first()
            if existing_fan_zone:
                abort(400, description="Este ventilador ya está asignado a otra zona")

            fan = Fan.query.get_or_404(data["fan_id"])
            zone.fan = fan
        if "status" in data:
            if data["status"].upper() == ZoneStatus.DISABLED.value:
                zone.status = ZoneStatus.DISABLED.value
                zone.sensor.status = SensorStatus.INACTIVE
                zone.fan.status = FanStatus.OFF.value
            elif data["status"].upper() == ZoneStatus.ENABLED.value:
                zone.status = ZoneStatus.ENABLED.value
                zone.sensor.status = SensorStatus.ACTIVE
  
        db.session.commit()
        
        return to_zone_full_info(zone)
    
    @staticmethod
    def delete_zone(zone_id):
        zone = Zone.query.get_or_404(zone_id)
        zone.sensor.status = SensorStatus.INACTIVE
        zone.fan.status = FanStatus.OFF.value
        db.session.delete(zone)
        db.session.commit()
