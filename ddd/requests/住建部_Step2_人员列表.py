# coding=UTF-8
from bs4 import BeautifulSoup
import sys
import requests
import time
sys.path.append("..")
import DataBase.DatabaseDAL

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

url="http://jzsc.mohurd.gov.cn/dataservice/query/comp/regStaffList/" ##人员列表页面
getJson={"姓名":"uu_Name","身份证号":"uu_ShenFenZheng"}
sleepTime=6 #请求间隔5秒
# 先清空表

def main():
    #获得上一步数据
    try:
        dbDAL = DataBase.DatabaseDAL.DatabaseDAL()
        # sql=" select * from Tab_ZJB_Company_Temp2 where not exists("
        # sql+=" select * from Tab_ZJB_LiuShui_User where uu_Company_Code=co_Company_Code) and co_Company_Code not in(select company_code from Tab_ZJB_Temp_Company_NoUser) "
        sql="  select * from dbo.Tab_ZJB_Company_Temp2  WHERE co_Company_Code IN(select company_code from dbo.Tab_ZJB_Temp_Company_NoUser where type='time out')";
        list=dbDAL.query(sql)
        resultList=[]
        # 先清空表
     #   dbDAL.execute(sql="truncate table Tab_ZJB_LiuShui_User")
        num=0
        for (co_Id,co_XinYongCode,co_QiYeMingCheng,co_FaRen,co_ZhuCeDi,co_Href,co_Company_Code,CO_Address) in list:
            #开始遍历每一家公司
            time.sleep(sleepTime)
            #001704270034042907
            params = {'$total': 1000, '$reload': 0, '$pg': 1, '$pgsz': 1000}
            r=""
            bsObj=""
            try:
                r=requests.post(url+co_Company_Code,data=params)
                bsObj = BeautifulSoup(r.text,"html.parser")
            except Exception as e:
                print e.message
                print "超时，等待10分钟,co_Company_Code={0}".format(co_Company_Code).decode("utf8")
                time.sleep(600)
                try:
                    r = requests.post(url + co_Company_Code, data=params)
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "再超时，跳过,co_Company_Code={0}".format(co_Company_Code).decode("utf8")
                    dbDAL.insert(tableName="Tab_ZJB_Temp_Company_NoUser",
                                 list=[{"company_code": co_Company_Code, "type": "time out"}])
                    continue
            table=bsObj.find(name="table")
            if table is None:
                continue
            trs=table.find(name="tbody").findAll(name="tr")
            i = 0
            for tr in trs:
                #开始遍历一家公司的人员
                obj={}
                try:
                    if len(tr.findAll(name="td"))<=1 and i==0 :
                        #没有人员。
                        print "没有注册人员，跳过,co_Company_Code={0}".format(co_Company_Code).decode("utf8")
                        dbDAL.insert(tableName="Tab_ZJB_Temp_Company_NoUser", list=[{"company_code":co_Company_Code,"type":"no users"}])
                        break
                    obj["uu_Company_Code"]=co_Company_Code
                except ValueError, Argument:
                    print Argument
                    continue
                uid=""
                try:
                    onclicks=tr.find(name="td",attrs={"data-header":"姓名"}).find(name="a").attrs["onclick"].split("/")
                    uid=onclicks[len(onclicks)-1].replace("'","")   ## 去掉最后的单引号
                except Exception as e:
                    print e.message
                obj["uu_Code"] = uid
                for key in getJson.keys():
                    value=getJson[key]
                    td=tr.find(name="td",attrs={"data-header":key})
                    name =""
                    if td is not None:
                        name = td.get_text().strip()
                        name=name.decode("utf8")
                    else:
                        name = list[i][value]
                    obj[value]=name
                resultList.append(obj)
                print "{0} {1} len={2}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                               obj["uu_Name"], len(resultList)+(num*100)).decode("utf8")
                i+=1
                # 存数据库，每100条存一次
                if len(resultList)==100:
                    print "{0} 开始入库....... ".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))).decode("utf8")
                    dbDAL.insert(tableName="Tab_ZJB_LiuShui_User", list=resultList)
                    resultList=[]
                    num+=1

        dbDAL.insert(tableName="Tab_ZJB_LiuShui_User", list=resultList)

    except Exception as e:
        print "错误：{0}".format(e.message).decode("utf8")
    else:
        print "+++++++++++++++++++++++++ 成功！".decode("utf8")
    finally:
        # 销毁
        dbDAL.dispose()





if __name__=="__main__":
    main()