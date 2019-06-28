import mysql.connector
from mysql.connector import Error
from mysql.connector import errorcode
from datetime import datetime, timedelta
import random
try:
    db = mysql.connector.connect(host="192.168.43.146", user="dev", passwd="devproject", database="statistics")

    cursor = db.cursor()
    query = """INSERT INTO stats(mac_address, device_type, timestamp, calculated_value) VALUES (%s, %s, %s, %s)"""
    values = []
    start_date = datetime.today()
    start_date = start_date - timedelta(
        days=30,
        seconds=start_date.second,
        minutes=start_date.minute)
    for i in range(744):
        values.append(
            (
                "A4:C4:94:3A:00:14",
                "humiditySensor",
                (start_date + timedelta(hours=i)).strftime('%Y-%m-%d %H:%M:%S'),
                random.randint(-100, 400)/10
            )
        )

    cursor.executemany(query, values)
    db.commit()
except mysql.connector.Error as error:
    print("Failed inserting date object into MySQL table {}".format(error))

finally:
    #closing database connection.
    if db.is_connected():
        cursor.close()
        db.close()
        print("MySQL connection is closed")




