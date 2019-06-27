from owlready2 import *

# repository = "/Users/jairoandresarizacastaneda/Desktop/IoT_segundo_semestre/codigo_gateway/ontology/repository"
# filename = "mod_SSN_fuseki.owl"
# onto_path.append(repository)
# onto_path.append("http://localhost:3030/myowl")
# memory_alpha = get_ontology("file:///"+repository+"/"+filename).load()
modified_SSN = get_ontology("http://localhost:3030/mod_ssn").load()
parsing = list()
reasoning = list()
saving = list()


for space in modified_SSN._namespaces:
    print(space)
    if space.endswith("sosa/"):
        sosa = modified_SSN.get_namespace(space)
    elif space.endswith("ssn/"):
        ssn = modified_SSN.get_namespace(space)
    elif space.endswith("systems/"):
        systems = modified_SSN.get_namespace(space)
    elif space.endswith("skos/core#"):
        skos = modified_SSN.get_namespace(space)


instances1 = [individual.name for individual in modified_SSN.individuals()]
instances2 = [individual.name for individual in modified_SSN.search(is_a=sosa.Sensor)]
print(instances1)
print(len(instances1))
print(instances2)
print(len(instances2))



# sensor = sosa.Sensor("RG-2300")
# print(sensor)
# modified_SSN.save()


file = open("testfile.txt", "a")

file.write("This is a test\n")
file.write("To add more lines.\n")

file.close()