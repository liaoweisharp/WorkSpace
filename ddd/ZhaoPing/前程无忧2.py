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

    try:
        ##需要改数据库名
        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=global_Vars.global_DataBase)
        #清空表
       # dbDAL.execute("TRUNCATE TABLE Tab_ODS_Users")
        #cookiesStr = "guid=1497948075960700029; EhireGuid=ad1743d5ef71411abea3a9919236775a; slife=lowbrowser%3Dnot%26%7C%26; search=jobarea%7E%60090200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0100%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243903%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243816%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21collapse_expansion%7E%601%7C%21; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0Bs4p00uiAsaKX3Fu000000IML1300000UsbDig.THLZ_Q5n1VeHksK85yF9pywdpAqVuNqsusK15y7-PH0zrj0knj0sPj0Lm1n0IHYdPDRLfHR1PDf3wW9An16sPYR4wjfkrRwanWn1PW6sn0K95gTqFhdWpyfqn10krjbsPHfkPzusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqrH01rf%2526tpl%253Dtpl_10085_15730_1%2526l%253D1054828295%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m7ad13823%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D25%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dbaiduhome_pg%2526inputT%253D4670%26%7C%26adsnum%3D789233; 51job=cenglish%3D0; ASP.NET_SessionId=oxdzaib0500iviieu32xbfom; LangType=Lang=&Flag=1; HRUSERINFO=CtmID=109776&DBID=1&MType=02&HRUID=2788209&UserAUTHORITY=1000110000&IsCtmLevle=1&UserName=siteqi-xinan&IsStandard=1&LoginTime=08%2f10%2f2017+09%3a19%3a56&ExpireTime=08%2f10%2f2017+09%3a29%3a56&CtmAuthen=0000011000000001000111010000000011100011&BIsAgreed=true&IsResetPwd=0&CtmLiscense=11&AccessKey=308584e21218da5c; AccessKey=825078f696694f0"
        cookiesStr = "guid=1497948075960700029; EhireGuid=ad1743d5ef71411abea3a9919236775a; slife=lowbrowser%3Dnot%26%7C%26; search=jobarea%7E%60090200%7C%21ord_field%7E%600%7C%21recentSearch0%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0100%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243903%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21recentSearch1%7E%601%A1%FB%A1%FA090200%2C00%A1%FB%A1%FA000000%A1%FB%A1%FA0000%A1%FB%A1%FA00%A1%FB%A1%FA9%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA99%A1%FB%A1%FA%A1%FB%A1%FA2%A1%FB%A1%FA%A1%FB%A1%FA-1%A1%FB%A1%FA1502243816%A1%FB%A1%FA0%A1%FB%A1%FA%A1%FB%A1%FA%7C%21collapse_expansion%7E%601%7C%21; nsearch=jobarea%3D%26%7C%26ord_field%3D%26%7C%26recentSearch0%3D%26%7C%26recentSearch1%3D%26%7C%26recentSearch2%3D%26%7C%26recentSearch3%3D%26%7C%26recentSearch4%3D%26%7C%26collapse_expansion%3D; adv=adsnew%3D0%26%7C%26adsresume%3D1%26%7C%26adsfrom%3Dhttp%253A%252F%252Fbzclk.baidu.com%252Fadrc.php%253Ft%253D06KL00c00fZEOkb0Bs4p00uiAsaKX3Fu000000IML1300000UsbDig.THLZ_Q5n1VeHksK85yF9pywdpAqVuNqsusK15y7-PH0zrj0knj0sPj0Lm1n0IHYdPDRLfHR1PDf3wW9An16sPYR4wjfkrRwanWn1PW6sn0K95gTqFhdWpyfqn10krjbsPHfkPzusThqbpyfqnHm0uHdCIZwsrBtEIZF9mvR8PH7JUvc8mvqVQLwzmyP-QMKCTjq9uZP8IyYqP164nWn1Fh7JTjd9i7csmYwEIbs1ujPbXHfkHNIsI--GPyGBnWKvRjFpXycznj-uURusyb9yIvNM5HYhp1YsuHDdnWfYnhf3mhn4PHK-PHbvmhnYPWD4mvm4nAuhm6KWThnqrH01rf%2526tpl%253Dtpl_10085_15730_1%2526l%253D1054828295%2526attach%253Dlocation%25253D%252526linkName%25253D%252525E6%252525A0%25252587%252525E9%252525A2%25252598%252526linkText%25253D%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252525E5%252525BF%252525A7%252851Job%2529-%252525E6%25252589%252525BE%252525E5%252525B7%252525A5%252525E4%252525BD%2525259C%252525E5%252525B0%252525BD%252525E5%2525259C%252525A8%252525E5%25252589%2525258D%252525E7%252525A8%2525258B%252525E6%25252597%252525A0%252526xp%25253Did%2528%25252522m7ad13823%25252522%2529%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FDIV%2525255B1%2525255D%2525252FH2%2525255B1%2525255D%2525252FA%2525255B1%2525255D%252526linkType%25253D%252526checksum%25253D25%2526wd%253D%2525E5%252589%25258D%2525E7%2525A8%25258B%2525E6%252597%2525A0%2525E5%2525BF%2525A7%2526issp%253D1%2526f%253D8%2526ie%253Dutf-8%2526rqlang%253Dcn%2526tn%253Dbaiduhome_pg%2526inputT%253D4670%26%7C%26adsnum%3D789233; 51job=cenglish%3D0; ASP.NET_SessionId=hzzrayyibdl3gym45wumju5o; LangType=Lang=&Flag=1; HRUSERINFO=CtmID=109776&DBID=1&MType=02&HRUID=2788209&UserAUTHORITY=1000110000&IsCtmLevle=1&UserName=siteqi-xinan&IsStandard=1&LoginTime=08%2f10%2f2017+14%3a23%3a22&ExpireTime=08%2f10%2f2017+14%3a33%3a22&CtmAuthen=0000011000000001000111010000000011100011&BIsAgreed=true&IsResetPwd=0&CtmLiscense=11&AccessKey=b6dfad4315938fd1; AccessKey=3ee80454d963473"
        cookiesJson = Comm.Funs.strConvertDic(cookiesStr)
        # url = 'http://ehire.51job.com/Navigate.aspx?ShowTips=11&PwdComplexity=N'
        # r = requests.get(url,cookies=cookiesJson, verify=False, headers={
        #     "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.115 Safari/537.36"})
        url = "http://ehire.51job.com/Candidate/SearchResumeNew.aspx"

        data={}
        data["__EVENTTARGET"]="pagerBottomNew$nextButton"
        data["__EVENTARGUMENT"] = ""
        data["__LASTFOCUS"] = ""
        #data["__VIEWSTATE"]="/wEPDwULLTE0NzQ1NjY2OTYPFg4eBElzRU5oHhB2c1NlbGVjdGVkRmllbGRzBTNBR0UsV09SS1lFQVIsU0VYLEFSRUEsV09SS0ZVTkMsVE9QREVHUkVFLExBU1RVUERBVEUeCFBhZ2VTaXplAjIeDHN0clNlbGVjdENvbAUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHglQYWdlSW5kZXgCBR4IUGFnZURhdGEFhhEyMDF8NDAwfDIwMHw1MDAwfDkyMzY4NDU4LDMxODM0NDQxOSwzNjQ2NDIxNTEsMzYzOTUzNjQ2LDU4NjQ2NDE1LDcyMzg5NzMwLDc0MTU1Njg0LDM2NDYzOTg2OSwzMjc1MDg0OTEsMzE4NzI4OTY0LDMzNjg2MzA1MiwzMTI4MDc2MDksMjQ2MjkzMTEsMzY0NDcyODY3LDM0NDM4NDM1NywzMDg1NzUwMTAsMzU3MDk2Njc3LDM2MTE1MjEzMSw2NDM0NTk4OSwzMTc0MjcxNjMsMzM4NzA4ODIwLDcwNjk3Mjc5LDUzMjcwNTAzLDM1ODM0NDc3NCwzNTgwMDMwOTEsMzEwMjIzMjQzLDM2NDMwNTYxNiwzNjMwNDMyODAsMzMzMzQyNTE4LDMxNzgyMzE5NiwzMjUxNjcxOTcsODIyMDQ3MjUsODA2MzkxNzUsMzM3NTcyNzQ1LDM2Mzk5MDY1OCwzNDg4NDk1MjUsOTQ4NzUyMzAsMzU2OTAwOTk2LDM2NDA2NTI5OSwzNjQzNTc1MDEsMzU1NzgzMTY0LDMyNzgzNjIwMCwzMDc2OTExNjUsMzYxNTMwMzIzLDMzNTY3MzM3MiwzMTE3ODcwNDAsNjMxMDY5MDYsMzY0NjIyNjM0LDkxMDE0MzIzLDMyMTg5MzI1OSwzNTI2NTQ5NjEsMzU1MDkxNjg1LDM2MzYwMjE0MCwzNjQ0NjY4NTcsMjQ5MjQ4NjEsMzY0NjI2MDA1LDM1ODIyMjk2NCwzNTM1MDcyMjQsMzUwOTMzNjQ4LDM2NDMwNTY3NCwzMzY4MzUzNDEsMzY0NjM1OTE1LDM0MTk3MzU4NCwzNDc2ODY4MDMsODA1ODE5MDYsMzY0MTYzOTk5LDM2MzgxMDAwMSwzMzAyMDcwNDYsMzIyNDg1OTc2LDMyNTEyMjI0MiwzMDg4NjEzNDcsMzU2MTIzODUwLDMxMzgyOTkyNCwzNDI1NzM2OTIsMzEyMTg1MjI3LDMwODM1NDM1MSwzNjQwNjcyNDUsMzYzODYxMzgxLDMwNjMxNTMyNiwzNjM1NzAxODIsMzY0MTI5MzUyLDMzNzI5MTAwMSwzNjM2NDc2MDgsMzU0ODM3MjI5LDM1OTYxODE3NiwzNTMwNjczOTMsMzYzMjE4Njc4LDM2NDMyMjg4MiwzMjAzMzkxMjEsMzYxOTg5OTY4LDM1MTY0NTEwMywzNjQ2MzU4MDQsMzYyNzMxNjkwLDM2NDEyNTcxOSw1NDU3MDMwMiwzNTM3MzQwODAsMzI0OTQyMDI3LDM0MzE5NzI2MSwzNjI1NjM2MzIsMzYxMTA3ODEzLDM0MDc4ODI0OCw4NTA1MTM5NCwzNjQyNTY3ODYsMzUwNTc1MjI4LDM2NDUxNjUwOCwzNTgwNjUxNzEsMzEzNjgzODk0LDM2NDMxMjg4MSwzNjE5OTE5MjgsMzM4NjMwNTA5LDcwNzM5NDQyLDM1NTU4ODY2MSwzNTc3ODY0NTYsMzQ4ODU0ODQ5LDMxNDk5NDE3NSwzNDgzNzc0MTIsMzYzODAyMzgzLDM2NDYzNDI1MCwzNjQyNjQ1MTUsMzAyNDc5OTY5LDM1NTU1NzY0MiwzMTI5NjU3OTEsMTMyMTU4MzAsMzU1NTczMDQ2LDM0MTg5NjY3OCw1ODY4NzgxNywzNjE2MjczMDgsNjg2NDEyODgsMzUxNTQyNTY5LDM2NDYyOTQ3NywzMzExNDgxNDgsMzYzNTExMDAyLDM0Mzk4OTQ5OSw4NzM1OTQ1OSwzMzQyNjY5NDgsMzYzNTY4MDQ2LDMwMDQ0NjY2MiwzNjI3MTcyMTIsMzI4MDQ3MDMwLDMwOTM0MjkzOSwzMDAyMzI3NjYsMzYzODI3MTAxLDM2MzY4NDM4NiwzNjQ0MTI3MDUsNTE5ODQzOTUsNTQ4NzY0MDksMzIzNTI3MjM2LDM1MTE5NDU4NSwzNTU4MjI4MjAsMzUwNTU1Nzc0LDMyMjAyMjU4OCwzNjQzNDc2MjQsMTkzMTY2NDksMzY0MjQxNDcwLDM2NDM2ODQxNyw5MTIyMDI3MywzNjQ2MzI4MTIsMzQ5NDU1ODE3LDM0OTYxODgxNiwzNjM4MDc4MDYsNzgwMDE5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"
        data["_VIEWSTATE"]="/wEPDwULLTE0NzQ1NjY2OTYPFg4eBElzRU5oHhB2c1NlbGVjdGVkRmllbGRzBTNBR0UsV09SS1lFQVIsU0VYLEFSRUEsV09SS0ZVTkMsVE9QREVHUkVFLExBU1RVUERBVEUeCFBhZ2VTaXplAjIeDHN0clNlbGVjdENvbAUzQUdFLFdPUktZRUFSLFNFWCxBUkVBLFdPUktGVU5DLFRPUERFR1JFRSxMQVNUVVBEQVRFHglQYWdlSW5kZXgCBB4IUGFnZURhdGEF9RAyMDF8NDAwfDIwMHw1MDAwfDUwNjI2MjU5LDY0NjA5MTc1LDM1NDY4ODM4Nyw2ODM0NTA3NiwzMTQ5MjgxMzUsMzY0NjQwODI4LDMwMzkyOTg0MCwzNjQ2MjIwNDQsMzUzNDg5MTEyLDgyODc0MjkzLDMyNjQ0NDY3OCwzMjAxNjMyNzEsMzU3NDA3OTY2LDM2NDYxNTcxNCw4MDUwNjMwNCwzNTk1NDQyNjIsMzYyNzc3Njg3LDM1OTI5Njg1OCwzMDI0ODI2MjcsMzU3ODE2NTE1LDM2MjY2ODAyNiw5MTY0NzM1MywzMDg0NTg2NjksMzYzODI5MTcwLDM0MTA2MDMxMywzNjM3NzQzNjYsMzUzNjA4OTUwLDMyNzk5ODg1OSwzNjM2ODQwMDUsOTM0MTg5ODcsMzYyNzU4NTQyLDMyNTk5NDAwNSwzMzc3MzkzNzUsMzYwNzcwMjE3LDExMjA5ODQ2LDE1OTc4MDg0LDU3NzY4OTAxLDMzNDU1NzcxNCwzNjA5ODgxMzQsNTUxNTQzNDMsMzY0NDI3NzY2LDMxNzIzMTUyMywzMDI4NjExNDEsMzIzNzI2MjQxLDM2MDY4OTUwNCwzNDU3MTE3NTAsMzMzNTg2MTIwLDM2MzkzNTExNywzMzM2NjczNzAsMzAyMTAwNjQ0LDQ5MDc4MDc3LDM2NDI5MjAwOCw4OTU3ODk1Niw5NDMwMTY1NCwxMTk5MDQ3LDc3NDc4MDEyLDMwMTQ0MzUwNiwzMTM4ODYyODMsMzU2NzkyMDQzLDM2NDU4MTEwOCwzMDQyMTIyNDIsNzg0OTA1MzEsMzU0MDI2MTk3LDM2MjIzNTg1NSwzMTI1MDMyOTYsODQzOTYzOCwzNjE4Mjc5NzksNTY3ODE1MTQsMzY0MTYyNjIyLDM1NDY1MDc4MywzMjQ1NTU4MDEsODI4NjI0NTYsNzk4NDc4MjIsMzY0NTk0NzUxLDM2NDYwNzMxMCwxNzQ4MDU5MiwzMDM0NDkxMjQsMzY0NjQ5MjQ5LDM2NDU1Nzg0MCwzNTE5NzUzMjYsMzYzNzExMTE3LDMyMjI5ODE0NSw4NTc5MzE4MiwzNjMwNTUxMzEsMzI0NjgwNTczLDgxNjM4NTU4LDMxMTkyNjE0NiwxMDQxNzU1OCwxNTk0NzI2NCwzNjMyNDU2NDgsMzY0NjQ3NTc3LDM2NDY0NTY2OCwzNjA3NTEyNDUsMzYzMjUyNzU4LDcyOTY0NTQwLDM2MjEzNzYzMywzNjEwMjEwNzQsMzY0NDQ5NjEwLDM2NDU5NzA2OCwzMzY1MTY3MDcsODQyNDAwNTksMzY0MTk1ODE4LDMzOTU4NjkwOSwzNTY3NDEwMTcsMzI0Mzk2MzAwLDMwMjE0Mjc5Myw2MjQ1Nzk2NSwzMDY0Mjg3NTMsMzI4ODkyMzY1LDMxNTk0NzE0NCw5Njg0ODA3NCwzNjExOTI5MDYsMzU1MzMwNDgxLDM0OTgwNDUyNCw5MTI3MDg4NiwzNTk0Njc0ODgsMzI1NTU2MzM0LDU4OTQwNzQzLDMwMzE1Mjc0OSwzNjQyMTA1MzYsMzAyNjEwNDE1LDM1NzA3NDAyMiwzNTY2NDI0OTAsMzY0NjM4NTc1LDM2MzA4NTcwNiwzNjQzNTYwMTgsMzQ1Nzc3ODI2LDM1MzM0MDA3MSwzMTAzMzEwMjcsMzAzODY3NzUwLDMyNzEzNTQ3OSwzNjQxNzUxNjQsMzU5NDA2OTg5LDM1NjY1MTA4OCw4MzgwNzE3MCw1Mzg5MTY4NSwzNjQzNzg0NDAsODE4NDUyODksMzQ0NjA1NjUyLDMxMTk5MTQ4MiwzNjQ1Njg0MzUsNzYxODcxNSwzNjAxODcxNTUsNzU3MDY3ODUsMzY0NjI1NTMxLDMxOTU4OTQ1Myw5MjM2ODQ1OCwzNjQ2NDIxNTEsMzYzOTUzNjQ2LDU4NjQ2NDE1LDcyMzg5NzMwLDc0MTU1Njg0LDMyNzUwODQ5MSwzMTg3Mjg5NjQsMzM2ODYzMDUyLDMxMjgwNzYwOSwyNDYyOTMxMSwzNjQ0NzI4NjcsMzQ0Mzg0MzU3LDMwODU3NTAxMCwzNTcwOTY2NzcsMzYxMTUyMTMxLDY0MzQ1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"
        data["ctrlSerach$search_keyword_txt"]=""
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
        data["hidCheckUserIds"] = "514621606,511100260,565607419,568868852,48950906,568648640,512447607,515106087,510958321,568504277,556254226,568654610,587937767,583628844,20130545,568768638,565272646,550405725,544824575,541747123,502270222,516747849,575252587,584138333,574724082,502521156,568066120,565270166,506574185,565133363,568752153,553499646,565686241,518256088,519675375,515066234,565475271,568546863,540562386,567932601,517684344,568653847,564360329,568744018,18133143,515360659,548986682,585796106,564168293,567705914"
        data["hidCheckKey"] = "90609fac4d77bfa6ee56301ed3df1dd1"
        data["hidEvents"] = ""
        data["hidNoSearchIDs"] = ""
        data["hidBtnType"] = ""
        data["hideMarkid"] = ""
        data["hidStrAuthority"] = "0"
        data["hidDownloadNum"] = "4"
        data["hidKeywordCookie"] = ""
        data["showGuide"]=""

        r = requests.post(url, data=data, cookies=cookiesJson, verify=False, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        bsObj = BeautifulSoup(r.text, "html.parser")
        print r.text
        return
        viewState=bsObj.find(id="__VIEWSTATE").attrs["value"]
        maxPage=bsObj.find(id="pagerBottomNew_btnNum_ma").get_text()
        num=1
        while num<=maxPage:
            time.sleep(random.randint(2, 6))
            try:
                print "page={0},hidAccessKey:{2},hidCheckKey={3},  viewState={1}".format(num,data["__VIEWSTATE"],data["hidAccessKey"],data["hidCheckKey"])
                r = requests.post(url, data=data, cookies=cookiesJson, verify=False, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(r.text, "html.parser")
                objList=getObj(bsObj)
            except:
                traceback.print_exc()
                time.sleep(random.randint(6, 10))
            else:
                if objList is not None and len(objList)>0:
                    print "入库中....{0}个, num/maxPage={1}/{2}".format(len(objList), num, maxPage).decode("utf8")
                    dbDAL.insert(tableName="Tab_ODS_Users", list=objList)
                    objList=[]
                elif objList is None:
                    print "objList is None . Page={0}".format(num)
                else:
                    print "objList 0 个元素. Page={0}".format(num)
                num += 1
                viewState = bsObj.find(id="__VIEWSTATE").attrs["value"]
                hidCheckKey=bsObj.find(id="hidCheckKey").attrs["value"]
                data["__VIEWSTATE"] = viewState
                data["__EVENTTARGET"]="pagerBottomNew$nextButton"
                data["hidCheckKey"]=hidCheckKey
                data["hidAccessKey"]=bsObj.find(id="hidAccessKey").attrs["value"]
                data["hidShowCode"] = bsObj.find(id="hidShowCode").attrs["value"]
                data["hidDisplayType"] =  bsObj.find(id="hidDisplayType").attrs["value"]
                # data["hidEhireDemo"] = ""
                # data["hidUserID"] = ""
                data["hidCheckUserIds"] =bsObj.find(id="hidCheckUserIds").attrs["value"]
                # data["hidEvents"] = ""
                # data["hidNoSearchIDs"] = ""
                # data["hidBtnType"] = ""
                # data["hideMarkid"] = ""
                data["hidStrAuthority"] = bsObj.find(id="hidStrAuthority").attrs["value"]
                data["hidDownloadNum"] = bsObj.find(id="hidDownloadNum").attrs["value"]
                # data["hidKeywordCookie"] = ""
                # data["showGuide"] = ""

                data["__EVENTTARGET"] = "pagerBottomNew$btnNum{0}".format(num)

    except:
        traceback.print_exc()
def getObj(bsObj):
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
            objList.append(obj)
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
    return objList


if __name__=="__main__":
    main()