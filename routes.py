from flask import Blueprint, jsonify, request
from models import db, classusuarios, classalimentos

#--------------------------------------------------Rutas para gestión de usuarios.--------------------------------------------------
usuarios_bp = Blueprint('usuarios', __name__)
@usuarios_bp.route('/usuarios', methods=['GET'])
def get_users():
    users = classusuarios.query.all()
    return jsonify([user.to_dict() for user in users])

@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_user(id):
    user = classusuarios.query.get_or_404(id)
    return jsonify(user.to_dict())

@usuarios_bp.route('/usuarios', methods=['POST'])
def create_user():
    data = request.json
    new_user = classusuarios(
        apellidopaterno=data['apellidopaterno'],
        apellidomaterno=data['apellidomaterno'],
        nombre=data['nombre'],
        rol=data['rol'],
        usuario=data['usuario'],
        correo=data['correo'],
        peso=data['peso'],
        estatura=data['estatura'],
        edad=data['edad'],
        actividad=data['actividad'],
        metabolismobasal=data['metabolismobasal'],
        imc=data['imc'],
        requerimentoagua=data['requerimentoagua'],
        objetivo=data['objetivo']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@usuarios_bp.route('/usuarios/<int:id>/personaldata', methods=['PUT'])
def update_userpersonaldata(id):
    user = classusuarios.query.get_or_404(id)
    data = request.json
    user.apellidopaterno = data['apellidopaterno']
    user.apellidomaterno = data['apellidomaterno']
    user.nombre = data['nombre']
    user.peso = data['peso']
    user.estatura = data['estatura']
    user.edad = data['edad']
    user.actividad = data['actividad']
    user.objetivo = data['objetivo']
    db.session.commit()
    return jsonify(user.to_dict())

@usuarios_bp.route('/usuarios/<int:id>/accountdata', methods=['PUT'])
def update_accountdata(id):
    user = classusuarios.query.get_or_404(id)
    data = request.json
    user.usuario = data['usuario']
    user.correo = data['correo']
    user.rol = data['rol']
    if 'password' in data and data['password']:
        user.set_password(data['password'])
    db.session.commit()
    return jsonify(user.to_dict())

@usuarios_bp.route('/usuarios/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = classusuarios.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204

@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = classusuarios.query.filter_by(correo=data['correo']).first()

    if user and user.check_password(data['password']):
        return jsonify({"message": "Login exitoso"})
    else:
        return jsonify({"error": "Credenciales inválidas"}), 401

#--------------------------------------------------Rutas para gestión de alimentos.--------------------------------------------------
alimentos_bp = Blueprint('alimentos' ,__name__)
@alimentos_bp.route('/alimentos', methods=['GET'])
def get_alimentos():
    alimentos = classalimentos.query.all()
    return jsonify([alimento.to_dict() for alimento in alimentos])

@alimentos_bp.route('/alimentos/<int:id>', methods=['GET'])
def get_alimento(id):
    alimento = classalimentos.query.get_or_404(id)
    return jsonify(alimento.to_dict())

@alimentos_bp.route('/alimentos', methods = ['POST'])
def crear_alimento():
    data = request.json()
    new_alimento = classalimentos(
        nombre=data['nombre'],
        porcion=data['porcion'],
        proteinas=data['proteinas'],
        carbohidratos=data['carbohidratos'],
        grasas=data['grasas'],
        calorias=data['calorias']
    )
    db.session.add(new_alimento)
    db.session.commit()
    return jsonify(new_alimento.to_dict()), 201

@alimentos_bp.route('/alimentos/<int:id>', methods = ['PUT'])
def update_alimento(id):
    alimento = classalimentos.query.get_or_404(id)
    data = request.json()
    alimento.nombre = data['nombre']
    alimento.porcion = data['porcion']
    alimento.proteinas = data['proteinas']
    alimento.carbohidratos = data['carbohidratos']
    alimento.grasas = data['grasas']
    alimento.calorias = data['calorias']
    db.session.commit()
    return jsonify(alimento.to_dict())
    
@alimentos_bp.route('/alimentos/<int:id>', methods = ['DELETE'])
def delete_alimento(id):
    alimento = classalimentos.query.get_or_404(id)
    db.session.delete(alimento)
    db.session.commit
    return '',204