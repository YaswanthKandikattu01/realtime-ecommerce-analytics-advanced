-- Example Snowflake schema for e-commerce analytics

CREATE OR REPLACE TABLE dim_customer (
  customer_id STRING PRIMARY KEY,
  country     STRING
);

CREATE OR REPLACE TABLE dim_product (
  product_id   STRING PRIMARY KEY,
  product_name STRING,
  category     STRING
);

CREATE OR REPLACE TABLE fact_order_item (
  order_id     STRING,
  customer_id  STRING,
  product_id   STRING,
  currency     STRING,
  unit_price   NUMBER(18,2),
  quantity     NUMBER(18,0),
  line_total   NUMBER(18,2),
  order_ts     TIMESTAMP_NTZ
);
