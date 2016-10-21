'''Sqlite3 Service'''
import sqlite3
import sys
import json
import requests
from flask import Flask
from jsonrpc.backend.flask import api

APP = Flask(__name__)
APP.register_blueprint(api.as_blueprint())

@api.dispatcher.add_method
def execute(sql):
    '''Execute SQL'''
    conn = sqlite3.connect(PATH)
    cursor = conn.execute(sql)
    result = []
    for row in cursor:
        result.append(row[0])
    return result

def register_service():
    '''Register service in consul'''
    data = {
        "Datacenter": "dc1",
        "Node": "database",
        "Address": "45.63.120.38",
        "Service": {"Service": "database", "Port": int(PORT), "Address": "45.63.120.38"}
        }
    response = requests.put(
        "http://" + CONSUL_ADDRESS + "/v1/catalog/register",
        data=str(json.dumps(data))
        )
    if response.status_code == 200:
        return True
    return False

if __name__ == '__main__':
    if len(sys.argv) == 4:
        PATH = sys.argv[1].replace("'", "")
        CONSUL_ADDRESS = sys.argv[2].replace("'", "")
        PORT = sys.argv[3]
        if PORT.isdigit():
            if register_service():
                print("Register consul service successful!")
                APP.run(host="0.0.0.0", port=int(PORT), debug=True)
            else:
                print("Consul service register failed!")
