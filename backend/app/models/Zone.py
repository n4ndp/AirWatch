from app import db
from app.models.enums.ZoneStatus import ZoneStatus

class Zone(db.Model):
    __tablename__ = "zones"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)
    location = db.Column(db.String(100), nullable=True)
    area = db.Column(db.Float, nullable=True)
    status = db.Column(db.Enum(ZoneStatus), nullable=False, default=ZoneStatus.ENABLED)

    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id", ondelete="CASCADE"), nullable=False, unique=True)
    fan_id = db.Column(db.Integer, db.ForeignKey("fans.id"), nullable=False, unique=True)
    
    sensor = db.relationship("Sensor", back_populates="zone", lazy="joined")
    fan = db.relationship("Fan", back_populates="zone", lazy="joined")

    alerts = db.relationship("Alert", back_populates="zone", cascade="all, delete-orphan")
