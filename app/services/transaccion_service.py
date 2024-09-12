from app import db
from app.models.cuenta_model import Cuenta
from app.models.user_model import Usuario
from app.models.transaccion_model import Transaccion
from flask import jsonify
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
import logging
from sqlalchemy import func

logging.basicConfig(level=logging.DEBUG, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filename='app.log',  # Guardar los logs en un archivo
                    filemode='a') 

def transaccion(data):
    try:
        logging.info("Iniciando transacción")  # Log de inicio

        if not data or not all(k in data for k in ('nroCuenta', 'tipo', 'monto', 'ciUsuario')):
            logging.warning("Faltan campos requeridos en la solicitud")  # Log de advertencia
            respuesta = jsonify({"message": "Todos los campos son requeridos", "status": False}), 400
            return respuesta

        tipo = data['tipo']
        nroCuenta = data['nroCuenta']
        monto = data['monto']
        ciUsuario = data['ciUsuario']

        logging.info(f"Datos de la transacción: tipo={tipo}, nroCuenta={nroCuenta}, monto={monto}, ciUsuario={ciUsuario}")

        if tipo == 1:  # Retiro
            logging.info("Iniciando retiro")
            if not hayfonndos(nroCuenta=nroCuenta, monto=monto):
                logging.warning("Fondos insuficientes para el retiro")  # Log de advertencia
                respuesta = jsonify({"message": "Fondos Insuficientes", "status": False}), 400
                return respuesta

            retiro(nroCuenta=nroCuenta, monto=monto)
            guardarTransaccion(nroCuenta=nroCuenta, ciUsuario=ciUsuario, monto=monto, tipo=tipo)
            logging.info("Retiro exitoso")  # Log de éxito
            respuesta = jsonify({"message": "Transaccion exitosa", "status": True}), 200
            return respuesta

        elif tipo == 0:  # Depósito
            logging.info("Iniciando depósito")
            deposito(nroCuenta=nroCuenta, monto=monto)
            guardarTransaccion(nroCuenta=nroCuenta, ciUsuario=ciUsuario, monto=monto, tipo=tipo)
            logging.info("Depósito exitoso")  # Log de éxito
            respuesta = jsonify({"message": "Transaccion exitosa", "status": True}), 200
            return respuesta

    except IntegrityError as e:
        db.session.rollback()
        logging.error(f"Error de integridad: {e}")  # Log de error
        respuesta = jsonify({"message": "El numero de transaccion ya exite", "status": False}), 409
        return respuesta

    except ValueError as e:
        db.session.rollback()
        logging.error(f"Error de valor: {e}")  # Log de error
        respuesta = jsonify({"message": "Error con los valores proporcionados", "status": False}), 400
        return respuesta

    except SQLAlchemyError as e:
        logging.error(f"Error en la base de datos: {e}")  # Log de error de SQL
        respuesta = jsonify({"message": "Error con la base de datos", "status": False}), 500
        return respuesta

    except Exception as e:
        logging.critical(f"Error interno del servidor: {e}")  # Log de error crítico
        respuesta = jsonify({"message": "Error interno del servidor", "status": False}), 500
        return respuesta

    finally:
        db.session.commit()
        db.session.remove()
        logging.info("Transacción finalizada y base de datos actualizada")  # Log final
    
    

def hayfonndos(nroCuenta, monto):
    saldo = db.session.query(Cuenta.saldo).filter_by(id = nroCuenta).scalar()
    if saldo >= monto:
        return True
    return False

def retiro(nroCuenta, monto):
    cuenta = db.session.query(Cuenta).filter(Cuenta.id == nroCuenta).first()
    cuenta.saldo = cuenta.saldo - monto
    db.session.commit()

def deposito(nroCuenta, monto):
    cuenta = db.session.query(Cuenta).filter(Cuenta.id == nroCuenta).first()
    cuenta.saldo = cuenta.saldo + monto
    db.session.commit()

def guardarTransaccion(nroCuenta,ciUsuario,monto,tipo):
    
    transaccion = Transaccion(
            ci_usuario= ciUsuario,
            id_cuenta= nroCuenta,
            tipo= tipo,
            monto=monto
        )
    db.session.add(transaccion)

def getAll():
    try:
        # Consultar los datos
        cis = db.session.query(Usuario.ci).all()
        cuentas = db.session.query(Cuenta.id).all()
        saldo_maximo = db.session.query(func.max(Cuenta.saldo)).scalar()
        saldo_minimo = db.session.query(func.min(Cuenta.saldo)).scalar()

        # Formatear los resultados para JSON
        cis_list = [ci[0] for ci in cis]  # Extraer valores de la tupla
        cuentas_list = [cuenta[0] for cuenta in cuentas]  # Extraer valores de la tupla

        # Crear la respuesta JSON
        respuesta = jsonify({
            "Usuarios": cis_list,
            "Cuentas": cuentas_list,
            "SaldoMax": saldo_maximo,
            "SaldoMin": saldo_minimo
        })
        return respuesta, 200
    except Exception as e:
        # Manejo de errores
        return jsonify({'error': str(e)}), 500



