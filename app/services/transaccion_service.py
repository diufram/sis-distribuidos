from app.extensions import db
from app.models.cuenta_model import Cuenta
from app.models.user_model import Usuario
from app.models.transaccion_model import Transaccion
from flask import jsonify

from sqlalchemy import func

import logging

# Configura el logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Ajusta el nivel de log a DEBUG o el que necesites

# Crea un manejador para el archivo de logs y establece el formato
log_file_path = 'transaccion.log'  # Archivo log en la raíz del proyecto
handler = logging.FileHandler(log_file_path)
handler.setLevel(logging.DEBUG)  # Ajusta el nivel de log a DEBUG o el que necesites
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)

# Agrega el manejador al logger
logger.addHandler(handler)

def transaccion(session, data,nro_transaccion):
    if not data or not all(k in data for k in ('nroCuenta', 'tipo', 'monto', 'ciUsuario')):
        logger.warning('Datos incompletos: %s', data)
        raise ValueError("Todos los campos son requeridos")

    tipo = data['tipo']
    nroCuenta = data['nroCuenta']
    monto = data['monto']
    ciUsuario = data['ciUsuario']

    if tipo == 1:  # Retiro
        if not hayfondos(session, nroCuenta=nroCuenta, monto=monto):
            logger.warning('Fondos insuficientes para cuenta %s con monto %s', nroCuenta, monto)
            raise ValueError("Fondos Insuficientes")
        retiro(session, nroCuenta=nroCuenta, monto=monto)
    elif tipo == 0:  # Depósito
        deposito(session, nroCuenta=nroCuenta, monto=monto)
    else:
        logger.warning('Tipo de transacción no válido: %s', tipo)
        raise ValueError("Tipo de transacción no válido")

    guardarTransaccion(session, nroCuenta=nroCuenta, ciUsuario=ciUsuario, monto=monto, tipo=tipo,nro_transaccion=nro_transaccion)
    logger.info('Transacción exitosa: cuenta %s, tipo %s, monto %s', nroCuenta, tipo, monto)

# Las funciones de retiro y depósito no deben hacer commit
def retiro(session, nroCuenta, monto):
    cuenta = session.query(Cuenta).filter(Cuenta.id == nroCuenta).first()
    cuenta.saldo -= monto

def deposito(session, nroCuenta, monto):
    cuenta = session.query(Cuenta).filter(Cuenta.id == nroCuenta).first()
    cuenta.saldo += monto


def hayfondos(session, nroCuenta, monto):
    saldo = session.query(Cuenta.saldo).filter_by(id=nroCuenta).scalar()
    return saldo >= monto


def guardarTransaccion(session, nroCuenta, ciUsuario, monto, tipo,nro_transaccion):
    transaccion = Transaccion(
        nro_transaccion=nro_transaccion,
        ci_usuario=ciUsuario,
        id_cuenta=nroCuenta,
        tipo=tipo,
        monto=monto
    )
    session.add(transaccion)


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



