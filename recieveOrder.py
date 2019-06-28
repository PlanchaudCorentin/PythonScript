import pika
import json
from gpiozero import LED

credentials = pika.PlainCredentials("admin", "devproject")
connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.43.88', credentials=credentials))
channel = connection.channel()

channel.queue_declare('Command', durable='false')

def callback(ch, method, properties, body):
    print(" [x] Received %r" % body)
    j = json.loads(body)
    if(body['commandType'] == "Led"):
        LED(17).

channel.basic_consume(queue='Command',
                      auto_ack=True,
                      on_message_callback=callback)

print(' [*] Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
