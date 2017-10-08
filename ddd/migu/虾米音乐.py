# coding=UTF-8
import json
import re
import sys
import time
import urllib

import requests
from bs4 import BeautifulSoup

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
        sql = "select 原始姓名  from Table_Spider where id>={0} and 虾米_URL is null".format(num)
        list = dbDAL.query(sql)
        resultList=[]
        for (name,) in list:
            obj = _getUrl(name, True)
            if obj is not None:
                print "{0},url={1}".format(name,obj["虾米_URL"]).decode("utf8")
                obj["原始姓名"]=name
                resultList.append(obj)
            else:
                print "{0},没有url".format(name)
        dbDAL.update(tableName="Table_Spider",list=resultList,whereTuple=("原始姓名",))
    except Exception as e:
        print "error"+e.message
    finally:
        dbDAL.dispose()

def _getUrl(name,isFirst):
    url = "http://www.xiami.com/ajax/search-index"
    sleepTime = random.randint(2, 5)
    time.sleep(sleepTime)
    parms = {"_": "1494903047880", "key": name}
    data = urllib.urlencode(parms)
    url = url + "?" + data
    try:
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        bsObj = BeautifulSoup(page.text, "html.parser")
    except:
        print "超时,1分钟后抓取，艺人：{0}".format(name)
        time.sleep(60)
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        bsObj = BeautifulSoup(page.text, "html.parser")

    domA = bsObj.findAll(name="a", attrs={"class": "artist_result"})
    if (len(domA) > 0):
        href = domA[0].attrs["href"]
       # print href
        return {"姓名": name, "虾米_URL": href}
    else:
        if isFirst and len(name.split("乐"))>1 :
            #在这里分割“乐”前面的字符
            return _getUrl(name.split("乐")[0], False)
        else :
            return None

def getData():
    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    sql = "select 姓名,虾米_URL  from Table_Spider where 虾米_URL is not null and id>={0}".format(num)
    list = dbDAL.query(sql)
    for (name, url) in list:
        sleepTime = random.randint(2, 5)
        time.sleep(sleepTime)
        sql2 = ""
        values = []
        try:

            page = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
            bsObj = BeautifulSoup(page.text, "html.parser")

            # 正则表达式先获取 id的变量名（有些起名叫"id",有些起名"object_id"）
            keys = re.findall(r"'id':(.+?),'type'", page.text)
            # 再根据上一步的变量名，正则匹配
            id = re.findall("var " + keys[0] + " = '(.+?)'", page.text)[0]

            # API地址
            _url = 'http://www.xiami.com/count/getplaycount'

            data = {'id': id, 'type': 'artist'}

            data = urllib.urlencode(data)

            _url2 = _url + '?' + data

            r = requests.get(_url2, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})

            responseJson = json.loads(r.text)
            values.append(responseJson["plays"])  # 试听

            lis = bsObj.find(name="div", attrs={"class": "music_counts"}).findAll(name="li")

            if (len(lis) == 3):
                print "{3},{0},{1},{2}".format(values[0], lis[1].get_text().split("粉丝")[0],
                                               lis[2].get_text().split("评论")[0], name);
                values.append(lis[1].get_text().split("粉丝")[0])  # 粉丝
                values.append(lis[2].get_text().split("评论")[0])  # 评论
            else:
                print "***意外:长度不够：{0},{1}".format(len(lis), name).decode("utf")
        except Exception as e:
            print e.message
            print "***超时 {0}".format(name).decode("utf8")
            sql2 = ""
        else:
            if len(values) == 3:
                sql2 = "update Table_Spider set 虾米_试听数='{0}',虾米_粉丝数='{1}',虾米_评论数='{2}' where 姓名='{3}'".format(values[0],
                                                                                                              values[1],
                                                                                                              values[2],
                                                                                                             name)
                try:
                    dbDAL.execute(sql2)
                except Exception as e:
                    print sql2

    dbDAL.dispose()

if __name__=="__main__":
    main()