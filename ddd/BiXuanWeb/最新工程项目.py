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

        sql = "SELECT MIN(gongShiDate) FROM ("
        sql += "    SELECT MAX(bxyj_GongShi_Date) gongShiDate FROM tab_bx_yeji"
        sql += "    WHERE bxyj_Status='公告' AND bxyj_Type=2"
        sql += "    UNION"
        sql += "    SELECT MAX(bxyj_GongShi_Date) gongShiDate FROM tab_bx_yeji"
        sql += "    WHERE bxyj_Status='公告' AND bxyj_Type=1"
        sql += "    ) temp"
        list = dbDAL.query(sql)

        lastDate=list[0][0] ##表里最近的时间
        print "最晚日期：{0}".format(lastDate).decode("utf8")
        url = 'https://www.sczbbx.com/Performance/ProjectList.aspx'

        data = {}
        data["ctl00$ctl00$ScriptManager1"]="ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCPerformanceList1$upPerformanceList|ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCPerformanceList1$PagerControl1"
        data["__EVENTTARGET"] = "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCPerformanceList1$PagerControl1"

        data["__VIEWSTATE"] = "/wEPDwULLTEyMjYxODEyMzFkGAEFTWN0bDAwJGN0bDAwJENvbnRlbnRQbGFjZUhvbGRlcjEkQ29udGVudFBsYWNlSG9sZGVyMiRVQ1BlcmZvcm1hbmNlTGlzdDEkZ3ZMaXN0DzwrAAwBCAIBZJkbuUc4gRqGGIVkX2pT7wQfitcLHqrH3liiUro5QQ3n"
        data["__VIEWSTATEGENERATOR"] = "E2CD98D0"
        data["__EVENTVALIDATION"] = "/wEdAAZ0MUqCzfikXwF5M+olG6ge4L4sMdJGI2kpw7/lMbgpEjGZi6YeqIWZymebjQ/vk74wMOKL0ZDLvRCEvVmB4sJr4EDuVjENGArvfZ/USi5p/9X8EC9OAuD/D2iEGlIh5Kso/9/lSACv9lBiR04UkHIWcy5YTRixy6Bo3HJQoTLYjg=="
        data["ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCPerformanceList1$txtProjectName"] = "项目名称 / 人员身份证"
        data["ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCPerformanceList1$ddlPerformanceType"]=""
        data["__ASYNCPOST"]="true"

        cookies=getCookies("Hm_lvt_378eb90e535a42045be40c893a471cd9=1494243609,1494286950,1494477260,1494564373; Hm_lpvt_378eb90e535a42045be40c893a471cd9=1494565107")

        pageNum=1;
        objList=[]
        bo=True
        while bo:
            time.sleep(random.randint(2,5))
            data["__EVENTARGUMENT"] = pageNum
            try:
                r = requests.post(url,data=data,cookies=cookies,verify=False, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                print e.message.decode("utf8")
                print "***超时，等待10分钟,pageNum={0}".format(pageNum).decode("utf8")
                time.sleep(600)
                try:
                    r = requests.post(url, data=data, cookies=cookies,verify=False, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message.decode("utf8")
                    print "***再超时，跳过页码：pageNum={0}".format(pageNum).decode("utf8")
                    pageNum += 1
                    continue

            table=bsObj.find(id="ContentPlaceHolder1_ContentPlaceHolder2_UCPerformanceList1_gvList")
            trs=table.findAll(name="tr")
            rowNum=0

            for tr in trs:
                if rowNum==0: #第一行是表头，不是数据，跳过
                    rowNum += 1
                    continue
                obj={}

                tds=tr.findAll(name="td")
                #第一列
                a=tds[0].find(name="a")
                obj["project_Name"]=a.attrs["title"].strip()
                obj["project_Code"]=a.attrs["href"].split("=")[1].strip()
                #第二列
                label = tds[1].find(name="label")
                obj["project_Type"]=label.attrs["title"].strip()
                #第三列
                obj["zhongBiao_Fee"] = tds[2].get_text().split("千万")[0].strip()
                #第四列
                obj["gongShi_Date"] = tds[3].get_text().strip()
                #第五列
                obj["status"] = tds[4].get_text().strip()
                #第六列
                obj["beiZhu"] = tds[5].get_text().strip()
                obj["create_Date"]=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
                if(obj["gongShi_Date"]<lastDate):
                    # 时间比数据库里的时间还小，则跳出循环
                    bo=False
                    break
                objList.append(obj)
                print  "len={2}, 项目：{0}，project_Code={1}".format(obj["project_Name"],obj["project_Code"],len(objList)).decode("utf8")

            pageNum += 1

        ## 先清空数据表
        dbDAL.execute("TRUNCATE TABLE Tab_BX_LiuShui_NewProject")
        ## 再插入数据表
        dbDAL.insert(tableName="Tab_BX_LiuShui_NewProject", list=objList)

    except Exception as e:
        print  e.message
    finally:
        dbDAL.dispose()


def getCookies(cookieStr):
    '''
    转换成cookie字典
    :return: 
    '''
    cookies = {}  # 初始化cookies字典变量
    for line in cookieStr.split(";"):
       # 其设置为1就会把字符串拆分成2份
       name, value = line.strip().split("=", 1)
       cookies[name] = value
    return cookies;

if __name__=="__main__":
    main()