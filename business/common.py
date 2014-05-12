#coding=utf8
from yuntao import dao
from threading import Lock
__author__ = 'yuntao.zyt'
lock = Lock()
commonDao = None
def getdao():
    global commonDao,lock
    if commonDao is not None:
        return commonDao
    try:
        lock.acquire()
        if commonDao is not None:
             return commonDao
        commonDao = dao.Dao("localhost","yuntao","root","",10)
        return commonDao;
    finally:
        lock.release()

