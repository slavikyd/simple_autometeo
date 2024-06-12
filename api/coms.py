"""Communication for RPi and API server module."""
import logging
import time
from datetime import datetime

import requests
import serial

SERIAL_SPEED = 9600
DELAY = 120
ser = serial.Serial('/dev/ttyUSB0', SERIAL_SPEED, timeout=1)
ser.reset_input_buffer()

ser.write(b'Server online\n')
time.sleep(1)

URL = 'http://5.101.180.71:5000/meteodata/create'

today = datetime.today()

logging.basicConfig(
    filename=f'{today.year}_{today.month}_{today.day}.txt',
    filemode='a',
    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
    datefmt='%H:%M:%S',
    level=logging.DEBUG,
)

logging.info('Running Urban Planning')

logger = logging.getLogger('urbanGUI')

ind = 0
SLEEP_TIME = 2.5
while True:
    ind += 1
    ser.write(b'Data request\n')
    temp = ser.readline().decode('utf-8').rstrip()
    pres = ser.readline().decode('utf-8').rstrip()
    hum = ser.readline().decode('utf-8').rstrip()
    if ind <= 2:
        continue
    else:
        SLEEP_TIME = 300
    json = {
        'temperature': temp,
        'pressure': pres,
        'humidity': hum,
        'created': f'{datetime.today()}',
    }
    requests.post(URL, json=json, timeout=DELAY)
    logging.info(f'Request sent: T = {temp}, P = {pres}, H = {hum}')
    time.sleep(SLEEP_TIME)
