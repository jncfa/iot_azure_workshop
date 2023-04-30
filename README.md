# iot_azure_workshop
> Instructions for replicating class nº7 and 8 of Internet of Things for Microsoft Azure.

## How to use this repository

The Python scripts are adapted versions of the previous mqtt bridge scripts for Azure, supporting only SAS (X.509 certificate support for Azure requires a self-hosted PKI setup and will not be discussed here).

For starters, download this repository to your local drive and download DigiCert's Baltimore CyberTrust Root for connecting to the Azure IoT Hub with TLS: [https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem](https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem)

### Connecting with SAS
To use SAS, you need to do the following steps:
- Create an IoT hub (ensure it's in the free tier, otherwise you might get charged).
- Create a device in your IoT hub. 
- Create a cloud shell using the "terminal" button on the top bar on the Azure Portal:
![https://i.imgur.com/ZM7RNkv.png](https://i.imgur.com/ZM7RNkv.png)
- Use the following command to generate a SAS token for your device, replacing `{device_id}` with the ID of the device created and `{iothub_name}` with the name of the IoT hub you chose: 
    - Please note this token will expire in 1 month or 2628000s after creating it, you can change this by indicating a different token duration on the `--du` parameter.
```bash
az iot hub generate-sas-token -d {device_id} -n {iothub_name} --du 2628000
```
- Replace the SAS token and path of the Baltimore CyberTrust Root file you downloaded previously on any of the Python scripts provided. 

We are now ready to test the connection to the Azure IoT hub. To test the device-to-cloud transmissions, do the following:
 - Using the cloud shell that was created previously, run the following command, replacing `{device_id}` with the ID of the device created and `{iothub_name}` with the name of the IoT hub you chose: 
```bash
    az iot hub monitor-events -n {iothub_name} -d {device_id}
```
 - Run `mqtt-publisher.py` and see if any event is detected on the cloud shell.

To test the cloud-to-device transmissions, do the following:
- Run the `mqtt-subscriber.py`.
- Using the cloud shell that was created previously, run the following command, r replacing `{device_id}` with the ID of the device created and `{iothub_name}` with the name of the IoT hub you chose, and see if any messages show up on the `mqtt-subscriber` running on your VM: 
```bash
    az iot device c2d-message send --hub-name {iothub_name} --device-id {device_id} --data "hello world"
```

## Routing messages to a database on the cloud

At this point, you should already be able to send messages to the cloud, but nothing should be happening, as we haven't defined any data processing pipelines.

For starters, we can route the messages from IoT hub to a Cosmos DB (currently in preview mode, but accessible and working). To acheive this, follow these instructions:
- Create a [Cosmos DB account for NoSQL](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.DocumentDb%2FdatabaseAccounts). 
    - Be careful selecting the regions, not all regions have availablity and will error when deploying. To ensure it will work, choose only the recommended regions (as of April 30th, West Europe should work).
- Go to Containers > Browse > Add Container, and create a database and collection. You can leave the default configurations, just make sure to remember the names of the database and collection you've created.
![https://i.imgur.com/TS2RevM.png](https://i.imgur.com/TS2RevM.png)

Now we need to define a message route that will reroute the message received on the IoT hub to the database. For this, we need to:
- Go to our "IoT Hub > Message Routing > Add" to add a new route.
![https://i.imgur.com/AgivSJt.png](https://i.imgur.com/AgivSJt.png)
- Click on Add endpoint > Cosmos DB (preview), and configure it with your database name and collection name you've created previously. 
![https://i.imgur.com/XCD7K0d.png](https://i.imgur.com/XCD7K0d.png)
- Afterwards, fill the Message Routing, and add the new Cosmos DB custom endpoint you just created, disable the synthetic partition key for now. You can also add special rules for filtering messages to have specific processing pipelines, but let's ignore this for now.

At this point you should be able to send messages to the cloud, which will be stored in the Cosmos DB database. To test this, do the following:
- Start `mqtt-publisher.py`.
- Go to the Cosmos DB > Containers > Browse, and select the container you created.
- You should start seeing the messages arriving in the "Items" tab.
![https://i.imgur.com/stCdIsf.png](https://i.imgur.com/stCdIsf.png)