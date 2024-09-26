from app.extensions import db
from sqlalchemy import func

class ColaResponse(db.Model):
    __tablename__ = 'ColaResponses'
    
    id = db.Column(db.Integer, primary_key=True)
    nro_transaccion = db.Column(db.Integer, nullable=False)
    datos = db.Column(db.JSON, nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=func.now())
    status = db.Column(db.Boolean, nullable=False)
    error = db.Column(db.String, nullable=False)
    

    def __repr__(self):
        return f'<ColaResponse id={self.id}, status={self.status}>'
    
def verificar_transaccion_realizada(nro_transaccion):
    # Realiza una consulta a la base de datos para verificar si ya existe la transacción
    transaccion = ColaResponse.query.filter_by(nro_transaccion=nro_transaccion).first()
    return transaccion

def add_cola_response(session, nro_transaccion, datos, error,status):
    # Crear una nueva instancia de ColaResponse
    nueva_transaccion = ColaResponse(
        nro_transaccion=nro_transaccion,
        datos=datos,
        error=error,
        status= status
    )
    session.add(nueva_transaccion)
