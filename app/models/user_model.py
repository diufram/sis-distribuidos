from app import db

# Modelo Usuario
class Usuario(db.Model):
    __tablename__ = 'usuarios'
    
    ci = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(120), nullable=False)
    sexo = db.Column(db.String(10), nullable=False)
    
    # Relación uno a muchos con Cuenta
    cuentas = db.relationship('Cuenta', back_populates='usuario')
    # Relación uno a muchos con Transacción
    transacciones = db.relationship('Transaccion', back_populates='usuario')

    def __repr__(self):
        return f'<Usuario {self.nombre}>'
