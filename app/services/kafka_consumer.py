import json
import time
from typing import Dict, Any
from datetime import datetime
from confluent_kafka import Consumer, KafkaError
from clickhouse_driver import Client
from app.core.config import Settings

settings = Settings()

class KafkaConsumerService:
    def __init__(self):
        self.consumer = Consumer({
            'bootstrap.servers': settings.KAFKA_BOOTSTRAP_SERVERS,
            'group.id': 'ecommerce-clickhouse-consumer',
            'auto.offset.reset': 'earliest',
            'session.timeout.ms': 6000,
            'heartbeat.interval.ms': 2000
        })
        self.topic = 'user_actions'
        
        # Use Docker service names when running in container
        clickhouse_host = "clickhouse" if settings.CLICKHOUSE_HOST == "localhost" else settings.CLICKHOUSE_HOST
        
        self.clickhouse_client = Client(
            host=clickhouse_host,
            port=settings.CLICKHOUSE_PORT
        )
        
    def process_message(self, message: Dict[str, Any]) -> None:
        """
        Process message and store in ClickHouse
        """
        try:
            # Extract data from message
            user_id = message.get('user_id')
            session_start = datetime.fromisoformat(message.get('session_start'))
            session_end = datetime.fromisoformat(message.get('session_end'))
            click_count = message.get('click_count', 0)
            
            # Insert into ClickHouse
            self.clickhouse_client.execute(
                '''
                INSERT INTO ecommerce.user_sessions 
                (session_id, user_id, session_start, session_end, click_count, created_at)
                VALUES
                ''',
                [(
                    message.get('session_id'),
                    user_id,
                    session_start,
                    session_end,
                    click_count,
                    datetime.now()
                )]
            )
        except Exception as e:
            print(f"Error processing message: {e}")

    def start_consuming(self) -> None:
        """
        Start consuming messages from Kafka
        """
        max_retries = 5
        retry_delay = 5  # seconds
        
        for attempt in range(max_retries):
            try:
                print(f"Attempting to connect to Kafka (attempt {attempt + 1}/{max_retries})...")
                self.consumer.subscribe([self.topic])
                
                while True:
                    msg = self.consumer.poll(1.0)
                    
                    if msg is None:
                        continue
                    if msg.error():
                        if msg.error().code() == KafkaError._PARTITION_EOF:
                            continue
                        else:
                            print(f"Consumer error: {msg.error()}")
                            break
                    
                    try:
                        # Parse message value
                        message = json.loads(msg.value().decode('utf-8'))
                        self.process_message(message)
                    except json.JSONDecodeError as e:
                        print(f"Error decoding message: {e}")
                    except Exception as e:
                        print(f"Error processing message: {e}")
                        
            except Exception as e:
                print(f"Error in consumer loop: {e}")
                if attempt < max_retries - 1:
                    print(f"Retrying in {retry_delay} seconds...")
                    time.sleep(retry_delay)
                    retry_delay *= 2  # Exponential backoff
                else:
                    print("Max retries reached. Exiting...")
                    break
            finally:
                try:
                    self.consumer.close()
                except Exception as e:
                    print(f"Error closing consumer: {e}") 