from app.extensions import db
from sqlalchemy import func

class ColaResponse(db.Model):
    __tablename__ = 'ColaResponses'
    
    id = db.Column(db.Integer, primary_key=True)
    nro_transaccion = db.Column(db.Integer, nullable=False)
    datos = db.Column(db.JSON, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.Boolean, nullable=False)
    urlCallback = db.Column(db.String, nullable=False)
    error = db.Column(db.String, nullable=False)
    
    def __repr__(self):
        return f'<ColaResponse id={self.id}, status={self.status}>'
    
def verificar_transaccion_realizada(nro_transaccion):
    # Realiza una consulta a la base de datos para verificar si ya existe la transacción
    transaccion = ColaResponse.query.filter_by(nro_transaccion=nro_transaccion).first()
    return transaccion

def add_cola_response(session, nro_transaccion, datos, error,status,urlCallback):
    # Crear una nueva instancia de ColaResponse
    nueva_transaccion = ColaResponse(
        nro_transaccion = nro_transaccion,
        datos = datos,
        error = error,
        status = status,
        urlCallback = urlCallback
    )
    session.add(nueva_transaccion)

def obtener_primero_en_cola_response(session):
    return session.query(ColaResponse)\
        .with_for_update(skip_locked=True)\
        .order_by(ColaResponse.id.asc())\
        .first()

def eliminar_cola_response(request, session):
    session.delete(request)