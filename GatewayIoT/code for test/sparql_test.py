from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint

# sparql = SPARQLWrapper("http://localhost:3030/mod_ssn")
# sparql.setQuery("""
#     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#     PREFIX owl: <http://www.w3.org/2002/07/owl#>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#     PREFIX sosa: <http://www.w3.org/ns/sosa/>
#     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#     PREFIX ssn: <http://www.w3.org/ns/ssn/>
#     PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
#     PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
#
#     SELECT ?subject ?object
#     WHERE { ?subject rdf:type sosa:Sensor }
# """)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
# pprint(results)
# for result in results["results"]["bindings"]:
#     print(result["subject"]["value"])

# sparql = SPARQLWrapper("http://localhost:3030/mod_ssn/update")
# sparql.setQuery("""
#     PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
#     PREFIX owl: <http://www.w3.org/2002/07/owl#>
#     PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
#     PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>
#     PREFIX sosa: <http://www.w3.org/ns/sosa/>
#     PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
#     PREFIX foaf: <http://xmlns.com/foaf/0.1/>
#     PREFIX ssn: <http://www.w3.org/ns/ssn/>
#     PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
#     PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
#
#     INSERT DATA
#     {sosa:sensor_FWKO rdf:type sosa:Sensor.
# }
#
#
# """)
# sparql.setReturnFormat(JSON)
# results = sparql.query().convert()
#
# pprint(results)


sparql = SPARQLWrapper("http://localhost:3030/mod_ssn/")
sparql.setQuery("""
    SELECT (COUNT(*) as ?Triples) 
    WHERE { ?s ?p ?o }
""")
sparql.setReturnFormat(JSON)
results = sparql.query().convert()
for result in results["results"]["bindings"]:
    triplets_number = result["Triples"]["value"]
print(triplets_number)
pprint(results)