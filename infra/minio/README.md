# MinIO Notes

This project uses **MinIO** as an S3‑compatible object store for local development.

- Console: http://localhost:9001
- API endpoint: http://localhost:9000
- Default credentials:
  - Access key: `minioadmin`
  - Secret key: `minioadmin`

The PySpark streaming job writes parquet files into the bucket defined by the
environment variable `MINIO_BUCKET` (default: `ecommerce-raw`).
