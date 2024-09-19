from flask import Blueprint, request
from app.services.transaccion_async_service import transaccion_asyn, iniciar_hilo

transaccion_async_bp = Blueprint('transaccion_async', __name__)

# Ruta para procesar transacción de forma asíncrona
@transaccion_async_bp.route('/transaccion', methods=['POST'])
def transaccionPost():
    data = request.get_json()
    respuesta = transaccion_asyn(datos=data)
    return respuesta
