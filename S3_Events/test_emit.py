#!/usr/bin/env python
import pika
import sys

amqp_host = "change me"
amqp_port = 0
ampq_credentials = pika.PlainCredentials("", "")  # Username, Password

connection = pika.BlockingConnection(
    pika.ConnectionParameters(
        host=amqp_host, port=amqp_port, credentials=ampq_credentials
    )
)
channel = connection.channel()

channel.exchange_declare(exchange="bucketevents", exchange_type="topic")

routing_key = sys.argv[1] if len(sys.argv) > 2 else "anonymous.info"
message = " ".join(sys.argv[2:]) or "Hello World!"
channel.basic_publish(exchange="bucketevents", routing_key=routing_key, body=message)
print(" [x] Sent %r:%r" % (routing_key, message))
connection.close()
