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
        list = dbDAL.query("SELECT company_Code,company_Name FROM Tab_BX_ZJT_LiuShui_Company WHERE company_Code NOT IN (SELECT company_Code FROM Tab_BX_ZJT_LiuShui_User)")
        companyNum=1
        while companyNum<=len(list):
            data = {}
            (companyCode,companyName) = list[companyNum - 1]
            #url = 'http://www.scjst.gov.cn:8081/QueryInfo/Ente/EnteCyry.aspx?id='+companyCode
            url='http://xmgk.scjst.gov.cn/QueryInfo/Ente/EnteCyry.aspx?id='+companyCode
            try:
                r = requests.get(url,headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                traceback.print_exc()
                print "超时，等待1秒分钟".decode("utf8")
                time.sleep(60)
                try:
                    r = requests.get(url,  headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "再超时，跳过！".decode("utf8")
                    continue
            table= bsObj.find(id="mainContent_gvBiddingResultPager")
            if table is None:
                print " *** 不存在分页元素。或者有 验证码".decode("utf8")
                time.sleep(30)
                continue



            pages= table.find(name="u").get_text().split("/")[1]
            pages=int(pages)
            print "{1},共{0}页".format(pages,companyName).decode("utf8")
            page=1
            objList = []

            data["ctl00$mainContent$txt_names"] = ""
            data["ctl00$mainContent$txt_zsh"]=""
            data["ctl00$mainContent$cxtj"]=" where  b.qybm = (select top 1  FCompanyId from qy_jbxx where qybm ='{0}')".format(companyCode)
            data["UBottom1:dg1"] = ""
            data["UBottom1:dg2"] = ""
            data["UBottom1:dg3"] = ""
            data["UBottom1:dg4"] = ""
            data["UBottom1:dg5"] = ""
            data["UBottom1:dg6"] = ""
            cookiesStr = "_gscu_2084958918=83414331nr0zef20; _gscbrs_2084958918=1; Hm_lvt_69ef768685e0c0a173fa77962dcbe767=1497583545,1497597563,1497618506,1497743667; Hm_lpvt_69ef768685e0c0a173fa77962dcbe767=1497743667; ASP.NET_SessionId=0eplua4lnwfkhrikualljfcd; Hm_lvt_6647b45850e12bf42ce7ed42bd381746=1497583544,1497597563,1497618506,1497743666; Hm_lpvt_6647b45850e12bf42ce7ed42bd381746=1497781209; Hm_lvt_dbbf22b04de47f1e3ea92efe186df1f3=1497583545,1497597563,1497618506,1497743667; Hm_lpvt_dbbf22b04de47f1e3ea92efe186df1f3=1497781209"
            cookiesJson = Comm.Funs.strConvertDic(cookiesStr)

            while page<=pages:
                time.sleep(random.randint(5,12))
                print "第{0}/{1},开始..........".format(page,pages).decode("utf8")
                if page>1:
                    data["__EVENTARGUMENT"] = page
                    try:
                        r = requests.post(url, data=data, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                        bsObj = BeautifulSoup(r.text, "html.parser")
                    except Exception as e:
                        traceback.print_exc()
                        print "超时22，等待40秒分钟,第{0}页".format(page).decode("utf8")
                        time.sleep(40)

                        try:
                            r = requests.post(url, data=data, headers={
                                "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"})
                            bsObj = BeautifulSoup(r.text, "html.parser")
                        except Exception as e:
                            print e.message
                            print "再超时22，第{0}页".format(page).decode("utf8")
                            continue
                try:
                    tables = bsObj.findAll(name="table", attrs={"class", "list"})
                    if tables is None or len(tables)<2:
                        print "有验证码".decode("utf8")
                        time.sleep(random.randint(20,30))
                        continue

                    table=tables[1] #第二个table 才是人员列表
                    trs=table.findAll(name="tr")
                    if len(trs)==1:
                        print " 第{1}页为空记录".format(page).decode("utf8")
                    row=1
                    for tr in trs:
                        if row==1:
                            row +=1
                            continue
                        tds=tr.findAll("td")
                        obj = {}
                        objList.append(obj)
                        domA=tds[1].find(name="a")
                        obj["company_Code"] = companyCode
                        obj["user_Name"]=domA.get_text().strip()
                        obj["user_Code"] = domA.attrs["href"].split("id=")[1].split("&")[0]
                        try:
                            print "len={0},userName:{1},id={2}".format(len(objList), obj["user_Name"], obj["company_Code"]).decode("utf8")
                        except:
                            ## 防止某些生僻字 decode("转换报错")
                            print "len={0},user_Code:{1},id={2}".format(len(objList), obj["user_Code"],
                                                                       obj["company_Code"]).decode("utf8")

                    data["__EVENTTARGET"] = "ctl00$mainContent$gvBiddingResultPager"
                    data["__VIEWSTATE"] = bsObj.find(id="__VIEWSTATE").attrs["value"]
                    data["__EVENTVALIDATION"] = bsObj.find(id="__EVENTVALIDATION").attrs["value"]
                except Exception as e:
                    traceback.print_exc()
                    continue
                else:
                    print "第{0}/{1}页，结束.".format(page,pages).decode("utf8")
                    page += 1
                finally:
                    pass

            if len(objList)>0:
                    pass
                    dbDAL.insert(tableName="Tab_BX_ZJT_LiuShui_User", list=objList)
                    objList=[]
            companyNum+=1
    except:
        traceback.print_exc()
    finally:
        dbDAL.dispose()


if __name__=="__main__":
    main()