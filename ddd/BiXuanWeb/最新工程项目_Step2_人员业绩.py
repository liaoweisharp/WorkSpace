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


        list = dbDAL.query("SELECT project_Code,status FROM Tab_BX_LiuShui_NewProject WHERE STATUS='公告' ")



        url = 'https://www.sczbbx.com/Performance/PerformanceInfo.aspx'

        pageNum=1;
        objList=[]
        companyList=[]
        for (project_Code,status) in list:
            time.sleep(random.randint(2,5))
            try:
                r = requests.get(url+"?id="+project_Code,verify=False, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
            except Exception as e:
                print e.message
                print "超时，等待10分钟,project_Code={0}".format(project_Code).decode("utf8")
                time.sleep(600)
                try:
                    r = requests.get(url + "?id=" + project_Code,verify=False, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "再超时，跳过project_Code={0}".format(project_Code).decode("utf8")
                    continue


            domDiv=bsObj.find(name="div", attrs={"class": "anno_details"})
            if domDiv is None:
                continue
            domTable=domDiv.find(name="table")
            if domTable is None:
                continue
            domTr=getNode(domTable,"委托招标代理合同")
            if domTr is None:
                domTr=getNode(domTable,"委托代理合同")
            if domTr is None:
                print "***没有找到用户:{0}".format(project_Code).decode("utf8")
                continue
            domTd=domTr.find(name="td",attrs={"colspan":"3"})
            if domTd is None:
                print "***表结构可能变动，请分析:project_Code=".format(project_Code).decode("utf8")
                continue

            domTr = getNode(domTable, "代理机构名称")
            if domTr is not None:
                domA = domTr.find(name="a");
                if domA is not None:
                    companyId = domA["href"].split("=")[1]
                    companyName = domA.get_text()
                    companyList.append({"project_Code": project_Code, "daiLiJiGouMingCheng": companyName,
                                        "daiLiJiGou_Code": companyId})
            domA=domTd.findAll(name="a")

            for a in domA:
                obj = {}
                obj["project_Code"]=project_Code
                obj["name"]=a.get_text().strip()
                href=a.attrs["href"]
                if href is not None:
                    arr=href.split("=")
                    if(len(arr)>1):
                        obj["name_Code"] =arr[1]
                objList.append(obj)
                print "len={2}, {0},{3},{1}".format(obj["project_Code"],obj["name"],len(objList),companyName).decode("utf8")



           # dbDAL.update("Tab_BX_LiuShui_NewProject",companyList,("project_Code",))

        ## 先清空数据表
        dbDAL.execute("TRUNCATE TABLE Tab_BX_LiuShui_NewProject_Users")
        ## 更新上一步的表
        if len(companyList)>0:
            for company in companyList:
                sql_update="update Tab_BX_LiuShui_NewProject set daiLiJiGou_Code='{1}',daiLiJiGouMingCheng='{2}' where project_Code='{0}'".format(company["project_Code"],company["daiLiJiGou_Code"],company["daiLiJiGouMingCheng"])
                dbDAL.execute(sql_update)
        ## 再插入数据表
        dbDAL.insert(tableName="Tab_BX_LiuShui_NewProject_Users", list=objList)

    except Exception as e:
        print  e.message
    finally:
        dbDAL.dispose()

def getNode(domTable,text):
    '''
    返回
    :param domTable: 
    :param text: 
    :return: 
    '''
    for tr in domTable.findAll(name="tr"):
        th=tr.find("th")
        if th is not None:
            if th.get_text().strip()==text:
                return tr
    return None
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