# coding=UTF-8
import json
import sys
import time

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
    print "开始获取每个艺人百度百科专辑数和获奖数量........"
    getData()



def getData():
    try:

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        sql = "select 原始姓名  from Table_Spider where id>={0} and 百度百科_URL is null".format(num)
        list = dbDAL.query(sql)
        resultList=[]
        for (name,) in list:
            obj = _getData(name, True)
            if obj is not None:
                print "{0},百度百科_获奖数={1},百度百科_专辑数={2}".format(name,obj["百度百科_获奖数"],obj["百度百科_专辑数"]).decode("utf8")
                obj["原始姓名"]=name
                resultList.append(obj)
            else:
                print "{0},没有url".format(name)
        dbDAL.update(tableName="Table_Spider",list=resultList,whereTuple=("原始姓名",))
    except Exception as e:
        print "error"+e.message
    finally:
        dbDAL.dispose()

def _getData(name,isFirst):
    url = "http://baike.baidu.com/item/"+name
    sleepTime = random.randint(2, 5)
    time.sleep(sleepTime)
    try:
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        bsObj = BeautifulSoup(page.text, "html.parser")

    except:
        print "超时,1分钟后抓取，艺人：{0}".format(name)
        time.sleep(60)
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        j = json.loads(page.text)

    try:
        pass
        tds=bsObj.findAll(name="td",attrs={"class":"submodule","colspan":"1"})
        obj = {}
        obj["百度百科_URL"] = url
        obj["百度百科_获奖数"] = 0
        obj["百度百科_专辑数"] = 0
        if tds is not None and len(tds)>0:
            for td in tds:
                nodes_HuoJiang = td.findAll(name="li", attrs={"class": "row"})  ##获奖数量
                obj["百度百科_获奖数"] += len(nodes_HuoJiang)


        nodes_ZhuanJi = bsObj.findAll(attrs={"class": "album-item"})  ##专辑数量
        if nodes_ZhuanJi is not None or len(nodes_ZhuanJi) > 0:
            obj["百度百科_专辑数"] = len(nodes_ZhuanJi)

        return obj

    except:
        if isFirst and len(name.split("乐"))>1 :
            #在这里分割“乐”前面的字符
            return _getData(name.split("乐")[0], False)
        else :
            return None



if __name__=="__main__":
    main()