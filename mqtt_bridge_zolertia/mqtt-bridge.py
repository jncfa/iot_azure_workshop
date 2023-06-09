# This "bridge" script subscribes to messages inside the 6LoWPAN network using unencrypted MQTT
# and then publishes the messages securely to the MQTT broker in the AWS cloud using TLS/SSL

# You can easily change this script, in case you need to subscribe to topics from the AWS cloud 
# and publish them locally in the 6LoWPAN network.

# Libraries:
import paho.mqtt.client as mqtt
import ssl
import sys


############ Please change these parameters for your own setup #########


# There is a Mosquitto server running locally on the Virtual Machine. 
# For the project, you should change this to the IPv6 server of the local MQTT broker:
LOCAL_MQTT_URL = "localhost"
# You may also try "test.mosquitto.org"

# A topic to get and send information from the zolertia board(s), respectively:	 
LOCAL_TOPIC_SUB = "zolertia/sensor_status"
LOCAL_TOPIC_PUB = "zolertia/devicebound"

# Connection parameters for the Azure IoT Hub:
PATH_TO_ROOT_CERT  = "<local path to digicert.crt.pem file>"
DEVICE_ID = "<device id from Azure's device registry>"
SAS_TOKEN = "<generated SAS token>"
IOT_HUB_NAME = "<iot hub name>"

# Address of the Cloud MQTT Broker for Azure IoT Hub and MQTT username of the device:
CLOUD_MQTT_URL = "{}.azure-devices.net".format(IOT_HUB_NAME)
USERNAME = "{}/{}/?api-version=2021-04-12".format(CLOUD_MQTT_URL, DEVICE_ID)

# Topics to send and get information from the cloud respectively:
JSON_METADATA = "$.ct=application%2Fjson%3Bcharset%3Dutf-8"	 
CLOUD_TOPIC_PUB = "devices/{}/messages/events/{}".format(DEVICE_ID, JSON_METADATA)
CLOUD_TOPIC_SUB = "devices/{}/messages/devicebound".format(DEVICE_ID)

#########################################################################

# Callback for initial local network connection:
def on_connect_lc(local_client, userdata, flags, rc):
    print("Connected to local MQTT broker with result code " + str(rc))
    local_client.subscribe(LOCAL_TOPIC_SUB)
    print("Subscribed to local topic: " + LOCAL_TOPIC_SUB + "\n")

def on_connect_cc(cloud_client, userdata, flags, rc):
    print("Connected to cloud MQTT broker with result code " + str(rc))
    cloud_client.subscribe(CLOUD_TOPIC_SUB + "/#") # add wildcard flag to subscribe to all subtopics
    print("Subscribed to cloud topic: " + CLOUD_TOPIC_SUB + "\n")

# Callback for received message in the local network:
def on_local_message(local_client, userdata, msg):
    #publish the exact same message on the MQTT broker in the cloud:
    print("Local -> Cloud: Topic [" + CLOUD_TOPIC_PUB + "]. Msg \""+str(msg.payload)+"\"")
    cloud_client.publish(CLOUD_TOPIC_PUB, str(msg.payload))

# Callback for received message in the cloud:
def on_cloud_message(cloud_client, userdata, msg):
    #publish the exact same message on the local MQTT broker:
    print("Cloud -> Local: Topic [" + LOCAL_TOPIC_PUB + "]. Msg \""+str(msg.payload)+"\"")
    local_client.publish(LOCAL_TOPIC_PUB, str(msg.payload))

#########################################################################

# 1st connect to the Cloud MQTT Client:
print("Connecting to the Cloud at " + CLOUD_MQTT_URL + "...")
cloud_client=client = mqtt.Client(client_id=DEVICE_ID, protocol=mqtt.MQTTv311)
cloud_client.username_pw_set(username=USERNAME, 
                             password=SAS_TOKEN)

cloud_client.tls_set(ca_certs=PATH_TO_ROOT_CERT, certfile=None, keyfile=None, tls_version=ssl.PROTOCOL_TLSv1_2, ciphers=None)
cloud_client.tls_insecure_set(False)

cloud_client.on_message = on_cloud_message
cloud_client.on_connect = on_connect_cc

cloud_client.connect(CLOUD_MQTT_URL, 8883, 60)
print("Connected to the Cloud MQTT Broker.")

# Then conect to the Local MQTT Client:
local_client = mqtt.Client()
local_client.on_connect = on_connect_lc
local_client.on_message = on_local_message

print("Connecting locally to " + LOCAL_MQTT_URL + "...")
local_client.connect(LOCAL_MQTT_URL, 1883, 60)

# If we had just 1 connection we coud use client.loop_forever()
# since we have two, we'll use a while loop this way:

try:
   while True:
        local_client.loop(0.01) # timeout of 0.01 secs (max 100Hz)
        cloud_client.loop(0.01)

except (KeyboardInterrupt): #catch keyboard interrupts
        sys.exit()


# You can test by running on your VM:
# mosquitto_pub -h localhost -t zolertia/sensor_status -m "Publiquei esta msg localmente e a bridge fez forward para a cloud!"

# Also test publishing something in the cloud and check if you receive it locally with:
# mosquitto_sub -h localhost -t cloud/action


