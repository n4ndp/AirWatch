from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import time

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

    with app.app_context():
        time.sleep(5)
        try:
            db.create_all()
            print("Database tables created successfully.")
        except Exception as e:
            print(f"Error creating database tables: {e}")

    from app.routes.AuthController import auth_bp
    from app.routes.UserController import user_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(user_bp)

    return app
