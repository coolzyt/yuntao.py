#!/usr/bin/env python
#coding=utf8

from yuntao import http
from business import common
from yuntao import dates
from yuntao import log
import re
import xml.etree.ElementTree as etree
class Crawler:
    def __init__(self):
        self.dao = common.getdao()
        self.seeds = ["http://huoding.com/feed","http://2014.54chen.com/rss.xml"]
  
    def fetchrss(self,url):
        page = http.fetchurl(url)
        root = etree.XML(page)[0];
        for child in root:
            if child.tag=="item":
                title = child.findall("title")[0].text
                desc = child.findall("description")[0].text
                pubdate = child.findall("pubDate")[0].text
                if re.match("^[a-zA-Z]{3}\\,", pubdate):
                    pubdate = pubdate[0:len("Thu, 19 Feb 2009 16:00:07")] #英文时间格式
                    DATE_FORMAT = '%a, %d %b %Y %H:%M:%S'
                    pubdate = dates.str2datetime(pubdate, DATE_FORMAT)
                if re.match("^\d{4}-\d{2}-\d{2}T.{8,}", pubdate):
                    pubdate = pubdate[0:19]
                    DATE_FORMAT = '%Y-%m-%dT%H:%M:%S'
                    pubdate = dates.str2datetime(pubdate, DATE_FORMAT)
                if not self.dao.exists("select count(0) from rss_article where source=%s and pubdate=%s",url,pubdate):
                    log.info("采集到文章:%s"%title);
                    self.dao.insert("insert into rss_article(title,description,pubdate,source) values(%s,%s,%s,%s)",title,desc,pubdate,url);

    
    def crawl(self):
        for url in self.seeds:
            try:
                log.debug("开始采集[%s]的文章"%url);
                self.fetchrss(url)
            except Exception as e:
                log.debug("采集[%s]的文章发生异常"%url);
                log.exception(e)
