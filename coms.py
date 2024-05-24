import serial
import time
import requests
from datetime import date
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.reset_input_buffer()

ser.write(b"Server online\n")
time.sleep(1)

URL = 'http://192.168.11.135:5000/meteodata/create'



i = 0
while True:
    i += 1
    ser.write(b"Data request\n")    
    temp = ser.readline().decode('utf-8').rstrip()
    pres = ser.readline().decode('utf-8').rstrip()
    hum = ser.readline().decode('utf-8').rstrip()
    if i <= 2:
        continue
    
    json = {
    "temperature": temp,
    "pressure": pres,
    "humidity": hum,
    "created": f'{date.today().year}-{date.today().month}-{date.today().day}'
    }
    #print(json['temperature'])
    requests.post(URL, json=json)
    print('request sent')
    time.sleep(2.5)
