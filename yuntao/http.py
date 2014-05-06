#!/usr/bin/env python
'''
Created on 2013-7-11

@author: zhaoyt
'''
import gzip
import io
import urllib.request, urllib.error, urllib.parse
from yuntao import log
import re

def post(url,body):
    req = urllib.request.Request(url);
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31");
    req.add_header("Accept-Charset","utf-8;q=0.7,*;q=0.3")
    opener = urllib.request.build_opener();
    ret = opener.open(req,body);
    return ret.read();

def get(url):
    req = urllib.request.Request(url);
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31");
    req.add_header("Accept-Charset","utf-8;q=0.7,*;q=0.3")
    filehandle = urllib.request.urlopen(req)
    return filehandle.read()

_regex_charset = '(charset|encoding)="?(GBK|GB2312|UTF8|UTF-8)"?'
def fetchurl(url,encoding="utf8"):
    """
                输出url的文档内容
    """
    req = urllib.request.Request(url);
    req.add_header("User-Agent", "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.31 (KHTML, like Gecko) Chrome/26.0.1410.64 Safari/537.31");
    req.add_header("Accept-Charset","utf-8;q=0.7,*;q=0.3")
    filehandle = urllib.request.urlopen(req)
    content_encoding = ( "Content-Encoding" in filehandle.headers and filehandle.headers["Content-Encoding"] or "" ) ;
    isgzip = re.search("gzip",content_encoding,re.I) is not None
    contentType = filehandle.headers["Content-Type"];
    matcher = re.search(_regex_charset,contentType,re.I)
    if isgzip:
        compresseddata = filehandle.read()
        compressedstream = io.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        ret = gzipper.read()
    else:
        ret = filehandle.read()
    ret = ret.decode();
    if matcher is None:
        matcher = re.search(_regex_charset,ret,re.I)
    if matcher is not None:
        charset = matcher.group(2)
        log.info("源文件编码为:"+charset)
        if charset.lower() in ("utf8,utf-8") and encoding.lower() in ("utf8,utf-8"):
            pass;
        elif charset.lower() != encoding.lower():
            log.info("进行转码,从"+charset+"转为"+encoding);
            ret = ret.encode(charset,"ignore").decode(encoding,"ignore")
    filehandle.close()
    return ret;
