import time
import uuid
import random
from owlready2 import *


def app_instance_load(functional, qos_prop):
    instances = [individual.name for individual in onto_hub.individuals()]
    if functional["App Name"] not in instances:
        properties = dict()
        properties["IoT_device"] = onto_hub.IoT_device(functional["App Name"])
        properties["IoT_device_url"] = onto_hub.URL(functional["App Name"] + "_URL")
        properties["subscribe"] = onto_hub.Subscribe("Subscribe_" + functional["App Name"])
        properties["get_last"] = onto_hub.Read("Read_last_" + functional["App Name"])
        properties["IoT_device"].hasAPIURL = [properties["IoT_device_url"]]
        properties["IoT_device_url"].hasStringValue = [functional["Base URL"] + functional["Relative URL"]]
        properties["IoT_device"].hasMethod = [properties["subscribe"], properties["get_last"]]
        properties["obs"] = onto_hub.Observation()
        if "Category" in functional.keys():
            properties["variable"] = onto_hub.Property(functional["Category"])
            properties["IoT_device"].hasObservation = [properties["obs"]]
            properties["obs"].aboutProperty = [properties["variable"]]
        if "Unit" in functional.keys():
            properties["unit"] = onto_hub.Unit(functional["Unit"])
            properties["obs"].hasUnit = [properties["unit"]]
        if "Location" in functional.keys():
            properties["location"] = onto_hub.Location(functional["Location"])
            properties["IoT_device"].hasLocation = [properties["location"]]
        properties["subscribe"].hasStringValue = [functional["Base URL"] + functional["Relative URL"] + "/" + functional["DATA"]["rn"]]
        properties["subscribe"].hasBodyfield = [onto_hub.valor]
        properties["get_last"].hasStringValue = [functional["Base URL"] + functional["DATA"]["la"]]
        properties["get_last"].hasBodyfield = [onto_hub.valor]

        system_property = dict()
        qos_instance = dict()
        units = dict()
        quality_list = [functional["System property"], qos_prop]
        quality_list_2 = [system_property, qos_instance]
        i = 0
        for quality in quality_list:
            for clase in list(onto_hub.classes()):
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
                            units[value["unit"]] = onto_hub.Unit(value["unit"])
                            quality_list_2[i][key].hasUnit = [units[value["unit"]]]
                            # else:
                            #     quality_list_2[i][key].hasUnit = [onto_hub.__getitem__(value["unit"])]
                        else:
                            quality_list_2[i][key] = clase(key+"_"+str(value))
                            if type(value) is str:
                                quality_list_2[i][key].hasStringValue = [value]
                            if type(value) is float or type(value) is int:
                                quality_list_2[i][key].hasNumericValue = [float(value)]
                            if type(value) is bool:
                                quality_list_2[i][key].hasBoolean = [value]
                        if key in ["Accuracy", "Actuation_Range", "Detection_limit", "Drift", "Frequency",
                                   "Measurement_range", "Precision", "Resolution", "Sensitivity", "Cost"]:
                            quality_list_2[i][key].hasConstraintOperator = [onto_hub.lower_than_equal]
                        elif key in ['Availability', "Capacity", "Throughput", "MTBF"]:
                            quality_list_2[i][key].hasConstraintOperator = [onto_hub.greater_than_equal]
                        else:
                            quality_list_2[i][key].hasConstraintOperator = [onto_hub.equal]
            i = i+1
        a = list(quality_list_2[0].values())
        b = list(quality_list_2[1].values())
        properties["IoT_device"].hasSystemProperty = a
        properties["IoT_device"].hasQoSParameter = b
        c = a+b+list(properties.values())+list(units.values())
        different_individuals = list(onto_hub.different_individuals())[0]
        different_individuals.entities.extend(c)

repository = "/Users/jairoandresarizacastaneda/Desktop/IoT_segundo_semestre/codigo_gateway/ontology/repository"
filename = "hub_iot_qos.owl"
onto_path.append(repository)
onto_hub = get_ontology("file:///"+repository+"/"+filename).load()

parsing = list()
reasoning = list()
saving = list()

