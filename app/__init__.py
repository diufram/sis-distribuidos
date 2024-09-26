from flask import Flask
from flask_migrate import Migrate
from flask_cors import CORS
from app.extensions import db, Session  # Importa db y Session
from app.routes import register_routes

migrate = Migrate()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)

    # Cargar la configuración de la aplicación
    app.config.from_object(config_class)

    # Inicializar la base de datos y migraciones utilizando la instancia de SQLAlchemy
    db.init_app(app)
    migrate.init_app(app, db)

    # Configura scoped_session dentro del contexto de la aplicación
    with app.app_context():
        Session.configure(bind=db.engine)

    # Configurar CORS para permitir solicitudes desde cualquier origen
    CORS(app, resources={r"/*": {"origins": "*"}})

    # Registrar las rutas de la aplicación
    register_routes(app)

    return app
