import numpy
import redis
import ast


# pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
pool = redis.ConnectionPool(host='172.24.100.98', port=8080, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)


def numeric_eval(number1, constraint, number2):
    if constraint == "equal":
        numeric_value = int(number1 == number2)
    elif constraint == "greater_than":
        numeric_value = int(number1 > number2)
    elif constraint == "greater_than_equal":
        numeric_value = int(number1 >= number2)
    elif constraint == "lower_than":
        numeric_value = int(number1 < number2)
    elif constraint == "lower_than_equal":
        numeric_value = int(number1 <= number2)
    return numeric_value


def string_bool_eval(number1, number2):
    string_value = int(number1 == number2)
    return string_value


def unit_eval(unit1, unit2):
    unit_value = int(unit1 == unit2)
    return unit_value


def properties_matching(requirement, system_prop, entry_list, threshold, application):
    match_list = entry_list
    total_weights = ast.literal_eval(redis_server.get(application))
    requirement_properties = list(requirement.keys())
    matching_vector = []
    matching_systems = []
    matching_threshold = threshold*len(requirement_properties)
    print("max value", len(requirement_properties))
    print("threshold", matching_threshold)
    for match in match_list:
        for match_key, previous_match_value in match.items():
            match_value = 0
            if system_prop is "System" and entry_list:
                type_properties = match_key.hasSystemProperty()
                # print(match_key.hasSSystem[0].hasSystemCapability[0])
                weights = total_weights["System property"]
            elif system_prop is not "System" and entry_list:
                type_properties = match_key.hasQoSParameter()
                weights = total_weights["QoS"]
            for requirement_property in requirement_properties:
                for type_property in type_properties:
                    if requirement_property == type_property.type():
                        # if type_property.hasNumericValue():
                        try:
                            offered = type_property.hasNumericValue()
                            operator = type_property.hasConstraintOperator()
                            required = requirement[requirement_property]["value"]
                            offered_unit = type_property.hasUnit()
                            required_unit = requirement[requirement_property]["unit"]
                            unit_evaluation = unit_eval(offered_unit, required_unit)
                            if type(required) is float or type(required) is int:
                                evaluation = numeric_eval(offered, operator, required)
                            elif type(required) is list and (type(required[0]) is int or type(required[0]) is float) \
                                    and (type(required[-1]) is int or type(required[-1]) is float):
                                evaluation = numeric_eval(offered, operator, required[0]) or \
                                             numeric_eval(offered, operator, required[-1])
                            match_value += evaluation*unit_evaluation*weights[requirement_property]
                            if evaluation == 1:
                                break
                        # elif type_property.hasStringValue():
                        except:
                            try:
                                offered = type_property.hasStringValue()
                                required = requirement[requirement_property]
                                evaluation = string_bool_eval(offered, required)
                                match_value += evaluation*weights[requirement_property]
                                break
                            except:
                            # elif type_property.hasBoolean():
                                offered = type_property.hasBoolean()
                                required = requirement[requirement_property]
                                evaluation = string_bool_eval(offered, required)
                                match_value += evaluation*weights[requirement_property]
                                break
            if match_value >= matching_threshold*weights["Weight Average"]:
                if system_prop is "System" and entry_list:
                    matching_systems.append({"app": match_key.url, "score": match_value+previous_match_value,
                                             "state": False})
                elif system_prop is not "System" and entry_list:
                    matching_systems.append({match_key: match_value+previous_match_value})
            matching_vector.append(match_value)
    print("new threshold", matching_threshold * weights["Weight Average"])
    if not matching_systems:
        maximum = numpy.amax(matching_vector)
        indexes = numpy.argwhere(matching_vector == maximum)
        for index in indexes:
            for key, value in match_list[index[0]].items():
                if system_prop is "System" and entry_list:
                    matching_systems.append({"app": key.url, "score": value+maximum, "state": False})
                elif system_prop is not "System" and entry_list:
                    matching_systems.append({key: value + maximum})
        print("max")
    print(matching_vector)
    print(matching_systems)
    return matching_systems

