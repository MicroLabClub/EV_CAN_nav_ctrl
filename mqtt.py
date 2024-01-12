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

def parse_sensor_data(line):
    try:
        # Extract numerical values from the line
        values = [float(val.split()[0]) for val in line.split('m') if val.strip()]
        sensor_data = (
            "{"
            f"\"sensor_id\": 1234, "  # Static sensor ID, change as needed
            f"\"us1\": {values[0] if len(values) > 0 else 0}, "
            f"\"us2\": {values[1] if len(values) > 1 else 0}, "
            f"\"us3\": {values[2] if len(values) > 2 else 0}, "
            f"\"us4\": {values[3] if len(values) > 3 else 0}"
            "}"
        )
        return sensor_data
    except ValueError:
        # Handle cases where conversion to float fails
        return None

try:
	print("Press CTRL+C to exit...")
    while True:
        client.loop_start()
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8', errors='replace').rstrip()

            if line not in ignored_messages:
                sensor_data_str = parse_sensor_data(line)
                if sensor_data_str:
                    client.publish('microlab/automotive/device/car/us/status', sensor_data_str)
        client.loop_stop()
except KeyboardInterrupt:
	print("Exiting...")
except Exception as e:
	print(f"Caught an Exception, something went wrong... {e}")
finally:
	print("Disconnecting from the MQTT broker")
	ser.close()
	client.disconnect()
