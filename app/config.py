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
        'postgresql://postgres:0000@localhost:5432/prueba'
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
