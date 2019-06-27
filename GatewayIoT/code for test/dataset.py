import json
import numpy
import pprint
from gateway.functional_matching import syntactic_match

file = "/Users/jairoandresarizacastaneda/Downloads/pruebas tesis/articulo1/yelp_dataset/tip.json"
# file = "/Users/jairoandresarizacastaneda/Desktop/IoT_segundo_mestre/pruebas/articulo1/yelp_dataset/tip.json"
pp = pprint.PrettyPrinter(depth=6)
y_test = []
y_pred = []
count = 0
for line in open(file, 'r', encoding='utf-8'):
    y_test.append(json.loads(line)["text"])
    count = count+1
    if count == 100:
        break
pp.pprint(y_test)
print()


for text in y_test:
    match_total_array = numpy.zeros(shape=(1, len(y_test)))
    corpus1 = [text] + y_test
    # pp.pprint(corpus1)
    # print()
    syntactic_array, semantic_array = syntactic_match(corpus1, "cosine")
    # print(syntactic_array, len(syntactic_array))
    # print(semantic_array, len(semantic_array))
    match_total_array = numpy.sum([match_total_array, syntactic_array], axis=0)
    match_total_array = numpy.sum([match_total_array, semantic_array], axis=0)
    # print(match_total_array[0])
    match_indexes = numpy.argwhere(match_total_array[0] == numpy.max(match_total_array[0]))
    # match_indexes = numpy.argwhere(match_total_array[0] == numpy.min(match_total_array[0]))
    # print(match_indexes)
    y_pred.append(y_test[match_indexes[0][0]])
print()
# pp.pprint(star_trek_expanded_data)
# pp.pprint(y_pred)
if y_test == y_pred:
    print("careverga")
# print(match_indexes[0][0])



