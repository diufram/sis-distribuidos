import threading
import uuid
import requests
import json
from flask import jsonify, current_app
from app.models import ColaRequest,ColaResponse
from app.extensions import get_session ,Session # Cambiar 'db' por get_session
from app.models.cola_request import obtener_primero_en_cola, eliminar_solicitud

from app.models.cola_response import obtener_primero_en_cola_response,eliminar_cola_response

from app.models.cola_response import verificar_transaccion_realizada,add_cola_response
hilos_activos = []
# hilo.py

def hilo_requests(app):
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
                    add_cola_response(session,request.nro_transaccion,data,"Ninguna", True,request.urlCallback)
                    eliminar_solicitud(request, session)
                    session.commit()
                except Exception as e:
                    add_cola_response(session,request.nro_transaccion,data,str(e), False,request.urlCallback)
                    eliminar_solicitud(request, session)
                    session.commit()
                  
            except Exception as e:
                session.rollback()
                
              
            finally:
                session.close()





def hilo_response(app):
    with app.app_context():
        while True:
            session = get_session()
            
            try:
                request = obtener_primero_en_cola_response(session)
                if request is None:
                    continue
                url = request.urlCallback
                data = {}
                if request.status == True:
                    monto = request.datos['monto']
                    if request.datos['tipo']== 1:
                        data = {
                            "nro_transaccion":request.nro_transaccion,
                            "message": f"Se realizó con éxito el Retiro de {monto}Bs."}
                    else:
                        data = {
                            "nro_transaccion":request.nro_transaccion,
                            "message":f"Se realizó con éxito el Deposito de {monto}Bs."}    
                else:
                    data = {
                        "nro_transaccion":request.nro_transaccion,
                        "message": request.error}
                    
                headers = {'Content-Type': 'application/json'}
                try: 
                    requests.post(url, data=json.dumps(data), headers=headers)
                    eliminar_cola_response(request,session)
                    session.commit()
                except Exception as e:
                    session.rollback()

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
        request = ColaRequest(nro_transaccion=nro_transaccion, datos=datos, urlCallback = datos['urlCallback'])
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
            "message": f"Ocurio un error Inesperado Intentelo Nuevamente",
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

    

def iniciar_hilo(tipo):
    if tipo == 1: #TIPO REQUEST
        print("HILO PARA PROCESAR INICIADO")
        nuevo_hilo = threading.Thread(target=hilo_requests, args=(current_app._get_current_object(),), daemon=True).start()
        #hilos_activos.append(nuevo_hilo)
    elif tipo == 2: #TIPO RESPONSE
        print("HILO PARA RESPONDER INICIADO")
        nuevo_hilo = threading.Thread(target=hilo_response, args=(current_app._get_current_object(),), daemon=True).start()
        #hilos_activos.append(nuevo_hilo)