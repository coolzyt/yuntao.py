#coding=utf8
import tornado
from yuntao import log
from yuntao import dates
from business import common
import json
class ReadRss(tornado.web.RequestHandler):
    def get(self):
        dao = common.getdao()
        datas = dao.query("select * from rss_article limit 10");
        for data in datas:
            data["description"] = data.description[0:20]
            data["pubdate"] = dates.datetime2str(data.pubdate)
        print(datas)
        result = {"success":True,"data":datas}
        self.set_header("Content-Type","text/json")
        self.write(json.dumps(result))
        log.info("收到查询RSS请求:%s"%json.dumps(result))
        self.finish()