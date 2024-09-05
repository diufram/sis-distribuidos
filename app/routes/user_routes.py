from sqlite3 import IntegrityError
from flask import Blueprint, request, jsonify
from app import db
from app.models import Usuario
from app.services.token_service import delete_token, generate_token, mark_token_as_used, store_token, verify_token, verify_token_exists
from app.models.redis_client import get_redis_client
user_bp = Blueprint('user', __name__)


@user_bp.route('/s', methods=['GET'])
def ejemplo():
    session = db.session
    try:
        data = {
            "ci": 9044956,
            "nombre": "Matias Franco",
            "apellido": "Ramos Limachi",
            "sexo": "Masculino"
        }

        # Generar el token
        token, expiration = generate_token(data)
        print(f"Token: {token}")
        print(f"Expiración del Token: {expiration}")

        # Verificar si el token ya existe
        token_status = verify_token_exists(token)
        if token_status:
            if token_status == 2:
                return jsonify({"message": "Se está procesando su solicitud"}), 200
            elif token_status == 0:
                print(f"Se borró el token porque se expiró: {delete_token(token)}")
                return jsonify({"message": "Su token expiró, intente nuevamente"}), 200
            elif token_status == 1:
                print(f"Se borró el token porque ya ha sido usado: {delete_token(token)}")
                return jsonify({"message": "Su token ya ha sido usado, intente más tarde"}), 200

        print("Se guardó el Token")
        store_token(token, expiration)

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            ci=data['ci'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            sexo=data['sexo']
        )

        # Agregar el nuevo usuario a la sesión
        session.add(nuevo_usuario)
        
        # Confirmar la transacción
        session.commit()

        mark_token_as_used(token)
        

        return jsonify({"message": "Usuario agregado exitosamente."}), 201

    except IntegrityError as e:
        session.rollback()
        print(f"Error de integridad: {e}")  # Registro del error en el log
        return jsonify({"message": "El usuario ya existe"}), 400

    except ValueError as e:
        session.rollback()
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        session.rollback()
        return jsonify({"message": "Error interno del servidor"}), 500

    finally:
        session.remove()  # Asegúrate de cerrar la sesión
        print(f"Se borró el token porque ya ha sido usado: {delete_token(token)}")
        print("Finalizó todo")

        
@user_bp.route('/pg')
def postgres_version():
    try:
        # Ejecuta una consulta para obtener la versión de PostgreSQL
        result = db.session.execute('SELECT * FROM YO;')
        version = result.fetchone()[0]
        return f'Versión de PostgreSQL: {version}'
    except Exception as e:
        return f'Error al obtener la versión de PostgreSQL: {e}'


