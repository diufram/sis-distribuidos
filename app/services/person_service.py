from lxml import etree
from flask import jsonify
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from app import db
from app.models import Usuario 
import time
from app.services.token_service import generate_token, store_token, verify_token, delete_token,mark_token_as_used,verify_token_exists


def rest(data):
    session = db.session
    try:
         if not data or not all(k in data for k in ('ci', 'nombre', 'apellido', 'sexo')):
            return jsonify({"message": "Todos los campos son requeridos"}), 400
         
         token, expiration = generate_token(data)

         token_status = verify_token_exists(token)
         if token_status:
            if verify_token == 2:
                return jsonify({"message": "Se está procesando su solicitud"}), 200
            elif verify_token == 0:
                return jsonify({"message": "Su token expiró, intente nuevamente"}), 200
            elif verify_token == 1:
                return jsonify({"message": "Su token ya ha sido usado, intente más tarde"}), 200

         store_token(token, expiration)

         nuevo_usuario = Usuario(
            ci=data['ci'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            sexo=data['sexo']
         )
         session.add(nuevo_usuario)
         #time.sleep(2)
         session.commit()
         mark_token_as_used(token)
         respuesta = jsonify({"message": "Usuario agregado exitosamente."}), 201
         return respuesta

    except IntegrityError as e:
      session.rollback()
      respuesta = jsonify({"message": "El usuario ya existe"}), 200
      return respuesta
    
    except ValueError as e:
      session.rollback()
      respuesta = jsonify({"message": str(e)}), 400
      return respuesta
    
    except SQLAlchemyError as e:
      print(e)
      respuesta=  jsonify({"message": "Error en la conexion con la base de datos"}), 200
      return respuesta

    except Exception as e:
      session.rollback()
      respuesta = jsonify({"message": "Error interno del servidor"}), 500
      return respuesta

    finally:
      session.remove() 
      delete_token(token)