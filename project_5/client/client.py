'''Client'''
import json
import sys
import requests

def execute_sql():
    '''main'''
    url = "http://" + HOST + "/"
    headers = {'content-type': 'application/json'}

    # Example echo method
    payload = {
        "method": "execute",
        "params": ["SELECT * FROM items"],
        "jsonrpc": "2.0",
        "id": 0,
    }
    response = requests.post(url, data=json.dumps(payload), headers=headers)
    if response.status_code == 200:
        print("Connecting to database... [OK]")
        print("Retrieving data... [OK]")
        print("--- RESULT ---")
        for row in response.json()["result"]:
            print(row)
        print("--------------")

def find_service(service):
    '''Find service'''
    response = requests.get("http://" + CONSUL_ADDRESS + "/v1/catalog/service/" + service)
    if response.status_code == 200:
        print("Connecting to consul... [OK]")
        print("Looking for database... [OK]")
    else:
        return False
    service_info = response.json()[0]
    print("---")
    print("[INFO]database host = " + service_info["ServiceAddress"])
    print("[INFO]database post = " + str(service_info["ServicePort"]))
    print("---")
    host = service_info["Address"] + ":" + str(service_info["ServicePort"])
    return host

if __name__ == "__main__":
    if len(sys.argv) == 2:
        CONSUL_ADDRESS = sys.argv[1].replace("'", "")
        HOST = find_service("database")
        if HOST:
            execute_sql()
