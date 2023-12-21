import sys
import ssl
import json
import paho.mqtt.client as paho
import serial
import time

client = paho.Client()

# Setare username și parolă
client.username_pw_set('sergiu.doncila', 'QWEasd!@#123')

# Setare SSL/TLS
client.tls_set()

if client.connect('9b7b323ee67e46d18f9317162c8e8841.s1.eu.hivemq.cloud', 8883, 60) != 0:
    print("Couldn't connect to the MQTT broker")
    sys.exit(1)

# Configurați și deschideți portul serial
ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
ser.flush()

try:
    while True:
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            # Presupunem că linia primită este un JSON valid
            try:
                data = json.loads(line)
                client.publish('microlab/automotive/device/car/us/status', json.dumps(data), 0)
            except json.JSONDecodeError:
                print("Received non-JSON data:", line)

except KeyboardInterrupt:
    print("Exiting...")
finally:
    print("Closing Serial Port and Disconnecting from the MQTT broker")
    ser.close()
    client.disconnect()