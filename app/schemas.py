from typing import List
from datetime import datetime
from pydantic import BaseModel

class OrderItemCreate(BaseModel):
    product_id: str
    product_name: str
    category: str
    unit_price: float
    quantity: int

class OrderCreate(BaseModel):
    order_id: str
    customer_id: str
    country: str
    currency: str = "USD"
    items: List[OrderItemCreate]

class OrderItemOut(BaseModel):
    product_id: str
    product_name: str
    category: str
    unit_price: float
    quantity: int
    line_total: float

    class Config:
        from_attributes = True

class OrderOut(BaseModel):
    order_id: str
    customer_id: str
    country: str
    currency: str
    total_amount: float
    created_at: datetime
    items: list[OrderItemOut]

    class Config:
        from_attributes = True

class SummaryMetrics(BaseModel):
    total_orders: int
    total_revenue: float
    avg_order_value: float
    unique_customers: int

class TimeBucket(BaseModel):
    bucket: str
    value: float

class TopProduct(BaseModel):
    product_name: str
    revenue: float
    quantity: int

class RealTimePayload(BaseModel):
    summary: SummaryMetrics
    revenue_last_10_min: list[TimeBucket]
    top_products: list[TopProduct]