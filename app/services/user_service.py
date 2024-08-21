from app.models import Usuario
from app import db

def create_user(nombre, email):
    nuevo_usuario = Usuario(nombre=nombre, email=email)
    db.session.add(nuevo_usuario)
    db.session.commit()
    return nuevo_usuario

def get_all_users():
    return Usuario.query.all()

def get_user_by_name(nombre):
    return Usuario.query.filter_by(nombre=nombre).first()
