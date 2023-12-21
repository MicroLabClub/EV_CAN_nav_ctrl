import sys
import ssl
import paho.mqtt.client as paho


def message_handling(client, userdata, msg):
    print(f"{msg.topic}: {msg.payload.decode()}")

client = paho.Client()

# Setare username și parolă
client.username_pw_set('sergiu.doncila', 'QWEasd!@#123')

# Setare SSL/TLS
client.tls_set()

client.on_message = message_handling

# Conectarea la HiveMQ Cloud
if client.connect('9b7b323ee67e46d18f9317162c8e8841.s1.eu.hivemq.cloud', 8883, 60) != 0:
    print("Couldn't connect to the MQTT broker")
    sys.exit(1)

client.subscribe("microlab/automotive/device/car/us/status")

try:
    print("Press CTRL+C to exit...")
    client.loop_forever()
except KeyboardInterrupt:
    print("Exiting...")
except Exception as e:
    print(f"Caught an Exception: {e}")
finally:
    print("Disconnecting from the MQTT broker")
    client.disconnect()