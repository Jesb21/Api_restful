from flask import Flask, jsonify, request
import pymysql

app = Flask(__name__)

def obtener_conexion():
    return pymysql.connect(
        host="localhost",
        user="root",
        password="eilaeila2106",
        database="api_restful",
        cursorclass=pymysql.cursors.DictCursor
    )

@app.route('/users', methods=['GET'])
def obtener_usuarios():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM users")
        usuarios = cursor.fetchall()
    conexion.close()
    return jsonify(usuarios)

@app.route('/users', methods=['POST'])
def agregar_usuario():
    datos = request.json
    nombre = datos.get('nombre')
    correo = datos.get('correo')
    contraseña = datos.get('contraseña')

    if not (nombre and correo and contraseña):
        return jsonify({'error': 'Faltan datos'}), 400

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        try:
            cursor.execute("INSERT INTO users (nombre, correo, contraseña) VALUES (%s, %s, %s)", 
                           (nombre, correo, contraseña))
            conexion.commit()
            return jsonify({'mensaje': 'Usuario agregado correctamente'}), 201
        except pymysql.err.IntegrityError:
            return jsonify({'error': 'El correo ya está en uso'}), 400
        finally:
            conexion.close()

@app.route('/users/<int:id>', methods=['PUT'])
def actualizar_usuario(id):
    datos = request.json
    nombre = datos.get('nombre')
    correo = datos.get('correo')
    contraseña = datos.get('contraseña')

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE users SET nombre=%s, correo=%s, contraseña=%s WHERE id=%s", 
                       (nombre, correo, contraseña, id))
        conexion.commit()

    conexion.close()
    return jsonify({'mensaje': 'Usuario actualizado correctamente'})

@app.route('/users/<int:id>', methods=['DELETE'])
def eliminar_usuario(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM users WHERE id = %s", (id,))
        conexion.commit()

    conexion.close()
    return jsonify({'mensaje': 'Usuario eliminado correctamente'})

@app.route('/products', methods=['GET'])
def obtener_productos():
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("SELECT * FROM products")
        productos = cursor.fetchall()
    conexion.close()
    return jsonify(productos)

@app.route('/products', methods=['POST'])
def agregar_producto():
    datos = request.json
    nombre = datos.get('nombre')
    precio = datos.get('precio')
    stock = datos.get('stock')

    if not (nombre and precio and stock):
        return jsonify({'error': 'Faltan datos'}), 400

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("INSERT INTO products (nombre, precio, stock) VALUES (%s, %s, %s)", 
                       (nombre, precio, stock))
        conexion.commit()

    conexion.close()
    return jsonify({'mensaje': 'Producto agregado correctamente'}), 201

@app.route('/products/<int:id>', methods=['PUT'])
def actualizar_producto(id):
    datos = request.json
    nombre = datos.get('nombre')
    precio = datos.get('precio')
    stock = datos.get('stock')

    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("UPDATE products SET nombre=%s, precio=%s, stock=%s WHERE id=%s", 
                       (nombre, precio, stock, id))
        conexion.commit()

    conexion.close()
    return jsonify({'mensaje': 'Producto actualizado correctamente'})

@app.route('/products/<int:id>', methods=['DELETE'])
def eliminar_producto(id):
    conexion = obtener_conexion()
    with conexion.cursor() as cursor:
        cursor.execute("DELETE FROM products WHERE id = %s", (id,))
        conexion.commit()

    conexion.close()
    return jsonify({'mensaje': 'Producto eliminado correctamente'})

if __name__ == '__main__':
    app.run(debug=True)
