from app import db
from datetime import datetime, timezone

class Reading(db.Model):
    __tablename__ = "readings"

    id = db.Column(db.Integer, primary_key=True)
    timestamp = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))
    co2 = db.Column(db.Float, nullable=False)

    sensor_id = db.Column(db.Integer, db.ForeignKey("sensors.id"), nullable=False)

    sensor = db.relationship("Sensor", back_populates="readings", lazy="joined")
    alert = db.relationship("Alert", back_populates="reading", uselist=False, cascade="all, delete-orphan")
