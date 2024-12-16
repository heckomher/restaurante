from flask import Flask, request, jsonify
from models.user import User
from models.menu import Menu
from models.order import Order
from database.connection import get_db_connection
from services.api_service import ApiService
import logging
import bcrypt
# Configuración de la Aplicación
app = Flask(__name__)
logging.basicConfig(filename='app.log', level=logging.ERROR)

@app.route('/menu', methods=['GET'])
def show_menu():
    try:
        menus = ApiService.get_all_menus()
        return jsonify(menus)
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Error al obtener el menú"}), 500

@app.route('/menu/<int:menu_id>', methods=['GET'])
def show_menu_by_id(menu_id):
    try:
        menu = ApiService.get_menu_details(menu_id)
        return jsonify(menu)
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Error al obtener el detalle del menú"}), 500

@app.route('/register', methods=['POST'])
def register_user():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        new_user = User(None, data['name'], data['username'], data['password'])
        cursor.execute("INSERT INTO users (name, username, password) VALUES (%s, %s, %s)",
                       (new_user.name, new_user.username, new_user.password))
        conn.commit()
        return jsonify({"message": "Usuario registrado correctamente"})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Error al registrar usuario"}), 500

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = %s", (data['username'],))
        user = cursor.fetchone()
        if user and bcrypt.checkpw(data['password'].encode(), user[3].encode()):
            return jsonify({"message": "Inicio de sesión exitoso"})
        else:
            return jsonify({"error": "Credenciales incorrectas"}), 401
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Error al iniciar sesión"}), 500

@app.route('/update_menu_db', methods=['POST'])
def update_menu_db():
    try:
        menus = ApiService.get_all_menus()
        conn = get_db_connection()
        cursor = conn.cursor()

        for menu in menus:
            cursor.execute(
                "REPLACE INTO menus (menu_id, name, description, price, availability) VALUES (%s, %s, %s, %s, %s)",
                (menu['id'], menu['name'], menu['description'], menu['price'], menu['availability'])
            )
        conn.commit()
        return jsonify({"message": "Base de datos actualizada correctamente"})
    except Exception as e:
        logging.error(f"Error: {e}")
        return jsonify({"error": "Error al actualizar la base de datos"}), 500

if __name__ == '__main__':
    app.run(debug=True)
