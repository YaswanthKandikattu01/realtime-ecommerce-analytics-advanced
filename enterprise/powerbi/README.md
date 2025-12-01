# Power BI Integration

This folder explains how to connect Power BI to your **Snowflake** data model
created from the e-commerce pipeline.

## Steps

1. Open **Power BI Desktop**.
2. Click **Get Data** → search for **Snowflake**.
3. Enter your Snowflake server, warehouse, database and schema.
4. Select the tables:
   - `DIM_CUSTOMER`
   - `DIM_PRODUCT`
   - `FACT_ORDER_ITEM`
5. Model relationships:
   - `FACT_ORDER_ITEM.customer_id` → `DIM_CUSTOMER.customer_id`
   - `FACT_ORDER_ITEM.product_id` → `DIM_PRODUCT.product_id`

## Example Measures (DAX)

```DAX
Total Revenue = SUM(FACT_ORDER_ITEM[line_total])

Total Orders = DISTINCTCOUNT(FACT_ORDER_ITEM[order_id])

Average Order Value = DIVIDE([Total Revenue], [Total Orders])

Quantity Sold = SUM(FACT_ORDER_ITEM[quantity])
```

## Example Dashboards

- Revenue by country (map or bar chart)
- Top products by revenue
- Daily revenue trend
- Category share of total sales
