from flask import Flask
from .config import Config
from .database import db
from .routes import bp
from datetime import datetime
from flask_cors import CORS

def create_app():
    # Inicializar la aplicación Flask
    app = Flask(__name__)
    
    CORS(app)
    
    app.config.from_object(Config)  # Configurar la base de datos desde config.py

    # Inicializar la base de datos con Flask
    db.init_app(app)

    with app.app_context():
        # Crear las tablas si no existen
        db.create_all()

        # Registrar las rutas
        app.register_blueprint(bp)

    return app
