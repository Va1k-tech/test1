# Реализация шлюза API Gateway

from fastapi import FastAPI, HTTPException
import httpx

app = FastAPI(title="API Gateway", version="1.0.0")

# Конфигурация URL микросервисов
PRODUCTS_SERVICE = "http://localhost:5001"
ORDERS_SERVICE = "http://localhost:5002"
CUSTOMERS_SERVICE = "http://localhost:5003"

# Таймаут для запросов к микросервисам (в секундах)
TIMEOUT = 5.0

# === МАРШРУТЫ ДЛЯ ТОВАРОВ ===

@app.get("/products")
async def get_products():
    """Получить список всех товаров через Products Service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{PRODUCTS_SERVICE}/products')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Products service unavailable: {str(e)}")

@app.get("/products/{product_id}")
async def get_product(product_id: int):
    """Получить товар по ID через Products Service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{PRODUCTS_SERVICE}/products/{product_id}')
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Product not found")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Products service unavailable: {str(e)}")

# === МАРШРУТЫ ДЛЯ ЗАКАЗОВ ===

@app.get("/orders")
async def get_orders():
    """Получить список всех заказов через Orders Service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{ORDERS_SERVICE}/orders')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Orders service unavailable: {str(e)}")

@app.post("/orders")
async def create_order(order: dict):
    """Создать новый заказ через Orders Service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.post(f'{ORDERS_SERVICE}/orders', json=order)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Orders service unavailable: {str(e)}")

# === МАРШРУТЫ ДЛЯ КЛИЕНТОВ ===

@app.get("/customers")
async def get_customers():
    """Получить список всех клиентов через Customers Service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{CUSTOMERS_SERVICE}/customers')
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Customers service unavailable: {str(e)}")

@app.get("/customers/{customer_id}")
async def get_customer(customer_id: int):
    """Получить клиента по ID через Customers Service"""
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            response = await client.get(f'{CUSTOMERS_SERVICE}/customers/{customer_id}')
            if response.status_code == 404:
                raise HTTPException(status_code=404, detail="Customer not found")
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=503, detail=f"Customers service unavailable: {str(e)}")