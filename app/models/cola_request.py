from app.extensions import db
from sqlalchemy import func

class ColaRequest(db.Model):
    __tablename__ = 'ColaRequests'
    
    id = db.Column(db.Integer, primary_key=True)
    nro_transaccion = db.Column(db.Integer, nullable=False)
    datos = db.Column(db.JSON, nullable=False)
    status = db.Column(db.Boolean, nullable=False, default=False)
    intentos = db.Column(db.Integer, nullable=False, default=3)
    fecha_procesado = db.Column(db.DateTime, nullable=True)
    fecha_creacion = db.Column(db.DateTime, default=func.now())

    def __repr__(self):
        return f'<ColaRequest id={self.id}, status={self.status}>'

# Función para obtener el primer elemento en la cola
def obtener_primero_en_cola(session):
    return session.query(ColaRequest)\
        .with_for_update(skip_locked=True)\
        .filter_by(status=False)\
        .order_by(ColaRequest.id.asc())\
        .first()


def eliminar_solicitud(request, session):
    session.delete(request)
# Función para incrementar los intentos
def incrementar_intentos(cola_request, session):
    try:
        cola_request.intentos -= 1
        if cola_request.intentos <= 0:
            cola_request.error = "Número máximo de intentos alcanzado"
        session.add(cola_request)
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
