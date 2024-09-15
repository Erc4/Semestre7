from flask import Blueprint, jsonify, request
from models import db, Paciente

pacientes_bp = Blueprint('pacientes', __name__)

@pacientes_bp.route('/pacientes', methods=['GET'])
def get_users():
    users = Paciente.query.all()
    return jsonify([user.to_dict() for user in users])

@pacientes_bp.route('/pacientes/<int:id>', methods=['GET'])
def get_user(id):
    user = Paciente.query.get_or_404(id)
    return jsonify(user.to_dict())

@pacientes_bp.route('/pacientes', methods=['POST'])
def create_user():
    data = request.json
    new_user = Paciente(
        apellidopaterno=data['apellidopaterno'],
        apellidomaterno=data['apellidomaterno'],
        nombre=data['nombre'],
        usuario=data['usuario'],
        correo=data['correo'],
        password=data['password'],
        peso=data['peso'],
        estatura=data['estatura'],
        edad=data['edad'],
        actividad=data['actividad'],
        metabolismobasal=data['metabolismobasal'],
        imc=data['imc'],
        requerimentoagua=data['requerimentoagua'],
        objetivo=data['objetivo']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@pacientes_bp.route('/pacientes/<int:id>', methods=['PUT'])
def update_user(id):
    user = Paciente.query.get_or_404(id)
    data = request.json
    user.apellidopaterno = data['apellidopaterno']
    user.apellidomaterno = data['apellidomaterno']
    user.nombre = data['nombre']
    user.usuario = data['usuario']
    user.correo = data['correo']
    user.password = data['password']
    user.peso = data['peso']
    user.estatura = data['estatura']
    user.edad = data['edad']
    user.actividad = data['actividad']
    user.metabolismobasal = data['metabolismobasal']
    user.imc = data['imc']
    user.requerimentoagua = data['requerimentoagua']
    user.objetivo = data['objetivo']
    db.session.commit()
    return jsonify(user.to_dict())

@pacientes_bp.route('/pacientes/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = Paciente.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
