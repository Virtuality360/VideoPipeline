#!/usr/bin/env python3
import pika
import sys

# Change the credentials
# Can't use enviroment variables?
amqp_host = ""
amqp_port = 0
ampq_credentials = pika.PlainCredentials("", "")  # Username, Password

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=amqp_host, port=amqp_port, credentials=ampq_credentials
    )
)
channel = connection.channel()

channel.exchange_declare(exchange="bucketevents", exchange_type="topic")

result = channel.queue_declare(exclusive=True, queue='')
queue_name = result.method.queue

binding_keys = sys.argv[1:]
if not binding_keys:
    sys.stderr.write("Usage: %s [binding_key]...\n" % sys.argv[0])
    sys.exit(1)

for binding_key in binding_keys:
    channel.queue_bind(
        exchange="bucketevents", queue=queue_name, routing_key=binding_key
    )

print(" [*] Waiting for logs. To exit press CTRL+C")


def callback(ch, method, properties, body):
    print(" [x] %r:%r" % (method.routing_key, body))


channel.basic_consume(queue=queue_name, on_message_callback=callback, auto_ack=True)

channel.start_consuming()
