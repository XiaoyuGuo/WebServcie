#!/usr/bin/python
# -*- coding: utf-8 -*-

'''This module is a simple rpc client'''
import json
import asyncio
import uuid
import aiohttp

class Client:
    '''
    A client class including some method
    Connect with remote server
    '''
    # Header information which is private and won't be changed
    __headers = {"content-type": "application/json"}

    def __init__(self, addr="127.0.0.1:8088"):
        '''
        Initial the instance with the address given
        And addr will have a default value 127.0.0.1:8088
        '''
        self.addr = "http://" + addr
        self.loop = asyncio.get_event_loop()

    def time(self):
        '''
        Call the remote function time()
        Return current timestamp as type int
        '''
        #test async
        #tasks = []
        #tasks.append(asyncio.ensure_future(self.__json_rpc("time", [])))
        #tasks.append(asyncio.ensure_future(self.__json_rpc("time", [])))
        #tasks.append(asyncio.ensure_future(self.__json_rpc("time", [])))
        #print(self.loop.run_until_complete(asyncio.gather(*tasks)))
        result = self.loop.run_until_complete(self.__json_rpc("time", []))["result"]
        return result

    def ram(self):
        '''
        Call the remote function ram()
        Return ram information
        [total, used] as type [int, int]
        '''
        result = self.loop.run_until_complete(self.__json_rpc("ram", []))["result"]
        return result

    def hdd(self):
        '''
        Call the remote function hdd()
        Return hdd information
        [total, used] as type [int, int]
        '''
        result = self.loop.run_until_complete(self.__json_rpc("hdd", []))["result"]
        return result

    def add(self, integer_num_a, integer_num_b):
        '''
        Call the remote function add(integer_num_a, integer_num_b)
        Return the sum of two integer as type int
        '''
        # Validation
        if not isinstance(integer_num_a, int) or not isinstance(integer_num_b, int):
            raise Exception("not an integer")

        result = self.loop.run_until_complete(
            self.__json_rpc("add", [integer_num_a, integer_num_b])
            )["result"]

        return result

    def sub(self, integer_num_a, integer_num_b):
        '''
        Call the remote function sub(integer_num_a, integer_num_b)
        Return the result of integer_num_a - integer_num_b as type int
        '''
        # Validation
        if not isinstance(integer_num_a, int) or not isinstance(integer_num_b, int):
            raise Exception("not an integer")

        result = self.loop.run_until_complete(
            self.__json_rpc("sub", [integer_num_a, integer_num_b])
            )["result"]
        return result

    def json_to_xml(self, json_data):
        '''
        Accept a json string and call the remote function
        Convert the json to xml and return xml string
        '''
        # Validation
        try:
            json.loads(json_data)
        except:
            raise Exception("invalid JSON string")

        result = self.loop.run_until_complete(self.__json_rpc("json_to_xml", [json_data]))["result"]
        return result

    async def __json_rpc(self, method, params):
        '''
        Private method _json_rpc
        According to the static params _url and _headers
        With the given params <method:string> and <params:list>
        Call the remote function and return the result
        '''
        payload = {
            "method": method,
            "params": params,
            "jsonrpc": "2.0",
            "id": str(uuid.uuid1())
        }
        try:
            with aiohttp.ClientSession() as session:
                async with session.post(
                    self.addr, data=json.dumps(payload),
                    headers=Client.__headers
                    ) as response:
                    return await response.json()
        except:
            raise Exception("server unreachable")
            