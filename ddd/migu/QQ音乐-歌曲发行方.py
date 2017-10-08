# coding=UTF-8
import json
import sys
import time
import traceback
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
    print "开始获取每个歌曲最后的url........".decode("utf8")
    getUrl()

    # 第二步，根据上一步的url，抓取发行方
    print "\n开始抓取发行方.......".decode("utf8")
    getData()




def getUrl():
    try:

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        sql = "select 原始姓名,QQ音乐发行方_歌曲名称  from Table_Spider where id>={0} and QQ音乐发行方_专辑ID is null".format(num)
        list = dbDAL.query(sql)
        resultList=[]
        for (name,songName) in list:
            obj = _getUrl(name, songName,True)
            if obj is not None:
                print "{0},专辑ID={1}".format(name,obj["QQ音乐发行方_专辑ID"]).decode("utf8")
                obj["原始姓名"]=name
                resultList.append(obj)
            else:
                print "{0},专辑ID".format(name).decode("utf8")
        dbDAL.update(tableName="Table_Spider",list=resultList,whereTuple=("原始姓名",))
    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()

def _getUrl(singerName,songName,isFirst):
    url = "https://c.y.qq.com/soso/fcgi-bin/client_search_cp"
    sleepTime = random.randint(2, 5)
    time.sleep(sleepTime)
    parms = {"ct":"24", "qqmusic_ver":"1298", "new_json": "1","remoteplace":"txt.yqq.center","searchid":"38813207194487968","t":"0","aggr":"1","cr":"1","catZhida":"1","lossless":"0","flag_qc":"0","p":"1","n":"100","g_tk":"5381","loginUin":"0","hostUin":"0","format":"json","inCharset":"utf8","outCharset":"utf-8","notice":"0","platform":"yqq","needNewCode":"0"}
    parms["w"]=songName
    data = urllib.urlencode(parms)
    url = url + "?" + data
    try:
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        j = json.loads(page.text)
    except:
        print "超时,1分钟后抓取，艺人：{0}".format(singerName)
        time.sleep(60)
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        j = json.loads(page.text)

    try:
        pass
        for song in j["data"]["song"]["list"]:
            singerList=[]
            mid=""
            for singer in song["singer"]:
                singerList.append(singer["name"])
            if singerName in singerList:
                mid=song["album"]["mid"]
                break
            isBreak=False
            for _singer in singerList:
                if singerName.lower() in _singer.lower() or _singer.lower() in singerName.lower():
                    # 如果包含字符串
                    mid = song["album"]["mid"]
                    isBreak=True #跳出外面的循环
                    break
            if isBreak:
                break
        return {"姓名": singerName, "QQ音乐发行方_专辑ID":mid}
    except:
        if isFirst and len(singerName.split("乐"))>1 :
            #在这里分割“乐”前面的字符
            return _getUrl(singerName.split("乐")[0], False)
        else :
            return None

def getData():
    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    sql = "select 原始姓名,QQ音乐发行方_专辑ID,QQ音乐发行方_歌曲名称 from Table_Spider where QQ音乐发行方 is null and id>={0}".format(num)
    list = dbDAL.query(sql)
    updateList=[]
    _url="https://c.y.qq.com/v8/fcg-bin/fcg_v8_album_info_cp.fcg"
    parms = {"format": "json", "g_tk": "5381", "hostUin": "0", "inCharset": "utf8",
             "loginUin": "0", "needNewCode": "0", "notice": "0", "outCharset": "utf-8", "platform": "yqq"}


    for (name, mid,songName) in list:
        sleepTime = random.randint(2, 5)
        parms["albummid"] = mid
        data = urllib.urlencode(parms)
        url = _url + "?" + data
        time.sleep(sleepTime)
        sql2 = ""
        values = []

        try:
            obj={}
            page = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
            company=""
            j = json.loads(page.text)

            company=j["data"]["company"]
            obj["QQ音乐发行方"]=company
            obj["原始姓名"]=name
            obj["QQ音乐发行方_歌曲名称"]=songName

            updateList.append(obj)

            print "{0},歌曲名：{1},发行公司:{2}".format(obj["原始姓名"],obj["QQ音乐发行方_歌曲名称"],obj["QQ音乐发行方"]).decode("utf8")
        except Exception as e:
            traceback.print_exc()
            print "***超时 {0}".format(name).decode("utf8")


    dbDAL.update(tableName="Table_Spider",list=updateList,whereTuple={"原始姓名","QQ音乐发行方_歌曲名称"})

    dbDAL.dispose()

if __name__=="__main__":
    main()