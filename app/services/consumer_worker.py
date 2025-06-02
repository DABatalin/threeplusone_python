from app.services.kafka_consumer import KafkaConsumerService

def main():
    """
    Main function to run the Kafka consumer
    """
    consumer = KafkaConsumerService()
    try:
        print("Starting Kafka consumer...")
        consumer.start_consuming()
    except KeyboardInterrupt:
        print("Stopping Kafka consumer...")
    except Exception as e:
        print(f"Error in consumer: {e}")

if __name__ == "__main__":
    main() 