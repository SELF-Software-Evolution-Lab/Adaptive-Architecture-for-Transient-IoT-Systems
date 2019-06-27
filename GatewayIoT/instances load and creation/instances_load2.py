import time
import random
import json
from pprint import pprint
import paho.mqtt.client as mqtt


def on_message(client, userdata, msg):
    print("Respuesta del topico: "+str(msg.payload.decode("UTF-8")))
    # Funcion recursiva que muestra la respuesta dada por el servidor de MQTT de OM2M despues de que se envia cada
    # payload


while True:
    for i in range(101, 115):
        new_app = dict()
        new_app["App Name"] = "Sensor_sa" + str(i)

        # enter username and password
        authenticate = """ "admin:admin" """
        topic = "/oneM2M/req/" + new_app["App Name"] + "/in-cse/json"
        payload_lista = []
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

        payload_lista.append(payload7)
        payload_lista.append(payload7)

        client = mqtt.Client("OM2M_MQTT")
        client.on_message = on_message
        client.connect("172.24.100.94", 1883)
        # client.connect("172.24.100.95", 1883)
        client.loop_start()
        for payload in payload_lista:
            client.subscribe("/oneM2M/resp/in-cse/" + new_app["App Name"] + "/json")
            print("prueba del MQTT: "+payload)
            print()
            client.publish(topic, payload)
            time.sleep(0.05)
            client.on_message = on_message
        client.loop_stop()
