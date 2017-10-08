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
app_Id=4 #appId  酷狗
pageSize=30
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
        sleepTime = random.randint(2, 6)
        time.sleep(sleepTime)
        _url = "http://songsearch.kugou.com/song_search_v2?userid=-1&clientver=&platform=WebFilter&tag=em&filter=2&iscorrection=1&privilege_filter=0&_=1505701594132"

        parms = {"page": pageObj["p"], "pagesize": pageObj["n"]}
        songName=pageObj["obj"][0]  #歌曲
        singer = pageObj["obj"][1]  #歌手
        id = pageObj["obj"][2]      # 歌曲ID
        parms["keyword"] = songName
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
        for item in json["data"]["lists"]:
            try:
                obj={}
                #歌手
                _singer=item["SingerName"]
                fileHash=item["FileHash"]
                extName = item["ExtName"]
                if singerName.lower() not in _singer.lower() and _singer.lower() not in singerName.lower():
                    # 不是目标歌手则继续查找下一首歌
                    continue

                zhaunJiName=item["AlbumName"]  #专辑名
                title=item["FileName"]         #显示的歌曲名
                returnValue.append(obj)
                obj["singer_Name"] = _singer
                obj["song_Id"]=id
                obj["app_Id"]=app_Id
                obj["song_Name"] = title
                obj["des"] = zhaunJiName
                obj["temp1"] = fileHash
                obj["temp2"] = extName
                obj["load_Date"]=time.strftime('%Y%m%d',time.localtime(time.time()))
            except:
                traceback.print_exc()
                continue
        pageObj["totalNum"] = json["data"]["total"]  # 得到歌曲总数，好判断爬取几页。
    except:
        traceback.print_exc()
    finally:
        return returnValue;

def fun_Print(list,obj,length,total):
    for item in list:
        print "len={3}/{4},过程id={5},歌名={0}，歌手={1}，专辑={2}".format(obj[0], obj[1], item["des"], total, length,item["temp1"]).decode("utf8","ignore").encode("GBK", "ignore");

#入库
def db(dbDAL,objList):

    dbDAL.insert(tableName="Tab_Phone_Songs_Keys4", list=objList)

def step1():
    resultValue = []
    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    # sql = "select top 1 song_Name,singer,id  from Tab_Phone_Songs a where app_4 is null and song_Name is not null and id>(select max(song_Id) from Tab_Phone_Songs_Keys4 b where  b.app_id={0})  order by id".format(
    #     app_Id)
    # 这里需要还原
    sql = "select top 1 song_Name,singer,id  from Tab_Phone_Songs a where app_4 is null  order by id"
    list = dbDAL.query(sql)
    num = 0

    while len(list)==1:

        obj=list[0]
        id=obj[2]
        updateList=[]
        # 这里需要还原
        _obj={"id":id,"app_4":"2"}
        updateList.append(_obj)
        dbDAL.update(tableName="Tab_Phone_Songs", list=updateList, whereTuple={"id", })

        _list = getOneSong(obj)
        fun_Print(_list, obj,len(list),num+1)
        db(dbDAL, _list)
        num += 1

        list = dbDAL.query(sql)
def step2():
    try:

        while True:
            resultValue = []
            dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
            # sql = "select top 1 id  from Tab_Phone_Songs a where app_4_1 is null and song_Name is not null  order by id"
            #还原
            sql = "select top 1 id  from Tab_Phone_Songs a where app_4_1 is null and song_Name is not null and and app_4='2'  order by id"
            list = dbDAL.query(sql)
            if len(list) == 0:
                break
            if len(list) == 1:
                (id,) = list[0]
                updateList = []
                _obj = {"id": id, "app_4_1": "1"}
                updateList.append(_obj)
                dbDAL.update(tableName="Tab_Phone_Songs", list=updateList, whereTuple={"id", })

                #开始遍历 表：Tab_Phone_Songs_Keys4
                sql = "select id,temp1,song_Id  from Tab_Phone_Songs_Keys4 where song_Id={1} and temp1 is not null and keys is null and app_id={0}".format(app_Id,id)
                list = dbDAL.query(sql)
                num=0
                while num < len(list):
                    (id, hash,songId) = list[num]
                    sleepTime = random.randint(2, 6)
                    time.sleep(sleepTime)

                    _url="http://www.kugou.com/yy/index.php?r=play/getdata&hash="
                    try:
                        url=_url+hash
                        page = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.3{0} (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.3{0}".format(
                                sleepTime)})
                        j = json.loads(page.text)
                        playUrl=j["data"]["play_url"]
                        arr=playUrl.split("/")
                        if len(arr)>0:
                            keys=arr[len(arr)-1]
                            obj = {"id": id}
                            obj["keys"]=keys.strip()
                            resultValue.append(obj)
                            logger.info("keys={0},id={1}".format(obj["keys"],obj["id"]))
                            # if len(resultValue) % 5==0:
                            #
                            #     status=dbDAL.update(tableName="Tab_Phone_Songs_Keys4", list=resultValue, whereTuple={"id", })
                            #
                            #     if status==-1:
                            #         print "*" * 30
                            #         for ins in resultValue:
                            #             print "id={0},keys={1},len={2}".format(ins["id"],ins["keys"],len(ins["keys"]))
                            #         print "*" * 30
                            #         return
                            #     resultValue=[]
                    except Exception, e:
                        logger.error(e)
                    finally:
                        num +=1

                    list = dbDAL.query(sql)

                dbDAL.update(tableName="Tab_Phone_Songs_Keys4", list=resultValue, whereTuple={"id", })

    except Exception, e:
        logger.error(e)
    finally:
        dbDAL.dispose()

def main():
    logger.info("开始获得中间id....".decode("utf8","ignore"))
    step1()
    logger.info("开始获得key.......".decode("utf8","ignore"))
    step2()

if __name__=="__main__":
    main()