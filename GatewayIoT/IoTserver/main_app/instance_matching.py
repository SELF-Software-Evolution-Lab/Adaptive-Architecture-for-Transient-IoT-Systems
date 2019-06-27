import string
import redis
import ast
import numpy
import requests
import json
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_distances
from sklearn.metrics.pairwise import euclidean_distances
from nltk.corpus import wordnet as wn


def syntactic_match(corpus_list_p):
    synonyms = wn.synsets(corpus_list_p[0])
    semantic_array_p = numpy.array([])
    syntactic_array_p = numpy.array([])

    vectorizer = CountVectorizer()
    features = vectorizer.fit_transform(corpus_list_p).todense()
    for i in range(1, len(features)):
        distance = euclidean_distances(features[0], features[i])
        syntactic_array_p = numpy.append(syntactic_array_p, distance)
        semantic_sim = semantic_matching(synonyms, corpus_list_p[i])
        semantic_array_p = numpy.append(semantic_array_p, semantic_sim)
    return syntactic_array_p, semantic_array_p


def semantic_matching(synonyms_1, word2):
    synonyms_2 = wn.synsets(word2)
    if len(synonyms_1) == 0 or len(synonyms_2) == 0:
        max_sim = 1
        return max_sim
    else:
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


def subscribe(match_app, requirement1):
    header = {"X-M2M-Origin": "admin:admin", "Accept": "application/json", 'content-type': 'application/json;ty=23'}
    url = match_app["Base URL"] + match_app["Relative URL"]+"/"+match_app["DATA"]["rn"]
    data = {
        "m2m:sub": {
            "xmlns:m2m": "http://www.onem2m.org/xml/protocols",
            "nu": requirement1["URL"],
            "nct": "2"
        }
    }
    try:
        subscription = requests.post(url, data=json.dumps(data), headers=header)
    except:
        pass


def instance_matching(requirement):
    pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
    redis_server = redis.Redis(connection_pool=pool)
    match_list = []
    corpus = {}
    match_list.append(requirement)
    execution_guidepost_services = redis_server.get("execution_guidepost_services")
    if execution_guidepost_services is None:
        execution_guidepost_services = {}
    else:
        execution_guidepost_services = ast.literal_eval(execution_guidepost_services)
    print(execution_guidepost_services)

    for key in requirement.keys():
        if key in ["Location", "Category", "Unit"]:
            corpus[key] = [requirement[key]]

    for app in redis_server.smembers("apps_list"):
        try:
            application = ast.literal_eval(redis_server.get(app))
            for key in corpus.keys():
                try:
                    sentence = application[key]
                    corpus[key].append(sentence.translate(sentence.maketrans('', '', string.punctuation)))
                except:
                    continue
            match_list.append(application)
        except:
            continue

    for app in match_list:
        print("app", app)
    print()
    print("corpus dict", corpus)
    match_total_array = numpy.zeros(shape=(1, len(match_list)-1))

    for key in corpus.keys():
        corpus_list = corpus[key]
        print()
        print("corpus", corpus_list)
        syntactic_array, semantic_array = syntactic_match(corpus_list)
        print("syntactic", syntactic_array)
        print("semantic", semantic_array)
        match_total_array = numpy.sum([match_total_array, syntactic_array], axis=0)
        match_total_array = numpy.sum([match_total_array, semantic_array], axis=0)

    print()
    print("total", match_total_array[0])
    match_indexes = numpy.argwhere(match_total_array[0] == numpy.min(match_total_array[0]))
    print(match_indexes)
    for index in match_indexes:
        print(match_list[index[0]+1])
        subscribe(match_list[index[0]+1], requirement)
        founded_app = match_list[index[0]+1]["Base URL"] + match_list[index[0]+1]["Relative URL"]
        if requirement["URL"] not in execution_guidepost_services:
            execution_guidepost_services[requirement["URL"]] = [founded_app]
        else:
            execution_guidepost_services[requirement["URL"]].append(founded_app)
        redis_server.set("execution_guidepost_services", str(execution_guidepost_services))
        print(execution_guidepost_services)


data = {"Name": "weather", "Location": "home", "Category": "temp", "Unit": "Celsius",
        "URL": "http://192.168.0.6:1400/monitor"}
instance_matching(data)
