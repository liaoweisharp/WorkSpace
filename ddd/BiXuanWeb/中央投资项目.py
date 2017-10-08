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

def main():
    url="http://www.ctba.org.cn/zt/zgglpt/map.jsp"
    try:
        r = requests.get(url, headers={
            "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8"
            ,"Accept-Encoding":"gzip, deflate"
            ,"Accept-Language":"zh-CN,zh;q=0.8"
            ,"Cache-Control":"max-age=0"
            ,"Connection":"keep-alive"
            ,"Cookie":"Hm_lvt_e082f8f19c492b003e7ac36caadd5ee3=1502331196,1502414362; JSESSIONID=agj4NZaGRR5e"
            ,"Host":"www.ctba.org.cn"
            ,"Upgrade-Insecure-Requests":"1"
            ,"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        bsObj = BeautifulSoup(r.text, "html.parser")
        objList=[]
        block=bsObj.find(id="block1")
        nodeA=block.findAll(name="a")
        print ""
        print "------- 甲级 ---------"
        print ""
        for node in nodeA:
            print node.get_text()


        block = bsObj.find(id="block2")
        nodeA = block.findAll(name="a")
        print ""
        print "------- 乙级 ---------"
        print ""
        for node in nodeA:
            print node.get_text()

        block = bsObj.find(id="block3")
        nodeA = block.findAll(name="a")
        print ""
        print "------- 暂定级 ---------"
        print ""
        for node in nodeA:
            print node.get_text()

    except Exception as e:
        print e.message
        print "***再超时".decode("utf8")

if __name__ == "__main__":
    main()