#!/usr/bin/python
# -*- coding: utf-8 -*-

'''Python class access github api'''

import requests
import json
import copy

class ClientError(Exception):

    '''An exception class'''

    __code_to_message = {
        100: "Continue",
        101: "Switching Protocols",
        102: "Processing",
        200: "OK",
        201: "Created",
        202: "Accepted",
        203: "Non-Authoritative Information",
        204: "No Content",
        205: "Reset Content",
        206: "Partial Content",
        207: "Multi-Status",
        208: "Already Reported",
        226: "IM Used",
        300: "Multiple Choices",
        301: "Moved Permanently",
        302: "Found",
        303: "See Other",
        304: "Not Modified",
        305: "Use Proxy",
        307: "Temporary Redirect",
        308: "Permanent Redirect",
        400: "Bad Request",
        401: "Unauthorized",
        402: "Payment Required",
        403: "Forbidden",
        404: "Not Found",
        405: "Method Not Allowed",
        406: "Not Acceptable",
        407: "Proxy Authentication Required",
        408: "Request Timeout",
        409: "Conflict",
        410: "Gone",
        411: "Length Required",
        412: "Precondition Failed",
        413: "Request Entity Too Large",
        414: "Request URI Too Long",
        415: "Unsupported Media Type",
        416: "Requested Range Not Satisfiable",
        417: "Expectation Failed",
        418: "I'm a teapot",
        422: "Unprocessable Entity",
        423: "Locked",
        424: "Failed Dependency",
        426: "Upgrade Required",
        428: "Precondition Required",
        429: "Too Many Requests",
        431: "Request Header Fields Too Large",
        451: "Unavailable For Legal Reasons",
        500: "Internal Server Error",
        501: "Not Implemented",
        502: "Bad Gateway",
        503: "Service Unavailable",
        504: "Gateway Timeout",
        505: "HTTP Version Not Supported",
        506: "Variant Also Negotiates",
        507: "Insufficient Storage",
        508: "Loop Detected",
        510: "Not Extended",
        511: "Network Authentication Required"
    }
    def __init__(self, status_code):

        '''Constractor'''

        self.status = status_code 
        self.message = self.__code_to_message[status_code] 

class GithubClient:
    
    '''A class can access github api'''
    
    def __init__(self, personal_access_token):

        '''Init github api requests headers'''

        self.headers = {
            "Accept":"application/vnd.github.v3+json",
            "Authorization": "token " + personal_access_token
        }

    def ListStars(self):

        '''List the repositories which user star'''

        r = requests.get("https://api.github.com/user/starred", headers=self.headers)
        if r.status_code == 200:
            result = []
            for x in r.json():
                result.append(
                    {
                        "id":x["id"],
                        "name":x["name"],
                        "full_name":x["full_name"],
                        "login":x["owner"]["login"],
                        "url":x["url"]
                    }
                )
            return str(json.dumps(result))
        else:
            raise ClientError(r.status_code)
    
    def ListFollowers(self):

        '''List user's followers'''

        r = requests.get("https://api.github.com/user/followers", headers=self.headers)
        if r.status_code == 200:
            result = []
            for x in r.json():
                result.append(
                    {
                        "login":x["login"],
                        "url":x["url"],
                    }
                )
            return str(json.dumps(result))
        else:
            raise ClientError(r.status_code)
        
    def ListRepositories(self):

        '''List user's repositories'''

        r = requests.get("https://api.github.com/user/repos", headers=self.headers)
        if r.status_code == 200:
            result = []
            for x in r.json():
                result.append(
                    {
                        "id":x["id"],
                        "name":x["name"],
                        "full_name":x["full_name"],
                        "login":x["owner"]["login"],
                        "login_id":x["owner"]["id"],
                        "url":x["url"]
                    }
                )
            return str(json.dumps(result))
        else:
            raise ClientError(r.status_code)
    
    def StarRepository(self, owner_id, repo_id):

        '''Star a repository'''

        special_headers = copy.deepcopy(self.headers)
        special_headers["Content-Length"] = "0"
        owner_r = requests.get("https://api.github.com/user/"+str(owner_id), headers=self.headers)
        if not owner_r.status_code == 200:
            raise ClientError(owner_r.status_code)
        owner = owner_r.json()["login"]
        repo_r = requests.get("https://api.github.com/repositories/"+str(repo_id), headers=self.headers)
        if not repo_r.status_code == 200:
            raise ClientError(repo_r.status_code)
        repo = repo_r.json()["name"]
        r = requests.put("https://api.github.com/user/starred/" + owner + "/" + repo, headers=special_headers)
        if r.status_code == 204:
            return str(json.dumps({"success": "ok"}))
        else:
            raise ClientError(r.status_code)

    def FollowUser(self, username):

        '''Follow a user'''

        special_headers = copy.deepcopy(self.headers)
        special_headers["Content-Length"] = "0"
        r = requests.put("https://api.github.com/user/following/" + username, headers=special_headers)
        if r.status_code == 204:
            return str(json.dumps({"success": "ok"}))
        else:
            raise ClientError(r.status_code)
    
    def UnfollowUser(self, username):

        '''Unfollow a user'''

        r = requests.delete("https://api.github.com/user/following/" + username, headers=self.headers)
        if r.status_code == 204:
            return str(json.dumps({"success": "ok"}))
        else:
            raise ClientError(r.status_code)
    
    def CreateRepository(self, repo_name):

        '''Create a repository'''

        payload = {
            "name": repo_name
        }
        r = requests.post("https://api.github.com/user/repos", data=str(json.dumps(payload)), headers=self.headers)
        if r.status_code == 201:
            repo_id = r.json()["id"]
            return str(json.dumps({"success":"ok", "id": repo_id}))
        else:
            raise ClientError(r.status_code)

    
    def DeleteRepository(self, owner_id, repo_id):

        '''Delete a repository'''

        owner_r = requests.get("https://api.github.com/user/" + str(owner_id), headers=self.headers)
        if not owner_r.status_code == 200:
            raise ClientError(owner_r.status_code)
        owner = owner_r.json()["login"]
        repo_r = requests.get("https://api.github.com/repositories/" + str(repo_id), headers=self.headers)
        if not repo_r.status_code == 200:
            raise ClientError(repo_r.status_code)
        repo = repo_r.json()["name"]
        r = requests.delete("https://api.github.com/repos/" + owner + "/" + repo, headers=self.headers)
        if r.status_code == 204:
            return str(json.dumps({"success":"ok"}))
        else:
            raise ClientError(r.status_code)