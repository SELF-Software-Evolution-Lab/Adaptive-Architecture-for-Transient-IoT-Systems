from SPARQLWrapper import SPARQLWrapper, JSON


# sparql_query = SPARQLWrapper("http://localhost:3030/mod_ssn")
# sparql_update = SPARQLWrapper("http://localhost:3030/mod_ssn/update")
sparql_query = SPARQLWrapper("http://172.24.100.100:8000/mod_ssn")
sparql_update = SPARQLWrapper("http://172.24.100.100:8000/mod_ssn/update")
mod_ssn_prefix = "http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#"
systems_prefix = "http://www.w3.org/ns/ssn/systems/"
ssn_prefix = "http://www.w3.org/ns/ssn/"
sosa_prefix = "http://www.w3.org/ns/sosa/"


def app_physical_properties(properties, functional):
    properties["Sensor"] = "<" + sosa_prefix + functional["Model"] + ">"
    properties["System Capability"] = "<" + systems_prefix + "System_capability_"+functional["Model"] + ">"
    sparql_update.setQuery("""
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
        INSERT DATA
        {"""+properties["Sensor"]+""" rdf:type sosa:Sensor.
         """+properties["System Capability"]+""" rdf:type systems:SystemCapability.
         """+properties["Sensor"]+""" systems:hasSystemCapability """+properties["System Capability"]+"""}""")
    sparql_update.setReturnFormat(JSON)
    results = sparql_update.query().convert()
    print("success 1")


def app_service_properties(properties, functional):
    properties["Sensor_service"] = "<" + mod_ssn_prefix + functional["Base URL"] + functional["Relative URL"]+">"
    properties["subscribe"] = "<" + mod_ssn_prefix + "Subscribe_" + functional["App Name"] + ">"
    properties["get_last"] = "<" + mod_ssn_prefix + "Read_last_" + functional["App Name"] + ">"
    properties["obs"] = "<" + sosa_prefix + "observation_" + functional["App Name"] + ">"
    if "Category" in functional.keys():
        properties["variable"] = "sosa:" + functional["Category"] + " rdf:type sosa:ObservableProperty."
        properties["observedProperty"] = properties["obs"] + " sosa:observedProperty " + "sosa:" + functional["Category"] + "."
    else:
        properties["variable"] = ""
        properties["observedProperty"] = ""
    if "Unit" in functional.keys():
        properties["mod_ssn_unit"] = "<" + mod_ssn_prefix + functional["Unit"] + ">"
        properties["unit"] = properties["mod_ssn_unit"] + " rdf:type modssn:Unit."
        properties["obsunit"] = properties["obs"] + " modssn:hasUnit " + properties["mod_ssn_unit"] + "."
    else:
        properties["unit"] = ""
        properties["obsunit"] = ""
    if "Location" in functional.keys():
        if " "in functional["Location"]:
            functional["Location"] = functional["Location"].replace(" ", "_")
        properties["location"] = "<" + mod_ssn_prefix + functional["Location"] + "> rdf:type modssn:Location."
        properties["Sensor_location"] = properties["Sensor_service"] + " modssn:hasLocation <" + mod_ssn_prefix + functional["Location"] + ">."
    else:
        properties["location"] = ""
        properties["Sensor_location"] = ""

    sparql_update.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX sosa: <http://www.w3.org/ns/sosa/>
            PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
            INSERT DATA
            {""" + properties["Sensor_service"] + """ rdf:type modssn:Provider.
             """ + properties["Sensor"] + """ modssn:hasService """ + properties["Sensor_service"] + """.
             """ + properties["Sensor_service"] + """ modssn:hasStringValue " """ + functional["Base URL"] + functional["Relative URL"] + """ ".
             """ + properties["subscribe"] + """ rdf:type modssn:Subscribe.
             """ + properties["get_last"] + """ rdf:type modssn:Read.
             """ + properties["Sensor_service"] + """ modssn:hasMethod """ + properties["subscribe"] + """.
             """ + properties["Sensor_service"] + """ modssn:hasMethod """ + properties["get_last"] + """.
             """ + properties["subscribe"] + """ modssn:hasStringValue " """ + functional["Base URL"] + functional["Relative URL"] + """/""" + functional["DATA"]["rn"] + """ ".
             """ + properties["subscribe"] + """ modssn:hasBodyField modssn:valor.
             """ + properties["get_last"] + """  modssn:hasStringValue " """ + functional["Base URL"] + functional["DATA"]["la"] + """ ".
             """ + properties["get_last"] + """ modssn:hasBodyField modssn:valor.
             """ + properties["obs"] + """ rdf:type sosa:Observation.
             """ + properties["Sensor_service"] + """ sosa:madeObservation """ + properties["obs"] + """.
             """ + properties["variable"] + """
             """ + properties["observedProperty"] + """
             """ + properties["unit"] + """
             """ + properties["obsunit"] + """
             """ + properties["location"] + """
             """ + properties["Sensor_location"] + """
        }""")
    sparql_update.setReturnFormat(JSON)
    results = sparql_update.query().convert()
    print("success 2")


