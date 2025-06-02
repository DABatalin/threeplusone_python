from confluent_kafka import Producer, Consumer, KafkaError
import json
import time
from datetime import datetime

def delivery_report(err, msg):
    if err is not None:
        print(f'Message delivery failed: {err}')
    else:
        print(f'Message delivered to {msg.topic()} [{msg.partition()}]')

def test_producer():
    # Producer configuration
    producer_conf = {
        'bootstrap.servers': 'localhost:9092',
        'client.id': 'test-producer'
    }

    producer = Producer(producer_conf)
    topic = "test-topic"

    # Send 5 test messages
    for i in range(5):
        message = {
            'id': i,
            'message': f'Test message {i}',
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            producer.produce(
                topic,
                key=str(i),
                value=json.dumps(message),
                callback=delivery_report
            )
            producer.flush()
            print(f"Produced message {i}")
            time.sleep(1)  # Wait a bit between messages
        except Exception as e:
            print(f"Error producing message: {e}")

def test_consumer():
    # Consumer configuration
    consumer_conf = {
        'bootstrap.servers': 'localhost:9092',
        'group.id': 'test-group',
        'auto.offset.reset': 'earliest'
    }

    consumer = Consumer(consumer_conf)
    topic = "test-topic"
    
    try:
        consumer.subscribe([topic])
        
        # Try to consume messages for 30 seconds
        start_time = time.time()
        messages_received = 0
        
        while time.time() - start_time < 30:
            msg = consumer.poll(1.0)
            
            if msg is None:
                continue
            if msg.error():
                if msg.error().code() == KafkaError._PARTITION_EOF:
                    print("Reached end of partition")
                else:
                    print(f"Error: {msg.error()}")
            else:
                messages_received += 1
                value = json.loads(msg.value().decode('utf-8'))
                print(f"Received message: {value}")
                
                # If we've received all 5 test messages, we can stop
                if messages_received >= 5:
                    break
                
    except Exception as e:
        print(f"Error in consumer: {e}")
    finally:
        consumer.close()

if __name__ == "__main__":
    print("Starting Kafka test...")
    print("\nTesting producer...")
    test_producer()
    
    print("\nTesting consumer...")
    test_consumer()
    
    print("\nKafka test completed") 