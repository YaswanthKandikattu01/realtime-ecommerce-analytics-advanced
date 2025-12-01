# Real-Time E‑Commerce Analytics Pipeline (Advanced)

This repo contains **Intermediate** and **Industry‑style** versions of a real‑time
e‑commerce analytics pipeline that you can directly push to GitHub and talk about in
interviews.

## Levels

### 2️⃣ Intermediate – Streaming Data Engineering with Docker

**Tech stack:**

- FastAPI **Ingestion API**
- Apache Kafka (orders events)
- PySpark Structured Streaming
- S3‑compatible storage (MinIO)
- Docker & Docker Compose
- Optional Kafka UI

**Flow:**

```text
Client / Simulator
      ↓  (HTTP)
  FastAPI Ingestion API
      ↓  (Kafka producer – topic: orders_raw)
    Kafka Broker
      ↓  (Spark Structured Streaming consumer)
  PySpark Streaming Job
      ↓  (Parquet files)
     MinIO (S3 bucket: ecommerce-raw)
```

You can extend the Spark job to also produce **aggregated metrics** into another topic
(e.g. `orders_aggregates`) that a separate service / dashboard could subscribe to.

### 3️⃣ Industry‑style – Batch Analytics & BI

On top of the intermediate stack we add:

- Apache Airflow (orchestration / scheduling)
- Snowflake (cloud data warehouse – configured via environment variables)
- Power BI (BI dashboard – documented steps)

**Extended flow:**

```text
MinIO (S3‑compatible)  --(Airflow DAG: S3 → Snowflake)-->  Snowflake
                                                          ↓
                                                    Power BI Reports
```

Airflow runs a daily/hourly DAG that loads the latest parquet data from S3/MinIO
into Snowflake fact and dimension tables. Power BI then connects to Snowflake.

---

## Repository Structure

```text
.
├── LICENSE
├── README.md
├── docker-compose.intermediate.yml
├── docker-compose.enterprise.yml
├── services/
│   ├── ingestion_api/        # FastAPI app that receives orders and pushes to Kafka
│   │   ├── app/
│   │   └── Dockerfile
│   └── streaming_job/        # PySpark Structured Streaming: Kafka → S3 (MinIO)
│       ├── job/
│       └── Dockerfile
├── infra/
│   ├── kafka/
│   │   └── create-topics.sh
│   └── minio/
│       └── README.md
└── enterprise/
    ├── airflow/
    │   ├── dags/
    │   └── Dockerfile
    ├── snowflake/
    │   ├── schema.sql
    │   └── README.md
    └── powerbi/
        └── README.md
```

---

## Quick Start – Intermediate Stack (Level 2)

### 1. Prerequisites

- Docker & Docker Compose installed
- Ports free: `8000`, `9092`, `29092`, `9000`, `9001`, `8080` (Kafka‑UI)

### 2. Start Services

```bash
docker compose -f docker-compose.intermediate.yml up -d
```

This starts:

- `zookeeper`
- `kafka`
- `minio`
- `kafka-ui`
- `ingestion-api`
- `spark-streaming-job`

### 3. Create Kafka Topics (optional if auto‑create disabled)

```bash
bash infra/kafka/create-topics.sh
```

### 4. Send Test Order Event

```bash
curl -X POST http://localhost:8000/events/order \
  -H "Content-Type: application/json" \
  -d '{
        "order_id": "test-1",
        "customer_id": "CUST-1234",
        "country": "India",
        "currency": "INR",
        "items": [
          {
            "product_id": "P-1001",
            "product_name": "Wireless Mouse",
            "category": "Electronics",
            "unit_price": 799.0,
            "quantity": 2
          }
        ]
      }'
```

The Spark job will read from Kafka (`orders_raw`) and write parquet files into
the MinIO bucket `ecommerce-raw`.

### 5. Access MinIO

- URL: http://localhost:9001
- Default creds (from compose file):
  - Access key: `minioadmin`
  - Secret key: `minioadmin`

---

## Quick Start – Enterprise Stack (Level 3)

⚠ **Note:** This expects you to have valid Snowflake credentials. The repo
contains sample Airflow DAGs and Snowflake DDL, but you must configure:

- `SNOWFLAKE_USER`
- `SNOWFLAKE_PASSWORD`
- `SNOWFLAKE_ACCOUNT`
- `SNOWFLAKE_ROLE`
- `SNOWFLAKE_WAREHOUSE`
- `SNOWFLAKE_DATABASE`
- `SNOWFLAKE_SCHEMA`

### 1. Bring up Enterprise Compose

```bash
docker compose -f docker-compose.enterprise.yml up -d
```

This starts:

- All intermediate services
- Airflow webserver & scheduler
- Postgres for Airflow metadata

### 2. Access Airflow

- URL: http://localhost:8080
- Username: `airflow`
- Password: `airflow`

Enable the DAG: `s3_to_snowflake_ecommerce`.

### 3. Power BI

In `enterprise/powerbi/README.md` you’ll find:

- Steps to connect Power BI Desktop to Snowflake
- Example star‑schema diagram for the e‑commerce model
- Sample measures (DAX) you can create

---

## How to Talk About This in Your Resume

> Built an end‑to‑end real‑time e‑commerce analytics platform using FastAPI,
> Kafka, PySpark Streaming, MinIO (S3), Airflow, Snowflake and Power BI, supporting
> both streaming and batch analytics with Docker‑based orchestration.

You can also mention that you implemented an **Intermediate streaming layer** and an
**Enterprise‑style batch + BI layer** in the same repo.
