import redis
import json 
from typing import Any 

class RedisQueue:

    def __init__(self, 
                 host:str="localhost", 
                 port:str=6379,
                 db:int=1):
        self.db = db
        self.qname = "yo"
        self.host = host
        self.port = port
        self._init(self.qname)

    def _init(self, qname):
        self.redis = redis.Redis(host=self.host, 
                                 port=self.port, 
                                 db=self.db)
        return self

    def get(self):
        msg = self.redis.lpop(self.qname)
        msg = json.loads(msg)
        return msg
    
    def put(self,msg):
        msg = json.dumps(msg)
        self.redis.rpush(self.qname, msg)


    def qsize(self):
        qsize = self.redis.llen(self.qname)
        return qsize
    
    def delete(self):
        pass
