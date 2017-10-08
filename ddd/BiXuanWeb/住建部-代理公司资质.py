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
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
errList=[]
def main():

        ##需要改数据库名

        print "   开始抓URL......."
        objList = getId()
        print "   开始抓资质 ......."
        returnValue = getData(objList)
        try:
            dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)
            #先清空
            dbDAL.execute("truncate table Tab_BX_LiuShui_Company_ZiZhi")
            #再插入
            dbDAL.insert(tableName="Tab_BX_LiuShui_Company_ZiZhi",list=returnValue)
        except:
            traceback.print_exc()
        finally:
            dbDAL.dispose()

        print "++++ 完成：错误={0}家".format(len(errList))
        for obj in errList:
            print "错误：{0}, 类型:{1}".format(obj["companyName"],obj["type"])

def getId():
    objList = []
    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)

    sql = "SELECT  bxc_ComanyName,bxc_PreCompanyName FROM Tab_BX_Company"
    list = dbDAL.query(sql)

    url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list'
    data = {}
    data = {"qy_type": "", "apt_scope": "", "apt_code": "", "qy_name": "", "qy_fr_name": "", "apt_certno": "",
            "qy_reg_addr": "", "qy_region": ""}

    for (companyName,preCompanyName) in list:
        try:
            time.sleep(random.randint(2, 5))
            if companyName=="中国建筑设计咨询公司":  ##特例，目前只发现一个就写死吧
                data["complexname"] = "中国建筑设计咨询有限公司"
            elif companyName=="河北华能招标有限责任公司":
                data["complexname"] = "华能招标有限公司"
            elif companyName=="重庆国际投资咨询集团有限公司":
                data["complexname"] = "重庆招标采购（集团）有限责任公司"
            elif companyName=="广州广大工程项目管理有限公司":
                data["complexname"] = "广东省广大工程顾问有限公司"
            elif companyName=="成都恒瑞招投标代理有限公司":
                data["complexname"] = "四川兴恒瑞建设工程有限公司"
            elif companyName=="成都鑫标点工程管理咨询有限公司":
                data["complexname"] = "鑫标点工程管理有限公司"
            elif companyName=="四川正信建设工程造价事务所有限公司":
                data["complexname"] = "四川信永中和正信建设工程造价事务所有限公司"
            else:
                data["complexname"] = companyName

            try:
                r = requests.post(url, data=data, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")

            except Exception as e:
                print e.message
                print "***超时，等待10分钟,{0}".format(companyName).decode("utf8")
                time.sleep(600)
                try:
                    r = requests.post(url, data=data, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "***再超时，跳过：{0}".format(companyName).decode("utf8")
                    errList.append({"companyName":companyName,"type":"超时"})
                    continue
            tbody = bsObj.find(name="tbody", attrs={"class": "cursorDefault"})
            trs = tbody.findAll(name="tr")
            if len(trs) > 1:
                print "*** 有多个公司重名‘{0}’，取第一个".format(companyName)
                tr = trs[0]
            elif len(trs) == 1:
                tr = trs[0]
                if tr.attrs.has_key("class") and tr.attrs["class"][0]== "nodata":
                    tr = None
                    print "*** 没有查找到公司：{0}".format(companyName)
                    errList.append({"companyName": companyName, "type": "没有URL"})
                    continue
            a = tr.find(name="td", attrs={"data-header": "企业名称"}).find(name="a")
            ids = a.attrs["href"].split("/")
            obj = {"companyName": companyName}
            obj["id"] = ids[len(ids) - 1]

            objList.append(obj)
            print "len={0},{1},{2}".format(len(objList),obj["companyName"],obj["id"])
        except:
            print "*** 报错:{0}".format(companyName)
            traceback.print_exc()
            continue
    return objList




def getData(objList):


    url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/'
    returnValue=[]
    pg=0
    while pg < len(objList):
        try:
            obj=objList[pg]
            time.sleep(random.randint(2, 5))
            id = obj["id"]
            companyName=obj["companyName"]
            _url=url+id
            data={"$total":50,"$reload":0,"$pg":1,"$pgsz":50}
            try:
                r = requests.post(_url,data=data, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")

            except Exception as e:
                print e.message
                print "***超时，等待30秒,{0}".format(companyName).decode("utf8")
                time.sleep(random.randint(25,35))
                try:
                    r = requests.get(_url, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "***再超时，跳过：{0}".format(companyName).decode("utf8")
                    errList.append({"companyName": companyName, "type": "超时"})
                    continue
            tbody = bsObj.find(name="tbody", attrs={"class": "cursorDefault"})
            trs = tbody.findAll(name="tr",attrs={"class":"row"})
            if len(trs) ==0:
                print "*** 没有资质‘{0}’".format(companyName)
                continue

            elif len(trs) > 0:
                for tr in trs:
                    ins={}
                    try:
                        ins["Company_Name"]=companyName
                        ins["ZiZhi_LeiBie"] = tr.find(name="td", attrs={"data-header": "资质类别"}).get_text().strip()
                        ins["ZiZhi_Name"] = tr.find(name="td", attrs={"data-header": "资质名称"}).get_text().strip()
                        ins["YouXiaoQi"] = tr.find(name="td", attrs={"data-header": "证书有效期"}).get_text().strip()
                    except:
                        traceback.print_exc()
                        continue
                    else:
                        returnValue.append(ins)
                        print "len={0},{1},{2}".format(len(returnValue),ins["Company_Name"],ins["ZiZhi_LeiBie"])


        except:
            print "*** 报错:{0}".format(companyName)
            traceback.print_exc()
            continue
        else:
            pg+=1
    return returnValue






if __name__=="__main__":
    main()