import os
from pyspark.sql import SparkSession
from pyspark.sql.functions import from_json, col, explode
from pyspark.sql.types import StructType, StructField, StringType, DoubleType, IntegerType, ArrayType

KAFKA_BOOTSTRAP_SERVERS = os.getenv("KAFKA_BOOTSTRAP_SERVERS", "kafka:9092")
KAFKA_ORDERS_TOPIC = os.getenv("KAFKA_ORDERS_TOPIC", "orders_raw")

MINIO_ENDPOINT = os.getenv("MINIO_ENDPOINT", "http://minio:9000")
MINIO_ACCESS_KEY = os.getenv("MINIO_ACCESS_KEY", "minioadmin")
MINIO_SECRET_KEY = os.getenv("MINIO_SECRET_KEY", "minioadmin")
MINIO_BUCKET = os.getenv("MINIO_BUCKET", "ecommerce-raw")

def main():
    spark = (
        SparkSession.builder.appName("EcommerceOrdersStreaming")
        .config("spark.hadoop.fs.s3a.endpoint", MINIO_ENDPOINT)
        .config("spark.hadoop.fs.s3a.access.key", MINIO_ACCESS_KEY)
        .config("spark.hadoop.fs.s3a.secret.key", MINIO_SECRET_KEY)
        .config("spark.hadoop.fs.s3a.path.style.access", "true")
        .config("spark.hadoop.fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
        .getOrCreate()
    )

    spark.sparkContext.setLogLevel("WARN")

    item_schema = StructType(
        [
            StructField("product_id", StringType()),
            StructField("product_name", StringType()),
            StructField("category", StringType()),
            StructField("unit_price", DoubleType()),
            StructField("quantity", IntegerType()),
        ]
    )

    order_schema = StructType(
        [
            StructField("order_id", StringType()),
            StructField("customer_id", StringType()),
            StructField("country", StringType()),
            StructField("currency", StringType()),
            StructField("items", ArrayType(item_schema)),
        ]
    )

    df_raw = (
        spark.readStream.format("kafka")
        .option("kafka.bootstrap.servers", KAFKA_BOOTSTRAP_SERVERS)
        .option("subscribe", KAFKA_ORDERS_TOPIC)
        .option("startingOffsets", "latest")
        .load()
    )

    df_parsed = df_raw.selectExpr("CAST(value AS STRING) as json_str").select(
        from_json(col("json_str"), order_schema).alias("data")
    )

    df_orders = df_parsed.select(
        col("data.order_id"),
        col("data.customer_id"),
        col("data.country"),
        col("data.currency"),
        explode(col("data.items")).alias("item"),
    ).select(
        "order_id",
        "customer_id",
        "country",
        "currency",
        col("item.product_id").alias("product_id"),
        col("item.product_name").alias("product_name"),
        col("item.category").alias("category"),
        col("item.unit_price").alias("unit_price"),
        col("item.quantity").alias("quantity"),
        (col("item.unit_price") * col("item.quantity")).alias("line_total"),
    )

    output_path = f"s3a://{MINIO_BUCKET}/orders"

    query = (
        df_orders.writeStream.outputMode("append")
        .format("parquet")
        .option("checkpointLocation", f"{output_path}_checkpoint")
        .option("path", output_path)
        .start()
    )

    query.awaitTermination()

if __name__ == "__main__":
    main()
