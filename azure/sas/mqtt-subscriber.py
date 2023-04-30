import time
import paho.mqtt.client as mqtt
import ssl
import sys

# Connection parameters for the Azure IoT Hub:
PATH_TO_ROOT_CERT  = "<local path to digicert.crt.pem file>"
DEVICE_ID = "<device id from Azure's device registry>"
SAS_TOKEN = "<generated SAS token>"
IOT_HUB_NAME = "<iot hub name>"

# Address of the Cloud MQTT Broker for Azure IoT Hub and MQTT username of the device:
CLOUD_MQTT_URL = "{}.azure-devices.net".format(IOT_HUB_NAME)
USERNAME = "{}/{}/?api-version=2021-04-12".format(CLOUD_MQTT_URL, DEVICE_ID)

# Topic to get information from the cloud:
CLOUD_TOPIC_SUB = "devices/{}/messages/devicebound".format(DEVICE_ID)

#Override MQTT_TOPIC from the cmd line:
if len(sys.argv) > 1:
  CLOUD_TOPIC = str(sys.argv[1])

def on_message(client, userdata, msg):
    print(msg.topic + " " + str(msg.payload))

def on_subscribe(mqttc, obj, mid, granted_qos):
    print("Subscribed: " + str(mid) + " " + str(granted_qos))

print("Connecting to Cloud MQTT Broker")
client = client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(username=USERNAME,
                       password=SAS_TOKEN)

client.tls_set(ca_certs=PATH_TO_ROOT_CERT, certfile=None,
               keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(False)
client.on_message = on_message
client.on_subscribe = on_subscribe

client.connect(CLOUD_MQTT_URL, 8883, 60)
print("Setup a subscriber in topic: \""+CLOUD_TOPIC_SUB+"\"")
client.subscribe(CLOUD_TOPIC_SUB+"/#")

try: 
	client.loop_forever()

except (KeyboardInterrupt):
        sys.exit()


