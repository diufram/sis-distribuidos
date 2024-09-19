import threading
import queue
import uuid
from flask import jsonify, current_app

# Cola de tareas global
cola_tareas = queue.Queue()
hilo_iniciado = False

def hilo(app):
    with app.app_context():  # Aseguramos que el hilo tiene acceso al contexto de la aplicación
        while True:
            try:
                data = cola_tareas.get(timeout=100)  # Obtiene tarea de la cola
            except queue.Empty:
                continue  # Si no hay tareas, sigue esperando

            if data is None:
                print(f"Salio del Hilo")
                break  # Salir del hilo si se envía None

            try:
                # Hacer la importación aquí para evitar el ciclo
                from app.services.transaccion_service import transaccion
                # Procesa la transacción
                transaccion(data['data'])
                print(f"Tarea {data['id']} procesada correctamente")
            except Exception as e:
                print(f"Error al procesar la transacción: {e}")

            cola_tareas.task_done()  # Marca la tarea como completada

def transaccion_asyn(datos):
    data = {
        "id": str(uuid.uuid4()),
        "data": datos,
        "proceso": "transaccion"
    }
    cola_tareas.put(data)  # Agrega la tarea a la cola

    respuesta = jsonify({"message": "Se está procesando su solicitud", "status": True}), 200
    return respuesta

def iniciar_hilo():
    global hilo_iniciado
    if not hilo_iniciado:
        print("Iniciando hilo...")
        hilo_iniciado = True
        # Pasamos la app actual al hilo
        threading.Thread(target=hilo, args=(current_app._get_current_object(),), daemon=True).start()
