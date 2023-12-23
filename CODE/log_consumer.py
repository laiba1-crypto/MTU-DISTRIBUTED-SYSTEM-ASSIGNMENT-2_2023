import pika

RABBITMQ_HOST = 'localhost'
RABBITMQ_PORT = 5672
RABBITMQ_QUEUE = 'activity_logs'

# Connect to RabbitMQ
connection = pika.BlockingConnection(pika.ConnectionParameters(host=RABBITMQ_HOST, port=RABBITMQ_PORT))
channel = connection.channel()

# Queue
channel.queue_declare(queue=RABBITMQ_QUEUE)

def callback(ch, method, properties, body):
    print(f"Log message received: {body}")

# Configure the user to receive messages from the queue.
channel.basic_consume(queue=RABBITMQ_QUEUE, on_message_callback=callback, auto_ack=True)

print("Awaiting messages from the activity_logs. Press 'CTRL+C' to exit.")
channel.start_consuming()
