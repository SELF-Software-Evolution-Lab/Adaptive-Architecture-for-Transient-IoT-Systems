import requests
import json

# this code reads the last value of the DATA container of the Temp_casa app
# enter username
username = "admin"
# enter password
password = "admin"
header = {"X-M2M-Origin": username+":"+password, "Accept": "application/json"}
base_url = "http://172.24.100.95:8000/~"
# base_url = "http://172.24.100.94:8080/~"
# base_url = "http://127.0.0.1:8282/~"
# you should change the device variable depending which functional_requirement do you want to read.
for i in range(3000, 5001):
    try:
        device = "/mn-cse/mn-name/Sensor_gd" + str(i)
        print(i)
        # device = "/in-cse/in-name/Sensor_sd" + str(i)
        url_om2m = base_url + device
        rec_server = requests.delete(url_om2m, headers=header)
    except:
        continue
#rec_server_dic = json.loads(rec_server.content)

#print(rec_server_dic)