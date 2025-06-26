from . import db
import uuid
from datetime import datetime

class Account(db.Model):
    __tablename__ = 'accounts'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(20), nullable=False)
    registered_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))

    users = db.relationship('User', backref='account', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    account_id = db.Column(db.String, db.ForeignKey('accounts.id'), nullable=False)

class Sensor(db.Model):
    __tablename__ = 'sensors'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)

class Ventilator(db.Model):
    __tablename__ = 'ventilators'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    model = db.Column(db.String(50), nullable=False)
    purchase_date = db.Column(db.DateTime, nullable=False)

class Zone(db.Model):
    __tablename__ = 'zones'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sensor_id = db.Column(db.String, db.ForeignKey('sensors.id'), nullable=False)
    ventilator_id = db.Column(db.String, db.ForeignKey('ventilators.id'), nullable=False)
    x_coordinate = db.Column(db.Float, nullable=False)
    y_coordinate = db.Column(db.Float, nullable=False)
    floor = db.Column(db.Integer, nullable=False)
    operation_date = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    description = db.Column(db.Text)

class Reading(db.Model):
    __tablename__ = 'readings'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    sensor_id = db.Column(db.String, db.ForeignKey('sensors.id'), nullable=False)
    timestamp = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
    co2 = db.Column(db.Float, nullable=False)
    temperature = db.Column(db.Float, nullable=False)
    humidity = db.Column(db.Float, nullable=False)

class Alert(db.Model):
    __tablename__ = 'alerts'
    id = db.Column(db.String, primary_key=True, default=lambda: str(uuid.uuid4()))
    reading_id = db.Column(db.String, db.ForeignKey('readings.id'), nullable=False)
    sensor_id = db.Column(db.String, db.ForeignKey('sensors.id'), nullable=False)
    alert_type = db.Column(db.String(20), nullable=False)
    severity = db.Column(db.String(20), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(datetime.timezone.utc))
