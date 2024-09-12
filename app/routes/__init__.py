# app/routes/__init__.py
from flask import Flask

def register_routes(app: Flask):
    from .user_routes import user_bp
    from .person_routes import person_bp
    from .transaccion_routes import transaccion_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(person_bp, url_prefix='/persons')
    app.register_blueprint(transaccion_bp, url_prefix='/transaccion')
