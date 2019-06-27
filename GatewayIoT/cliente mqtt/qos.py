import ast
from owlready2 import *

QoS = {'Security': {'Authentication': True, 'Auditability': True, 'Encryption': False}, 'Economy': '$1',
       'Availability': 0.9, 'Reliability': 3, 'Stability': 'medium'}
# QoS = ast.literal_eval(QoS)

print(QoS)
print(type(QoS))


repository = "/Users/jairoandresarizacastaneda/Desktop/IoT_segundo_semestre/codigo_gateway/ontology/repository"
filename = "iot_qos.owl"
onto_path.append(repository)
onto_hub = get_ontology("file:///"+repository+"/"+filename).load()
instance = dict()
if True:
    #Availability
    service = onto_hub.Service("Temp_casa")
    availability = onto_hub.QosParameter("Availability")
    weight = onto_hub.QosWeight()
    MTTF = onto_hub.Metric("MTTF")
    MTTR = onto_hub.Metric("MTTR")
    metric_type = onto_hub.Numeric()
    value_MTTF = onto_hub.Value()
    value_MTTR = onto_hub.Value()
    high = onto_hub.High()
    av_aggregate = onto_hub.Aggregated()
    unit = onto_hub.Unit("hr")

    service.hasQoS = [availability]
    availability.hasTendency = [high]
    availability.hasMetric = [MTTF, MTTR]
    availability.hasWeight = [weight]
    availability.hasAggregated = [av_aggregate]
    weight.hasNumericValue = [0.5]
    MTTF.hasValue = [value_MTTF]
    MTTR.hasValue = [value_MTTR]
    MTTF.hasMetricType = [metric_type]
    MTTR.hasMetricType = [metric_type]
    value_MTTF.hasNumericValue = [8759]
    value_MTTR.hasNumericValue = [1]
    av_aggregate.hasStringValue = ["MTTF/(MTTF+MTTR)"]
    MTTF.hasUnit = [unit]
    MTTR.hasUnit = [unit]
    #Availability

if True:
    #Stability
    service1 = onto_hub.Service("Temp_cocina")
    Stability = onto_hub.QosParameter("Stability")
    weight1 = onto_hub.QosWeight()
    service_interface_Stability = onto_hub.Metric("service_interface_Stability")
    method_signature_Stability = onto_hub.Metric("method_signature_Stability")
    metric_type1 = onto_hub.Enumeration()
    value_service_interface_Stability = onto_hub.Value()
    value_method_signature_Stability = onto_hub.Value()
    high1 = onto_hub.High()
    # stab_aggregate = onto_hub.Aggregated()
    eq = onto_hub.ConstrainOperator("equal")

    service1.hasQoS = [Stability]
    Stability.hasTendency = [high1]
    Stability.hasMetric = [service_interface_Stability, method_signature_Stability]
    Stability.hasWeight = [weight1]
    # Stability.hasAggregated = [stab_aggregate]
    weight1.hasNumericValue = [1]
    service_interface_Stability.hasValue = [value_service_interface_Stability]
    method_signature_Stability.hasValue = [value_method_signature_Stability]
    service_interface_Stability.hasConstrainOperator = [eq]
    method_signature_Stability.hasConstrainOperator = [eq]
    service_interface_Stability.hasMetricType = [metric_type1]
    method_signature_Stability.hasMetricType = [metric_type1]
    value_service_interface_Stability.hasStringValue = ["high"]
    value_method_signature_Stability.hasStringValue = ["medium"]
    # stab_aggregate.hasStringValue = ["MTTF/(MTTF+MTTR)"]
    #Stability

