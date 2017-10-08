# coding=UTF-8
import sys
import traceback

import requests
import time
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

        list = dbDAL.query("SELECT bxu_code,bxu_name FROM dbo.Tab_BX_User WHERE bxu_ShenFenZheng IS null")

        url = 'https://www.sczbbx.com/Performance/PerformanceEmployee.aspx'

        num=0
        objList=[]
        for (bxu_code,bxu_name) in list:
            time.sleep(random.randint(1,4))
            try:
                r = requests.get(url+"?EmployeeId="+bxu_code,verify=False, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                traceback.print_exc()
                print "超时，等待30秒,User_Code={0}".format(bxu_code).decode("utf8")
                time.sleep(30)
                try:
                    r = requests.get(url + "?EmployeeId=" + bxu_code,verify=False, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    traceback.print_exc()
                    print "再超时，跳过，User_Code={0}".format(bxu_code).decode("utf8")
                    continue

            label =bsObj.find(id="ContentPlaceHolder1_ContentPlaceHolder2_UCPerformanceList1_lbTitle")
            if label is None:
                print "没有label节点，跳过bxu_code={0}".format(bxu_code).decode("utf8")
                continue

            str=label.get_text()
            shenFenZhengHao=str.split("身份证号：")[1].split("业绩")[0].strip()
            obj={}
            obj["bxu_ShenFenZheng"]=shenFenZhengHao
            obj["bxu_Code"] = bxu_code
            objList.append(obj)
            print "len={3},user_Code={0},userName={1},身份证号={2}".format(obj["bxu_Code"],bxu_name,obj["bxu_ShenFenZheng"],num*10+len(objList)).decode("utf8")
            ## 再插入数据表
            if len(objList)==10:

                dbDAL.update(tableName="Tab_BX_User", list=objList, whereTuple=("bxu_Code",))
                objList=[]
                num +=1
        #剩下的继续更新
        dbDAL.update(tableName="Tab_BX_User", list=objList, whereTuple=("bxu_Code",))
    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()



if __name__=="__main__":
    main()