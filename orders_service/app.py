import os
import pyodbc
from flask import Flask, jsonify, request
from flasgger import Swagger
from dotenv import load_dotenv

# Загружаем настройки из .env (если он есть)
load_dotenv()

app = Flask(__name__)
# Настройка Swagger (авто-документация)
app.config['SWAGGER'] = {'title': 'Orders Service API', 'uiversion': 3}
swagger = Swagger(app)

@app.route('/')
def home():
    return "Orders Service is running!"

def get_db_connection():
    """Умное подключение к БД"""
    server = os.getenv('DB_SERVER', 'localhost')
    database = os.getenv('DB_DATABASE', '445_EPD')
    username = os.getenv('DB_USER')
    password = os.getenv('DB_PASSWORD')

    if username and password:
        # Режим 1: Для GitHub Actions (с паролем)
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};DATABASE={database};'
            f'UID={username};PWD={password};'
            f'TrustServerCertificate=yes;'
        )
    else:
        # Режим 2: Локальный (Windows Auth, без пароля)
        conn_str = (
            f'DRIVER={{ODBC Driver 17 for SQL Server}};'
            f'SERVER={server};DATABASE={database};'
            f'Trusted_Connection=yes;'  # Используем текущую Windows-учетку
            f'TrustServerCertificate=yes;'  # Игнорируем ошибки сертификатов
        )

    return pyodbc.connect(conn_str)


@app.route('/orders', methods=['GET'])
def get_orders():
    """
    Получить список всех заказов
    ---
    responses:
      200:
        description: Список заказов
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT id, product_id, customer_id, quantity FROM Orders')
    rows = cursor.fetchall()
    # Превращаем строки БД в красивый JSON
    orders = [{"id": r.id, "product_id": r.product_id, "customer_id": r.customer_id, "quantity": r.quantity} for r in
              rows]
    conn.close()
    return jsonify(orders)


@app.route('/orders', methods=['POST'])
def create_order():
    """
    Создать новый заказ
    ---
    parameters:
      - name: body
        in: body
        required: true
        schema:
          type: object
          properties:
            product_id: {type: integer}
            customer_id: {type: integer}
            quantity: {type: integer}
    responses:
      201:
        description: Заказ создан
    """
    new_order = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    query = "INSERT INTO Orders (product_id, customer_id, quantity) OUTPUT INSERTED.id VALUES (?, ?, ?)"
    cursor.execute(query, (new_order['product_id'], new_order['customer_id'], new_order['quantity']))
    new_id = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    new_order['id'] = new_id
    return jsonify(new_order), 201


if __name__ == '__main__':
    app.run(port=5002, debug=True)