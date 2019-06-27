import sys
sys.path.append("/home/profesor/GatewayIoT")
import time
import requests
import json
from gateway import RD_functions
import redis
import socket

# def main():

# pool = redis.ConnectionPool(host='localhost', port=6379, db=0, decode_responses=True)
# pool = redis.ConnectionPool(host='172.24.100.98', port=8080, db=0, decode_responses=True)
# redis_server = redis.Redis(connection_pool=pool)
header = {"X-M2M-Origin": "admin:admin", "Accept": "application/json"}
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
s.connect(("8.8.8.8", 80))
ip_address = s.getsockname()[0]
s.close()
# base_url = "http://"+ip_address+":8080/~"
# base_url = "http://172.24.100.94:8080/~"
base_url = "http://172.24.100.95:8000/~"
# base_url = "http://127.0.0.1:8080/~"
# base_url = "http://127.0.0.1:8282/~"
# server_flag = True
server_flag = False
if server_flag is True:
    device = "/in-cse/in-name"
else:
    device = "/mn-cse/mn-name"
search = "?fu=1&rty=3&drt=1"
url_om2m = base_url + device + search

while True:
    try:
        rec_server = requests.get(url_om2m, headers=header)
        rec_server_dic = json.loads(rec_server.content)
        RD_functions.find_device(base_url, header, rec_server_dic, server_flag)
        #print(redis_server.smembers("registered_urls"))
        # print()
        # print("Number of visited resources ", len(redis_server.smembers("registered_urls")))
        # print()
        # print("Number de apps ", len(redis_server.smembers("apps_list")))
        # print(redis_server.smembers("apps_list"))
        print()
        # print(redis_server.get("execution_guidepost_apps"))
        time.sleep(10)
    except:
        print("error")
        continue


# if __name__ == "__main__":
#     main()

