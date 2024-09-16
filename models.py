from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class usuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellidopaterno = db.Column(db.String(255), nullable=False)
    apellidomaterno = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Integer, nullable = False)
    usuario = db.Column (db.String(255), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    estatura = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    actividad = db.Column(db.String(255), nullable=False)
    metabolismobasal = db.Column(db.Integer, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    requerimentoagua = db.Column(db.Integer, nullable=False)
    objetivo = db.Column(db.String(255), nullable=False)

    def to_dict(self):
        return {
            'id': self.id,
            'apellidopaterno': self.apellidopaterno,
            'apellidomaterno': self.apellidomaterno,
            'nombre': self.nombre,
            'rol' : self.rol,
            'usuario': self.usuario,
            'correo': self.correo,
            'password': self.password,
            'peso': self.peso,
            'estatura': self.estatura,
            'edad': self.edad,
            'actividad': self.actividad,
            'metabolismobasal': self.metabolismobasal,
            'imc': self.imc,
            'requerimentoagua': self.requerimentoagua,
            'objetivo': self.objetivo
        }
