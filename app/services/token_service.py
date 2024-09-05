import base64
from app.models.redis_client import get_redis_client

def generate_token(data):
    """
    Genera un token basado en los datos proporcionados.
    
    :param data: Un diccionario con los datos para el token.
    :return: El token generado y el tiempo de expiración en segundos.
    """
    # Verifica que todos los campos necesarios estén presentes
    required_fields = ['ci', 'nombre', 'apellido', 'sexo']
    if not isinstance(data, dict) or not all(field in data for field in required_fields):
        raise ValueError("Datos inválidos")

    # Combina los datos para crear una cadena única
    data_str = f"{data['ci']}{data['nombre']}{data['apellido']}{data['sexo']}"
    
    # Genera el token
    encoded_data = base64.urlsafe_b64encode(data_str.encode()).decode()
    token = f"token_{encoded_data}"
    
    # Define el tiempo de expiración en segundos
    expiration = 1000  # Ejemplo de expiración
    
    return token, expiration

def store_token(token, expiration):
    """
    Almacena el token en Redis con un tiempo de expiración.
    
    :param token: El token que se almacenará.
    :param expiration: Tiempo en segundos antes de que el token expire.
    """
    r = get_redis_client()
    r.setex(token, expiration, 'not_used')

def mark_token_as_used(token):
    """
    Marca el token como usado en Redis.
    
    :param token: El token que se marcará como usado.
    """
    r = get_redis_client()
    r.set(token, 'used')

def verify_token_exists(token):
    r = get_redis_client()
    # Usa EXISTS para verificar si el token está en Redis
    exists = r.exists(token)
    return exists == 1  # True si el token existe, False en caso contrario


def verify_token(token):
    """
    Verifica si el token es válido y no ha sido usado.
    
    :param token: El token a verificar.
    :return: True si el token es válido y no ha sido usado, False en caso contrario.
    """
    r = get_redis_client()
    status = r.get(token)
    
    if status is None:
        return 0  # Token no encontrado o expirado
    
    if status == 'used':
        return 1  # Token ya ha sido usado
    
    return 2  # Token es válido y no ha sido usado
def delete_token(token):
    """
    Elimina el token de Redis.
    
    :param token: El token que se eliminará.
    :return: True si el token fue eliminado exitosamente, False en caso contrario.
    """
    try:
        r = get_redis_client()
        resultado = r.delete(token)
        
        return resultado == 1  # Devuelve True si el token fue eliminado, False si no fue encontrado
    except get_redis_client.RedisError as e:
        # En caso de error, puedes elegir manejarlo de manera diferente o registrar el error
        print(f"Error al intentar eliminar el token: {e}")
        return False