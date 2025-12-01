from datetime import datetime, timedelta
from airflow import DAG
from airflow.operators.python import PythonOperator
import os
import snowflake.connector

SNOWFLAKE_USER = os.getenv("SNOWFLAKE_USER")
SNOWFLAKE_PASSWORD = os.getenv("SNOWFLAKE_PASSWORD")
SNOWFLAKE_ACCOUNT = os.getenv("SNOWFLAKE_ACCOUNT")
SNOWFLAKE_ROLE = os.getenv("SNOWFLAKE_ROLE", "SYSADMIN")
SNOWFLAKE_WAREHOUSE = os.getenv("SNOWFLAKE_WAREHOUSE", "COMPUTE_WH")
SNOWFLAKE_DATABASE = os.getenv("SNOWFLAKE_DATABASE", "ECOMMERCE_DB")
SNOWFLAKE_SCHEMA = os.getenv("SNOWFLAKE_SCHEMA", "PUBLIC")

def load_from_s3_to_snowflake(**context):
    """Placeholder loader: configure external stage + COPY INTO in real setup."""
    if not SNOWFLAKE_USER:
        raise RuntimeError("Snowflake credentials not set in environment.")

    conn = snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        role=SNOWFLAKE_ROLE,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA,
    )
    cur = conn.cursor()
    try:
        cur.execute("SELECT CURRENT_TIMESTAMP()")
        _ = cur.fetchone()
    finally:
        cur.close()
        conn.close()

default_args = {
    "owner": "airflow",
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    dag_id="s3_to_snowflake_ecommerce",
    default_args=default_args,
    description="Load ecommerce parquet data from S3/MinIO into Snowflake",
    start_date=datetime(2025, 1, 1),
    schedule_interval="@daily",
    catchup=False,
) as dag:
    load_task = PythonOperator(
        task_id="load_parquet_to_snowflake",
        python_callable=load_from_s3_to_snowflake,
        provide_context=True,
    )
