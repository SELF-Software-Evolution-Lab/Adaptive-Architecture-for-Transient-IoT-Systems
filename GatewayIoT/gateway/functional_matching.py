import numpy
import requests
import json
import time
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import euclidean_distances
from sklearn.metrics.pairwise import cosine_distances
from gateway import ontology_as_classes

# based on instance matching in the IoT server website
# calling the ontology and specifying variables
# euclidean distance the lower the value, the similarity is higher. 0 the values are equal. there is no maximum
# cosine distance lower value, higher similarity. 0 the values are equal. 1 is the maximum.
# synset similarity ranges from 0 to 1. 1 is equal 0 is opposite
enable_semantic = False
if enable_semantic: from nltk.corpus import wordnet as wn


def syntactic_match(corpus_list_p, method_selection):
    # creating syntactic array results and extracting features from corpus
    syntactic_array_p = numpy.array([])
    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus_list_p).todense()
    # creating semantic array results
    if enable_semantic: semantic_array_p = numpy.array([])
    syntactic_time = 0
    semantic_time = 0
    for i in range(1, len(features)):
        if method_selection is "cosine":
            # Calculating cosine distance between the features requirement and each app. Adding the result to the array
            start_syntactic = time.perf_counter()
            distance = cosine_distances(features[0], features[i])
            syntactic_array_p = numpy.append(syntactic_array_p, 1-distance)
            stop_syntactic = time.perf_counter()
            # calculating semantic similarity of the synonyms of the requirement and the description if each app
            if enable_semantic:
                semantic_sim = semantic_matching(corpus_list_p[0], corpus_list_p[i])
                semantic_array_p = numpy.append(semantic_array_p, 1-semantic_sim)
            stop_semantic = time.perf_counter()
            syntactic_time += (stop_syntactic - start_syntactic)
            semantic_time += (stop_semantic - stop_syntactic)
        else:
            # idem but using euclidean distance
            distance = euclidean_distances(features[0], features[i])
            syntactic_array_p = numpy.append(syntactic_array_p, distance)
            if enable_semantic:
                semantic_sim = semantic_matching(corpus_list_p[0], corpus_list_p[i])
                semantic_array_p = numpy.append(semantic_array_p, semantic_sim)
    if enable_semantic:
        return syntactic_array_p, semantic_array_p, syntactic_time, semantic_time
    else:
        return syntactic_array_p, syntactic_time, semantic_time


def semantic_matching(word1, word2):
    # getting synonyms set from the first word of the corpus (requirement)
    synonyms_1 = wn.synsets(word1)
    # getting synonyms set from the app
    synonyms_2 = wn.synsets(word2)
    # if there are no synonyms for the word, words are opposite
    if len(synonyms_1) == 0 or len(synonyms_2) == 0:
        max_sim = 1
        return max_sim
    else:
        # it compares all the synsets and find the highest similarity
        max_sim = -1
        best_pair = None, None
        for synonym in synonyms_1:
            for synonym_2 in synonyms_2:
                sim = synonym.path_similarity(synonym_2)
                if sim is None:
                    continue
                if sim > max_sim:
                    max_sim = sim
                    best_pair = synonym, synonym_2
        max_sim = 1 - max_sim
        return max_sim


def subscribe(match_app, previus_match, requirement1):
    # specifying data for post to subscribe serveces and apps
    header = {"X-M2M-Origin": "admin:admin", "Accept": "application/json", 'content-type': 'application/json;ty=23'}
    url = match_app[0]["app"]+"/DATA"
    data = {
        "m2m:sub": {
            "xmlns:m2m": "http://www.onem2m.org/xml/protocols",
            "nu": requirement1,
            "nct": "2"
        }
    }
    # deleting previous subscriptions if exists
    for match in previus_match:
        if "subscription" in match:
            requests.delete(match["subscription"], headers=header)
            print("borrando subs", match["subscription"])
    # performing subscription with the best match, which is position 0 of the list because is ordered
    subscription = requests.post(url, data=json.dumps(data), headers=header)
    subs_url = url+"/"+json.loads(subscription.content)["m2m:sub"]["rn"]
    match_app[0]["subscription"] = subs_url
    return match_app


