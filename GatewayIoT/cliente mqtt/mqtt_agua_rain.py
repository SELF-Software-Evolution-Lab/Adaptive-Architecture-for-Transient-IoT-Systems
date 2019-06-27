# /usr/local/sbin/mosquitto -c /usr/local/etc/mosquitto/mosquitto.conf

import paho.mqtt.client as mqtt
import time
import random
import json

def on_message(client, userdata, msg):
    print("Respuesta del topico: "+str(msg.payload.decode("UTF-8")))
    # Funcion recursiva que muestra la respuesta dada por el servidor de MQTT de OM2M despues de que se envia cada
    # payload


unit = ["in"]
unit_coin = ["USD", "COL"]
binary = [True, False]
quantitative = ["high", "medium", "low", "very_low", "very_high"]
m_unit = random.choice(unit)

QoS = {"Availability": {"value": round(random.random(), 2), "unit": "%"}, "Capacity": "TBD",
       'Cost': {"value": random.randint(0, 1000), "unit": random.choice(unit_coin)},
       "Interoperability": random.choice(binary),
       "Throughput": {"value": random.randint(0, 1000), "unit": "ms"},
       "Consistency": "TBD", "Messaging": "TBD",
       "MTBF": {"value": random.randint(0, 8760), "unit": "hr"}, "Disaster": random.choice(binary),
       "Failover": random.choice(binary), "Reputation": random.choice(binary),
       "Robustness": random.choice(quantitative),
       "Scalability": random.choice(quantitative), "Auditability": random.choice(binary),
       'Authentication': random.choice(binary),
       'Data_encryption': random.choice(binary), 'Message_encryption': random.choice(binary),
       "Non_repudiation": random.choice(binary), 'Method_stability': random.choice(quantitative),
       "Interface_stability": random.choice(quantitative)}
qos_string = json.dumps(QoS)
qos_string = qos_string.replace("""\"""", "'")


system_prop = {"Accuracy": {"value": 3, "unit": "%"},
               "ActuationRange": "None",
               "DetectionLimit": {"value": 0.01, "unit": "in"},
               "Drift": "None",
               "Frequency": {"value": 6, "unit": "s"},
               "Latency": {"value": 135, "unit": "ms"},
               "MeasurementRange": "None",
               "Precision": {"value": 0.01, "unit": "in"},
               "Resolution": {"value": 0.01, "unit": "in"},
               "ResponseTime": {"value": 135, "unit": "ms"},
               "Selectivity": "None", "Sensitivity": "None"}

system_prop_string = json.dumps(system_prop)
system_prop_string = system_prop_string.replace("""\"""", "'")


# enter username and password
authenticate = """ "admin:admin" """

topic = "/oneM2M/req/park_rain1/in-cse/json"
payload_lista = []
payload1 = """{"m2m:rqp": {"m2m:fr": "park_rain1","m2m:to": "/in-cse","m2m:op": 2,"m2m:rqi": 123456}}"""
# Payload de prueba

payload2 = """{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {
"m2m:ae": {
     "api": "app-sensor",
     "rr": "false",
     "lbl": ["Type/sensor", "Category/rain", "Location/park", "Model/RG-200", "Unit/in"],
     "rn": "park_rain1"}},
"m2m:ty": 2}}"""
# payload para crear la aplicacion con el nombre park_rain1

payload3="""{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "QoS"}},
"m2m:ty": 3}}"""
# payload para crear el contenedor QoS en la aplicacion.

payload4="""{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "Healthcheck"}},
"m2m:ty": 3}}"""
# payload para crear el contenedor Healthcheck en la aplicacion.

payload5="""{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "DATA"}},
"m2m:ty": 3}}"""
# payload para crear el contenedor DATA en la aplicacion.

payload6="""{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1/DATA",
"m2m:op" : 1,
"m2m:rqi": 123454,
"m2m:pc": {
   "m2m:cin": {"cnf":"message",
   "con":"55 C"
   }
},
"m2m:ty": 4}}"""
# este payload crea un dato en el contenedor DATA


payload7 = """{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1/Healthcheck",
"m2m:op" : 1,
"m2m:rqi": 123454,
"m2m:pc": {
   "m2m:cin": {"cnf":"message",
   "con":"10s"
   }
},
"m2m:ty": 4}}"""
# este payload crea un dato en el contenedor Healthcheck

payload8 = """{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1",
"m2m:op" : 1,
"m2m:rqi": 123456,
"m2m:pc": {"m2m:cnt": {"rn": "System_Properties"}},
"m2m:ty": 3}}"""
# payload para crear el contenedor System_Properties en la aplicacion.

payload9 = """{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1/System_Properties",
"m2m:op" : 1,
"m2m:rqi": 123454,
"m2m:pc": {
   "m2m:cin": {"cnf":"message",
   "con":\""""+system_prop_string+"""\"
   }
},
"m2m:ty": 4}}"""
# este payload crea un dato en el contenedor System_Properties

payload10 = """{"m2m:rqp": {
"m2m:fr" : """+authenticate+""",
"m2m:to" : "/in-cse/in-name/park_rain1/QoS",
"m2m:op" : 1,
"m2m:rqi": 123454,
"m2m:pc": {
   "m2m:cin": {"cnf":"message",
   "con":\""""+qos_string+"""\"
   }
},
"m2m:ty": 4}}"""
# este payload crea un dato en el contenedor System_Properties

# payload_lista.append(payload1)
# payload_lista.append(payload2)
# payload_lista.append(payload3)
# payload_lista.append(payload4)
# payload_lista.append(payload5)
# payload_lista.append(payload6)
payload_lista.append(payload7)
# payload_lista.append(payload8)
# payload_lista.append(payload9)
# payload_lista.append(payload10)
# Despues de creada la aplicacion, si solo desean enviar datos, agregar comentarios al append de payload 1 al 5.

while True:
    for payload in payload_lista:
        client = mqtt.Client("OM2M_MQTT")
        client.on_message = on_message
        client.connect("127.0.0.1", 1883)

        client.loop_start()
        client.subscribe("/oneM2M/resp/in-cse/park_rain1/json")
        print("prueba del MQTT: "+payload)
        print()
        client.publish(topic, payload)
        time.sleep(2)
        client.on_message = on_message
        client.loop_stop()
