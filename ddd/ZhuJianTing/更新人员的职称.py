# coding=UTF-8
import sys
import traceback

import requests
import time
sys.path.append("..")
import Comm.Funs
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json
import urllib
import random

sys.path.append("..")
import DataBase.DatabaseDAL
import global_Vars

def main():

    try:
        ##需要改数据库名

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)
        list = dbDAL.query("SELECT user_Name,user_Code FROM Tab_BX_ZJT_LiuShui_User WHERE zhi_Cheng IS NULL order by company_Code desc,user_Code desc")
        userNum=1
        objList=[]
        while userNum<=len(list):
            ra=random.randint(5, 12)
            time.sleep(ra)
            (userName,userCode) = list[userNum - 1]
            url = 'http://xmgk.scjst.gov.cn/QueryInfo/Person/PersonInfo.aspx?id='+userCode
            try:
                r = requests.get(url,headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT {0}.1; WOW64) AppleWebKit/537.36{0} (KHTML, like Gecko) Chrome/54.0.2840.99{0} Safari/537.36{0}".format(ra)})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                traceback.print_exc()
                print "超时，等待1秒分钟".decode("utf8")
                time.sleep(60)
                try:
                    r = requests.get(url,  headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:54.0) Gecko/20100101 Firefox/54.0"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "再超时,重新获取".decode("utf8")
                    continue
            try:
                table = bsObj.find(name="table", attrs={"class", "list"})
                if table is None:
                    print "有验证码".decode("utf8")
                    time.sleep(random.randint(12, 25))
                    continue
                obj={}
                objList.append(obj)
                td = table.find(id="mainContent_ucPersonBaseInfo_lbl_zc")
                zhiCheng="" ##默认值
                obj["user_Code"] = userCode
                if td is not None:
                    zhiCheng=td.get_text().strip()
                obj["zhi_Cheng"]=zhiCheng
                print "len={2}/{3},{0},{1}".format(userCode,zhiCheng,userNum,len(list)).decode("utf8")
                if len(objList)%3==0:
                    print "入库中.......".decode("utf8")
                    dbDAL.update(tableName="Tab_BX_ZJT_LiuShui_User", list=objList, whereTuple=("user_Code",))
                    objList=[]
            except:
                traceback.print_exc()
            else:
                userNum += 1
        if len(objList)>0:
                dbDAL.update(tableName="Tab_BX_ZJT_LiuShui_User", list=objList, whereTuple=("user_Code",))
                objList=[]

    except:
        traceback.print_exc()
    finally:
        dbDAL.dispose()


if __name__=="__main__":
    main()