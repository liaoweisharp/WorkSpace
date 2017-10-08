# coding=UTF-8
import json
import re
import sys
import time
import traceback
import urllib

import requests
from bs4 import BeautifulSoup
from pip import logger

import DataBase.DatabaseDAL_Oracle
import logger
import random
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
app_Id=3 #appId  虾米
pageSize=20
#得到数据
def getOneSong(obj):
    returnValue=[]

    pageObj={"totalNum":20,"p":1,"n":pageSize,"obj":obj}
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
        sleepTime = random.randint(2, 6)
        time.sleep(sleepTime)
        _url = "http://www.xiami.com/search/song/page/"


        songName=pageObj["obj"][0]  #歌曲
        singer = pageObj["obj"][1]  #歌手
        id = pageObj["obj"][2]  #歌曲ID

        curentPage = pageObj["p"]
        parms = {"category": "-1", "key": songName}
        data = urllib.urlencode(parms)
        url = _url + str(curentPage)+"?"+ data
        j=None
        try:
            page = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3{0} (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.3{0}".format(sleepTime)})
            bsObj = BeautifulSoup(page.text, "html.parser")
        except:
            traceback.print_exc()
            print "*** URL GET出错 歌曲：{0},歌手:{1}".format(songName,singer).decode("utf8","ignore")
            sleepTime = random.randint(5, 10)
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

#获得页面数据
def getJsonData(pageObj,bsObj):

    returnValue=[]
    try:
        songName = pageObj["obj"][0]  # 歌曲
        singerName = pageObj["obj"][1]  # 歌手
        id = pageObj["obj"][2]  # id

        nodeTable=bsObj.find(name="table",attrs={"class","track_list"})
        if nodeTable is None:
            # 搜索没有记录
            return returnValue
        nodeTbody=nodeTable.find(name="tbody")
        if nodeTbody is None:
            return returnValue
        nodeTrs=nodeTbody.findAll(name="tr")
        if nodeTrs is None or len(nodeTrs)==0:
            return returnValue
        for tr in nodeTrs:
            obj={"id":"SEED_Tab_Phone_Songs_Keys3","song_Id":id,"app_Id":app_Id,"load_Date":time.strftime('%Y%m%d',time.localtime(time.time()))}

            # 歌手
            td_Singer=tr.find(name="td",attrs={"class":"song_artist"})
            if td_Singer is None:
                continue
            _singer =td_Singer.get_text().strip()
            if singerName.lower() not in _singer.lower() and _singer.lower() not in singerName.lower():
                ## 不是指定歌手则跳过
                continue
            obj["singer_Name"]=_singer

            # key
            td_Singer = tr.find(name="td", attrs={"class": "song_act"})
            if td_Singer is None:
                continue
            nodeAs = td_Singer.findAll(name="a")
            nodeA=None
            for a in nodeAs:
                if a.attrs.has_key("onclick"):
                    nodeA=a
                    break
            if nodeA is not None:
                strClick=nodeA.attrs["onclick"]
                arr=strClick.split(",")
                if len(arr)>0:
                    arr=arr[0].split("(")
                    if len(arr)>1:
                        _id=arr[1].replace("'","")
                        obj["keys"]=_id.strip()
            # 歌名
            td_songName = tr.find(name="td", attrs={"class": "song_name"})
            if td_songName is None:
                continue
            nodeA = td_songName.find(name="a")
            if nodeA is None:
                _songName = nodeA.get_text().strip()
            else:
                _songName = nodeA.attrs["title"].strip()
            obj["song_Name"]=_songName
            # 专辑
            td_album = tr.find(name="td", attrs={"class": "song_album"})
            if td_album is None:
                continue
            nodeA = td_album.find(name="a")
            if nodeA is None:
                _album = nodeA.get_text().strip()
            else:
                _album = nodeA.attrs["title"].strip()
            obj["des"] = _album


            returnValue.append(obj)
        nodeP=bsObj.find(name="p",attrs={"class":"seek_counts"})
        if nodeP is not None:
            nodeB=nodeP.find(name="b")
            if nodeB is not None:
                try:
                    # 总页码
                    num=int(nodeB.get_text())
                except:
                    pass
                else:
                    pageObj["totalNum"]=num
    except Exception, e:
        logger.error(e)
    finally:
        return returnValue;

def fun_Print(list,obj,length,total):
    for item in list:
        print "len={4}/{5},唯一标识：{2}，歌名={0}，歌手={1}，专辑={3}".format(obj[0],obj[1],item["keys"],item["des"],total,length).decode("utf8","ignore")
def db(dbDAL,objList):
    dbDAL.insert(tableName="Tab_Phone_Songs_Keys3", list=objList,sequenceList=["id"])
def main():
    dbDAL = DataBase.DatabaseDAL_Oracle.DatabaseDAL()
    sql = "select song_Name,singer,id  from Tab_Phone_Songs3 a where rownum=1 and lock1 is null and  song_Name is not null order by id"
    list = dbDAL.query(sql)
    num=0


    while len(list)==1:

        obj=list[0]
        id=obj[2]
        updateList=[]
        _obj={"id":id,"lock1":"1"}
        updateList.append(_obj)
        dbDAL.update(tableName="Tab_Phone_Songs3", list=updateList, whereTuple={"id", })

        _list=getOneSong(obj)
        fun_Print(_list, obj,len(list),num+1)
        db(dbDAL, _list)
        num+=1

        list = dbDAL.query(sql)

if __name__=="__main__":
    main()