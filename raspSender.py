import sys
import pika
import Adafruit_DHT
import time
import math


sensor_args = { '11': Adafruit_DHT.DHT11,
                '22': Adafruit_DHT.DHT22,
                '2302': Adafruit_DHT.AM2302 }
if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
    sensor = sensor_args[sys.argv[1]]
    pin = sys.argv[2]
else:
    print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
    print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
    sys.exit(1)

connection = pika.BlockingConnection(pika.ConnectionParameters('192.168.43.88', credentials=pika.PlainCredentials('admin', 'devproject')))
channel = connection.channel()

channel.queue_declare('Rasp', durable='false')

t_end = time.time() + 10
while time.time() < t_end:
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    if humidity is not None and temperature is not None:
        print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        body = temperature
        channel.basic_publish(exchange="", routing_key='Rasp', body=str(body))
        reftime = time.time()
        time.sleep(abs(math.trunc(reftime) + 0.9 - reftime))
    else:
        print('Failed to get reading. Try again!')
        sys.exit(1)
