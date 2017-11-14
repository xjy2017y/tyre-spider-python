# -*- coding: utf-8
import cookielib
import urllib2
import urllib
import re
from selenium import webdriver
import chardet
import time
from common import *
class GetObj(object):

    def __init__(self,url,default = ""):
        if default == "":
            cookie_jar = cookielib.LWPCookieJar()        #LWPCookieJar()是管理cookie的工具  cookie中存有个人的私有属性，所以要先拿到cookie的数据
            cookie = urllib2.HTTPCookieProcessor(cookie_jar)   #默认的opener并不支持cookie。 那么我们先新建一个支持cookie的opener。urllib2中供我们使用的是HTTPCookieProcessor。
            self.opener = urllib2.build_opener(cookie)   #创建一个opener
            user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"   #修改默认请求头，为了避免自动化程序被拒绝，
            self.url=url          #填充url
            self.send_headers={'User-Agent':user_agent}  #设置
        else:
            self.opener.close() #关闭Opener
            httpproxy_handler = urllib2.ProxyHandler(default)
            self.opener = urllib2.build_opener(httpproxy_handler)
            user_agent="Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36"   #修改默认请求头，为了避免自动化程序被拒绝，
            self.url=url          #填充url
            self.send_headers={'User-Agent':user_agent}  #设置


    def getcodeing(self,obj):
        if obj:
            coding=chardet.detect(obj)["encoding"]   # chardet.detect(obj)返回的是{'confidence': 0.98999999999999999, 'encoding': 'GB2312'}数组格式，在根据字段取encoding值
            return coding   #返回编码类型



    def gethtml(self):
        request = urllib2.Request(self.url,headers=self.send_headers)
        try:
            #response = self.opener.open(request)
            #reurl = response.geturl()
            soures_home = self.opener.open(request).read()   #  打开该请求网址，并记录到soures_home中
        except urllib2.URLError,e:
            logger.info('URLError')
            logger.info(e.reason)
            return None
        except urllib2.HTTPError,e:
            logger.info('URLError')
            print "httpError!!!"
            return None
        return soures_home


