from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import time
from app.utils.SeedData import seed_data

db = SQLAlchemy()
jwt = JWTManager()
cors = CORS(resources={r"/api/*": {"origins": "*"}})

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    db.init_app(app)
    jwt.init_app(app)
    cors.init_app(app)
    
    from app.models.User import User
    from app.models.Account import Account
    from app.models.Command import Command
    from app.models.Fan import Fan
    from app.models.Alert import Alert
    from app.models.Reading import Reading
    from app.models.Sensor import Sensor
    from app.models.Zone import Zone

    with app.app_context():
        time.sleep(6)
        try:
            db.create_all()
            time.sleep(2)
            seed_data()
        except Exception as e:
            print(f"Error: {e}")

    from app.routes.AuthController import auth_bp
    from app.routes.UserController import user_bp
    from app.routes.ZoneController import zone_bp
    from app.routes.MonitoringController import monitoring_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)
    app.register_blueprint(zone_bp)
    app.register_blueprint(monitoring_bp)

    return app
