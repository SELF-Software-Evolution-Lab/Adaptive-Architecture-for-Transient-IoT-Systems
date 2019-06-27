import time
import uuid
import random
import string
from owlready2 import *


def app_physical_properties(properties, functional, qos_prop):
    properties["Sensor"] = sosa.Sensor(functional["App Name"])
    properties["System Capability"] = systems.SystemCapability("System_capability_" + functional["App Name"])
    properties["Sensor"].hasSystemCapability = [properties["System Capability"]]


def app_Service_properties(properties, functional, qos_prop):
    Service_name = str(uuid.uuid4())
    properties["Sensor_service"] = modified_SSN.Provider(functional["App Name"] + "_URL_" + Service_name)
    properties["Sensor"].hasService.append(properties["Sensor_service"])
    properties["Sensor_service"].hasStringValue = [functional["Base URL"] + functional["Relative URL"]]
    properties["subscribe"] = modified_SSN.Subscribe("Subscribe_" + functional["App Name"])
    properties["get_last"] = modified_SSN.Read("Read_last_" + functional["App Name"])
    properties["Sensor_service"].hasMethod = [properties["subscribe"], properties["get_last"]]
    properties["subscribe"].hasStringValue = [functional["Base URL"] + functional["Relative URL"] + "/" +
                                              functional["DATA"]["rn"]]
    properties["subscribe"].hasBodyField = [modified_SSN.valor]
    properties["get_last"].hasStringValue = [functional["Base URL"] + functional["DATA"]["la"]]
    properties["get_last"].hasBodyField = [modified_SSN.valor]
    properties["obs"] = sosa.Observation()
    properties["Sensor_service"].madeObservation = [properties["obs"]]
    if "Category" in functional.keys():
        properties["variable"] = sosa.ObservableProperty(functional["Category"])
        properties["obs"].observedProperty = [properties["variable"]]
    if "Unit" in functional.keys():
        properties["unit"] = modified_SSN.Unit(functional["Unit"])
        properties["obs"].hasUnit = [properties["unit"]]
    if "Location" in functional.keys():
        properties["location"] = modified_SSN.Location(functional["Location"])
        properties["Sensor_service"].hasLocation = [properties["location"]]


def qos_system_properties(quality_list, quality_list_2, units):
    i = 0
    for quality in quality_list:
        for clase in list(modified_SSN.classes()):
            for key, value in quality.items():
                if clase.name == key:
                    if type(value) is dict:
                        quality_list_2[i][key] = clase(key + "_" + str(value["value"]))
                        if type(value["value"]) is str:
                            quality_list_2[i][key].hasStringValue = [value["value"]]
                        if type(value["value"]) is float or type(value["value"]) is int:
                            quality_list_2[i][key].hasNumericValue = [float(value["value"])]
                        if type(value["value"]) is bool:
                            quality_list_2[i][key].hasBoolean = [value["value"]]
                        # if value["unit"] not in instances:
                        units[value["unit"]] = modified_SSN.Unit(value["unit"])
                        quality_list_2[i][key].hasUnit = [units[value["unit"]]]
                        # else:
                        #     quality_list_2[i][key].hasUnit = [onto_hub.__getitem__(value["unit"])]
                    else:
                        quality_list_2[i][key] = clase(key + "_" + str(value))
                        if type(value) is str:
                            quality_list_2[i][key].hasStringValue = [value]
                        if type(value) is float or type(value) is int:
                            quality_list_2[i][key].hasNumericValue = [float(value)]
                        if type(value) is bool:
                            quality_list_2[i][key].hasBoolean = [value]
                    if key in ["Accuracy", "ActuationRange", "DetectionLimit", "Drift", "Frequency",
                               "MeasurementRange", "Precision", "Resolution", "Sensitivity", "Cost", "Latency"]:
                        quality_list_2[i][key].hasConstraintOperator = [modified_SSN.lower_than_equal]
                    elif key in ['Availability', "Capacity", "Throughput", "MTBF"]:
                        quality_list_2[i][key].hasConstraintOperator = [modified_SSN.greater_than_equal]
                    else:
                        quality_list_2[i][key].hasConstraintOperator = [modified_SSN.equal]
        i = i + 1


def app_instance_load(functional, qos_prop):
    instances = [individual.name for individual in modified_SSN.individuals()]
    # for clase in memory_alpha.classes():
    #     print(clase)
    properties = dict()
    system_property = dict()
    qos_instance = dict()
    units = dict()
    if functional["App Name"] not in instances:
        print(functional["App Name"])
        app_physical_properties(properties, functional, qos_prop)
        app_Service_properties(properties, functional, qos_prop)
        quality_list = [functional["System property"], qos_prop]
        quality_list_2 = [system_property, qos_instance]
        qos_system_properties(quality_list, quality_list_2, units)

        a = list(quality_list_2[0].values())
        b = list(quality_list_2[1].values())
        properties["System Capability"].hasSystemProperty = a
        properties["Sensor_service"].hasQoSParameter = b
        c = a + b + list(properties.values()) + list(units.values())
        different_individuals = list(modified_SSN.different_individuals())[0]
        different_individuals.entities.extend(c)
    else:
        properties["Sensor"] = sosa.Sensor(functional["App Name"])
        app_Service_properties(properties, functional, qos_prop)
        quality_list = [qos_prop]
        quality_list_2 = [qos_instance]
        qos_system_properties(quality_list, quality_list_2, units)
        b = list(quality_list_2[0].values())
        properties["Sensor_service"].hasQoSParameter = b
        c = b + list(properties.values()) + list(units.values())
        different_individuals = list(modified_SSN.different_individuals())[0]
        different_individuals.entities.extend(c)


