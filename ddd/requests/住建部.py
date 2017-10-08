# coding=UTF-8
from bs4 import BeautifulSoup
import sys
sys.path.append("..")
import DataBase.DatabaseDAL
import requests
reload(sys)   #解决乱码问题
sys.setdefaultencoding('utf8')  #解决乱码问题

params={'apt_code':'','qy_region':'510000','qy_fr_name':'','qy_reg_addr':'四川省','$reload':'0','qy_type':'QY_ZZ_ZZZD_001','qy_name':'','apt_scope':'','apt_certno':''}
params['$pg']=1         ## 页码（需要改）
params['$pgsz']=15    ## 每页显示记录数（需要改,之前改的7000）
params['$total']=18105  ## 总记录数（需要改）

r= requests.post("http://jzsc.mohurd.gov.cn/dataservice/query/comp/list", data=params)
bsObj=BeautifulSoup(r.text,"html.parser")
tbody=bsObj.find(name="tbody",attrs={"class":"cursorDefault"})
print r.text
trs=tbody.findAll(name="tr")
print "*"*100
print "len={0}".format(len(trs))
list=[];
for tr in trs:
    json = {}
    for td in tr.findAll(name="td"):
        try:
            dataHeader=td.attrs["data-header"]
        except Exception as e:
            continue
        value=td.get_text().strip();
        if dataHeader=='企业名称':
            a=td.find(name="a")
            if a is not None:
                json["co_Href"] = a.attrs["href"]
                hrefs=json["co_Href"].split("/")
                json["co_Company_Code"] = hrefs[len(hrefs)-1]
            json["co_QiYeMingCheng"]=value
        elif dataHeader=="企业法定代表人":
            json["co_FaRen"] = value
        elif dataHeader=="企业注册属地":
            json["co_ZhuCeDi"] = value
        elif dataHeader=="统一社会信用代码":
            json["co_XinYongCode"] = value

    list.append(json)
# for ins in list:
#     print ins

obj=DataBase.DatabaseDAL.DatabaseDAL()
n=obj.insert("Tab_ZJB_Company_Temp2",list)
obj.dispose()