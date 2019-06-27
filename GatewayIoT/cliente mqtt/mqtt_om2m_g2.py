#/usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf
import paho.mqtt.client as mqtt
import time


def on_message(client, userdata, msg):
    print("Respuesta del topico: "+str(msg.payload.decode("UTF-8")))

topic="/oneM2M/req/CO2_garage/mn-cse/json"
payload_lista=[]
payload1="""{"m2m:rqp": {"m2m:fr": "CO2_garage","m2m:to": "/mn-cse","m2m:op": 2,"m2m:rqi": 123456}}"""

payload2="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/mn-cse/mn-name",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {
"m2m:ae": {
     "api": "app-sensor",
     "rr": "false",
     "lbl": ["Type/sensor", "Category/CO2", "Location/garage","Unit/ppm"],
     "rn": "CO2_garage"}},
"m2m:ty": 2}}"""

# payload3="""{"m2m:rqp": {
# "m2m:fr" : "admin:admin",
# "m2m:to" : "/mn-cse/mn-name/CO2_garage",
# "m2m:op" : 1,
# "m2m:rqi": 123456,
# "m2m:pc": {"m2m:cnt": {"rn": "DESCRIPTOR"}},
# "m2m:ty": 3}}"""

payload4="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/mn-cse/mn-name/CO2_garage",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "Healthcheck"}},
"m2m:ty": 3}}"""

payload5="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/mn-cse/mn-name/CO2_garage",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "DATA"}},
"m2m:ty": 3}}"""

payload6="""{"m2m:rqp": {
"m2m:fr" : "admin:admin",
"m2m:to" : "/mn-cse/mn-name/CO2_garage/DATA",
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
"m2m:to" : "/mn-cse/mn-name/CO2_garage/Healthcheck",
"m2m:op" : 1,
"m2m:rqi": 123454,
"m2m:pc": {
   "m2m:cin": {"cnf":"message",
   "con":"1s"
   }
},
"m2m:ty": 4}}"""

payload_lista.append(payload1)
payload_lista.append(payload2)
# payload_lista.append(payload3)
payload_lista.append(payload4)
payload_lista.append(payload5)
# payload_lista.append(payload6)
# payload_lista.append(payload7)


for payload in payload_lista:
    client = mqtt.Client("OM2M_MQTT")
    client.on_message = on_message
    client.connect("192.168.0.8", 1883)
    client.loop_start()
    client.subscribe("/oneM2M/resp/mn-cse/CO2_garage/json")
    print("prueba del MQTT: "+payload)
    print()
    client.publish(topic, payload)
    time.sleep(1)
    client.on_message = on_message
    client.loop_stop()

