#!/usr/bin/env bash
set -e

KAFKA_CONTAINER=${KAFKA_CONTAINER:-$(docker ps --filter "ancestor=confluentinc/cp-kafka:7.5.0" --format "{{.ID}}" | head -n1)}

if [ -z "$KAFKA_CONTAINER" ]; then
  echo "Kafka container not found. Make sure docker-compose is running."
  exit 1
fi

docker exec -it "$KAFKA_CONTAINER" kafka-topics --create --topic orders_raw --bootstrap-server localhost:9092 --replication-factor 1 --partitions 3 || true
echo "Topics created (or already exist)."
