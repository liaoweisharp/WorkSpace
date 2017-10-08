# coding=UTF-8
import json
import sys
import time
import traceback
import urllib

import requests
from selenium import webdriver

sys.path.append("..")
import DataBase.DatabaseDAL
import Comm.Funs
import random
import global_Vars
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

num = global_Vars.startRowNum  #从第几行开始

def main():

    # 第一步，抓取艺人的最后url,入库
    print "开始获取每个艺人最后的url........".decode("utf8")
    getUrl()

    # # 第二步，根据上一步的url，抓取试听、粉丝、评论
    # print "\n开始抓取试听、粉丝、评论........".decode("utf8")
    # getData()




def getUrl():
    try:

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        sql = "select 原始姓名  from Table_Spider where id>={0} and 新浪_URL is null".format(num)
        list = dbDAL.query(sql)
        resultList=[]
        for (name,) in list:
            sleepTime = random.randint(5, 20)
            obj = _getUrl(name, True)
            if obj is not None:
                print "{0},粉丝：{1}，url:{2}".format(name,obj["新浪_粉丝数"],obj["新浪_URL"]).decode("utf8")
                obj["原始姓名"]=name
                resultList.append(obj)
            else:
                print "{0},没有url".format(name)
        dbDAL.update(tableName="Table_Spider",list=resultList,whereTuple=("原始姓名",))
    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()

def _getUrl(name,isFirst):

    time.sleep(5)
    url = "http://s.weibo.com/ajax/topsuggest.php"
    data = {'_k': '149560638462620', '_t': 1, '_v': 'STK_149560638462621', 'uid': '3202411913','retcode':'6102'}
    data['key'] = name
    data = urllib.urlencode(data)
    url += "?" + data
    cookiesStr = "SINAGLOBAL=4712863384112.549.1484556799232; SCF=Aprk0H9cB4KJmusCwJbnimW-dVST_B2Z_P1eONB8qwLJQiSU-pE3yF-3TFxFlRoEL9qZ_06nW0_h0vcf8fQgGss.; SUHB=0tKa1f4xBqMZqN; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhSE7ZDxGfRwWjO2TODnJ0Z5JpX5K2hUgL.FoeEehzXeK24eKe2dJLoIEnLxK-LB.zL1KqLxKBLB.eL1-qLxKqL1K-L1h-LxKBLB.2L12ikS057; UOR=database.51cto.com,widget.weibo.com,www.pythontip.com; ULV=1498180072846:17:1:1:1599765809467.4038.1498180072215:1495761192727"
    cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
    try:
        page = requests.get(url, cookies=cookiesJson, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36"})
    except:
        print "超时,1分钟后抓取，艺人：{0}".format(name)
        time.sleep(60)
        page = requests.get(url, cookies=cookiesJson, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
       # t page = requests.get(url, headers={
       #      "User-Agen": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
    str=page.text

    index_s = str.find('{"code"')
    index_e = str.find(');}catch(e){}')
    jsonStr = str[index_s:index_e]
    j = json.loads(jsonStr)

    userList=j["data"]["user"]
    if len(userList)>0:
        obj=userList[0]  # 目前取第一，不太准确。
        uid=obj["u_id"]
        fans=obj["fans_n"]
        url="http://weibo.com/u/{0}?topnav=1&wvr=6&topsug=1".format(uid)
        return {"姓名": name,"新浪_粉丝数":fans, "新浪_URL": url}
    else:
        if isFirst and len(name.split("乐")) > 1:
            # 在这里分割“乐”前面的字符
            return _getUrl(name.split("乐")[0], False)
        else:
            return None

def getData():
    driver = webdriver.Firefox(executable_path="D:\Python27\WorkSpace\ddd\geckodriver.exe")
    # driver.get("http://weibo.com/")

    # time.sleep(5)
    # driver.maximize_window()  # 浏览器全屏显示
    # userName=driver.find_element_by_id("loginname")
    # userName.click()
    # userName.send_keys("13540643543")
    # btn_password=driver.find_element_by_name("password")
    # btn_password.click()
    # btn_password.send_keys("liaowei123456")
    # time.sleep(3)
    # # 点击登陆按钮
    # bt=driver.find_element_by_class_name("btn_32px")
    # bt.click()

    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    sql = "select 姓名,新浪_URL  from Table_Spider where 新浪_URL is not null and id>={0}".format(num)
    # cookiesStr = "UOR=book.51cto.com,widget.weibo.com,www.hankcs.com; SINAGLOBAL=2552976350699.8384.1477980499736; ULV=1495593747334:3:1:1:7527490636867.572.1495593746920:1480060374093; login_sid_t=8956f5851dc03f309b70128b6bec7c76; _s_tentry=-; Apache=7527490636867.572.1495593746920; NSC_wjq_txfjcp_mjotij=ffffffff094113db45525d5f4f58455e445a4a423660; SCF=AqHYn1sVghF-jN4S-MgTtJAJ8yvVCLEqP9OsH8NtrSgbROA5yeBdUnre2jhDSQc4MqVWPds-4DAOa5bgkfQ1dzA.; SUB=_2A250IId7DeRhGeVM61AV8S_Fyj-IHXVXV_-zrDV8PUNbmtAKLROskW-Dlg51CzRaesul1-sw0LqTwa6-hg..; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WhSE7ZDxGfRwWjO2TODnJ0Z5JpX5K2hUgL.FoeEehzXeK24eKe2dJLoIEnLxK-LB.zL1KqLxKBLB.eL1-qLxKqL1K-L1h-LxKBLB.2L12ikS057; SUHB=0h15XLQOCxJ6wc; ALF=1496199588; SSOLoginState=1495594795; un=13540643543; wvr=6"
    # cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
    list = dbDAL.query(sql)
    updateList=[]
    for (name, url) in list:
        sleepTime = random.randint(2, 5)
        # driver.get("http://weibo.com/")
        time.sleep(sleepTime)
        values = []
        try:
            # driver = webdriver.PhantomJS(executable_path=r"D:\Python27\phantomjs-2.1.1-windows\bin\phantomjs.exe")

            driver.get(url)

            # driver.add_cookie(cookiesJson)
            time.sleep(10)
            table=driver.find_element_by_class_name("tb_counter")
            nodeList=table.find_elements_by_tag_name("strong")

            if(len(nodeList)>=3):
                obj={}
                updateList.append(obj)
                obj["新浪_关注数"]=nodeList[0].text
                obj["新浪_粉丝数"]=nodeList[1].text
                obj["新浪_微博数"]=nodeList[2].text
                obj["姓名"]=name
                print "{0},粉丝：{1}".format(obj["姓名"],obj["新浪_粉丝数"])
            else:
                print "跳过{0}".format(name)



        except Exception as e:
            print "***超时 {0}".format(name).decode("utf8")
            traceback.print_exc()


    dbDAL.update(tableName="Table_Spider",list=updateList,whereTuple=("姓名",))

    dbDAL.dispose()

if __name__=="__main__":
    main()