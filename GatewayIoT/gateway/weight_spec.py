import json
import pprint
import redis


pp = pprint.PrettyPrinter(depth=6)
# pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
pool = redis.ConnectionPool(host='172.24.100.98', port=8080, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)

monitoring_weight = {
    "System property": {"Accuracy": 0.5, "ActuationRange": 0, "DetectionLimit": 0.75, "Drift": 0.5, "Frequency": 0.5,
                        "Latency": 0.5, "MeasurementRange": 1, "Precision": 0.5, "Resolution": 0.5,
                        "ResponseTime": 0.5, "Selectivity": 0.5, "Sensitivity": 0.5},
    "QoS": {"Availability": 0.5, "Capacity": 0.5, 'Cost': 1, "Interoperability": 0.5, "Throughput": 0.5,
            "Consistency": 0.5, "Messaging": 0.5, "MTBF": 0.5, "Disaster": 0.5, "Failover": 0.5, "Reputation": 0.5,
            "Robustness": 0.5, "Scalability": 0.5, "Auditability": 0.5, 'Authentication': 0.5, 'Data_encryption': 0.75,
            'Message_encryption': 0.75, "Non_repudiation": 0.5, 'Method_stability': 0.5, "Interface_stability": 0.75}}

system_values = list(monitoring_weight["System property"].values())
system_average = sum(system_values)/len(system_values)
monitoring_weight["System property"]["Weight Average"] = system_average

qos_values = list(monitoring_weight["QoS"].values())
qos_average = sum(qos_values)/len(qos_values)
monitoring_weight["QoS"]["Weight Average"] = qos_average


non_critical_alarms_weight = {
    "System property": {"Accuracy": 0.75, "ActuationRange": 0, "DetectionLimit": 0.8, "Drift": 0.5, "Frequency": 0.75,
                        "Latency": 0.5, "MeasurementRange": 1, "Precision": 0.5, "Resolution": 0.5,
                        "ResponseTime": 0.75, "Selectivity": 0.5, "Sensitivity": 0.5},
    "QoS": {"Availability": 0.75, "Capacity": 0.5, 'Cost': 1, "Interoperability": 0.5, "Throughput": 0.5,
            "Consistency": 0.5, "Messaging": 0.5, "MTBF": 0.5, "Disaster": 0.5, "Failover": 0.5, "Reputation": 0.75,
            "Robustness": 0.5, "Scalability": 0.5, "Auditability": 0.75, 'Authentication': 0.5, 'Data_encryption': 0.75,
            'Message_encryption': 0.75, "Non_repudiation": 0.5, 'Method_stability': 0.75, "Interface_stability": 0.75}}

system_values = list(non_critical_alarms_weight["System property"].values())
system_average = sum(system_values)/len(system_values)
non_critical_alarms_weight["System property"]["Weight Average"] = system_average

qos_values = list(non_critical_alarms_weight["QoS"].values())
qos_average = sum(qos_values)/len(qos_values)
non_critical_alarms_weight["QoS"]["Weight Average"] = qos_average


control_weight = {
    "System property": {"Accuracy": 0.75, "ActuationRange": 0, "DetectionLimit": 1, "Drift": 1, "Frequency": 1,
                        "Latency": 1, "MeasurementRange": 1, "Precision": 1, "Resolution": 1,
                        "ResponseTime": 0.75, "Selectivity": 0.5, "Sensitivity": 0.5},
    "QoS": {"Availability": 1, "Capacity": 0.8, 'Cost': 0.5, "Interoperability": 1, "Throughput": 0.75,
            "Consistency": 1, "Messaging": 0.5, "MTBF": 0.75, "Disaster": 0.75, "Failover": 0.75, "Reputation": 1,
            "Robustness": 1, "Scalability": 0.5, "Auditability": 1, 'Authentication': 0.75, 'Data_encryption': 0.75,
            'Message_encryption': 0.75, "Non_repudiation": 1, 'Method_stability': 0.75, "Interface_stability": 1}}

system_values = list(control_weight["System property"].values())
system_average = sum(system_values)/len(system_values)
control_weight["System property"]["Weight Average"] = system_average

qos_values = list(control_weight["QoS"].values())
qos_average = sum(qos_values)/len(qos_values)
control_weight["QoS"]["Weight Average"] = qos_average


critical_alarms_weight = {
    "System property": {"Accuracy": 1, "ActuationRange": 0, "DetectionLimit": 1, "Drift": 0.75, "Frequency": 1,
                        "Latency": 0.75, "MeasurementRange": 1, "Precision": 0.75, "Resolution": 0.75,
                        "ResponseTime": 1, "Selectivity": 0.5, "Sensitivity": 0.5},
    "QoS": {"Availability": 1, "Capacity": 1, 'Cost': 0.5, "Interoperability": 0.75, "Throughput": 0.75,
            "Consistency": 1, "Messaging": 1, "MTBF": 1, "Disaster": 1, "Failover": 1, "Reputation": 1,
            "Robustness": 1, "Scalability": 0.5, "Auditability": 1, 'Authentication': 1, 'Data_encryption': 1,
            'Message_encryption': 1, "Non_repudiation": 1, 'Method_stability': 1, "Interface_stability": 1}}

system_values = list(critical_alarms_weight["System property"].values())
system_average = sum(system_values)/len(system_values)
critical_alarms_weight["System property"]["Weight Average"] = system_average

qos_values = list(critical_alarms_weight["QoS"].values())
qos_average = sum(qos_values)/len(qos_values)
critical_alarms_weight["QoS"]["Weight Average"] = qos_average


all_weights = {"monitoring_weight": monitoring_weight, "non_critical_alarms_weight": non_critical_alarms_weight,
               "control_weight": control_weight, "critical_alarms_weight": critical_alarms_weight}

pp.pprint(all_weights)
redis_server.set("monitoring", str(monitoring_weight))
redis_server.set("non critical alarms", str(non_critical_alarms_weight))
redis_server.set("control", str(control_weight))
redis_server.set("critical alarms", str(critical_alarms_weight))


# with open('all_weights.json', 'w') as fp:
#     json.dump(all_weights, fp)

# with open('monitoring_weight.json', 'w') as fp:
#     json.dump(monitoring_weight, fp)

# with open('non_critical_alarms_weight.json', 'w') as fp:
#     json.dump(non_critical_alarms_weight, fp)

# with open('control_weight.json', 'w') as fp:
#     json.dump(control_weight, fp)

# with open('critical_alarms_weight.json', 'w') as fp:
#     json.dump(critical_alarms_weight, fp)

# for key, value in all_weights.items():
#     print(value["System property"])
#     print(value["QoS"])
