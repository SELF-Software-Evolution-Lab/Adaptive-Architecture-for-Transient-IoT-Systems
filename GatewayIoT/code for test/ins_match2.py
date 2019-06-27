import random
import string
from gateway.instance_matching import instance_matching


# user requirements
functional_requirement1 = {"Name": "weather", "Location": "home", "Category": "rain", "Unit": "in", "threshold": 0.5,
                          "URL": "http://127.0.0.1:1400/monitor", "application": "control"}

# generating random system properties requirements
letters = string.ascii_uppercase
letter = random.choice(letters)
letter_number = letters.index(letter)
system_properties_requirement1 = {"Accuracy": {"value": letter_number / 100 * 2, "unit": "%"}, "ActuationRange": "None",
                                 "DetectionLimit": {"value": [1, 2], "unit": "ft"}, "Drift": "None",
                                 "DetectionLimit": {"value": letter_number, "unit": "ft"}, "Drift": "None",
                                 "Frequency": {"value": letter_number, "unit": "s"},
                                 "Latency": {"value": letter_number, "unit": "s"},
                                 "MeasurementRange": {"value": "0-"+str(letter_number), "unit": "ft"},
                                 "Precision": {"value": letter_number/100*2, "unit": "in"},
                                 "Resolution": {"value": letter_number, "unit": "in"},
                                 "ResponseTime": {"value": letter_number, "unit": "ms"}, "Selectivity": "None",
                                 "Sensitivity": "None"}

# generating random QoS requirements
unit = ["in"]
unit_coin = ["USD", "COL"]
binary = [True, False]
quantitative = ["high", "medium", "low", "very_low", "very_high"]
m_unit = random.choice(unit)
# QoS_requirement = {"Availability": {"value": [0.99, 0.4], "unit": "%"}, "Capacity": "TBD",
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

# print(system_properties_requirement1.keys())
# device = "#http://127.0.0.1:8282/~/mn-cse/mn-name/Drenaje1"
device = "http://127.0.0.1:8080/~/in-cse/in-name/park_rain1"
# device = "http://127.0.0.1:8282/~/mn-cse/mn-name/park_rain1"
# device = "http://127.0.0.1:8080/~/in-cse/in-name/Drenaje2"

instance_matching(functional_requirement1, system_properties_requirement1, QoS_requirement1, None)
# instance_matching(functional_requirement1, system_properties_requirement1, QoS_requirement1, device)
