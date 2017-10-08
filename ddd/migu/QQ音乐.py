# coding=UTF-8
import json
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

num =  global_Vars.startRowNum  #从第几行开始


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
        sql = "select 原始姓名  from Table_Spider where id>={0} and QQ音乐_URL is null".format(num)
        list = dbDAL.query(sql)
        resultList=[]
        for (name,) in list:
            obj = _getUrl(name, True)
            if obj is not None:
                print "{0},url={1}".format(name,obj["QQ音乐_URL"]).decode("utf8")
                obj["原始姓名"]=name
                resultList.append(obj)
            else:
                print "{0},没有url".format(name).decode("utf8")
        dbDAL.update(tableName="Table_Spider",list=resultList,whereTuple=("原始姓名",))
    except Exception as e:
        print "error"+e.message
    finally:
        dbDAL.dispose()

def _getUrl(name,isFirst):
    url = "https://c.y.qq.com/splcloud/fcgi-bin/smartbox_new.fcg"
    sleepTime = random.randint(2, 5)
    time.sleep(sleepTime)
    parms = {"format":"jsonp", "g_tk":"5381", "hostUin": "0","inCharset":"utf8","is_xml":"0","loginUin":"0","needNewCode":"0","notice":"0","outCharset":"utf-8","platform":"yqq"}
    parms["key"]=name
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
        mid=j["data"]["singer"]["itemlist"][0]["mid"];
        href="https://y.qq.com/n/yqq/singer/{0}.html".format(mid)
        return {"姓名": name, "QQ音乐_URL": href ,"QQ音乐_MID":mid}
    except:
        if isFirst and len(name.split("乐"))>1 :
            #在这里分割“乐”前面的字符
            return _getUrl(name.split("乐")[0], False)
        else :
            return None

def getData():
    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    sql = "select 姓名,QQ音乐_URL,QQ音乐_MID  from Table_Spider where QQ音乐_URL is not null and id>={0}".format(num)
    list = dbDAL.query(sql)
    updateList=[]
    for (name, url,mid) in list:
        sleepTime = random.randint(2, 5)
        time.sleep(sleepTime)
        sql2 = ""
        values = []
        try:
            obj={}
            page = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
            bsObj = BeautifulSoup(page.text, "html.parser")
            nodes=bsObj.findAll(name="strong",attrs={"class":"data_statistic__number"})
            # 正则表达式先获取 id的变量名（有些起名叫"id",有些起名"object_id"）
            if len(nodes)==3:
                obj["QQ音乐_单曲数"] = nodes[0].get_text()
                obj["QQ音乐_专辑数"] = nodes[1].get_text()
                obj["QQ音乐_MV数"] = nodes[2].get_text()
            # 再根据上一步的变量名，正则匹配


            # API地址
            url = 'https://c.y.qq.com/rsc/fcgi-bin/fcg_get_singer_fan_num.fcg?g_tk=5381&hostUin=0&format=jsonp&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0&cid=205361944&reqtype=1&singermid='+mid


            # data = urllib.urlencode(data)



            r = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})

            responseJson = json.loads(r.text)
            obj["QQ音乐_粉丝数"]=responseJson["data"]["music_num"]
            obj["QQ音乐_腾讯微博粉丝"] = responseJson["data"]["blog_num"]

            if obj.has_key("QQ音乐_粉丝数"):
                print ""
                updateList.append(obj)
                obj["姓名"]=name
                print "{0},粉丝：{1}".format(obj["姓名"],obj["QQ音乐_粉丝数"]).decode("utf8")
            else:
                print "***意外:"+obj
        except Exception as e:
            print e.message
            print "***超时 {0}".format(name).decode("utf8")


    dbDAL.update(tableName="Table_Spider",list=updateList,whereTuple={"姓名",})

    dbDAL.dispose()

if __name__=="__main__":
    main()