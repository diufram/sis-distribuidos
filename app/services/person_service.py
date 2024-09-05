from lxml import etree
from app.models import Usuario
from app import db

# Datos simulados en memoria para el ejemplo
people_db = {}

def handle_create_person(operation):
    ci = operation.find('{http://person_service}ci').text
    nombre = operation.find('{http://person_service}nombre').text
    apellido = operation.find('{http://person_service}apellido').text
    sexo = operation.find('{http://person_service}sexo').text
    token = operation.find('{http://person_service}token').text

    if token != "valid_token":  # Simple token validation
        return create_soap_response('create_person', 'Invalid token')
    
    people_db[ci] = {'nombre': nombre, 'apellido': apellido, 'sexo': sexo}
    return create_soap_response('create_person', 'Success')

def handle_get_person(operation):
    ci = operation.find('{http://person_service}ci').text
    token = operation.find('{http://person_service}token').text

    if token != "valid_token":
        return create_soap_response('get_person', 'Invalid token')
    
    person = people_db.get(ci, None)
    if person:
        response_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
        <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:my="http://person_service">
           <soapenv:Header/>
           <soapenv:Body>
              <my:get_personResponse>
                 <nombre>{person['nombre']}</nombre>
                 <apellido>{person['apellido']}</apellido>
                 <sexo>{person['sexo']}</sexo>
              </my:get_personResponse>
           </soapenv:Body>
        </soapenv:Envelope>'''
        return response_xml
    else:
        return create_soap_response('get_person', 'Person not found')

def create_soap_response(operation, status):
    """Generates a SOAP response based on the operation and status."""
    response_xml = f'''<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:my="http://person_service">
       <soapenv:Header/>
       <soapenv:Body>
          <my:{operation}Response>
             <status>{status}</status>
          </my:{operation}Response>
       </soapenv:Body>
    </soapenv:Envelope>'''
    return response_xml
