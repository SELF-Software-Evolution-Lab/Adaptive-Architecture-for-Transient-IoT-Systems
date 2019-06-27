import time
import random
import json
from pprint import pprint
import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):
    print("Respuesta del topico: "+str(msg.payload.decode("UTF-8")))
    # Funcion recursiva que muestra la respuesta dada por el servidor de MQTT de OM2M despues de que se envia cada
    # payload


sensor_list = list()
location_list = ["room", "kitchen", "garage", "Backyard", "Bogota", "Colombia", "USA", "ML", "University", "Balcony",
                 "attic", "playroom", "bedroom", "bathroom", "laboratory", "bosa", "suba", "kennedy", "candelaria",
                 "centro", "niza", "galerias", "castellana", "soledad", "puente aranda"]
category_list = ["Level", "temperature", "pressure", "CO2", "flow", "fire", "power", "sound", "moisture",
                 "vibration", "distance", "rain"]

units = {"Level": ["m", "cm", "mm", "in", "ft"], "temperature": ["C", "K", "F"],
         "pressure": ["psig", "pascal", "bar", "at", "atm", "Torr"], "CO2": ["ppm", "%c"], "flow": ["m3/s", "ft3/s"],
         "fire": ["kW/m2", "W/m2", "W/in2"], "power": ["W", "kW", "hp"], "sound": ["dB", "sone"],
         "moisture": ["%h"], "vibration": ["ips", "mm/s"], "distance": ["m", "cm", "mm", "in", "ft"],
         "rain": ["mm", "in"]}

for i in range(1, 126):
    model = "Model_sd" + str(i)
    category = random.choice(category_list)
    location = random.choice(location_list)
    unit = random.choice(units[category])
    system_prop = {'Accuracy': {'value': round(random.random(), 2), 'unit': '%'},
                   'ActuationRange': 'none',
                   'DetectionLimit': {'value': random.randint(0, 10), 'unit': unit},
                   'Drift': 'none',
                   'Frequency': {'value': random.randint(0, 100), 'unit': 's'},
                   'Latency': {'value': random.randint(0, 100), 'unit': 'ms'},
                   'MeasurementRange': {'value': '0-' + str(random.randint(0, 100)), 'unit': unit},
                   'Precision': {'value': round(random.random(), 2), 'unit': unit},
                   'Resolution': {'value': round(random.random(), 2), 'unit': unit},
                   'ResponseTime': {'value': random.randint(0, 100), 'unit': 'ms'},
                   'Selectivity': 'none', 'Sensitivity': 'none'}

    system_prop_string = json.dumps(system_prop)
    system_prop_string = system_prop_string.replace("""\"""", "'")
    functional_prop = {'lbl': '"Type/sensor", "Cat/' + category + '", "Loc/' + location + '", "Model/' + model
                              + '", "Unit/' + unit + '"', "sys_prop": system_prop_string}
    sensor_list.append(functional_prop)

pprint(sensor_list)

for i in range(1, 2501):
    unit_coin = ["USD", "COL", "CAD", "CHF", "JPY", "EUR"]
    binary = [True, False]
    quantitative = ["high", "medium", "low", "very_low", "very_high"]
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
    new_app = random.choice(sensor_list)
    new_app["App Name"] = "Sensor_sd" + str(i)

    # enter username and password
    authenticate = """ "admin:admin" """
    topic = "/oneM2M/req/" + new_app["App Name"] + "/in-cse/json"
    payload_lista = []
    payload1 = """{"m2m:rqp": {"m2m:fr": '""" + new_app["App Name"] + """', 
    "m2m:to": "/in-cse","m2m:op": 2,"m2m:rqi": 123456}}"""
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
         "lbl": [""" + new_app["lbl"] + """],
         "rn": " """ + new_app["App Name"] + """"}},
    "m2m:ty": 2}}"""
    # payload para crear la aplicacion con el nombre Drenaje2

    payload3="""{"m2m:rqp": {
    "m2m:fr" : """+authenticate+""",
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """",
    "m2m:op" : 1,
    "m2m:rqi": 123456,
    "m2m:pc": {"m2m:cnt": {"rn": "QoS"}},
    "m2m:ty": 3}}"""
    # payload para crear el contenedor QoS en la aplicacion.

    payload4 = """{"m2m:rqp": {
    "m2m:fr" : """+authenticate+""",
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """",
    "m2m:op" : 1,
    "m2m:rqi": 123456,
    "m2m:pc": {"m2m:cnt": {"rn": "Healthcheck"}},
    "m2m:ty": 3}}"""
    # payload para crear el contenedor Healthcheck en la aplicacion.

    payload5 = """{"m2m:rqp": {
    "m2m:fr" : """+authenticate+""",
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """",
    "m2m:op" : 1,
    "m2m:rqi": 123456,
    "m2m:pc": {"m2m:cnt": {"rn": "DATA"}},
    "m2m:ty": 3}}"""
    # payload para crear el contenedor DATA en la aplicacion.

    payload6 = """{"m2m:rqp": {
    "m2m:fr" : """+authenticate+""",
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """/DATA",
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
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """/Healthcheck",
    "m2m:op" : 1,
    "m2m:rqi": 123454,
    "m2m:pc": {
       "m2m:cin": {"cnf":"message",
       "con":"2s"
       }
    },
    "m2m:ty": 4}}"""
    # este payload crea un dato en el contenedor Healthcheck

    payload8 = """{"m2m:rqp": {
    "m2m:fr" : """+authenticate+""",
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """",
    "m2m:op" : 1,
    "m2m:rqi": 123456,
    "m2m:pc": {"m2m:cnt": {"rn": "System_Properties"}},
    "m2m:ty": 3}}"""
    # payload para crear el contenedor System_Properties en la aplicacion.

    payload9 = """{"m2m:rqp": {
    "m2m:fr" : """+authenticate+""",
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """/System_Properties",
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
    "m2m:to" : "/in-cse/in-name/""" + new_app["App Name"] + """/QoS",
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
    payload_lista.append(payload2)
    payload_lista.append(payload3)
    payload_lista.append(payload4)
    payload_lista.append(payload5)
    # payload_lista.append(payload6)
    # payload_lista.append(payload7)
    payload_lista.append(payload8)
    payload_lista.append(payload9)
    payload_lista.append(payload10)
    client = mqtt.Client("OM2M_MQTT")
    client.on_message = on_message
    client.connect("172.24.100.94", 1883)
    client.loop_start()
    for payload in payload_lista:
        client.subscribe("/oneM2M/resp/in-cse/" + new_app["App Name"] + "/json")
        print("prueba del MQTT: "+payload)
        print()
        client.publish(topic, payload)
        time.sleep(0.05)
        client.on_message = on_message
    client.loop_stop()
