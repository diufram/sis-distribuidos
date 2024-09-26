from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import scoped_session, sessionmaker

# Inicialización de SQLAlchemy
db = SQLAlchemy()

# Configura una fábrica de sesiones por hilo/contexto
Session = scoped_session(sessionmaker(autocommit=False, autoflush=False,))

# Función para obtener la sesión actual (por hilo/contexto)
def get_session():
    return Session()
