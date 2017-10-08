# coding=UTF-8
import json
import sys
import time
import urllib

import requests


sys.path.append("..")
import DataBase.DatabaseDAL
import random
import global_Vars
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

num = global_Vars.startRowNum  #从第几行开始

def main():

    # 第一步，抓取艺人的最后url,入库
    print "开始获取每个艺人最后的url........".decode("utf8")
    getUrl()

    # 第二步，根据上一步的url，抓取试听、粉丝、评论
    print "\n开始抓取试听、粉丝、评论........".decode("utf8")
    getData()




def getUrl():
    try:

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        sql = "select 原始姓名  from Table_Spider where id>={0} and 酷狗音乐_URL is null".format(num)
        list = dbDAL.query(sql)
        resultList=[]
        for (name,) in list:
            obj = _getUrl(name, True)
            if obj is not None:
                print "{0},url={1}".format(name,obj["酷狗音乐_URL"]).decode("utf8")
                obj["原始姓名"]=name
                resultList.append(obj)
            else:
                print "{0},没有url".format(name).decode("utf8")
        dbDAL.update(tableName="Table_Spider",list=resultList,whereTuple=("原始姓名",))
    except Exception as e:
        print "error"+e.message.decode("utf8")
    finally:
        dbDAL.dispose()

def _getUrl(name,isFirst):
    url = "http://so.service.kugou.com/get/complex"
    sleepTime = random.randint(2, 5)
    time.sleep(sleepTime)
    parms ={}
    parms["word"]=name
    data = urllib.urlencode(parms)
    url = url + "?" + data
    try:
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        j = json.loads(page.text)
    except:
        print "超时,1分钟后抓取，艺人：{0}".format(name)
        time.sleep(60)
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        j = json.loads(page.text)

    try:
        pass
        singerId=j["data"]["1"]["singerid"];
        href="http://public.service.kugou.com/user/singer?action=getfansnum&uid=&singerid={0}".format(singerId)
        return {"姓名": name, "酷狗音乐_URL": href}
    except:
        if isFirst and len(name.split("乐"))>1 :
            #在这里分割“乐”前面的字符
            return _getUrl(name.split("乐")[0], False)
        else :
            return None

def getData():
    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    sql = "select 姓名,酷狗音乐_URL  from Table_Spider where 酷狗音乐_URL is not null and id>={0}".format(num)
    list = dbDAL.query(sql)
    updateList=[]
    for (name, url) in list:
        sleepTime = random.randint(2, 5)
        time.sleep(sleepTime)
        sql2 = ""
        values = []
        try:
            obj={}
            page = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
            j = json.loads(page.text)
            fansnum=j["data"]["fansnum"]

            # API地址

            obj["酷狗音乐_粉丝数"]=fansnum

            if obj.has_key("酷狗音乐_粉丝数"):
                updateList.append(obj)
                obj["姓名"]=name
                print "{0},粉丝：{1}".format(obj["姓名"],obj["酷狗音乐_粉丝数"])
            else:
                print "***意外:"+obj
        except Exception as e:
            print e.message
            print "***超时 {0}".format(name).decode("utf8")


    dbDAL.update(tableName="Table_Spider",list=updateList,whereTuple={"姓名",})

    dbDAL.dispose()

if __name__=="__main__":
    main()