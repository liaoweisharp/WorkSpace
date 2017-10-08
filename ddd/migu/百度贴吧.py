# coding=UTF-8
import sys
import time
import traceback

import requests
from bs4 import BeautifulSoup

sys.path.append("..")
import DataBase.DatabaseDAL
import random
import global_Vars
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

num = global_Vars.startRowNum  #从第几行开始


def main():

    # 第一步，抓取艺人的最后url,入库
    print "获取最大页数......".decode("utf8")
    #maxPag=geteMaxPage()
    maxPage=50  #目前只抓50页
    if maxPage is None:
        print "*** 总页数出错".decode("utf8")
        return

    dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
    ## 先清空数据表
    dbDAL.execute("TRUNCATE TABLE Table_BaiDu_TeiBa")
    dbDAL.dispose();

    print "总页数为:{0}页".format(maxPage)
    print "开始获取内地明星 会员数........".decode("utf8")
    url="http://tieba.baidu.com/sign/index?kw=%D5%C5%F6%A6%D3%B1&type=3"
    getData(maxPage,url)
    print "总页数为:{0}页".format(maxPage)
    print "开始获取 港台东南亚明星 会员数........".decode("utf8")
    url = "http://tieba.baidu.com/sign/index?kw=%C1%F5%B5%C2%BB%AA&type=3"
    getData(maxPage,url)




def getData(maxPage,url):
    try:
        pageNum=1
        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database="MiGu")
        while pageNum<=maxPage:
            try:
                resultList=[]

                url = url+"&pn={0}".format(pageNum)
                sleepTime = random.randint(2, 5)
                time.sleep(sleepTime)
                page = requests.get(url, headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
                bsObj = BeautifulSoup(page.text, "html.parser")
                trs= bsObj.findAll(name="tr",attrs={"class":"j_rank_row"})
                for tr in trs:
                    obj = {}
                    obj["orderNum"]=tr.find(attrs={"rank_index"}).get_text().strip() ## 排名
                    obj["name"] = tr.find(attrs={"forum_name"}).get_text().strip()   ##姓名
                    obj["qianDaoNum"] = tr.find(attrs={"forum_sign_num"}).get_text().strip()  ## 签到数
                    obj["huiYuanShu"] = tr.find(attrs={"forum_member"}).get_text().strip()    ## 会员数
                    obj["type"] = "月排名"
                    print "排名：{0}，姓名：{1}，签到人数:{2},会员数:{3}".format(obj["orderNum"],obj["name"],obj["qianDaoNum"],obj["huiYuanShu"]).decode("utf8")
                    resultList.append(obj)
            except:
                print "*** 第{0}页异常，等待几分钟....".format(pageNum).decode("utf8")
                time.sleep(random.randint(8,20))
                pass
            else:
                print "入库中,第{0}页......".format(pageNum).decode("utf8")
                dbDAL.insert(tableName="Table_BaiDu_TeiBa", list=resultList)
                pageNum += 1

    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()

def getMaxPage():
    ## 先获得总页数
    url = "http://tieba.baidu.com/sign/index?kw=%D5%C5%F6%A6%D3%B1&type=3&pn=1"
    sleepTime = random.randint(2, 5)
    time.sleep(sleepTime)
    try:
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.99 Safari/537.36"})
        bsObj = BeautifulSoup(page.text, "html.parser")
        div=bsObj.find(name="div",attrs={"class","pagination"})
        aNodes=div.findAll(name="a")
        aLast=aNodes[len(aNodes)-1]
        href=aLast.attrs["href"]
        maxPage=href.split("&pn=")[1]
        return int(maxPage)

    except:
        return None





if __name__=="__main__":
    main()