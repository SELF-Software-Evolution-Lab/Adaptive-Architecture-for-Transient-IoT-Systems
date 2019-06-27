from gateway import functional_matching
from gateway import Non_functional_matching
import pprint
import redis
import ast
import time


# pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
pool = redis.ConnectionPool(host='172.24.100.98', port=8080, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)
pp = pprint.PrettyPrinter(depth=6)
file_output = open('instance matching.txt', 'a')
file_output.write("Parsing time;Functional matching time;Corpus time;Semantic matching time;Syntactic matching time;"
                  "Ordering time;QoS matching time;SP matching time;""Total matching time\n")
file_output.close()


def instance_matching(functional_requirement, system_properties_requirement, qos_requirement, new_app, services):
    start_matching = time.perf_counter()  # time
    if new_app is None:
        # print("Functional requirement")
        # pp.pprint(functional_requirement)
        print()
        # if there is no threshold a default of 0.7 i set
        if "threshold" in functional_requirement.keys() and \
                (type(functional_requirement["threshold"]) is float or type(functional_requirement["threshold"]) is int) \
                and 0.4 < functional_requirement["threshold"] <= 1:
            functional_requirement["threshold"] = functional_requirement["threshold"]
        else:
            functional_requirement["threshold"] = 0.7
        # if there is no application type, monitoring is setting as default
        if "application" in functional_requirement.keys() and \
                functional_requirement["application"] in ["monitoring", "non critical alarms", "control",
                                                          "critical alarms"]:
            functional_requirement["application"] = functional_requirement["application"]
        else:
            functional_requirement["application"] = "monitoring"

        # print("System property requirement")
        # pp.pprint(system_properties_requirement)
        print()

        # print("QoS requirement")
        # pp.pprint(qos_requirement)
        print()
        redis_server.set(functional_requirement["URL"] + "_requirement",
                         str({"functional": functional_requirement, "system": system_properties_requirement,
                              "qos": qos_requirement}))
    stop_parsing_requirements = time.perf_counter()  # time
    parsing_requirements_time = stop_parsing_requirements - start_matching  # time
    # calculating functional matching
    services, corpus_time, semantic_time, syntactic_time, ordering_time = functional_matching.instance_matching(functional_requirement, "cosine", new_app, services)
    stop_functional = time.perf_counter()  # time
    functional_time = stop_functional - stop_parsing_requirements
    print()
    print("functional result")
    pp.pprint(services)
    if services:
        # calculating QoS matching
        start_qos = time.perf_counter()  # time
        qos_match_services = Non_functional_matching.properties_matching(qos_requirement, "qos", services,
                                                                         functional_requirement["threshold"],
                                                                         functional_requirement["application"])
        stop_qos = time.perf_counter()  # time
        qos_matching_time = stop_qos - start_qos
        print("qos match")
        pp.pprint(qos_match_services)
        # calculating system properties matching
        start_sp = time.perf_counter()  # time
        system_match_services = Non_functional_matching.properties_matching(system_properties_requirement,
                                                                            "System", qos_match_services,
                                                                            functional_requirement["threshold"],
                                                                            functional_requirement["application"])
        stop_sp = time.perf_counter()  # time
        sp_matching_time = stop_sp - start_sp  # time
        # reading the last guidepost registry for the match of the url
        try:
            previous_match = ast.literal_eval(redis_server.get(functional_requirement["URL"]))
            print(previous_match)
        except Exception as e:
            print(str(e))
            previous_match = None
        if new_app is not None:
            for app in previous_match:
                if app["app"] == system_match_services[0]["app"]:
                    continue
                else:
                    system_match_services.append(app)
        print("system match")
        pp.pprint(system_match_services)
        # sorting the total results by score from highest to lowest
        system_match_services.sort(key=lambda x: x["score"], reverse=True)
        print("ordered system match")
        if len(system_match_services) > 5:
            system_match_services = system_match_services[:5]
        pp.pprint(system_match_services)

        # making the subscription between the service and the best match
        try:
            system_match_services = functional_matching.subscribe(system_match_services, previous_match,
                                                                  functional_requirement["URL"])
            system_match_services[0]["state"] = True
        except Exception as e:
            print("matching error", str(e))

        # updating guidepost with a list of subscribed services and the its best matching apps
        redis_server.sadd("execution_guidepost_services", functional_requirement["URL"])
        redis_server.set(functional_requirement["URL"], str(system_match_services))

        # updating the guidepost with a list of apps and a list of services thath match the app
        print()
        print()
        for service in system_match_services:
            redis_server.sadd(service["app"], functional_requirement["URL"])
            redis_server.sadd("app_list", service["app"])
        stop_matching = time.perf_counter()  # time
        total_matching_time = stop_matching - start_matching
        file_output1 = open('instance matching.txt', 'a')  # time
        file_output1.write(str(parsing_requirements_time) + ";" + str(functional_time) + ";" + str(corpus_time) + ";"
                           + str(semantic_time) + ";" + str(syntactic_time) + ";" + str(ordering_time) + ";"
                           + str(qos_matching_time)
                           + ";" + str(sp_matching_time) + ";" + str(total_matching_time) + ";" + "\n")  # time
        file_output1.close()  # time
        # printing guidepost from redis to check if the data is stored correctly
        # print("app list")
        # pp.pprint(redis_server.smembers("app_list"))
        # print()
        # print(functional_requirement["URL"])
        # pp.pprint(ast.literal_eval(redis_server.get(functional_requirement["URL"])))

        # for service in redis_server.smembers("app_list"):
        #     print(service)
        #     pp.pprint(redis_server.smembers(service))
        #     print()

        # print("guidepost services")
        # pp.pprint(redis_server.smembers("execution_guidepost_services"))
        # print()
        # for service in redis_server.smembers("execution_guidepost_services"):
        #     print(service)
        #     pp.pprint(ast.literal_eval(redis_server.get(service)))
        #     print()




