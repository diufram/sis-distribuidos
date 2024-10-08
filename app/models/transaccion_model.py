from app.extensions import db

from datetime import datetime

class Transaccion(db.Model):
    __tablename__ = 'transacciones'
    
    id = db.Column(db.Integer, primary_key=True)
    nro_transaccion = db.Column(db.Integer, nullable=False)
    fecha = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    monto = db.Column(db.Float(), nullable=False)
    tipo = db.Column(db.Integer,nullable = False)
    id_cuenta = db.Column(db.Integer, db.ForeignKey('cuentas.id'), nullable=False)
    ci_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.ci'), nullable=False)
    
    # Relación muchos a uno con Cuenta
    cuenta = db.relationship('Cuenta', back_populates='transacciones')
    
    # Relación muchos a uno con Usuario
    usuario = db.relationship('Usuario', back_populates='transacciones')

    def __repr__(self):
        return f'<Transaccion {self.id} - {self.monto}>'