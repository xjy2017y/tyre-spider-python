# -*- coding: utf-8
import threading
import re
from bs4 import BeautifulSoup
from db import ConnectDB
from getobj import GetObj
from common import *


url = "http://www.mailuntai.cn"


def threadSpider(brand,url2):   #获取到brand
    fname = brand+".txt"
    path ="../file/"+fname
    fobj = open(path,'a+')
    fileList = fobj.read().splitlines()
    print fileList
    fobj.close()
    obj = GetObj(url2)
    html = obj.gethtml()
    coding = obj.getcodeing(html)
    soup = BeautifulSoup(html,"html5lib",from_encoding=coding)
    clearfix = re.compile(r'list clearfix')
    clearfix = soup.find_all("div",attrs={"class":clearfix})
    figure = clearfix[1].find_all("a")
    for item in figure:
        flow = item.text.strip()
        streak = re.sub(r'\([^\)]*\)',"",flow)    #获取到花纹
        logger.info("streak:" + streak)
        href = item.get("href")
        newUrl = url + href
        obj = GetObj(newUrl)
        html = obj.gethtml()
        coding = obj.getcodeing(html);
        soup = BeautifulSoup(html,"html5lib",from_encoding=coding)
        clearfix = re.compile(r'products clearfix')
        clearfix = soup.find("div",attrs={"class":clearfix})
        clearfix2 = re.compile(r'product clearfix')
        clearfix2 = clearfix.find_all("div",attrs={"class":clearfix2})
        for i in clearfix2:
            name = i.a.get("title")                     #获取到轮胎name
            print name
            logger.info("name:" + name)
            href = i.a.get("href")
            print href
            xx= href.split("/")
            xh = xx[2].split(".")
            tyreid = xh[0]
            if href not in fileList:
                fobj = open(path,'a+')
                print u'写入'+href
                fobj.write(href+'\n')
                fobj.flush()
                fobj.close()

                db=ConnectDB()
                n = db.select(table_name="tyreinfo",field="tyreID",value=tyreid)
                if n != 0:
                    logger.info("tyreID: %s exists " %  tyreid )
                    print tyreid + u"存在"
                    continue
                tyreUrl = url + href
                tyreObj = GetObj(tyreUrl)
                tyreHtml = tyreObj.gethtml()
                tyreSoup = BeautifulSoup(tyreHtml,"html5lib",from_encoding=coding)
                basic = re.compile(r'basic free')
                basic = tyreSoup.find("div",attrs={"class":basic})
                fl = re.compile(r'fl')
                fl = basic.find("span",attrs={"class":fl})


                standard = fl.text.strip()                  #获取到standard
                logger.info("standard:" + standard)

                dl = basic.find_all("dl")
                loaded = dl[4].dd.text.strip()            #获取到load
                #loaded = re.sub(r'\([^\)]*\)',"",loaded)
                logger.info("load:" + loaded)

                speed = dl[5].dd.text.strip()       #获取到speed
                #speed = re.sub(r'\([^\)]*\)',"",speed)
                logger.info("speed:"+speed)

                place = dl[6].dd.text.strip()
                logger.info("place:"+place)



                pi3c = re.compile(r'clearfix pi3c')
                pi3c = basic.find("div",attrs={"class":pi3c})
                pi3c = pi3c.find_all("em")

                wearproof = pi3c[0].text.strip()            #获取到wearproof
                #wearproof = ""
                logger.info("wearproof:"+wearproof)

                traction = pi3c[1].text.strip()             #获取到traction
                logger.info("traction:"+traction)

                highTemperature = pi3c[2].text.strip()      #获取到highTemperature
                logger.info("highTemperature:"+highTemperature)

                db.insert("tyreinfo",tyreid,brand,streak,name,standard,loaded,speed,wearproof,traction,highTemperature)
                db.dbclose()

            else:
                logger.info(u"跳过"+href)
                print(u"跳过"+href)
                continue
    logger.info("finish:" + brand)



def firstGetHtml():
    obj = GetObj(url);
    html = obj.gethtml();
    coding = obj.getcodeing(html);
    soup = BeautifulSoup(html,"html5lib",from_encoding=coding)
    list = re.compile(r'i4')
    list = soup.find("div",attrs={"id":list})
    li = list.find_all("li")
    for item in li:
        if(item.a.get("href").strip() != '//'):         #排除掉空的url
            href = url + item.a.get("href")
            brand = item.a.text.strip()
            print brand+u"开始爬取"
            logger.info(brand + u" 开始爬取")
            t = threading.Thread(target=threadSpider,args=(brand,href))
            t.start()
            while True:
                if(len(threading.enumerate()) < THARED_NUMBER + 1 ):      #threading.enumerate(): 返回一个包含正在运行的线程的list。正在运行指线程启动后、结束前，不包括启动前和终止后的线程。  这里限制线程数不大于6个
                    break
    return

def begin():
    logger.info("start spider!")
    firstGetHtml()
    logger.info("finish spider!")



if __name__ == "__main__":
    print "start!!"
    begin();