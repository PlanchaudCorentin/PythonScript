import pika
import time
import random
import json
import sys

ip = '192.168.43.88'
u = "admin"
p = "devproject"
q = 'Test'
d = 1

i = 0
for arg in sys.argv:
    if arg == "-ip":
        ip = sys.argv[i + 1]
    if arg == "-u":
        u = sys.argv[i + 1]
    if arg == "-p":
        p = sys.argv[i + 1]
    if arg == "-q":
        q = sys.argv[i + 1]
    if arg == "-d":
        d = float(sys.argv[i + 1])
    i += 1

credentials = pika.PlainCredentials(u, p)
connection = pika.BlockingConnection(pika.ConnectionParameters(ip, credentials=credentials))
channel = connection.channel()
channel.exchange_declare(exchange='metrics', exchange_type='fanout', durable='false')
# channel.queue_declare(q, durable='false')

macAddress = ["44:81:C0:0D:6C:E3", "44:81:C0:0D:6C:E4", "44:81:C0:0D:6C:E5", "44:81:C0:0D:6C:E6"]
name = ["humiditySensor", "temperatureSensor"]

loop = 0
t_end = time.time() + d
print(t_end)
while time.time() < t_end:
    loop = loop + 1
    body = {
        "name": "Antoine",
        "metricValue": random.randint(-10, 30),
        "deviceType": name[random.randint(0, 1)],
        "macAddress": macAddress[random.randint(0, 3)],
        "metricDate": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
    }
    channel.basic_publish(exchange='metrics', routing_key='', body=json.dumps(body))
# print(loop)
# print(t_end - time.time())
print("Sent")
print(loop)
