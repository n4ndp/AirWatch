from app import db
from datetime import datetime, timezone

class Alert(db.Model):
    __tablename__ = "alerts"

    id = db.Column(db.Integer, primary_key=True)
    message = db.Column(db.String(255), nullable=False)
    co2 = db.Column(db.Float, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now(timezone.utc))

    reading_id = db.Column(db.Integer, db.ForeignKey("readings.id"), nullable=False)
    zone_id = db.Column(db.Integer, db.ForeignKey("zones.id"), nullable=False)

    reading = db.relationship("Reading", back_populates="alert", lazy="joined")
    zone = db.relationship("Zone", back_populates="alerts", lazy="joined")
