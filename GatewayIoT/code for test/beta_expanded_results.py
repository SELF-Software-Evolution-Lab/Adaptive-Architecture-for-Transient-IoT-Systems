from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report
import numpy as np
import redis


pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
redis_server = redis.Redis(connection_pool=pool)
beta = redis_server.lrange("memory_beta_data", 0, 80)
y_true = redis_server.lrange("true_expanded_data_2", 0, 80)
y_pred = redis_server.lrange("predicted_expanded_data_2", 0, 80)
file_output = open('beta_expanded_metric.txt', 'w')  # added
file_output.write("input;True;Predicted\n")  # added

for i in range(len(y_true)):
    print("input", beta[i], "\nTrue", y_true[i], "\nPredicted", y_pred[i])
    print()
    file_output.write(beta[i] + ";" + y_true[i] + ";" + y_pred[i] + "\n")  # added
print(len(y_true), len(y_pred))

cnf_matrix = confusion_matrix(y_true, y_pred)
np.set_printoptions(precision=2)
report = classification_report(y_true, y_pred, output_dict=True)
class_names = list(report.keys())
class_names = class_names[:-3]
print(classification_report(y_true, y_pred))
print()
file_output.write("\nResult;Precision;Recall;F1-score;Support\n")  # added
for key, value in report.items():
    results = list(value.values())
    file_output.write(key + ";" + str(results[0]) + ";" + str(results[1]) + ";" + str(results[2]) + ";" + str(results[3]) + "\n")  # added
file_output.close()  # added


