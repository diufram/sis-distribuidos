import os

class Config:
    # Clave secreta para la firma de tokens y sesiones
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_para_firmar')
    
    # Configuración de Redis
    REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))
    REDIS_DB = int(os.environ.get('REDIS_DB', 0))
    
    # Tiempo de expiración del token en segundos
    TOKEN_EXPIRATION = int(os.environ.get('TOKEN_EXPIRATION', 3600))  # 1 hora en segundos
    
    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = os.environ.get(
    'SQLALCHEMY_DATABASE_URI', 
    'postgresql://matias:0000@localhost:5432/distribuido'
)


    SQLALCHEMY_TRACK_MODIFICATIONS = False

    SQLALCHEMY_ENGINE_OPTIONS = {
        'pool_size': int(os.environ.get('POOL_SIZE', 5)),  # Tamaño máximo del pool
        'max_overflow': int(os.environ.get('MAX_OVERFLOW', 1)),  # Conexiones adicionales permitidas si el pool está lleno
        'pool_timeout': int(os.environ.get('POOL_TIMEOUT', 10)),  # Tiempo máximo de espera para una conexión en el pool
        'pool_recycle': int(os.environ.get('POOL_RECYCLE', 5)),  # Tiempo en segundos para reciclar conexiones
        'pool_pre_ping': bool(os.environ.get('POOL_PRE_PING', True))  # Habilitar verificación previa de la conexión
    }
