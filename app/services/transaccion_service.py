from app import db
from app.models.cuenta_model import Cuenta
from app.models.user_model import Usuario
from app.models.transaccion_model import Transaccion
from flask import jsonify
from sqlalchemy.exc import IntegrityError,SQLAlchemyError
from sqlalchemy import func

def transaccion (data):
    try:
        if not data or not all(k in data for k in ('nroCuenta', 'tipo', 'monto','ciUsuario')):
            respuesta = jsonify({"message": "Todos los campos son requeridos", "status": False}), 400
            return respuesta
        tipo = data['tipo']
        nroCuenta = data['nroCuenta']
        monto = data['monto']
        ciUsuario = data['ciUsuario']
        

        if tipo == 1: #retiro

            if not hayfonndos(nroCuenta=nroCuenta, monto= monto):
                respuesta = jsonify({"message": "Fondos Insuficientes", "status": False}), 400
                return respuesta
            retiro(nroCuenta=nroCuenta,monto=monto)
            guardarTransaccion(nroCuenta=nroCuenta,ciUsuario=ciUsuario,monto=monto,tipo=tipo)
            respuesta = jsonify({"message": "Transaccion exitosa", "status": True}), 200
            return respuesta
        
        else: 

            if tipo == 0: #deposito
                deposito(nroCuenta=nroCuenta,monto=monto)
                guardarTransaccion(nroCuenta=nroCuenta,ciUsuario=ciUsuario,monto=monto,tipo=tipo)
                respuesta = jsonify({"message": "Transaccion exitosa", "status": True}), 200
                return respuesta
            
    except IntegrityError as e:
        db.session.rollback()
        respuesta = jsonify({"message": "El numero de transaccion ya exite", "status": False}), 409
        return respuesta
    
    except ValueError as e:
        db.session.rollback()
        
    except SQLAlchemyError as e:
        respuesta = jsonify({"message": "Error con la base de datos", "status": False}), 500
        return respuesta
    
    except Exception as e:
        print(f"Error: {e}")
        respuesta = jsonify({"message": "Error interno del servidor", "status": False}), 500
        return respuesta
        
    finally:
        db.session.commit()
        db.session.remove() 

    
    

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



