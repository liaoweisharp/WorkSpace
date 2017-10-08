# coding=UTF-8
from bs4 import BeautifulSoup
import sys
import requests
import time
sys.path.append("..")
import DataBase.DatabaseDAL

reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

url="http://jzsc.mohurd.gov.cn/dataservice/query/staff/staffDetail/" ##一个人员页面
getJson={"姓名":"uu_Name","身份证号":"uu_ShenFenZheng"}
sleepTime=6 #请求间隔5秒
# 先清空表

def main():
    #获得上一步数据
    try:
        dbDAL = DataBase.DatabaseDAL.DatabaseDAL()
        # sql=" select * from Tab_ZJB_Company_Temp2 where not exists("
        # sql+=" select * from Tab_ZJB_LiuShui_User where uu_Company_Code=co_Company_Code) and co_Company_Code not in(select company_code from Tab_ZJB_Temp_Company_NoUser) "
        sql=" SELECT uu_Code,uu_Name FROM dbo.Tab_ZJB_LiuShui_User";
        list=dbDAL.query(sql)
        resultList=[]
        # 先清空表
     #   dbDAL.execute(sql="truncate table Tab_ZJB_LiuShui_User")
        num=0
        for (uu_Code,uu_Name) in list:
            #开始遍历一个人的所有资格证

            time.sleep(sleepTime)
            r=""
            bsObj=""
            try:
                r=requests.get(url+uu_Code)
                bsObj = BeautifulSoup(r.text,"html.parser")
            except Exception as e:
                print e.message
                print "超时，等待10分钟,uu_Code={0}".format(uu_Code).decode("utf8")
                time.sleep(600)
                try:
                    r = requests.get(url + uu_Code)
                    bsObj = BeautifulSoup(r.text, "html.parser")
                except Exception as e:
                    print e.message
                    print "再超时，跳过,uu_Code={0}".format(uu_Code).decode("utf8")
                    dbDAL.insert(tableName="Tab_ZJB_Temp_UserZhuanYe_NoUser",
                                 list=[{"user_code": uu_Code, "type": "time out"}])
                    continue
            div=bsObj.find(id="regcert_tab")
            if div is None:
                continue
            dls=div.findAll(name="dl")
            i = 0
            for dl in dls:
                #开始遍历一家公司的人员
                obj={}
                dds=dl.findAll(name="dd");
                lenth_dd=len(dds) #dd的个数，5个有专业，4个没有专业
                if lenth_dd==0:
                    dbDAL.insert(tableName="Tab_ZJB_Temp_UserZhuanYe_NoUser",
                                 list=[{"user_code": uu_Code, "type": "no users"}])
                    break
                if lenth_dd < 4:
                    continue
                obj["uzy_User_Code"]=uu_Code
                #第一个dd
                value=dds[0].get_text();
                valueArr=value.split("：")
                if(len(valueArr)==2):
                    obj["uzy_ZiGeZheng"]=valueArr[1].strip()

                #第二个dd
                value = dds[1].get_text();
                valueArr =  value.split("：")
                if (len(valueArr) == 2):
                    if lenth_dd==4:
                        obj["uzy_ZhengShuBianHao"] = valueArr[1].strip()
                    elif lenth_dd==5:
                        obj["uzy_ZhuanYe"]=valueArr[1].strip()

                # 第三个dd
                value = dds[2].get_text();
                valueArr = value.split("：")
                if (len(valueArr) == 2):
                    if lenth_dd == 4: #没有专业
                        obj["uzy_YinZhangHao"] = valueArr[1].strip()
                    elif lenth_dd == 5: #有专业
                        obj["uzy_ZhengShuBianHao"] = valueArr[1].strip()

                # 第四个dd
                value = dds[3].get_text();
                valueArr = value.split("：")
                if (len(valueArr) == 2):
                    if lenth_dd == 4:  # 没有专业
                        obj["uzy_YouXiaoQi"] = valueArr[1].strip()
                    elif lenth_dd == 5:  # 有专业
                        obj["uzy_YinZhangHao"] = valueArr[1].strip()

                if lenth_dd==5:
                    # 第五个dd
                    value = dds[4].get_text();
                    valueArr = value.split("：")
                    if (len(valueArr) == 2):
                        obj["uzy_YouXiaoQi"] = valueArr[1].strip()

                resultList.append(obj)
                print "len={2} {1} {0} {3}  ".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                                               uu_Name, len(resultList)+(num*100),obj["uzy_ZiGeZheng"]).decode("utf8")
                i+=1
                # 存数据库，每100条存一次
                if len(resultList)==100:
                    print "{0} 开始入库....... ".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))).decode("utf8")
                    dbDAL.insert(tableName="Tab_ZJB_LiuShui_User_ZhuanYe", list=resultList)
                    resultList=[]
                    num+=1
                # try:
                #     if len(tr.findAll(name="td"))<=1 and i==0 :
                #         #没有人员。
                #         print "没有注册资格证，跳过,uu_Code={0}".format(uu_Code).decode("utf8")
                #         dbDAL.insert(tableName="Tab_ZJB_Temp_UserZhuanYe_NoUser", list=[{"user_code":uu_Code,"type":"no users"}])
                #         break
                #     obj["uu_Company_Code"]=uu_Code
                # except ValueError, Argument:
                #     print Argument
                #     continue
                # uid=""
                # try:
                #     onclicks=tr.find(name="td",attrs={"data-header":"姓名"}).find(name="a").attrs["onclick"].split("/")
                #     uid=onclicks[len(onclicks)-1].replace("'","")   ## 去掉最后的单引号
                # except Exception as e:
                #     print e.message
                # obj["uu_Code"] = uid
                # for key in getJson.keys():
                #     value=getJson[key]
                #     td=tr.find(name="td",attrs={"data-header":key})
                #     name =""
                #     if td is not None:
                #         name = td.get_text().strip()
                #         name=name.decode("utf8")
                #     else:
                #         name = list[i][value]
                #     obj[value]=name
                # resultList.append(obj)
                # print "{0} {1} len={2}".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
                #                                obj["uu_Name"], len(resultList)+(num*100)).decode("utf8")
                # i+=1
                # # 存数据库，每100条存一次
                # if len(resultList)==100:
                #     print "{0} 开始入库....... ".format(time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))).decode("utf8")
                #     dbDAL.insert(tableName="Tab_ZJB_LiuShui_User", list=resultList)
                #     resultList=[]
                #     num+=1

        dbDAL.insert(tableName="Tab_ZJB_LiuShui_User_ZhuanYe", list=resultList)

    except Exception as e:
        print "错误：{0}".format(e.message).decode("utf8")
    else:
        print "+++++++++++++++++++++++++ 成功！".decode("utf8")
    finally:
        # 销毁
        dbDAL.dispose()





if __name__=="__main__":
    main()