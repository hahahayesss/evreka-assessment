import os
import pika
import json
from app import repository

RABBITMQ_HOST = os.getenv("RABBITMQ_HOST", "rabbitmq")
QUEUE_NAME = "location_queue"


def callback(ch, method, properties, body):
    try:
        data = json.loads(body)
        repository.insert(
            data["device_id"],
            data["latitude"],
            data["longitude"],
            data["speed"],
            data["timestamp"]
        )
        ch.basic_ack(delivery_tag=method.delivery_tag)
    except Exception as e:
        print(f"Error processing message: {e}")
        ch.basic_nack(delivery_tag=method.delivery_tag)


def main():
    connection = pika.BlockingConnection(
        pika.ConnectionParameters(
            host=RABBITMQ_HOST
        )
    )
    channel = connection.channel()
    channel.queue_declare(
        queue=QUEUE_NAME,
        durable=True
    )
    channel.basic_qos(
        prefetch_count=1
    )
    channel.basic_consume(
        queue=QUEUE_NAME,
        on_message_callback=callback
    )

    print("Waiting for events...")
    channel.start_consuming()


if __name__ == '__main__':
    main()
