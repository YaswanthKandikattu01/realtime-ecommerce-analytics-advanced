# Snowflake Integration

This folder contains:

- `schema.sql` – example dimension/fact tables for e-commerce analytics.
- Example usage for Airflow + Snowflake.

## Steps

1. Create database & schema in Snowflake (or use defaults):

   ```sql
   CREATE DATABASE IF NOT EXISTS ECOMMERCE_DB;
   CREATE SCHEMA IF NOT EXISTS ECOMMERCE_DB.PUBLIC;
   ```

2. Run `schema.sql` in Snowflake to create `dim_customer`, `dim_product`,
   and `fact_order_item`.

3. Configure an **external stage** on S3/MinIO (or use Snowpipe) and load
   parquet data created by the PySpark streaming job into `fact_order_item`.

4. Use `enterprise/airflow/dags/s3_to_snowflake_ecommerce.py` as a template
   for an automated daily load using Airflow.
