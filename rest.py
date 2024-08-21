from flask import Flask, jsonify
import psycopg2

app = Flask(__name__)

# Configura los detalles de conexión a la base de datos PostgreSQL
DB_HOST = '10.29.8.72'
DB_PORT = '5432'
DB_NAME = 'distribuido'
DB_USER = 'postgres'
DB_PASSWORD = '0910'

@app.route('/')
def index():
    return "Hola, mundo!"

@app.route('/test')
def test():
    try:
        # Conectarse a la base de datos usando psycopg2
        conn = psycopg2.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        cur.execute('SELECT nombre from public."user";')
        version = cur.fetchone()[0]
        cur.close()
        conn.close()
        return jsonify(version=version)
    except Exception as e:
        return jsonify(error=str(e))

if __name__ == '__main__':
    app.run(host='10.29.9.59', port=5000, debug=True)
