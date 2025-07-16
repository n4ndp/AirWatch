from app import db
from datetime import datetime, timezone
from app.models.enums.SensorStatus import SensorStatus

class Sensor(db.Model):
    __tablename__ = "sensors"
    __table_args__ = (
        db.UniqueConstraint("serial_number", name="uk_sensors_serial_number"),
    )

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=SensorStatus.INACTIVE.value)
    purchase_date = db.Column(db.Date, nullable=False, default=datetime.now(timezone.utc))

    zone = db.relationship("Zone", back_populates="sensor", uselist=False)

    readings = db.relationship("Reading", back_populates="sensor", cascade="all, delete-orphan")
