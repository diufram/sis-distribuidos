from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS

db = SQLAlchemy()
migrate = Migrate()

def create_app(config_class='app.config.Config'):
    app = Flask(__name__)
  
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)

    # Configurar CORS para permitir todas las solicitudes
    CORS(app, resources={r"/*": {"origins": "*"}})

    from app.routes.user_routes import user_bp
    app.register_blueprint(user_bp, url_prefix='/users')

    return app
