from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, timezone

from . import models, schemas

def create_order(db: Session, order_data: schemas.OrderCreate) -> models.Order:
    total_amount = 0.0
    order = models.Order(
        order_id=order_data.order_id,
        customer_id=order_data.customer_id,
        country=order_data.country,
        currency=order_data.currency,
    )
    db.add(order)
    db.flush()

    for item in order_data.items:
        line_total = item.unit_price * item.quantity
        total_amount += line_total
        db_item = models.OrderItem(
            order_id=order.id,
            product_id=item.product_id,
            product_name=item.product_name,
            category=item.category,
            unit_price=item.unit_price,
            quantity=item.quantity,
            line_total=line_total,
        )
        db.add(db_item)

    order.total_amount = total_amount
    db.commit()
    db.refresh(order)
    return order