import base64
from datetime import timedelta
from app.models.redis_client import get_redis_client

def generate_token(data):
    # Verifica que todos los campos necesarios estén presentes
    required_fields = ['nombre', 'ci', 'telefono', 'lugar_de_nacimiento']
    if not isinstance(data, dict) or not all(field in data for field in required_fields):
        raise ValueError("Datos inválidos")

    # Combina los datos para crear una cadena única
    data_str = f"{data['nombre']}{data['ci']}{data['telefono']}{data['lugar_de_nacimiento']}"
    
    # Genera el token
    encoded_data = base64.b64encode(data_str.encode()).decode()
    token = f"token_{encoded_data}"
    expiration = 3600  # Ejemplo de expiración en segundos

    return token, expiration

def store_token(token, expiration):
    r = get_redis_client()
    # Solo almacenamos el token cuando es utilizado, en caso de GET token
    r.setex(token, expiration, 'not_used')

def verify_token(token):
    r = get_redis_client()
    # Verificamos si el token existe y si ha sido usado
    status = r.get(token)
    if status is None:
        return False  # Token no encontrado
    return status == 'not_used'
