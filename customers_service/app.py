# Микросервис управления клиентами

from flask import Flask, jsonify

app = Flask(__name__)

# Данные клиентов (в реальном приложении это была бы база данных)
customers = [
    {"id": 1, "name": "Customer A"},
    {"id": 2, "name": "Customer B"},
    {"id": 3, "name": "Customer C"},
]

@app.route('/customers', methods=['GET'])
def get_customers():
    """Получить список всех клиентов"""
    return jsonify(customers)

@app.route('/customers/<int:customer_id>', methods=['GET'])
def get_customer(customer_id):
    """Получить клиента по ID"""
    customer = next((cust for cust in customers if cust["id"] == customer_id), None)
    return jsonify(customer) if customer else ('Not Found', 404)

if __name__ == '__main__':
    app.run(port=5003, debug=True)