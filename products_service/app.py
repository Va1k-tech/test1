# Микросервис управления товарами

from flask import Flask, jsonify

app = Flask(__name__)

# Данные товаров (в реальном приложении это была бы база данных)
products = [
    {"id": 1, "name": "Product A", "price": 10.0},
    {"id": 2, "name": "Product B", "price": 20.0},
    {"id": 3, "name": "Product C", "price": 15.5},
]

@app.route('/products', methods=['GET'])
def get_products():
    """Получить список всех товаров"""
    return jsonify(products)

@app.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Получить товар по ID"""
    product = next((prod for prod in products if prod["id"] == product_id), None)
    return jsonify(product) if product else ('Not Found', 404)

if __name__ == '__main__':
    app.run(port=5001, debug=True)