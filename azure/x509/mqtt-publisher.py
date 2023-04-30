import time
import paho.mqtt.client as mqtt
import ssl
import sys

# Connection parameters for the Azure IoT Hub:
PATH_TO_ROOT_CERT = "<local path to digicert.crt.pem file>"
DEVICE_ID = "<device id from Azure's device registry>"
SAS_TOKEN = "<generated SAS token>"
IOT_HUB_NAME = "<iot hub name>"

# Address of the Cloud MQTT Broker for Azure IoT Hub:
CLOUD_MQTT_URL = f"{IOT_HUB_NAME}.azure-devices.net"

MQTT_TOPIC = "test_topic"

# Override MQTT_TOPIC from the cmd line:
if len(sys.argv) > 1:
    MQTT_TOPIC = str(sys.argv[1])


print("Connecting to the Cloud at " + CLOUD_MQTT_URL + "...")
client = client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
client.username_pw_set(username=f"{CLOUD_MQTT_URL}/{DEVICE_ID}/?api-version=2021-04-12",
                       password=SAS_TOKEN)

client.tls_set(ca_certs=PATH_TO_ROOT_CERT, certfile=None,
               keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
client.tls_insecure_set(False)
client.connect(CLOUD_MQTT_URL, 8883, 60)

# start loop to process received messages
# client.loop_start()
pub_count = 0

print("Setup a publisher in topic: \""+MQTT_TOPIC+"\"")

while True:
    try:
        print("publishing: msg " + str(pub_count))
        client.publish(MQTT_TOPIC, "msg " + str(pub_count))
        pub_count += 1
        # wait to allow publishing continuously
        time.sleep(2)
    except (KeyboardInterrupt):
        sys.exit()
