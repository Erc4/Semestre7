from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class classusuarios(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    apellidopaterno = db.Column(db.String(255), nullable=False)
    apellidomaterno = db.Column(db.String(255), nullable=False)
    nombre = db.Column(db.String(255), nullable=False)
    rol = db.Column(db.Integer, nullable = False)
    usuario = db.Column (db.String(255), nullable=False)
    correo = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    peso = db.Column(db.Float, nullable=False)
    estatura = db.Column(db.Integer, nullable=False)
    edad = db.Column(db.Integer, nullable=False)
    actividad = db.Column(db.String(255), nullable=False)
    metabolismobasal = db.Column(db.Integer, nullable=False)
    imc = db.Column(db.Float, nullable=False)
    requerimentoagua = db.Column(db.Integer, nullable=False)
    objetivo = db.Column(db.String(255), nullable=False)

    def set_password(self,password):
        self.password_hash = generate_password_hash(password)

    def check_password(self,password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        return {
            'id': self.id,
            'apellidopaterno': self.apellidopaterno,
            'apellidomaterno': self.apellidomaterno,
            'nombre': self.nombre,
            'rol' : self.rol,
            'usuario': self.usuario,
            'correo': self.correo,
            'peso': self.peso,
            'estatura': self.estatura,
            'edad': self.edad,
            'actividad': self.actividad,
            'metabolismobasal': self.metabolismobasal,
            'imc': self.imc,
            'requerimentoagua': self.requerimentoagua,
            'objetivo': self.objetivo
        }
    
class classalimentos(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(255), nullable=False)
    porcion = db.Column(db.Integer, nullable=False)
    proteinas = db.Column(db.Float, nullable=False)
    carbohidratos = db.Column(db.Float, nullable=False)
    grasas = db.Column(db.Float, nullable=False)
    calorias = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return{
            'id': self.id,
            'nombre': self.nombre,
            'porcion': self.porcion,
            'proteinas': self.proteinas,
            'carbohidratos': self.carbohidratos,
            'grasas': self.grasas,
            'calorias': self.calorias 
        }

