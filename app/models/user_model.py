from app import db

class Usuario(db.Model):
    ci = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(50), nullable=False)
    apellido = db.Column(db.String(120),  nullable=False)
    sexo = db.Column(db.String(10),  nullable=False)
    def __repr__(self):
        return f'<Usuario {self.nombre}>'
