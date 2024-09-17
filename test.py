import requests
import json
import time
import random
from concurrent.futures import ThreadPoolExecutor

# Configura el URL del endpoint de tu servidor Flask
url = 'http://127.0.0.1:5000/transaccion/transaccion'

def getAll():
    headers = {'Content-Type': 'application/json'}
    try:
        response = requests.get("http://127.0.0.1:5000/transaccion/getall", headers=headers)
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
def thread_function(cuentas, saldo_maximo, saldo_minimo, usuarios):
    while True:
        cuenta_aleatoria = random.choice(cuentas)
        usuario_aleatorio = random.choice(usuarios)
        monto_aleatorio = random.uniform(saldo_minimo, saldo_maximo)
        numero_aleatorio = random.choice([0, 1])
        make_request(cuenta_aleatoria, numero_aleatorio, monto_aleatorio, usuario_aleatorio)
        time.sleep(0.1)  # Opcional: retraso para no sobrecargar el servidor

# Número de hilos
num_threads = 1000

# Crea y arranca los hilos
response_data = getAll()
cuentas = response_data.get('Cuentas', [])  # Lista de cuentas
saldo_maximo = response_data.get('SaldoMax', 0.0)  # Saldo máximo
saldo_minimo = response_data.get('SaldoMin', 0.0)  # Saldo mínimo
usuarios = response_data.get('Usuarios', [])  # Lista de usuarios

with ThreadPoolExecutor(max_workers=num_threads) as executor:
    futures = [executor.submit(thread_function, cuentas, saldo_maximo, saldo_minimo, usuarios) for _ in range(num_threads)]

    # Espera a que todos los hilos terminen (esto es opcional y depende de cómo quieras manejar el tiempo de ejecución)
    for future in futures:
        future.result()  # Puedes manejar excepciones aquí si es necesario

