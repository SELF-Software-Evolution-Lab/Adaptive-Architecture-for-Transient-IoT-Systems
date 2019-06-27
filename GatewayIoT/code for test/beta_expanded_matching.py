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
filename = "expanded_v2.owl"
json_file = "beta_expanded.json"
memory_beta_data = []
true_expanded_data_2 = []
predicted_expanded_data_2 = []
string_cleaning_time = list()  # added
matching_time = list()  # added
redis_server.delete("memory_beta_data")
redis_server.delete("true_expanded_data_2")
redis_server.delete("predicted_expanded_data_2")
enable_semantic = False

with open(repository+"/"+json_file, encoding='utf-8') as f:
    data = json.load(f)

for entry in data["rdf:RDF"]["Alignment"]["map"]:
    try:
        individual1 = re.findall("^http.*/(resource|property|class)/(.*)", entry["Cell"]["entity1"]['-rdf:resource'])[0][1].replace("_"," ")
        memory_beta_data.append(individual1)
        redis_server.lpush("memory_beta_data", individual1)
    except Exception as e:
        if entry["Cell"]["entity1"]['-rdf:resource'] == "null":
            continue
    try:
        individual2 = re.findall("^http.*/(resource|property|class)/(.*)", entry["Cell"]["entity2"]['-rdf:resource'])[0][1].replace("_"," ")
        true_expanded_data_2.append(individual2)
        redis_server.lpush("true_expanded_data_2", individual2)
        print(individual1, individual2)
    except Exception as e:
        true_expanded_data_2.append(entry["Cell"]["entity2"]['-rdf:resource'])
        redis_server.lpush("true_expanded_data_2", entry["Cell"]["entity2"]['-rdf:resource'])
        print(individual1, entry["Cell"]["entity2"]['-rdf:resource'])

print(len(memory_beta_data))
print(len(true_expanded_data_2))

onto_path.append(repository)
star_trek = get_ontology("file:///"+repository+"/"+filename).load()
star_trek_expanded = list()


for individual in star_trek.individuals():
    start_string_cleaning = time.perf_counter()  # added
    individual = individual.name.translate(str.maketrans(string.punctuation, ' '*len(string.punctuation)))
    individual = re.sub("GIF|svg|gif|png|jpg|JPG|jpeg|width 300", "", individual)
    stop_string_cleaning = time.perf_counter()  # added
    string_cleaning_time.append(stop_string_cleaning - start_string_cleaning)  # added
    star_trek_expanded.append(individual)

for annotation in star_trek.annotation_properties():
    star_trek_expanded.append(annotation.name)

print(len(star_trek_expanded))

count = 0
for text in memory_beta_data:
    start_matching = time.perf_counter()  # added
    count = count+1
    match_total_array = numpy.zeros(shape=(1, len(star_trek_expanded)))
    corpus1 = [text] + star_trek_expanded
    # pp.pprint(corpus1)
    # print()
    if enable_semantic:
        syntactic_array, semantic_array, a, b = syntactic_match(corpus1, "cosine")
    else:
        syntactic_array, a, b = syntactic_match(corpus1, "cosine")
    # print(syntactic_array, len(syntactic_array))
    # print(semantic_array, len(semantic_array))
    match_total_array = numpy.sum([match_total_array, syntactic_array], axis=0)
    if enable_semantic: match_total_array = numpy.sum([match_total_array, semantic_array], axis=0)
    # print(match_total_array[0])
    match_indexes = numpy.argwhere(match_total_array[0] == numpy.max(match_total_array[0]))
    # match_indexes = numpy.argwhere(match_total_array[0] == numpy.min(match_total_array[0]))
    # print(match_indexes)
    stop_matching = time.perf_counter()  # added
    matching_time.append(stop_matching - start_matching)  # added
    print(count)
    print(text)
    print(numpy.max(match_total_array[0]))
    print(star_trek_expanded[match_indexes[0][0]])
    if numpy.max(match_total_array[0]) <= 0.6:
        predicted_expanded_data_2.append("null")
        redis_server.lpush("predicted_expanded_data_2", "null")
    else:
        predicted_expanded_data_2.append(star_trek_expanded[match_indexes[0][0]])
        redis_server.lpush("predicted_expanded_data_2", star_trek_expanded[match_indexes[0][0]])
    print()
print()

file_output = open('beta_expanded.txt', 'w')  # added
file_output.write("Number of individuals;Matching time\n")  # added
for i in range(len(matching_time)):  # added
    file_output.write(str(i+1)+";"+str(matching_time[i])+"\n")  # added
file_output.close()  # added

file_output = open('beta_expanded_2.txt', 'w')  # added
file_output.write("Number of individuals;String cleaning time\n")  # added
for i in range(len(string_cleaning_time)):  # added
    file_output.write(str(i+1)+";"+str(string_cleaning_time[i])+"\n")  # added
file_output.close()  # added
