# app/routes/__init__.py
from flask import Flask

def register_routes(app: Flask):
    from .user_routes import user_bp
    from .person_routes import person_bp

    app.register_blueprint(user_bp, url_prefix='/users')
    app.register_blueprint(person_bp, url_prefix='/persons')
