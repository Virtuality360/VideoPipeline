#!/usr/bin/env python3
import pika

# Change the credentials
# Can't use enviroment variables?
amqp_host = "change me"
amqp_port = 0
ampq_credentials = pika.PlainCredentials("", "") # Username, Password

connection = pika.BlockingConnection(
    pika.ConnectionParameters(host=amqp_host, port=amqp_port, credentials=ampq_credentials)
)
channel = connection.channel()

channel.exchange_declare(exchange='bucketevents',
                         exchange_type='fanout')

result = channel.queue_declare(exclusive=True, queue='')
queue_name = result.method.queue

channel.queue_bind(exchange='bucketevents',
                   queue=queue_name)

print(' [*] Waiting for logs. To exit press CTRL+C')

def callback(ch, method, properties, body):
    print(" [x] %r" % body)

channel.basic_consume(on_message_callback=callback,
                      queue=queue_name,
                      auto_ack=True)

channel.start_consuming()
