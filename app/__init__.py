from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import db  # Asegúrate de que la inicialización de la base de datos esté en extensions.py
from app.routes import register_routes
from app.services.transaccion_async_service import iniciar_hilo

migrate = Migrate()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
  
    # Cargar la configuración de la aplicación
    app.config.from_object(config_class)

    # Inicializar la base de datos y migraciones
    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS para permitir solicitudes desde cualquier origen
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Registrar las rutas de la aplicación
    register_routes(app=app)

    # Iniciar el hilo de procesamiento de tareas dentro del contexto de la aplicación
    with app.app_context():
        iniciar_hilo()

    return app
