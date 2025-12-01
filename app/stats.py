from dataclasses import dataclass, field
from collections import deque, Counter
from datetime import datetime, timezone
from typing import Deque, Tuple

from .models import Order

@dataclass
class RealTimeStats:
    total_orders: int = 0
    total_revenue: float = 0.0
    unique_customers: set = field(default_factory=set)
    revenue_per_minute: Deque[Tuple[str, float]] = field(default_factory=deque)
    product_revenue: Counter = field(default_factory=Counter)
    product_quantity: Counter = field(default_factory=Counter)
    max_minutes_window: int = 10

    def update_from_order(self, order: Order):
        self.total_orders += 1
        self.total_revenue += float(order.total_amount)
        self.unique_customers.add(order.customer_id)
        created = order.created_at
        if created.tzinfo is None:
            created = created.replace(tzinfo=timezone.utc)
        bucket = created.strftime("%Y-%m-%d %H:%M")

        if self.revenue_per_minute and self.revenue_per_minute[-1][0] == bucket:
            last_bucket, last_value = self.revenue_per_minute.pop()
            self.revenue_per_minute.append((last_bucket, last_value + float(order.total_amount)))
        else:
            self.revenue_per_minute.append((bucket, float(order.total_amount)))

        while len(self.revenue_per_minute) > self.max_minutes_window:
            self.revenue_per_minute.popleft()

        for item in order.items:
            self.product_revenue[item.product_name] += float(item.line_total)
            self.product_quantity[item.product_name] += int(item.quantity)

    def to_payload_dict(self):
        avg_order_value = self.total_revenue / self.total_orders if self.total_orders > 0 else 0.0
        return {
            "summary": {
                "total_orders": self.total_orders,
                "total_revenue": round(self.total_revenue, 2),
                "avg_order_value": round(avg_order_value, 2),
                "unique_customers": len(self.unique_customers),
            },
            "revenue_last_10_min": [{"bucket": b, "value": v} for b, v in list(self.revenue_per_minute)],
            "top_products": [
                {"product_name": p, "revenue": float(r), "quantity": int(self.product_quantity[p])}
                for p, r in self.product_revenue.most_common(5)
            ],
        }