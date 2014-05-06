#coding=utf8
import sched,time
from yuntao import pool
from threading import Thread
from threading import Lock
from threading import Condition
from threading import Timer
from yuntao import log
from yuntao import dates
import queue;

class Task:
    def __init__(self,function,*args ,**kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
    
    def _execute(self):
        self.function(*self.args,**self.kwargs)

class FutureTask(Task):
    def __init__(self,function,*args,**kwargs):
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.lock = Lock()
        self.e = None
        self.executing = False;
    
    def _execute(self):
        try:
            self.lock.acquire()
            self.executing = True;
            self.result = self.function(*self.args,**self.kwargs);
        except Exception as e:
            self.e = e;
        finally:
            self.lock.release()
        
    def result(self):
        try:
            while True:
                if self.executing: #检查标志位，避免死锁
                    self.lock.acquire()
                    if self.e is not None:
                        raise self.e;
                    return self.result
        finally:
            self.lock.release()




class ThreadPool:    
    def __init__(self,worker_num):
        self.queue = queue.Queue()
        self.workers = []
        for i in range(worker_num):
            worker = _Worker(self.queue)
            self.workers.append(worker)
            worker.start()
    
    def submit(self,function,*args,**kwargs):
        task = FutureTask(function,*args,**kwargs)
        self.queue.put(task);
        return task

    def execute(self,function,*args,**kwargs):
        task = Task(function,*args,**kwargs)
        self.queue.put(task);
    
    def shutdown(self):
        for worker in self.workers:
            try:
                worker._stop();
            except Exception as e:
                log.exception(e)


class ScheduleTask(Task):
    def __init__(self,nexttime,period,function,*args ,**kwargs):
        self.nexttime = nexttime
        self.period = period
        self.function = function
        self.args = args
        self.kwargs = kwargs

class CoreScheduleThread(Thread):
    def __init__(self,threadpool):
        self.scheduletasks = [];
        self.tasklock = Lock();
        self.condition = Condition(Lock())
        self.threadpool = threadpool
        Thread.__init__(self)

    def run(self):
        while True:
            self.condition.acquire()
            if len(self.scheduletasks) == 0:
                self.condition.wait();
            else:
                task = self.scheduletasks.pop(0)
                if dates.current_timestamps()>=task.nexttime: 
                    self.threadpool.execute(task.function,*task.args,**task.kwargs)
                    task.nexttime = dates.current_timestamps()+task.period;
                else:
                    self.condition.wait(task.nexttime-dates.current_timestamps())
                self.addtask(task)
            self.condition.release()

    
    def addtask(self,task): # copy on write
        self.tasklock.acquire()
        tasks = [ t for t in self.scheduletasks ]
        tasks.append(task)
        tasks.sort(key=lambda task:task.nexttime)
        self.scheduletasks = tasks
        self.tasklock.release()

class ScheduledThreadPool(ThreadPool):
    
    def __init__(self,worker_num):
        ThreadPool.__init__(self,worker_num)
        self.core_thread = CoreScheduleThread(self)
        self.core_thread.start()
        
    def schedule(self,function,delay=0,period=0,*args,**kwargs):
        curtime = dates.current_timestamps();
        nexttime = curtime+delay
        task = ScheduleTask(nexttime,period,function,*args,**kwargs)
        self.core_thread.addtask(task);
        self.core_thread.condition.acquire()
        self.core_thread.condition.notify_all()
        self.core_thread.condition.release()

class _Worker(Thread):
    def __init__(self,queue):
        Thread.__init__(self)
        self.queue = queue
        
    def run(self):
        queue = self.queue
        while True:
            try:
                task = queue.get() 
                task._execute()
            except Exception as e:
                log.exception(e)
                raise e;

                            
def new_threadpool(threadnum):
    return ThreadPool(threadnum)

def new_scheduled_threadpool(threadnum):
    return ScheduledThreadPool(threadnum)

if __name__ == "__main__":
    threadpool = new_scheduled_threadpool(3)
    def a():
        print("执行a:"+dates.current_datetime_as_str())
    def b():
        print("执行b:"+dates.current_datetime_as_str())
    def c():
        print("执行c:"+dates.current_datetime_as_str()) 
    time.sleep(2)    
    threadpool.schedule(a,delay=0,period=2)
    time.sleep(4)
    threadpool.schedule(b,delay=2,period=5)
    time.sleep(4)
    threadpool.schedule(c,delay=0,period=3)