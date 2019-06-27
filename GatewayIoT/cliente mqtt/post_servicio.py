import requests
import json
import socket
import ast

# dicc1={'nombre':'Jairo','apellido':'ariza','apellido2':'castañeda'}
# dicc2={'nombre':'Andres','apellido':'ariza','apellido2':'clavijo'}
# lista=[dicc1,dicc2]
#
# # with open('result.json', 'w') as fp:
# #     json.dump(lista, fp)
# # fp.close()
#
# a = json.loads('["foo", {"bar":["baz", null, 1.0, 2]}]')
# print(a)
# print(type(a[1]))
#
# with open('result.json') as f:
#     functional_requirement = json.load(f)
#
# print(functional_requirement)
# print(type(functional_requirement[0]))

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()
# ip_address = socket.gethostbyname(socket.gethostname())

url = "http://localhost:8000/post_service/"
data = {"Name": "weather", "Location": "home", "Category": "temp", "Unit": "Celsius",
        "URL": "http://"+ip_address+":1400/monitor"}


headers = {'content-type': 'application/json'}
r = requests.post(url, data=json.dumps(data), headers=headers)

# base_url = "http://192.168.0.7:8080/~"
# header = {"X-M2M-Origin": "admin:admin", "Accept": "application/json"}
# device = "/in-cse/in-name/Temp_casa/QoS/la"
# rec_server = requests.get(base_url+device, headers=header)
# rec_server_dic = json.loads(rec_server.content)
# QoS = rec_server_dic["m2m:cin"]["con"]

# QoS = """{'Security':{'Authentication':True,'Auditability':True,'Encryption':False},'Economy': '$1','Availability':0.9,
# 'Reliability':3,'Stability':'medium'}"""
# QoS = ast.literal_eval(QoS)
# print(QoS)
# print(type(QoS))

