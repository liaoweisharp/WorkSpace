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
import Comm.Funs
import global_Vars
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
errList=[]
def main():

        ##需要改数据库名

        print "   开始抓URL......."
        returnValue = getData()
        try:
            dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)
            #先清空
            #dbDAL.execute("truncate table Tab_BX_ZJT_Company_URL")
            #再插入
            dbDAL.insert(tableName="Tab_BX_ZJT_Company_URL",list=returnValue)
        except:
            traceback.print_exc()
        finally:
            dbDAL.dispose()

        print "++++ 完成：错误={0}家".format(len(errList))
        for obj in errList:
            print "错误：{0}, 类型:{1}".format(obj["companyName"],obj["type"])






def getData():


        url = 'http://jzsc.mohurd.gov.cn/dataservice/query/comp/list'
        returnValue=[]
        try:
            time.sleep(random.randint(2, 5))
            cookiesStr = "filter_comp=show; _gscu_1181410730=811977694e56yh88; JSESSIONID=97FD233869F6F6DE1180617A401536F0; Hm_lvt_b1b4b9ea61b6f1627192160766a9c55c=1498620592,1498814278,1499812894,1499821141; Hm_lpvt_b1b4b9ea61b6f1627192160766a9c55c=1499821220"
            cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
            data={"apt_code":"","qy_fr_name":"","qy_code":"","qy_name":"","apt_certno":"","qy_gljg":"","apt_scope":""}
            data["$total"]=369
            data["$pgsz"] =15
            data["qy_reg_addr"]="四川省"
            data["qy_region"]="510000"
            data["$reload"]="0"
            data["qy_type"]="QY_ZZ_ZZZD_006"  ## 监理 :QY_ZZ_ZZZD_002  ##代理 ：QY_ZZ_ZZZD_006
            page=1
            while True:
                ram=random.randint(2, 7)
                time.sleep(ram)
                data["$pg"]=page

                try:
                    r = requests.post(url,data=data, headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/53{0}.{0}".format(ram)})
                    bsObj = BeautifulSoup(r.text, "html.parser")
                    # print r.text
                except Exception as e:
                    print e.message
                    print "***超时，等待10分钟,{0}".decode("utf8")
                    time.sleep(600)
                    try:
                        r = requests.get(url, headers={
                            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                        bsObj = BeautifulSoup(r.text, "html.parser")
                    except Exception as e:
                        print e.message
                        print "***再超时".decode("utf8")
                tbody = bsObj.find(name="tbody", attrs={"class": "cursorDefault"})
                if int(data["$total"])==len(returnValue):
                    # 结束
                    return returnValue
                if tbody is None:
                    print  "**空对象".decode("utf8")
                    time.sleep(20)
                    continue
                trs = tbody.findAll(name="tr")
                if len(trs) ==0:
                    print "*** 没有"

                elif len(trs) > 0:
                    for tr in trs:

                        try:
                            domA=tr.find(name="a")
                            if domA is not None:
                                ins = {}
                                ins["company_Name"] =domA.get_text().strip()
                                ins["url"]=domA.attrs["href"]
                                if data["qy_type"]=="QY_ZZ_ZZZD_002":
                                    ins["type"] ="监理"
                                else:
                                    ins["type"] = "招标代理"

                                returnValue.append(ins)
                                print "第{3}页，len={0},{1},{2}".format(len(returnValue), ins["company_Name"], ins["url"],page)
                        except:
                            traceback.print_exc()


                page+=1

        except:
            print "*** 报错:{0}"
            traceback.print_exc()
        return returnValue






if __name__=="__main__":
    main()