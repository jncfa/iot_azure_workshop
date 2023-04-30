import time
import paho.mqtt.client as mqtt
import ssl
import sys
import json

# Connection parameters for the Azure IoT Hub:
PATH_TO_ROOT_CERT  = "<local path to digicert.crt.pem file>"
DEVICE_ID = "<device id from Azure's device registry>"
SAS_TOKEN = "<generated SAS token>"
IOT_HUB_NAME = "<iot hub name>"

# Address of the Cloud MQTT Broker for Azure IoT Hub and MQTT username of the device:
CLOUD_MQTT_URL = "{}.azure-devices.net".format(IOT_HUB_NAME)
USERNAME = "{}/{}/?api-version=2021-04-12".format(CLOUD_MQTT_URL, DEVICE_ID)

# A topic to push information to the cloud:
JSON_METADATA = "$.ct=application%2Fjson%3Bcharset%3Dutf-8"	 
CLOUD_TOPIC_PUB = "devices/{}/messages/events/{}".format(DEVICE_ID, JSON_METADATA)

# Override CLOUD_TOPIC from the cmd line:
if len(sys.argv) > 1:
    CLOUD_TOPIC_PUB = str(sys.argv[1])


print("Connecting to the Cloud at " + CLOUD_MQTT_URL + "...")
client = client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(username=USERNAME,
                       password=SAS_TOKEN)

client.tls_set(ca_certs=PATH_TO_ROOT_CERT, certfile=None,
               keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(False)
client.connect(CLOUD_MQTT_URL, 8883, 60)

# start loop to process received messages
# client.loop_start()
pub_count = 0

print("Setup a publisher in topic: \""+CLOUD_TOPIC_PUB+"\"")

while True:
    try:
        msg = json.dumps({"msgid": pub_count})
        print("publishing: " + msg)
        client.publish(CLOUD_TOPIC_PUB, msg)
        pub_count += 1
        # wait to allow publishing continuously
        time.sleep(2)
    except (KeyboardInterrupt):
        sys.exit()
