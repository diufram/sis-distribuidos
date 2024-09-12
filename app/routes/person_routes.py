from flask import Blueprint, request,jsonify


from app.models import Usuario 
from app.services.person_service import rest

person_bp = Blueprint('person', __name__)

@person_bp.route('/rest', methods=['POST'])
def createrest():
    data = request.get_json()
    respuesta = rest(data)
    return respuesta


    

@person_bp.route('/get-datos', methods=['GET'])
def get_datos():
    users = Usuario.query.all()
    users_list = [{'ci': user.ci, 'nombre': user.nombre, 'apellido': user.apellido, 'sexo': user.sexo} for user in users]
    return jsonify(users_list),200





