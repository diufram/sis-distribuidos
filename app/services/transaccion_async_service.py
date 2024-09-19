import threading
import queue
import uuid
from flask import jsonify, current_app
from app.services.transaccion_service import transaccion

# Cola de tareas
cola_tareas = queue.Queue()

def hilo():
    while True:
        try:
            print(cola_tareas.qsize())
            data = cola_tareas.get(timeout=100)
            
        except queue.Empty:
            continue

        if data is None:
            break
        
        # Asegúrate de que se ejecuta dentro del contexto de la aplicación
        try:
                #respuesta = transaccion(data=data['data'])
                print(cola_tareas.qsize())
        except Exception as e:
                print(f"Error al procesar la transacción: {e}")

        #cola_tareas.task_done()

def transaccion_asyn(datos):
    data = {
        "id": str(uuid.uuid4()),
        "data": datos,
        "proceso": "transaccion"
    }
    cola_tareas.put(data)

    respuesta = jsonify({"message": "Se está procesando su solicitud", "status": True}), 200
    return respuesta

def iniciar_hilo():
    print("Hilo Iniciado")
    threading.Thread(target=hilo, daemon=True).start()
