from flask import Blueprint, request, Response,jsonify
from lxml import etree
from app import db
from sqlalchemy.exc import IntegrityError
from app.models import Usuario 
from app.services.person_service import handle_create_person, handle_get_person
from app.services.token_service import generate_token, store_token, verify_token, delete_token,mark_token_as_used,verify_token_exists

person_bp = Blueprint('person', __name__)

def parse_soap_request(xml):
    """Parses the incoming SOAP XML request and extracts the body."""
    tree = etree.fromstring(xml)
    body = tree.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
    return body

@person_bp.route('/persons', methods=['POST'])
def soap():
    xml = request.data
    body = parse_soap_request(xml)
    operation = body.find('.//{http://person_service}create_person')
    
    if operation is not None:
        response_xml = handle_create_person(operation)
        return Response(response_xml, content_type='text/xml')

    operation = body.find('.//{http://person_service}get_person')
    if operation is not None:
        response_xml = handle_get_person(operation)
        return Response(response_xml, content_type='text/xml')

    return Response('Operation not supported', status=400, content_type='text/xml')

@person_bp.route('/rest', methods=['GET'])
def rest():
    session = db.session
    try:
        data = {
            "ci": 9044956,
            "nombre": "Matias Franco",
            "apellido": "Ramos Limachi",
            "sexo": "Masculino"
        }

        # Generar el token
        token, expiration = generate_token(data)
        print(f"Token: {token}")
        print(f"Expiración del Token: {expiration}")

        # Verificar si el token ya existe
        token_status = verify_token_exists(token)
        if token_status:
            if verify_token == 2:
                return jsonify({"message": "Se está procesando su solicitud"}), 200
            elif verify_token == 0:
                print(f"Se borró el token porque se expiró: {delete_token(token)}")
                return jsonify({"message": "Su token expiró, intente nuevamente"}), 200
            elif verify_token == 1:
                print(f"Se borró el token porque ya ha sido usado: {delete_token(token)}")
                return jsonify({"message": "Su token ya ha sido usado, intente más tarde"}), 200

        print("Se guardó el Token")
        store_token(token, expiration)

        # Crear un nuevo usuario
        nuevo_usuario = Usuario(
            ci=data['ci'],
            nombre=data['nombre'],
            apellido=data['apellido'],
            sexo=data['sexo']
        )

        # Agregar el nuevo usuario a la sesión
        session.add(nuevo_usuario)
        
        # Confirmar la transacción
        session.commit()

        mark_token_as_used(token)
        

        return jsonify({"message": "Usuario agregado exitosamente."}), 201

    except IntegrityError as e:
        session.rollback()
        print(f"Error de integridad: {e}")  # Registro del error en el log
        return jsonify({"message": "El usuario ya existe"}), 400

    except ValueError as e:
        session.rollback()
        return jsonify({"message": str(e)}), 400

    except Exception as e:
        session.rollback()
        return jsonify({"message": "Error interno del servidor"}), 500

    finally:
        session.remove()  # Asegúrate de cerrar la sesión
        print(f"Se borró el token porque ya ha sido usado: {delete_token(token)}")
        print("Finalizó todo")

        


@person_bp.route('/soap', methods=['POST'])
def soap_service():
    # Parsear el mensaje SOAP recibido
    soap_request = etree.fromstring(request.data)
    
    # Extraer los parámetros del mensaje SOAP
    ci = soap_request.find('.//{http://example.com/}ci').text
    nombre = soap_request.find('.//{http://example.com/}nombre').text
    apellido = soap_request.find('.//{http://example.com/}apellido').text
    sexo = soap_request.find('.//{http://example.com/}sexo').text

    response_message = ""
    try:
        data = {
            "ci": int(ci),
            "nombre": nombre,
            "apellido": apellido,
            "sexo": sexo
        }

        # Generar el token
        token, expiration = generate_token(data)
        print(f"Token: {token}")
        print(f"Expiración del Token: {expiration}")

        # Verificar si el token ya existe
        token_status = verify_token_exists(token)
        if token_status:
            if token_status == 2:
                response_message = "Se está procesando su solicitud"
            elif token_status == 0:
                print(f"Se borró el token porque se expiró: {delete_token(token)}")
                response_message = "Su token expiró, intente nuevamente"
            elif token_status == 1:
                print(f"Se borró el token porque ya ha sido usado: {delete_token(token)}")
                response_message = "Su token ya ha sido usado, intente más tarde"
        else:
            print("Se guardó el Token")
            store_token(token, expiration)

            # Crear un nuevo usuario
            nuevo_usuario = Usuario(
                ci=data['ci'],
                nombre=data['nombre'],
                apellido=data['apellido'],
                sexo=data['sexo']
            )

            # Agregar el nuevo usuario a la sesión
            db.session.add(nuevo_usuario)
            db.session.commit()

            mark_token_as_used(token)

            response_message = "Usuario agregado exitosamente."

    except IntegrityError as e:
        db.session.rollback()
        response_message = "El usuario ya existe"
    except ValueError as e:
        response_message = str(e)
    except Exception as e:
        response_message = "Error interno del servidor"

    # Construir la respuesta SOAP
    soap_envelope = etree.Element("{http://schemas.xmlsoap.org/soap/envelope/}Envelope", xmlns="http://schemas.xmlsoap.org/soap/envelope/")
    soap_body = etree.SubElement(soap_envelope, "{http://schemas.xmlsoap.org/soap/envelope/}Body")
    add_user_response = etree.SubElement(soap_body, "AddUserResponse", xmlns="http://example.com/")
    message_element = etree.SubElement(add_user_response, "message")
    message_element.text = response_message

    # Convertir el árbol XML a una cadena
    soap_response = etree.tostring(soap_envelope, pretty_print=True, xml_declaration=True, encoding="UTF-8")

    # Devolver la respuesta SOAP
    return Response(soap_response, content_type='text/xml; charset=utf-8')