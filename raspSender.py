import sys
import pika
import Adafruit_DHT
import time
import threading
from Queue import Queue
import getmac
import json


def run(queue, chan):
    while True:
        temp = queue.get()
        body = {
            "name": "Antoine",
            "metricValue": temp,
            "deviceType": "temperatureSensor",
            "macAddress": getmac.get_mac_address().upper(),
            "metricDate": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())
        }
        print(body)
        chan.basic_publish(exchange="metrics", routing_key='', body=json.dumps(body))
        queue.task_done()
        time.sleep(0.9)


if __name__ == '__main__':
    sensor_args = {'11': Adafruit_DHT.DHT11,
                   '22': Adafruit_DHT.DHT22,
                   '2302': Adafruit_DHT.AM2302}
    if len(sys.argv) == 3 and sys.argv[1] in sensor_args:
        sensor = sensor_args[sys.argv[1]]
        pin = sys.argv[2]
    else:
        print('Usage: sudo ./Adafruit_DHT.py [11|22|2302] <GPIO pin number>')
        print('Example: sudo ./Adafruit_DHT.py 2302 4 - Read from an AM2302 connected to GPIO pin #4')
        sys.exit(1)

    connection = pika.BlockingConnection(
    pika.ConnectionParameters('192.168.43.88', credentials=pika.PlainCredentials('admin', 'devproject')))
    channel = connection.channel()
    m_queue = Queue(maxsize=1)
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    t = threading.Thread(target=run, args=(m_queue, channel))
    t.start()
    while True:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        m_queue.put(temperature)
        if humidity is not None and temperature is not None:
            print('Temp={0:0.1f}*  Humidity={1:0.1f}%'.format(temperature, humidity))
        else:
            print('Failed to get reading. Try again!')
            sys.exit(1)