def instance_matching(requirement, method_selection, new_app, services):
    # creating dictionary for corpus and a list of comparing service and apps
    start_matching_time = time.perf_counter()
    match_list = []
    corpus = {}
    match_list.append(requirement)
    # creating a corpus for each location, category and unit functional properties, the first entry on the lists are
    # are requirements values
    for key in requirement.keys():
        if key in ["Location", "Category", "Unit"]:
            corpus[key] = [requirement[key]]
    # getting list with all the available services
    # services = ontology_as_classes.get_providers(new_app) if new_app else ontology_as_classes.get_providers()
    services = ontology_as_classes.get_providers(new_app) if new_app else services
    # adding the value of the location, category and unit properties of the app to the corpus
    for service in services:
        app = dict()
        try:
            if not service.hasLocation() and not service.madeObservation():
                continue
            app["Location"] = service.hasLocation() if service.hasLocation() else ""
            if service.madeObservation():
                app["Category"] = service.madeObservation().observedProperty() if service.madeObservation().observedProperty() else ""
                app["Unit"] = service.madeObservation().hasUnit() if service.madeObservation().hasUnit() else ""
            app["Base URL"] = service.url
            app["Ontology"] = service
            for key in corpus.keys():
                try:
                    corpus[key].append(app[key])
                except Exception as e:
                    print(str(e))
                    continue
            match_list.append(app)
        except Exception as e:
            print(str(e))
            continue
    # defining threshold for the matching algorithm
    threshold = len(corpus.keys()) * 2 * requirement["threshold"] if enable_semantic is True else len(corpus.keys()) * requirement["threshold"]
    print("threshold", threshold)
    print("max value", len(corpus.keys())*2) if enable_semantic is True else print("max value", len(corpus.keys()))
    # creating an array to store matching results
    match_total_array = numpy.zeros(shape=(1, len(match_list)-1))

    # getting the corpus for each property(location, category and unit) and calculating systanctic and
    # semantic similarity
    stop_corpus_time = time.perf_counter()
    semantic_time1 = 0
    syntactic_time1 = 0
    for key in corpus.keys():
        corpus_list = corpus[key]
        print()
        # print("corpus list", corpus_list)
        if enable_semantic:
            syntactic_array, semantic_array, syntactic_time, semantic_time = syntactic_match(corpus_list, method_selection)
        else:
            syntactic_array, syntactic_time, semantic_time = syntactic_match(corpus_list, method_selection)
        # print("syntactic", syntactic_array)
        if enable_semantic: print("semantic", semantic_array)
        # adding syntactic and semantic similarity results to the total array
        match_total_array = numpy.sum([match_total_array, syntactic_array], axis=0)
        if enable_semantic: match_total_array = numpy.sum([match_total_array, semantic_array], axis=0)
        semantic_time1 += semantic_time
        syntactic_time1 += syntactic_time
    stop_syntactic_semantic_time = time.perf_counter()
    # print()
    # print("total", match_total_array[0])
    # calculating the indexes of the values higher than the defined threshold if cosine similarity is used
    if method_selection is "cosine":
        match_indexes = numpy.argwhere(match_total_array[0] > threshold)
        print(match_indexes.size)
    else:
        # this is not implemented for euclidean distance
        match_indexes = numpy.argwhere(match_total_array[0] == numpy.min(match_total_array[0]))
    # print("match indexes", match_indexes)
    # making the list of matching apps
    founded_ontologies = []
    for index in match_indexes:
        # print("match", match_list[index[0]+1])
        try:
            if new_app is None:
                founded_ontologies.append({match_list[index[0]+1]["Ontology"]: match_total_array[0][index[0]]})
            else:
                founded_ontologies.append({match_list[index[0]+1]["Ontology"]: match_total_array[index[0]]})
        except Exception as e:
            print(str(e))
            continue
    stop_matching_time = time.perf_counter()
    corpus_time = stop_corpus_time - start_matching_time
    ordering_time = stop_matching_time - stop_syntactic_semantic_time
    return founded_ontologies, corpus_time, semantic_time1, syntactic_time1, ordering_time


