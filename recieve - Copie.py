import pika

credentials = pika.PlainCredentials("admin", "devproject")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.43.88', credentials=credentials))
channel = connection.channel()

channel.queue_declare('Test', durable='false')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)

channel.basic_consume(queue='Test',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()