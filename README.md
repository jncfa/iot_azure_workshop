# iot_azure_workshop


## How to use this repository

The Python scripts are adapted versions of the previous mqtt bridge scripts for Azure, supporting only SAS (X.509 certificate support for Azure requires a self-hosted PKI setup).

For starters, download this repository to your local drive and download DigiCert's Baltimore CyberTrust Root for connecting to the Azure IoT Hub with TLS: [https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem](https://cacerts.digicert.com/BaltimoreCyberTrustRoot.crt.pem)

Depending on what method of connecting you'll be using with your devices, you'll need to perform different steps, choose the method you'll be using and follow the instructions.

### Connecting with SAS
To use SAS, you need to do the following steps:
- Create a device in your IoT hub. 
- Create a cloud shell using the "terminal" button on the top bar on the Azure Portal:
![https://i.imgur.com/ZM7RNkv.png](https://i.imgur.com/ZM7RNkv.png)
- Use the following command to generate a SAS token for your device: 
    - Please note this token will expire in 1 month or 2628000s after creating it.
```bash
az iot hub generate-sas-token -d {device_id} -n {iothub_name} --du 2628000
```
- Replace the SAS token on any of the Python scripts provided. 

### Connecting with X.509
