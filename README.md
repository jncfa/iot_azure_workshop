# iot_azure_workshop
> English instructions for replicating class nº7 and 8 of Internet of Things for Microsoft Azure.

## How to use this repository

This repository contains the English instructions for the IoT class lectures regarding Microsoft Azure, as well as some Python scripts used to facilitate the connection to the cloud service.

For starters, download this repository to your local drive and download DigiCert's Baltimore CyberTrust Root for connecting to the Azure IoT Hub with TLS: [https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem](https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem)

## Microsoft Azure - Cloud Computing Services

As an example of a cloud service, we will be using Microsoft's cloud, Microsoft Azure. For the final project, the use of this service is not mandatory. You can use other services such as AWS from Amazon, The Things.IO, Google Cloud, Ubidots, among others. Alternatively, if you prefer, you can run a local cloud on your PC.

### Creating a student account on Microsoft Azure
Azure allows you to create a student account where you will have access to $100 in credits that can be used in the first 12 months. In addition, you will have access to a set of free services without the need to provide a credit card at registration.

The following steps will be presented to create a student account on Azure:

- Go to the Azure for Students registration page: https://aka.ms/azureforstudents.
- Enter the email you want to use to create the Azure account. We suggest using a personal email so that the account can continue to be accessible after you finish your course. You can always create a new Microsoft email, although this is not necessary.
- Verification of identity as a student: First, it will be necessary to associate a mobile number with the account. An SMS will be sent to this number with a validation code. Later, a form will appear to verify your association with the University of Coimbra. In the "Verification Method" field, select the "School Email Address" option and enter your UC email (ucxxxxxxx@student.uc.pt). You will receive a confirmation message with a link to follow at that email address.
- After this process, you will be redirected to the Azure portal's homepage. If you are not automatically redirected, you can navigate to the following address: https://portal.azure.com/
- On the homepage, you will have access to a summary of the expenses already made and the remaining balance. You can also use the homepage to navigate to the various services provided by Azure. Our initial focus will be on the IoT Hub service. If you do not find it in the initial menu, select the "Explore All" option to access the complete listing of services offered.

To get an idea of the free services you will have access to with your student account, you can follow this link:
https://azure.microsoft.com/en-us/free/students/

### How to create an IoT Hub on Microsoft Azure
An IoT Hub is a service provided by Microsoft Azure that allows us to connect our IoT devices to the cloud. The Hub acts as a bridge between the devices and the cloud, allowing data sent by these devices to be stored and analyzed. It enables secure and reliable bidirectional communication (from device to cloud [D2C] and from cloud to device [C2D]) using commonly used IoT communication protocols such as HTTP, MQTT, and AMQP.

For more information on this service, you can refer to the Microsoft Azure IoT Hub documentation. To add a new Hub, you can follow these steps:

- Navigate to the IoT Hub page.A
- Click on "Add Device."
- In the form, select the following options:
    - a. Subscription: Azure for Students
    - b. Resource Group: Create a new resource group called IOT_Class (or another name you choose)
    - c. Enter the name of the Hub (for example: IoT-Class-Hub)
    - d. Region: West Europe (geographic region where the Hub servers will be located)
    - e. Tier: Free
    - f. Daily Message Limit: 8,000 (limit of the free version)  

- Select the "Review+Create" option to confirm the addition of the new IoT Hub.

> :memo: Take note of this: With the Student account, only one IoT Hub will be entitled to exchange 8,000 messages per day completely free of charge. Additional hubs may charge a fee depending on the number of messages exchanged between the hub and the device. It may take a few minutes for the hub to become active!

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

### Routing messages to a database on the cloud

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
