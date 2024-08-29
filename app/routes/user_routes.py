from flask import Blueprint, request, jsonify
from app.models.user_model import Usuario
from app import db
from app.services.token_service import generate_token, store_token, verify_token
from app.models.redis_client import get_redis_client
user_bp = Blueprint('user', __name__)

@user_bp.route('/submit', methods=['POST'])
def submit_form():
    data = request.json
    token = data.get('token')
    print(f"Token recibido: {token}")
    print(f"Verificación del token: {verify_token(token)}")

    # Verifica el token
    if not verify_token(token):
        return jsonify({"error": "Token inválido o ya utilizado"}), 400

    # Inserta los datos en la base de datos
    try:
        print("Procesando Informacion")
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Error al guardar el usuario en la base de datos", "details": str(e)}), 500

    # Marca el token como usado después de la inserción en la base de datos
    try:
        r = get_redis_client()
        r.set(token, 'used')  # Cambiamos el estado del token a 'used'
    except Exception as e:
        return jsonify({"error": "Error al actualizar el estado del token", "details": str(e)}), 500

    return jsonify({"message": "Usuario creado exitosamente"}), 200

@user_bp.route('/get-token', methods=['POST'])
def get_token():
    data = request.json

    # Verifica que 'data' sea un diccionario
    if not isinstance(data, dict):
        return jsonify({"error": "Datos inválidos, JSON no recibido"}), 400

    # Verifica que todos los campos necesarios estén presentes
    required_fields = ['nombre', 'ci', 'telefono', 'lugar_de_nacimiento']
    missing_fields = [field for field in required_fields if field not in data]
    if missing_fields:
        return jsonify({"error": f"Campos faltantes: {', '.join(missing_fields)}"}), 400

    try:
        token, expiration = generate_token(data)
        store_token(token, expiration)
        print(f"Token generado: {token}")
        return jsonify({"token": token}), 200
    except Exception as e:
        # Captura y muestra el error
        print(f"Error en get_token: {e}")
        return jsonify({"error": str(e)}), 500

