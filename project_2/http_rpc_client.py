#!/usr/bin/python
# -*- coding: utf-8 -*-

'''This module is a simple rpc client'''
import json
import asyncio
import aiohttp
import uuid

class Client:
    '''
    A client class including some method
    Connect with remote server
    '''
    # Header information which is private and won't be changed
    __headers = {"content-type": "application/json"}

    def __init__(self, addr = "127.0.0.1:8088"):
        '''
        Initial the instance with the address given
        And addr will have a default value
        http://127.0.0.1:8088
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

    def add(self, a, b):
        '''
        Call the remote function add(int, int)
        Return the sum of two integer as type int
        '''
        
        result = self.loop.run_until_complete(self.__json_rpc("add", [a, b]))["result"]
        return result

    def sub(self, a, b):
        '''
        Call the remote function sub(<a:int>, <b:int>)
        Return the result of a - b as type int
        '''
        result = self.loop.run_until_complete(self.__json_rpc("sub", [a, b]))["result"]
        return result

    def json_to_xml(self, json_data):
        '''
        Accept a json string and call the remote function
        Convert the json to xml and return xml string
        '''
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
        with aiohttp.ClientSession() as session:
            async with session.post(
                self.addr, data = json.dumps(payload),
                headers = Client.__headers
                ) as response:
                return await response.json()