# coding=UTF-8
import json
import sys
import time
import traceback
import urllib

import requests
from bs4 import BeautifulSoup
from logger import logger

sys.path.append("../..")
import DataBase.DatabaseDAL
import random
import global_Vars
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
app_Id=1 #appId  QQ
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
        _url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp?ct=24&qqmusic_ver=1298&new_json=1&remoteplace=txt.yqq.center&searchid=36662154408878938&t=0&aggr=1&cr=1&catZhida=1&lossless=0&flag_qc=0&g_tk=5381&loginUin=0&hostUin=0&format=json&inCharset=utf8&outCharset=utf-8&notice=0&platform=yqq&needNewCode=0"

        parms = {"p": pageObj["p"], "n": pageObj["n"]}
        songName=pageObj["obj"][0]  #歌曲
        singer = pageObj["obj"][1]  #歌手
        id = pageObj["obj"][2]      # 歌曲ID
        parms["w"] = songName
        data = urllib.urlencode(parms)
        url = _url +"&"+ data
        j=None
        try:
            page = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3{0} (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.3{0}".format(sleepTime)})
            j = json.loads(page.text)
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
            j = json.loads(page.text)
        if j is None:
            return None
        else:
            return getJsonData(pageObj,j)

        #下面开始获得数据
    except:
        traceback.print_exc()
        print "*** 出错 歌曲：{0},歌手:{1}".format(songName, singer).decode("utf8","ignore")
        return None

def getJsonData(pageObj,json):

    returnValue=[]
    songName=pageObj["obj"][0]  #歌曲
    singerName = pageObj["obj"][1]  # 歌手
    id = pageObj["obj"][2]  # id
    try:
        for item in json["data"]["song"]["list"]:
            try:
                obj={}
                for singer in item["singer"]:
                    _singer=singer["name"]
                    isSinger=False #是否是目标歌手
                    if singerName.lower() in _singer.lower() or _singer.lower() in singerName.lower():
                        isSinger=True
                        obj["singer_Name"] = _singer
                        break
                if isSinger==False:
                    # 不是目标歌手则继续查找下一首歌
                    continue
                zhaunJiName=item["album"]["name"]  #专辑名
                keys=item["file"]["media_mid"]       #唯一标识
                title=item["title"]                #显示的歌曲名
                returnValue.append(obj)
                obj["song_Id"]=id
                obj["app_Id"]=app_Id

                obj["keys"] = keys  #唯一标识
                obj["song_Name"] = title
                obj["des"] = zhaunJiName
                obj["load_Date"]=time.strftime('%Y%m%d',time.localtime(time.time()))
            except:
                traceback.print_exc()
                continue
        pageObj["totalNum"] = json["data"]["song"]["totalnum"]  # 得到歌曲总数，好判断爬取几页。
    except:
        pass
    finally:
        return returnValue;

def fun_Print(list,obj,length,total):
    for item in list:
        print "len={4}/{5},唯一标识：{2}，歌名={0}，歌手={1}，专辑={3}".format(obj[0],obj[1],item["keys"],item["des"],total,length).decode("utf8","ignore").encode("GBK", "ignore");


def db(dbDAL,objList):

    dbDAL.insert(tableName="Tab_Phone_Songs_Keys", list=objList)

def main():
    resultValue=[]
    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    sql = "select top 1 song_Name,singer,id  from Tab_Phone_Songs a where app_1 is null and song_Name is not null and id>(select max(song_Id) from Tab_Phone_Songs_Keys b where  b.app_id={0})  order by id".format(app_Id)
    list = dbDAL.query(sql)
    num=0


    while len(list)==1:

        obj=list[0]
        id=obj[2]
        updateList=[]
        _obj={"id":id,"app_1":"1"}
        updateList.append(_obj)
        dbDAL.update(tableName="Tab_Phone_Songs", list=updateList, whereTuple={"id", })

        _list=getOneSong(obj)
        fun_Print(_list, obj,len(list),num+1)
        db(dbDAL, _list)
        num+=1
        list = dbDAL.query(sql)

if __name__=="__main__":
    main()