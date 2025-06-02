echo "Waiting for Kafka and ClickHouse to be ready..."
sleep 10

python -m app.services.consumer_worker 