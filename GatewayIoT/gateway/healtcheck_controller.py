import sys
sys.path.append("/home/profesor/GatewayIoT")
import json
import onem2mlib.constants as const
import onem2mlib.notifications as notifs
import redis
import socket
import re
import ast
import time
import datetime
import requests
from onem2mlib import *
from pprint import pprint
from SPARQLWrapper import SPARQLWrapper, JSON


def get_providers():
    sparql.setQuery(""" 
                PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                SELECT ?provider  
                WHERE { ?provider rdf:type modssn:Provider. 
                }""")
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    query_result = results["results"]["bindings"]
    providers = [result["provider"]["value"].replace(modssn_prefix, "") for result in query_result]
    return providers


def callback(resource):
    if resource.type == const.Type_ContentInstance:
        # print(resource)
        for application in applications:
            if resource.parentID == application["cnt"].resourceID:
                # print(resource.parentID)
                application["Readings"].insert(0, resource)
                if len(application["Readings"]) > 3:
                    application["Readings"].pop()
                # print(application["Readings"])
                # print()
    else:
        print(resource)


def create_health_check(ip, device_name):
    for application in available_apps:
        file_output1 = open('Health check creation.txt', 'a')
        try:
            start_creation = time.perf_counter()  # time
            app1 = dict()
            if device_name in application and ip in application:
                name = re.findall(".*-name/(.*)", application)
                if name:
                    name = name[0]
                app1["URL"] = application
                app1["Parent"] = CSEBase(session, device_name)
                app1["name"] = AE(app1["Parent"], name)
                app1["cnt"] = Container(app1["name"], "Healthcheck")
                app1["cnt"].subscribe()
                app1["cnt"].maxNrOfInstances = 10
                app1["cnt"].updateInCSE()
                app1["Readings"] = [datetime.datetime.now()]
                app1["Health check estimated time"] = 2
                app1["State"] = None
                app1["Lost health checks"] = 0
                applications.append(app1)
                application_names.append(application)
                stop_creation = time.perf_counter()
                creation_time = stop_creation - start_creation
                file_output1.write(str(creation_time) + "\n")
            else:
                continue
        except Exception as error:
            print(str(error))
            continue
    file_output1.close()


sys.path.append('..')
# sparql = SPARQLWrapper("http://localhost:3030/mod_ssn/")
sparql = SPARQLWrapper("http://172.24.100.100:8000/mod_ssn")
modssn_prefix = "http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#"

# pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
pool = redis.ConnectionPool(host='172.24.100.98', port=8080, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()

file_output = open('Health check creation.txt', 'a')
file_output.write("Health check creation time\n")
file_output.close()

guidepost = redis_server.smembers("execution_guidepost_services")
len_guidepost = len(guidepost)
app_list = redis_server.smembers("app_list")
len_app = len(app_list)
file_output = open('guidepost update.txt', 'a')
file_output.write("Matching number;App list;Guidepost update\n")


header = {"X-M2M-Origin": "admin:admin", "Accept": "application/json", 'content-type': 'application/json;ty=23'}
applications = []
application_names = []
notifs.setupNotifications(callback, host="127.0.0.1", port=1400)
# session = Session("http://"+ip_address+":8080", 'admin:admin')
# ip_device = "127.0.0.1:8080"
ip_device = "172.24.100.94:8080"
session = Session("http://"+ip_device, 'admin:admin')
cont = 0

server_flag = True
# server_flag = False
if server_flag is True:
    device = "in-cse"
else:
    device = "mn-cse"

count = 0
while True:
    try:
        count = count+1
        if count == 1: available_apps = get_providers()
        if count == 10: count = 0
        print("Applications")
        if not applications:
            available_apps = available_apps
            # pprint(available_apps)
            create_health_check(ip_device, device)
        elif set(available_apps)-set(application_names):
            available_apps = set(available_apps) - set(application_names)
            # pprint(available_apps)
            create_health_check(ip_device, device)
        for app in applications:
            try:
                start_update = time.perf_counter()  # time
                print(app["URL"])
                last_state = app["State"]
                if app["Readings"]:
                    try:
                        time1 = datetime.datetime.strptime((app["Readings"][0].creationTime.replace("T", "")), '%Y%m%d%H%M%S')
                    except Exception as e:
                        time1 = app["Readings"][0]
                        print(str(e))
                    lost = (datetime.datetime.now() - time1) \
                        / datetime.timedelta(seconds=app["Health check estimated time"])
                    app["Lost health checks"] = int(lost) if lost > 1.2 else 0
                    print("Lost health checks ", app["Lost health checks"])
                    app["State"] = False if app["Lost health checks"] >= 3 else True
                    # print("listado", redis_server.smembers(app["URL"]), app["URL"])
                    if last_state != app["State"] and redis_server.smembers(app["URL"]):
                        print("last states", last_state, app["State"])
                        # print("listado", redis_server.smembers(app["URL"]))
                        for service in redis_server.smembers(app["URL"]):
                            # print("set")
                            # pprint(service)
                            service_guidepost = ast.literal_eval(redis_server.get(service))
                            # print("antes")
                            # pprint(service_guidepost)
                            for index, dic in enumerate(service_guidepost):
                                if app["URL"] == dic["app"]:
                                    service_guidepost[index]["state"] = app["State"]
                                    if last_state is True and app["State"] is False and "subscription" in dic:
                                        try:
                                            # print("borrando subs1", dic["subscription"])
                                            requests.delete(dic["subscription"], headers=header)
                                            del service_guidepost[index]["subscription"]
                                        except:
                                            # print("borrando subs2", dic["subscription"])
                                            del service_guidepost[index]["subscription"]
                                    break

                            subscription_flag = False
                            for index, dic in enumerate(service_guidepost):
                                if service_guidepost[index]["state"] is True and "subscription" in dic \
                                        and subscription_flag is False:
                                    subscription_flag = True
                                elif service_guidepost[index]["state"] is True and "subscription" not in dic \
                                        and subscription_flag is False:
                                    print("subs", index, dic, service)
                                    data = {
                                        "m2m:sub": {
                                            "xmlns:m2m": "http://www.onem2m.org/xml/protocols",
                                            "nu": service,
                                            "nct": "2"
                                        }
                                    }
                                    url = service_guidepost[index]["app"]+"/DATA"
                                    try:
                                        subscription = requests.post(url, data=json.dumps(data), headers=header)
                                        subs_url = url + "/" + json.loads(subscription.content)["m2m:sub"]["rn"]
                                        service_guidepost[index]["subscription"] = subs_url
                                        subscription_flag = True
                                    except Exception as e:
                                        print("try sub", str(e))
                                        service_guidepost[index]["subscription"] = "suscrito"
                                        subscription_flag = True
                                elif service_guidepost[index]["state"] is True and "subscription" in dic \
                                        and subscription_flag is True:
                                    try:
                                        requests.delete(dic["subscription"], headers=header)
                                        del service_guidepost[index]["subscription"]
                                        print("borrando subs3", dic["subscription"])
                                    except:
                                        print("borrando subs4", dic["subscription"])
                                        del service_guidepost[index]["subscription"]
                            redis_server.set(service, str(service_guidepost))
                            # print("despues")
                            pprint(ast.literal_eval(redis_server.get(service)))
                        stop_update = time.perf_counter()  # time
                        guide_update = stop_update - start_update
                        print("escribiendo")
                        file_output.write(str(len_guidepost) + ";" + str(len_app) + ";" + str(guide_update) + "\n")
                print("App state", app["State"])
                print()
            except Exception as e:
                print("error health", str(e))
                print(app["URL"])
                # app["State"] = False
                # print("App state", app["State"])
                continue
        time.sleep(5)
        cont += 1
        print("Counter ", cont)
        if cont == 60:
            break
    except Exception as e:
        print(str(e))


notifs.shutdownNotifications()
file_output.close()
