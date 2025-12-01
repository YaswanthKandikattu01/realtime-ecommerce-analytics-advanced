import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from kafka import KafkaProducer
import json

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_ORDERS_TOPIC = os.getenv("KAFKA_ORDERS_TOPIC", "orders_raw")

app = FastAPI(title="Real-Time E-Commerce Ingestion API")

class OrderItem(BaseModel):
    product_id: str
    product_name: str
    category: str
    unit_price: float
    quantity: int

class OrderEvent(BaseModel):
    order_id: str
    customer_id: str
    country: str
    currency: str
    items: List[OrderItem]

producer = None

def get_producer():
    global producer
    if producer is None:
        producer = KafkaProducer(
            bootstrap_servers=KAFKA_BOOTSTRAP_SERVERS.split(","),
            value_serializer=lambda v: json.dumps(v).encode("utf-8"),
        )
    return producer

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/events/order")
def ingest_order(order: OrderEvent):
    """Receive a single order event and push it to Kafka."""
    p = get_producer()
    payload = order.dict()
    p.send(KAFKA_ORDERS_TOPIC, payload)
    return {"status": "queued", "topic": KAFKA_ORDERS_TOPIC, "order_id": order.order_id}
