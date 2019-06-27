import redis
import json
import re
import numpy
import string
from gateway.functional_matching import syntactic_match
from pprint import pprint
from owlready2 import *
import time


pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)
repository = "/Users/jairoandresarizacastaneda/Downloads/iot datasets/OAEI"
filename = "alpha_v2.owl"
json_file = "alpha_expanded.json"
star_trek_expanded_data = []
true_alpha_data = []
predicted_alpha_data = []
string_cleaning_time = list()  # added
matching_time = list()  # added

with open(repository+"/"+json_file, encoding='utf-8') as f:
    data = json.load(f)

for entry in data["Alignment"]["map"]:
    try:
        individual1 = re.findall("^http.*/(resource|property|class)/(.*)", entry["Cell"]["entity2"]['@resource'])[0][1].replace("_", " ")
        star_trek_expanded_data.append(individual1)
        redis_server.lpush("star_trek_expanded_data", individual1)
    except Exception as e:
        if entry["Cell"]["entity2"]['@resource'] is None:
            continue
    try:
        individual2 = re.findall("^http.*/(resource|property)/(.*)", entry["Cell"]["entity1"]['@resource'])[0][1].replace("_", " ")
        true_alpha_data.append(individual2)
        redis_server.lpush("true_alpha_data", individual2)
        print(individual1, individual2)
    except Exception as e:
        true_alpha_data.append(entry["Cell"]["entity1"]['@resource'])
        redis_server.lpush("true_alpha_data", str(entry["Cell"]["entity1"]['@resource']))
        print(individual1, entry["Cell"]["entity1"]['@resource'])

print(len(star_trek_expanded_data))
print(len(true_alpha_data))

onto_path.append(repository)
star_trek = get_ontology("file:///"+repository+"/"+filename).load()
star_trek_alpha = list()


for individual in star_trek.individuals():
    start_string_cleaning = time.perf_counter()  # added
    individual = individual.name.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    individual = re.sub("GIF|svg|gif|png|jpg|JPG|jpeg|width 300", "", individual)
    stop_string_cleaning = time.perf_counter()  # added
    string_cleaning_time.append(stop_string_cleaning-start_string_cleaning)  # added
    star_trek_alpha.append(individual)

for annotation in star_trek.annotation_properties():
    star_trek_alpha.append(annotation.name)

print(len(star_trek_alpha))

count = 0
for text in star_trek_expanded_data:
    start_matching = time.perf_counter()  # added
    count = count+1
    match_total_array = numpy.zeros(shape=(1, len(star_trek_alpha)))
    corpus1 = [text] + star_trek_alpha
    # pp.pprint(corpus1)
    # print()
    syntactic_array, semantic_array, a, b = syntactic_match(corpus1, "cosine")
    # print(syntactic_array, len(syntactic_array))
    # print(semantic_array, len(semantic_array))
    match_total_array = numpy.sum([match_total_array, syntactic_array], axis=0)
    match_total_array = numpy.sum([match_total_array, semantic_array], axis=0)
    # print(match_total_array[0])
    match_indexes = numpy.argwhere(match_total_array[0] == numpy.max(match_total_array[0]))
    # match_indexes = numpy.argwhere(match_total_array[0] == numpy.min(match_total_array[0]))
    # print(match_indexes)
    stop_matching = time.perf_counter()  # added
    matching_time.append(stop_matching - start_matching)  # added
    print(count)
    print(text)
    print(numpy.max(match_total_array[0]))
    print(star_trek_alpha[match_indexes[0][0]])
    if numpy.max(match_total_array[0]) == 0:
        predicted_alpha_data.append(None)
        redis_server.lpush("predicted_alpha_data", "None")
    else:
        predicted_alpha_data.append(star_trek_alpha[match_indexes[0][0]])
        redis_server.lpush("predicted_alpha_data", star_trek_alpha[match_indexes[0][0]])
    print()
print()

