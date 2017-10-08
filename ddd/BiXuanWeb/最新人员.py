# coding=UTF-8
import sys
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

        list = dbDAL.query("SELECT bxc_Code,bxc_ComanyName FROM Tab_BX_Company")

        url = 'https://www.sczbbx.com/Performance/PerformanceCompany.aspx'

        pageNum=0;
        objList=[]
        companyList=[]
        for (bxc_Code,bxc_ComanyName) in list:
            time.sleep(random.randint(2,5))
            pageNum +=1
            try:
                r = requests.get(url+"?CompanyId="+bxc_Code,verify=False, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                print e.message
                print "超时，等待1秒分钟,Company_Code={0}".format(bxc_Code).decode("utf8")
                time.sleep(60)
                try:
                    r = requests.get(url + "?CompanyId=" + bxc_Code,verify=False, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "再超时，Company_Code={0}".format(bxc_Code).decode("utf8")
                    continue

            td=bsObj.find(name="td", attrs={"class": "personnel_name"})
            if td is None:
                print "跳过Company_Code={0}".format(bxc_Code).decode("utf8")
                continue
            domA=td.findAll(name="a")
            if domA is None:
                print "跳过,没有用户，Company_Code={0}".format(bxc_Code).decode("utf8")
                continue

            for a in domA:
                obj = {}
                obj["bxu_Name"]=a.get_text().strip()
                obj["bxu_Company_Code"]=bxc_Code
                href=a.attrs["href"]
                if href is not None:
                    arr=href.split("=")
                    if(len(arr)>1):
                        obj["bxu_Code"] =arr[1]
                objList.append(obj)
                print "公司数量:{4},len={2}, 公司:{0} {3}, 姓名:{1}".format(obj["bxu_Company_Code"],obj["bxu_Name"],len(objList),bxc_ComanyName,pageNum).decode("utf8")


        ## 先清空数据表
        dbDAL.execute("TRUNCATE TABLE Tab_BX_LiuShui_User")
        ## 再插入数据表
        dbDAL.insert(tableName="Tab_BX_LiuShui_User", list=objList)

    except Exception as e:
        print  e.message
    finally:
        dbDAL.dispose()



if __name__=="__main__":
    main()