def qos_system_properties(quality_list, properties):
    i = 0
    units = list()
    quality_list_2 = [list(), list()]
    sparql_query.setQuery("""
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
    SELECT ?subclass
    WHERE { ?subclass rdfs:subClassOf* modssn:QosParameter.}""")
    sparql_query.setReturnFormat(JSON)
    results = sparql_query.query().convert()
    modssn_classes = list()
    for result in results["results"]["bindings"]:
        modssn_class = result["subclass"]["value"]
        modssn_classes.append(modssn_class)

    sparql_query.setQuery("""
        PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
        SELECT ?subclass
        WHERE { ?subclass rdfs:subClassOf* systems:SystemProperty.}""")
    sparql_query.setReturnFormat(JSON)
    results = sparql_query.query().convert()
    for result in results["results"]["bindings"]:
        modssn_class = result["subclass"]["value"]
        modssn_classes.append(modssn_class)
    data_properties = list()
    for quality in quality_list:
        for clase in modssn_classes:
            for key, value in quality.items():
                if key in clase:
                    if type(value) is dict:
                        individual_names = [str(value["value"])]
                        units.append("<" + mod_ssn_prefix + str(value["unit"]) + "> rdf:type modssn:Unit.")
                        if type(value["value"]) is str:
                            quality_list_2[i].append("<" + clase + "_" + str(value["value"]) + \
                                                     "> rdf:type " + "<" + clase + ">.")
                            data_properties.append("<" + clase + "_" + str(value["value"]) +
                                                   "> modssn:hasStringValue '" + value["value"]+"'.")
                        if type(value["value"]) is float or type(value["value"]) is int:
                            quality_list_2[i].append("<" + clase + "_" + str(value["value"]) + \
                                                     "> rdf:type " + "<" + clase + ">.")
                            data_properties.append("<" + clase + "_" + str(value["value"]) +
                                                   "> modssn:hasNumericValue " + str(value["value"])+".")
                        if type(value["value"]) is bool:
                            quality_list_2[i].append("<" + clase + "_" + str(value["value"]) + \
                                                     "> rdf:type " + "<" + clase + ">.")
                            data_properties.append("<" + clase + "_" + str(value["value"]) +
                                                   "> modssn:hasBoolean " + str(value["value"])+".")
                        if type(value["value"]) is list:
                            individual_names = [str(value["value"][0]), str(value["value"][-1]) ]
                            quality_list_2[i].append("<" + clase + "_" + str(value["value"][0]) + \
                                                     "> rdf:type " + "<" + clase + ">.")
                            data_properties.append("<" + clase + "_" + str(value["value"][0]) +
                                                   "> modssn:hasNumericValue " + str(value["value"][0])+".")
                            quality_list_2[i].append("<" + clase + "_" + str(value["value"][-1]) + \
                                                     "> rdf:type " + "<" + clase + ">.")
                            data_properties.append("<" + clase + "_" + str(value["value"][-1]) +
                                                   "> modssn:hasNumericValue " + str(value["value"][-1])+".")
                            data_properties.append("<" + clase + "_" + str(value["value"][0]) +
                                                   "> modssn:hasUnit <" + mod_ssn_prefix + str(value["unit"])+">.")
                            data_properties.append("<" + clase + "_" + str(value["value"][1]) +
                                                   "> modssn:hasUnit <" + mod_ssn_prefix + str(value["unit"])+">.")
                        else:
                            data_properties.append("<" + clase + "_" + str(value["value"]) +
                                                   "> modssn:hasUnit <" + mod_ssn_prefix + str(value["unit"])+">.")
                    else:
                        individual_names = [str(value)]
                        quality_list_2[i].append("<" + clase + "_" + str(value) + \
                                                 "> rdf:type " + "<" + clase + ">.")
                        if type(value) is str:
                            data_properties.append("<" + clase + "_" + str(value) +
                                                   "> modssn:hasStringValue '" + value + "'.")
                        if type(value) is float or type(value) is int:
                            data_properties.append("<" + clase + "_" + str(value) +
                                                   "> modssn:hasNumericValue " + str(value)+".")
                        if type(value) is bool:
                            data_properties.append("<" + clase + "_" + str(value) +
                                                   "> modssn:hasBoolean " + str(value)+".")
                    for individual_name in individual_names:
                        if key in ["Accuracy", "ActuationRange", "DetectionLimit", "Drift", "Frequency",
                                   "MeasurementRange", "Precision", "Resolution", "Sensitivity", "Cost", "Latency"]:
                            data_properties.append("<" + clase + "_" + individual_name +
                                                   "> modssn:hasConstraintOperator modssn:lower_than_equal.")
                        elif key in ['Availability', "Capacity", "Throughput", "MTBF"]:
                            data_properties.append("<" + clase + "_" + individual_name +
                                                   "> modssn:hasConstraintOperator modssn:greater_than_equal.")
                        else:
                            data_properties.append("<" + clase + "_" + individual_name +
                                                   "> modssn:hasConstraintOperator modssn:equal.")
        i = i + 1
    has_qos = [(properties["Sensor_service"] + " modssn:hasQoSParameter " + system_property.split("rdf:type", 1)[0] + ".")
               for system_property in quality_list_2[0]]
    if len(quality_list_2) == 2:
        has_system_property = [(properties["System Capability"] + " systems:hasSystemProperty " +
                                system_property.split("rdf:type", 1)[0] + ".")
                               for system_property in quality_list_2[1]]
    else:
        has_system_property = list()
    sep = "\n"
    insert_data = sep.join(quality_list_2[0]+quality_list_2[1]+units+data_properties+has_system_property+has_qos)
    sparql_update.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
            PREFIX systems: <http://www.w3.org/ns/ssn/systems/>
            INSERT DATA
            {""" + insert_data + """}""")
    sparql_update.setReturnFormat(JSON)
    results = sparql_update.query().convert()
    print("success 3")
    print()


def app_instance_load(functional):
    sparql_query.setQuery("""
        PREFIX sosa: <http://www.w3.org/ns/sosa/>
        PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        SELECT ?subject
        WHERE {?subject rdf:type sosa:Sensor}""")
    sparql_query.setReturnFormat(JSON)
    results = sparql_query.query().convert()
    instances = list()
    for result in results["results"]["bindings"]:
        instance = result["subject"]["value"].replace(sosa_prefix, "")
        instances.append(instance)

    properties = dict()
    if functional["Model"] not in instances:
        print(functional["App Name"])
        app_physical_properties(properties, functional)
        app_service_properties(properties, functional)
        if not "System property" in functional:
            functional["System property"] = dict()
        quality_list = [functional["QoS"], functional["System property"]]
        qos_system_properties(quality_list, properties)
    else:
        properties["Sensor"] = "<" + sosa_prefix + functional["Model"] + ">"
        properties["System Capability"] = "<" + systems_prefix + "System_capability_" + functional["Model"] + ">"
        app_service_properties(properties, functional)
        quality_list = [functional["QoS"]]
        qos_system_properties(quality_list, properties)


def om2m_instance_load(om2m):
    sparql_query.setQuery("""
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            PREFIX ssn: <http://www.w3.org/ns/ssn/>
            SELECT ?subject
            WHERE {?subject rdf:type ssn:System}""")
    sparql_query.setReturnFormat(JSON)
    results = sparql_query.query().convert()
    instances = list()
    for result in results["results"]["bindings"]:
        instance = result["subject"]["value"].replace(ssn_prefix, "")
        instances.append(instance)
    if om2m["Name"] not in instances:
        service = "<" + ssn_prefix + om2m["Name"] + ">"
        service_url = "<" + mod_ssn_prefix + om2m["Name"] + "_URL" + ">"
        sparql_update.setQuery("""
                PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
                PREFIX ssn: <http://www.w3.org/ns/ssn/>
                PREFIX modssn: <http://www.semanticweb.org/jairoandresarizacastaneda/ontologies/2018/9/Mod_SSN#>
                INSERT DATA
                {""" + service + """ rdf:type ssn:System.
                 """ + service_url + """ rdf:type modssn:Provider.
                 """ + service + """ modssn:hasService """ + service_url + """.
                 """ + service_url + """ modssn:hasStringValue " """ + om2m["Base URL"] + om2m["Relative URL"] + """ ".
                 }""")
        sparql_update.setReturnFormat(JSON)
        results = sparql_update.query().convert()
        print("success 4")
        print(service_url)

