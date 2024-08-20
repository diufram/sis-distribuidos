from flask import Flask, jsonify

app = Flask(__name__)

@app.route('/rest', methods=['GET'])
def say_hello():
    return jsonify(message="Hola, mundo!")

if __name__ == '__main__':
    app.run(host='192.168.0.3', port=5000, debug=True)
