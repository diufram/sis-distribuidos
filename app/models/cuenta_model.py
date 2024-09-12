from app import db

class Cuenta(db.Model):
    __tablename__ = 'cuentas'
    
    id = db.Column(db.Integer, primary_key=True)
    saldo =db.Column(db.Float, nullable=False)
    ci_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.ci'), nullable=False)
    
    # Relación muchos a uno con Usuario
    usuario = db.relationship('Usuario', back_populates='cuentas')
    
    # Relación uno a muchos con Transacción
    transacciones = db.relationship('Transaccion', back_populates='cuenta')

    def __repr__(self):
        return f'<Cuenta {self.nombre}>'