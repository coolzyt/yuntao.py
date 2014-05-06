#coding=utf8
import queue
"""
    简单的对象池
"""
class Pool:
    def __init__(self,poolsize):
        self.queue = queue.Queue(poolsize) 
    
    def get(self,block=True,timeout=None):
        return self.queue.get(block=block,timeout=timeout);
            
    def put(self,item,block=True,timeout=None):
        self.queue.put(item,block=block,timeout=timeout);