if True:
    # Performance
    service3 = onto_hub.Service("Temp_garage")
    Performance = onto_hub.QosParameter("Performance")
    weight3 = onto_hub.QosWeight()
    TransTime = onto_hub.Metric("TransTime")
    ResponseTime = onto_hub.Metric("ResponseTime")
    Throughput = onto_hub.Metric("Throughput")
    metric_type3 = onto_hub.Numeric()
    value_TransTime = onto_hub.Value()
    value_ResponseTime = onto_hub.Value()
    value_Throughput = onto_hub.Value()
    low = onto_hub.Low()
    # av_aggregate = onto_hub.Aggregated()
    unit2 = onto_hub.Unit("ms")
    lt = onto_hub.ConstrainOperator("lower_than")
    gt = onto_hub.ConstrainOperator("greater_than")

    service3.hasQoS = [Performance]
    Performance.hasTendency = [low]
    Performance.hasMetric = [TransTime, ResponseTime, Throughput]
    Performance.hasWeight = [weight3]
    # Performance.hasAggregated = [av_aggregate]
    weight.hasNumericValue = [0.1]
    TransTime.hasValue = [value_TransTime]
    ResponseTime.hasValue = [value_ResponseTime]
    Throughput.hasValue = [value_Throughput]
    TransTime.hasConstrainOperator = [lt]
    ResponseTime.hasConstrainOperator = [lt]
    Throughput.hasConstrainOperator = [gt]

    TransTime.hasMetricType = [metric_type3]
    ResponseTime.hasMetricType = [metric_type3]
    Throughput.hasMetricType = [metric_type3]
    value_TransTime.hasNumericValue = [100]
    value_ResponseTime.hasNumericValue = [10]
    value_Throughput.hasNumericValue = [0.9]
    # av_aggregate.hasStringValue = ["MTTF/(MTTF+MTTR)"]
    TransTime.hasUnit = [unit2]
    ResponseTime.hasUnit = [unit2]
    # Performance

if True:
    #Security
    service4 = onto_hub.Service("Temp_banco")
    security = onto_hub.QosParameter("Security")
    weight4 = onto_hub.QosWeight()
    Authentication = onto_hub.Metric("Authentication")
    Auditability = onto_hub.Metric("Auditability")
    Encryption = onto_hub.Metric("Encryption")
    Non_repudiation = onto_hub.Metric("Non_repudiation")
    metric_type4 = onto_hub.Enumeration()
    value_Authentication = onto_hub.Value()
    value_Auditability = onto_hub.Value()
    value_Encryption = onto_hub.Value()
    value_Non_repudiation = onto_hub.Value()
    # low = onto_hub.Low()
    # av_aggregate = onto_hub.Aggregated()
    # unit2 = onto_hub.Unit("ms")
    eq = onto_hub.ConstrainOperator("equal")

    service4.hasQoS = [security]
    # security.hasTendency = [low]
    security.hasMetric = [Authentication, Encryption, Auditability, Non_repudiation]
    security.hasWeight = [weight4]
    # Performance.hasAggregated = [av_aggregate]
    weight.hasNumericValue = [0.3]
    Authentication.hasValue = [value_Authentication]
    Auditability.hasValue = [value_Auditability]
    Encryption.hasValue = [value_Encryption]
    Non_repudiation.hasValue = [value_Non_repudiation]
    Authentication.hasConstrainOperator = [eq]
    Auditability.hasConstrainOperator = [eq]
    Encryption.hasConstrainOperator = [eq]
    Non_repudiation.hasConstrainOperator = [eq]

    Authentication.hasMetricType = [metric_type4]
    Auditability.hasMetricType = [metric_type4]
    Encryption.hasMetricType = [metric_type4]
    Non_repudiation.hasMetricType = [metric_type4]
    value_Authentication.hasStringValue = ["Required"]
    value_Auditability.hasStringValue = ["yes"]
    value_Encryption.hasStringValue = ["yes"]
    value_Non_repudiation.hasStringValue = ["no"]
    # av_aggregate.hasStringValue = ["MTTF/(MTTF+MTTR)"]
    # TransTime.hasUnit = [unit2]
    # ResponseTime.hasUnit = [unit2]
    #Security

for individual in onto_hub.individuals():
    instance[individual.name] = individual
print(instance)

onto_hub.save()
