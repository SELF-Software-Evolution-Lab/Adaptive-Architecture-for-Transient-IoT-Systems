import string
# import redis
# import ast
# import numpy
# import requests
# import json
import random
# from sklearn.feature_extraction.text import CountVectorizer
# from sklearn.metrics.pairwise import cosine_distances
# from sklearn.metrics.pairwise import euclidean_distances
# from nltk.corpus import wordnet as wn
from owlready2 import *

# functional_requirement = {"Name": "weather", "Location": "home", "Category": "temp", "Unit": "Celsius",
#         "URL": "http://"+ip_address+":1400/monitor"}


def boolean_eval(number1, constraint, number2):
    if constraint == "equal":
        logic_value = int(number1 == number2)
    elif constraint == "greater_than":
        logic_value = int(number1 > number2)
    elif constraint == "greater_than_equal":
        logic_value = int(number1 >= number2)
    elif constraint == "lower_than":
        logic_value = int(number1 < number2)
    elif constraint == "lower_than_equal":
        logic_value = int(number1 <= number2)
    return logic_value


def unit_eval(unit1, unit2):
    unit_value = int(unit1 == unit2)
    return unit_value


def qos_matching(requirement):
    match_list = modified_SSN.search(is_a=systems.SystemCapability)
    print(match_list)
    corpus = {}
    # match_total_array = numpy.zeros(shape=(1, len(match_list) - 1))
    requirement_properties = []
    for require in requirement.keys():
        if require not in ["ActuationRange", "Drift", "MeasurementRange", "Selectivity", "Sensitivity"]:
            requirement_properties.append(require)
    # requirement_properties = list(requirement.keys())
    # print(requirement_properties)
    matching_vector = []
    for match in match_list:
        match_value = 0
        # value_vector = []
        # unit_vector = []
        # total_vector = []
        # print(match)
        physical_properties = match.hasSystemProperty
        # print(physical_properties)
        for requirement_property in requirement_properties:
            # print(requirement_property)
            for physical_property in physical_properties:
                if requirement_property == physical_property.is_a[0].name:
                    offered = physical_property.hasNumericValue[0]
                    operator = physical_property.hasConstraintOperator[0].name
                    required = requirement[requirement_property]["value"]
                    offered_unit = physical_property.hasUnit[0].name
                    required_unit = requirement[requirement_property]["unit"]
                    # print("offered", offered)
                    # print(operator)
                    # print("required", required)
                    # print(offered_unit)
                    # print(required_unit)
                    evaluation = boolean_eval(offered, operator, required)
                    unit_evaluation = unit_eval(offered_unit, required_unit)
                    match_value += evaluation*unit_evaluation
                    # value_vector.append(evaluation)
                    # unit_vector.append(unit_evaluation)
                    # total_vector.append(evaluation*unit_evaluation)
        matching_vector.append(match_value)
        # print(value_vector)
        # print(unit_vector)
        # print(total_vector)
    print(matching_vector)
    # print(len(value_vector))
    # print(len(match_list))



repository = "/Users/jairoandresarizacastaneda/Desktop/IoT_segundo_semestre/codigo_gateway/ontology/repository"
filename = "mod_SSN.owl"
onto_path.append(repository)
modified_SSN = get_ontology("file:///"+repository+"/"+filename).load()
for space in modified_SSN._namespaces:
    if "sosa" in space:
        sosa = modified_SSN.get_namespace(space)
    elif space.endswith("ssn/"):
        ssn = modified_SSN.get_namespace(space)
    elif "systems" in space:
        systems = modified_SSN.get_namespace(space)
    elif "skos" in space:
        skos = modified_SSN.get_namespace(space)


letters = string.ascii_uppercase
letter = random.choice(letters)
letter_number = letters.index(letter)
unit = ["C", "F", "K", "psi", "ppm", "W", "dB", "/s", "Hz",  "day", "year", "%", "m", "mm", "in", "ft", "cm", "km"]
m_unit = random.choice(unit)

qos_requirement = {"Accuracy": {"value": letter_number/100*2, "unit": "%"}, "ActuationRange": "none",
                   "DetectionLimit": {"value": letter_number, "unit": m_unit}, "Drift": "none",
                   "Frequency": {"value": letter_number, "unit": "s"}, "Latency": {"value": letter_number, "unit": "s"},
                   "MeasurementRange": {"value": "0-"+str(letter_number), "unit": m_unit},
                   "Precision": {"value": letter_number/100*2, "unit": "%"},
                   "Resolution": {"value": letter_number, "unit": m_unit},
                   "ResponseTime": {"value": letter_number, "unit": "s"}, "Selectivity": "none", "Sensitivity": "none"}

print(qos_requirement)
print()

qos_matching(qos_requirement)

