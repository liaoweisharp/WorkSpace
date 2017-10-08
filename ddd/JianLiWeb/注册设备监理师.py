# coding=UTF-8
import sys
import requests
import time
from selenium import webdriver
from bs4 import BeautifulSoup
import traceback
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题
sys.path.append("..")
import DataBase.DatabaseDAL
import ddd.JianLiWeb.global_Vars

def main():

    try:
        ##需要改数据库名

        dbDAL = DataBase.DatabaseDAL.DatabaseDAL(database=ddd.JianLiWeb.global_Vars.global_DataBase)


        list = dbDAL.query("    SELECT ec_Name FROM Tab_Excel_Company WHERE ec_Name NOT in (SELECT company FROM dbo.Tab_Excel_LiuShui_SheBeiShi) ORDER BY ec_Name")
        # ## 先清空数
        # dbDAL.execute("TRUNCATE TABLE Tab_Excel_LiuShui_SheBeiShi")
        driver = webdriver.Firefox(executable_path="D:\Python27\WorkSpace\ddd\geckodriver.exe")
        url = 'http://www.capec.org.cn/ca/search_zhuce.aspx'



        # # 获取cookie信息并打印
        # cookie = driver.get_cookies()
        # print cookie
        # print "*" * 20
        # time.sleep(2)
      #  print driver.page_source


        pageNum=1;
        companyList=[]
        while len(list)>=pageNum:
            # time.sleep(random.randint(2,5))
            (companyName,)=list[pageNum-1]
            # if pageNum==1:
            #     companyName="中铁华铁工程设计集团有限公司"
            # elif pageNum==2:
            #     companyName = "黄河勘测规划设计有限公司"


            try:
                # 通过用户名密码登陆
                driver.get(url)

                time.sleep(3)
                # driver.maximize_window()  # 浏览器全屏显示

                driver.find_element_by_id("searchkeyword").send_keys(companyName.decode("utf8"))
                driver.find_element_by_id("Button1").click()
                time.sleep(2)
                bsObj = BeautifulSoup(driver.page_source, "html.parser")

            except Exception as e:
                print e.message
                print "超时，等待1分钟,companyName={0}".format(companyName).decode("utf8")
                time.sleep(60)
                try:
                    driver.find_element_by_id("searchkeyword").send_keys(companyName.decode("utf8"))
                    driver.find_element_by_id("Button1").click()
                    time.sleep(2)
                    bsObj = BeautifulSoup(driver.page_source, "html.parser")

                except Exception as e:
                    print e.message
                    print "再超时，companyName={0}".format(companyName).decode("utf8")
                    continue
            else:
                objList=[]
                objList.extend(getObj(bsObj))
                try:
                    GridView1=bsObj.find(id="GridView1")
                    right=GridView1.find(name="tr", attrs={"align": "right"})
                    table=right.find(name="table")
                    tr=table.find(name="tr")
                    ttt = tr.findAll(name="td")
                    pagesNode = tr.findAll(name="a")
                except:
                    pass
                else:
                    for index in range(2,len(pagesNode)+2): ##从1开始
                        xpath="//*[@id='GridView1']//tr[@align='right']//table//td[{0}]/a".format(index)
                        driver.find_element_by_xpath(xpath).click()
                        time.sleep(2)
                        bsObj = BeautifulSoup(driver.page_source, "html.parser")
                        objList.extend(getObj(bsObj))

                finally:
                    ## 再插入数据表
                    if len(objList) > 0:
                        dbDAL.insert(tableName="Tab_Excel_LiuShui_SheBeiShi", list=objList)
                    pageNum += 1


            # dbDAL.update("Tab_BX_LiuShui_NewProject",companyList,("project_Code",))




    except Exception as e:
        traceback.print_exc()
    finally:
        dbDAL.dispose()
        driver.close()

def getObj(bsObj):
    '''
    爬取数据
    :param bsObj: 
    :return: 
    '''
    objList=[]
    try:
        trNodes=bsObj.find(id="GridView1").findAll(name="tr")
    except:
        pass
    else:
        for tr in trNodes[1:len(trNodes)]:
            tdsNodes=tr.findAll(name="td")
            if len(tdsNodes)<10:  ##小于10列就是分页行
                #分页行
                break
            obj={}
            objList.append(obj)
            obj["userName"]=tdsNodes[1].get_text().strip()
            obj["zhengShu"] = tdsNodes[4].get_text().strip()
            obj["company"] = tdsNodes[2].get_text().strip()
            obj["youXiaoQi"] = tdsNodes[7].get_text().strip()
            obj["zhiCheng"] = tdsNodes[8].get_text().strip()
    return objList
if __name__=="__main__":
    main()