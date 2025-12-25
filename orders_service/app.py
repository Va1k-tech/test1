# Микросервис управления заказами

from flask import Flask, jsonify, request

app = Flask(__name__)

# Хранилище заказов (в реальном приложении это была бы база данных)
orders = []

@app.route('/orders', methods=['GET'])
def get_orders():
    """Получить список всех заказов"""
    return jsonify(orders)

@app.route('/orders', methods=['POST'])
def create_order():
    """Создать новый заказ"""
    order = request.json
    # Добавляем ID заказа
    order['id'] = len(orders) + 1
    orders.append(order)
    return jsonify(order), 201

if __name__ == '__main__':
    app.run(port=5002, debug=True)