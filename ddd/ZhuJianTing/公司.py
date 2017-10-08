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
        for num in range(1,3):
            data = {}
            if num==1:
                ## 四川本地招标代理机构
                ## 先清空数据表
                dbDAL.execute("TRUNCATE TABLE Tab_BX_ZJT_LiuShui_Company")
                #url = 'http://www.scjst.gov.cn:8081/QueryInfo/Ente/EnteList.aspx?type=105'
                url='http://xmgk.scjst.gov.cn/QueryInfo/Ente/EnteList.aspx?type=105'
                data["ctl00$mainContent$cxtj"] = " where  1=1    and qylxbm = '105'  and isnull(regadrCity,'') like '51%'"
                data["ctl00$mainContent$lx114"] = "105"
            elif num==2:
                ## 入川招标代理机构
                url = 'http://xmgk.scjst.gov.cn/QueryInfo/Ente/EnteList.aspx?type=205'
                data["ctl00$mainContent$lx114"] = "205"
                data["ctl00$mainContent$cxtj"] = " where  1=1    and qylxbm = '205'"

            data["__VIEWSTATE"]="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"
            data["__EVENTTARGET"]="ctl00$mainContent$gvPager"
            data["__EVENTVALIDATION"]="rpJqyoef0hvZihY2mSoC7HXatsFmctRxHxfiJ1FcG9lw6Xni5+1iV7YwtgnZ5RI6almsyNZR50hX/qgDbhm3KNh9WCam2smuGKgEOJwqjGcPWcMr1/LP9Qh1147QAhBw09kS++JPwUsG5sGrDnGAaZKWFB8Hj2746bjXjMHvsGNaX3Q+NEtwb8pCXo6ZbQKL"
            data["ctl00$mainContent$txt_entname"]=""


            data["UBottom1:dg1"]= ""
            data["UBottom1:dg2"] = ""
            data["UBottom1:dg3"] = ""
            data["UBottom1:dg4"] = ""
            data["UBottom1:dg5"] = ""
            data["UBottom1:dg6"] = ""


            cookiesStr = "_gscu_2084958918=83414331nr0zef20; _gscbrs_2084958918=1; Hm_lvt_69ef768685e0c0a173fa77962dcbe767=1497583545,1497597563,1497618506,1497743667; Hm_lpvt_69ef768685e0c0a173fa77962dcbe767=1497743667; ASP.NET_SessionId=0eplua4lnwfkhrikualljfcd; Hm_lvt_6647b45850e12bf42ce7ed42bd381746=1497583544,1497597563,1497618506,1497743666; Hm_lpvt_6647b45850e12bf42ce7ed42bd381746=1497748719; Hm_lvt_dbbf22b04de47f1e3ea92efe186df1f3=1497583545,1497597563,1497618506,1497743667; Hm_lpvt_dbbf22b04de47f1e3ea92efe186df1f3=1497748719"
            cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
            try:
                r = requests.post(url,data=data,cookies=cookiesJson,headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                traceback.print_exc()
                print "超时，等待1秒分钟".decode("utf8")
                time.sleep(60)
                try:
                    r = requests.post(url, data=data, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "再超时，跳过！".decode("utf8")
                    continue
            table= bsObj.find(id="mainContent_gvPager")
            if table is None:
                print " *** 不存在分页元素。company:{0}"



            pages= table.find(name="u").get_text().split("/")[1]
            pages=int(pages)
            print "共{0}页".format(pages)
            page=1
            objList = []
            while page<=pages:
                time.sleep(random.randint(3,8))
                print "第{0}页..........".format(page).decode("utf8")
                data["__EVENTARGUMENT"] = page
                try:
                    r = requests.post(url, data=data,cookies=cookiesJson, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    traceback.print_exc()
                    print "超时22，等待40秒分钟,第{0}页".format(page).decode("utf8")
                    time.sleep(40)

                    try:
                        r = requests.post(url, data=data,cookies=cookiesJson, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                        bsObj = BeautifulSoup(r.text, "html.parser")
                        print r.text
                    except Exception as e:
                        print e.message
                        print "再超时22，跳过，第{0}页".format(page).decode("utf8")
                        continue
                try:
                    table = bsObj.find(name="table", attrs={"class", "list"})
                    if table is None:
                        print "有验证码"
                        time.sleep(30)
                        continue
                    trs=table.findAll(name="tr")
                    if len(trs)==1:
                        print " 第{1}页为空记录".format(page)
                    row=1
                    for tr in trs:
                        if row==1:
                            row +=1
                            continue
                        tds=tr.findAll("td")
                        if len(tds)>4:
                            obj = {}
                            objList.append(obj)
                            obj["shuDi"]=tds[1].get_text().strip()
                            adom=tds[2].find(name="a")
                            obj["company_Name"] =adom.attrs["title"]
                            obj["company_Code"] = adom.attrs["href"].split("id=")[1].split("&")[0]
                            obj["faDingDaiBiao"] = tds[4].get_text().strip()
                            print "len={0},company:{1},id={2}".format((page-1)*10+len(objList), obj["company_Name"], obj["company_Code"])
                        if (len(objList) % 10 == 0):
                            dbDAL.insert(tableName="Tab_BX_ZJT_LiuShui_Company", list=objList)
                            objList = []

                except Exception as e:
                    traceback.print_exc()
                    continue
                else:
                    print "第{0}页，结束.".format(page)
                    page += 1

                finally:
                    pass

            if len(objList)>0:
                pass
                dbDAL.insert(tableName="Tab_BX_ZJT_LiuShui_Company", list=objList)
    except:
        traceback.print_exc()
    finally:
        dbDAL.dispose()


if __name__=="__main__":
    main()