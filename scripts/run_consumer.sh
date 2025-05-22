#!/bin/bash

# Wait for Kafka and ClickHouse to be ready
echo "Waiting for Kafka and ClickHouse to be ready..."
sleep 10

# Run the consumer
python -m app.services.consumer_worker 