# coding=UTF-8
import re
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

num = global_Vars.startRowNum  #从第几行开始


def main():

    # 第一步，抓取艺人的最后url,入库
    print "开始获取每个艺人百度贴吧粉丝数........"
    getData()





def getData():
    try:

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        sql = "select 原始姓名  from Table_Spider where id>={0} and 百度贴吧_URL is null".format(num)
        list = dbDAL.query(sql)
        resultList=[]
        for (name,) in list:
            obj = _getData(name, True)
            if obj is not None:
                fans=0;
                if obj.has_key("百度贴吧_粉丝数"):
                    fans=obj["百度贴吧_粉丝数"]
                print "{0},百度贴吧_粉丝数={1}".format(name,fans).decode("utf8")
                obj["原始姓名"]=name
                resultList.append(obj)
            else:
                print "{0},没有url".format(name)
        dbDAL.update(tableName="Table_Spider",list=resultList,whereTuple=("原始姓名",))
    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()

def _getData(name,isFirst):
    url = "http://tieba.baidu.com/f"
    sleepTime = random.randint(2, 5)
    time.sleep(sleepTime)
    parms = {"ie":"utf-8", "fr":"search"}
    parms["kw"]=name
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
        print bsObj.text
    try:
        pass
        obj = {}
        obj["百度贴吧_URL"] = url
        # 用正则匹配字符串
        keys = re.findall(r" 'memberNumber': '(.+?)'", page.text)
        if len(keys)>=1:
            obj["百度贴吧_粉丝数"] = keys[0]


        return obj

    except:
        if isFirst and len(name.split("乐"))>1 :
            #在这里分割“乐”前面的字符
            return _getData(name.split("乐")[0], False)
        else :
            return None



if __name__=="__main__":
    main()