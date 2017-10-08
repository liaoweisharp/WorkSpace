# coding=UTF-8
import sys
import traceback

import requests
import time

import global_Vars
from selenium import webdriver
from bs4 import BeautifulSoup
import re
import json
import urllib
import random
sys.path.append("..")
import DataBase.DatabaseDAL
# import global_Vars
import Comm.Funs

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

def main():
    # getUrl()
    getUserDetail()

def getUrl():
    try:
        ##需要改数据库名
        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)
        # 清空表
        dbDAL.execute("TRUNCATE TABLE Tab_ODS_Users")
        cookiesStr = "guid=1497948075960700029; EhireGuid=ad1743d5ef71411abea3a9919236775a; slife=lowbrowser%3Dnot%26%7C%26; search=jobarea%7E%60090200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0100%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243903%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243816%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21collapse_expansion%7E%601%7C%21; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0Bs4p00uiAsaKX3Fu000000IML1300000UsbDig.THLZ_Q5n1VeHksK85yF9pywdpAqVuNqsusK15y7-PH0zrj0knj0sPj0Lm1n0IHYdPDRLfHR1PDf3wW9An16sPYR4wjfkrRwanWn1PW6sn0K95gTqFhdWpyfqn10krjbsPHfkPzusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqrH01rf%2526tpl%253Dtpl_10085_15730_1%2526l%253D1054828295%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m7ad13823%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D25%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dbaiduhome_pg%2526inputT%253D4670%26%7C%26adsnum%3D789233; 51job=cenglish%3D0; ASP.NET_SessionId=0zco5eonjevgzpbo1ova15r3; HRUSERINFO=CtmID=109776&DBID=1&MType=02&HRUID=2788209&UserAUTHORITY=1000110000&IsCtmLevle=1&UserName=siteqi-xinan&IsStandard=1&LoginTime=08%2f11%2f2017+09%3a39%3a29&ExpireTime=08%2f11%2f2017+09%3a49%3a29&CtmAuthen=0000011000000001000111010000000011100011&BIsAgreed=true&IsResetPwd=0&CtmLiscense=11&AccessKey=4488a5a575f12a6a; AccessKey=4e9dbf0c1dc9489; LangType=Lang=&Flag=1"
        cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
        # url = 'http://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N'
        # r = requests.get(url,cookies=cookiesJson, verify=False, headers={
        #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"})
        url = "http://ehire.51job.com/Candidate/SearchResumeNew.aspx"

        data = {}
        data["__EVENTTARGET"] = "ctrlSerach$search_submit"
        data["__EVENTARGUMENT"] = ""
        data["__LASTFOCUS"] = ""
        data[
            "__VIEWSTATE"] = "/wEPDwULLTE0NzQ1NjY2OTYPFg4eBElzRU5oHhB2c1NlbGVjdGVkRmllbGRzBTNBR0UsV09SS1lFQVIsU0VYLEFSRUEsV09SS0ZVTkMsVE9QREVHUkVFLExBU1RVUERBVEUeCFBhZ2VTaXplAjIeDHN0clNlbGVjdENvbAUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHglQYWdlSW5kZXhmHghQYWdlRGF0YQXVEDF8MjAwfDIwMHw1MDAwfDY2NDU4NzYsMzQ5OTkyNTQzLDM1OTg5Nzc5MywzNDEzNzg4MjYsMzAyNDEyNDM3LDM2Mzg3MDA5MSwzNjEyODc0NzIsMzU1ODU3NDc3LDM0MTE3ODQ5NCw3MDM2NDQwNCw2MzQ1MjAxMywzMzIzMDkyMDYsNTQ2Mzk1MjgsMzU3NjQ2NTcxLDY3MjQ0NjE2LDM2Mzk0ODUzMiwzNTM2MjgxODMsMzU2NjU5NTQyLDM1NDk2ODg1MywzNTcyMDE0NDEsMzA4NjIxNDc4LDMxNDkzMDgyOSw2NTI4NDQ5MSwxNzIwNTI5OSw4MTY0MzgyOSwzNDE1NjUwNDcsMzY0MTk2ODYwLDMzNzU2ODgyNSwzNjQyODEyMDcsMzMzMjU2NjkwLDk2NDk1MzA1LDE1NDk4MjI2LDM1MjMzMzkxNiw4MjY5NjI1MSwzMTQ4MDYwMjEsMzAzNDU1OTYxLDM0MDYwMzY5MSw5NDM4NDE1Niw3MDQwODQwMCw3OTM2ODA1OCwzMjU5NDg5MjgsNTc2MDQzNTksMzUwODM0NzY1LDY3NDQ5NzIyLDM2MjM5ODg4NSwzMzM2NzU4OTgsMzM0NzIzOTYzLDM2MjIzOTg1MywzNjMwNTIxNDYsMzU3OTA3MTI5LDMwNzc5MDg4OSwzNTk1NDQyNjIsMzI3MTM3MDg3LDgzNjE5ODg4LDM2NDE5OTkxMiw2NTk3NDIzMCw4NDc5NzA5OSw0NDc4NzA3LDMzOTQ0MzE1NiwzMDM2MDk3NDcsNzk3NjM3MzgsMzY0NjIwODQ0LDM2Mjk3NDU0OCwzMjkwNTg2NzksMTI3ODAzNDgsNzUzMjgyMzMsMjI4NjYzMywzMzg5NjQ5NTksODUzMzU1MzAsODEwODA0OTgsOTY5Nzg1ODMsMzYyNjg2NjAzLDg0MDUwNDk4LDM0NTcwMDc3Niw3MTU5MzQ3MCw1MzQ2MTIyNiwzMjg1ODcyNTcsNTA3OTE4NzksMzUzODM5NjQyLDM2MzUwMDExMSwzNDgxNDY4MDMsMzQzNTQ2Mjg0LDM1NDQ3NjU3OCwzNjQ1NjEzNjYsMzUyMTI4OTA3LDc2NDEyNjI0LDM2NDUzMDMwMyw5MDgxMjQzOCwzNTY4NDUwNjksMzU0MzU1NzEwLDc5OTc2OTY0LDYyNTgxLDUwODEzMTQ5LDMzNjQwMzkzMCw5NDk1MTc1Nyw2NTUwNDQ3OCwzNjM5NDkzMDMsMzA4NzIxMzU4LDM2MDk4MDcwNywzMTg0NzkzNjEsMzY0NDY2ODU3LDU5NDU1NzY0LDM1ODA0OTk2OSw5MDkxMzA4NSw3NjgyMDM3OCwyOTM2MTU4MywzNTAyMjY1NDUsMzYyOTQ4MzcxLDM0Nzc5NDA0MSwzNDQ5MDk5ODcsMjc3MjgwNzEsMzMzMTc5MTQ3LDkxNDc1NDE1LDM2NDYyMDgxNywzMzczNDM2NzYsMzY0NjIwNjQ4LDMyMTg5NzAzOSwzMTkxMTc2NjgsNzMzNDI3NDUsMzYzMzAzOTc5LDM2NDI4NjU3MywzNTcwNTIxNTAsMzMwNDIxNTk5LDc5ODQwMjAyLDM2NDMwMTczMSwzNjI1NTA3ODIsMzU3NTgzMjk3LDM2MTUyNzEyNCw4NzY3NjU1LDY2NDMyMDcsMzE2NjI0MzIsMzY0MzI5NjE5LDU4ODM4NDgyLDk2ODExNzYwLDY0MDQ1ODMwLDM0MzY5OTg2MiwzNTM3MjAyMTksMzU0NTcyODkzLDMyOTIxNTg0MCwzNTYyNTg0MzMsNjk5Njc5MTEsMzM0MzUzMDAyLDMyNzM2MjQ5MCw2ODM4ODM1OCw2OTkyNzc1OCwxNzEyOTcyOSwzMjA3MDgwNzAsNTI1OTU5NzcsNzA4MzkwMDgsNTkzNDQ4MywzNTQxODUzODgsMTc4NTM0MzgsMzIyNDMzNDI1LDM1OTA2OTg4MSwzNjQ1NDI3MTUsMzAzOTIyOTEyLDMwMDc0Mjg3NiwxMzQxNDU4MCwzNTI3NTM5NTksMzYzNTUyMDM3LDMyMzk5MDU5OSw2Mjc4OTkzNywzMTU5NTczNCwzNjMxOTk0NjQsNTY3MzMwNTcsMzU2MDc3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"
        data["ctrlSerach$search_keyword_txt"] = ""
        data["ctrlSerach$search_company_txt"] = ""
        data["ctrlSerach$search_area_input"] = ""
        data["ctrlSerach$search_area_hid"] = ""
        data["ctrlSerach$search_funtype_hid"] = "$计算机软件|0100$"
        data["ctrlSerach$search_expectsalaryf_input"] = "不限"
        data["ctrlSerach$search_expectsalaryt_input"] = "不限"
        data["ctrlSerach$search_industry_hid"] = ""
        data["ctrlSerach$search_wyf_input"] = "不限"
        data["ctrlSerach$search_wyt_input"] = "不限"
        data["ctrlSerach$search_df_input"] = "不限"
        data["ctrlSerach$search_dt_input"] = "不限"
        data["ctrlSerach$search_cursalaryf_input"] = "不限"
        data["ctrlSerach$search_cursalaryt_input"] = "不限"
        data["ctrlSerach$search_age_input"] = "年龄"
        data["ctrlSerach$search_agef_input"] = ""
        data["ctrlSerach$search_aget_input"] = ""
        data["ctrlSerach$search_expjobarea_input"] = "成都"
        data["ctrlSerach$search_expjobarea_hid"] = "成都|090200"
        data["ctrlSerach$search_forlang_input"] = "语言"
        data["ctrlSerach$search_fl_input"] = "不限"
        data["ctrlSerach$search_fllsabilityll_input"] = "不限"
        data["ctrlSerach$search_englishlevel_input"] = "英语等级"
        data["ctrlSerach$search_sex_input"] = "性别"
        data["ctrlSerach$search_major_input"] = "专业"
        data["ctrlSerach$search_major_hid"] = ""
        data["ctrlSerach$search_hukou_input"] = "户口"
        data["ctrlSerach$search_hukou_hid"] = ""
        data["ctrlSerach$search_rsmupdate_input"] = "近1年"
        data["ctrlSerach$search_jobstatus_input"] = "求职状态"
        data["send_cycle"] = "1"
        data["send_time"] = "7"
        data["send_sum"] = "10"
        data["ctrlSerach$hidSearchValue"] = "##0#计算机软件|0100###################近1年|6##1###成都|090200#0#0#0"
        data["ctrlSerach$hidKeyWordMind"] = ""
        data["ctrlSerach$hidRecommend"] = "#####"
        data["ctrlSerach$hidWorkYearArea"] = ""
        data["ctrlSerach$hidDegreeArea"] = ""
        data["ctrlSerach$hidSalaryArea"] = ""
        data["ctrlSerach$hidCurSalaryArea"] = ""
        data["ctrlSerach$hidIsRecDisplay"] = "1"
        data["showselected"] = ""
        data["pagerTopNew$ctl06"] = "50"
        data["cbxColumns$0"] = "AGE"
        data["cbxColumns$1"] = "WORKYEAR"
        data["cbxColumns$2"] = "SEX"
        data["cbxColumns$3"] = "AREA"
        data["cbxColumns$4"] = "WORKFUNC"
        data["cbxColumns$5"] = "TOPDEGREE"
        data["cbxColumns$6"] = "LASTUPDATE"
        data["hidAccessKey"] = "825078f696694f0"
        data["hidShowCode"] = "0"
        data["hidDisplayType"] = "0"
        data["hidEhireDemo"] = ""
        data["hidUserID"] = ""
        data[
            "hidCheckUserIds"] = "568459808,16032055,74151334,77478003,581174108,94113703,546802421,29464377,8491918,565884048,516446350,23279055,27511096,568845934,579761843,25634173,24734499,512091738,501403691,517848568,578094688,544500996,518153943,542997558,570921151,568061030,541560165,548260093,72448060,39264545,511971146,9298185,565286757,565509642,553653983,5500187,542082915,560288080,513207787,71090746,503935832,11049192,552647484,519196176,568184021,2992254,504073894,78277050,504618700,22837556"
        data["hidCheckKey"] = "96868a5c2db55573dab23df93f3250ae"
        data["hidEvents"] = ""
        data["hidNoSearchIDs"] = ""
        data["hidBtnType"] = ""
        data["hideMarkid"] = ""
        data["hidStrAuthority"] = "0"
        data["hidDownloadNum"] = "4"
        data["hidKeywordCookie"] = ""
        data["showGuide"] = ""

        r = requests.post(url, data=data, cookies=cookiesJson, verify=False, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        bsObj = BeautifulSoup(r.text, "html.parser")
        viewState = bsObj.find(id="__VIEWSTATE").attrs["value"]
        maxPage = bsObj.find(id="pagerBottomNew_btnNum_ma").get_text()
        num = 1
        while num <= maxPage:
            time.sleep(random.randint(5, 10))
            try:
                print "page={0},hidAccessKey:{2},hidCheckKey={3},  viewState={1}".format(num, data["__VIEWSTATE"],
                                                                                         data["hidAccessKey"],
                                                                                         data["hidCheckKey"])
                r = requests.post(url, data=data, cookies=cookiesJson, verify=False, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
                objList = getObj(bsObj)
            except:
                traceback.print_exc()
                time.sleep(random.randint(10, 15))
            else:
                if objList is not None and len(objList) > 0:
                    print "入库中....{0}个, num/maxPage={1}/{2},{3}".format(len(objList), num, maxPage,
                                                                        objList[0]["uu_Number"]).decode("utf8")
                    dbDAL.insert(tableName="Tab_ODS_Users", list=objList)
                    objList = []
                elif objList is None:
                    print "objList is None . Page={0}".format(num)
                else:
                    print "objList 0 个元素. Page={0}".format(num)
                num += 1
                viewState = bsObj.find(id="__VIEWSTATE").attrs["value"]
                hidCheckKey = bsObj.find(id="hidCheckKey").attrs["value"]
                data["__VIEWSTATE"] = viewState
                data["__EVENTTARGET"] = "pagerBottomNew$nextButton"
                data["hidCheckKey"] = hidCheckKey
                data["hidAccessKey"] = bsObj.find(id="hidAccessKey").attrs["value"]
                data["hidShowCode"] = bsObj.find(id="hidShowCode").attrs["value"]
                data["hidDisplayType"] = bsObj.find(id="hidDisplayType").attrs["value"]
                # data["hidEhireDemo"] = ""
                # data["hidUserID"] = ""
                data["hidCheckUserIds"] = bsObj.find(id="hidCheckUserIds").attrs["value"]
                # data["hidEvents"] = ""
                # data["hidNoSearchIDs"] = ""
                # data["hidBtnType"] = ""
                # data["hideMarkid"] = ""
                data["hidStrAuthority"] = bsObj.find(id="hidStrAuthority").attrs["value"]
                data["hidDownloadNum"] = bsObj.find(id="hidDownloadNum").attrs["value"]
                # data["hidKeywordCookie"] = ""
                # data["showGuide"] = ""

                data["__EVENTTARGET"] = "pagerBottomNew$nextButton"

    except:
        traceback.print_exc()
    finally:
        dbDAL.dispose()
def getObj(bsObj):
    try:
        nodeTable=bsObj.find(name="div",attrs={"class":"Common_list-table"})
        nodeTrs1=nodeTable.find(name="tbody").findAll(name="tr",attrs={"class":"inbox_tr1"})
        nodeTrs2 = nodeTable.find(name="tbody").findAll(name="tr", attrs={"class": "inbox_tr2"})
        nodeTrs=[]
        nodeTrs.extend(nodeTrs1)
        nodeTrs.extend(nodeTrs2)
        objList=[]
        for i in range(0,len(nodeTrs)):
            try:
                obj={}

                tr=nodeTrs[i]
                nodeTds=tr.findAll(name="td")
                ## id
                nodeA=nodeTds[1].find(name="a")
                href=nodeA.attrs["href"]
                id=nodeA.get_text()
                obj["uu_Number"]=id
                obj["uu_URL"]=href
                obj["uu_Web_Id"] = 2  #前程无忧
            except:
                traceback.print_exc()
                continue
            else:
                objList.append(obj)

    except:
        return None
    else:
        return objList
def getUserDetail():
    try:
        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)
        # 清空表
        webList=dbDAL.query("select wb_URL,wb_Name from Tab_Web where wb_Name='前程无忧'")
        (wbUrl,webName)=webList[0]
        dataList=dbDAL.query("select uu_Id,uu_Number,uu_URL from Tab_ODS_Users where uu_Vaild is null or uu_Vaild=0")
        num=1
        cookiesStr = "guid=1497948075960700029; EhireGuid=ad1743d5ef71411abea3a9919236775a; slife=lowbrowser%3Dnot%26%7C%26; search=jobarea%7E%60090200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0100%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243903%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243816%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21collapse_expansion%7E%601%7C%21; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0Bs4p00uiAsaKX3Fu000000IML1300000UsbDig.THLZ_Q5n1VeHksK85yF9pywdpAqVuNqsusK15y7-PH0zrj0knj0sPj0Lm1n0IHYdPDRLfHR1PDf3wW9An16sPYR4wjfkrRwanWn1PW6sn0K95gTqFhdWpyfqn10krjbsPHfkPzusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqrH01rf%2526tpl%253Dtpl_10085_15730_1%2526l%253D1054828295%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m7ad13823%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D25%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dbaiduhome_pg%2526inputT%253D4670%26%7C%26adsnum%3D789233; 51job=cenglish%3D0; ASP.NET_SessionId=estkktqxvdsxf43nm2sifvos; HRUSERINFO=CtmID=109776&DBID=1&MType=02&HRUID=2788209&UserAUTHORITY=1000110000&IsCtmLevle=1&UserName=siteqi-xinan&IsStandard=1&LoginTime=08%2f15%2f2017+11%3a08%3a51&ExpireTime=08%2f15%2f2017+11%3a18%3a51&CtmAuthen=0000011000000001000111010000000011100011&BIsAgreed=true&IsResetPwd=0&CtmLiscense=11&AccessKey=ffd8e856f0ef6020; AccessKey=3a1a85774ad9440; LangType=Lang=&Flag=1"
        cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
        objList=[]
        while num<=len(dataList):
            try:
                ran=random.randint(3, 10)
                time.sleep(ran)
                (id,uu_Number,url)=dataList[num-1]
                url=wbUrl+url
                page = requests.get(url,cookies=cookiesJson, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/53{0}.3{0}".format(ran)})
                bsObj = BeautifulSoup(page.text, "html.parser")
                # print page.text
                #更新时间
                obj ={}
                obj["uu_Id"]=id
                obj["uu_Vaild"]='0'  #无效的（保密的简历）
                objList.append(obj)

                #
                nodeDiv=bsObj.find(id="divResume")
                if nodeDiv is None:
                    num += 1
                    obj["uu_Vaild"] = '2' # 账号下线
                    print "uu_Number={0}没有id=divResume节点。账号下线".format(uu_Number).decode("utf8")
                    dbDAL.update(tableName="Tab_ODS_Users", list=objList, whereTuple=("uu_Id",))
                    objList = []
                    continue
                node=nodeDiv.find(name="table")
                if node is None:
                    num += 1
                    print "uu_Number={0},（保密的简历）".format(uu_Number).decode("utf8")
                    dbDAL.update(tableName="Tab_ODS_Users", list=objList, whereTuple=("uu_Id",))
                    objList = []
                    continue

                obj = {"uu_Position": "", "uu_Profession": "", "uu_Major": "", "uu_University": "", "uu_Education": "",
                       "uu_HuJi": "", "uu_Marry": "", "uu_WorkAddress": "", "uu_Wages": ""}
                obj["uu_Vaild"] = '1'  # 有效的（非保密的简历）
                nodeUpdate = bsObj.find(id="lblResumeUpdateTime")
                if nodeUpdate is not None:
                    nodeB = nodeUpdate.find(name="b")
                    if nodeB is not None:
                        obj["uu_UpdateDate"] = nodeB.get_text()
                dd= len(node)
                if nodeDiv is not None:
                    nodeTable=nodeDiv.find(name="table")
                    if nodeTable is not None:
                        nodeTable1=nodeTable.find(name="table")
                        if nodeTable1 is not None:
                            nodeTable1 = nodeTable.find(name="table")
                            nodeTrs=nodeTable1.findAll(name="tr")
                            if len(nodeTrs)==4:
                                text=nodeTrs[3].get_text().strip()
                                obj["uu_AgeInfo"]=text
                nodeTds=nodeDiv.findAll(name="td")
                index=0
                while index<len(nodeTds):
                    title=nodeTds[index].get_text().strip()
                    s1 =''.join(title.split()) ##去空格
                    s1= s1.replace('：', '')
                    s1 = s1.replace(':', '')

                    if index < (len(nodeTds)-1):  #不是最后一个
                        val=None
                        if s1=="职位" :
                            val="uu_Position"
                        elif s1=="行业":
                            val="uu_Profession"
                        elif s1=="专业":
                            val="uu_Major"
                        elif s1 == "学校":
                            val = "uu_University"
                        elif s1 == "学历/学位":
                            val = "uu_Education"
                        elif s1 == "户口/国籍":
                            val = "uu_HuJi"
                        elif s1 == "婚姻状况":
                            val = "uu_Marry"
                        elif s1 == "地点":
                            val = "uu_WorkAddress"
                        elif s1 == "期望薪资":
                            val = "uu_Wages"
                        if val is not None:
                            obj[val]=nodeTds[index+1].get_text().strip()
                    index+=1
                #抓工作经验


            except:
                traceback.print_exc()
                continue
            else:
                print "入库：id={0},url={1},期望薪资:{2},职位={3}".format(id,url,obj["uu_Wages"],obj["uu_Position"])
                dbDAL.update(tableName="Tab_ODS_Users", list=objList, whereTuple=("uu_Id",))
                objList=[]
                num+=1
                #保存文件
                fp = open("html/"+uu_Number+".html", "w")
                fp.write(page.text)

    except:
        traceback.print_exc()






if __name__=="__main__":
    main()