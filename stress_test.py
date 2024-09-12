import threading
import requests
import json
import time
import random

# Configura el URL del endpoint de tu servidor Flask
url = 'http://127.0.0.1:5000/transaccion/transaccion'
def getAll():
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get("http://127.0.0.1:5000/transaccion/getall", headers=headers)
        
        #print(f"Status Code: {response.status_code}, Response: {response.json()}")
        return response.json()
    except requests.RequestException as e:
        print(f"Error: {e}")

# Función que realiza una solicitud POST al endpoint
def make_request(nroCuenta, tipo, monto, ciUsuario):
    payload = {
        "nroCuenta": nroCuenta,
        "tipo": tipo,
        "monto": monto,
        "ciUsuario": ciUsuario
    }
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.post(url, data=json.dumps(payload), headers=headers)
        print(f"Status Code: {response.status_code}, Response: {response.json()}")
    except requests.RequestException as e:
        print(f"Error: {e}")

# Función que ejecuta solicitudes indefinidamente

def thread_function(cuentas,saldo_maximo,saldo_minimo,usuarios):
    
    while True:
        cuenta_aleatoria = random.choice(cuentas)
        usuario_aleatorio = random.choice(usuarios)
        monto_aleatorio = random.uniform(saldo_minimo, saldo_maximo)
        numero_aleatorio = random.choice([0, 1])
        make_request(cuenta_aleatoria,numero_aleatorio,monto_aleatorio,usuario_aleatorio)
        # Opcional: agregar un pequeño retraso entre solicitudes para no sobrecargar el servidor
        time.sleep(0.1)

# Número de hilos
num_threads = 300





# Crea y arranca los hilos
threads = []
response_data = getAll()
cuentas = response_data.get('Cuentas', [])  # Lista de cuentas
saldo_maximo = response_data.get('SaldoMax', 0.0)  # Saldo máximo
saldo_minimo = response_data.get('SaldoMin', 0.0)  # Saldo mínimo
usuarios = response_data.get('Usuarios', [])  # Lista de usuarios
for i in range(num_threads):

    # Modifica la creación del hilo para usar una lambda o función envolvente
    thread = threading.Thread(target=lambda: thread_function(cuentas, saldo_maximo, saldo_minimo, usuarios))

    thread.daemon = True  # Configura el hilo como daemon para que se termine cuando el programa principal termine
    thread.start()
    threads.append(thread)

# Mantén el programa principal en ejecución indefinidamente
try:
    while True:
        time.sleep(0.1)  # Simple espera para que el programa principal siga ejecutándose
except KeyboardInterrupt:
    print("Programa terminado por el usuario.")
