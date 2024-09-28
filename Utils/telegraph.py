# Copyright 2023 Qewertyy, MIT License
from httpx import Client,AsyncClient
import os,traceback,json
from .htmlParser import htmlToNodes
from .constants import URLS

TELEGRAPH = URLS.get("TELEGRAPH")

class GraphClient:
    def __init__(self,author_name,author_url,short_name,access_token=None):
        self.baseUrl = TELEGRAPH
        self.client = Client(http2=True)
        self.access_token = access_token
        self.author_name = author_name
        self.author_url = author_url
        self.short_name = short_name
        self.headers = {
            "User-Agent":"SDWaifuRobot/1.0",
            "Content-Type":"application/json"
        }
    
    def createAccount(self,):
        url = self.baseUrl+"/createAccount"
        data = {
            "author_name":self.author_name,
            "author_url":self.author_url,
            "short_name":self.short_name
        }
        resp = self.client.post(url,json=data,headers=self.headers)
        if resp.status_code != 200:
            return None
        resp = resp.json()
        if resp.get('ok'):
            self.access_token = resp['result']['access_token']
            return None
        raise Exception(resp['error'])
    
    def createPage(self,title,content):
        url = self.baseUrl+"/createPage"
        content_json = json.dumps(htmlToNodes(content),separators=(',', ':'), ensure_ascii=False)
        data = {
            'access_token': self.access_token,
            'title': title,
            'author_name': self.author_name,
            'author_url':   self.author_url,
            'content': content_json,
            'return_content': False
        }
        resp = self.client.post(url,json=data,headers=self.headers)
        if resp.status_code != 200:
            return None
        resp = resp.json()
        if resp.get('ok'):
            return resp['result']['url']
        raise Exception(resp['error'])
