# coding=utf8
'''
Created on 2013年8月21日
数据库访问层
@author: zhaoyuntao
'''
from . import torndb
from . import log
from . import pool
from . import dates

class Dao:
    def __init__(self,host, database, user=None, password=None,poolsize=10):
        self.initialed = False
        start = dates.current_timestampms()
        log.debug("开始初始化连接池");
        self.host = host;
        self.database = database;
        self.user = user;
        self.password = password;
        self.poolsize = poolsize
        self._connection_pool = pool.Pool(poolsize)
        for i in range(poolsize):
            self._connection_pool.put(torndb.Connection(self.host, self.database, self.user, self.password))
        log.debug("初始化连接池结束,花费时间%dms"%(dates.current_timestampms()-start));
    
    def _getconnection(self):
        return self._connection_pool.get(timeout=1)
    
    def _returnconnection(self,conn):
        return self._connection_pool.put(conn,timeout=1)

    def execute(self,func,*parameters,**kwparameters):
        conn = None;
        try:
            conn = self._getconnection()
            return getattr(conn,func)(*parameters,**kwparameters)
        finally:
            self._returnconnection(conn)
    
    def query(self,*parameters,**kwparameters): return self.execute("query",*parameters,**kwparameters)
    def insert(self,*parameters,**kwparameters): return self.execute("insert",*parameters,**kwparameters)
    def insertmany(self,*parameters,**kwparameters): return self.execute("insertmany",*parameters,**kwparameters)
    def load(self,*parameters,**kwparameters): return self.execute("load",*parameters,**kwparameters)
    def update(self,*parameters,**kwparameters): return self.execute("update",*parameters,**kwparameters)
    def updatemany(self,*parameters,**kwparameters): return self.execute("updatemany",*parameters,**kwparameters)
    def remove(self,*parameters,**kwparameters): return self.execute("remove",*parameters,**kwparameters)

    def count(self,*parameters,**kwparameters):
        result = self.query(*parameters,**kwparameters)
        if len(result) == 0:
            return 0
        return list(result[0].items())[0][1]
    
    def exists(self,*parameters,**kwparameters):
        return self.count(*parameters,**kwparameters)>0

if __name__ == "__main__":
    dao = Dao("localhost","test",user="root",password="",poolsize=10)
    print(dao.count("select count(0) from user"))

