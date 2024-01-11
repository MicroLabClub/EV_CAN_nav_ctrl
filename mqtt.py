import sys
import ssl
import json
import serial
import time
import paho.mqtt.client as paho


def message_handling(client, userdata, msg):
	print(f"{msg.topic}: {msg.payload.decode()}")


client = paho.Client()
client.username_pw_set('sergiu.doncila', 'QWEasd!@#123')
client.tls_set()
client.on_message = message_handling

if client.connect("9b7b323ee67e46d18f9317162c8e8841.s1.eu.hivemq.cloud", 8883, 60) != 0:
	print("Couldn't connect to the mqtt broker")
	sys.exit(1)

client.subscribe("microlab/automotive/device/car/us/status")

ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)

ignored_messages = [
	"Entering Configuration Mode Successful!",
	"Setting Baudrate Successful!",
	"MCP2515 Initialized Successfully!",
	"MCP2515 Driver started..."
]

try:
	print("Press CTRL+C to exit...")
	while True:
		client.loop_start()
		if ser.in_waiting > 0:
			line = ser.readline().decode('utf-8').rstrip()
			print(line)
			if line not in ignored_messages:
				data_to_publish = {
					'us_data': line,  # Aici introducem datele din USB
					'sensor_id': 1
				}

				json_data = json.dumps(data_to_publish)
				client.publish('microlab/automotive/device/car/us/status', json_data)
			else:
				print("Received non-JSON data:", line)
		client.loop_stop()
except KeyboardInterrupt:
	print("Exiting...")
except Exception as e:
	print(f"Caught an Exception, something went wrong... {e}")
finally:
	print("Disconnecting from the MQTT broker")
	ser.close()
	client.disconnect()
