import re
from SPARQLWrapper import SPARQLWrapper, JSON
from pprint import pprint


# sparql = SPARQLWrapper("http://localhost:3030/mod_ssn/")
sparql = SPARQLWrapper("http://172.24.100.100:8000/mod_ssn")
modssn_prefix = "http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#"
sosa_prefix = "http://www.w3.org/ns/sosa/"
rdf_prefix = "http://www.w3.org/1999/02/22-rdf-syntax-ns#"
system_prefix = "http://www.w3.org/ns/ssn/systems/"
qos_properties = ('Availability', 'Capacity', 'Cost', 'Interoperability', 'Throughput', 'Consistency',
                  'Messaging', 'MTBF', 'Disaster', 'Failover', 'Reputation', 'Robustness', 'Scalability',
                  'Auditability', 'Authentication', 'Data_encryption', 'Message_encryption', 'Non_repudiation',
                  'Method_stability', 'Interface_stability')
system_properties = ('Accuracy', 'ActuationRange', 'DetectionLimit', 'Drift', 'Frequency', 'Latency',
                     'MeasurementRange', 'Precision', 'Resolution', 'ResponseTime', 'Selectivity', 'Sensitivity')


def get_providers_functional(one=None):
    if type(one) is str:
        one = "VALUES ?provider{<" + modssn_prefix + one + ">}"
    elif type(one) is list:
        text = ""
        for data in one:
            text = text + "<" + modssn_prefix + data + "> "
        one = "VALUES ?provider{" + text + "}"
    else:
        one = ""
    sparql.setQuery(""" 
                PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX sosa: <http://www.w3.org/ns/sosa/>
                PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
                SELECT ?provider ?location ?observation ?category ?unit  
                 (group_concat(DISTINCT ?sys2) as ?SYS) 
                WHERE { """ + one + """
                ?provider rdf:type modssn:Provider. 
                ?provider sosa:madeObservation ?observation. 
                ?provider modssn:hasLocation ?location.
                ?observation sosa:observedProperty ?category.
                ?observation modssn:hasUnit ?unit.}   
                group by ?provider ?location ?observation ?category ?unit  
            """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    query_result = results["results"]["bindings"]
    # pprint(query_result)
    providers = list()
    for provider in query_result:
        for key in provider.keys():
            provider[key]["value"] = re.sub(modssn_prefix + "|" + sosa_prefix + "|" + rdf_prefix + "|" + system_prefix, "", provider[key]["value"])
        observation1 = Observation(provider["observation"]["value"], provider["category"]["value"], provider["unit"]["value"])
        app = Provider(provider["provider"]["value"], observation1, provider["location"]["value"])
        providers.append(app)
    # print()
    pprint(providers)
    # print()
    # for pro in providers:
    #     pprint(pro.__dict__)
    return providers


def get_providers_qos(one=None):
    if type(one) is str:
        one = "VALUES ?provider{<" + modssn_prefix + one + ">}"
    elif type(one) is list:
        text = ""
        for data in one:
            text = text + "<" + modssn_prefix + data + "> "
        one = "VALUES ?provider{" + text + "}"
    else:
        one = ""
    sparql.setQuery(""" 
                PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX sosa: <http://www.w3.org/ns/sosa/>
                PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
                SELECT ?provider ?location ?observation ?category ?unit 
                (group_concat(DISTINCT ?qos_prop) as ?QOS)  
                WHERE { """ + one + """
                ?provider rdf:type modssn:Provider. 
                ?provider sosa:madeObservation ?observation. 
                ?provider modssn:hasLocation ?location.
                ?provider modssn:hasQoSParameter ?qos.
                ?qos ?predicate ?object.
                
                ?system modssn:hasService ?provider.
                ?system systems:hasSystemCapability ?sys_cap.
                ?sys_cap systems:hasSystemProperty ?sys_prop.
                ?sys_prop ?pred ?obj.
                
                ?observation sosa:observedProperty ?category.
                ?observation modssn:hasUnit ?unit.
                BIND(CONCAT(str(?qos)," ",str(?predicate)," ",str(?object),";") AS ?qos_prop).
                BIND(CONCAT(str(?sys_prop)," ",str(?pred)," ",str(?obj),";") AS ?sys2)}   
                group by ?provider ?location ?observation ?category ?unit ?system ?sys_cap 
            """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    query_result = results["results"]["bindings"]
    # pprint(query_result)
    providers = list()
    for provider in query_result:
        for key in provider.keys():
            provider[key]["value"] = re.sub(modssn_prefix + "|" + sosa_prefix + "|" + rdf_prefix + "|" + system_prefix, "", provider[key]["value"])
        observation1 = Observation(provider["observation"]["value"], provider["category"]["value"], provider["unit"]["value"])
        app = Provider(provider["provider"]["value"], observation1, provider["location"]["value"])
        qos_triplet = provider["QOS"]["value"].split(";")
        qos_dict = {key: Qos() for key in qos_properties}
        for triplet in qos_triplet:
            triplet = triplet.split()
            if triplet:
                for qos_property in qos_properties:
                    if triplet[0].startswith(qos_property):
                        if triplet[1] == "type":
                            qos_dict[qos_property].set_qos(triplet[0])
                            qos_dict[qos_property].set_type(triplet[2])
                        if triplet[1] == "hasConstraintOperator":
                            qos_dict[qos_property].set_hasConstraintOperator(triplet[2])
                        if triplet[1] == "hasUnit":
                            qos_dict[qos_property].set_hasUnit(triplet[2])
                        if triplet[1] == "hasStringValue":
                            qos_dict[qos_property] = QosString(qos_dict[qos_property].qos, qos_dict[qos_property].qos_type, qos_dict[qos_property].value,
                                                               qos_dict[qos_property].constraint_operator, qos_dict[qos_property].unit)
                            qos_dict[qos_property].set_hasStringValue(triplet[2])
                        if triplet[1] == "hasNumericValue":
                            qos_dict[qos_property] = QosNumeric(qos_dict[qos_property].qos, qos_dict[qos_property].qos_type, qos_dict[qos_property].value,
                                                               qos_dict[qos_property].constraint_operator, qos_dict[qos_property].unit)
                            qos_dict[qos_property].set_hasNumericValue(float(triplet[2]))
                        if triplet[1] == "hasBoolean":
                            qos_dict[qos_property] = QosBoolean(qos_dict[qos_property].qos, qos_dict[qos_property].qos_type, qos_dict[qos_property].value,
                                                               qos_dict[qos_property].constraint_operator, qos_dict[qos_property].unit)
                            qos_dict[qos_property].set_hasBoolean(bool(triplet[2]))
        app.set_hasQoSParameter(list(qos_dict.values()))

        sys_triplet = provider["SYS"]["value"].split(";")
        sys_dict = {key: Qos() for key in system_properties}
        for triplet in sys_triplet:
            triplet = triplet.split()
            if triplet:
                for system_property in system_properties:
                    if triplet[0].startswith(system_property):
                        if triplet[1] == "type":
                            sys_dict[system_property].set_qos(triplet[0])
                            sys_dict[system_property].set_type(triplet[2])
                        if triplet[1] == "hasConstraintOperator":
                            sys_dict[system_property].set_hasConstraintOperator(triplet[2])
                        if triplet[1] == "hasUnit":
                            sys_dict[system_property].set_hasUnit(triplet[2])
                        if triplet[1] == "hasStringValue":
                            sys_dict[system_property] = QosString(sys_dict[system_property].qos,
                                                               sys_dict[system_property].qos_type,
                                                               sys_dict[system_property].value,
                                                               sys_dict[system_property].constraint_operator,
                                                               sys_dict[system_property].unit)
                            sys_dict[system_property].set_hasStringValue(triplet[2])
                        if triplet[1] == "hasNumericValue":
                            sys_dict[system_property] = QosNumeric(sys_dict[system_property].qos,
                                                                sys_dict[system_property].qos_type,
                                                                sys_dict[system_property].value,
                                                                sys_dict[system_property].constraint_operator,
                                                                sys_dict[system_property].unit)
                            sys_dict[system_property].set_hasNumericValue(float(triplet[2]))
                        if triplet[1] == "hasBoolean":
                            sys_dict[system_property] = QosBoolean(sys_dict[system_property].qos,
                                                                sys_dict[system_property].qos_type,
                                                                sys_dict[system_property].value,
                                                                sys_dict[system_property].constraint_operator,
                                                                sys_dict[system_property].unit)
                            sys_dict[system_property].set_hasBoolean(bool(triplet[2]))
        app.set_hasSystemProperty(list(sys_dict.values()))
        providers.append(app)
        # for key, value in qos_dict.items():
        #     print(value.__dict__)
        # print()
        # for key, value in sys_dict.items():
        #     print(value.__dict__)
        # print()
    # print()
    pprint(providers)
    # print()
    # for pro in providers:
    #     pprint(pro.__dict__)
    return providers


def get_providers(one=None):
    if type(one) is str:
        one = "VALUES ?provider{<" + modssn_prefix + one + ">}"
    elif type(one) is list:
        text = ""
        for data in one:
            text = text + "<" + modssn_prefix + data + "> "
        one = "VALUES ?provider{" + text + "}"
    else:
        one = ""
    sparql.setQuery(""" 
                PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX sosa: <http://www.w3.org/ns/sosa/>
                PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
                SELECT ?provider ?location ?observation ?category ?unit ?system ?sys_cap 
                (group_concat(DISTINCT ?qos_prop) as ?QOS) (group_concat(DISTINCT ?sys2) as ?SYS) 
                WHERE { """ + one + """
                ?provider rdf:type modssn:Provider. 
                ?provider sosa:madeObservation ?observation. 
                ?provider modssn:hasLocation ?location.
                ?provider modssn:hasQoSParameter ?qos.
                ?qos ?predicate ?object.
                ?system modssn:hasService ?provider.
                ?system systems:hasSystemCapability ?sys_cap.
                ?sys_cap systems:hasSystemProperty ?sys_prop.
                ?sys_prop ?pred ?obj.
                ?observation sosa:observedProperty ?category.
                ?observation modssn:hasUnit ?unit.
                BIND(CONCAT(str(?qos)," ",str(?predicate)," ",str(?object),";") AS ?qos_prop).
                BIND(CONCAT(str(?sys_prop)," ",str(?pred)," ",str(?obj),";") AS ?sys2)}   
                group by ?provider ?location ?observation ?category ?unit ?system ?sys_cap 
            """)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    query_result = results["results"]["bindings"]
    # pprint(query_result)
    providers = list()
    for provider in query_result:
        for key in provider.keys():
            provider[key]["value"] = re.sub(modssn_prefix + "|" + sosa_prefix + "|" + rdf_prefix + "|" + system_prefix, "", provider[key]["value"])
        observation1 = Observation(provider["observation"]["value"], provider["category"]["value"], provider["unit"]["value"])
        app = Provider(provider["provider"]["value"], observation1, provider["location"]["value"])
        qos_triplet = provider["QOS"]["value"].split(";")
        qos_dict = {key: Qos() for key in qos_properties}
        for triplet in qos_triplet:
            triplet = triplet.split()
            if triplet:
                for qos_property in qos_properties:
                    if triplet[0].startswith(qos_property):
                        if triplet[1] == "type":
                            qos_dict[qos_property].set_qos(triplet[0])
                            qos_dict[qos_property].set_type(triplet[2])
                        if triplet[1] == "hasConstraintOperator":
                            qos_dict[qos_property].set_hasConstraintOperator(triplet[2])
                        if triplet[1] == "hasUnit":
                            qos_dict[qos_property].set_hasUnit(triplet[2])
                        if triplet[1] == "hasStringValue":
                            qos_dict[qos_property] = QosString(qos_dict[qos_property].qos, qos_dict[qos_property].qos_type, qos_dict[qos_property].value,
                                                               qos_dict[qos_property].constraint_operator, qos_dict[qos_property].unit)
                            qos_dict[qos_property].set_hasStringValue(triplet[2])
                        if triplet[1] == "hasNumericValue":
                            qos_dict[qos_property] = QosNumeric(qos_dict[qos_property].qos, qos_dict[qos_property].qos_type, qos_dict[qos_property].value,
                                                               qos_dict[qos_property].constraint_operator, qos_dict[qos_property].unit)
                            qos_dict[qos_property].set_hasNumericValue(float(triplet[2]))
                        if triplet[1] == "hasBoolean":
                            qos_dict[qos_property] = QosBoolean(qos_dict[qos_property].qos, qos_dict[qos_property].qos_type, qos_dict[qos_property].value,
                                                               qos_dict[qos_property].constraint_operator, qos_dict[qos_property].unit)
                            qos_dict[qos_property].set_hasBoolean(bool(triplet[2]))
        app.set_hasQoSParameter(list(qos_dict.values()))

        sys_triplet = provider["SYS"]["value"].split(";")
        sys_dict = {key: Qos() for key in system_properties}
        for triplet in sys_triplet:
            triplet = triplet.split()
            if triplet:
                for system_property in system_properties:
                    if triplet[0].startswith(system_property):
                        if triplet[1] == "type":
                            sys_dict[system_property].set_qos(triplet[0])
                            sys_dict[system_property].set_type(triplet[2])
                        if triplet[1] == "hasConstraintOperator":
                            sys_dict[system_property].set_hasConstraintOperator(triplet[2])
                        if triplet[1] == "hasUnit":
                            sys_dict[system_property].set_hasUnit(triplet[2])
                        if triplet[1] == "hasStringValue":
                            sys_dict[system_property] = QosString(sys_dict[system_property].qos,
                                                               sys_dict[system_property].qos_type,
                                                               sys_dict[system_property].value,
                                                               sys_dict[system_property].constraint_operator,
                                                               sys_dict[system_property].unit)
                            sys_dict[system_property].set_hasStringValue(triplet[2])
                        if triplet[1] == "hasNumericValue":
                            sys_dict[system_property] = QosNumeric(sys_dict[system_property].qos,
                                                                sys_dict[system_property].qos_type,
                                                                sys_dict[system_property].value,
                                                                sys_dict[system_property].constraint_operator,
                                                                sys_dict[system_property].unit)
                            sys_dict[system_property].set_hasNumericValue(float(triplet[2]))
                        if triplet[1] == "hasBoolean":
                            sys_dict[system_property] = QosBoolean(sys_dict[system_property].qos,
                                                                sys_dict[system_property].qos_type,
                                                                sys_dict[system_property].value,
                                                                sys_dict[system_property].constraint_operator,
                                                                sys_dict[system_property].unit)
                            sys_dict[system_property].set_hasBoolean(bool(triplet[2]))
        app.set_hasSystemProperty(list(sys_dict.values()))
        providers.append(app)
        # for key, value in qos_dict.items():
        #     print(value.__dict__)
        # print()
        # for key, value in sys_dict.items():
        #     print(value.__dict__)
        # print()
    # print()
    # pprint(providers)
    # print()
    # for pro in providers:
    #     pprint(pro.__dict__)
    return providers


class Provider:
    def __init__(self, url, observation, location, qos=None, sys_prop=None):
        self.url = url
        self.observation = observation
        self.location = location
        self.qos = qos
        self.sys_prop = sys_prop

    def set_hasLocation(self, location):
        self.location = location

    def hasLocation(self):
        return self.location

    def set_madeObservation(self, observation):
        self.observation = observation

    def madeObservation(self):
        return self.observation

    def set_hasQoSParameter(self, qos):
        self.qos = qos

    def hasQoSParameter(self):
        return self.qos

    def set_hasSystemProperty(self, sys_prop):
        self.sys_prop = sys_prop

    def hasSystemProperty(self):
        return self.sys_prop

    def __repr__(self):
        return self.url


class Observation:
    def __init__(self, observation, category, unit):
        self.observation = observation
        self.category = category
        self.unit = unit

    def set_observedProperty(self, category):
        self.observation = category

    def observedProperty(self):
        return self.category

    def set_hasUnit(self, unit):
        self.observation = unit

    def hasUnit(self):
        return self.unit

    def __repr__(self):
        return self.observation


class Qos:
    def __init__(self, qos=None, qos_type=None, value=None, constraint_operator=None, unit=None):
        self.qos = qos
        self.qos_type = qos_type
        self.value = value
        self.constraint_operator = constraint_operator
        self.unit = unit

    def set_qos(self, qos):
        self.qos = qos

    def set_type(self, qos_type):
        self.qos_type = qos_type

    def type(self):
        return self.qos_type

    def set_hasConstraintOperator(self, constraint_operator):
        self.constraint_operator = constraint_operator

    def hasConstraintOperator(self):
        return self.constraint_operator

    def set_hasUnit(self, unit):
        self.unit = unit

    def hasUnit(self):
        return self.unit

    def __repr__(self):
        return self.qos


class QosString(Qos):
    def __init__(self, qos=None, qos_type=None, value=None, constraint_operator=None, unit=None):
        Qos.__init__(self, qos, qos_type, value, constraint_operator, unit)

    def set_hasStringValue(self, value):
        self.value = value

    def hasStringValue(self):
        return self.value


class QosNumeric(Qos):
    def __init__(self, qos=None, qos_type=None, value=None, constraint_operator=None, unit=None):
        Qos.__init__(self, qos, qos_type, value, constraint_operator, unit)

    def set_hasNumericValue(self, value):
        self.value = value

    def hasNumericValue(self):
        return self.value


class QosBoolean(Qos):
    def __init__(self, qos=None, qos_type=None, value=None, constraint_operator=None, unit=None):
        Qos.__init__(self, qos, qos_type, value, constraint_operator, unit)

    def set_hasBoolean(self, value):
        self.value = value

    def hasBoolean(self):
        return self.value


# url = ["http://172.24.100.94:8080/~/in-cse/in-name/Sensor_sd100", "http://172.24.100.94:8080/~/in-cse/in-name/Sensor_sd200"]
# url = "http://172.24.100.94:8080/~/in-cse/in-name/Sensor_sd100"
res = get_providers_qos()
# print(res[0].url)


