import nltk
from nltk.corpus import wordnet as wn

synonyms_1 = wn.synsets("auto")
print(synonyms_1)
synonyms_2 = wn.synsets("car")
print(synonyms_2)
print()
if len(synonyms_1) == 0 or len(synonyms_2) == 0:
    print("No results")
    # return None, None
else:
    max_sim = -1
    best_pair = None, None
    for synonym in synonyms_1:
        for synonym_2 in synonyms_2:
            sim = synonym.path_similarity(synonym_2)
            print(1-sim)
            if sim is None:
                continue
            if sim > max_sim:
                max_sim = sim
                best_pair = synonym, synonym_2
    max_sim = 1-max_sim
    print(best_pair)
    print(max_sim)
    # return best_pair
