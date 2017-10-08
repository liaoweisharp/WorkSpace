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

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        #先清空
        dbDAL.execute("TRUNCATE TABLE Tab_WangYiYun_Classfiy")
        list = dbDAL.query("SELECT c_Id,c_Name FROM Tab_WangYiYun_Classfiy")



        objList=[]
        companyList=[]
        for (c_Id,c_Name) in list:
            time.sleep(random.randint(2,5))
            pageNum = 1;
            step = 35  # 步长 记录数
            offset = 0
            # try:
            url = "http://music.163.com/discover/playlist/"
            data = urllib.urlencode({"cat":c_Name,"order":"hot"})
            url = url + "?" + data
            r = requests.get(url, headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
            bsObj = BeautifulSoup(r.content, "html.parser")

            nodeDiv=bsObj.find(id="m-pl-pager")
            nodeA=nodeDiv.findAll(name="a")
            length=len(nodeA)
            maxOffset=nodeA[length-2].attrs["href"].split("offset=")[1]  # 最大的offset
            maxOffset=int(maxOffset)
            while maxOffset>offset:
                try:
                    offset=(pageNum-1) * step

                    url = "http://music.163.com/discover/playlist/"
                    data = urllib.urlencode({"cat": c_Name, "order": "hot"})
                    url = url + "?" + data

                    url = url+"&limit={0}&offset={1}".format(step,offset)
                    r = requests.get(url, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.content, "html.parser")
                    nodeDiv= bsObj.find(id="m-pl-container")
                    nodeAList=nodeDiv.findAll(name="a",attrs={"class":"msk"})
                    objList=[];
                    for nodeA in nodeAList:
                        obj={}
                        obj["ci_Classfiy_Id"]=c_Id
                        obj["ci_Name"]=nodeA.attrs["title"]
                        obj["ci_URL"] = nodeA.attrs["href"]
                        obj["ci_Name"]=obj["ci_Name"].decode("utf8")
                        obj["ci_URL"] = obj["ci_URL"].decode("utf8")
                        objList.append(obj)
                    print "入库中,风格：{1}，第{0}页......".format(pageNum,c_Name).decode("utf8")
                    dbDAL.insert(tableName="Tab_WangYiYun_Classfiy_Item", list=objList)
                except :
                    traceback.print_exc()
                    print "***报错，第{0}页".format(pageNum).decode("utf8")
                    time.sleep(random.randint(5,10))
                    continue
                else:
                    pageNum += 1


            # except Exception as e:
            #     print e.message
            #     print "超时，等待1秒分钟,Company_Code={0}".format(bxc_Code).decode("utf8")
            #     time.sleep(60)
            #     try:
            #         r = requests.get(url + "?CompanyId=" + bxc_Code,verify=False, headers={
            #             "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
            #         bsObj = BeautifulSoup(r.text, "html.parser")
            #     except Exception as e:
            #         print e.message
            #         print "再超时，Company_Code={0}".format(bxc_Code).decode("utf8")
            #         continue
            #
            # td=bsObj.find(name="td", attrs={"class": "personnel_name"})
            # if td is None:
            #     print "跳过Company_Code={0}".format(bxc_Code).decode("utf8")
            #     continue
            # domA=td.findAll(name="a")
            # if domA is None:
            #     print "跳过,没有用户，Company_Code={0}".format(bxc_Code).decode("utf8")
            #     continue
            #
            # for a in domA:
            #     obj = {}
            #     obj["bxu_Name"]=a.get_text().strip()
            #     obj["bxu_Company_Code"]=bxc_Code
            #     href=a.attrs["href"]
            #     if href is not None:
            #         arr=href.split("=")
            #         if(len(arr)>1):
            #             obj["bxu_Code"] =arr[1]
            #     objList.append(obj)
            #     print "公司数量:{4},len={2}, 公司:{0} {3}, 姓名:{1}".format(obj["bxu_Company_Code"],obj["bxu_Name"],len(objList),bxc_ComanyName,pageNum).decode("utf8")
            #

        # ## 先清空数据表
        # dbDAL.execute("TRUNCATE TABLE Tab_BX_LiuShui_User")
        # ## 再插入数据表
        # dbDAL.insert(tableName="Tab_BX_LiuShui_User", list=objList)

    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()



if __name__=="__main__":
    main()