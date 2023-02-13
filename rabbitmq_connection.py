import pickle

import pika


def consume_messages(queue_name, callback_function):
    """
    Consumes messages from a RabbitMQ queue.
    """
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()
    channel.queue_declare(queue=queue_name)
    channel.basic_consume(queue=queue_name,
                          on_message_callback=callback_function, auto_ack=True)
    print(f"Waiting for messages from queue {queue_name}...")
    channel.start_consuming()


def populate_queue(queue_name: str, urls: list):
    connection = pika.BlockingConnection(
        pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue=queue_name)

    for url in urls:
        channel.basic_publish(exchange='', routing_key=queue_name,
                              body=pickle.dumps(url))

    print(" [x] Sent urls to queue")
    connection.close()
