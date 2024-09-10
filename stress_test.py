import threading
import requests
import json
import time

# Configura el URL del endpoint de tu servidor Flask
url = 'http://127.0.0.1:5000/persons/rest'

# Función que realiza una solicitud POST al endpoint
def make_request():
    payload = {
        'ci': '12323782',
        'nombre': 'Nombre',
        'apellido': 'Apellido',
        'sexo': 'M'  # Puedes ajustar estos valores según sea necesario
    }
    headers = {'Content-Type': 'application/json'}
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    print(f"Status Code: {response.status_code}, Response: {response.json()}")

# Número de hilos y de repeticiones por hilo
num_threads = 10
num_requests_per_thread = 100

# Crea y arranca los hilos
threads = []
for i in range(num_threads):
    thread = threading.Thread(target=lambda: [make_request() for _ in range(num_requests_per_thread)])
    thread.start()
    threads.append(thread)

# Espera a que todos los hilos terminen
for thread in threads:
    thread.join()

print("Todas las solicitudes han sido enviadas.")
