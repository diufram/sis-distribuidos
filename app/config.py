import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'clave_secreta_para_firmar')
    REDIS_HOST = 'localhost'
    REDIS_PORT = 6379
    REDIS_DB = 0
    TOKEN_EXPIRATION = 3600  # 1 hora en segundos
    
    # Configuración de SQLAlchemy
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:0000@localhost/python"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
