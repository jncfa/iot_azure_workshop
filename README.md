# iot_azure_workshop


## How to use this repository

The Python scripts are adapted versions of the previous mqtt bridge scripts for Azure, supporting both SAS and X.509v3 certificates.

To use SAS, you need to do the following steps:
- Create a device in your IoT hub. 
- Create a cloud shell using the "terminal" button on the top bar on the Azure Portal:
![https://i.imgur.com/ZM7RNkv.png](https://i.imgur.com/ZM7RNkv.png)

- Use the following command to generate a SAS token for your device: `az iot hub generate-sas-token -d {device_id} -n {iothub_name} --du 2628000`
    - Please note this token will expire in 1 month or 2628000s after creating it.

- Replace the SAS token on any of the Python scripts provided. 