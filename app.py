from flask import Flask, jsonify, request
import mysql.connector

app = Flask(__name__)

app.config['MYSQL_HOST'] = 'mysql'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = '12345'
app.config['MYSQL_DATABASE'] = 'mydatabase'

def get_db():
    conn = mysql.connector.connect(
        host=app.config['MYSQL_HOST'],
        user=app.config['MYSQL_USER'],
        password=app.config['MYSQL_PASSWORD'],
        database=app.config['MYSQL_DATABASE']
    )
    return conn


@app.route('/', methods=['GET'])
def get_consumables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consumables")
    consumables = cursor.fetchall()
    conn.close()
    return jsonify([{'id': c[0], 'name': c[1], 'quantity': c[2]} for c in consumables])


@app.route('/consumables', methods=['POST'])
def add_consumable():
    conn = get_db()
    cursor = conn.cursor()
    data = request.get_json()
    cursor.execute("INSERT INTO consumables (name, quantity) VALUES (%s, %s)", (data['name'], data['quantity']))
    conn.commit()
    conn.close()
    return jsonify({'message': 'Consumable added successfully!'}), 201


@app.route('/consumables/<name>', methods=['GET'])
def get_consumable_by_name(name):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consumables WHERE name = %s", (name,))
    consumables = cursor.fetchall()
    conn.close()
    if not consumables:
        return jsonify({'message': 'No consumables found!'}), 404
    return jsonify([{'id': c[0], 'name': c[1], 'quantity': c[2]} for c in consumables])


@app.route('/consumables', methods=['GET'])
def get_all_consumables():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM consumables")
    consumables = cursor.fetchall()
    conn.close()
    return jsonify([{'id': c[0], 'name': c[1], 'quantity': c[2]} for c in consumables])


if __name__ == '__main__':
    app.run(debug=True)