for i in range(3):
    print("Individual number", i)
    name = str(uuid.uuid4())
    location = random.choice(["room", "kitchen", "garage", "Backyard", "Bogota", "Colombia", "USA", "ML", "University",
                              "Balcony", "attic", "playroom", "bedroom", "bathroom"])
    category = random.choice(["Level", "temperature", "pressure", "CO2", "flow", "power", "fire", "position", "sound",
                              "moisture", "vibration", "distance"])
    unit = ["m", "s", "mm", "hr", "C", "F", "K", "psi", "ppm", "W", "dB", "/s", "Hz", "in", "ft", "cm", "day", "year", "km",
            "%"]
    binary = [True, False]
    quantitative = ["high", "medium", "low", "very_low", "very_high"]

    QoS = {"Availability": {"value": round(random.random(), 2), "unit": "%"}, "Capacity": "TBD",
           'Cost': {"value": random.randint(0, 1000), "unit": random.choice(unit)}, "Interoperability": random.choice(binary),
           "Throughput": {"value": random.randint(0, 1000), "unit": random.choice(unit)}, "Consistency": "TBD", "Messaging": "TBD",
           "MTBF": {"value": random.randint(0, 8760), "unit": random.choice(unit)}, "Disaster": random.choice(binary),
           "Failover": random.choice(binary), "Reputation": random.choice(binary), "Robustness": random.choice(quantitative),
           "Scalability": random.choice(quantitative), "Auditability": random.choice(binary),
           'Authentication': random.choice(binary),
           'Data_encryption': random.choice(binary), 'Message_encryption': random.choice(binary),
           "Non_repudiation": random.choice(binary), 'Method_stability': random.choice(quantitative),
           "Interface_stability": random.choice(quantitative)}

    functional_prop = {'Base URL': 'http://192.168.0.7:8080/~', 'Relative URL': '/in-cse/in-name/'+name,
                       'lbl': ['Cat/'+category, 'Loc/'+location, 'Typ/Sensor', 'Unit/'+random.choice(unit)], 'Category': category,
                       'Location': location, 'Unit': random.choice(unit),
                       'DATA': {'rn': 'DATA', 'ty': 3, 'ri': '/in-cse/cnt-872275463', 'pi': '/in-cse/CAE283708670',
                                'ct': '20180717T180620', 'lt': '20180717T180620', 'acpi': ['/in-cse/acp-874554584'],
                                'et': '20190717T180620', 'st': 14114, 'mni': 10, 'mbs': 10000, 'mia': 0, 'cni': 10,
                                'cbs': 100, 'ol': '/in-cse/in-name/Tank_level/DATA/ol',
                                'la': '/in-cse/in-name/Tank_level/DATA/la'},
                       'Healthcheck': {'rn': 'Healthcheck', 'ty': 3, 'ri': '/in-cse/cnt-38108401',
                                       'pi': '/in-cse/CAE283708670','ct': '20180705T110847', 'lt': '20180726T142558',
                                       'acpi': ['/in-cse/acp-874554584'], 'et': '20190705T110847', 'st': 10856, 'mni': 10,
                                       'mbs': 10000, 'mia': 0, 'cni': 10, 'cbs': 80,
                                       'ol': '/in-cse/in-name/Tank_level/Healthcheck/ol',
                                       'la': '/in-cse/in-name/Tank_level/Healthcheck/la'},
                       'QoS': {'rn': 'QoS', 'ty': 3, 'ri': '/in-cse/cnt-48012623', 'pi': '/in-cse/CAE283708670',
                               'ct': '20180803T153443', 'lt': '20180803T153443', 'acpi': ['/in-cse/acp-874554584'],
                               'et': '20190803T153443', 'st': 16, 'mni': 10, 'mbs': 10000, 'mia': 0, 'cni': 10, 'cbs': 908,
                               'ol': '/in-cse/in-name/Tank_level/QoS/ol', 'la': '/in-cse/in-name/Tank_level/QoS/la'},
                       'Date': '2018-08-31 21:52:33.418998', 'Readings': [], 'Health check estimated time': 10,
                       'State': False, 'Lost health checks': 0, 'Parent': 'in-cse', 'App Name': name,
                       "System property": {"Accuracy": {"value": round(random.random(), 2), "unit": "%"},
                                           "Actuation_Range": "none",
                                           "Detection_limit": {"value": random.randint(0, 100), "unit": random.choice(unit)},
                                           "Drift": "none",
                                           "Frequency": {"value": random.randint(0, 100), "unit": random.choice(unit)},
                                           "Measurement_range": {"value": "0-8", "unit": random.choice(unit)},
                                           "Precision": {"value": round(random.random(),2), "unit": random.choice(unit)},
                                           "Resolution": {"value": random.randint(0, 100), "unit": random.choice(unit)},
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
    onto_hub.save()
    stop_saving = time.perf_counter()
    print("Saving time", stop_saving - stop_reasoner, "seconds")
    saving.append(stop_saving - stop_reasoner)

file_output = open('output.txt', 'w')
file_output.write("Number of individuals;Parsing time;Reasoning Time;Saving time\n")
for i in range(len(parsing)):
    file_output.write(str(i+1)+";"+str(parsing[i])+";"+str(reasoning[i])+";"+str(saving[i])+"\n")
file_output.close()


