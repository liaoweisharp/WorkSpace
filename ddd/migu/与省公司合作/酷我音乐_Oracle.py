# coding=UTF-8
import json
import sys
import time
import traceback
import urllib

import requests
from bs4 import BeautifulSoup
from logger import logger

import DataBase.DatabaseDAL_Oracle
import random
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
app_Id=5 #appId  QQ
pageSize=25
#得到数据
def getOneSong(obj):
    returnValue=[]

    pageObj={"totalNum":pageSize,"p":1,"n":pageSize,"obj":obj}
    while pageObj["p"]<=5 and pageObj["p"]-1 * pageObj["n"] < pageObj["totalNum"]:
        _list = getOnePage(pageObj)
        if _list is not None and len(_list)>0:

            returnValue.extend(_list)
            ## 打印
        pageObj["p"]+=1
    return returnValue

#爬取一页数据
def getOnePage(pageObj):
    try:
        sleepTime = random.randint(2,5)
        time.sleep(sleepTime)
        _url = "http://sou.kuwo.cn/ws/NSearch?type=music&catalog=yueku2016"
        parms = {}
        songName=pageObj["obj"][0]  #歌曲
        singer = pageObj["obj"][1]  #歌手
        id = pageObj["obj"][2]      # 歌曲ID
        parms["key"] = songName
        parms["pn"] = pageObj["p"]
        data = urllib.urlencode(parms)
        url = _url +"&"+ data
        try:
            page = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3{0} (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.3{0}".format(sleepTime)})
            bsObj = BeautifulSoup(page.text, "html.parser")
        except:
            traceback.print_exc()
            print "*** URL GET出错 歌曲：{0},歌手:{1}".format(songName,singer).decode("utf8","ignore")
            sleepTime = random.randint(5, 8)
            time.sleep(sleepTime)
            try:
                page = requests.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3{0} (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.3{0}".format(
                        sleepTime)})
            except:
                traceback.print_exc()
                logger.error("**  URL GET出错再次失败，跳过歌曲，歌曲:{0},歌手:{1},id:{2}".format(songName,singer,id))
                return None
            bsObj = BeautifulSoup(page.text, "html.parser")
        if bsObj is None:
            return None
        else:
            return getJsonData(pageObj,bsObj)

        #下面开始获得数据
    except:
        traceback.print_exc()
        print "*** 出错 歌曲：{0},歌手:{1}".format(songName, singer).decode("utf8","ignore")
        return None

def getJsonData(pageObj,bsObj):
    returnValue = []
    try:
        songName = pageObj["obj"][0]  # 歌曲
        singerName = pageObj["obj"][1]  # 歌手
        id = pageObj["obj"][2]  # id

        noNode=bsObj.find(name="p",attrs={"class":"nosearch"})
        if noNode is not None:
            #  # 搜索没有记录
            return returnValue
        listNodes=bsObj.find(name="div",attrs={"class":"m_list"})
        if listNodes is None:
            return returnValue
        spanNode=listNodes.find(name="span")
        if spanNode is None:
            return returnValue
        pageObj["totalNum"]=int(spanNode.get_text())

        divNode=bsObj.find(name="div",attrs={"class","list"})
        if divNode is None:
            return returnValue
        liNodes=divNode.findAll(name="li",attrs={"class":"clearfix"})
        if liNodes is None or len(liNodes)==0:
            return returnValue
        for li in liNodes:
            try:
                obj={"id":"SEED_Tab_Phone_Songs_Keys5","song_Id":id,"app_Id":app_Id,"song_Name":"","singer_Name":"","des":"","load_Date":""}
                obj["load_Date"]=time.strftime('%Y%m%d', time.localtime(time.time()))
                # 歌手名
                p = li.find(name="p", attrs={"class": "s_name"})
                if p is None:
                    continue
                a = p.find(name="a")
                if a is not None:
                    _singer = a.attrs["title"]
                    if singerName.lower() not in _singer.lower() and _singer.lower() not in singerName.lower():
                        continue
                    obj["singer_Name"]=_singer
                else:
                    continue

                # mid
                input=li.find(name="input",attrs={"name":"musicNum"})
                if input is None:
                    continue
                mid=input.attrs["value"]
                obj["temp1"]=mid
                #歌曲名
                p = li.find(name="p", attrs={"class": "m_name"})
                if p is None:
                    continue
                a = p.find(name="a")
                if a is not None:
                    _songName = a.attrs["title"]
                    obj["song_Name"] = _songName
                # 专辑名
                p = li.find(name="p", attrs={"class": "a_name"})
                if p is None:
                    continue
                a = p.find(name="a")
                if a is not None:
                    obj["des"]=a.attrs["title"]


            except Exception,e:
                logger.error(e)
                continue
            else:
                returnValue.append(obj)


    except Exception, e:
        logger.error(e)
    finally:
        return returnValue;


