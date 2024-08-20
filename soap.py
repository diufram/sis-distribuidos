from flask import Flask, request, Response
from flask import jsonify
from lxml import etree

app = Flask(__name__)

@app.route('/soap', methods=['POST'])
def soap():
    xml = request.data
    # Parse the incoming XML to process the request
    tree = etree.fromstring(xml)
    # Extract the method and parameters
    body = tree.find('.//{http://schemas.xmlsoap.org/soap/envelope/}Body')
    method = body.find('.//{http://my_service}say_hello')
    
    # Prepare the response
    response_xml = '''<?xml version="1.0" encoding="UTF-8"?>
    <soapenv:Envelope xmlns:soapenv="http://schemas.xmlsoap.org/soap/envelope/" xmlns:my="http://my_service">
       <soapenv:Header/>
       <soapenv:Body>
          <my:say_helloResponse>
             <return>Hola, mundo!</return>
          </my:say_helloResponse>
       </soapenv:Body>
    </soapenv:Envelope>'''

    return Response(response_xml, content_type='text/xml')

if __name__ == '__main__':
    app.run(debug=True)
