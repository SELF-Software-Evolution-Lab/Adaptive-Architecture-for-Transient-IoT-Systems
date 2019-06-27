import distance
import string
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_distances
from fuzzywuzzy import fuzz
from owlready2 import *


repository = "/Users/jairoandresarizacastaneda/Desktop/IoT_segundo_semestre/codigo_gateway/ontology/repository"
filename = "hub_iot_qos.owl"
onto_path.append(repository)
onto_hub = get_ontology("file:///"+repository+"/"+filename).load()
instances1 = [individual.name for individual in onto_hub.individuals()]
print(instances1)
print(len(instances1))


corpus = ["Temperature, in room",
          "Temperatura in the room???",
          "room temperature/("]
corpus2 = []
corpus3 = []

for sentence in corpus:
    data = sentence.translate(sentence.maketrans('', '', string.punctuation))
    corpus2.append(data)
    corpus3.append(data.split())
print(corpus2)

vectorizer = CountVectorizer()
features = vectorizer.fit_transform(corpus2).todense()

for feature in features:
    print("coseno ", cosine_distances(features[0], feature))
for feature in features:
    print("euclidiana ", euclidean_distances(features[0], feature))

print()
for sentence in corpus2:
    print("levenshtein ", distance.levenshtein(corpus2[0], sentence))
for sentence in corpus2:
    print("jaccard ", distance.jaccard(corpus2[0], sentence))
for sentence in corpus2:
    print("fuzzy ", fuzz.QRatio(corpus2[0], sentence))



# from owlready2 import *

# repository = "/Users/jairoandresarizacastaneda/Desktop/IoT segundo semestre/codigo gateway/ontology/repository"
# filename = "hub_iot_qos.owl"
# onto_path.append(repository)
# onto_hub = get_ontology("file:///"+repository+"/"+filename).load()

# for individual in onto_hub.individuals():
#     # print(individual)
#     # if individual.aboutProperty:
#     #     print("prop", individual.aboutProperty)
#     if isinstance(individual, onto_hub.Service):
#         if individual.hasObservation:
#             services.append(individual)
#             corpus.append(individual.hasObservation[0].aboutProperty[0].name)
#             observation = individual.hasObservation[0].aboutProperty[0].name
