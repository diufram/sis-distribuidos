from flask import Blueprint, request, jsonify
from app.services.user_service import create_user, get_all_users, get_user_by_name

user_bp = Blueprint('users', __name__)

@user_bp.route('/', methods=['GET'])
def list_users():
    usuarios = get_all_users()
    return jsonify([{'id': u.id, 'nombre': u.nombre, 'email': u.email} for u in usuarios])

@user_bp.route('/', methods=['POST'])
def add_user():
    data = request.get_json()
    nombre = data.get('nombre')
    email = data.get('email')
    usuario = create_user(nombre, email)
    return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email}), 201

@user_bp.route('/<nombre>', methods=['GET'])
def get_user(nombre):
    usuario = get_user_by_name(nombre)
    if usuario:
        return jsonify({'id': usuario.id, 'nombre': usuario.nombre, 'email': usuario.email})
    return jsonify({'message': 'Usuario no encontrado'}), 404
