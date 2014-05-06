# coding=utf8
'''
Created on 2013年8月21日
数据库访问层
@author: zhaoyuntao
'''
import threading
from . import torndb
from . import log
from . import pool
class _Context:
    pass;

context = _Context()
context.lock = threading.Lock();
context.initialed = False
from . import dates
def init(host, database, user=None, password=None,poolsize=10):
    try:
        context.lock.acquire();
        if context.initialed:
            log.debug("已经进行过初始化");
            return;
        start = dates.current_timestampms()
        log.debug("开始初始化连接池");
        context.host = host;
        context.database = database;
        context.user = user;
        context.password = password;
        context.poolsize = poolsize
        context._connection_pool = pool.Pool(poolsize) 
        for i in range(context.poolsize):
            context._connection_pool.put(torndb.Connection(context.host, context.database, context.user, context.password))
        context.initialed = True
        log.debug("初始化连接池结束,花费时间%dms"%(dates.current_timestampms()-start));
    finally:
        context.lock.release();

def _getconnection():
    return context._connection_pool.get(timeout=1)

def _returnconnection(conn):
    return context._connection_pool.put(conn,timeout=1)

def _wrapper(func):
    def executor(*parameters,**kwparameters):
        try:
            conn = _getconnection()
            return getattr(conn,func)(*parameters,**kwparameters)
        finally:
            _returnconnection(conn)
    return executor;

query = _wrapper("query")
insert = _wrapper("insert")
insertmany = _wrapper("insertmany")
load = _wrapper("get")
update = _wrapper("update")
updatemany = _wrapper("updatemany")
remove = update
def count(*parameters,**kwparameters):
    result = query(*parameters,**kwparameters)
    if len(result) == 0:
        return 0
    return list(result[0].items())[0][1]

def exists(*parameters,**kwparameters):
    return count(*parameters,**kwparameters)>0

if __name__ == "__main__":
    init("localhost","test",user="root",password="root",poolsize=10)
    print(count("select count(0) from user"))

