#!/user/bin/env python
# coding:utf-8



import json
import sys
import time
import traceback
import urllib

import datetime
import requests
from bs4 import BeautifulSoup
from logger import logger

sys.path.append("..")
import DataBase.DatabaseDAL_Oracle
import random
import global_Vars
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
app_Id=1 #appId  QQ
pageSize=20
def main():
    dbDAL = DataBase.DatabaseDAL_Oracle.DatabaseDAL()

    list=dbDAL.query("select * from Tab_Phone_Songs1 where song_Name is not null")
    for obj in list:
        print obj[1]

    obj = {"id": 7, "song_Name": u"心爱的姑娘3", "singer": u"周杰伦3", "app_1": "1"}

    objList = []
    objList.append(obj)
    dbDAL.update(tableName="Tab_Phone_Songs1",list=objList,whereTuple=("id",))

    # obj={"id":u"SEED_Tab_Phone_Songs1","song_Name":u"心爱的姑娘2","singer":u"周杰伦","app_1":"1"}
    # objList=[]
    # objList.append(obj)
    # dbDAL.insert(tableName="Tab_Phone_Songs1", list=objList,sequenceList=["id"])

# ##以下查询某个日期是第多少周##
# def getweekmsg(strdate):
#     _datetime = datetime.datetime.strptime(strdate, '%Y%m%d')
#     weekmsg = _datetime.isocalendar()
#     print weekmsg
#     ####strdate为字符串格式，如20140828  输出为(2014, 35, 4)
#
#
# # weekflag格式为201435（即2014年第35周）
# def getfirstday(weekflag):
#     yearnum = weekflag[0:4]  # 取到年份
#     weeknum = weekflag[4:6]  # 取到周
#     stryearstart = yearnum + '0101'  # 当年第一天
#     yearstart = datetime.datetime.strptime(stryearstart, '%Y%m%d')  # 格式化为日期格式
#     yearstartcalendarmsg = yearstart.isocalendar()  # 当年第一天的周信息
#     yearstartweek = yearstartcalendarmsg[1]
#     yearstartweekday = yearstartcalendarmsg[2]
#     yearstartyear = yearstartcalendarmsg[0]
#     if yearstartyear < int(yearnum):
#         daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 1) * 7
#     else:
#         daydelat = (8 - int(yearstartweekday)) + (int(weeknum) - 2) * 7
#     result=[];
#     a = (yearstart + datetime.timedelta(days=daydelat)).date()
#     for i in range(7):
#         result.append((a+datetime.timedelta(days = i)).strftime('%Y%m%d'))
#     return result


if __name__ == '__main__':
   main()