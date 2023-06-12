import requests
import json
import re
import sys
from datetime import date
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# get date for name
today=date.today()

# Config
api_key = '---REPLACE--'
cert_path = '---REPLACE--/fullchain.pem'
key_path = '---REPLACE--/privkey.pem'
cert_pass = '---REPLACE--'
cert_name = f"---REPLACE--_{today}"
vserver_name = '---REPLACE--'
url = f"https://---REPLACE--/api/v2/monitor/vpn-certificate/local/import?scope=global&access_token={api_key}"

# Read and convert certificates and keyfile
cert=""
with open(cert_path, "r") as file:
    for line in file:
        if '----' not in line:
            cert+=line           
cert=re.sub(r"(\s*\n)+", "\x20", cert)
cert=re.sub(r" ", "", cert)

key=""
with open(key_path, "r") as file:
    for line in file:
        if '----' not in line:
            key+=line           
key=re.sub(r"(\s*\n)+", "\x20", key)
key=re.sub(r" ", "", key)

# create query
headers = {
    "Content-Type": "application/json"
}

data = {
    "type": "regular",
    "certname": cert_name,
    "password": cert_pass,
    "scope": "global",
    "file_content": cert,
    "key_file_content": key,
 
}

# Uploadf Certs
json_data = json.dumps(data)
response = requests.post(url, headers=headers, data=json_data, verify=False)
if response.status_code == 200:
    print("Certificate uploaded successfully!")
else:
    print("Failed to upload Certificate (Cert with same name already exists?). Error:", response.status_code)
    sys.exit()


# Assign new certs to vserver
url = f"https://10.11.1.1/api/v2/cmdb/firewall/vip/{vserver_name}/?scope=global&access_token={api_key}"  # Replace with your actual URL
data2 = {
    #"name": vserver_name,
    "ssl-certificate": cert_name
}
json_data2 = json.dumps(data2)
response = requests.put(url, headers=headers, data=json_data2, verify=False)
if response.status_code == 200:
    print("New Certificate successfully set on VIP!")
else:
    print(f"Failed to set Certificate on VIP. Error:", response.status_code)
