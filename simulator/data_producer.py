import random
import time
import uuid
import requests

BACKEND_URL = "http://127.0.0.1:8000/api/events/order"

PRODUCTS = [
    {"product_id": "P-1001", "product_name": "Wireless Mouse", "category": "Electronics", "price": 799.0},
]

COUNTRIES = ["India"]
CURRENCIES = {"India": "INR"}

def generate_order():
    product = random.choice(PRODUCTS)
    return {
        "order_id": str(uuid.uuid4()),
        "customer_id": "CUST-1",
        "country": "India",
        "currency": "INR",
        "items": [{
            "product_id": product["product_id"],
            "product_name": product["product_name"],
            "category": product["category"],
            "unit_price": product["price"],
            "quantity": 1,
        }],
    }

def main():
    while True:
        order = generate_order()
        requests.post(BACKEND_URL, json=order)
        time.sleep(1)

if __name__ == "__main__":
    main()