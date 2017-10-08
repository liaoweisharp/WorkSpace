
# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import sys
import requests
import time
sys.path.append("..")
import DataBase.DatabaseDAL

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
#sys.setdefaultencoding('GB2312')  #解决乱码问题

url="http://jzsc.mohurd.gov.cn/dataservice/query/comp/caDetailList/" ##公司资质页面
getJson={"资质类别":"zz_LieBie_Name","资质证书号":"zz_ZhengShuHao","资质名称":"zz_Name","发证日期":"zz_FaZheng_Date","证书有效期":"zz_YouXiao_Date","发证机关":"zz_FaZhengJiGuan"}
sleepTime=5 #请求间隔5秒

def main():
    #获得上一步数据
    try:
        dbDAL = DataBase.DatabaseDAL.DatabaseDAL()
        sql="select top 2 * from Tab_ZJB_Company_Temp2"
        list=dbDAL.query(sql)
        resultList=[]
        # 先清空表
        dbDAL.execute(sql="truncate table Tab_ZJB_LiuShui_CompanyZiZhi")
        for (co_Id,co_XinYongCode,co_QiYeMingCheng,co_FaRen,co_ZhuCeDi,co_Href,co_Company_Code,CO_Address) in list:
            #开始遍历每一家公司
            time.sleep(sleepTime)
            r=requests.get(url+co_Company_Code)
            bsObj = BeautifulSoup(r.text,"html.parser")
            table=bsObj.find(name="table",attrs={"id":"catabled"})
            if table is None:
                continue
            trs=table.find(name="tbody").findAll(name="tr")
            i = 0
            for tr in trs:
                #开始遍历一家公司的所有资质
                obj={}
                if len(tr.findAll(name="td"))<=1 and i==0 :
                    #没有资质，直接跳过这个公司。
                    break
                obj["zz_Company_Code"]=co_Company_Code
                for key in getJson.keys():
                    value=getJson[key]
                    td=tr.find(name="td",attrs={"data-header":key})
                    name =""
                    if td is not None:
                        name = td.get_text().strip()
                    else:
                        name = list[i][value]
                    obj[value]=name
                resultList.append(obj)
                print "{0} {1} len={2}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                               obj["zz_Company_Code"], len(resultList))
                i += 1
                # 存数据库，每10000条存一次
                if len(resultList)==10000:
                    print "{0} 开始入库....... ".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))).decode("utf8")
                    dbDAL.insert(tableName="Tab_ZJB_LiuShui_CompanyZiZhi", list=resultList)
                    resultList=[]

        dbDAL.insert(tableName="Tab_ZJB_LiuShui_CompanyZiZhi", list=resultList)
    except Exception as e:
        print e.message
    else:
        print "+++++++++++++++++++++++++++++"+"成功！".decode("utf8")
    finally:
        # 销毁
        dbDAL.dispose()





if __name__=="__main__":
    main()