repository = "/Users/jairoandresarizacastaneda/Desktop/IoT_segundo_semestre/codigo_gateway/ontology/repository"
filename = "mod_SSN_agua.owl"
onto_path.append(repository)
modified_SSN = get_ontology("file:///"+repository+"/"+filename).load()
parsing = list()
reasoning = list()
saving = list()
for space in modified_SSN._namespaces:
    if "sosa" in space:
        sosa = modified_SSN.get_namespace(space)
    elif space.endswith("ssn/"):
        ssn = modified_SSN.get_namespace(space)
    elif "systems" in space:
        systems = modified_SSN.get_namespace(space)
    elif "skos" in space:
        skos = modified_SSN.get_namespace(space)


for j in range(1):
    print("Individual number", j)
    letters = string.ascii_uppercase
    letter = random.choice([0.5])
    letter_number = letter
    print(letter_number*2)
    name = random.choice(["RG-200"])
    # Service_name = str(uuid.uuid4())
    location = random.choice(["ML"])
    category = random.choice(["Rain rate"])
    unit_time = ["s", "hr"]
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
    functional_prop = {'Base URL': 'http://192.168.0.7:8080/~', 'Relative URL': '/in-cse/in-name/'+name,
                       'lbl': ['Cat/'+category, 'Loc/'+location, 'Typ/Sensor', 'Unit/'+random.choice(unit)],
                       'Category': category, 'Location': location, 'Unit': m_unit,
                       'DATA': {'rn': 'DATA', 'ty': 3, 'ri': '/in-cse/cnt-872275463', 'pi': '/in-cse/CAE283708670',
                                'ct': '20180717T180620', 'lt': '20180717T180620', 'acpi': ['/in-cse/acp-874554584'],
                                'et': '20190717T180620', 'st': 14114, 'mni': 10, 'mbs': 10000, 'mia': 0, 'cni': 10,
                                'cbs': 100, 'ol': '/in-cse/in-name/'+name+'/DATA/ol',
                                'la': '/in-cse/in-name/'+name+'/DATA/la'},
                       'Healthcheck': {'rn': 'Healthcheck', 'ty': 3, 'ri': '/in-cse/cnt-38108401',
                                       'pi': '/in-cse/CAE283708670','ct': '20180705T110847', 'lt': '20180726T142558',
                                       'acpi': ['/in-cse/acp-874554584'], 'et': '20190705T110847', 'st': 10856, 'mni': 10,
                                       'mbs': 10000, 'mia': 0, 'cni': 10, 'cbs': 80,
                                       'ol': '/in-cse/in-name/'+name+'/Healthcheck/ol',
                                       'la': '/in-cse/in-name/'+name+'/Healthcheck/la'},
                       'QoS': {'rn': 'QoS', 'ty': 3, 'ri': '/in-cse/cnt-48012623', 'pi': '/in-cse/CAE283708670',
                               'ct': '20180803T153443', 'lt': '20180803T153443', 'acpi': ['/in-cse/acp-874554584'],
                               'et': '20190803T153443', 'st': 16, 'mni': 10, 'mbs': 10000, 'mia': 0, 'cni': 10, 'cbs': 908,
                               'ol': '/in-cse/in-name/'+name+'/QoS/ol', 'la': '/in-cse/in-name/'+name+'/QoS/la'},
                       'Date': '2018-08-31 21:52:33.418998', 'Readings': [], 'Health check estimated time': 10,
                       'State': False, 'Lost health checks': 0, 'Parent': 'in-cse', 'App Name': name,
                       "System property": {"Accuracy": {"value": 3, "unit": "%"},
                                           "ActuationRange": "none",
                                           "DetectionLimit": {"value": 0.01, "unit": "in"},
                                           "Drift": "none",
                                           "Frequency": {"value": 6, "unit": "m"},
                                           "Latency": {"value": 135, "unit": "ms"},
                                           "MeasurementRange": {"value": "N/A", "unit": "N/A"},
                                           "Precision": {"value": 0.01, "unit": "in"},
                                           "Resolution": {"value": 0.01, "unit": "in"},
                                           "ResponseTime": {"value": 135, "unit": "ms"},
                                           "Selectivity": "none", "Sensitivity": "none"}}

    start_instantiation = time.perf_counter()
    app_instance_load(functional_prop, QoS)
    start_reasoner = time.perf_counter()
    print("Parsing time", start_reasoner - start_instantiation, "seconds")
    parsing.append(start_reasoner - start_instantiation)
    # sync_reasoner()
    stop_reasoner = time.perf_counter()
    print("Reasoning time", stop_reasoner - start_reasoner, "seconds")
    reasoning.append(stop_reasoner - start_reasoner)
    modified_SSN.save()
    stop_saving = time.perf_counter()
    print("Saving time", stop_saving - stop_reasoner, "seconds")
    saving.append(stop_saving - stop_reasoner)
    print()

# file_output = open('output.txt', 'w')
# file_output.write("Number of individuals;Parsing time;Reasoning Time;Saving time\n")
# for i in range(len(parsing)):
#     file_output.write(str(i+1)+";"+str(parsing[i])+";"+str(reasoning[i])+";"+str(saving[i])+"\n")
# file_output.close()
