import random
import sys
import redis
sys.path.append("/home/profesor/GatewayIoT")
from gateway.instance_matching import instance_matching
from gateway import ontology_as_classes


pool = redis.ConnectionPool(host='172.24.100.98', port=8080, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)


location_list = ["room", "kitchen", "garage", "Backyard", "Bogota", "Colombia", "USA", "ML", "University", "Balcony",
                 "attic", "playroom", "bedroom", "bathroom", "laboratory", "bosa", "suba", "kennedy", "candelaria",
                 "centro", "niza", "galerias", "castellana", "soledad", "puente_aranda"]
category_list = ["Level", "temperature", "pressure", "CO2", "flow", "fire", "power", "sound", "moisture",
                 "vibration", "distance", "rain"]

units = {"Level": ["m", "cm", "mm", "in", "ft"], "temperature": ["C", "K", "F"],
         "pressure": ["psig", "pascal", "bar", "at", "atm", "Torr"], "CO2": ["ppm", "%c"], "flow": ["m3/s", "ft3/s"],
         "fire": ["kW/m2", "W/m2", "W/in2"], "power": ["W", "kW", "hp"], "sound": ["dB", "sone"],
         "moisture": ["%h"], "vibration": ["ips", "mm/s"], "distance": ["m", "cm", "mm", "in", "ft"],
         "rain": ["mm", "in"]}

services = ontology_as_classes.get_providers()

for i in range(3000):
    # user requirements
    matches_number = redis_server.smembers("execution_guidepost_services")
    if len(matches_number) == 500:
        break
    category = random.choice(category_list)
    location = random.choice(location_list)
    unit = random.choice(units[category])
    application = random.choice(["monitoring", "non critical alarms", "control", "critical alarms"])

    functional_requirement1 = {"Name": "weather", "Location": location, "Category": category, "Unit": unit,
                               "threshold": 0.41,
                               "URL": "http://127.0.0.1:" + str(i), "application": application}
    if functional_requirement1["URL"] in matches_number:
        continue
        print("founded")
    else:
        # generating random system properties requirements
        system_properties_requirement1 = {'Accuracy': {'value': round(random.random(), 2), 'unit': '%'},
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


        # generating random QoS requirements
        unit_coin = ["USD", "COL", "CAD", "CHF", "JPY", "EUR"]
        binary = [True, False]
        quantitative = ["high", "medium", "low", "very_low", "very_high"]
        QoS_requirement1 = {"Availability": {"value": round(random.random(), 2), "unit": "%"}, "Capacity": "TBD",
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

        instance_matching(functional_requirement1, system_properties_requirement1, QoS_requirement1, None, services)
        matches_number = len(redis_server.smembers("execution_guidepost_services"))
        print("numero de emparejamientos", matches_number)




