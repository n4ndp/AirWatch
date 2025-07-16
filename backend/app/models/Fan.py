from app import db
from datetime import datetime, timezone
from app.models.enums.FanStatus import FanStatus

class Fan(db.Model):
    __tablename__ = "fans"
    __table_args__ = (
        db.UniqueConstraint("serial_number", name="uk_fans_serial_number"),
    )

    id = db.Column(db.Integer, primary_key=True)
    serial_number = db.Column(db.String(100), nullable=False)
    status = db.Column(db.String(20), nullable=False, default=FanStatus.OFF.value)
    purchase_date = db.Column(db.Date, nullable=False, default=datetime.now(timezone.utc))

    zone = db.relationship("Zone", back_populates="fan", uselist=False)
