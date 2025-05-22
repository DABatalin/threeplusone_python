from typing import Dict, Any
from confluent_kafka import Producer
from app.core.config import Settings

settings = Settings()

class KafkaProducerService:
    def __init__(self):
        # Use Docker service name when running in container
        kafka_host = "kafka:29092" if "localhost" in settings.KAFKA_BOOTSTRAP_SERVERS else settings.KAFKA_BOOTSTRAP_SERVERS
        
        self.producer = Producer({
            'bootstrap.servers': kafka_host,
            'client.id': 'ecommerce-user-actions',
            'request.timeout.ms': 5000,
            'message.timeout.ms': 5000
        })
        self.topic = 'user_actions'

    def delivery_report(self, err: Any, msg: Any) -> None:
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

    def send_user_action(self, user_id: int, action_data: Dict[str, Any]) -> None:
        """
        Send user action to Kafka topic
        """
        try:
            # Add user_id to action data
            action_data['user_id'] = user_id
            
            # Convert dict to string for Kafka
            import json
            message = json.dumps(action_data)
            
            # Produce message
            self.producer.produce(
                self.topic,
                key=str(user_id),
                value=message,
                callback=self.delivery_report
            )
            
            # Flush to ensure the message is sent
            self.producer.flush()
            
        except Exception as e:
            print(f"Error sending message to Kafka: {e}")

# Create a singleton instance
kafka_producer = KafkaProducerService() 