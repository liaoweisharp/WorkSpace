# coding=UTF-8
import sys
import traceback

import requests
import time

from logger import logger
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json
import urllib
import random

sys.path.append("..")
import DataBase.DatabaseDAL
import Comm.Funs
import global_Vars
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
errList=[]
def main():

        ##需要改数据库名

        print "   开始抓URL......."
        getURL()




def getURL():
        #http://cydj.5anquan.com/UILogin/BeforeUserInfoSearch
        _url = 'http://cydj.5anquan.com/UILogin/UserInfoSearchResult'
        returnValue=[]

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)
        sql = "select bxc_Code,bxc_PreCompanyName  from Tab_BX_Company where bxc_PreCompanyName is not null order by bxc_Id"
        list = dbDAL.query(sql)

        try:
            time.sleep(random.randint(2, 5))
            para={"ddlItem":"3","hidId":"0","pageSize":"1000","pageIndex":"1"}

            num=0
            while num<len(list):
                (bxc_Code,bxc_ComanyName)=list[num]
                para["txtStr"] = bxc_ComanyName
                ram=random.randint(2, 7)
                time.sleep(ram)

                data = urllib.urlencode(para)
                url = _url + "?" + data
                try:
                    r = requests.get(url,headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/53{0}.{0}".format(ram)})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                    # print r.text
                except Exception as e:
                    print e.message
                    print "***超时，等待10分钟,{0}".decode("utf8")
                    time.sleep(600)
                    try:
                        r = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                        bsObj = BeautifulSoup(r.text, "html.parser")
                    except Exception as e:
                        print e.message
                        print "***再超时".decode("utf8")
                nodeTable = bsObj.find(name="table", attrs={"class": "modifyNewsTab"})
                if nodeTable is None:
                    print  "**空对象".decode("utf8")
                    time.sleep(20)
                    num += 1
                    continue
                trs = nodeTable.findAll(name="tr")
                if len(trs) <=1:
                    logger.info("没有数据。公司：{0}".format(bxc_ComanyName))

                elif len(trs) > 0:
                    objList=[]
                    for tr in trs[1:]:
                        obj={"company_Code":bxc_Code}
                        try:
                            nodeTds=tr.findAll(name="td")
                            if len(nodeTds)==4:
                                # 姓名
                                nodeA=nodeTds[0].find(name="a")
                                if nodeA is not None:
                                    obj["userName"]=nodeA.get_text()
                                    obj["url"]=nodeA.attrs["href"]
                                # 证书编号
                                obj["zhengShuBianHao"] = nodeTds[2].get_text()
                                # 资格等级
                                obj["dengJi"] = nodeTds[3].get_text()


                                print "公司：{0}, {1},{2}".format(bxc_ComanyName,obj["userName"],obj["dengJi"])
                        except:
                            traceback.print_exc()
                        else:
                            objList.append(obj)
                    dbDAL.insert(tableName="Tab_BX_LiuShui_AnQuanPingJiaShi", list=objList)
                    objList=[]


                num+=1

        except:
            print "*** 报错:{0}"
            traceback.print_exc()
        return returnValue






if __name__=="__main__":
    main()