def fun_Print(list,obj,length,total):

    for item in list:
        print "len={3}/{4},过程id={5},歌名={0}，歌手={1}，专辑={2}".format(obj[0],obj[1],item["des"],total,length,item["temp1"]).decode("utf8","ignore")

#入库
def db(dbDAL,objList):

    dbDAL.insert(tableName="Tab_Phone_Songs_Keys5", list=objList,sequenceList=["id"])

def step1():
    resultValue = []
    dbDAL = DataBase.DatabaseDAL_Oracle.DatabaseDAL()
    sql="select song_Name,singer,id  from Tab_Phone_Songs5 a where rownum=1 and lock1 is null and song_Name is not null  order by id"
    list = dbDAL.query(sql)
    num = 0

    while len(list)==1:

        obj=list[0]
        id=obj[2]
        updateList=[]
        _obj = {"id": id, "lock1": "1"}
        updateList.append(_obj)
        dbDAL.update(tableName="Tab_Phone_Songs5", list=updateList, whereTuple={"id", })
        _list = getOneSong(obj)
        fun_Print(_list, obj,len(list),num+1)
        db(dbDAL, _list)
        num += 1

        list = dbDAL.query(sql)
def step2():

    try:
        while True:
            try:
                resultValue = []
                dbDAL = DataBase.DatabaseDAL_Oracle.DatabaseDAL()
                sql = "select  id  from Tab_Phone_Songs5 a where rownum=1 and  lock2 is null and song_Name is not null  order by id"

                list = dbDAL.query(sql)
                if len(list) == 0:
                    break
                if len(list) == 1:
                    (id,) = list[0]
                    updateList = []
                    _obj = {"id": id, "lock2": "1"}
                    updateList.append(_obj)
                    dbDAL.update(tableName="Tab_Phone_Songs5", list=updateList, whereTuple={"id", })

                    #开始遍历 表：Tab_Phone_Songs_Keys5
                    sql = "select id,temp1,song_Id  from Tab_Phone_Songs_Keys5 where song_Id={0} and temp1 is not null and keys is null".format(id)
                    list = dbDAL.query(sql)
                    num=0
                    while num < len(list):
                        (id, hash,songId) = list[num]
                        sleepTime = random.randint(2, 6)
                        time.sleep(sleepTime)
                        obj = {"id": id}
                        for i in range(1,3):
                            format=""
                            if i==1:
                                format="aac"
                            elif i==2:
                                format="mp3"
                            _url="http://antiserver.kuwo.cn/anti.s?type=convert_url"
                            try:
                                url=_url+"&format="+format+"&rid=MUSIC_"+str(hash)
                                page =None
                                try:
                                    page = requests.get(url, headers={
                                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3{0} (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.3{0}".format(
                                            sleepTime)})
                                except Exception,e:
                                    logger.error(e)
                                    time.sleep(random.randint(6, 10))
                                    try:
                                        page = requests.get(url, headers={
                                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3{0} (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.3{0}".format(
                                                sleepTime)})
                                    except  Exception,e:
                                        logger.error(e)
                                        logger.error("** get url异常，跳过。url={0}".format(url))
                                        num += 1
                                        continue

                                arr=page.text.split("/")
                                keys=arr[len(arr) - 1]
                                if i==1:
                                    obj["keys"] = keys
                                elif i==2:
                                    obj["keys2"] = keys
                            except  Exception, e:
                                logger.error(e)

                        resultValue.append(obj)
                        num +=1
                    dbDAL.update(tableName="Tab_Phone_Songs_Keys5", list=resultValue, whereTuple={"id", })
                    resultValue = []


            except Exception,e:
                logger.error(e)

    except Exception, e:
        logger.error(e)
    finally:
        dbDAL.dispose()

def main():
    logger.info("开始获得中间id....")
    step1()
    logger.info("开始获得key.......")
    step2()

if __name__=="__main__":
    main()