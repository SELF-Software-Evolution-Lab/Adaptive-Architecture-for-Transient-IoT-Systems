import paho.mqtt.client as mqtt
import time


def on_message(client, userdata, msg):
    print("Respuesta del topico: "+str(msg.payload.decode("UTF-8")))

topic="/oneM2M/req/Temp_cocina/in-cse/json"
payload_lista=[]
payload1="""{"m2m:rqp": {"m2m:fr": "Temp_cocina","m2m:to": "/in-cse","m2m:op": 2,"m2m:rqi": 123456}}"""

payload2="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/in-cse/in-name",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {
"m2m:ae": {
     "api": "app-sensor",
     "rr": "false",
     "lbl": ["Type/sensor", "Category/temperature", "Location/home","Unit/F"],
     "rn": "Temp_cocina"}},
"m2m:ty": 2}}"""

payload3="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/in-cse/in-name/Temp_cocina",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "DESCRIPTOR"}},
"m2m:ty": 3}}"""

payload4="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/in-cse/in-name/Temp_cocina",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "Healthcheck"}},
"m2m:ty": 3}}"""

payload5="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/in-cse/in-name/Temp_cocina",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "DATA"}},
"m2m:ty": 3}}"""

payload6="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/in-cse/in-name/Temp_cocina/DATA",
"m2m:op" : 1,
"m2m:rqi": 123454,
"m2m:pc": {
   "m2m:cin": {"cnf":"message",
   "con":"666 C"
   }
},
"m2m:ty": 4}}"""

payload7="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/in-cse/in-name/Temp_cocina/Healthcheck",
"m2m:op" : 1,
"m2m:rqi": 123454,
"m2m:pc": {
   "m2m:cin": {"cnf":"message",
   "con":"12s"
   }
},
"m2m:ty": 4}}"""

# payload_lista.append(payload1)
# payload_lista.append(payload2)
# payload_lista.append(payload3)
# payload_lista.append(payload4)
# payload_lista.append(payload5)
# payload_lista.append(payload6)
payload_lista.append(payload7)

cont = 0
while True:
    cont += 1
    print("Contador ", cont)
    for payload in payload_lista:
        client = mqtt.Client("OM2M_MQTT")
        client.on_message = on_message
        client.connect("18.188.112.170", 1883)
        client.loop_start()
        client.subscribe("/oneM2M/resp/in-cse/Temp_cocina/json")
        print("prueba del MQTT: "+payload)
        print()
        client.publish(topic, payload)
        time.sleep(1)
        client.on_message = on_message
        client.loop_stop()
    if cont == 1:
        break
