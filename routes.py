import jwt
import datetime
from flask import Blueprint, jsonify, request, current_app
from models import db, classusuarios, classalimentos
from werkzeug.security import check_password_hash
from functools import wraps


#--------------------------------------------------Proteger rutas ------------------------------------------------------------
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'Authorization' in request.headers:
            token = request.headers['Authorization'].split(" ")[1]
        
        if not token:
            return jsonify({'message': 'Necesitas un token'})
        
        try:
            data=jwt.decode(token, current_app.config['SECRET KEY'],algorithms=['HS256'])
            current_user= classusuarios.query.get(data['id'])
        except:
            return jsonify({'message': 'Token inválido o exprirado'})

        return f(current_user, *args, **kwargs)
    return decorated
    

usuarios_bp = Blueprint('usuarios', __name__)
#--------------------------------------------------Rutas para login ------------------------------------------------------------
@usuarios_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = classusuarios.query.filter_by(usuario=data['usuario']).first()

    if user and check_password_hash(user.password_hash, data['password']):
        token = jwt.encode({
            'id': user.id,
            'usuario':user.usuario,
            'correo':user.correo,
            'rol': user.rol,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=24)
        }, current_app.config['SECRET_KEY'], algorithm='HS256')

        return jsonify ({'token':token}),200
    else:
        return jsonify ({'message': 'Credenciales invalidas'})
#--------------------------------------------------Rutas para gestión de usuarios.--------------------------------------------------

@usuarios_bp.route('/usuarios', methods=['GET'])
#@token_required
def get_users():
    users = classusuarios.query.all()
    return jsonify([user.to_dict() for user in users])

@usuarios_bp.route('/usuarios/<int:id>', methods=['GET'])
def get_user(id):
    user = classusuarios.query.get_or_404(id)
    return jsonify(user.to_dict())

@usuarios_bp.route('/usuarios', methods=['POST'])
#@token_required
def create_user():

    data = request.json
    if not data:  # Verifica que se recibió datos
        return jsonify({"error": "No se recibieron datos"}), 400

    #Calcular imc
    alturaMetros = data['estatura'] / (100)
    imc = data['peso'] / (alturaMetros ** 2)

    #Calcular metabolismo basal
    if data['sexo'] == 'm' or 'M':
        metabolismobasal = 88.362 + (13.97 * data['peso']) + (4.799 * data['estatura']) - (5.677 * data['edad'])
    else:
        metabolismobasal = 447.593 + (9.247 * data['peso']) + (3.098 * data['estatura']) - (4.330 * data['edad'])

    #Calcular requerimiento de agua.
    requerimientoagua = data['peso'] * 35
    
    #Calcular valor numérico de factor de avtividad física
    if data['actividad'] == "baja":
        fap = 1.2
    elif data['actividad'] == "moderada":
        fap = 1.55
    elif data['actividad'] == "alta":
        fap = 1.9
    else:
        return jsonify({"error": "Nivel de actividad no válido"})
    
    # Calcular Requerimiento Calórico según el objetivo
    if data['objetivo'] == 'mantener':
        requerimientocalorico = metabolismobasal * fap
    elif data['objetivo'] == 'aumentar':
        requerimientocalorico = metabolismobasal * fap * 1.15
    elif data['objetivo'] == 'disminuir':
        requerimientocalorico = metabolismobasal * fap * 1.85

    
    
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
        sexo=data['sexo'],
        actividad=data['actividad'],
        metabolismobasal=metabolismobasal,
        imc=imc,
        requerimentoagua=requerimientoagua,
        requerimientocalorico = requerimientocalorico,
        objetivo=data['objetivo']
    )
    new_user.set_password(data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@usuarios_bp.route('/usuarios/<int:id>/personaldata', methods=['PUT'])
#@token_required
def update_userpersonaldata(id):
    user = classusuarios.query.get_or_404(id)
    data = request.json

    if not data:  # Verifica que se recibió datos
        return jsonify({"error": "No se recibieron datos"}), 400

    user.apellidopaterno = data['apellidopaterno']
    user.apellidomaterno = data['apellidomaterno']
    user.nombre = data['nombre']
    user.peso = data['peso']
    user.estatura = data['estatura']
    user.edad = data['edad']
    user.sexo=data['sexo']
    user.actividad = data['actividad']
    user.objetivo = data['objetivo']

    # Recalcular IMC
    altura_metros = user.estatura / 100  # Convertir altura a metros
    user.imc = user.peso / (altura_metros ** 2)

    # Recalcular Metabolismo Basal
    if user.sexo == 'm' or 'M':
        user.metabolismobasal = 88.362 + (13.397 * user.peso) + (4.799 * user.estatura) - (5.677 * user.edad)
    else:
        user.metabolismobasal = 447.593 + (9.247 * user.peso) + (3.098 * user.estatura) - (4.330 * user.edad)

    # Recalcular Requerimiento de Agua
    user.requerimentoagua = user.peso * 35

    # Mapear el nivel de actividad física a un factor numérico
    if user.actividad == 'baja':
        actividad_factor = 1.2
    elif user.actividad == 'moderada':
        actividad_factor = 1.55
    elif user.actividad == 'alta':
        actividad_factor = 1.9
    else:
        return jsonify({"error": "Nivel de actividad no válido"}), 400

    # Recalcular Requerimiento Calórico según el objetivo
    if data['objetivo'] == 'mantener':
        user.requerimientocalorico = user.metabolismobasal * actividad_factor
    elif data['objetivo'] == 'aumentar':
        user.requerimientocalorico = user.metabolismobasal * actividad_factor * 1.15
    elif data['objetivo'] == 'disminuir':
        user.requerimientocalorico = user.metabolismobasal * actividad_factor * 0.85
    else:
        return jsonify({"error": "Objetivo no válido"}), 400

    # Actualizar el campo de objetivo
    user.objetivo = data['objetivo']

    db.session.commit()
    return jsonify(user.to_dict())

@usuarios_bp.route('/usuarios/<int:id>/accountdata', methods=['PUT'])
#@token_required
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
#@token_required
def delete_user(id):
    user = classusuarios.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return '', 204
#--------------------------------------------------Rutas para gestión de alimentos.--------------------------------------------------
alimentos_bp = Blueprint('alimentos' ,__name__)
#@token_required
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
    data = request.json
    new_alimento = classalimentos(
        nombre=data['nombre'],
        porcion=data['porcion'],
        tipo_porcion=data['tipo_porcion'],
        proteinas=data['proteinas'],
        carbohidratos=data['carbohidratos'],
        grasas=data['grasas'],
        calorias=data['calorias']
    )
    db.session.add(new_alimento)
    db.session.commit()
    return jsonify(new_alimento.to_dict()), 201

@alimentos_bp.route('/alimentos/<int:id>', methods = ['PUT'])
#@token_required
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
#@token_required
def delete_alimento(id):
    alimento = classalimentos.query.get_or_404(id)
    db.session.delete(alimento)
    db.session.commit
    return '',204