# iot_azure_workshop
> Instructions for replicating class nº7 and 8 of Internet of Things for Microsoft Azure.

## How to use this repository

The Python scripts are adapted versions of the previous mqtt bridge scripts for Azure, supporting only SAS (X.509 certificate support for Azure requires a self-hosted PKI setup and will not be discussed here).

For starters, download this repository to your local drive and download DigiCert's Baltimore CyberTrust Root for connecting to the Azure IoT Hub with TLS: [https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem](https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem)

Depending on what method of connecting you'll be using with your devices, you'll need to perform different steps, choose the method you'll be using and follow the instructions.

### Connecting with SAS
To use SAS, you need to do the following steps:
- Create an IoT hub (ensure it's in the free tier, otherwise you might get charged).
- Create a device in your IoT hub. 
- Create a cloud shell using the "terminal" button on the top bar on the Azure Portal:
![https://i.imgur.com/ZM7RNkv.png](https://i.imgur.com/ZM7RNkv.png)
- Use the following command to generate a SAS token for your device: 
    - Please note this token will expire in 1 month or 2628000s after creating it.
```bash
az iot hub generate-sas-token -d {device_id} -n {iothub_name} --du 2628000
```
- Replace the SAS token and path of the Baltimore CyberTrust Root file you downloaded previously on any of the Python scripts provided. 

## Routing messages to a database on the cloud

At this point, you should already be able to send messages to the cloud, but nothing should be happening, as we haven't defined any data processing pipelines.

For starters, we can route the messages from IoT hub to a Cosmos DB (currently in preview mode, but accessible and working). To acheive this, follow these instructions:
- Create a [Cosmos DB account for NoSQL](https://portal.azure.com/#view/HubsExtension/BrowseResource/resourceType/Microsoft.DocumentDb%2FdatabaseAccounts). 
    - Be careful selecting the regions, not all regions have availablity and will error when deploying. To ensure it will work, choose only the recommended regions (as of April 30th, West Europe should work).
- Go to Containers > Browse > Add Container, and create a database and collection. You can leave the default configurations, just make sure to remember the names of the database and collection you've created.

Now we need to define a message route that will reroute the message received on the IoT hub to the database. For this, we need to:
- Go to our IoT Hub > Message Routing > Add to add a new route.
- Click on Add endpoint > Cosmos DB (preview), and configure it with your database name and collection name you've created previously. Disable the synthetic partition key for now.
