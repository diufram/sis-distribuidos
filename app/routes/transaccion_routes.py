from flask import Blueprint,request
from app.services.transaccion_service import getAll,transaccion
transaccion_bp = Blueprint('transaccion', __name__)



@transaccion_bp.route('/transaccion', methods=['POST'])
def transaccionPost():
    data = request.get_json()
    repuesta =  transaccion(data= data)
    return repuesta

@transaccion_bp.route('/getall', methods=['GET'])
def get():
    return getAll()
    
