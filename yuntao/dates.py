#coding=utf8
'''
Created on 2011-6-26

@author: zhaoyuntao
'''

import datetime
import time
def current_datetime_as_str(format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.now().strftime(format);

def current_datetime():
    return datetime.datetime.now();

def datetime2str(datetime,format="%Y-%m-%d %H:%M:%S"):
    return datetime.strftime(format);

def str2datetime(datetime_str,format="%Y-%m-%d %H:%M:%S"):
    return datetime.datetime.strptime(datetime_str,format);

def current_timestampms():
    return int(time.time()*1000)

def timestampms2datetime(timestamp):
    return datetime.datetime.fromtimestamp(timestamp/float(1000));

def datetime2timestampms(datetime):
    return int(time.mktime(datetime.timetuple())*1000);

def timestampms2datetimestr(timestampms,format="%Y-%m-%d %H:%M:%S"):
    return datetime2str(timestampms2datetime(timestampms),format);
