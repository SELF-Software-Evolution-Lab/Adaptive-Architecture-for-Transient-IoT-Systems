import requests
import re
import json
import datetime
import redis
import ast
import time
from gateway import ontology_instance_manager
from gateway import instance_matching
from SPARQLWrapper import SPARQLWrapper, JSON


def get_triples():
    sparql.setQuery("""
        SELECT (COUNT(*) as ?Triples) 
        WHERE { ?s ?p ?o }
    """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    for result in results["results"]["bindings"]:
        triplets_number = result["Triples"]["value"]
    return triplets_number


def find_gateway(base_url, header, gateways):
    search = "?fu=1&rty=3&drt=1"
    for gateway, url in gateways.items():
        tree = {}
        try:
            start_all_process = time.perf_counter()  # time
            rec_gateway = requests.get(base_url + url + search, headers=header)
            rec_gateway_dic = json.loads(rec_gateway.content)
            find_apps(base_url, header, rec_gateway_dic, start_all_process)
            tree["Relative URL"] = url
            tree["Base URL"] = base_url
            tree["Name"] = gateway
            tree["Date"] = datetime.datetime.now()
            ontology_instance_manager.om2m_instance_load(tree)
        except:
            print("Cannot connect with the following gateway", url)
            continue


def find_server(base_url, header, servers):
    search = "?fu=1&rty=3&drt=1"
    for server, url in servers.items():
        tree = {}
        try:
            start_all_process = time.perf_counter()  # time
            rec_server = requests.get(base_url + url + search, headers=header)
            rec_server_dic = json.loads(rec_server.content)
            find_apps(base_url, header, rec_server_dic, start_all_process)
            tree["Relative URL"] = url
            tree["Name"] = server
            tree["Base URL"] = base_url
            tree["Date"] = datetime.datetime.now()
            ontology_instance_manager.om2m_instance_load(tree)
        except Exception as e:
            print("Cannot connect with the following server", url)
            print("error", str(e))
            continue


def find_device(base_url, header, urls, server_flag):
    start_initial_execution = time.perf_counter()  # time
    if urls['m2m:uril']:
        servers = {}
        gateways = {}
        ng = 0
        ns = 0
        reg_urls = redis_server.smembers("registered_urls")
        for resource in urls['m2m:uril']:
            if resource in reg_urls:
                continue
            result = requests.get(base_url + resource, headers=header)
            result_dic = json.loads(result.content)
            if ("m2m:cin" in result_dic) and (resource not in reg_urls):
                redis_server.sadd("registered_urls", resource)
            if "m2m:cb" in result_dic and server_flag is True:
                ns += 1
                servers["Server_" + str(ns)] = result_dic["m2m:cb"]["ri"] + "/" + result_dic["m2m:cb"]["rn"]
            if "m2m:cb" in result_dic and server_flag is False:
                ng += 1
                gateways["Gateway_"+str(ng)] = result_dic["m2m:cb"]["ri"] + "/" + result_dic["m2m:cb"]["rn"]
        stop_initial_execution = time.perf_counter()  # time
        initial_execution = stop_initial_execution - start_initial_execution
        file_output2 = open('resource discovery.txt', 'a')
        file_output2.write("Initial execution;" + str(initial_execution) + "\n")  # time
        file_output2.close()
        print("start_finding apps")
        if server_flag is True:
            find_server(base_url, header, servers)
        else:
            find_gateway(base_url, header, gateways)
        print("stop finding apps")


def find_apps(base_url, header, urls, start_all_process):
    if urls['m2m:uril']:
        registered_urls = redis_server.smembers("registered_urls")
        for resource in urls['m2m:uril']:
            start_parsing = time.perf_counter()  # time
            try:
                if resource in registered_urls:
                    continue
                print("res", resource)
                result = requests.get(base_url + resource, headers=header)
                result_dic = json.loads(result.content)
                if "m2m:cin" in result_dic:
                    redis_server.sadd("registered_urls", resource)
                if "m2m:sub" in result_dic:
                    redis_server.sadd("registered_urls", resource)
                if "m2m:ae" in result_dic:
                    app = dict()
                    app["Base URL"] = base_url
                    app["Relative URL"] = resource
                    app["lbl"] = result_dic["m2m:ae"]["lbl"]
                    for data in app["lbl"]:
                        var = re.findall("(^Cat.*|^cat.*)/(.*)", data)
                        if var:
                            app["Category"] = var[0][1]
                        un = re.findall("^(Un.*|^un.*)/(.*)", data)
                        if un:
                            app["Unit"] = un[0][1]
                        loc = re.findall("(^Lo.*|^lo.*)/(.*)", data)
                        if loc:
                            app["Location"] = loc[0][1]
                        mod = re.findall("(^Mo.*|^mo.*)/(.*)", data)
                        if mod:
                            app["Model"] = mod[0][1]
                    rec_app = requests.get(base_url + resource + "?fu=1&rty=3&drt=1", headers=header)
                    rec_app_dic = json.loads(rec_app.content)
                    if rec_app_dic['m2m:uril']:
                        rec_app_dic['m2m:uril'] = [x for x in rec_app_dic['m2m:uril'] if
                                                   x.startswith(resource + "/")]
                        urls_cont = []
                        for cont in rec_app_dic['m2m:uril']:
                            if cont in registered_urls:
                                continue
                            container = requests.get(base_url + cont, headers=header)
                            container_dic = json.loads(container.content)
                            if "m2m:cin" in container_dic:
                                urls_cont.append(cont)
                                continue
                            if "m2m:cnt" in container_dic:
                                urls_cont.append(cont)
                                app[container_dic["m2m:cnt"]["rn"]] = container_dic["m2m:cnt"]
                    app["Parent"] = re.findall("/(.*?)/", resource)[0]
                    app["App Name"] = re.findall("/.*/(.*)", resource)[0]
                    qos = requests.get(base_url + resource + "/QoS/la", headers=header)
                    qos_dic = json.loads(qos.content)
                    qos_text = qos_dic["m2m:cin"]["con"].replace("false", "False").replace("true", "True")\
                        .replace("none", "None")
                    app["QoS"] = ast.literal_eval(qos_text)
                    system_properties = requests.get(base_url + resource + "/System_Properties/la", headers=header)
                    system_properties_dic = json.loads(system_properties.content)
                    system_properties_text = system_properties_dic["m2m:cin"]["con"].replace("false", "False")\
                        .replace("true", "True").replace("none", "None")
                    app["System property"] = ast.literal_eval(system_properties_text)
                    if app["DATA"] and app["Healthcheck"]:
                        stop_parsing = time.perf_counter()  # time
                        ontology_instance_manager.app_instance_load(app)
                        stop_instantiation = time.perf_counter()   # time
                        redis_server.sadd("registered_urls", resource)
                        for cont in urls_cont:
                            redis_server.sadd("registered_urls", cont)
                        guidepost = redis_server.smembers("execution_guidepost_services")
                        len_guidepost = len(guidepost)
                        inclusion_time = list()
                        for service in guidepost:
                            start_inclusion = time.perf_counter()
                            try:
                                service_requirement = ast.literal_eval(redis_server.get(service + "_requirement"))
                                functional_requirement = service_requirement["functional"]
                                if app["Category"] == functional_requirement["Category"]:
                                    system_properties_requirement = service_requirement["system"]
                                    qos_requirement = service_requirement["qos"]
                                    device = app["Base URL"] + app["Relative URL"]
                                    instance_matching.instance_matching(functional_requirement, system_properties_requirement, qos_requirement,
                                                      device, None)
                                    stop_inclusion = time.perf_counter()
                                    inclusion_time.append(stop_inclusion - start_inclusion)
                                else:
                                    stop_inclusion = time.perf_counter()
                                    inclusion_time.append(stop_inclusion - start_inclusion)
                                    continue
                            except Exception as e:
                                stop_inclusion = time.perf_counter()
                                inclusion_time.append(stop_inclusion - start_inclusion)
                        stop_all_process = time.perf_counter()  # time
                        parsing = stop_parsing - start_parsing  # time
                        ontology_instantiation = stop_instantiation - stop_parsing  # time
                        discovery_parsing = stop_all_process - start_all_process  # time
                        triplets_number = get_triples()
                        file_output1 = open('resource discovery.txt', 'a')  # time
                        file_output1.write(str(discovery_parsing) + ";" + str(parsing) + ";"
                                           + str(ontology_instantiation) + ";" + str(triplets_number) + "\n")  # time
                        file_output1.close()  # time
                        print(inclusion_time)
                        if inclusion_time:
                            print("printing inclusion time")
                            file_output1 = open('Device inclusion.txt', 'a')  # time
                            inclusion_text = ""
                            for text in inclusion_time:
                                inclusion_text = inclusion_text + str(text) + ";"
                            file_output1.write(str(triplets_number) + ";" + str(len_guidepost) + ";"
                                               + str(discovery_parsing) + ";" + str(parsing) + ";"
                                               + str(ontology_instantiation) + ";" + str(sum(inclusion_time)) + ";"
                                               + inclusion_text + "\n")  # time
                            file_output1.close()


            except Exception as e:
                print("error", str(e))
                if resource in registered_urls:
                    continue
                else:
                    print("not valid app")
                    continue


# sparql = SPARQLWrapper("http://localhost:3030/mod_ssn/")
sparql = SPARQLWrapper("http://172.24.100.100:8000/mod_ssn")
# pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
pool = redis.ConnectionPool(host='172.24.100.98', port=8080, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)
file_output = open('resource discovery.txt', 'a')
file_output.write("Discovery and Parsing time;Parsing time;Ontology instantiation time;Triples numbers\n")
file_output.write("0;0;" + str(get_triples()) + "\n")  # time
file_output.close()

file_output = open('Device inclusion.txt', 'a')
file_output.write("Triples numbers;Guidepost_size;Discovery and Parsing time;Parsing time;Ontology instantiation time;"
                  "Total inclusion time;Inclusion time\n")
file_output.write("0;0;0;" + str(get_triples()) + ";0\n")  # time
file_output.close()
