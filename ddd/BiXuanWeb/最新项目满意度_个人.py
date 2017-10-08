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


        url = 'https://www.sczbbx.com/Evaluation/Satisfaction_Starff.aspx'

        data = {}
        data["ctl00$ctl00$ScriptManager1"]="ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCEmpEvaluation1$upEvaluationList|ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCEmpEvaluation1$PagerControl1"
        data["__EVENTTARGET"] = "ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCEmpEvaluation1$PagerControl1"

        data["__VIEWSTATE"] = "/wEPDwUJMzM2MjE2NDI0ZBgBBVljdGwwMCRjdGwwMCRDb250ZW50UGxhY2VIb2xkZXIxJENvbnRlbnRQbGFjZUhvbGRlcjIkVUNFbXBFdmFsdWF0aW9uMSRndkVtcEV2YWx1YXRpb25QYWdlcg88KwAMAQgCAWR2p+ar437nuD2hzmFZpAp7miUIEJDsFzYINaGqajlG3g=="
        data["__VIEWSTATEGENERATOR"] = "4DB4217F"
        data["__EVENTVALIDATION"] = "/wEdAAeI+Z4pxr5fJMqUnyfNkGprRWa41QMMoqXFsa8WXPkBfyTngd2j0G3goKEZuhVUnL81LlJMF/NoKvBqo07j/Cf+3ooLubqKcE/OKxsuX8DbSX4U+eZyicxCIxEXpdIB/D9Uteo/IPukRdei58RdkIafggVloL+2OquIn0D8zwzFwrSBE1etO+NldQ3TSqDBaHk="
        data["ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCEmpEvaluation1$txt_name"] = "项目名称 / 机构名称 / 项目业主 / 人员身份证"
        data["ctl00$ctl00$ContentPlaceHolder1$ContentPlaceHolder2$UCEmpEvaluation1$ddlGoodOrBad"]="0"
        data["__ASYNCPOST"]="true"

        #cookies=getCookies("Guide=\"ENCAAAAAAVMIvWSl4dM5XTqVqbo0gQOPDKYpE32u/JgiDHBF2Fq6+obQlAGv9OKtWQ0w3F3GDc=\"; Hm_lvt_378eb90e535a42045be40c893a471cd9=1496215207,1496229687,1496391293,1496457441; Hm_lpvt_378eb90e535a42045be40c893a471cd9=1496458862")

        pageNum=1;
        objList=[]
        bo=True
        maxPage=0 #最大页数
        while pageNum==1 or (bo and  maxPage>=pageNum):
            time.sleep(random.randint(2,7))
            data["__EVENTARGUMENT"] = pageNum
            try:
                r = requests.post(url,data=data,verify=False, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                traceback.print_exc()
                print "***超时，等待10分钟,pageNum={0}".format(pageNum).decode("utf8")
                time.sleep(600)
                try:
                    r = requests.post(url, data=data, verify=False, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    traceback.print_exc()
                    print "***再超时，跳过页码：pageNum={0}".format(pageNum).decode("utf8")
                    pageNum += 1
                    continue
            if maxPage==0:
                nodeA=bsObj.find(id="ContentPlaceHolder1_ContentPlaceHolder2_UCEmpEvaluation1_PagerControl1").findAll("a")
                if(len(nodeA)>=4):
                    maxPage=nodeA[3].attrs["href"].split("=")[1]
            table=bsObj.find(id="ContentPlaceHolder1_ContentPlaceHolder2_UCEmpEvaluation1_gvEmpEvaluationPager")
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
                obj["daiLiCompany_Name"]=label.attrs["title"].strip()
                #第三列
                label = tds[2].find(name="label")
                obj["user_Name"] =label.attrs["title"].strip()
                #第四列
                label = tds[3].find(name="label")
                obj["shenFenZhengHao"] = label.attrs["title"].strip()
                # 第五列
                label = tds[4].find(name="label")
                obj["manYiDu"] = label.attrs["title"].strip()

                objList.append(obj)
                print  "len={2}, 项目：{0}，project_Code={1},userName:{3}".format(obj["project_Name"],obj["project_Code"],len(objList),obj["user_Name"]).decode("utf8")
                # if len(objList)==100:
                #     dbDAL.insert(tableName="Tab_BX_LiuShui_User_Satisfaction", list=objList)
                #     print  "正在存数据库....."
                #     objList=[]

            #如果最后一个项目已经存在正式表里，则退出循环
            sql="select count(1) from Tab_BX_XinYong_User where bxxu_Project_Code='{0}'".format(obj["project_Code"])
            a1=dbDAL.query(sql)
            if int(a1[0][0])>0:
                bo=False
            pageNum += 1

        ## 先清空数据表
        dbDAL.execute("TRUNCATE TABLE Tab_BX_LiuShui_User_Satisfaction")
        ## 再插入数据表
        dbDAL.insert(tableName="Tab_BX_LiuShui_User_Satisfaction", list=objList)

    except Exception as e:
        traceback.print_exc()
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