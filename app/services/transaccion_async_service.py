import threading
import uuid
from flask import jsonify, current_app
from app.models import ColaRequest,ColaResponse
from app.extensions import get_session ,Session # Cambiar 'db' por get_session
from app.models.cola_request import obtener_primero_en_cola, eliminar_solicitud
from app.models.cola_response import verificar_transaccion_realizada,add_cola_response
hilo_iniciado = False

# hilo.py

def hilo(app):
    with app.app_context():
        while True:
            session = get_session()
            try:
                request = obtener_primero_en_cola(session)
                if request is None:
                   
                    continue

                data = request.datos
                if data is None:
                    print("Salió del Hilo")
                    break

                from app.services.transaccion_service import transaccion
                try:
                    transaccion(session, data,request.nro_transaccion)
                    add_cola_response(session,request.nro_transaccion,data,"Ninguna", True)
                    eliminar_solicitud(request, session)
                    session.commit()
                except Exception as e:
                    add_cola_response(session,request.nro_transaccion,data,str(e), False)
                    eliminar_solicitud(request, session)
                    session.commit()
                  
            except Exception as e:
                session.rollback()
                
              
            finally:
                session.close()


def generar_nro_transaccion():
    # Generar un UUID y tomar solo los caracteres numéricos
    nro_transaccion = ''.join(filter(str.isdigit, str(uuid.uuid4())))
    # Limitarlo a una cantidad deseada de dígitos, por ejemplo 8
    return nro_transaccion[:8]



def transaccion_asyn(datos):
    nro_transaccion = generar_nro_transaccion()
    session = get_session()

    try:
        # Crear la nueva solicitud en la cola
        request = ColaRequest(nro_transaccion=nro_transaccion, datos=datos)
        session.add(request)
        session.commit()

        respuesta = jsonify({
            "nro_transaccion": nro_transaccion,
            "message": "Se está procesando su solicitud",
            "status": True
        }), 200
    except Exception as e:
        session.rollback()  # Revertir en caso de error
        respuesta = jsonify({
            "message": f"Error al procesar su solicitud: {e}",
            "status": False
        }), 500
    finally:
        Session.remove()  # Cerrar la sesión
    return respuesta

def verificacion(nro_transaccion):
    response =  verificar_transaccion_realizada(nro_transaccion=nro_transaccion)
  
    if response is None:
        return jsonify({
            "message":"Se esta Procesasando su Transaccion",
            "status": False}),200
    elif response.status:
        return jsonify({
            "message":"Se realizo correctamente su solicitud",
            "status": True}),200
    else:
        return jsonify({
            "message":response.error,
            "status": False}),200

    

def iniciar_hilo():
    global hilo_iniciado
    if not hilo_iniciado:
        print("Iniciando hilo...")
        hilo_iniciado = True
        threading.Thread(target=hilo, args=(current_app._get_current_object(),), daemon=True).start()
